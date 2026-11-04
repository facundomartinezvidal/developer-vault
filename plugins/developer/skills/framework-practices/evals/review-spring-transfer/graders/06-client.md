---
type: llm
focus: trace
weight: 1
---

It flags that RestTemplate has no timeouts and is discouraged for new code, proposing RestClient with timeouts, or it flags the network call inside the unit of work.
