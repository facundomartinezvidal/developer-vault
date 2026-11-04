---
type: llm
focus: trace
weight: 1
---

It treats the credit limit as an invariant across Customer and Order and states an explicit decision on how it is enforced (e.g. reservation with a short transaction or a separate credit aggregate), and doesn't ignore the race.
