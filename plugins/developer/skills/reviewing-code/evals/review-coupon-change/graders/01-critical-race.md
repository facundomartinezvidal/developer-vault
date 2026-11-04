---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. It identifies that checking used and later setting it is a race, so two concurrent requests can both use the coupon, contradicting the purpose of the PR. It proposes an atomic update or a constraint.
