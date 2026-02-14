from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


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
