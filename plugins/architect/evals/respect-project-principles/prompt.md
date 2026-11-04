---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tenemos este package Python de cotización. Revisá ARCHITECTURE.md, el ADR y el caller antes de decidir: queremos separar la política de precios de la lectura del cupón sin cambiar el contrato público ni el cálculo monetario. Por ahora solo asesorame sobre el refactor, con una propuesta concreta y los principios que la justifican. No cambies el código ni los acuerdos. No necesito un proyecto nuevo.

Input files: ARCHITECTURE.md, docs/adr/0002-orm-en-core.md, billing/__init__.py, billing/service.py, main.py, test_quote.py
