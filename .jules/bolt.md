## 2025-05-14 - Optimized git-find-dirs-many-files to O(N)
**Learning:** Nested directory traversals (find -exec find) are extremely slow due to quadratic complexity and process spawning overhead. Aggregating data in a single pass using awk's associative arrays is significantly more efficient.
**Action:** Always prefer single-pass pipelines with aggregation for repository analysis tools.

## 2025-05-14 - Ghost Memories of Optimized Scripts
**Learning:** Discovered a discrepancy where memories claimed `git-find-large-files` was optimized, but the file was still in its original slow state.
**Action:** Always verify the actual state of the codebase and do not rely solely on memory for the current implementation details.
