## 2025-01-24 - [Webhook IP Metadata Caching]
**Learning:** Fetching external metadata (like GitHub's IP ranges) on every request introduces significant latency (~200ms) and redundant processing. A simple process-level cache can reduce this overhead to near-zero.
**Action:** Always identify external API calls in hot paths and implement appropriate caching (process-level for static/slow-changing data).

## 2025-01-24 - [Python 3 HMAC Key Encoding]
**Learning:** In Python 3, `hmac.new` requires the key to be bytes. `isinstance(secret, bytes)` is the robust way to check if encoding is needed across Python 2 and 3, as `bytes` is an alias for `str` in Python 2.
**Action:** Use `if not isinstance(key, bytes): key = key.encode('utf-8')` for cross-version HMAC key preparation.
