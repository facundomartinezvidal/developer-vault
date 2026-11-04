---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. It identifies that AuditService is registered as a singleton and holds AppDbContext, a captive dependency that shares a non-thread-safe scoped context across requests. It proposes a correct lifetime or a scope or context factory.
