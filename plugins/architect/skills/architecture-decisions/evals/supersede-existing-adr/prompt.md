---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Mirá los ADRs que tenemos en docs/adr. Nos entró un cliente enterprise (un banco, 8000 empleados, sería el 35% de nuestro ingreso) que por contrato exige que sus datos estén aislados físicamente de otros clientes y poder elegir cuándo se le aplican las migraciones. Ya hablamos en el equipo y vamos a armarle una base dedicada solo para los clientes que lo requieran y seguir con el esquema compartido para el resto. Dejá registrada la decisión.

Input files: docs/adr/0001-registrar-decisiones.md, docs/adr/0003-multi-tenancy-esquema-compartido.md, docs/adr/0005-hosting-aws.md
