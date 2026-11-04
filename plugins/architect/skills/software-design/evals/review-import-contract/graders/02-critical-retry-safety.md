---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. It recognizes that chunk commits plus timeouts/whole-file retries can duplicate already committed rows. It does not promise atomicity or safe retries from batchId alone. It offers a concrete viable guarantee: atomic batch with an operation identity/result recovery, or durable per-row deduplication/progress with stable identity and reconciliation, or explicitly suspends blind retries pending such a mechanism. A generic instruction to add retries or use idempotency without explaining durable state or uniqueness does not pass.
