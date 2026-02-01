## 2025-05-22 - [Optimization of Git Analysis Scripts]
**Learning:** Replacing Bash loops that call external commands (grep, sed, etc.) with a single `awk` pass using hash maps (associative arrays) provides a massive performance boost (30x speedup in this repo) by eliminating process spawn overhead. This is especially critical when analyzing Git objects where history can be large.
**Action:** Always prefer `awk` or `join` for correlating data from multiple Git commands over Bash loops with search calls.
