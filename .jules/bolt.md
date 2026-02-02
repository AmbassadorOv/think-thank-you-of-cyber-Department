## 2025-01-30 - Network and Disk I/O Caching in Flask Webhooks
**Learning:** Performing network requests (e.g., fetching GitHub IP metadata) and disk I/O (e.g., reading configuration) inside a request handler significantly increases latency and risks hitting rate limits. Moving these to the global scope or implementing a process-level cache reduces latency from >100ms to <1ms.
**Action:** Always move static configuration loading and external metadata fetching out of the hot path of request handlers. Use global variables for simple process-level caching.
