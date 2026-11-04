---
type: llm
focus: trace
weight: 1
---

CRITICAL correctness criterion. It identifies that transfer calls the @Transactional doTransfer method on the same object, so the proxy is bypassed and there is no transaction: a failure between the two saves leaves money moved from only one account. It also accepts noting the private visibility. It proposes a workable fix.
