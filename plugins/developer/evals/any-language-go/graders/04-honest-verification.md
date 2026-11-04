---
type: llm
focus: trace
weight: 1
---

It attempts to run go test or go vet, including the race detector if available. If Go is unavailable, it says plainly that the code was not compiled or run, and gives the command to run. It does not claim that tests pass.
