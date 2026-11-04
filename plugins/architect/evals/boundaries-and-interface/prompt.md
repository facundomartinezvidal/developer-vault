---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tenemos un módulo de reportes Python: el cálculo recibe una Session de SQLAlchemy, llama consultas y devuelve objetos ORM al handler HTTP. Queremos probar el cálculo sin base. Además, cada caller debe invocar begin(), load(), compute(), close() en ese orden y a veces olvida close() al fallar. Revisá los límites y proponé una interfaz local más fácil de usar. No implementes ni rediseñes todo el proyecto.
