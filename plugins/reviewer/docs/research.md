# Investigación para un asistente de review colaborativa

Consulta realizada el 2026-11-07. Síntesis propia; las decisiones del agente son una adaptación a este producto, no resultados medidos de su eficacia.

| Fuente primaria | Qué aporta al diseño |
|---|---|
| [Google: estándar de revisión](https://google.github.io/eng-practices/review/reviewer/standard.html) | Equilibrar calidad y avance. Una mejora útil no necesita perfección; una preferencia menor no justifica bloquear. |
| [Google: qué revisar](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Comprender funcionalidad, integración, complejidad y tests, mirando el contexto del cambio. |
| [Google: comentarios](https://google.github.io/eng-practices/review/reviewer/comments.html) | Explicar el motivo, hablar del código y distinguir exigencias de sugerencias. Dejar espacio para que el autor elija la solución. |
| [Bacchelli y Bird, Microsoft Research, ICSE 2013](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/) | El estudio identifica la comprensión del cambio como parte central y observa beneficios de transferencia de conocimiento y alternativas, además de detectar defectos. Es evidencia de equipos estudiados, no una garantía universal. |
| [Conventional Comments](https://conventionalcomments.org/) | Etiquetas opcionales para aclarar intención y carácter bloqueante. No se exige adoptarlas si el equipo usa otra convención. |
| [Context7 MCP, documentación oficial](https://github.com/upstash/context7/blob/master/packages/mcp/README.md) | Resolver la biblioteca antes de consultar documentación y acotar la búsqueda al problema técnico. La fuente debe corresponder a la versión del proyecto. |

## Uso del plugin Vercel y Context7

Se leyó la skill `build-agents` del plugin Vercel instalado y se consultó su herramienta `search_vercel_documentation`, que usa un índice de Context7, sobre revisión de código, instrucciones y falsos positivos. Los resultados fueron mayormente de configuración de agentes y plataforma, insuficientes para fundamentar el método de review; se complementaron con las fuentes de la tabla. La skill `vercel-agent` se inspeccionó para distinguir el servicio de revisión de Vercel de un agente portable del marketplace.

No estaba disponible un MCP general de Context7 en esta sesión. No se afirma haber consultado por esa vía las guías de Google o las librerías de una PR. El plugin nuevo usa Context7 cuando el cliente lo provee; la alternativa es documentación oficial o código instalado.

`build-agents` recomienda eve para proyectos nuevos, con excepción de stacks existentes. Aquí se amplía el marketplace existente: fuente Markdown y generación de formatos para clientes. No se necesita despliegue, AI Gateway ni credenciales Vercel. No se afirma que el servicio Vercel Agent ejecute este plugin o consulte automáticamente a los agentes de este repo.

## Decisiones del producto

La separación entre análisis privado, discusión con la persona y borrador para el autor responde al pedido del usuario. También son decisiones del producto la consulta acotada a especialistas, la pausa antes de cerrar el borrador y la verificación de la versión de la PR antes de una publicación solicitada. Las fuentes respaldan claridad, comprensión y comentarios útiles; no demuestran que este flujo específico mejore una métrica.

Para evaluar utilidad conviene observar hallazgos confirmados y descartados, comprensión del revisor, comentarios elegidos y accionables, tiempo de revisión y falsos positivos. Más comentarios o más texto no equivalen a una mejor revisión.

## Cómo estructurar la review que recibe el autor

Se investigó también la composición de la devolución, además del análisis técnico. [GitHub, quickstart de reviews](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart) distingue comentarios sobre líneas, sugerencias concretas, resumen y disposición (comment, approve o request changes). Eso respalda separar el panorama general de los detalles localizados, sin trasladar todo el informe privado al autor. Las [guías de GitLab](https://docs.gitlab.com/development/code_review/) aportan el contexto de conversación entre autor, revisor y especialistas; sus reglas internas no se convierten en requisitos universales para este plugin.

La orientación de Google sobre explicar motivos y graduar comentarios, junto con las etiquetas de Conventional Comments, se tradujo en dos propuestas prácticas:

- Resumen corto del alcance y valoración, cambios requeridos con referencias a comentarios, sugerencias opcionales separadas y próximo paso. Se omiten partes vacías; una PR simple puede merecer una sola frase.
- Cada comentario comunica observación o escenario, consecuencia y próximo paso con su razón. Ubicación concreta, carácter bloqueante y evidencia se agregan donde ayudan a actuar. No hacen falta títulos rígidos en cada comentario.

Estas estructuras son una síntesis para este agente, no una plantilla oficial compartida por todas las fuentes ni una forma demostrada como superior a cualquier otra. Primero se respeta la práctica del equipo. No se exige un comentario positivo para amortiguar cada crítica, ni se diluyen defectos confirmados en preguntas retóricas. El borrador debe permitir distinguir qué impide integrar, qué es opcional y qué se necesita aclarar.
