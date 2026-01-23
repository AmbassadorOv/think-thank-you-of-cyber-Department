## 2025-06-17 - [Optimized git-find-dirs-many-files]
**Learning:** The nested `find` pattern in shell scripts (e.g., `find . -type d -exec find {} ...`) causes an exponential or O(N*Depth) performance bottleneck due to redundant file system traversals and high process-spawning overhead.
**Action:** Use a single-pass `find` to list all files and aggregate counts for parent directories using `awk` to achieve O(N) performance.
