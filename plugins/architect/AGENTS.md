# AGENTS.md — estado del plugin `architect`

Estado al **2026-11-03**. Este archivo es para quien continúe el trabajo, persona o agente. Resume qué hay, cómo se mantiene, cómo vamos con cada skill y qué sigue. El uso del plugin está en `README.md`.

## Qué es

Un agente de arquitectura de software y 6 skills, instalable en **Claude Code** y **GitHub Copilot CLI**. Codex se probó y se sacó por ahora: su formato de plugin no documenta agentes y no hubo forma de probarlo con sesión iniciada.

- **Agente:** `architect`. Entiende el problema, elige la skill, compara opciones y recomienda. Asesora; no modifica código salvo que se lo pidan. Esa regla es una instrucción, no un bloqueo técnico.
- **Skills:** manuales que el agente abre según la tarea. Un `SKILL.md` corto, con material de consulta aparte.

## Cómo está armado

```
plugins/architect/
├── src/architect.md          fuente única del agente (editar acá)
├── agents/, com.github.copilot/agents/, skills/architect/   generados desde src/
├── skills/<skill>/
│   ├── SKILL.md              cuándo usarla y el método (menos de 500 líneas)
│   ├── references/           material de consulta; se lee solo el archivo que hace falta
│   ├── assets/               plantillas (solo architecture-decisions)
│   └── evals/                casos de prueba; el agente nunca los lee
└── scripts/
    ├── build_agents.py       genera los 3 archivos del agente
    ├── sync_vault.py         regenera references/ desde el vault de Obsidian
    └── vault_manifest.py     qué notas alimentan qué archivo
```

Reglas de mantenimiento:

- **No editar a mano** lo generado: `agents/`, `com.github.copilot/`, `skills/architect/` ni los `references/` de `clean-architecture`, `domain-driven-design`, `software-design` y `architecture-decisions/references/decision-principles.md`. Se cambian en `src/` o en el vault.
- Se regeneran con `python3 scripts/build_agents.py` y `python3 scripts/sync_vault.py <ruta al vault developer-knowledge>`. Con `--check` fallan si algo quedó desactualizado.
- A mano quedan: `architecture-documentation/references/c4-mermaid.md`, `threat-modeling/references/common-threats.md` y los `SKILL.md`.
- El vault vive fuera de este repo. No se copian los PDFs de los libros y no deben entrar.
- Validar: `claude plugin validate .` desde `plugins/architect` y desde la raíz del repo.

## Cómo vamos

Cada caso se corrió con y sin skill, y se calificó contra una lista de criterios verificables. Los números son puntos cumplidos sobre el total.

| Skill | Con skill | Sin skill | Estado |
|---|---|---|---|
| `clean-architecture` | 19/20 | 12/20 | Funciona; es la que más mejora las respuestas |
| `architecture-documentation` | 13/13 | 9/13 | Funciona |
| `threat-modeling` | 14/15 → 17/17 tras corregirla | 11/15 | Funciona; la corrección no se comparó otra vez contra sin skill |
| `architecture-decisions` | 12/14 → 13/14 tras corregirla | 13/14 | Funciona con un error pendiente |
| `domain-driven-design` | 15/16 | 14/16 | Aporta poco en estos casos |
| `software-design` | 14/14 | 13/14 | Aporta poco en estos casos |
| `architect` (agente) | — | — | Solo una pregunta de prueba, en Claude Code y Copilot |

Las 7 skills pasan la revisión estática: nombre igual a la carpeta, descripción de menos de 1024 caracteres, `SKILL.md` de menos de 500 líneas, referencias existentes y citadas, y sin restos de Obsidian.

### Cuánto confiar en los números

- Cada versión corrió **una sola vez** por caso. Una diferencia chica es una señal débil.
- Muchos criterios pasan igual con y sin skill, porque los casos plantan fallas obvias. Por eso `domain-driven-design` y `software-design` no están bien medidas: no se sabe si aportan poco o si los casos eran fáciles.
- Algunos criterios eran permisivos o juntaban dos cosas.
- Las respuestas con skill son más largas. En `clean-architecture`, unas 1,8 veces. No se midió si lo extra aporta.

### Problemas conocidos

1. **`architecture-decisions`:** la sección "Consecuencias" de un ADR todavía afirma datos no verificados como hechos.
2. **`domain-driven-design`:** cuando recomienda una transacción para un límite de crédito, el ejemplo no cierra la condición de carrera (lee y después escribe, sin bloqueo ni versión). La respuesta sin skill usó un `UPDATE` condicional atómico. Ambas versiones fallaron el criterio de mostrar comportamiento en el agregado en TypeScript.
3. **`clean-architecture`:** dejó la regla de suspensión de clientes en el caso de uso y no en el dominio. Es una mejora a la skill, y también hay que dividir el criterio, que juntaba precios y suspensión.
4. **`threat-modeling`:** en el caso grande escribe unas 1.800 palabras. Está dentro del límite que se fijó (unas 2.000), pero es largo.
5. **`architect`:** falta una evaluación completa.

## Qué sigue

1. **`domain-driven-design`:** pedir un mecanismo concreto que cierre la carrera cuando se recomienda una transacción, y escribir casos más difíciles.
2. **`software-design`:** escribir casos más difíciles. Si tampoco mejora las respuestas, sacarla: cada skill suma una descripción que compite por activarse.
3. **`architecture-decisions`:** no afirmar como hecho lo que no se verificó, tampoco en "Consecuencias".
4. **`clean-architecture`:** regla de suspensión en el dominio; dividir el criterio de precios y suspensión.
5. **`architect`:** casos que crucen varias skills.
6. **Todas:** repetir cada caso más de una vez y agregar casos que no sean obvios.

## Cómo evaluar sin contaminar

Se hizo con subagentes, sin `claude plugin eval`, que son corridas pagas.

- **Sacar `skills/*/evals/` de la carpeta del plugin antes de correr.** Cuatro corridas vieron los nombres de los criterios porque un `ls -R` los listó. Se repitieron desde cero. Después, devolverlos.
- Por caso, una corrida con skill y otra sin skill, con el mismo prompt. Los casos con archivos reciben una copia del repo de ejemplo.
- Calificar contra los mismos criterios y con la misma exigencia.
- Los resultados crudos de las corridas estaban en una carpeta temporal y **no se guardaron en el repo**. Lo que queda es este resumen.

## Decisiones abiertas

- **Repo público y citas:** los `references/` incluyen citas textuales de libros que salen de las notas del vault. No hay PDFs. Quien publique esto debería decidir si deja el repo público con esas citas o lo pasa a privado.
- **Dos copias de `clean-architecture`:** también existe en `skillswap/.claude/skills/clean-architecture`. La del plugin es la que se mantiene. Falta decidir si skillswap pasa a usar la del plugin.
- **Codex:** pendiente. Si se retoma, hay que revisar cómo instalar agentes, porque su formato de plugin no lo documenta.
- **Nombre del agente en Copilot:** con `--plugin-dir`, el agente se llama `architect:architect`, no `architect`.
