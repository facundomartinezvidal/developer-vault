# AGENTS.md — estado del plugin `developer`

Estado al **2026-11-04**. Este archivo es para quien continúe el trabajo, persona o agente. El uso del plugin está en `README.md`.

## Qué es

Un agente de desarrollo y 17 skills para cualquier lenguaje, instalable en **Claude Code**, **GitHub Copilot CLI** y **Codex**, armado igual que `architect`. **Codex** carga el plugin y sus skills, probado el 2026-11-04 con `codex-cli` 0.166 en un `CODEX_HOME` aislado, tanto local como desde GitHub. Sus plugins no incluyen agentes, así que el rol llega como skill y hay un agente TOML opcional en `com.openai.codex/agents/`.

- **Agente:** `developer`. Trabaja como consultor y como realizador. Una pregunta o revisión produce análisis sin tocar archivos; un pedido de implementar, arreglar o refactorizar autoriza ese trabajo y su verificación dentro del alcance. Las convenciones del proyecto están por encima de las preferencias de los libros. Estas reglas son instrucciones, no bloqueos técnicos.
- **Lenguajes:** no está atado a ninguno. Descubre el toolchain del proyecto, escribe código idiomático y consulta la documentación de la versión instalada. `clean-code/references/across-languages.md` traduce los principios entre familias de lenguajes.
- **Frameworks:** `framework-practices` tiene guía profunda para ASP.NET Core y Spring Boot y, para cualquier versión o framework, consulta la documentación actual con Context7 o las fuentes oficiales. Si no puede verificar, lo dice.
- **Límite con `architect`:** el usuario definió esta división el 2026-11-04: `architect` planea, diseña y consulta, y no edita código; `developer` implementa lo planeado y consulta. Es decir, `architect` propone diseños para aprobación del usuario y `developer` implementa las decisiones aprobadas, con `implementing-designs`: las decisiones aceptadas son compromisos y las propuestas no. Las decisiones estructurales nuevas se derivan a `architect`. `developer` trabaja dentro de una función, una clase, un módulo o una funcionalidad. Las notas de `software-architecture/`, `component-principles/` y `domain-driven-design/`, y la mayoría de `software-design/`, siguen allá.

## Cómo está armado

```
plugins/developer/
├── src/developer.md          fuente única del agente (editar acá)
├── agents/, com.github.copilot/agents/, com.openai.codex/agents/, skills/developer/   generados desde src/
├── skills/<skill>/
│   ├── SKILL.md              cuándo usarla y el método (menos de 500 líneas)
│   ├── references/           generados desde el vault o escritos a mano (lo dice cada archivo)
│   └── evals/                casos de prueba; el agente nunca los lee
├── evals/                    casos del agente completo
└── scripts/
    ├── build_agents.py       genera los 3 archivos del agente
    ├── sync_vault.py         regenera references/ desde el vault
    ├── vault_manifest.py     qué notas alimentan qué archivo
    └── eval_suite.py         valida y prepara evaluaciones; no invoca modelos
```

Reglas de mantenimiento:

- **Versión:** Codex guarda los plugins por versión, así que conviene subirla en `plugin.json` y `.claude-plugin/plugin.json` al publicar cambios.
- **No editar a mano** `agents/`, `com.github.copilot/`, `com.openai.codex/`, `skills/developer/` ni los `references/` listados en `vault_manifest.py`. A mano quedan los `SKILL.md` y las referencias que no están en el manifest, que empiezan con "Hand-written".
- Las referencias a mano están escritas con palabras propias. No copiar texto de los libros ni de otras fuentes, también porque el repo puede publicarse.
- `sync_vault.py` no toca las referencias a mano. Si más adelante una nota del vault cubre el mismo tema, reemplazarla y borrar la copia manual.
- Regenerar: `python3 scripts/build_agents.py` y `python3 scripts/sync_vault.py <ruta a developer-knowledge>`. Con `--check` fallan si algo quedó desactualizado.
- **Sin citas:** al sumar notas, revisar si aparecen pasajes textuales de libros y agregarlos a `scripts/quote_rewrites.py`.
- Los scripts son copias adaptadas de los de `architect`. Si se corrige un error en uno, revisar el otro.
- El vault vive fuera del repo. No se copian los PDFs y no deben entrar.
- Validar: `claude plugin validate .` desde `plugins/developer` y desde la raíz del repo.

## De dónde sale el contenido

| Origen | Qué aporta |
|---|---|
| Notas del vault | Referencias sincronizadas por el manifest. |
| PDFs en `books/` sin notas | *Refactoring* caps. 2 y 6–12 (principios y catálogo), cap. 4 (tests); *Applying UML and Patterns* (GRASP); *Agile Principles, Patterns, and Practices* (Null Object, Gateway, tests). |
| Frameworks | `framework-practices` fusiona *ASP.NET Core in Action* 3.ª ed. (.NET 7) y *Spring Boot in Action* (Boot 1.3) con la documentación oficial, leída con Context7 y las webs de Microsoft y Spring. Si difieren, gana la documentación. De los libros se leyeron índices y resúmenes de capítulo, no el texto completo. |
| Investigación externa | Lo de abajo. |

De *Refactoring* se leyeron los capítulos 2 y 4 en parte, y del catálogo se tomó la lista de movimientos del índice: los pasos de cada movimiento se escribieron de conocimiento general y falta cotejarlos con el libro. GRASP y los otros patrones también se escribieron a partir del índice, sin leer esos capítulos completos.

Ninguna nota del vault se modificó; si el usuario estudia estos temas, las notas pueden reemplazar a las referencias manuales.

## Investigación: qué necesita un agente developer (2026-11-04)

**Conducta.** Lo más frecuente no es falta de conocimiento técnico, sino de disciplina. Por eso el agente lo tiene siempre cargado (sección "Where coding agents actually go wrong") y no en una skill:

- [How Coding Agents Fail Their Users](https://arxiv.org/abs/2605.29442) analiza 20.574 sesiones reales. Síntomas: violar una restricción explícita 38,33 %, malinterpretar la intención 26,95 %, informar mal el propio estado 22,58 %, implementación incorrecta 17,82 %, mal diagnóstico del proyecto 11,56 %, excederse del alcance 10,20 %. Son categorías con varias etiquetas, así que no suman 100 %.
- [What Breaks When LLMs Code?](https://arxiv.org/html/2605.30777v3) analiza 547 incidentes confirmados: violación de instrucciones 40,4 %, operaciones destructivas 24,5 %, saltear autorización 18,3 %, engaño 15,7 %, inventar datos 9,7 %, falsa seguridad 9,1 %. Corrección de bugs y configuración suman más del 65 %.
- [Slopsquatting](https://labs.cloudsecurityalliance.org/research/csa-research-note-slopsquatting-ai-supply-chain-20260419-csa/) resume la tasa de paquetes inventados por modelos. Por eso se pide verificar que un paquete exista.
- [Best practices de Claude Code](https://code.claude.com/docs/en/best-practices): darle un chequeo ejecutable y pedir evidencia de lo corrido. Las reglas sin excepciones se aplican con hooks, no con instrucciones.

**Cobertura técnica.** Se contrastó con estas fuentes para ver qué faltaba:

- [SWEBOK v4](https://www.computer.org/education/bodies-of-knowledge/software-engineering): sumó seguridad, operaciones y arquitectura como áreas propias. De ahí `secure-coding` y `production-readiness`, además de configuración (Git) y mantenimiento.
- [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction): cadena de suministro (A03) y manejo de condiciones excepcionales (A10) son categorías nuevas.
- [Guía de revisión de Google](https://google.github.io/eng-practices/review/reviewer/looking-for.html): base de `reviewing-code`.
- [Capacidades DORA](https://docs.cloud.google.com/architecture/devops): lotes chicos, automatización de tests y desarrollo sobre trunk.

Límites: son fuentes de distinta calidad, y los porcentajes salen de estudios con métodos distintos, con etiquetado apoyado en modelos. Sirven para priorizar, no como medida exacta. Las referencias técnicas salen sobre todo de práctica común y deben contrastarse con la documentación vigente.

## Commits (`writing-commits`)

Decisiones del usuario (2026-11-07):

- **Dónde viven las convenciones:** en `conventions/commits.md` de cada proyecto, con una línea en `AGENTS.md` que apunta ahí. Si faltan, la skill lo avisa y ofrece dos caminos: que las escriba la persona o crearlas con el default.
- **Default:** títulos de Conventional Commits 1.0 y cuerpos al estilo del proyecto Git. Está en `assets/default-commit-conventions.md`, que se copia al proyecto y por eso no empieza con "Hand-written".
- **Sin coautoría de modelos:** ningún commit acredita a un modelo o herramienta de IA, aunque la herramienta anfitriona lo pida.
- **Confirmación:** `developer` sugiere el commit y lo hace solo si la persona confirma. Un pedido de implementar no alcanza.
- **Hook opcional:** al crear las convenciones, la skill ofrece instalar `assets/commit-msg`, que rechaza mensajes que acreditan a un modelo o herramienta y deja pasar coautores humanos. Se probó con 8 mensajes y commits reales en un repo descartable; ninguna evaluación cubre todavía la oferta ni la instalación.
- **Commits atómicos:** cada commit agrupa lo relacionado. Si un cambio mezcla propósitos, la skill lo divide sin preguntar antes, también dentro de un mismo archivo, y lo informa.

Fuentes, leídas con Context7: especificación de Conventional Commits, `config-conventional` de commitlint, `SubmittingPatches` y `MyFirstContribution` de Git, `submitting-patches` del kernel de Linux, guía de descripciones de Google y Gitmoji. La guía de Angular no apareció en Context7.

Los límites del título no coinciden entre fuentes: Git usa 50, el kernel 70–75 y `config-conventional` 100, mientras que la referencia de reglas de commitlint muestra 72. El default usa 72 para título y cuerpo. Es una elección, no un estándar.

Son reglas por instrucción, no bloqueos técnicos.

## Pull requests (`opening-pull-requests`)

Es el par de `writing-commits` del lado de quien abre el PR. Para revisar el PR de otra persona está el plugin `reviewer`. Decisiones del usuario (2026-11-07):

- **Convenciones:** en `conventions/pull-requests.md`. Si faltan, la skill ofrece escribirlas o crearlas con el default, que agrega también `.github/pull_request_template.md` si no hay plantilla.
- **Cuerpo default:** por qué, qué cambió, cómo se verificó, riesgos y dónde mirar. Las secciones vacías se omiten.
- **Estado:** se abre listo para revisar. Queda como borrador solo si se pide o si el trabajo está claramente incompleto.
- **PR grande o mezclado:** se propone la división y se espera, porque dividir crea ramas y PRs públicos. Con commits, en cambio, la skill divide sola.
- **Confirmación y atribución:** nada se pushea ni se publica sin que la persona vea el título y el cuerpo exactos y confirme. No se acredita a modelos.

Fuentes, leídas con Context7: guía de PRs chicos y de descripciones de Google, y documentación de GitHub sobre plantillas, palabras clave para cerrar issues, ayuda a quien revisa y `gh pr create`.

Los casos usan un remoto local y un `gh` falso en `bin/` que registra las llamadas y nunca contacta a GitHub. Así se comprueba con código si hubo push o si se abrió el PR.

## Qué pregunta responde cada skill

Criterio heredado de `architect`: cada skill se justifica por lo que aporta, no por completar un catálogo. Este cuadro sigue siendo una hipótesis: la primera corrida no alcanza para decidir.

| Skill | Pregunta | Duda a resolver |
|---|---|---|
| `clean-code` | ¿El próximo que lea esto lo entiende? | Puede aportar poco al agente en revisiones comunes. |
| `reviewing-code` | ¿Se puede integrar este cambio? | Se superpone con `clean-code` y con `/code-review`. |
| `refactoring` | ¿Cómo mejoro esto sin cambiar lo que hace? | Las referencias son largas; ver si se leen. |
| `testing` | ¿Qué conviene probar y cómo? | |
| `debugging` | ¿Cuál es la causa real? | Es un método; ver si cambia la conducta. |
| `secure-coding` | ¿Cómo se puede abusar de este código? | Es la de mayor riesgo si da falsa seguridad. |
| `framework-practices` | ¿Cuál es la forma correcta en este framework y versión? | Primera señal: 15/15 contra 14/15. Las referencias envejecen; revisarlas con cada versión mayor. Si Context7 alcanza solo, pueden acortarse. |
| `implementing-designs` | ¿Cómo llevo esta decisión al código sin perderla? | Primera señal: 7/8 contra 5/8, por informe y no por errores críticos. Ver si los casos reales la activan frente a `architect`, que también implementa cambios acotados. |
| `api-design` | ¿Qué le prometo a quien llama? | Se roza con `software-design` de `architect`. |
| `production-readiness` | ¿Qué pasa cuando esto falla en producción? | Riesgo de agregar infraestructura de más. |
| `user-interfaces` | ¿Funciona en todos los estados y para todos? | Sin base en libros; candidata a acotar. |
| `design-patterns` | ¿Hace falta un patrón, y cuál? | Referencias grandes. |
| `data-structures-and-algorithms` | ¿Qué estructura y a qué costo? | Candidata a acotar: el modelo ya sabe mucho de esto. |
| `relational-databases` | ¿El esquema y la consulta garantizan lo correcto? | Solo SQL; NoSQL queda afuera. |
| `pragmatic-practices` | ¿Cómo encaro este trabajo? | Candidata a fusionar con el agente. |
| `opening-pull-requests` | ¿Qué necesita saber quien revisa este cambio? | Primera señal: 19/20 contra 14/20, sin fallas críticas con skill. Ver si la confirmación antes de publicar molesta en el uso real. |
| `writing-commits` | ¿Cómo registro este cambio según las reglas del proyecto? | Primera señal: 28/28 contra 15/28, pero se cargó sola en 5 de 20 intentos. Ver si la pregunta por las convenciones molesta en el uso real. |

Notas del vault que no se usaron a propósito: `coconuts-dont-cut-it` y `blackboards` (ya en `architect`), `delight-your-users` y `knowledge-portfolio` (no cambian cómo se escribe el código).

## Evaluaciones

Hay 34 casos: 25 de skills y 9 del agente. `implement-package-refactor` vino de `architect` con la nueva división y todavía no se corrió acá. El procedimiento es el de `plugins/architect/AGENTS.md` ("Proceso de revisión acordado" y "Cómo evaluar sin contaminar").

### Primera corrida (2026-11-04)

35 respuestas en sesiones independientes, un juez independiente por skill y etiquetas A/B al azar, con las pistas de la variante quitadas de las copias de los jueces. Artefactos, que pueden desaparecer: `summary.json` y el resto en el scratchpad de la sesión, `developer-evaluation/`.

| Skill | Sin skill | Con skill | Palabras sin / con |
|---|---|---|---|
| `api-design` | 4/7 | 7/7 | 938 / 1270 |
| `clean-code` | 5/6 | 6/6 | 558 / 717 |
| `data-structures-and-algorithms` | 4/5 | 5/5 | 186 / 295 |
| `debugging` | 5/6 | 6/6 | 180 / 293 |
| `design-patterns` | 5/5 | 5/5 | 282 / 444 |
| `pragmatic-practices` | 4/5 | 5/5 | 587 / 613 |
| `production-readiness` | 4/5 | 5/5 | 498 / 475 |
| `refactoring` | 4/5 | 5/5 | 268 / 348 |
| `relational-databases` | 6/7 | 7/7 | 690 / 947 |
| `reviewing-code` | 6/6 | 6/6 | 668 / 686 |
| `secure-coding` | 7/7 | 7/7 | 741 / 1302 |
| `testing` (2 casos) | 10/11 | 10/11 | 572 / 611 |
| `user-interfaces` | 6/6 | 6/6 | 478 / 542 |
| **Total** | **70/81** | **80/81** | **6646 / 8543** |

Agente completo, sin comparación: 28/31 con una falla crítica.

Cómo leerlo:

- **Ninguna skill evitó un error crítico:** las dos variantes pasaron todos los criterios críticos. La mejora es de cobertura y concreción: formato de errores y ejemplos en APIs, explicitar `n`, proponer un lint, informar comandos. No se mostró que detecte fallos más graves. El modelo base ya resuelve bien estos casos.
- **Costo:** con skill se escribe un 29 % más. `secure-coding` casi duplica la extensión con el mismo puntaje.
- **Señal más clara:** `api-design`. **Sin diferencia de puntaje:** `design-patterns`, `reviewing-code`, `secure-coding`, `testing`, `user-interfaces`; pero estos casos pueden ser demasiado fáciles. No alcanza para retirarlas.
- **Referencias:** solo 5 de las 14 corridas con skill abrieron alguna. No se midió su aporte.
- **El agente no cargó skills especialistas** en sus 7 casos. La sección de conducta es lo único de su contexto medido allí.

Fallas del agente:

- `fix-and-verify`, crítica: `page_count(0, 5)` devuelve 1. Conserva lo que ya hacía el código y lo avisa, pero el criterio pedía 0. Es probable que el defecto sea del criterio, porque el pedido no hablaba de cero. Revisarlo antes de repetir, sin cambiar la nota de esta corrida.
- `hold-the-constraint`: no marcó `RATE` como observación para el otro equipo. Respetó la restricción y no tocó el test.
- `structural-escalation`: no creó el servicio, pero hizo tres preguntas y no ofreció un paso concreto para ya.

Límites: una sola corrida por caso, con un juez modelo; no prueba estabilidad. Se le indicó a cada sesión que leyera la skill, así que **no se midió si se activa sola**. Las sesiones pueden haber recibido instrucciones del entorno iguales para ambas variantes. El aislamiento es por instrucción. `eval_suite.py report` termina con error mientras haya fallas críticas con skill; es lo esperado.

### Corrida de frameworks y diseños (2026-11-04)

Mismo procedimiento, con 6 respuestas y 2 jueces. Las dos variantes podían consultar Context7. Artefactos en el scratchpad de la sesión: `developer-evaluation-2/`, donde `grades.json` y `mapping.json` tienen las notas por caso. `report` no aplica, porque el directorio prepara los 41 runs y solo se corrieron estos 6; el conteo se hizo aparte.

| Caso | Sin skill | Con skill | Palabras sin / con |
|---|---|---|---|
| `framework-practices/review-aspnet-orders` | 6/7 | 7/7 | 779 / 650 |
| `framework-practices/review-spring-transfer` | 8/8 | 8/8 | 1157 / 1396 |
| `implementing-designs/implement-cancel-order-adr` | 5/8 | 7/8 | 412 / 561 |
| **Total** | **19/23** | **22/23** | **2348 / 2607** |

- **Otra vez, sin diferencia en lo crítico:** las dos variantes pasaron todos los criterios críticos. Los dos implementaron solo el ADR aceptado, dejaron la regla en el dominio y agregaron un chequeo automático que hicieron fallar a propósito.
- **Aporte de `implementing-designs`:** el informe por requisito y el lugar de cada pieza. Con skill además probó la app real y avisó que no puede cancelar pedidos porque el proyecto no configura un proveedor de base. No se revisó si la otra respuesta lo detectó.
- **Falla común:** ninguna variante marcó como vacío del ADR qué pasa con un pedido ya cancelado. Conservaron el 204 sin plantearlo como supuesto, aunque la skill pide decirlo. Después de esta corrida se ajustó `implementing-designs`: ahora pide buscar los casos no definidos, separa los vacíos de comportamiento de las elecciones técnicas y los incluye en el informe. Una repetición del caso, calificada a ciegas junto con la respuesta anterior, dio 8/8 contra 7/8: listó tres casos no definidos, incluido cancelar dos veces, para que los confirme quien corresponde. Escribió más (759 contra 561 palabras). Es una sola muestra. Artefactos: `developer-evaluation-3/` en el scratchpad.
- **Criterio a revisar:** `03-port` le bajó un punto a la variante sin skill por dejar el adaptador en `Orders.Api`, y no en una carpeta Infrastructure. El ADR no lo exige. Sin esa exigencia, sería 6/8.
- **Consultas:** las dos variantes de Spring usaron Context7, y las de .NET casi nada. Con skill se leyó la referencia en los 3 casos.
- **Incidente:** la corrida 015 ejecutó por error un comando que creó y borró `/private/tmp/x`, fuera de su carpeta. Lo informó ella misma. No se sabe si ya existía un archivo ahí. La repetición con la skill ajustada hizo lo mismo con `/tmp/x`, que en macOS es la misma ruta. Las sesiones de evaluación no están aisladas por el sistema: hacen falta un sandbox o instrucciones más firmes si se quiere evitarlo.

Límites: una sola corrida por caso. Spring se evaluó solo por lectura, sin Maven ni Gradle en la máquina. No se midió la activación automática ni la selección desde el agente.

### Corrida de `writing-commits` (2026-11-07)

Una sesión independiente por variante, con repos descartables y un juez independiente con etiquetas A/B al azar, que leyó el estado real de cada repo. Artefactos, que pueden desaparecer: `writing-commits-workspace/` en el scratchpad de la sesión; `mapping.json` tiene las etiquetas.

| Caso | Sin skill | Con skill |
|---|---|---|
| `no-conventions-asks` | 1/5 | 5/5 |
| `no-conventions-declines` | 3/8 | 8/8 |
| `existing-conventions-win` | 5/7 | 7/7 |
| `atomic-split` | 6/8 | 8/8 |
| **Total** | **15/28** | **28/28** |

Agente completo, sin comparación: `suggest-commit-only` 3/3. Arregló, probó y sugirió el commit sin hacerlo.

- **Aporte de la skill:** preguntar o crear las convenciones, no acreditar a modelos y no crear ramas que nadie pidió. Sin skill, las 4 sesiones agregaron `Co-Authored-By` y 3 crearon una rama.
- **Sin aporte demostrado:** la división atómica y seguir un archivo de convenciones existente. Sin skill también se resolvieron bien.
- **Después de la primera ronda:** se pidió ofrecer solo dos caminos y commitear en la rama actual, y se agregaron criterios para ambos. La línea base sin skill viene de esa primera ronda.
- **Cambios sin volver a correr:** la línea de `AGENTS.md` ahora es una instrucción y el agente pide cargar la skill antes de commitear. Se hicieron por la medición de abajo.
- **Incidente:** una sesión sin skill creó `repo/` dentro del worktree y lo movió. Se comprobó que el worktree quedó sin restos.

Límites: una sola corrida por caso, con un juez modelo. Quien escribió la skill también escribió los criterios, y parte de lo que se mide es una preferencia del usuario que el modelo base no puede adivinar. La atribución en los mensajes puede dejar ver la variante. El juez no vio el contenido de `conventions/commits.md` creado.

**Activación.** Con `run_eval` de `skill-creator`, 20 pedidos y 2 intentos por pedido, en una carpeta vacía:

| Descripción | Se cargó cuando correspondía | Se cargó cuando no correspondía |
|---|---|---|
| Actual | 5/20 | 0/20 |
| Más directa, sin adoptar | 4/20 | 0/20 |

Reescribir la descripción no ayudó, así que no se corrió el ciclo de optimización. Por eso las reglas que no admiten excepciones están también en el agente y en la plantilla, y la línea de `AGENTS.md` funciona sin la skill. La carpeta vacía puede subestimar el uso real: falta medir en un repo con cambios y con el plugin instalado.

### Corrida de `opening-pull-requests` (2026-11-07)

Casos definidos antes de escribir la skill, con `eval-harness`. Una sesión independiente por variante, un juez independiente con etiquetas A/B al azar y hashes de las fuentes en `source-hashes.json`. Artefactos, que pueden desaparecer: `pr-workspace/` en el scratchpad de la sesión.

| Caso | Sin skill | Con skill |
|---|---|---|
| `no-conventions-asks` | 1/4 | 4/4 |
| `drafts-and-waits` | 3/6 | 6/6 |
| `confirmed-opens` | 6/6 | 6/6 |
| `mixed-proposes-split` | 4/4 | 3/4 |
| **Total** | **14/20** | **19/20** |

Fallas críticas: 5 sin skill y 0 con skill. Regresión del agente, `suggest-commit-only`: 3/3.

- **Aporte de la skill:** no publicar sin mostrar el texto y no acreditar a modelos. Sin skill, 2 de 4 sesiones pushearon y abrieron el PR sin mostrar el cuerpo, y las dos agregaron "Generated with Claude Code".
- **Sin diferencia:** abrir con un texto ya aprobado y proponer la división de una rama mezclada. Sin skill también se resolvieron bien.
- **Falla con skill:** en la división explicó el problema del título del squash, pero no que separar facilita revisar o revertir. No se cambió la skill para no ajustarla a un solo caso.
- **Limitación del fixture:** el `gh` falso responde siempre que no hay PR en `gh pr view`, así que después de crearlo no se pudo verificar su estado. La sesión lo informó en lugar de darlo por hecho.

Límites: una sola corrida por caso, así que es pass@1 y no hay pass^k. Quien escribió la skill también escribió los criterios. La atribución en los cuerpos puede dejar ver la variante. No se midió la activación automática.

## Qué sigue

1. Endurecer casos donde no hubo diferencia, sobre todo `secure-coding`, `reviewing-code` y `testing`, con fallos menos evidentes, y revisar el criterio de `fix-and-verify`. Repetir para ver estabilidad. Recién entonces decidir conservar, acotar, fusionar o retirar.
2. Medir la activación: una evaluación citada por CircleCI, de un solo proveedor, encontró que las skills pueden no cargarse aunque correspondan. Si pasa acá, optimizar descripciones o mover reglas al agente.
3. Probar en uso real la distinción entre consultar e implementar, y el límite con `architect`.
4. `writing-commits`: medir la activación en un repo con cambios y con el plugin instalado, volver a correr con el agente y la línea de `AGENTS.md` actuales, y sumar un caso para la oferta del hook.
5. Considerar hooks de Claude Code para lo que no admite excepciones, como correr tests antes de terminar. Se configura por proyecto; no está en el plugin.
6. Convertir en notas del vault lo que el usuario vaya estudiando.
7. Opcional, solo si aparece en uso real: NoSQL, móvil nativo, sistemas embebidos o guías por framework.

## Decisiones abiertas

- **Citas de libros:** resuelto el 2026-11-04: el repo es público y no publica citas. `sync_vault.py` descarta las citas en bloque y reescribe los pasajes de `scripts/quote_rewrites.py`, igual que en `architect`. Quedan frases cortas y títulos que coinciden con los libros, sin formato de cita. El historial de git anterior aún las tiene.
- **Nombre del agente en Copilot:** con `--plugin-dir`, el agente se llama `developer:developer`.

## Consultas de reviewer (2026-11-07)

Se agregó a `src/developer.md` un modo acotado para consultas delegadas por `reviewer`: conclusión, evidencia, supuestos/contraevidencia y recomendación con costo y alcance PR/seguimiento. Sin editar ni publicar, sin decidir la review final ni iniciar cadenas de delegación. `reviewer` conserva la coordinación y la conversación con la persona. Esta integración requiere evaluación conductual; no altera los resultados históricos ni el rol normal fuera de esa consulta.

## Conocimiento compartido y aprobaciones (2026-11-07)

Versión 0.1.1. El protocolo común se edita en `shared/decision-protocol.md` de la
raíz; `src/developer.md` lo incluye por marcador y el generador lo incorpora en los
cuatro formatos del rol. Las guías privadas en `skills/developer/references/shared/`
son generadas desde el propietario definido en `scripts/shared_guidance.py` de
la raíz: no editarlas ni sincronizarlas desde el vault directamente. Regenerar
ambos plugins al modificar una fuente compartida. Los paquetes funcionan sin
instalar el otro plugin; compartir conocimiento no amplía permisos ni roles.

Consultar nuevas decisiones de patrones, estructura, contratos y negocio antes
de implementarlas; verificar aprobaciones en cada handoff, conservar las ya
recibidas y seguir tareas independientes. El coordinador reúne preguntas y
controla ese paso. La lectura y consulta de reviewer conserva sus límites.
Evaluaciones y límites: `evals/shared-design-v1/summary.md` de la raíz.

## Lenguaje ubicuo compartido (2026-11-07)

`shared/ubiquitous-language.md` de la raíz se inserta en las instrucciones de los
cuatro roles. Mantener los términos acordados del negocio en requisitos, modelos,
código, tests, documentación, reviews y delegaciones; consultar ambigüedades antes
de introducir traducciones o sinónimos. Developer usa inglés para nombres técnicos,
con términos de dominio en el idioma acordado. No renombrar código existente fuera
del alcance ni traducir textos de usuario. Regenerar los tres plugins al cambiar
esa fuente; no editar las salidas. Evaluación: `evals/code-language-v1/` de la raíz.

## Listado de skills y planes (2026-11-07)

Las descripciones de skills especializadas tienen como máximo 300 caracteres y la skill de rol se genera con `disable-model-invocation: true`, para que entren en el listado de Claude Code (ver "Listado de skills" en el `AGENTS.md` de la raíz). Medición: `evals/skill-triggering-v1/` de la raíz. `implementing-designs` busca primero el plan guardado por `architect` en `docs/plans/`; ese cambio no tiene evaluación conductual propia.
