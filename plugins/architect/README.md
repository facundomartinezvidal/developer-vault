# architect

A software architecture agent and six skills, usable from Claude Code and GitHub Copilot CLI.

| Skill | Use it for |
|---|---|
| `architecture-decisions` | Comparing options, recommending one, writing ADRs |
| `architecture-documentation` | C4 diagrams and architecture docs for a specific audience |
| `threat-modeling` | Design-level security review with STRIDE |
| `clean-architecture` | Layers, boundaries, dependencies and project structure |
| `domain-driven-design` | Bounded contexts, context maps and aggregates |
| `software-design` | Modules, interfaces, coupling and concurrency |

`architect` is both an agent and a skill, so it still works in tools without custom agents.

## Install

From a clone of this repo. Replace the path with a repo reference once it's published.

**Claude Code**

```bash
claude plugin marketplace add ./
claude plugin install architect@developer-vault
```

For a single session: `claude --plugin-dir plugins/architect --agent architect:architect`

**GitHub Copilot CLI**

```bash
copilot plugin marketplace add ./
copilot plugin install architect@developer-vault
```

For a single session: `copilot --plugin-dir plugins/architect --agent architect:architect`

## Develop

- Agent: edit `src/architect.md`, then run `python3 scripts/build_agents.py`.
- Vault-backed references: run `python3 scripts/sync_vault.py <path-to-developer-knowledge>`. `scripts/vault_manifest.py` lists which notes feed which file. Don't edit those references by hand.
- Tests: each skill has `evals/`. Run them with `claude plugin eval plugins/architect`. These are billed model runs.
- Add `--check` to either script in CI to catch stale output.
