---
type: llm
focus: trace
weight: 1
---

It puts pricing/discount decisions in domain policy with no Mongoose, Express or Stripe imports. Application orchestration may load required data and call that policy; leaving the pricing decision itself in the HTTP handler or orchestration service does not pass.
