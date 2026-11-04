---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Armé un bot de Slack interno para el equipo de soporte (somos 30 en la empresa). Con /cliente <email> te muestra plan y último pago del cliente, pegándole a una réplica de lectura de Postgres. Corre como un Lambda con una Function URL pública, porque Slack la tiene que poder llamar. ¿Le ves algo de seguridad que tenga que arreglar? No quiero hacer un proyecto de esto.
