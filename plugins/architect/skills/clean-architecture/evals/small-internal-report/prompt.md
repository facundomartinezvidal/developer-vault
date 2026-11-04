---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Tengo un script Python de 90 líneas que lee un CSV exportado por soporte y genera un resumen de tickets por semana. Lo corre una persona a mano una vez al mes. No hay servidor, base de datos, reglas de autorización ni planes de convertirlo en producto. Está en un solo archivo con main(), parse_rows() y summarize(). Me dijeron que para aplicar Clean Architecture tengo que agregar entidades, casos de uso, repositorios y cuatro carpetas. ¿Qué harías? Explicalo breve; no cambies archivos.
