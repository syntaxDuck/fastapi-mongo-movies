"""
Admin API routes for utility endpoints including poster validation.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from ...schemas.schemas import MovieResponse
from ...services.poster_validation_service import PosterValidationService
from ...services.job_management_service import JobManagementService
from ...core.logging import get_logger
from ...core.exceptions import NotFoundError, DatabaseError

logger = get_logger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])


# Response models
class JobResponse(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(
        ..., description="Job status: 'queued', 'running', 'completed', 'failed'"
    )
    message: str = Field(..., description="Job description or status message")
    created_at: datetime = Field(..., description="Job creation timestamp")


class JobStatus(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(
        ..., description="Job status: 'queued', 'running', 'completed', 'failed'"
    )
    progress_percentage: float = Field(..., description="Progress percentage (0-100)")
    total_movies: int = Field(..., description="Total number of movies to process")
    processed_movies: int = Field(..., description="Number of movies processed so far")
    valid_posters: int = Field(..., description="Number of valid posters found")
    invalid_posters: int = Field(..., description="Number of invalid posters found")
    errors: List[str] = Field(
        default_factory=list, description="List of errors encountered"
    )
    started_at: Optional[datetime] = Field(None, description="Job start timestamp")
    completed_at: Optional[datetime] = Field(
        None, description="Job completion timestamp"
    )
    estimated_remaining_minutes: Optional[float] = Field(
        None, description="Estimated time remaining in minutes"
    )


class ValidationResult(BaseModel):
    movie_id: str = Field(..., description="Movie ID")
    is_valid: bool = Field(..., description="Whether poster is valid")
    http_status: Optional[int] = Field(None, description="HTTP status code")
    content_type: Optional[str] = Field(None, description="Content type header")
    response_time_ms: Optional[float] = Field(
        None, description="Response time in milliseconds"
    )
    file_size_bytes: Optional[int] = Field(
        None, description="Estimated file size in bytes"
    )
    error_reason: Optional[str] = Field(
        None, description="Reason for validation failure"
    )
    validation_timestamp: datetime = Field(
        ..., description="When validation was performed"
    )


class ValidationStats(BaseModel):
    total_movies: int = Field(..., description="Total movies in database")
    movies_with_posters: int = Field(..., description="Movies that have poster URLs")
    valid_posters: int = Field(..., description="Movies with valid posters")
    invalid_posters: int = Field(..., description="Movies with invalid posters")
    last_validation_date: Optional[datetime] = Field(
        None, description="Last full validation date"
    )
    validation_success_rate: float = Field(
        ..., description="Percentage of posters that are valid"
    )


# Dependency injection
async def get_poster_validation_service() -> PosterValidationService:
    """Dependency to get poster validation service instance."""
    return PosterValidationService()


async def get_job_management_service() -> JobManagementService:
    """Dependency to get job management service instance."""
    return JobManagementService()


@router.post("/movies/validate-posters", response_model=JobResponse)
async def start_poster_validation(
    background_tasks: BackgroundTasks,
    batch_size: int = Query(
        100, ge=1, le=1000, description="Number of movies to process per batch"
    ),
    concurrent_requests: int = Query(
        10, ge=1, le=50, description="Number of concurrent HTTP requests"
    ),
    update_database: bool = Query(
        True, description="Whether to update valid_poster field in database"
    ),
    poster_service: PosterValidationService = Depends(get_poster_validation_service),
    job_service: JobManagementService = Depends(get_job_management_service),
):
    """
    Start poster validation background job.

    - **batch_size**: Number of movies to process per batch (default: 100)
    - **concurrent_requests**: Number of concurrent HTTP requests (default: 10)
    - **update_database**: Whether to update valid_poster field (default: True)
    """
    logger.info(
        f"Starting poster validation job with batch_size={batch_size}, concurrent_requests={concurrent_requests}"
    )

    try:
        # Create job
        job_id = await job_service.create_job(
            job_type="poster_validation",
            parameters={
                "batch_size": batch_size,
                "concurrent_requests": concurrent_requests,
                "update_database": update_database,
            },
        )

        # Start background task
        background_tasks.add_task(
            poster_service.validate_all_posters,
            job_id=job_id,
            batch_size=batch_size,
            concurrent_requests=concurrent_requests,
            update_database=update_database,
        )

        logger.info(f"Poster validation job started: {job_id}")

        return JobResponse(
            job_id=job_id,
            status="queued",
            message="Poster validation job queued and starting",
            created_at=datetime.utcnow(),
        )

    except Exception as e:
        logger.error(f"Failed to start poster validation job: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to start poster validation job"
        )


@router.get("/movies/validate-posters/{job_id}", response_model=JobStatus)
async def get_validation_status(
    job_id: str,
    job_service: JobManagementService = Depends(get_job_management_service),
):
    """
    Get poster validation job status and progress.

    - **job_id**: Unique job identifier returned by start endpoint
    """
    logger.info(f"Getting validation job status: {job_id}")

    try:
        job_status = await job_service.get_job_status(job_id)

        if not job_status:
            logger.warning(f"Validation job not found: {job_id}")
            raise HTTPException(status_code=404, detail="Validation job not found")

        return job_status

    except Exception as e:
        logger.error(f"Failed to get validation job status: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to get validation job status"
        )


@router.post("/movies/{movie_id}/validate-poster", response_model=ValidationResult)
async def validate_single_poster(
    movie_id: str,
    poster_service: PosterValidationService = Depends(get_poster_validation_service),
):
    """
    Validate poster for specific movie.

    - **movie_id**: Movie ID to validate poster for
    """
    logger.info(f"Validating poster for movie: {movie_id}")

    try:
        result = await poster_service.validate_movie_poster(movie_id)

        if not result:
            logger.warning(f"Movie not found for poster validation: {movie_id}")
            raise HTTPException(status_code=404, detail="Movie not found")

        return result

    except Exception as e:
        logger.error(f"Failed to validate poster for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate poster")


@router.get("/movies/validate-posters/statistics", response_model=ValidationStats)
async def get_validation_statistics(
    poster_service: PosterValidationService = Depends(get_poster_validation_service),
):
    """
    Get comprehensive poster validation statistics.
    """
    logger.info("Getting poster validation statistics")

    try:
        stats = await poster_service.get_validation_statistics()
        return stats

    except Exception as e:
        logger.error(f"Failed to get validation statistics: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to get validation statistics"
        )


@router.get("/movies/validate-posters/invalid", response_model=List[MovieResponse])
async def get_invalid_posters(
    limit: int = Query(
        50, ge=1, le=500, description="Maximum number of results to return"
    ),
    poster_service: PosterValidationService = Depends(get_poster_validation_service),
):
    """
    Get list of movies with invalid posters.

    - **limit**: Maximum number of results to return (default: 50)
    """
    logger.info(f"Getting movies with invalid posters (limit: {limit})")

    try:
        invalid_movies = await poster_service.get_invalid_posters(limit=limit)
        return invalid_movies

    except Exception as e:
        logger.error(f"Failed to get invalid posters: {e}")
        raise HTTPException(status_code=500, detail="Failed to get invalid posters")


@router.post("/movies/validate-posters/revalidate/{movie_id}")
async def revalidate_movie_poster(
    movie_id: str,
    poster_service: PosterValidationService = Depends(get_poster_validation_service),
):
    """
    Revalidate poster for specific movie and update database.

    - **movie_id**: Movie ID to revalidate poster for
    """
    logger.info(f"Revalidating poster for movie: {movie_id}")

    try:
        result = await poster_service.revalidate_movie_poster(movie_id)

        if not result:
            logger.warning(f"Movie not found for revalidation: {movie_id}")
            raise HTTPException(status_code=404, detail="Movie not found")

        return {
            "message": f"Poster revalidation completed for movie {movie_id}",
            "result": result,
        }

    except Exception as e:
        logger.error(f"Failed to revalidate poster for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to revalidate poster")


@router.delete("/jobs/{job_id}")
async def cancel_job(
    job_id: str,
    job_service: JobManagementService = Depends(get_job_management_service),
):
    """
    Cancel a running background job.

    - **job_id**: Job ID to cancel
    """
    logger.info(f"Cancelling job: {job_id}")

    try:
        success = await job_service.cancel_job(job_id)

        if not success:
            logger.warning(f"Job not found or cannot be cancelled: {job_id}")
            raise HTTPException(
                status_code=404, detail="Job not found or cannot be cancelled"
            )

        return {"message": f"Job {job_id} cancelled successfully"}

    except Exception as e:
        logger.error(f"Failed to cancel job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to cancel job")
