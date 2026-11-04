---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Implementá lo que decidió el arquitecto para cancelar pedidos: las decisiones están en docs/adr/. El código está en src/. Es ASP.NET Core, .NET 10.

Input files: docs/adr/0007-cancel-orders.md, docs/adr/0008-publish-order-events.md, src/Program.cs, src/Order.cs, src/AppDbContext.cs
