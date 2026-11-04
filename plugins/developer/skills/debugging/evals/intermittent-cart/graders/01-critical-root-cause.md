---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. It identifies the mutable default argument items=[] in Cart.__init__ as the cause, and fixes it in cart.py so each cart gets its own list. Reordering tests, resetting state in a test, or skipping the test does not pass.
