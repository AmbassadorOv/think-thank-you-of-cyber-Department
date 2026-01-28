# Bolt's Performance Journal

## 2025-05-23 - Single-pass traversal for directory statistics
**Learning:** Using `find -exec` with nested `find` calls to calculate directory statistics results in $O(N \times D)$ complexity (where $N$ is files and $D$ is directories) and massive process overhead. A single-pass `find` piped into `awk` can aggregate these statistics in memory with $O(N)$ complexity and minimal process spawning.
**Action:** Always prefer single-pass traversals and in-memory aggregation (e.g., with `awk`) for file system statistics over nested shell commands.
