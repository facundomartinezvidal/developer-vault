---
type: llm
focus: trace
weight: 1
---

It flags the .Result call as blocking, with thread pool starvation as the consequence, and proposes awaiting.
