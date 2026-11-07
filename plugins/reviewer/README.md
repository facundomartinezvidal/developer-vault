# reviewer

Asistente para una persona que revisa la PR de un compañero. Primero entiende la descripción, los requisitos y el código modificado con sus callers y tests. Investiga riesgos y alternativas, consulta a `developer` o `architect` según el tema y presenta sus conclusiones con evidencia. Después conversa con la persona para elegir y redactar los comentarios. No termina una review por su cuenta ni publica, aprueba o cambia código sin un pedido explícito.

## Uso

Con el plugin cargado, pedí:

> Ayudame a revisar https://github.com/equipo/proyecto/pull/123. Primero explicame qué cambió y por qué; después armemos juntos los comentarios.

También acepta un número de PR con su repositorio, una comparación local de ramas o descripción y diff pegados. Para PRs privadas hace falta acceso desde el cliente, por ejemplo mediante un conector o CLI autenticada. El plugin no incluye credenciales ni instala servidores MCP.

La primera respuesta sustancial es una explicación para vos: intención, implementación, posibles hallazgos, alternativas y límites de lo comprobado. El agente pausa para discutirlos. Podés decirle «incluyamos el primero», «ese comportamiento está permitido por este requisito» o «investigá el segundo antes de comentarlo». Con esa conversación prepara el borrador para el autor y una recomendación de disposición; vos decidís la review.

También ayuda a estructurar la devolución: resumen breve, cambios requeridos, sugerencias opcionales y próximo paso, omitiendo lo que no aplique. Los detalles van como comentarios en la ubicación adecuada, explicando el escenario, su consecuencia y qué se propone hacer. Sigue las convenciones de tu equipo y adapta la extensión a la PR; la estructura se basa en la investigación de Google, GitHub y Conventional Comments, no en llenar una plantilla obligatoria.

Todo el contenido destinado a publicarse se arma consultándote: estructura, resumen, redacción de cada comentario, preguntas, sugerencias, snippets, tono, carácter bloqueante y decisión de la review. Elegir un hallazgo no significa aceptar su redacción. Podés acordar propuestas por grupos; al terminar ves el contenido completo con sus ubicaciones y decidís qué queda. Nada se considera listo para publicar sin tu conformidad con esa versión. «Publicá esta versión» puede aceptar el texto mostrado y autorizar su envío en un mismo paso.

`developer` ayuda con implementación, frameworks, tests y seguridad del código; `architect`, con límites, dominio, decisiones y diseño. Instalalos desde este marketplace para habilitar esas consultas. La delegación depende del cliente y de que los agentes estén disponibles. Sin ella, el agente avisa, usa las skills disponibles o prepara una consulta concreta; no simula especialistas. No necesita ambos para revisar una PR simple.

Para detalles de librerías usa Context7 si está conectado, o documentación oficial de la versión instalada. Distingue una preferencia de un defecto y no exige otro diseño sin explicar el beneficio concreto y su costo.

## Instalación

El plugin incluye ambos roles para los tres clientes, generados desde sus fuentes:

| Cliente | `reviewer` | `code-investigator` |
|---|---|---|
| Claude Code | `agents/reviewer.md` | `agents/code-investigator.md` |
| GitHub Copilot CLI | `com.github.copilot/agents/reviewer.agent.md` | `com.github.copilot/agents/code-investigator.agent.md` |
| Codex | `skills/reviewer/SKILL.md` y `com.openai.codex/agents/reviewer.toml` | `skills/code-investigator/SKILL.md` y `com.openai.codex/agents/code-investigator.toml` |

En Claude Code:

```bash
claude plugin marketplace add facundomartinezvidal/developer-vault
claude plugin install reviewer@developer-vault
```

En GitHub Copilot CLI:

```bash
copilot plugin marketplace add facundomartinezvidal/developer-vault
copilot plugin install reviewer@developer-vault
```

En Codex, siguiendo el formato de los otros plugins del repo:

```bash
codex plugin marketplace add facundomartinezvidal/developer-vault
codex plugin add reviewer@developer-vault
```

Usá la skill `reviewer:reviewer` para cargar el rol en Codex. El TOML opcional de `com.openai.codex/agents/reviewer.toml` permite configurar un agente personalizado en clientes compatibles; la instalación del plugin por sí sola no garantiza su registro como subagente. Esta integración nueva todavía no se probó en sesiones reales de los tres clientes.

Para configurar subagentes personalizados en Codex, los archivos opcionales son `com.openai.codex/agents/reviewer.toml` y `com.openai.codex/agents/code-investigator.toml`. Copialos a la carpeta de agentes de tu configuración de Codex si tu cliente admite ese formato. Para las consultas a los otros plugins, sus agentes también deben estar configurados y disponibles; cargar una skill de rol no equivale a registrar un subagente.

Desde un clon podés probar Claude Code o Copilot con `--plugin-dir plugins/reviewer --agent reviewer:reviewer`. Para consultas reales también deben estar cargados los plugins especialistas correspondientes.

## Mantenimiento

Editá `src/reviewer.md` o `src/code-investigator.md` y regenerá con `python3 scripts/build_agents.py` desde esta carpeta. `--check` detecta salidas desactualizadas. Validá con `claude plugin validate .` acá y en la raíz. Los archivos generados no se editan a mano.

La investigación y sus límites están en [docs/research.md](docs/research.md). Los escenarios de comportamiento están en `evals/`; no forman parte de las instrucciones del agente. La primera [evaluación textual](evals/behavior-v1/summary.md) registró 8/9 ejecuciones completas y una omisión del investigador, sin demostrar todavía confiabilidad general. El estado de mantenimiento está en [AGENTS.md](AGENTS.md).

## Investigación delegada y especialistas

En PRs que requieren recorrer varios módulos, `reviewer` puede usar el subagente `code-investigator` para seguir diff, callers, invariantes y tests. Recibe una pregunta abierta y devuelve evidencia y dudas; no ejecuta código, modifica archivos ni redacta la review. Para cambios pequeños, `reviewer` investiga directamente. La delegación depende del cliente; el agente también se genera como skill de rol y TOML opcional, igual que `reviewer`.

`reviewer` consulta directamente a `developer` y `architect`: pregunta y contexto; conclusión y evidencia; supuestos y contraejemplos; recomendación, costo y si corresponde a esta PR o a un trabajo posterior. Reúne y verifica las respuestas, distinguiendo defectos demostrados de propuestas de diseño. No hay un subagente recolector. Los especialistas mantienen el modo consulta y devuelven sus dudas al coordinador.

## Project vocabulary

All roles share the project's approved ubiquitous language in requirements,
models, code, tests, documentation, reviews and handoffs. They preserve business
terms in the agreed language and consult conflicting terms before renaming.
Developer uses English technical identifiers while preserving domain vocabulary.
The maintained source is `shared/ubiquitous-language.md` at the repository root;
regenerate all three plugins after changes. Existing code is not mass-renamed.
