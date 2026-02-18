## 2025-05-14 - Stable Component Optimizations
**Learning:** In React applications with long lists (like MovieList), missing `React.memo` and unstable function/object references in parents (like `MoviePage` and `GenresPage`) cause massive cascading re-renders. Hoisting animation variants outside the component is a zero-cost way to ensure stable references for memoized children.
**Action:** Always wrap list items in `React.memo` and ensure that all props passed to them (callbacks, objects) are stable via `useCallback`, `useMemo`, or hoisting.

## 2025-05-15 - Efficient History Tracking and Aggregation
**Learning:** Using Python lists for fixed-size history tracking results in O(N) append operations due to manual slicing. Additionally, scanning full history for time-windowed aggregations is O(N). Switching to `collections.deque` with `maxlen` provides O(1) appends, and utilizing `reversed()` iteration with early exit reduces aggregation complexity to O(k) where k is the number of records within the window.
**Action:** Use `collections.deque` for metrics history and always prefer early-exit iteration for chronologically ordered data.
