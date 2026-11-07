# AGENTS.md — estado del plugin `architect`

Estado al **2026-11-03**. Este archivo es para quien continúe el trabajo, persona o agente. Resume qué hay, cómo se mantiene, cómo vamos con cada skill y qué sigue. El uso del plugin está en `README.md`.

## Qué es

Un agente de arquitectura de software y 6 skills, instalable en **Claude Code**, **GitHub Copilot CLI** y **Codex**. **Codex** carga el plugin y sus skills, probado el 2026-11-04 con `codex-cli` 0.166 en un `CODEX_HOME` aislado, tanto local como desde GitHub. Sus plugins no incluyen agentes, así que el rol llega como skill y hay un agente TOML opcional en `com.openai.codex/agents/`.

- **Agente:** `architect`. Planea, diseña y consulta sobre interfaces, packages, módulos, capas o sistemas completos, y no edita código. Produce análisis, diseños, ADRs, diagramas y planes. Si le piden implementar, entrega un plan para el agente `developer`. Esta división la pidió el usuario el 2026-11-04 y reemplaza a la anterior, en la que también implementaba refactors. Identifica y respeta los principios del proyecto y ADRs aceptados; distingue propuestas pendientes. Estas reglas son instrucciones, no bloqueos técnicos.
- **Skills:** manuales que el agente abre según la tarea. Un `SKILL.md` corto, con material de consulta aparte.

## Cómo está armado

```
plugins/architect/
├── src/architect.md          fuente única del agente (editar acá)
├── agents/, com.github.copilot/agents/, com.openai.codex/agents/, skills/architect/   generados desde src/
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

- **Sin citas:** al sumar notas, revisar si aparecen pasajes textuales de libros y agregarlos a `scripts/quote_rewrites.py`. `quote_rewrites.py` es igual en ambos plugins.
- **No editar a mano** lo generado: `agents/`, `com.github.copilot/`, `com.openai.codex/`, `skills/architect/` ni los `references/` de `clean-architecture`, `domain-driven-design`, `software-design` y `architecture-decisions/references/decision-principles.md`. Se cambian en `src/` o en el vault.
- Se regeneran con `python3 scripts/build_agents.py` y `python3 scripts/sync_vault.py <ruta al vault developer-knowledge>`. Con `--check` fallan si algo quedó desactualizado.
- A mano quedan: `architecture-documentation/references/c4-mermaid.md`, `threat-modeling/references/common-threats.md` y los `SKILL.md`.
- El vault vive fuera de este repo. No se copian los PDFs de los libros y no deben entrar.
- Validar: `claude plugin validate .` desde `plugins/architect` y desde la raíz del repo.

## Ronda integral en curso

Nota del 2026-11-04: esta ronda es anterior a la división actual, así que sus resultados del agente reflejan el rol anterior. El caso `create-package-refactor` pasó a `developer` como `implement-package-refactor`, y acá lo reemplaza `refactor-request-handoff`. El usuario pidió dejar todas las skills validadas y útiles, y aclaró entonces que el arquitecto debía funcionar como consultor y creador, también para refactors de packages/módulos/capas, respetando principios acordados. La ronda actual incluye 27 casos: 21 de las seis especialistas (con/sin skill) y seis del agente. Hay 48 respuestas previstas, con reutilización explícita de nueve respuestas previas cuyo pedido coincide (software-design sin cambios de instrucciones y tres baselines de DDD).

- Estado vivo y artefactos: `/private/tmp/architect-final-evaluation/manifest.json`, `runs/`, `contexts/`, `grading/` y `attempts/`.
- Hubo dos correcciones basadas en fallos reales: puntuación inválida en un diagrama de secuencia y omisión de la regla de suspensión en una revisión. Se conservan las primeras respuestas y sus calificaciones en `attempts/`; se repitieron los casos con sesiones nuevas.
- Los ejemplos de Mermaid y los diagramas actuales de documentation con skill renderizaron; la variante sin skill mantiene un fallo de sintaxis registrado. Las imágenes con skill y los ejemplos fueron inspeccionados visualmente.
- Antes de declarar cierre, faltan las respuestas del agente que estén pendientes en el manifest, completar calificaciones y conservar un resumen durable. No interpretar las tablas históricas de abajo como el resultado final de esta ronda.

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
- **`software-design`:** revisada, refinada y evaluada; 20/20 frente a 16/20 en tres casos. Se conserva con foco en callers, conocimiento y contratos. La señal es favorable en concreción de la propuesta, no demuestra ventaja en detectar el fallo crítico del caso nuevo. Ver resultados y límites abajo.
- **Cierre de `software-design`:** el usuario dio conformidad para continuar. Se cierra esta ronda de refinamiento; queda probarla en uso real, sin seguir ampliándola por el puntaje.
- **Las otras tres:** análisis de propósito y utilidad realizado abajo; pendientes de revisión detallada. La próxima recomendada es `architecture-decisions`; su revisión aún no comenzó.

## Propósito y utilidad de las skills

Este análisis sale de los `SKILL.md`, del enrutamiento en `src/architect.md` y de los casos/criterios existentes. Los puntajes históricos son señales de una sola corrida; no constituyen una demostración de calidad ni permiten comparar skills con tareas distintas.

| Skill | Pregunta que ayuda a responder | Ejemplo concreto | Qué aporta frente a las vecinas |
|---|---|---|---|
| `clean-architecture` | ¿Qué depende de qué y dónde vive cada responsabilidad? | El caso de uso depende del ORM: decidir qué interfaz introducir y quién la posee. | Estructura de dependencias, capas y límites entre política y detalles. |
| `domain-driven-design` | ¿Qué significa el negocio y qué reglas deben mantenerse juntas? | Dos áreas entienden distinto “cliente”; dos pedidos compiten por crédito. | Lenguaje, modelos, contextos e invariantes; no determina por sí sola el despliegue. |
| `software-design` | ¿Esta interfaz simplifica el trabajo de quien la usa? | Una API de archivos obliga a cada caller a conocer región, reintentos y errores de S3. | Ocultamiento de información, contratos y costo de uso dentro de módulos. |
| `architecture-decisions` | ¿Qué opción conviene dadas las restricciones y por qué? | Sacar mails del checkout: comparar una cola de jobs con operar un broker. | Drivers, alternativas, costos, incertidumbre y registro de la decisión. |
| `architecture-documentation` | ¿Cómo explicamos el sistema a esta audiencia con evidencia? | Onboarding técnico frente a un diagrama para gerencia. | Selección de vistas y nivel de detalle, relaciones reales y discrepancias con documentación. |
| `threat-modeling` | ¿Cómo se puede abusar del diseño y qué cambiamos primero? | Un usuario cambia un ID y accede a documentos de otro cliente. | Activos, límites de confianza, escenarios de ataque y mitigaciones verificables. |

### `software-design`: foco definido y primera reevaluación favorable

Su aporte más específico es mirar la experiencia de los callers: una dependencia puede apuntar en la dirección correcta y seguir exponiendo una interfaz difícil, demasiadas opciones o conocimiento del proveedor. Clean Architecture puede justificar un puerto delgado; esta skill pregunta si el costo que agrega se paga. En un módulo de archivos, puede proponer una interfaz que oculte configuración y errores del SDK sin inventar soporte para proveedores que nadie necesita.

El riesgo de superposición es alto: ambas hablan de acoplamiento, límites, costo del cambio y revisión de módulos. El agente también la enruta para concurrencia, mientras DDD la necesita para invariantes; conviene distinguir concurrencia técnica de estado compartido de reglas del negocio. La skill no debería repetir una revisión completa de capas ni imponer varias alternativas para una consulta pequeña.

**Evidencia:** la evaluación histórica dio 14/14 frente a 13/14 en casos explícitos. Tras refinar la skill, aceptar varias formas válidas de interfaz en rate limiting y agregar el caso de importación, la reevaluación dio 20/20 frente a 16/20. Las ventajas fueron concretar alternativas, política ante fallos, firmas y comprobaciones. Ambas variantes resolvieron el criterio crítico de reintentos; no se demostró una ventaja de detección en ese escenario.

**Recomendación:** conservar con el alcance refinado y probar en uso real. Su unidad de análisis es módulo más callers: conocimiento expuesto, orden, ciclo de vida, resultados y recuperación. No seguir ampliándola para mantener un puntaje perfecto. Falta comprobar estabilidad y si el detalle adicional ayuda al usuario; si el aporte no se sostiene, reconsiderar su separación de Clean Architecture.

### `architecture-decisions`: útil para decidir y preservar el razonamiento

Sirve cuando hay alternativas plausibles y elegir tiene consecuencias duraderas. También sirve cuando la decisión ya está tomada y solo hay que registrarla fielmente. Un ADR conserva contexto, decisión y consecuencias para que el equipo pueda entender después por qué eligió eso y cuándo reconsiderarlo. Para una elección pequeña y reversible, el propio texto pide una respuesta breve.

Se superpone con el agente: ambos piden comparar opciones, recomendar y separar hechos de supuestos. La parte distintiva de la skill es profundizar los drivers y mantener el historial de ADRs, incluidos cambios parciales. No debería producir un ADR para cualquier opinión técnica.

**Evidencia actual:** 12/14 y luego 13/14, frente a 13/14 sin skill; no demuestra una mejora general. Sí hay reglas operativas específicas útiles, pero queda un fallo conocido de presentar supuestos como hechos en Consecuencias. El criterio del caso de colas exige recomendar una cola de jobs de Rails; puede castigar una alternativa bien justificada. El caso de ADRs mide también fidelidad al registro, que es un objetivo distinto de elegir tecnología.

**Recomendación provisional:** conservar, corregir el problema de hechos/supuestos al revisar esta skill y evaluar por separado decisión y registro. Probar opciones defendibles sin imponer una tecnología ganadora de antemano.

### `architecture-documentation`: responsabilidad distinta y aporte observado

Convierte evidencia del sistema en una explicación para alguien concreto. C4 organiza las vistas: contexto para personas y sistemas externos; contenedores para aplicaciones, procesos y almacenes; componentes para una parte interna que necesite más detalle. Su utilidad es elegir qué mostrar y comprobar conexiones, no producir más diagramas. Puede detectar que el README dice Kafka mientras el despliegue y el código usan RabbitMQ.

Se relaciona con las demás porque comunica sus resultados, pero no sustituye modelar el negocio, decidir una alternativa ni analizar amenazas. Un diagrama puede describir fielmente una arquitectura problemática.

**Evidencia actual:** 13/13 frente a 9/13; señal favorable. Parte del puntaje corresponde a notación y presentación, además de discrepancias verificables. No se comprobó todavía que alguien nuevo entienda mejor el sistema ni que todos los diagramas se rendericen mediante una herramienta.

**Recomendación provisional:** conservar. En la próxima revisión, probar documentación incompleta o contradictoria, comprobar renderizado y evaluar si el lector puede responder preguntas concretas sobre el sistema. Evitar agregar vistas que no ayuden a esa audiencia.

### `threat-modeling`: perspectiva distinta que merece conservarse

Agrega preguntas que las otras skills no cubren sistemáticamente: quién podría abusar de una capacidad, qué límite de confianza cruza, qué activo queda expuesto y cómo verificar la mitigación. STRIDE funciona como recordatorio de clases de amenaza; la salida útil es el escenario concreto y su corrección priorizada. No reemplaza una auditoría de código ni certifica que el sistema sea seguro.

Su mapa de flujos se parece a un diagrama de arquitectura, pero está organizado alrededor de confianza y amenazas. Reutilizar evidencia y diagramas entre ambas puede evitar trabajo repetido. El riesgo es responder con un catálogo genérico o un informe excesivo para una consulta pequeña.

**Evidencia actual:** 14/15 frente a 11/15; después de corregir formato/proporción obtuvo 17/17, sin nueva comparación completa contra la variante sin skill. Cambió la rúbrica, por lo que el aumento no demuestra por sí solo una mejora equivalente. Sigue pendiente controlar extensión y comprobar riesgos menos evidentes que los plantados en los casos actuales.

**Recomendación provisional:** conservar. Revisar escenarios concretos, priorización y proporcionalidad; usar también un diseño con controles ya resueltos para comprobar que no inventa vulnerabilidades ni recomienda controles innecesarios.

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
| `architect` (agente) | — | — | Solo una pregunta de prueba, en Claude Code y Copilot |

Las 7 skills pasan la revisión estática: nombre igual a la carpeta, descripción de menos de 1024 caracteres, `SKILL.md` de menos de 500 líneas, referencias existentes y citadas, y sin restos de Obsidian.

### Cuánto confiar en los números

- Cada versión corrió **una sola vez** por caso. Una diferencia chica es una señal débil.
- Muchos criterios pasan igual con y sin skill porque los casos plantan fallas obvias. Las reevaluaciones de DDD y software-design aportan evidencia adicional, pero todavía no establecen estabilidad ni una ventaja general en problemas difíciles.
- Algunos criterios eran permisivos o juntaban dos cosas.
- Las respuestas con skill son más largas. En `clean-architecture`, unas 1,8 veces. No se midió si lo extra aporta.

### Reevaluación de `software-design` — 2026-11-03

**Cambios:** se acotó el alcance a módulo y callers, con seguimiento del conocimiento que comparten. Se explicitaron contratos de efectos, fallos parciales, orden y reintentos. Se corrigió la idea de que una capa delgada siempre sobra y se dejó de exigir múltiples alternativas para decisiones pequeñas. No se editaron las referencias generadas del vault. El enrutamiento se ajustó en `src/architect.md` y se regeneraron las tres salidas del agente con `build_agents.py`.

**Casos:** se conservaron los dos existentes, se corrigió `05-somewhat-general` para aceptar primitivas, limitadores configurados o fachadas justificadas, y se agregó `review-import-contract`. El caso nuevo tiene dependencias internas correctas, conocimiento de CSV duplicado en callers, commits parciales y un wrapper que sí autoriza. El criterio `02-critical-retry-safety` se identifica como crítico, independientemente del total.

Se corrieron seis respuestas con subagentes independientes sin historial compartido ni acceso autorizado a rúbricas: tres con la copia refinada y tres sin skill. Se usaron pedidos idénticos y copias separadas de fixtures. Otros tres subagentes calificaron pares A/B aleatorios sin saber la variante; se revisaron sus justificaciones. Modelo heredado de la sesión sin overrides; no se fijó su versión exacta. No se invocó `claude plugin eval`.

| Caso | Con skill | Sin skill | Palabras con / sin |
|---|---|---|---|
| `design-rate-limiter-interface` | 6/6 | 4/6 | 980 / 545 |
| `review-pass-through-layers` | 8/8 | 7/8 | 824 / 603 |
| `review-import-contract` | 6/6 | 5/6 | 1257 / 945 |
| **Total** | **20/20** | **16/20** | **3061 / 2093** |

- **Rate limiting:** la respuesta con skill comparó políticas por llamada frente a limitadores configurados y eligió uno; también concretó el comportamiento de API y SMS ante una caída. Sin skill hubo una propuesta válida, pero sin segunda alternativa ni recomendación específica de política ante esa caída. Es una diferencia de cobertura y concreción, no evidencia de una implementación incorrecta.
- **Archivos:** ambas detectaron configuración y SDK filtrados hacia el controller, delegación vacía y el coste del prechequeo de borrado. Con skill hubo una interfaz TypeScript concreta; sin ella se describió la simplificación sin firmas concretas.
- **Importación:** ambas reconocieron el conocimiento de formato duplicado, preservaron la autorización y explicaron estado durable/identidad/unicidad para recuperación. **Ambas aprobaron el criterio crítico.** La diferencia de puntaje fue proponer escenarios observables de comprobación; no una ventaja demostrada en seguridad de reintentos.
- **Coste de extensión:** con skill hubo unas 1.46 veces más palabras en total. No se midió si el usuario necesita todo ese detalle. Es un aspecto a observar en uso real, no una mejora automática.
- **Conclusión:** conservar por ahora, con foco más claro y una señal favorable en propuestas concretas. No concluir que evita cuatro errores críticos adicionales ni que 20/20 significa calidad perfecta. Tampoco se comparó la skill anterior contra la refinada: la comparación actual fue refinada frente a conocimiento general.
- **Límites de la rúbrica:** parte del puntaje premia alternativas y presentación de firmas. El criterio de proporcionalidad del caso nuevo también incluye verificación; separar esas condiciones en la próxima revisión de rúbrica permitiría atribuir mejor la diferencia. Los 14/14 y 13/14 históricos no son directamente comparables con el nuevo total de 20 ni con el criterio modificado.
- **Pendiente:** repetir para estabilidad, probar pedidos menos explícitos y negativos (el diseño ya es suficiente), medir decisiones/costos para el usuario y probar selección automática por el agente completo. Los casos evalúan respuestas; no se ejecutaron implementaciones, Redis ni pruebas concurrentes de los diseños propuestos.
- **Validación:** `quick_validate.py`, YAML de los casos y criterios, referencias existentes, límite de líneas, `git diff --check`, `build_agents.py --check` y manifiestos de plugin/marketplace pasaron. Persisten los avisos preexistentes de licencia e icono para publicar en el directorio.
- **Artefactos:** `/private/tmp/architect-software-design-evaluation/` contiene respuestas, pares A/B, calificaciones, resumen y hashes de skill/rúbricas en `metadata.json`. Está fuera del repo y puede desaparecer al limpiar temporales. Se reutilizó el entorno virtual con PyYAML de la revisión de DDD.

### Reevaluación de `domain-driven-design` — 2026-11-03

Se ejecutaron los tres casos con y sin la skill refinada, con subagentes independientes sin historial compartido. Cada ejecución recibió solo el pedido y, en la variante correspondiente, una copia de la skill y sus referencias sin `evals/`. Otros subagentes calificaron pares A/B con asignación aleatoria, sin conocer qué variante usó la skill. Se aplicaron los mismos criterios binarios a ambas respuestas y se revisaron las justificaciones. No se invocó `claude plugin eval`.

| Caso | Con skill | Sin skill | Palabras con / sin |
|---|---|---|---|
| `aggregate-boundaries` | 7/8 | 5/8 | 948 / 950 |
| `split-marketplace-monolith` | 8/8 | 7/8 | 1317 / 833 |
| `context-boundary-evidence` | 4/4 | 4/4 | 1106 / 1087 |
| **Total** | **19/20** | **16/20** | **3371 / 2870** |

- **Crédito:** con skill se explicó el control de versión, rollback completo y recarga/validación al reintentar, con el ejemplo de dos pedidos concurrentes. También se mostró comportamiento en `Order`. Sin skill faltó proteger explícitamente la liberación contra duplicados, mostrar comportamiento del agregado en TypeScript y explicitar la referencia a producto por ID.
- **Punto perdido con skill:** no explicitó repositorios por raíz ni los mostró; solo excluyó un repositorio independiente para las líneas. Es una omisión de la respuesta, no evidencia de una implementación incorrecta.
- **Marketplace:** la diferencia de puntaje fue nombrar los patrones de relación en el mapa. La respuesta con skill fue aproximadamente 1,58 veces más larga; el puntaje no demuestra que toda esa extensión aporte.
- **Caso nuevo:** ambas variantes pasaron todo. Este caso no distinguió el aporte de la skill en esta corrida.
- **Límites:** una corrida por caso y variante, con evaluación por modelo. Son pruebas de respuestas de subagentes, no de activación automática ni del agente en Claude Code/Copilot. Los 15/16 y 14/16 anteriores no son directamente comparables: cambió el criterio de crédito y se agregó un caso. Falta repetir las corridas para estimar estabilidad.
- **Validación estática:** `quick_validate.py` pasó con PyYAML 6.0.3 instalado en el entorno virtual temporal `/private/tmp/architect-ddd-validation`. Manifiestos del plugin y marketplace válidos; la validación del directorio de publicación sigue señalando falta de licencia e icono. No se modificó el Python del sistema.
- **Artefactos crudos y calificaciones:** `/private/tmp/architect-ddd-evaluation/`, fuera del repo; pueden desaparecer al limpiar temporales.

### Problemas conocidos

1. **`architecture-decisions`:** la sección "Consecuencias" de un ADR todavía afirma datos no verificados como hechos.
2. **`domain-driven-design`:** la corrida anterior dejó abierta la carrera de crédito y no mostró comportamiento en el agregado. Ambos problemas se resolvieron en la respuesta con skill de la reevaluación; falta comprobar estabilidad. La nueva respuesta omitió explicitar repositorios por raíz (ver detalle arriba).
3. **`clean-architecture`:** dejó la regla de suspensión de clientes en el caso de uso y no en el dominio. Es una mejora a la skill, y también hay que dividir el criterio, que juntaba precios y suspensión.
4. **`threat-modeling`:** en el caso grande escribe unas 1.800 palabras. Está dentro del límite que se fijó (unas 2.000), pero es largo.
5. **`architect`:** falta una evaluación completa.

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
- Los artefactos crudos se mantienen fuera del repo. Registrar su ubicación y advertir que los temporales pueden desaparecer; el resumen durable queda en este archivo.

## Decisiones abiertas

- **Citas de libros:** resuelto el 2026-11-04: el repo es público y no publica citas. `sync_vault.py` descarta las citas en bloque y reescribe los pasajes de `scripts/quote_rewrites.py`. El vault privado las conserva. Siguen en el historial de git de antes de ese cambio; reescribirlo es una decisión aparte.
- **Dos copias de `clean-architecture`:** también existe en `skillswap/.claude/skills/clean-architecture`. La del plugin es la que se mantiene. Falta decidir si skillswap pasa a usar la del plugin.
- **Codex:** falta probar una sesión real con modelo y el agente TOML. Solo se verificó la instalación y la carga de skills. Si Codex permite incluir agentes en plugins, reemplazar el archivo suelto.
- **Nombre del agente en Copilot:** con `--plugin-dir`, el agente se llama `architect:architect`, no `architect`.


## Consultas de reviewer (2026-11-07)

Se agregó a `src/architect.md` un modo acotado para consultas delegadas por `reviewer`: conclusión, evidencia, supuestos/contraevidencia y recomendación con costo y alcance PR/seguimiento. Sin editar ni publicar, sin decidir la review final ni iniciar cadenas de delegación. `reviewer` conserva la coordinación y la conversación con la persona. Esta integración requiere evaluación conductual; no altera los resultados históricos ni el rol normal fuera de esa consulta.
