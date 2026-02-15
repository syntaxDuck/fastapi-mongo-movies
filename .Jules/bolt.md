## 2025-05-15 - [React List Optimization]
**Learning:** Large lists using `motion.div` and complex child components like `MovieCard` suffer from significant re-render overhead. Even if child props don't change, React's default diffing process re-evaluates all children when the parent state updates (e.g., during pagination). Inline arrow functions as props (like `onClick`) also break memoization.
**Action:** Always wrap list items in `React.memo` and ensure callbacks are stable using `useCallback` with proper dependency management. Move constants like `PAGE_SIZE` outside of components to avoid unnecessary dependency changes.

## 2025-05-16 - [Backend Metadata Caching]
**Learning:** Frequent fetching of slow-changing metadata (like genres and types) can be a significant source of database load. Implementing a simple class-level in-memory cache with TTL is highly effective for these use cases.
**Action:** Use class-level variables in service layers for global metadata caching. Always return copies of cached mutable objects (like lists) to prevent accidental mutation of the cache by callers.
