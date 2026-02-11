"""
Request logging middleware for API requests.
"""

import time
from fastapi import Request, Response
from typing import Callable
from .logging import get_logger

logger = get_logger(__name__)


async def log_requests(request: Request, call_next: Callable) -> Response:
    """
    Middleware to log incoming HTTP requests and responses.
    """
    start_time = time.time()

    # Log request details
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Client: {request.client.host if request.client else 'unknown'} - "
        f"User-Agent: {request.headers.get('user-agent', 'unknown')}"
    )

    # Process the request
    try:
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response details
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {process_time:.3f}s - "
            f"Size: {len(response.body) if hasattr(response, 'body') else 'unknown'} bytes"
        )

        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"{request.method} {request.url.path} - "
            f"Error: {str(e)} - "
            f"Duration: {process_time:.3f}s"
        )
        raise
