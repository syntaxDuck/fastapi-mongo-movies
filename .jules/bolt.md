## 2025-05-14 - Stable Component Optimizations
**Learning:** In React applications with long lists (like MovieList), missing `React.memo` and unstable function/object references in parents (like `MoviePage` and `GenresPage`) cause massive cascading re-renders. Hoisting animation variants outside the component is a zero-cost way to ensure stable references for memoized children.
**Action:** Always wrap list items in `React.memo` and ensure that all props passed to them (callbacks, objects) are stable via `useCallback`, `useMemo`, or hoisting.
