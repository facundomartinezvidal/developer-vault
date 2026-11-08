# AGENTS.md — estado del plugin `architect`

Estado al **2026-11-07**. Este archivo es para quien continúe el trabajo, persona o agente: qué hay, cómo se mantiene, cómo vamos y qué sigue. El historial de evaluaciones está en `evals/HISTORY.md`, y el uso del plugin, en `README.md`.

## Qué es

Un agente de arquitectura de software y 6 skills, instalable en **Claude Code**, **GitHub Copilot CLI** y **Codex**. **Codex** carga el plugin y sus skills, probado el 2026-11-04 con `codex-cli` 0.166 en un `CODEX_HOME` aislado, tanto local como desde GitHub. Sus plugins no incluyen agentes, así que el rol llega como skill y hay un agente TOML opcional en `com.openai.codex/agents/`.

- **Agente:** `architect`. Planea, diseña y consulta sobre interfaces, packages, módulos, capas o sistemas completos, y no edita código. Produce análisis, diseños, ADRs, diagramas y planes. Si le piden implementar, entrega un plan para el agente `developer` (división pedida por el usuario el 2026-11-04, que reemplazó un rol anterior en el que también implementaba refactors). Identifica y respeta los principios del proyecto y los ADRs aceptados, y distingue las propuestas pendientes.
- **Planes guardados (2026-11-07):** los planes para implementar van a la carpeta de planes del repo, o a `docs/plans/AAAA-MM-DD-tema.md`, empezando con una tabla de decisiones (estado y fuente de aprobación). Las consultas quedan en la conversación. `developer` los busca ahí primero.
- **Prototipos (2026-11-07):** puede probar un diseño en una copia temporal fuera del proyecto si lo declara como prototipo, sin presentarlo como el cambio verificado.
- **Guard de escritura:** en Claude Code, `hooks/architect_write_guard.py` bloquea `Edit`, `Write` y `NotebookEdit` del agente salvo en `.md`, `.mmd` y prototipos en el directorio temporal fuera del proyecto. `Bash`, Copilot, Codex y el modo skill siguen dependiendo de las instrucciones.
- **Evidencia (2026-11-07):** usa el historial de git para medir el costo de cambio en revisiones estructurales, y verifica en fuentes actuales los datos de tecnología que cambian con el tiempo, o los marca como no verificados.
- **Skills:** manuales que el agente abre según la tarea. Un `SKILL.md` corto, con material de consulta aparte.

## Cómo está armado

```
plugins/architect/
├── src/architect.md          fuente única del agente (editar acá)
├── agents/, com.github.copilot/agents/, com.openai.codex/agents/, skills/architect/   generados desde src/
├── hooks/                    guard de escritura del agente (solo Claude Code)
├── skills/<skill>/
│   ├── SKILL.md              cuándo usarla y el método (menos de 500 líneas)
│   ├── references/           material de consulta; se lee solo el archivo que hace falta
│   ├── assets/               plantillas (solo architecture-decisions)
│   └── evals/                casos de prueba de la skill; el agente nunca los lee
├── evals/                    casos del agente completo e HISTORY.md con el historial de evaluaciones
└── scripts/
    ├── build_agents.py       genera los 4 formatos del agente
    ├── sync_vault.py         regenera references/ desde el vault de Obsidian
    └── vault_manifest.py     qué notas alimentan qué archivo
```

Reglas de mantenimiento:

- **Sin citas:** al sumar notas, revisar si aparecen pasajes textuales de libros y agregarlos a `scripts/quote_rewrites.py`. `quote_rewrites.py` es igual en ambos plugins.
- **No editar a mano** lo generado: `agents/`, `com.github.copilot/`, `com.openai.codex/`, `skills/architect/` ni los `references/` de `clean-architecture`, `domain-driven-design`, `software-design` y `architecture-decisions/references/decision-principles.md`. Se cambian en `src/` o en el vault.
- Se regeneran con `python3 scripts/build_agents.py` y `python3 scripts/sync_vault.py <ruta al vault developer-knowledge>`. Con `--check` fallan si algo quedó desactualizado.
- A mano quedan: `architecture-documentation/references/c4-mermaid.md`, `threat-modeling/references/common-threats.md` y los `SKILL.md`.
- El vault vive fuera de este repo. No se copian los PDFs de los libros y no deben entrar.
- Validar: `claude plugin validate .` desde `plugins/architect` y desde la raíz del repo.

## Integración con los otros roles

### Consultas de reviewer

Se agregó a `src/architect.md` un modo acotado para consultas delegadas por `reviewer`: conclusión, evidencia, supuestos/contraevidencia y recomendación con costo y alcance PR/seguimiento. Sin editar ni publicar, sin decidir la review final ni iniciar cadenas de delegación. `reviewer` conserva la coordinación y la conversación con la persona. Esta integración requiere evaluación conductual; no altera los resultados históricos ni el rol normal fuera de esa consulta.

### Conocimiento compartido y aprobaciones

Versión 0.1.1. El protocolo común se edita en `shared/decision-protocol.md` de la
raíz; `src/architect.md` lo incluye por marcador y el generador lo incorpora en los
cuatro formatos del rol. Las guías privadas en `skills/architect/references/shared/`
son generadas desde el propietario definido en `scripts/shared_guidance.py` de
la raíz: no editarlas ni sincronizarlas desde el vault directamente. Regenerar
ambos plugins al modificar una fuente compartida. Los paquetes funcionan sin
instalar el otro plugin; compartir conocimiento no amplía permisos ni roles.

Consultar nuevas decisiones de patrones, estructura, contratos y negocio antes
de implementarlas; verificar aprobaciones en cada handoff, conservar las ya
recibidas y seguir tareas independientes. El coordinador reúne preguntas y
controla ese paso. La lectura y consulta de reviewer conserva sus límites.
Evaluaciones y límites: `evals/shared-design-v1/summary.md` de la raíz.

### Lenguaje ubicuo compartido

`shared/ubiquitous-language.md` de la raíz se inserta en las instrucciones de los
cuatro roles. Mantener los términos acordados del negocio en requisitos, modelos,
código, tests, documentación, reviews y delegaciones; consultar ambigüedades antes
de introducir traducciones o sinónimos. Developer usa inglés para nombres técnicos,
con términos de dominio en el idioma acordado. No renombrar código existente fuera
del alcance ni traducir textos de usuario. Regenerar los tres plugins al cambiar
esa fuente; no editar las salidas. Evaluación: `evals/code-language-v1/` de la raíz.

## Proceso de revisión acordado

El objetivo es entender y justificar cada skill del agente arquitecto, no conservarlas porque las creó la IA ni completar un catálogo de libros. Una tarea puede ser útil y, aun así, no necesitar una skill separada si el agente ya la resuelve bien.

Para cada skill:

1. **Entender su propósito con el usuario:** qué problema concreto resuelve, un ejemplo de uso y cuándo no hace falta. Distinguirlo del propósito de las skills vecinas y del agente que las selecciona.
2. **Revisar sus instrucciones y referencias:** qué decisiones mejora, qué supuestos impone, dónde se superpone y qué proceso innecesario puede agregar. La revisión del texto no prueba su eficacia.
3. **Refinar solo con una razón concreta:** una ambigüedad, un error observado o una cobertura importante que falta. No agregar instrucciones para forzar un puntaje perfecto.
4. **Evaluar con y sin skill:** pedidos y archivos iguales, sesiones independientes, sin exponer criterios a quien responde; calificación ciega con evidencia. Separar los criterios críticos de los de cobertura o presentación. Un error que rompe una invariante de crédito no se compensa con acertar nombres o formatos.
5. **Interpretar el resultado:** un punto significa un criterio cumplido, no un porcentaje de calidad. Registrar errores, extensión y límites de la medición. Repetir para comprobar estabilidad y evaluar también al agente completo eligiendo skills.
6. **Decidir su destino:** conservar, acotar, fusionar o retirar según su aporte y costo. Si está bien encaminada, probarla en uso real antes de seguir ampliándola.

Estado de esta revisión conjunta:

- **`clean-architecture`:** el usuario indicó que ya la revisó. Se conserva como referencia para complementar las demás; quedan los pendientes históricos que figuran abajo.
- **`domain-driven-design`:** revisada, refinada y evaluada en esta conversación. Está bien encaminada; no se acordó seguir ampliándola por el punto perdido de repositorios. Sigue la prueba en casos reales y de estabilidad.
- **Lenguaje ubicuo en DDD:** está en las instrucciones como primer paso estratégico. Los casos prueban diferencias de significado entre contextos, pero no prueban explícitamente cómo el agente ayuda a descubrir, negociar y validar lenguaje compartido con expertos ni cómo lo conecta con código y pruebas. Es una cobertura pendiente de evaluación, no una ausencia de la skill.
- **`software-design`:** revisada, refinada y evaluada; 20/20 frente a 16/20 en tres casos. Se conserva con foco en callers, conocimiento y contratos. La señal es favorable en concreción de la propuesta, no demuestra ventaja en detectar el fallo crítico del caso nuevo. Ver resultados y límites en `evals/HISTORY.md`.
- **Cierre de `software-design`:** el usuario dio conformidad para continuar. Se cierra esta ronda de refinamiento; queda probarla en uso real, sin seguir ampliándola por el puntaje.
- **Las otras tres:** análisis de propósito y utilidad en `evals/HISTORY.md`; pendientes de revisión detallada. La próxima recomendada es `architecture-decisions`; su revisión aún no comenzó.

## Propósito de cada skill

Este análisis sale de los `SKILL.md`, del enrutamiento en `src/architect.md` y de los casos/criterios existentes. Los puntajes históricos son señales de una sola corrida; no constituyen una demostración de calidad ni permiten comparar skills con tareas distintas.

| Skill | Pregunta que ayuda a responder | Ejemplo concreto | Qué aporta frente a las vecinas |
|---|---|---|---|
| `clean-architecture` | ¿Qué depende de qué y dónde vive cada responsabilidad? | El caso de uso depende del ORM: decidir qué interfaz introducir y quién la posee. | Estructura de dependencias, capas y límites entre política y detalles. |
| `domain-driven-design` | ¿Qué significa el negocio y qué reglas deben mantenerse juntas? | Dos áreas entienden distinto “cliente”; dos pedidos compiten por crédito. | Lenguaje, modelos, contextos e invariantes; no determina por sí sola el despliegue. |
| `software-design` | ¿Esta interfaz simplifica el trabajo de quien la usa? | Una API de archivos obliga a cada caller a conocer región, reintentos y errores de S3. | Ocultamiento de información, contratos y costo de uso dentro de módulos. |
| `architecture-decisions` | ¿Qué opción conviene dadas las restricciones y por qué? | Sacar mails del checkout: comparar una cola de jobs con operar un broker. | Drivers, alternativas, costos, incertidumbre y registro de la decisión. |
| `architecture-documentation` | ¿Cómo explicamos el sistema a esta audiencia con evidencia? | Onboarding técnico frente a un diagrama para gerencia. | Selección de vistas y nivel de detalle, relaciones reales y discrepancias con documentación. |
| `threat-modeling` | ¿Cómo se puede abusar del diseño y qué cambiamos primero? | Un usuario cambia un ID y accede a documentos de otro cliente. | Activos, límites de confianza, escenarios de ataque y mitigaciones verificables. |

El análisis detallado de cada una está en `evals/HISTORY.md`.

## Cómo vamos

Cada caso se corrió con y sin skill, y se calificó contra una lista de criterios verificables. Los números son puntos cumplidos sobre el total.

| Skill | Con skill | Sin skill | Estado |
|---|---|---|---|
| `clean-architecture` | 19/20 | 12/20 | Señal favorable en los casos existentes; revisada por el usuario |
| `architecture-documentation` | 13/13 | 9/13 | Señal favorable en los casos existentes |
| `threat-modeling` | 14/15 → 17/17 tras corregirla | 11/15 | Señal favorable; corrección sin nueva comparación completa |
| `architecture-decisions` | 12/14 → 13/14 tras corregirla | 13/14 | Aporte diferencial no demostrado; un error pendiente |
| `domain-driven-design` | 19/20 | 16/20 | Versión refinada; tres casos, una corrida por variante |
| `software-design` | 20/20 | 16/20 | Versión refinada; tres casos, una corrida por variante |
| `architect` (agente) | 29/30, sin fallos críticos | — | Versión actual, una corrida por caso en modo skill (2026-11-07); ver `evals/HISTORY.md` |

Las 7 skills pasan la revisión estática: nombre igual a la carpeta, descripción de 300 caracteres o menos, `SKILL.md` de menos de 500 líneas, referencias existentes y citadas, y sin restos de Obsidian.

### Cuánto confiar en los números

- Cada versión corrió **una sola vez** por caso. Una diferencia chica es una señal débil.
- Muchos criterios pasan igual con y sin skill porque los casos plantan fallas obvias. Las reevaluaciones de DDD y software-design aportan evidencia adicional, pero todavía no establecen estabilidad ni una ventaja general en problemas difíciles.
- Algunos criterios eran permisivos o juntaban dos cosas.
- Las respuestas con skill son más largas. En `clean-architecture`, unas 1,8 veces. No se midió si lo extra aporta.

### Problemas conocidos

1. **`architecture-decisions`:** la sección "Consecuencias" de un ADR todavía afirma datos no verificados como hechos.
2. **`domain-driven-design`:** la corrida anterior dejó abierta la carrera de crédito y no mostró comportamiento en el agregado. Ambos problemas se resolvieron en la respuesta con skill de la reevaluación; falta comprobar estabilidad. La nueva respuesta omitió explicitar repositorios por raíz (detalle en `evals/HISTORY.md`).
3. **`clean-architecture`:** dejó la regla de suspensión de clientes en el caso de uso y no en el dominio. Es una mejora a la skill, y también hay que dividir el criterio, que juntaba precios y suspensión.
4. **`threat-modeling`:** en el caso grande escribe unas 1.800 palabras. Está dentro del límite que se fijó (unas 2.000), pero es largo.
5. **`architect`:** falta un caso para el uso del historial de git como evidencia (necesita un fixture con historial) y repetir corridas para estabilidad. La última ronda fue en modo skill; el hook se probó aparte.

## Qué sigue

1. **`architecture-decisions`:** próxima revisión conjunta. Revisar decisión frente a registro, corregir afirmaciones no verificadas también en Consecuencias y probar sin imponer una tecnología ganadora.
2. **`software-design`:** ya revisada y evaluada. Probar en uso real, comprobar estabilidad y proporcionalidad, y separar las condiciones independientes de la rúbrica antes de futuras corridas. No ampliarla solo por el puntaje.
3. **`architecture-documentation`:** revisar evidencia, audiencia y utilidad de las vistas; probar discrepancias y renderizado.
4. **`threat-modeling`:** revisar proporcionalidad y riesgos concretos; repetir comparación completa y agregar un caso con controles ya implementados.
5. **`domain-driven-design`:** probar en uso real y repetir para estabilidad. Agregar cobertura de descubrimiento y validación del lenguaje ubicuo. No seguir ampliándola solo para completar el punto de repositorios.
6. **`clean-architecture`:** conservar como revisada; atender el pendiente histórico de suspensión en dominio y dividir el criterio que mezcla reglas.
7. **`architect`:** después, evaluar selección de skills y tareas que crucen varias, incluida una tarea simple que no necesite cargar ninguna.

## Cómo evaluar sin contaminar

Se usa el procedimiento de subagentes independientes descrito en la reevaluación de DDD, sin invocar `claude plugin eval`. No cambiar de herramienta de evaluación ni asumir costos adicionales sin necesidad.

- Preparar fuera del repo una copia de la skill y sus referencias **sin `evals/`**, y copias de los pedidos sin metadatos de evaluación. La variante sin skill solo recibe pedido y archivos de ejemplo. No exponer otras respuestas, criterios ni historial de la revisión a quienes resuelven.
- No mover los `evals/` originales para lograr aislamiento: trabajar con copias filtradas. En corridas antiguas, cuatro respuestas vieron nombres de criterios mediante `ls -R`; se descartaron y repitieron.
- Mantener iguales modelo, pedido, archivos y condiciones entre variantes. Registrar diferencias si no se puede controlar alguna. Repetir cada caso cuando se quiera concluir estabilidad.
- Calificar con otros subagentes sin contexto previo, respuestas A/B asignadas al azar y los mismos criterios para ambas. Exigir evidencia y revisar la justificación; el juez también puede equivocarse.
- Distinguir fallos críticos de omisiones secundarias. Separar condiciones independientes en criterios distintos y no dar por inválida una solución alternativa correcta. Revisar la rúbrica antes de la siguiente corrida; si cambia, recalificar ambas variantes y dejar constancia.
- Registrar resultado por caso, fallos, extensión, versión/rúbrica utilizada y límites de la conclusión. Un mayor puntaje no basta para decidir conservar una skill.
- Los artefactos crudos se mantienen fuera del repo. Registrar su ubicación y advertir que los temporales pueden desaparecer; el resumen durable de cada ronda va a `evals/HISTORY.md`, y el estado actual, a este archivo.
- En los casos del agente, extraer `trace.json` de la transcripción con `eval_suite.py trace` para que el juez vea skills y escrituras reales. Marcar `fixtures_immutable: true` donde el agente no debe tocar archivos: `report` lo comprueba por hash.
- Las reglas comunes de la raíz (`AGENTS.md`, "Al crear o modificar agentes") prevalecen: usar `eval-harness`, sesiones independientes y ningún script que invoque modelos pagos.

## Decisiones abiertas

- **Citas de libros:** resuelto el 2026-11-04: el repo es público y no publica citas. `sync_vault.py` descarta las citas en bloque y reescribe los pasajes de `scripts/quote_rewrites.py`. El vault privado las conserva. Siguen en el historial de git de antes de ese cambio; reescribirlo es una decisión aparte.
- **Dos copias de `clean-architecture`:** también existe en `skillswap/.claude/skills/clean-architecture`. La del plugin es la que se mantiene. Falta decidir si skillswap pasa a usar la del plugin.
- **Codex:** falta probar una sesión real con modelo y el agente TOML. Solo se verificó la instalación y la carga de skills. Si Codex permite incluir agentes en plugins, reemplazar el archivo suelto.
- **Nombre del agente en Copilot:** con `--plugin-dir`, el agente se llama `architect:architect`, no `architect`.
