---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tenemos un marketplace en un monolito Java. Somos 3 equipos: catálogo, logística y finanzas. La clase Product tiene 60 campos y cada cambio de un equipo rompe a otro; para finanzas "producto" es una línea facturable, para logística es un SKU en un depósito. También hablamos con un ERP viejo de terceros con un modelo espantoso que no podemos cambiar, y hacemos todo a mano: cálculo de comisiones a vendedores (nuestro modelo de negocio depende de esto), impuestos y envío de mails. El CTO quiere "pasar a microservicios con DDD". ¿Cómo lo encaramos?
