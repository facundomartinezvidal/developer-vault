---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. Retries are limited, with backoff, and only on transient failures, not on a 400. It addresses duplicates by sending an idempotency key or by saying that the receiver must support it, rather than assuming that retrying is safe.
