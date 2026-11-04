---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Arreglá el bug en store.go: Get devuelve un valor vacío sin avisar cuando la clave no existe. Y cuando dos goroutines escriben a la vez a veces explota. Los llamadores aún no existen, así que podés cambiar la firma.

Input files: store.go
