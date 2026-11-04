---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Ayudame a explicar y revisar este diseño antes de implementarlo. Es una API de documentos multi-tenant: los usuarios inician sesión y reciben un token con tenantId; GET /documents/:id consulta solo por id y acepta un tenantId opcional del query. Un worker convierte PDFs subidos, con permisos para leer todos los documentos. Necesito una vista de contenedores para devs nuevos y los riesgos que deberíamos corregir primero. No quiero un ADR ni implementación.
