# Reviewer: evaluación de producto v1

Criterios fijados antes de las respuestas; fuentes del agente congeladas por hash. Se evalúa el comportamiento actual, sin afirmar mejora contra una versión anterior.

Seis casos: review colaborativa de tres turnos (tres sesiones independientes), cambio correcto con guard y ADR, cobertura parcial con head nuevo, investigador, developer y architect. Ocho sesiones; catorce respuestas esperadas. Modelos heredados de la sesión sin override; registrar límites de identificación y consumo.

Éxito estricto de caso: todos sus criterios pasan. Fallo crítico: falla cualquier criterio marcado critical, independientemente del total. Juez independiente con evidencia por criterio; adjudicación humana pendiente para seguridad y calidad de comunicación.

Métricas: fracción empírica de éxito por sesión; para review colaborativa registrar cuántas de tres pasan y si todas pasan (pass^3 observado). No estimar pass@3 de la suite con casos de un solo intento. Sin selección de mejor respuesta, sin retries guiados por el juez. Sin baseline previo validado: estos casos fijan una referencia inicial, no demuestran ausencia de regresiones históricas.

Modalidad: agentes responden a snapshots textuales de PRs ficticias, sin ejecutar código ni consultar servicios. No prueba herramientas reales, instalación en clientes, publicación ni contención del SO. La integración se limita al contrato de las respuestas de los roles, no a delegación real dentro de reviewer. Aislamiento por contexto e instrucciones, no barrera de acceso de archivos. No usar el gate ejecutable bloqueado del harness.

Artefactos de respuesta y grading fuera del repo; resumen durable aquí. Referencia de rúbrica: cases.json. No entregar definición ni criterios a quienes responden.

Se agregó después una prueba de coordinación delegada, definida en `integration.json` y congelada antes de ejecutarla. No altera los criterios de la primera tanda: agrega una ejecución principal con tres consultas a subagentes reales. El resumen separa las 9 ejecuciones puntuadas de las 3 sesiones delegadas adicionales.
