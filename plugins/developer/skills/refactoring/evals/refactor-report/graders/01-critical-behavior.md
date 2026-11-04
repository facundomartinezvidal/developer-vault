---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. The original behavior is preserved, including the fact that the csv total truncates with int() while the text total rounds. It does not silently unify them. The existing tests pass after the change, as shown by a run actually executed.
