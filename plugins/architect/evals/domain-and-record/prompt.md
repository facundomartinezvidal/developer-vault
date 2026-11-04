---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

En nuestro monolito B2B, dos pedidos simultáneos pueden consumir el mismo crédito disponible porque cada uno lee el saldo y después lo descuenta. El límite es estricto sobre la exposición acumulada del cliente. Queremos comparar cómo corregirlo sin separar servicios: bloqueo, versión optimista o actualización condicional. Modelá quién posee esa regla y dejá un ADR propuesto con la recomendación y sus costos. No elegimos mecanismo todavía. No implementes.
