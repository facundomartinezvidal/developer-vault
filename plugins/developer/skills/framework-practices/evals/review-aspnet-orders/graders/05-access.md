---
type: llm
focus: trace
weight: 1
---

It flags that GET /orders/{id} loads any order without checking ownership, so any authenticated user can read it, and proposes a scoped query or resource-based authorization.
