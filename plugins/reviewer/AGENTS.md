# AGENTS.md — plugin `reviewer`

Estado al **2026-11-07**.

## Alcance y división

Ayuda a una persona a revisar una PR de un compañero: analiza antes de conversar, consulta especialistas según la duda y construye el borrador con la persona. `reviewer` coordina la revisión; `developer` consulta sobre implementación y realiza cambios cuando se le pide; `architect` planea y consulta sobre estructura sin editar código. No convertir este plugin en un bot que publica o aprueba automáticamente.

Todo el contenido para publicación se consulta con la persona durante su composición, incluida su redacción, resumen, ubicaciones, etiquetas y disposición. Aceptar un hallazgo no acepta texto no visto. Mostrar el paquete final completo para acordar esa versión; permitir aceptación por grupos y no repetir consultas sobre contenido ya aceptado sin cambios. La conformidad con el texto no implica publicación salvo pedido explícito de enviarlo.

## Fuentes y mantenimiento

- `src/reviewer.md` y `src/code-investigator.md` son las fuentes de los dos roles. `agents/`, `com.github.copilot/`, `com.openai.codex/` y `skills/<rol>/` son generados; no editarlos a mano.
- Ejecutar `python3 scripts/build_agents.py`, y `python3 scripts/build_agents.py --check` para detectar divergencias. El generador se adaptó del de `developer`; revisar los otros generadores si se corrige un defecto compartido.
- Mantener versión y descripción consistentes entre `plugin.json` y `.claude-plugin/plugin.json`. Registrado en ambos marketplaces de la raíz.
- Validar con `claude plugin validate .` desde el plugin y la raíz. Validar también ambos manifiestos como JSON y el agente Codex como TOML.
- Investigación escrita con palabras propias en `docs/research.md`; no copiar manuales, libros ni material del vault. Este plugin no sincroniza referencias del vault.
- No modificar los plugins especialistas para duplicar o absorber sus funciones. La skill `developer/reviewing-code` sigue cubriendo revisión técnica; este rol agrega la colaboración con el revisor humano.

## Evaluación y límites

Los casos de `evals/` son material del evaluador: nunca darlos al agente que responde ni enlazarlos desde su fuente o skill. Para probar comportamiento, entregar solamente instrucciones, pedido y artefactos del caso en una sesión aislada; calificar después con los criterios separados. No afirmar eficacia por pasar validadores estáticos. No ejecutar modelos pagos desde scripts.

Primera evaluación conductual textual independiente realizada: ver `evals/behavior-v1/summary.md`. Pendiente: ampliar cobertura y estabilidad, prueba real de instalación e invocación en los tres clientes y una PR real revisada en conjunto. Las reglas de lectura y publicación son instrucciones, no un bloqueo técnico del host. No se incluye un runtime alojado en Vercel: se mantiene el stack de plugins existente siguiendo la excepción de su skill `build-agents`.

Validación estática inicial: `build_agents.py --check`, `quick_validate.py`, JSON, TOML y `claude plugin validate .` en plugin y raíz. La validación de Claude distingue el manifiesto válido de los requisitos para presentar al directorio: falta licencia y recomienda icono. No se asignó una licencia al proyecto; no confundir esta validación con aprobación para ese directorio ni con pruebas de comportamiento.

## Investigación y consultas (2026-11-07)

`code-investigator` es un subagente opcional para inspección de fuentes en PRs que requieren seguir flujos entre archivos. No ejecuta código, edita ni consulta especialistas. `reviewer` recibe y verifica la evidencia, consulta directamente a `developer` y `architect` con un formato común y sintetiza sus respuestas; no hay un recolector intermediario. La disponibilidad de delegación depende del cliente; las skills de rol y TOML se generan para ambos agentes. El flujo delegado se probó con subagentes reales y fuentes copiadas en `behavior-v1`; sigue pendiente verificar descubrimiento e invocación de plugins instalados en los clientes.

## Evaluación inicial con eval-harness (2026-11-07)

Nueve ejecuciones puntuadas en siete escenarios: 8/9 completas, 48/49 criterios. Colaboración de tres turnos: 3/3 repeticiones. Coordinación con investigador y ambos especialistas: 1/1. Un fallo según rúbrica original: el investigador enumera incertidumbres sin proponer explícitamente cómo verificarlas; el criterio compuesto `scope` mezcla esa cobertura con límites de actuación y debe separarse antes de usarlo como gate. Se preserva la calificación original, sin cambios de prompts ni retries correctivos. Fracción de primer intento por escenario: 6/7; no hay pass@3 de suite ni comparación con una variante sin instrucciones.

Fuentes y fixtures congelados por hash, candidatos sin rúbricas, juez independiente y revisión de evidencia. Resumen durable en `evals/behavior-v1/summary.md`, resultados y metadata al lado; crudos en `/tmp/reviewer-product-eval-v1/` (temporales). La prueba usa snapshots sintéticos, sin ejecutar código de PRs ni conectores; no demuestra contención del SO ni instalación en clientes. Queda juicio humano sobre seguridad/utilidad y ampliar casos antes de afirmar confiabilidad. Los scripts de esta evaluación no invocan modelos.

## Lenguaje ubicuo compartido (2026-11-07)

`shared/ubiquitous-language.md` de la raíz se inserta en las instrucciones de los
cuatro roles. Mantener los términos acordados del negocio en requisitos, modelos,
código, tests, documentación, reviews y delegaciones; consultar ambigüedades antes
de introducir traducciones o sinónimos. Developer usa inglés para nombres técnicos,
con términos de dominio en el idioma acordado. No renombrar código existente fuera
del alcance ni traducir textos de usuario. Regenerar los tres plugins al cambiar
esa fuente; no editar las salidas. Evaluación: `evals/code-language-v1/` de la raíz.
