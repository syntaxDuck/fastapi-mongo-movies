# BOLT'S JOURNAL - CRITICAL LEARNINGS ONLY

## 2025-05-15 - [GZip Compression for API Responses]
**Learning:** Large JSON payloads, such as movie lists and comments, can significantly increase network latency and data transfer costs. While Nginx often handles GZip compression in production environments, it is frequently absent in development or other deployment scenarios where the FastAPI backend is accessed directly. Adding `GZipMiddleware` to the FastAPI application ensures consistent response compression across all environments.
**Action:** Always include `GZipMiddleware` in FastAPI projects with a reasonable `minimum_size` (e.g., 1000 bytes) to optimize network efficiency regardless of the proxy configuration.
