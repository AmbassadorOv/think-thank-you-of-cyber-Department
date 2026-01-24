# Bolt Performance Journal

## 2025-05-22 - [Optimizing Directory File Counts]
**Learning:** The previous implementation of `git-find-dirs-many-files` used a nested `find` loop within a `find -exec` call. This resulted in an O(N*Depth) complexity because files in deep subdirectories were scanned multiple times (once for each parent directory). A single-pass approach using `find . -type f` and aggregating counts in `awk` reduces this to O(N).
**Action:** Use single-pass `find` and `awk` aggregation for directory-level file counting in scripts.
