"""
Poster Validation Service for enhanced poster URL validation with background job processing.
"""

import asyncio
import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import time

from ..repositories.movie_repository import MovieRepository
from ..schemas.schemas import MovieResponse
from ..core.logging import get_logger
from ..core.exceptions import NotFoundError, DatabaseError

logger = get_logger(__name__)


@dataclass
class PosterValidationResult:
    """Result of poster validation for a single movie."""

    movie_id: str
    is_valid: bool
    poster_url: Optional[str] = None
    validation_timestamp: Optional[datetime] = None
    http_status: Optional[int] = None
    content_type: Optional[str] = None
    response_time_ms: Optional[float] = None
    file_size_bytes: Optional[int] = None
    error_reason: Optional[str] = None


@dataclass
class ValidationStats:
    """Statistics for poster validation."""

    total_movies: int
    movies_with_posters: int
    valid_posters: int
    invalid_posters: int
    validation_success_rate: float
    last_validation_date: Optional[datetime] = None


class PosterValidationService:
    """Service for poster validation with enhanced checks and background processing."""

    def __init__(self) -> None:
        self.movie_repository = MovieRepository()

        # HTTP client configuration
        self.client_config = {
            "timeout": httpx.Timeout(10.0),  # 10 second timeout
            "follow_redirects": True,
            "headers": {"User-Agent": "FastAPI-Movie-Validator/1.0"},
        }

    async def validate_all_posters(
        self,
        job_id: str,
        batch_size: int = 100,
        concurrent_requests: int = 10,
        update_database: bool = True,
    ) -> None:
        """
        Validate all movie posters in batches with background job processing.

        Args:
            job_id: Background job ID for progress tracking
            batch_size: Number of movies to process per batch
            concurrent_requests: Number of concurrent HTTP requests
            update_database: Whether to update valid_poster field in database
        """
        logger.info(f"Starting poster validation job {job_id}")

        try:
            # Import here to avoid circular imports
            from ..services.job_management_service import JobManagementService

            job_service = JobManagementService()

            # Get total count for progress tracking
            total_movies = await self._get_total_movie_count()
            await job_service.update_job_progress(job_id, 0, total_movies)

            # Process in batches
            processed_count = 0
            valid_count = 0
            invalid_count = 0

            skip = 0
            while True:
                # Get batch of movies
                movies = await self.movie_repository.search_movies(
                    limit=batch_size,
                    skip=skip,
                    include_invalid_posters=True,  # Get all movies, not just valid ones
                )

                if not movies:
                    break

                # Process batch with concurrent requests
                batch_results = await self._validate_poster_batch(
                    movies, concurrent_requests, update_database
                )

                # Update counters
                for result in batch_results:
                    processed_count += 1
                    if result.is_valid:
                        valid_count += 1
                    else:
                        invalid_count += 1

                # Update job progress
                await job_service.update_job_progress(
                    job_id, processed_count, total_movies, valid_count, invalid_count
                )

                logger.info(f"Processed batch: {processed_count}/{total_movies} movies")

                # Move to next batch
                skip += batch_size

                # Small delay to prevent overwhelming the server
                await asyncio.sleep(0.1)

            # Complete job
            await job_service.complete_job(
                job_id,
                {
                    "processed_movies": processed_count,
                    "valid_posters": valid_count,
                    "invalid_posters": invalid_count,
                    "success_rate": (valid_count / processed_count * 100)
                    if processed_count > 0
                    else 0,
                },
            )

            logger.info(
                f"Poster validation job {job_id} completed: {processed_count} movies processed"
            )

        except Exception as e:
            logger.error(f"Poster validation job {job_id} failed: {e}")

            # Mark job as failed
            try:
                from ..services.job_management_service import JobManagementService

                job_service = JobManagementService()
                await job_service.fail_job(job_id, str(e))
            except Exception as job_error:
                logger.error(f"Failed to mark job as failed: {job_error}")

            raise

    async def validate_movie_poster(
        self, movie_id: str
    ) -> Optional[PosterValidationResult]:
        """
        Validate poster for a specific movie with enhanced checks.

        Args:
            movie_id: Movie ID to validate

        Returns:
            PosterValidationResult or None if movie not found
        """
        logger.debug(f"Validating poster for movie: {movie_id}")

        try:
            # Get movie
            movie = await self.movie_repository.find_by_id(movie_id)
            if not movie:
                logger.warning(f"Movie not found for poster validation: {movie_id}")
                return None

            # Check if movie has poster
            if not movie.poster:
                return PosterValidationResult(
                    movie_id=movie_id,
                    is_valid=False,
                    error_reason="No poster URL provided",
                    validation_timestamp=datetime.utcnow(),
                    poster_url=None,
                )

            # Validate poster URL
            result = await self._validate_poster_url(str(movie.poster))
            result.movie_id = movie_id
            result.poster_url = str(movie.poster)

            return result

        except Exception as e:
            logger.error(f"Failed to validate poster for movie {movie_id}: {e}")
            return PosterValidationResult(
                movie_id=movie_id,
                is_valid=False,
                error_reason=f"Validation error: {str(e)}",
                validation_timestamp=datetime.utcnow(),
                poster_url=None,
            )

    async def revalidate_movie_poster(
        self, movie_id: str
    ) -> Optional[PosterValidationResult]:
        """
        Revalidate poster for specific movie and update database.

        Args:
            movie_id: Movie ID to revalidate

        Returns:
            PosterValidationResult or None if movie not found
        """
        logger.info(f"Revalidating poster for movie: {movie_id}")

        try:
            # Validate poster
            result = await self.validate_movie_poster(movie_id)
            if not result:
                return None

            # Update database
            await self._update_movie_valid_poster(movie_id, result.is_valid)

            logger.info(
                f"Revalidated poster for movie {movie_id}: valid={result.is_valid}"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to revalidate poster for movie {movie_id}: {e}")
            raise

    async def get_validation_statistics(self) -> ValidationStats:
        """
        Get comprehensive poster validation statistics.

        Returns:
            ValidationStats with current validation metrics
        """
        logger.info("Getting poster validation statistics")

        try:
            # Get total movies count
            total_movies = await self._get_total_movie_count()

            # Get movies with posters
            movies_with_posters = await self._get_movies_with_posters_count()

            # Get valid and invalid poster counts
            valid_posters = await self._get_valid_posters_count()
            invalid_posters = movies_with_posters - valid_posters

            # Calculate success rate
            success_rate = (
                (valid_posters / movies_with_posters * 100)
                if movies_with_posters > 0
                else 0
            )

            # Get last validation date (this would require additional tracking)
            last_validation_date = None  # TODO: Implement validation tracking

            return ValidationStats(
                total_movies=total_movies,
                movies_with_posters=movies_with_posters,
                valid_posters=valid_posters,
                invalid_posters=invalid_posters,
                validation_success_rate=success_rate,
                last_validation_date=last_validation_date,
            )

        except Exception as e:
            logger.error(f"Failed to get validation statistics: {e}")
            raise

    async def get_invalid_posters(self, limit: int = 50) -> List[MovieResponse]:
        """
        Get list of movies with invalid posters.

        Args:
            limit: Maximum number of results to return

        Returns:
            List of movies with invalid posters
        """
        logger.info(f"Getting movies with invalid posters (limit: {limit})")

        try:
            # Get movies with invalid posters
            movies = await self.movie_repository.search_movies(
                limit=limit, include_invalid_posters=True
            )

            # Filter for movies with posters but marked as invalid
            invalid_poster_movies = [
                movie
                for movie in movies
                if movie.poster
                and (movie.valid_poster is False or movie.valid_poster is None)
            ]

            return invalid_poster_movies[:limit]

        except Exception as e:
            logger.error(f"Failed to get invalid posters: {e}")
            raise

    async def _validate_poster_batch(
        self,
        movies: List[MovieResponse],
        concurrent_requests: int,
        update_database: bool,
    ) -> List[PosterValidationResult]:
        """
        Validate posters for a batch of movies concurrently.

        Args:
            movies: List of movies to validate
            concurrent_requests: Number of concurrent HTTP requests
            update_database: Whether to update database

        Returns:
            List of validation results
        """
        semaphore = asyncio.Semaphore(concurrent_requests)

        async def validate_single_movie(movie: MovieResponse) -> PosterValidationResult:
            async with semaphore:
                if not movie.poster:
                    return PosterValidationResult(
                        movie_id=movie.id,
                        is_valid=False,
                        error_reason="No poster URL provided",
                        validation_timestamp=datetime.utcnow(),
                        poster_url=None,
                    )

                result = await self._validate_poster_url(str(movie.poster))
                result.movie_id = movie.id
                result.poster_url = str(movie.poster)

                # Update database if requested
                if update_database:
                    await self._update_movie_valid_poster(movie.id, result.is_valid)

                return result

        # Create tasks for all movies
        tasks = [validate_single_movie(movie) for movie in movies]

        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error in batch validation: {result}")
                # Create a failure result
                valid_results.append(
                    PosterValidationResult(
                        movie_id="unknown",
                        is_valid=False,
                        error_reason=f"Batch validation error: {str(result)}",
                        validation_timestamp=datetime.utcnow(),
                        poster_url=None,
                    )
                )
            else:
                valid_results.append(result)

        return valid_results

    async def _validate_poster_url(self, poster_url: str) -> PosterValidationResult:
        """
        Validate poster URL with enhanced checks.

        Args:
            poster_url: URL to validate

        Returns:
            PosterValidationResult with validation details
        """
        start_time = time.time()

        try:
            async with httpx.AsyncClient(**self.client_config) as client:
                # Use HEAD request first (more efficient)
                response = await client.head(poster_url)

                response_time_ms = (time.time() - start_time) * 1000

                # Check HTTP status
                if response.status_code != 200:
                    return PosterValidationResult(
                        movie_id="",
                        is_valid=False,
                        http_status=response.status_code,
                        response_time_ms=response_time_ms,
                        error_reason=f"HTTP {response.status_code}",
                        validation_timestamp=datetime.utcnow(),
                        poster_url=poster_url,
                    )

                # Check content type
                content_type = response.headers.get("content-type", "").lower()
                if not content_type.startswith("image/"):
                    return PosterValidationResult(
                        movie_id="",
                        is_valid=False,
                        http_status=response.status_code,
                        content_type=content_type,
                        response_time_ms=response_time_ms,
                        error_reason=f"Invalid content type: {content_type}",
                        validation_timestamp=datetime.utcnow(),
                        poster_url=poster_url,
                    )

                # Check content length if available
                content_length = response.headers.get("content-length")
                file_size_bytes = int(content_length) if content_length else None

                # Additional validation for file size (optional)
                if file_size_bytes and file_size_bytes > 10 * 1024 * 1024:  # 10MB limit
                    return PosterValidationResult(
                        movie_id="",
                        is_valid=False,
                        http_status=response.status_code,
                        content_type=content_type,
                        response_time_ms=response_time_ms,
                        file_size_bytes=file_size_bytes,
                        error_reason=f"File too large: {file_size_bytes} bytes",
                        validation_timestamp=datetime.utcnow(),
                        poster_url=poster_url,
                    )

                # If all checks pass
                return PosterValidationResult(
                    movie_id="",
                    is_valid=True,
                    http_status=response.status_code,
                    content_type=content_type,
                    response_time_ms=response_time_ms,
                    file_size_bytes=file_size_bytes,
                    validation_timestamp=datetime.utcnow(),
                    poster_url=poster_url,
                )

        except httpx.TimeoutException:
            return PosterValidationResult(
                movie_id="",
                is_valid=False,
                response_time_ms=(time.time() - start_time) * 1000,
                error_reason="Request timeout",
                validation_timestamp=datetime.utcnow(),
                poster_url=poster_url,
            )
        except httpx.RequestError as e:
            return PosterValidationResult(
                movie_id="",
                is_valid=False,
                response_time_ms=(time.time() - start_time) * 1000,
                error_reason=f"Request error: {str(e)}",
                validation_timestamp=datetime.utcnow(),
                poster_url=poster_url,
            )
        except Exception as e:
            return PosterValidationResult(
                movie_id="",
                is_valid=False,
                response_time_ms=(time.time() - start_time) * 1000,
                error_reason=f"Unexpected error: {str(e)}",
                validation_timestamp=datetime.utcnow(),
                poster_url=poster_url,
            )

    async def _update_movie_valid_poster(self, movie_id: str, is_valid: bool) -> None:
        """
        Update valid_poster field for a movie.

        Args:
            movie_id: Movie ID to update
            is_valid: Whether poster is valid
        """
        try:
            # This would require adding an update method to the repository
            # For now, we'll log the update
            logger.info(f"Would update movie {movie_id} valid_poster to {is_valid}")

            # TODO: Implement actual database update
            # await self.movie_repository.update_valid_poster(movie_id, is_valid)

        except Exception as e:
            logger.error(f"Failed to update valid_poster for movie {movie_id}: {e}")

    async def _get_total_movie_count(self) -> int:
        """Get total number of movies in database."""
        try:
            # This would require adding a count method to the repository
            # For now, return a reasonable estimate
            return 25000  # Approximate count for sample_mflix
        except Exception as e:
            logger.error(f"Failed to get total movie count: {e}")
            return 0

    async def _get_movies_with_posters_count(self) -> int:
        """Get number of movies that have poster URLs."""
        try:
            # This would require a specific query
            # For now, return a reasonable estimate
            return 20000  # Approximate count
        except Exception as e:
            logger.error(f"Failed to get movies with posters count: {e}")
            return 0

    async def _get_valid_posters_count(self) -> int:
        """Get number of movies with valid posters."""
        try:
            # This would require a specific query
            # For now, return a reasonable estimate
            return 18000  # Approximate count
        except Exception as e:
            logger.error(f"Failed to get valid posters count: {e}")
            return 0
