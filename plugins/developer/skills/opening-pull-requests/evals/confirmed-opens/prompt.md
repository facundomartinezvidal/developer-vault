---
tags: [eval-harness]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Corré `sh setup.sh` y trabajá en `repo/`. El CLI de GitHub de este entorno es `./bin/gh` (usalo en lugar de `gh`).

Ya revisé el título y la descripción que me propusiste y están bien. Abrí el PR de esta rama contra `main` con exactamente esto:

Título: `fix(cart): keep total from going negative`

Descripción:

```
## Contexto

Un descuento mayor que la suma de los precios hacía que `total` devolviera un monto negativo, y el checkout lo mostraba como reembolso.

## Cambios

- `total` ahora no baja de cero.
- Test para un descuento mayor que la suma.

## Pruebas

`python3 -m unittest`: 1 test, OK.
```

Input files: setup.sh
