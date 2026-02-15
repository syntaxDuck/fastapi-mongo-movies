"""
Admin API routes for utility endpoints including poster validation.
"""

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Query

from ...core.config import settings
from ...core.database import DatabaseManager
from ...core.exceptions import NotFoundError
from ...core.logging import get_logger
from ...core.metrics import get_metrics as get_db_metrics
from ...core.request_metrics import get_request_metrics
from ...core.security import verify_admin_api_key
from ...schemas import (
    JobResponse,
    JobStatus,
    ValidationResult,
    ValidationStats,
)
from ...schemas.movie import MovieResponse
from ...services.job_management_service import JobManagementService
from ...services.poster_validation_service import PosterValidationService

logger = get_logger(__name__)

_poster_validation_service: PosterValidationService | None = None
_job_management_service: JobManagementService | None = None


def _get_poster_validation_service() -> PosterValidationService:
    global _poster_validation_service
    if _poster_validation_service is None:
        _poster_validation_service = PosterValidationService()
    return _poster_validation_service


def _get_job_management_service() -> JobManagementService:
    global _job_management_service
    if _job_management_service is None:
        _job_management_service = JobManagementService()
    return _job_management_service


router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(verify_admin_api_key)])


async def get_poster_validation_service() -> PosterValidationService:
    """Dependency to get poster validation service instance."""
    return _get_poster_validation_service()


async def get_job_management_service() -> JobManagementService:
    """Dependency to get job management service instance."""
    return _get_job_management_service()


@router.get("/health")
async def health_check() -> dict[str, Any]:
    logger.debug("Health check requested")
    pool_status = await DatabaseManager.get_pool_status()
    return {
        "status": "healthy",
        "service": "FastAPI Backend",
        "version": settings.__VERSION__,
        "database_pool": pool_status,
    }


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
):
    """
    Start poster validation background job.

    - **batch_size**: Number of movies to process per batch (default: 100)
    - **concurrent_requests**: Number of concurrent HTTP requests (default: 10)
    - **update_database**: Whether to update valid_poster field (default: True)
    """
    poster_service = _get_poster_validation_service()
    job_service = _get_job_management_service()
    logger.info(
        f"Starting poster validation job with batch_size={batch_size}, concurrent_requests={concurrent_requests}"
    )

    job_id = await job_service.create_job(
        job_type="poster_validation",
        parameters={
            "batch_size": batch_size,
            "concurrent_requests": concurrent_requests,
            "update_database": update_database,
        },
    )

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
        created_at=datetime.now(UTC),
    )


@router.get("/movies/validate-posters/statistics", response_model=ValidationStats)
async def get_validation_statistics():
    poster_service = _get_poster_validation_service()
    """
    Get comprehensive poster validation statistics.
    """
    logger.info("Getting poster validation statistics")

    stats = await poster_service.get_validation_statistics()
    return stats


@router.get("/movies/validate-posters/{job_id}", response_model=JobStatus)
async def get_validation_status(
    job_id: str,
):
    """
    Get poster validation job status and progress.

    - **job_id**: Unique job identifier returned by start endpoint
    """
    job_service = _get_job_management_service()
    logger.info(f"Getting validation job status: {job_id}")

    job_status = await job_service.get_job_status(job_id)

    if not job_status:
        logger.warning(f"Validation job not found: {job_id}")
        raise NotFoundError("Validation job not found")

    return job_status


@router.post("/movies/{movie_id}/validate-poster", response_model=ValidationResult)
async def validate_single_poster(
    movie_id: str,
):
    """
    Validate poster for specific movie.

    - **movie_id**: Movie ID to validate poster for
    """
    poster_service = _get_poster_validation_service()
    logger.info(f"Validating poster for movie: {movie_id}")

    result = await poster_service.validate_movie_poster(movie_id)

    if not result:
        logger.warning(f"Movie not found for poster validation: {movie_id}")
        raise NotFoundError("Movie not found")

    return result


# TODO: Could probably add pagination here
@router.get("/movies/validate-posters/invalid", response_model=list[MovieResponse])
async def get_invalid_posters(
    limit: int = Query(50, ge=1, le=500, description="Maximum number of results to return"),
):
    """
    Get list of movies with invalid posters.

    - **limit**: Maximum number of results to return (default: 50)
    """
    poster_service = _get_poster_validation_service()
    logger.info(f"Getting movies with invalid posters (limit: {limit})")

    invalid_movies = await poster_service.get_invalid_posters(limit=limit)
    return invalid_movies


@router.post("/movies/validate-posters/revalidate/{movie_id}")
async def revalidate_movie_poster(
    movie_id: str,
):
    """
    Revalidate poster for specific movie and update database.

    - **movie_id**: Movie ID to revalidate poster for
    """
    poster_service = _get_poster_validation_service()
    logger.info(f"Revalidating poster for movie: {movie_id}")

    result = await poster_service.revalidate_movie_poster(movie_id)

    if not result:
        logger.warning(f"Movie not found for revalidation: {movie_id}")
        raise NotFoundError("Movie not found")

    return {
        "message": f"Poster revalidation completed for movie {movie_id}",
        "result": result,
    }


@router.delete("/jobs/{job_id}")
async def cancel_job(
    job_id: str,
):
    """
    Cancel a running background job.

    - **job_id**: Job ID to cancel
    """
    job_service = _get_job_management_service()
    logger.info(f"Cancelling job: {job_id}")

    success = await job_service.cancel_job(job_id)

    if not success:
        logger.warning(f"Job not found or cannot be cancelled: {job_id}")
        raise NotFoundError(f"Job id: {job_id} not found or cannot be cancelled")

    return {"message": f"Job {job_id} cancelled successfully"}


@router.get("/db-stats")
async def get_database_stats():
    """
    Get database operation statistics and metrics.

    Returns aggregated metrics for database operations including:
    - Total operations in the last hour and 24 hours
    - Operations by type (find, insert, update, delete, distinct)
    - Operations by collection
    - Average query duration
    - Recent operation details
    """
    logger.info("Getting database statistics")

    metrics = get_db_metrics()

    return {
        "summary": metrics.get_summary(),
        "recent_operations": metrics.get_recent_operations(limit=50),
    }


@router.delete("/db-stats")
async def reset_database_stats():
    """
    Reset all database statistics and metrics.
    """
    logger.info("Resetting database statistics")

    metrics = get_db_metrics()
    metrics.reset()

    return {"message": "Database statistics reset successfully"}


@router.get("/request-metrics")
async def get_request_metrics_stats():
    """
    Get HTTP request statistics and metrics.

    Returns aggregated metrics for HTTP requests including:
    - Total requests in the last hour and 24 hours
    - Unique IPs making requests
    - Blocked requests count
    - Requests by endpoint
    - Top IPs by request volume
    """
    logger.info("Getting request metrics")

    metrics = get_request_metrics()

    return {
        "summary": metrics.get_summary(),
        "top_ips": metrics.get_top_ips(limit=20),
        "recent_requests": metrics.get_recent_requests(limit=50),
    }


@router.get("/request-metrics/ip/{ip}")
async def get_request_metrics_by_ip(ip: str):
    """
    Get detailed metrics for a specific IP address.
    """
    logger.info(f"Getting request metrics for IP: {ip}")

    metrics = get_request_metrics()
    details = metrics.get_ip_details(ip)

    if not details:
        raise NotFoundError(f"No metrics found for IP: {ip}")

    return details


@router.get("/request-metrics/blocked")
async def get_blocked_ips():
    """
    Get list of IPs with blocked requests.
    """
    logger.info("Getting blocked IPs")

    metrics = get_request_metrics()
    return {"blocked_ips": metrics.get_blocked_ips()}


@router.delete("/request-metrics")
async def reset_request_metrics():
    """
    Reset all request metrics.
    """
    logger.info("Resetting request metrics")

    metrics = get_request_metrics()
    metrics.reset()

    return {"message": "Request metrics reset successfully"}
