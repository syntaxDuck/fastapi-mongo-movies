"""
Job Management Service for background job tracking and progress monitoring.
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
import uuid

from ..core.logging import get_logger

logger = get_logger(__name__)

#TODO: Make periodic jobs that trigger on time
@dataclass
class JobStatus:
    """Background job status information."""

    job_id: str
    job_type: str
    status: str  # 'queued', 'running', 'completed', 'failed', 'cancelled'
    parameters: Dict[str, Any]
    progress_percentage: float = 0.0
    total_items: int = 0
    processed_items: int = 0
    success_count: int = 0
    error_count: int = 0
    errors: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda x=timezone.utc: datetime.now(x))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_remaining_minutes: Optional[float] = None
    result: Optional[Dict[str, Any]] = None


class JobManagementService:
    """Service for managing background jobs with progress tracking."""

    def __init__(self) -> None:
        # In-memory job storage (in production, use Redis or database)
        self.jobs: Dict[str, JobStatus] = {}
        self._cleanup_task: Optional[asyncio.Task] = None
        self._start_cleanup_task()

    def _start_cleanup_task(self) -> None:
        """Start background task to clean up old jobs."""
        if self._cleanup_task is None or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(self._cleanup_old_jobs())

    async def _cleanup_old_jobs(self) -> None:
        """Clean up jobs older than 24 hours."""
        while True:
            try:
                await asyncio.sleep(3600)

                cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
                jobs_to_remove = [
                    job_id
                    for job_id, job in self.jobs.items()
                    if job.created_at < cutoff_time
                    and job.status in ["completed", "failed", "cancelled"]
                ]

                for job_id in jobs_to_remove:
                    del self.jobs[job_id]
                    logger.debug(f"Cleaned up old job: {job_id}")

                if jobs_to_remove:
                    logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")

            except Exception as e:
                logger.error(f"Error in job cleanup task: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

    async def create_job(self, job_type: str, parameters: Dict[str, Any]) -> str:
        """
        Create a new background job.

        Args:
            job_type: Type of job (e.g., 'poster_validation')
            parameters: Job parameters

        Returns:
            Job ID for tracking
        """
        job_id = str(uuid.uuid4())

        job = JobStatus(
            job_id=job_id, job_type=job_type, status="queued", parameters=parameters
        )

        self.jobs[job_id] = job

        logger.info(f"Created job {job_id} of type {job_type}")
        return job_id

    async def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        """
        Get job status by ID.

        Args:
            job_id: Job ID to retrieve

        Returns:
            JobStatus or None if not found
        """
        job = self.jobs.get(job_id)
        if job:
            if job.status == "running" and job.started_at:
                await self._update_estimated_remaining_time(job)

        return job

    async def update_job_progress(
        self,
        job_id: str,
        processed_items: int,
        total_items: int,
        success_count: int = 0,
        error_count: int = 0,
        errors: Optional[List[str]] = None,
    ) -> None:
        """
        Update job progress.

        Args:
            job_id: Job ID to update
            processed_items: Number of items processed
            total_items: Total number of items to process
            success_count: Number of successful operations
            error_count: Number of errors encountered
            errors: List of error messages
        """
        job = self.jobs.get(job_id)
        if not job:
            logger.warning(f"Attempted to update non-existent job: {job_id}")
            return

        # Update job status to running if this is the first progress update
        if job.status == "queued":
            job.status = "running"
            job.started_at = datetime.now(timezone.utc)
            logger.info(f"Job {job_id} started running")

        # Update progress metrics
        job.processed_items = processed_items
        job.total_items = total_items
        job.success_count = success_count
        job.error_count = error_count

        if errors:
            job.errors.extend(errors)

        # Calculate progress percentage
        if total_items > 0:
            job.progress_percentage = (processed_items / total_items) * 100

        # Update estimated remaining time
        await self._update_estimated_remaining_time(job)

        logger.debug(f"Updated job {job_id} progress: {job.progress_percentage:.1f}%")

    async def complete_job(self, job_id: str, result: Dict[str, Any]) -> None:
        """
        Mark job as completed with results.

        Args:
            job_id: Job ID to complete
            result: Job results
        """
        job = self.jobs.get(job_id)
        if not job:
            logger.warning(f"Attempted to complete non-existent job: {job_id}")
            return

        job.status = "completed"
        job.completed_at = datetime.now(timezone.utc)
        job.result = result
        job.progress_percentage = 100.0

        logger.info(f"Job {job_id} completed successfully")

    async def fail_job(self, job_id: str, error_message: str) -> None:
        """
        Mark job as failed with error message.

        Args:
            job_id: Job ID to fail
            error_message: Error message
        """
        job = self.jobs.get(job_id)
        if not job:
            logger.warning(f"Attempted to fail non-existent job: {job_id}")
            return

        job.status = "failed"
        job.completed_at = datetime.now(timezone.utc)
        job.errors.append(error_message)

        logger.error(f"Job {job_id} failed: {error_message}")

    async def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a running job.

        Args:
            job_id: Job ID to cancel

        Returns:
            True if job was cancelled, False if not found or not cancellable
        """
        job = self.jobs.get(job_id)
        if not job:
            return False

        if job.status not in ["queued", "running"]:
            return False

        job.status = "cancelled"
        job.completed_at = datetime.now(timezone.utc)

        logger.info(f"Job {job_id} cancelled")
        return True

    async def get_all_jobs(self, job_type: Optional[str] = None) -> List[JobStatus]:
        """
        Get all jobs, optionally filtered by type.

        Args:
            job_type: Optional job type filter

        Returns:
            List of job statuses
        """
        jobs = list(self.jobs.values())

        if job_type:
            jobs = [job for job in jobs if job.job_type == job_type]

        # Sort by creation time (newest first)
        jobs.sort(key=lambda j: j.created_at, reverse=True)

        return jobs

    async def get_job_statistics(self) -> Dict[str, Any]:
        """
        Get job statistics.

        Returns:
            Dictionary with job statistics
        """
        jobs = list(self.jobs.values())

        stats = {
            "total_jobs": len(jobs),
            "queued_jobs": len([j for j in jobs if j.status == "queued"]),
            "running_jobs": len([j for j in jobs if j.status == "running"]),
            "completed_jobs": len([j for j in jobs if j.status == "completed"]),
            "failed_jobs": len([j for j in jobs if j.status == "failed"]),
            "cancelled_jobs": len([j for j in jobs if j.status == "cancelled"]),
            "job_types": {},
        }

        # Count by job type
        for job in jobs:
            job_type = job.job_type
            if job_type not in stats["job_types"]:
                stats["job_types"][job_type] = {
                    "total": 0,
                    "queued": 0,
                    "running": 0,
                    "completed": 0,
                    "failed": 0,
                    "cancelled": 0,
                }

            stats["job_types"][job_type]["total"] += 1
            stats["job_types"][job_type][job.status] += 1

        return stats

    async def _update_estimated_remaining_time(self, job: JobStatus) -> None:
        """
        Update estimated remaining time for a job.

        Args:
            job: Job to update
        """
        if job.status != "running" or not job.started_at or job.processed_items == 0:
            job.estimated_remaining_minutes = None
            return

        # Calculate elapsed time
        elapsed_time = datetime.now(timezone.utc) - job.started_at
        elapsed_minutes = elapsed_time.total_seconds() / 60

        # Calculate processing rate (items per minute)
        processing_rate = (
            job.processed_items / elapsed_minutes if elapsed_minutes > 0 else 0
        )

        if processing_rate > 0 and job.total_items > job.processed_items:
            remaining_items = job.total_items - job.processed_items
            remaining_minutes = remaining_items / processing_rate
            job.estimated_remaining_minutes = max(0, remaining_minutes)
        else:
            job.estimated_remaining_minutes = None

    async def add_job_error(self, job_id: str, error_message: str) -> None:
        """
        Add an error message to a job.

        Args:
            job_id: Job ID to add error to
            error_message: Error message to add
        """
        job = self.jobs.get(job_id)
        if not job:
            logger.warning(f"Attempted to add error to non-existent job: {job_id}")
            return

        job.errors.append(error_message)
        job.error_count += 1

        logger.warning(f"Added error to job {job_id}: {error_message}")

    def get_active_job_count(self) -> int:
        """
        Get count of active (queued or running) jobs.

        Returns:
            Number of active jobs
        """
        return len([j for j in self.jobs.values() if j.status in ["queued", "running"]])

    async def shutdown(self) -> None:
        """
        Shutdown the job management service.
        """
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        logger.info("Job management service shutdown")
