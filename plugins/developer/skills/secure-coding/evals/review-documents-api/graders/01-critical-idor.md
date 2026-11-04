---
type: llm
focus: trace
weight: 1
---

CRITICAL security criterion. It identifies that GET /documents/:id loads a document by ID without checking that it belongs to req.user, so any authenticated user can read other users' documents. It proposes a check or a query scoped by owner.
