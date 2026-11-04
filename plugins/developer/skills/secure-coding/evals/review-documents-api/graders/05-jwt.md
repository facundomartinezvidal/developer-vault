---
type: llm
focus: trace
weight: 1
---

It flags that jwt.decode does not verify the signature, so identities can be forged, and proposes verify with a fixed algorithm.
