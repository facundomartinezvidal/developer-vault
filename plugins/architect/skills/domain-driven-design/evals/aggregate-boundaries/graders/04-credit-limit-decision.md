---
type: llm
focus: trace
weight: 1
---

It explicitly states whether credit limits each order or total outstanding exposure. For a shared credit limit, it identifies a concrete mechanism that prevents two concurrent orders from spending the same credit: a conditional atomic update, a version check with fresh validation on retry, or locking with a stated protocol for all competing writers. Merely saying "transaction", showing read-check-write, or creating a Credit aggregate without protecting concurrent persistence does not pass. If it chooses reservations, it also explains how failed confirmation releases credit without duplicate release.
