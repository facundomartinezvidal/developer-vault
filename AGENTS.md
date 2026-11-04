# AGENTS.md

Marketplace de plugins para desarrolladores (`.claude-plugin/marketplace.json`). Hoy tiene un solo plugin: `plugins/architect`.

## Dónde trabajar

- `plugins/architect/` — agente `architect` y 6 skills (decisiones/ADRs, documentación C4, threat modeling, Clean Architecture, DDD, software design). Instalable en Claude Code y GitHub Copilot CLI.
- **Antes de tocar el plugin, leé `plugins/architect/AGENTS.md`**: estado, reglas de mantenimiento, evaluaciones y próximos pasos. El uso está en `plugins/architect/README.md`.

## Reglas clave

- **No editar a mano lo generado:** `plugins/architect/agents/`, `com.github.copilot/`, `skills/architect/` y los `references/` sincronizados del vault. Se cambian en `plugins/architect/src/architect.md` o en el vault.
- Regenerar con `python3 scripts/build_agents.py` (desde `plugins/architect`); con `--check` falla si algo quedó desactualizado.
- Validar: `claude plugin validate .` desde `plugins/architect` y desde la raíz.
- Las evaluaciones (`evals/`) no las lee el agente; no exponer criterios a quien responde.
- El vault de Obsidian vive fuera de este repo. No copiar PDFs de libros.
- Commits: sin cambios no relacionados; los scripts no invocan modelos ni cuestan dinero.

## Al agregar un plugin

Registrarlo en `.claude-plugin/marketplace.json`, darle su propio `AGENTS.md` y `README.md`, y enlazarlo desde este archivo.
