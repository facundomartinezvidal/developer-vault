# AGENTS.md

Marketplace de plugins para desarrolladores (`.claude-plugin/marketplace.json` y, para Codex, `.agents/plugins/marketplace.json`). Tiene dos plugins: `plugins/architect` y `plugins/developer`.

## Dónde trabajar

- `plugins/architect/` — agente `architect` y 6 skills (decisiones/ADRs, documentación C4, threat modeling, Clean Architecture, DDD, software design). Instalable en Claude Code, GitHub Copilot CLI y Codex.
- `plugins/developer/` — agente `developer` (consultor y realizador de código, para cualquier lenguaje) y 15 skills (frameworks con ASP.NET Core y Spring Boot, implementación de diseños de `architect`, clean code, revisión, refactoring, testing, debugging, seguridad, APIs, producción, interfaces, patrones, estructuras y algoritmos, bases relacionales, prácticas). Instalable en Claude Code, GitHub Copilot CLI y Codex.
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
