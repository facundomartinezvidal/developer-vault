---
type: llm
focus: trace
weight: 1
---

CRITICAL security criterion. It identifies command injection in /convert, because req.query.name reaches exec within a shell string, and proposes an argument array with validated input or a similar fix.
