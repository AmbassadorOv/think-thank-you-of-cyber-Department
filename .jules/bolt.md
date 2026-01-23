## 2025-05-14 - [Inefficient nested find in shell scripts]
**Learning:** Shell scripts that use 'find' inside a loop over another 'find' output have (N \times D)$ complexity and high overhead due to process forking. This can be optimized to (N)$ using a single 'find' pass combined with 'awk' for in-memory aggregation.
**Action:** When encountering nested 'find' or 'grep' in loops, replace them with a single pass aggregation using 'awk' or a hash map in a more capable language.
