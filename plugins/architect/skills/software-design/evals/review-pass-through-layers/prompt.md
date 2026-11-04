---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

¿Está bien diseñado este módulo de archivos? En src/files. Lo armó un compañero con Controller → Service → Manager "para que quede limpio y podamos cambiar de proveedor". Solo usamos S3 y no hay planes de cambiarlo por ahora. Sé honesto.

Input files: src/files/FileController.ts, src/files/FileService.ts, src/files/FileManager.ts
