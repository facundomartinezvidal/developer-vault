# AGENTS.md

Marketplace de plugins para desarrolladores (`.claude-plugin/marketplace.json` y, para Codex, `.agents/plugins/marketplace.json`). Tiene tres plugins: `plugins/architect`, `plugins/developer` y `plugins/reviewer`.

## Dónde trabajar

- `plugins/architect/` — agente `architect` y 6 skills (decisiones/ADRs, documentación C4, threat modeling, Clean Architecture, DDD, software design). Instalable en Claude Code, GitHub Copilot CLI y Codex.
- `plugins/developer/` — agente `developer` (consultor y realizador de código, para cualquier lenguaje) y 15 skills (frameworks con ASP.NET Core y Spring Boot, implementación de diseños de `architect`, clean code, revisión, refactoring, testing, debugging, seguridad, APIs, producción, interfaces, patrones, estructuras y algoritmos, bases relacionales, prácticas). Instalable en Claude Code, GitHub Copilot CLI y Codex.
- `plugins/reviewer/` — agente `reviewer`: analiza PRs, consulta a `developer` o `architect` y construye la review junto con la persona. No implementa ni publica sin pedido explícito.
- **Antes de tocar un plugin, leé su `AGENTS.md`**: estado, reglas de mantenimiento, evaluaciones y próximos pasos. El uso está en su `README.md`.

## División entre agentes

`architect` planea, diseña y consulta, y no edita código. `developer` implementa lo planeado y consulta sobre código. Mantener esta división al cambiar cualquiera de los dos.

## Reglas clave

- **No editar a mano lo generado:** en cada plugin, `agents/`, `com.github.copilot/`, `com.openai.codex/`, `skills/<agente>/` y los `references/` sincronizados del vault. Se cambian en `src/<agente>.md` o en el vault.
- Regenerar con `python3 scripts/build_agents.py` (desde la carpeta del plugin); con `--check` falla si algo quedó desactualizado.
- Validar: `claude plugin validate .` desde cada plugin y desde la raíz.
- Las evaluaciones (`evals/`) no las lee el agente; no exponer criterios a quien responde.
- El vault de Obsidian vive fuera de este repo. No copiar PDFs de libros ni citas textuales: el repo es público, y `sync_vault.py` las filtra.
- Commits: sin cambios no relacionados; los scripts no invocan modelos ni cuestan dinero.

## Al agregar un plugin

Registrarlo en `.claude-plugin/marketplace.json` y `.agents/plugins/marketplace.json`, darle su propio `AGENTS.md` y `README.md`, y enlazarlo desde este archivo.

## Compatibilidad obligatoria con los tres clientes

Todo agente, subagente, skill o plugin nuevo o modificado debe estar disponible para **Codex, Claude Code y GitHub Copilot CLI**. No dar por terminado un cambio que solo se entrega para uno de los tres.

- Mantener una fuente única en `src/<agente>.md` y generar sus formatos: `agents/<agente>.md` para Claude Code, `com.github.copilot/agents/<agente>.agent.md` para Copilot y `skills/<agente>/SKILL.md` más el TOML opcional en `com.openai.codex/agents/` para Codex, según las capacidades del cliente. Las skills compartidas conservan el formato `SKILL.md`.
- Registrar cada plugin en ambos marketplaces y documentar instalación, invocación y disponibilidad de sus subagentes en los tres clientes.
- Regenerar y comprobar con `--check`, validar manifiestos y verificar que las instrucciones equivalentes estén presentes en todos los formatos.
- Si un cliente no soporta una capacidad o necesita configuración adicional, documentar la alternativa y la limitación. No presentar generación de archivos como prueba de instalación, descubrimiento o delegación real.

## Al crear o modificar agentes

Usar la skill `eval-harness` para evaluar cada agente nuevo y los cambios de comportamiento de agentes existentes. Si no está disponible, indicar esa limitación y aplicar el procedimiento documentado acá; no afirmar que se usó la skill sin haberla leído.

- **Definir antes de implementar o ajustar:** tareas representativas, criterios observables de éxito y fallos críticos. Incluir casos normales, negativos y ambiguos, límites de autorización y, cuando corresponda, conversaciones de varios turnos, delegación y herramientas faltantes. Adaptar la cantidad de casos al alcance y al riesgo.
- **Separar capacidad y regresión:** probar lo nuevo y preservar lo que ya funciona. Guardar una versión o hashes de las instrucciones, fixtures y rúbricas para poder comparar sin cambiar las condiciones silenciosamente.
- **Evaluar comportamiento, además de estructura:** validadores, manifiestos y archivos generados son comprobaciones estáticas; no prueban la calidad ni la confiabilidad del agente.
- **Evitar contaminación:** guardar casos y criterios en `evals/`. Quien responde recibe solo instrucciones, pedido y artefactos necesarios, sin rúbricas, respuestas esperadas ni conclusiones previas. Usar sesiones independientes y, para juzgar respuestas abiertas, subagentes separados sin historial compartido. Mantener las mismas condiciones entre variantes; si se compara con/sin instrucciones, asignar etiquetas ciegas.
- **Verificar con evidencia:** preferir comprobaciones deterministas para propiedades observables y jueces independientes para calidad abierta. Revisar sus justificaciones; un juez también puede equivocarse. Reservar a la persona los juicios ambiguos o de seguridad que requieran validación humana. Un fallo crítico no se compensa con presentación o cobertura secundaria.
- **Medir sin exagerar:** registrar intentos, fallos, extensión y costo/latencia cuando se puedan medir. Informar `pass@k` y `pass^k` solo con intentos comparables suficientes y explicar qué se contó como éxito. Una corrida no demuestra estabilidad ni una ventaja frente a otra variante no evaluada.
- **Registrar y mantener:** conservar definiciones y resumen durable de resultados en el plugin, con ubicación de artefactos crudos, límites y pendientes. Repetir las pruebas afectadas después de cambios respaldados por fallos observados; conservar los resultados previos. No ajustar instrucciones solo para satisfacer ejemplos conocidos.
- **Respetar ejecución y permisos:** usar el procedimiento de sesiones independientes del repo, sin scripts que invoquen modelos pagos. No sortear negativas del harness ni confundir aislamiento por instrucciones con aislamiento del sistema. Si una herramienta impide ejecutar candidatos por falta de contención, respetar ese límite y declarar qué modalidades de evaluación sí se realizaron.
