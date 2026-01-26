## 2026-01-26 - [O(N*Depth) to O(N) optimization in bash scripts]
**Learning:** Nested loops calling 'find' for every directory in a tree leads to O(N*Depth) performance, which scales poorly with repository size and depth. This can be optimized by using a single-pass 'find' and aggregating results in 'awk'.
**Action:** Always look for patterns where 'find' or similar traversal tools are called inside a loop over their own results. Replace with a single-pass aggregation using 'awk' or a hash map.
