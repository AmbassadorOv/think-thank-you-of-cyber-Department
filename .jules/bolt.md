## 2025-01-30 - GitHub IP Whitelist Caching
**Learning:** Fetching the GitHub meta API (IP whitelist) on every webhook request introduces ~200ms latency and creates a dependency on GitHub's API availability/rate limits. Caching this data with a 24h TTL improves response time by ~10x.
**Action:** Always cache external metadata that changes infrequently when processing latency-sensitive requests like webhooks.
