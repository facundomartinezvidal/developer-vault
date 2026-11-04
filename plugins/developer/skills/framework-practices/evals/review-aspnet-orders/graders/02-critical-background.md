---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. It identifies that the Task.Run closure captures the request-scoped db and HttpContext, which can be disposed or recycled after the response, and proposes copying data plus a hosted service with a scope, or an equivalent.
