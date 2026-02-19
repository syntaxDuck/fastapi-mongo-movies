## 2025-05-14 - Stable Component Optimizations
**Learning:** In React applications with long lists (like MovieList), missing `React.memo` and unstable function/object references in parents (like `MoviePage` and `GenresPage`) cause massive cascading re-renders. Hoisting animation variants outside the component is a zero-cost way to ensure stable references for memoized children.
**Action:** Always wrap list items in `React.memo` and ensure that all props passed to them (callbacks, objects) are stable via `useCallback`, `useMemo`, or hoisting.

## 2025-05-15 - Optimized Metrics Collection
**Learning:** Using a standard 'list' for high-frequency metrics collection with manual slicing (O(N)) creates a hidden performance tax on every operation. 'collections.deque' with 'maxlen' provides O(1) history management. Additionally, summary queries on chronological metrics should always use 'reversed()' iteration with early exit to avoid full O(N) scans.
**Action:** Use 'deque(maxlen=K)' for history buffers and implement early-exit loops for time-series aggregations.
