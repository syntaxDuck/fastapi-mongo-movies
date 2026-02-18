"""
User request metrics tracking module.
Tracks HTTP requests by IP for monitoring and security analysis.
"""

from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from itertools import islice
from threading import Lock
from typing import Any, Optional


@dataclass
class RequestMetric:
    """Single request metric."""

    ip: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    timestamp: datetime
    blocked: bool = False


@dataclass
class IpMetrics:
    """Metrics for a single IP address."""

    total_requests: int = 0
    blocked_requests: int = 0
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    by_path: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    by_status: dict[str, int] = field(default_factory=lambda: defaultdict(int))


class RequestMetrics:
    """Thread-safe metrics collector for HTTP requests."""

    _instance: Optional["RequestMetrics"] = None
    _lock = Lock()

    def __new__(cls) -> "RequestMetrics":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._max_history = 50000
        self._requests: deque[RequestMetric] = deque(maxlen=self._max_history)
        self._ip_metrics: dict[str, IpMetrics] = {}
        self._initialized = True

    def record_request(
        self,
        ip: str,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        blocked: bool = False,
    ) -> None:
        """Record an HTTP request."""
        with self._lock:
            metric = RequestMetric(
                ip=ip,
                method=method,
                path=self._normalize_path(path),
                status_code=status_code,
                duration_ms=duration_ms,
                timestamp=datetime.now(),
                blocked=blocked,
            )
            self._requests.append(metric)
            self._update_ip_metrics(metric)

    def _normalize_path(self, path: str) -> str:
        """Normalize path by removing query parameters and IDs."""
        normalized = path.split("?")[0]
        normalized = normalized.rstrip("/")

        segments = normalized.split("/")
        normalized_segments = []
        for seg in segments:
            if seg and seg not in ("api", "admin"):
                if seg.isdigit() or self._is_object_id(seg):
                    normalized_segments.append("{id}")
                else:
                    normalized_segments.append(seg)
            else:
                normalized_segments.append(seg)

        return "/".join(normalized_segments)

    def _is_object_id(self, s: str) -> bool:
        """Check if string looks like a MongoDB ObjectId."""
        return len(s) == 24 and all(c in "0123456789abcdef" for c in s.lower())

    def _update_ip_metrics(self, metric: RequestMetric) -> None:
        """Update aggregated metrics for an IP."""
        if metric.ip not in self._ip_metrics:
            self._ip_metrics[metric.ip] = IpMetrics()

        ip_metrics = self._ip_metrics[metric.ip]
        ip_metrics.total_requests += 1
        if metric.blocked:
            ip_metrics.blocked_requests += 1

        now = datetime.now()
        if ip_metrics.first_seen is None:
            ip_metrics.first_seen = now
        ip_metrics.last_seen = now

        ip_metrics.by_path[metric.path] += 1
        ip_metrics.by_status[str(metric.status_code)] += 1

    def get_recent_requests(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get recent requests.

        Performance: O(limit) by using islice on reversed deque.
        """
        with self._lock:
            # Optimization: Use islice on reversed deque for O(limit) access
            recent = list(islice(reversed(self._requests), limit))
            # Put back in chronological order for the return list
            recent.reverse()
            return [
                {
                    "ip": m.ip,
                    "method": m.method,
                    "path": m.path,
                    "status_code": m.status_code,
                    "duration_ms": round(m.duration_ms, 2),
                    "timestamp": m.timestamp.isoformat(),
                    "blocked": m.blocked,
                }
                for m in reversed(recent)
            ]

    def get_summary(self) -> dict[str, Any]:
        """Get summary of all request metrics.

        Performance: O(k) where k is the number of records within the last 24h,
        utilizing a single-pass reversed iteration with early exit.
        """
        now = datetime.now()
        cutoff_1h = now - timedelta(hours=1)
        cutoff_24h = now - timedelta(hours=24)

        with self._lock:
            count_1h = 0
            count_24h = 0
            unique_ips_1h = set()
            unique_ips_24h = set()
            blocked_1h = 0
            blocked_24h = 0
            by_endpoint = defaultdict(int)

            # Optimization: Use single pass with early exit for aggregation
            for r in reversed(self._requests):
                if r.timestamp < cutoff_24h:
                    break

                count_24h += 1
                unique_ips_24h.add(r.ip)
                if r.blocked:
                    blocked_24h += 1

                if r.timestamp >= cutoff_1h:
                    count_1h += 1
                    unique_ips_1h.add(r.ip)
                    if r.blocked:
                        blocked_1h += 1
                    by_endpoint[r.path] += 1

            return {
                "total_requests_1h": count_1h,
                "total_requests_24h": count_24h,
                "unique_ips_1h": len(unique_ips_1h),
                "unique_ips_24h": len(unique_ips_24h),
                "blocked_requests_1h": blocked_1h,
                "blocked_requests_24h": blocked_24h,
                "by_endpoint": dict(by_endpoint),
            }

    def get_ip_details(self, ip: str) -> dict[str, Any] | None:
        """Get detailed metrics for a specific IP."""
        with self._lock:
            if ip not in self._ip_metrics:
                return None

            metrics = self._ip_metrics[ip]
            return {
                "ip": ip,
                "total_requests": metrics.total_requests,
                "blocked_requests": metrics.blocked_requests,
                "first_seen": (metrics.first_seen.isoformat() if metrics.first_seen else None),
                "last_seen": (metrics.last_seen.isoformat() if metrics.last_seen else None),
                "by_path": dict(metrics.by_path),
                "by_status": dict(metrics.by_status),
            }

    def get_top_ips(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get top IPs by request count."""
        with self._lock:
            sorted_ips = sorted(
                self._ip_metrics.items(),
                key=lambda x: x[1].total_requests,
                reverse=True,
            )
            return [
                {
                    "ip": ip,
                    "total_requests": metrics.total_requests,
                    "blocked_requests": metrics.blocked_requests,
                }
                for ip, metrics in sorted_ips[:limit]
            ]

    def get_blocked_ips(self) -> list[dict[str, Any]]:
        """Get IPs with blocked requests."""
        with self._lock:
            return [
                {
                    "ip": ip,
                    "blocked_requests": metrics.blocked_requests,
                    "total_requests": metrics.total_requests,
                    "last_seen": (metrics.last_seen.isoformat() if metrics.last_seen else None),
                }
                for ip, metrics in self._ip_metrics.items()
                if metrics.blocked_requests > 0
            ]

    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._requests.clear()
            self._ip_metrics.clear()


def get_request_metrics() -> RequestMetrics:
    """Get the singleton metrics instance."""
    return RequestMetrics()
