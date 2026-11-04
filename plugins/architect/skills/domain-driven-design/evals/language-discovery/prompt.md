---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Estamos modelando turnos médicos. Recepción dice que un turno está confirmado cuando el paciente responde al recordatorio; facturación dice confirmado cuando está autorizada la cobertura; el médico lo usa cuando acepta la consulta. Hoy todos escriben un booleano confirmed y se pisan. Una consulta puede estar aceptada por el médico, con cobertura pendiente y sin respuesta al recordatorio. El administrador quiere que elijamos un nombre mejor y sigamos.

Ayudame a trabajar el lenguaje ubicuo con estas personas. No tenemos su respuesta todavía: proponé ejemplos y preguntas concretas para validar qué significa cada cosa y cómo llevar el acuerdo al modelo y a pruebas. No necesito un mapa completo ni separar servicios.
