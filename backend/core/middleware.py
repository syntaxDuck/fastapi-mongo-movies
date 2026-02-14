"""
Request logging middleware for API requests.
"""

import time
from fastapi import Request, Response
from typing import Callable
from .logging import get_logger
from .rate_limiter import get_real_ip
from .request_metrics import get_request_metrics

logger = get_logger(__name__)


async def log_requests(request: Request, call_next: Callable) -> Response:
    """
    Middleware to log incoming HTTP requests and responses.
    Records metrics and handles rate limiting tracking.
    """
    start_time = time.time()
    client_ip = get_real_ip(request)
    request_metrics = get_request_metrics()

    blocked = False
    status_code = 200

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:
        status_code = 500
        raise
    finally:
        duration_ms = (time.time() - start_time) * 1000

        if status_code == 429:
            blocked = True

        request_metrics.record_request(
            ip=client_ip,
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            duration_ms=duration_ms,
            blocked=blocked,
        )

        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {status_code} - "
            f"Duration: {process_time:.3f}s - "
            f"Client: {client_ip}"
        )
