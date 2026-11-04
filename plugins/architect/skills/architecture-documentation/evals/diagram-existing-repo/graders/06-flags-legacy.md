---
type: llm
focus: trace
weight: 1
---

It identifies that the inspected repository does not establish an invocation path for legacy-reports, rather than inventing a normal caller/flow. It treats the service's usage as unresolved and asks for scheduler, external caller or production evidence before declaring it unused. Merely asserting it is dead because no API call was found does not pass.
