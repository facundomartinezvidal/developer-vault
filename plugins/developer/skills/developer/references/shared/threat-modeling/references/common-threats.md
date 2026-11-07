# Recurring architecture-level threats

A memory aid to run after your own analysis. Each item only counts if you can write it as a concrete scenario in the system at hand.

## Identity and access
- Object-level authorization missing: an ID in the request is trusted without an ownership check (IDOR/BOLA).
- Tenant identifier taken from client input instead of the authenticated session; background jobs or caches that lose the tenant scope.
- Authorization checked in the UI or gateway only, with internal services reachable directly.
- Long-lived or shared service credentials; a service account with far more access than its callers.
- Session and token weaknesses: no revocation, tokens in URLs or logs, password reset and invite flows that bypass normal checks.
- Admin and support tools with weaker controls than the product, and no audit trail.

## Integrations and inbound data
- Webhooks accepted without signature verification, replay protection, or idempotency.
- User-supplied URLs fetched server-side (SSRF), reaching cloud metadata or internal services.
- Files parsed by complex libraries (PDF, images, Office, archives): malicious content, decompression bombs, resource exhaustion. Isolate the parser.
- Uploads served from the app's own origin (stored XSS); presigned URLs too broad or long-lived.
- A third party treated as fully trusted: compromised vendor, or responses used without validation.

## Data
- Sensitive data in logs, traces, analytics, error trackers, backups or lower environments.
- Secrets in the repo, images, build logs or client bundles.
- Data retained with no purpose or no deletion path: data that doesn't exist can't leak.
- Cache keys that omit the user or tenant, serving one user's data to another.

## Availability and abuse
- Expensive operations with no rate limit, quota or size limit (exports, search, report generation, LLM calls).
- Queues with no backpressure or dead-letter handling, so one poison message or one noisy tenant affects everybody.
- Business logic abuse: races on balances, coupons, refunds or inventory; retries that double-charge.

## Integrity and evidence
- Client-calculated values trusted by the server (prices, totals, roles).
- Security-relevant actions with no tamper-resistant record of who did what.
- CI/CD with production access and weak protection; unpinned dependencies or images (supply chain).

## AI features and agents
- Untrusted content (documents, web pages, tickets, emails) processed by a model that also has tools or sensitive data: prompt injection leading to data exfiltration or unwanted actions.
- Agent tools with broader permissions than the user who triggered them.
- Model output rendered or executed without validation.
