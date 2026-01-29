## 2026-01-29 - [Optimized git-find-dirs-many-files]
**Learning:** Nested recursive calls (like find within find) in shell scripts create a massive performance bottleneck, especially as the directory structure deepens. A single-pass approach using awk to aggregate data from a single walk is significantly more efficient (O(N) vs O(N*Depth)).
**Action:** Always prefer single-pass data aggregation (using awk or maps) over nested traversals in analysis scripts.

## 2026-01-29 - [Bug in IP validation]
**Learning:** The Flask webhook server in `hooks/python/flask-github-webhooks/webhooks.py` has a flawed IP validation loop that aborts on the first mismatch instead of checking the entire whitelist.
**Action:** (Future) Ensure validation loops only abort after checking all possibilities.
