# Historial de evaluaciones del plugin `architect`

Registro durable de cada ronda, de la más reciente a la más antigua. El estado actual y lo que sigue están en `../AGENTS.md`. Los artefactos crudos citados vivían en carpetas temporales y pueden no existir ya.

## Re-evaluación final — 2026-11-07

Después de los cambios de esta fecha (guard, prototipos, planes guardados, evidencia de git y fuentes actuales, descripciones recortadas). Versión evaluada: `agents/architect.md` sha256 `a04c58580710`.

**Cómo se corrió:** subagentes independientes, sin scripts que invoquen modelos. Cada uno recibió el `SKILL.md` del rol y las skills en una copia del plugin sin `evals/` (modo skill, sin el hook ni el Skill tool), una carpeta aislada y el pedido. `trace.json` se extrajo de su transcripción. Calificó un juez independiente por caso sobre el paquete ciego de `blind`. `report` controló hashes en los casos `fixtures_immutable`. Una corrida por caso.

| Caso | Puntos | Palabras | Skills leídas |
|---|---|---|---|
| `boundaries-and-interface` | 4/4 | 1026 | `clean-architecture`, `software-design` |
| `document-and-threats` | 5/5 | 1317 | `architecture-documentation`, `threat-modeling` |
| `domain-and-record` | 4/4 | 2543 | `architecture-decisions`, `domain-driven-design` |
| `refactor-request-handoff` | 7/7 | 1180 | ninguna |
| `respect-project-principles` | 4/5 | 1022 | ninguna |
| `small-question` | 2/2 | 37 | ninguna |
| `tech-choice-currency` | 3/3 | 846 | `architecture-decisions` |
| **Total** | **29/30**, sin fallos críticos | | |

- **Planes guardados:** en `refactor-request-handoff` escribió `docs/plans/2026-11-07-separar-politica-de-precios.md` con tabla de decisiones (estado y fuente) y no tocó el código; `report` confirmó los hashes.
- **Prototipos:** tres casos prototiparon en el directorio temporal fuera del proyecto, lo declararon y lo borraron. Ninguno presentó el resultado como el cambio verificado.
- **Fuentes actuales:** `tech-choice-currency` consultó y citó cinco páginas oficiales con fecha.
- **Punto perdido (`05-no-plan-file`):** el criterio pedía "ninguna escritura" y el prototipo temporal contó como tal. Choca con la decisión de permitir prototipos; se corrigió la redacción para la próxima ronda. El puntaje queda registrado con el criterio anterior.
- **Límites:** modo skill, no el agente de Claude Code con hook; una corrida por caso, sin variante de comparación, así que no hay `pass@k` ni estabilidad. La detección de skills por comando registró un falso `B` en un caso porque leyó con una variable de shell.
- **Artefactos crudos:** `/tmp/claude-1000/-home-fmartinezvidal-Documents-github/ecb9e8fd-4c0f-45a5-bf31-11a7448e0987/scratchpad/final/`, temporal.

## Evaluación del agente — 2026-11-07

Primera ronda de los 6 casos con el agente real (`--agent architect:architect`) en Claude Code, modelo `claude-opus-5-5`, con hook de escritura activo. Una corrida por caso, sin variante de comparación. Plugin copiado sin `evals/` ni scripts, y cada caso en una carpeta aislada. Jueces: una sesión independiente por caso, con `trace.json` extraído de la transcripción. Las sesiones se lanzaron con `claude -p` desde un script fuera del repo; costo informado de quienes respondieron: USD 7,60, sin contar jueces.

| Caso | Puntos | Palabras | Skills cargadas |
|---|---|---|---|
| `boundaries-and-interface` | 4/4 | 1052 | `software-design`, `clean-architecture` |
| `document-and-threats` | 5/5 | 1229 | `architecture-documentation`, `threat-modeling` |
| `domain-and-record` | 4/4 | 2456 | `domain-driven-design`, `architecture-decisions` |
| `refactor-request-handoff` | 5/6 | 622 | ninguna |
| `respect-project-principles` | 4/4 | 977 | `clean-architecture`, `software-design` |
| `small-question` | 2/2 | 38 | ninguna |

- **Sin cambios en fixtures:** `report` comparó hashes en los dos casos marcados `fixtures_immutable` y no encontró violaciones.
- **Punto perdido (`05-checks`):** el agente escribió el refactor propuesto con `Bash` en un `mktemp -d`, corrió las pruebas ahí, borró la copia e informó que pasaban. Lo declaró y la traza lo confirma, pero el criterio prohíbe afirmar que corrieron comprobaciones del código refactorizado. `respect-project-principles` usó la misma técnica, con una comparación diferencial. El hook no lo cubre porque va por `Bash`. **Decisión del usuario (2026-11-07):** se permite prototipar en una copia temporal si se declara; se ajustaron `src/architect.md`, el hook y el criterio `05-checks`. Falta repetir los dos casos afectados con la versión nueva.
- **Límites:** versión evaluada `agents/architect.md` sha256 `c72297751d4d`; la actual incorpora la consulta de `reviewer` y no fue evaluada. Con una sola corrida no se puede hablar de estabilidad ni de aporte frente a otra variante. En la sesión también estaban los demás plugins y la configuración del usuario, sin el aislamiento de un entorno limpio. El bloqueo del hook no se disparó en esta ronda: se comprobó en una prueba aparte con `--agent`.
- **Artefactos crudos:** `/tmp/claude-1000/-home-fmartinezvidal-Documents-github/ecb9e8fd-4c0f-45a5-bf31-11a7448e0987/scratchpad/evalround/`, temporal; puede desaparecer.

## Reevaluación de `software-design` — 2026-11-03

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

## Reevaluación de `domain-driven-design` — 2026-11-03

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

## Análisis de propósito y utilidad — 2026-11-03

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

## Ronda integral iniciada el 2026-11-04 (sin cerrar)

Quedó abierta: sus artefactos estaban en `/private/tmp/architect-final-evaluation/`, en otra máquina, y no se recuperaron. Para el agente, la reemplaza la evaluación del 2026-11-07.

Nota del 2026-11-04: esta ronda es anterior a la división actual, así que sus resultados del agente reflejan el rol anterior. El caso `create-package-refactor` pasó a `developer` como `implement-package-refactor`, y acá lo reemplaza `refactor-request-handoff`. El usuario pidió dejar todas las skills validadas y útiles, y aclaró entonces que el arquitecto debía funcionar como consultor y creador, también para refactors de packages/módulos/capas, respetando principios acordados. La ronda actual incluye 27 casos: 21 de las seis especialistas (con/sin skill) y seis del agente. Hay 48 respuestas previstas, con reutilización explícita de nueve respuestas previas cuyo pedido coincide (software-design sin cambios de instrucciones y tres baselines de DDD).

- Estado vivo y artefactos: `/private/tmp/architect-final-evaluation/manifest.json`, `runs/`, `contexts/`, `grading/` y `attempts/`.
- Hubo dos correcciones basadas en fallos reales: puntuación inválida en un diagrama de secuencia y omisión de la regla de suspensión en una revisión. Se conservan las primeras respuestas y sus calificaciones en `attempts/`; se repitieron los casos con sesiones nuevas.
- Los ejemplos de Mermaid y los diagramas actuales de documentation con skill renderizaron; la variante sin skill mantiene un fallo de sintaxis registrado. Las imágenes con skill y los ejemplos fueron inspeccionados visualmente.
- Antes de declarar cierre, faltan las respuestas del agente que estén pendientes en el manifest, completar calificaciones y conservar un resumen durable. No interpretar las tablas históricas de abajo como el resultado final de esta ronda.
