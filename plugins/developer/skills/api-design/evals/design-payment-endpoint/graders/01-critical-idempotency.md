---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. It explains that a retry after a dropped connection can create a duplicate transfer. It proposes an idempotency key with durable storage under a unique constraint, and says what a repeated request returns.
