"""
Database metrics tracking module.
Tracks query operations for monitoring and performance analysis.
"""

import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import Lock
from typing import Any, Optional


@dataclass
class OperationMetric:
    """Single operation metric."""

    operation: str
    collection: str
    duration_ms: float
    timestamp: datetime
    success: bool
    filters: dict[str, Any] | None = None


@dataclass
class AggregatedMetrics:
    """Aggregated metrics for a time window."""

    total_operations: int = 0
    total_duration_ms: float = 0
    successful_operations: int = 0
    failed_operations: int = 0
    by_operation: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    by_collection: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    avg_duration_ms: float = 0


class DatabaseMetrics:
    """Thread-safe metrics collector for database operations."""

    _instance: Optional["DatabaseMetrics"] = None
    _lock = Lock()

    def __new__(cls) -> "DatabaseMetrics":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._operations: list[OperationMetric] = []
        self._lock = Lock()
        self._initialized = True
        self._max_history = 10000

    def record_operation(
        self,
        operation: str,
        collection: str,
        duration_ms: float,
        success: bool = True,
        filters: dict[str, Any] | None = None,
    ) -> None:
        """Record a database operation."""
        with self._lock:
            metric = OperationMetric(
                operation=operation,
                collection=collection,
                duration_ms=duration_ms,
                timestamp=datetime.now(),
                success=success,
                filters=self._sanitize_filters(filters),
            )
            self._operations.append(metric)

            if len(self._operations) > self._max_history:
                self._operations = self._operations[-self._max_history :]

    def _sanitize_filters(self, filters: dict[str, Any] | None) -> dict[str, Any] | None:
        """Remove sensitive data from filters for logging."""
        if not filters:
            return None
        sensitive_keys = {"password", "token", "secret", "api_key", "email"}
        return {
            k: "***REDACTED***" if any(s in k.lower() for s in sensitive_keys) else v
            for k, v in filters.items()
        }

    def get_recent_operations(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get recent operations."""
        with self._lock:
            recent = self._operations[-limit:]
            return [
                {
                    "operation": m.operation,
                    "collection": m.collection,
                    "duration_ms": round(m.duration_ms, 2),
                    "timestamp": m.timestamp.isoformat(),
                    "success": m.success,
                    "filters": m.filters,
                }
                for m in reversed(recent)
            ]

    def get_aggregated_metrics(
        self,
        since: datetime | None = None,
        operation: str | None = None,
        collection: str | None = None,
    ) -> AggregatedMetrics:
        """Get aggregated metrics for a time window."""
        with self._lock:
            if since is None:
                since = datetime.now() - timedelta(hours=1)

            filtered_ops = [
                op
                for op in self._operations
                if op.timestamp >= since
                and (operation is None or op.operation == operation)
                and (collection is None or op.collection == collection)
            ]

            metrics = AggregatedMetrics()
            metrics.total_operations = len(filtered_ops)

            if filtered_ops:
                metrics.total_duration_ms = sum(op.duration_ms for op in filtered_ops)
                metrics.avg_duration_ms = metrics.total_duration_ms / metrics.total_operations
                metrics.successful_operations = sum(1 for op in filtered_ops if op.success)
                metrics.failed_operations = sum(1 for op in filtered_ops if not op.success)

                for op in filtered_ops:
                    metrics.by_operation[op.operation] += 1
                    metrics.by_collection[op.collection] += 1

            return metrics

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of all metrics."""
        now = datetime.now()

        metrics_1h = self.get_aggregated_metrics(since=now - timedelta(hours=1))
        metrics_24h = self.get_aggregated_metrics(since=now - timedelta(hours=24))

        return {
            "last_hour": {
                "total_operations": metrics_1h.total_operations,
                "successful": metrics_1h.successful_operations,
                "failed": metrics_1h.failed_operations,
                "avg_duration_ms": round(metrics_1h.avg_duration_ms, 2),
                "by_operation": dict(metrics_1h.by_operation),
                "by_collection": dict(metrics_1h.by_collection),
            },
            "last_24_hours": {
                "total_operations": metrics_24h.total_operations,
                "successful": metrics_24h.successful_operations,
                "failed": metrics_24h.failed_operations,
                "avg_duration_ms": round(metrics_24h.avg_duration_ms, 2),
                "by_operation": dict(metrics_24h.by_operation),
                "by_collection": dict(metrics_24h.by_collection),
            },
            "total_tracked": len(self._operations),
            "oldest_operation": (
                self._operations[0].timestamp.isoformat() if self._operations else None
            ),
            "newest_operation": (
                self._operations[-1].timestamp.isoformat() if self._operations else None
            ),
        }

    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._operations.clear()


def get_metrics() -> DatabaseMetrics:
    """Get the singleton metrics instance."""
    return DatabaseMetrics()


class OperationTimer:
    """Context manager for timing database operations."""

    def __init__(
        self,
        operation: str,
        collection: str,
        filters: dict[str, Any] | None = None,
    ):
        self.operation = operation
        self.collection = collection
        self.filters = filters
        self._start_time: float = 0
        self._success: bool = True

    def __enter__(self):
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type):
        duration_ms = (time.perf_counter() - self._start_time) * 1000
        self._success = exc_type is None

        get_metrics().record_operation(
            operation=self.operation,
            collection=self.collection,
            duration_ms=duration_ms,
            success=self._success,
            filters=self.filters,
        )
        return False
