# developer

A software developer agent and fifteen skills for any programming language, usable from Claude Code, GitHub Copilot CLI and Codex. It builds and changes code, and it also works as a consultant: a question gets analysis, and a request to build or change gets the verified change.

| Skill | Use it for |
|---|---|
| `framework-practices` | Framework best practices for the installed version, with deep guidance for ASP.NET Core and Spring Boot, looked up through Context7 or the official docs |
| `implementing-designs` | Turning ADRs, designs and threat models from `architect` into enforced, verified code |
| `clean-code` | Names, functions, comments, classes, errors, async code, translating ideas across languages |
| `reviewing-code` | Reviewing diffs and pull requests, and preparing them |
| `refactoring` | Code smells, the catalog of moves and behavior-preserving changes |
| `testing` | What to test, test levels and doubles, legacy code, flaky tests, TDD |
| `debugging` | Root causes, intermittent and production failures, tools by symptom |
| `secure-coding` | Injection, access control, secrets, crypto, dependencies |
| `api-design` | Endpoints, errors, pagination, idempotency, compatibility |
| `production-readiness` | Logs, metrics, timeouts, retries, safe releases |
| `user-interfaces` | Screen states, forms, accessibility, front-end behavior |
| `design-patterns` | Whether a pattern fits, GRASP, modern equivalents, anti-patterns |
| `data-structures-and-algorithms` | Choosing structures and algorithms, complexity, profiling |
| `relational-databases` | Schemas, SQL, indexes, transactions, migrations |
| `pragmatic-practices` | Requirements, estimates, Git, upgrades, documentation, teamwork |

`developer` is both an agent and a skill, so it still works in tools without custom agents. Use the [`architect`](../architect/README.md) agent to plan, design and consult on structure, and `developer` to implement the plan and consult on code. It hands new structural decisions back to `architect`. Framework lookups work best with the [Context7](https://context7.com) MCP server connected; without it the agent uses the official docs, or says that it couldn't check.

## Install

You don't need to clone the repo.

**Claude Code**

```bash
claude plugin marketplace add facundomartinezvidal/developer-vault
```

```bash
claude plugin install developer@developer-vault
```

**GitHub Copilot CLI**

```bash
copilot plugin marketplace add facundomartinezvidal/developer-vault
```

```bash
copilot plugin install developer@developer-vault
```

**Codex**

```bash
codex plugin marketplace add facundomartinezvidal/developer-vault
```

```bash
codex plugin add developer@developer-vault
```

In Codex, the plugin provides the skills, and `developer:developer` holds the agent's instructions, so mention that skill to work in this role. Codex plugins can't ship custom agents yet. To also use it as a Codex subagent, install the plugin and add the agent file:

```bash
mkdir -p ~/.codex/agents && curl -fsSL https://raw.githubusercontent.com/facundomartinezvidal/developer-vault/main/plugins/developer/com.openai.codex/agents/developer.toml -o ~/.codex/agents/developer.toml
```

To get updates, run `codex plugin marketplace upgrade developer-vault`, or the matching `marketplace update` command in the other tools.

For a single session from a clone: `claude --plugin-dir plugins/developer --agent developer:developer`, or the same flags with `copilot`.

## Develop

- Agent: edit `src/developer.md`, then run `python3 scripts/build_agents.py`.
- References: those listed in `scripts/vault_manifest.py` come from the vault, via `python3 scripts/sync_vault.py <path-to-developer-knowledge>`, so don't edit them by hand. The rest are hand-written, and say so at the top.
- Static validation: create a virtual environment, install `requirements-dev.txt`, then run `python scripts/eval_suite.py validate` from this folder. Run `python -m unittest discover -s scripts/tests -v` for evaluation-accounting checks.
- Behavioral evaluation: `python scripts/eval_suite.py prepare --output /tmp/developer-evaluation`, then `blind` and `report`. The procedure is the same as in the architect plugin, and is described in `AGENTS.md`.
- The scripts do not invoke or bill models. Add `--check` to the build and sync scripts in CI to catch stale output.

## Consultas durante una review

El agente puede responder preguntas acotadas del plugin [reviewer](../reviewer/README.md) en modo consulta: devuelve conclusión, evidencia, supuestos, contraejemplos y una recomendación proporcionada, indicando si corresponde a la PR o a un seguimiento. No edita ni publica durante esa consulta. `reviewer` integra las respuestas y acuerda con la persona todo el contenido de la review.
