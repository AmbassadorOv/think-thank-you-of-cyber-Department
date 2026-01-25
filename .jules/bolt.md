## 2025-01-29 - GitHub API Caching in Webhooks
**Learning:** Calling `https://api.github.com/meta` on every webhook request introduces significant latency (180ms-600ms). GitHub's IP whitelist changes very infrequently, making it a prime candidate for long-term caching (e.g., 24h).
**Action:** Always implement a caching mechanism for GitHub meta-information in webhook handlers to keep response times under 100ms.

## 2025-01-29 - IP Validation Loop Anti-pattern
**Learning:** A common bug in IP whitelist validation is terminating the loop early on the first non-match instead of checking the entire list.
**Action:** Use Python's `for...else` construct or a flag to ensure all whitelist entries are checked before rejecting a request.
