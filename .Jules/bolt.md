
## 2026-02-11 - [Preserving Invariants after Optimization]
**Learning:** When optimizing data fetching (e.g., reducing fetch limits or parallelizing), it is crucial to ensure that business invariants (like poster uniqueness across genre cards) are maintained. A performance optimization that trades off correctness (like introducing duplicate posters) is a regression. In this case, skipping genres without unique candidates preserved the invariant while keeping the performance gains.
**Action:** Always verify that performance optimizations do not silently break existing data constraints or UI logic. In parallel loops, maintain state (like a `Set` of used IDs) to enforce uniqueness across results.
