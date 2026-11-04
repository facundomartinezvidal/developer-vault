---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

sender.py manda notificaciones al sistema de facturación y a veces se cuelga todo el worker o se pierden. Dejalo bien para producción. Usa la biblioteca estándar, y los tests están en test_sender.py (python3 -m unittest).

Input files: sender.py, test_sender.py
