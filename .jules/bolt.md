# Bolt's Performance Journal

## 2025-05-14 - [Optimizing Git Metadata Joining in Shell Scripts]
**Learning:** Shell loops that invoke `look` or `grep` for every object in a Git repository introduce significant overhead due to process spawning (fork/exec). Even for repositories with < 1000 objects, this can add nearly a second of latency.
**Action:** Use `awk` with associative arrays to perform hash-joins of metadata in a single pass. This reduces O(N*logN) or O(N^2) shell-based lookups to O(N) memory-based lookups, achieving speedups of 20x-100x.
