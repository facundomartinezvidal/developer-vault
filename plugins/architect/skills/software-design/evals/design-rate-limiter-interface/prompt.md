---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tengo que diseñar en TypeScript un módulo interno de rate limiting para nuestros servicios. Hoy lo necesitan: la API pública (por API key, 100 req/min) y el envío de SMS (por usuario, 5 por hora). Usamos Redis. ¿Cómo diseñarías la interfaz? Todavía no escribas la implementación completa.
