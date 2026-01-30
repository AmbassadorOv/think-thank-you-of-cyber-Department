## 2025-05-22 - Optimized git-find-dirs-many-files
**Learning:** Found a classic O(N*Depth) bottleneck where nested find calls were used to count files in subdirectories. Replaced with a single-pass find | awk pipeline that aggregates counts for all parent directories.
**Action:** Always look for nested tree traversals in analysis scripts and replace with single-pass aggregation pipelines using awk.
