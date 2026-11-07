# architect

A software architecture agent and six skills, usable from Claude Code, GitHub Copilot CLI and Codex.

| Skill | Use it for |
|---|---|
| `architecture-decisions` | Comparing options, recommending one, writing ADRs |
| `architecture-documentation` | C4 views, focused class diagrams and evidence-based architecture docs |
| `threat-modeling` | Design-level security review with STRIDE |
| `clean-architecture` | Layers, boundaries, dependencies and project structure |
| `domain-driven-design` | Shared business language, bounded contexts and consistency rules |
| `software-design` | Interfaces, information hiding, caller protocols and failure contracts |

`architect` plans, designs and consults, and doesn't edit code. The [`developer`](../developer/README.md) agent implements its plans. `architect` is both an agent and a skill, so it still works in tools without custom agents.

## Install

You don't need to clone the repo.

**Claude Code**

```bash
claude plugin marketplace add facundomartinezvidal/developer-vault
```

```bash
claude plugin install architect@developer-vault
```

**GitHub Copilot CLI**

```bash
copilot plugin marketplace add facundomartinezvidal/developer-vault
```

```bash
copilot plugin install architect@developer-vault
```

**Codex**

```bash
codex plugin marketplace add facundomartinezvidal/developer-vault
```

```bash
codex plugin add architect@developer-vault
```

In Codex, the plugin provides the skills, and `architect:architect` holds the agent's instructions, so mention that skill to work in this role. Codex plugins can't ship custom agents yet. To also use it as a Codex subagent, install the plugin and add the agent file:

```bash
mkdir -p ~/.codex/agents && curl -fsSL https://raw.githubusercontent.com/facundomartinezvidal/developer-vault/main/plugins/architect/com.openai.codex/agents/architect.toml -o ~/.codex/agents/architect.toml
```

To get updates, run `codex plugin marketplace upgrade developer-vault`, or the matching `marketplace update` command in the other tools.

For a single session from a clone: `claude --plugin-dir plugins/architect --agent architect:architect`, or the same flags with `copilot`.

## Develop

- Agent: edit `src/architect.md`, then run `python3 scripts/build_agents.py`.
- Vault-backed references: run `python3 scripts/sync_vault.py <path-to-developer-knowledge>`. `scripts/vault_manifest.py` lists which notes feed which file. Don't edit those references by hand.
- Static validation: create a virtual environment, install `requirements-dev.txt`, then run `python scripts/eval_suite.py validate` from this folder. It checks all seven skill entrypoints, referenced files, case metadata, fixtures, criteria and generated agent freshness. Run `python -m unittest discover -s scripts/tests -v` for evaluation-accounting checks.
- Behavioral evaluation: `python scripts/eval_suite.py prepare --output /tmp/architect-evaluation` creates fresh workspaces and snapshots without exposing criteria to solvers. Use independent model sessions with identical requests for each variant. Give each solver only its run directory and optional context path; save its response as `answer.md` and the requested artifacts inside that workspace. This is instruction-based isolation, not an OS access boundary.
- Once answers exist, `python scripts/eval_suite.py blind --output /tmp/architect-evaluation` creates randomized A/B packages. Independent judges receive only their `grading/<skill>` directory, apply each criterion with evidence, and write `grades.json` as `{"cases":{"case-name":{"A":{"results":[{"criterion":"criterion-id","pass":true,"reason":"evidence"}],"total":1},"B":{...}}}}`. The agent-only cases have one label. `python scripts/eval_suite.py report --output /tmp/architect-evaluation` checks completeness and fails on critical with-skill errors; inspect other failures and limitations before interpreting totals. `--skill <name>` can limit blind packaging to a completed skill.
- Diagram rendering: `python scripts/render_mermaid.py <markdown-file-or-folder> --mmdc <path-to-mmdc> --output /tmp/architect-diagrams` renders the exact Mermaid fences to SVG and PNG and records tool failures. Supply `--puppeteer-config <file>` when a local browser is needed. It downloads nothing. Inspect the rendered images separately; rendering is not visual review.
- The scripts do not invoke or bill models. `claude plugin eval` is a separate billed workflow, not required for these checks. Evaluation status, known limits and maintenance rules are in `AGENTS.md`.
- Add `--check` to either script in CI to catch stale output.


## Consultas durante una review

El agente puede responder preguntas acotadas del plugin [reviewer](../reviewer/README.md) en modo consulta: devuelve conclusión, evidencia, supuestos, contraejemplos y una recomendación proporcionada, indicando si corresponde a la PR o a un seguimiento. No edita ni publica durante esa consulta. `reviewer` integra las respuestas y acuerda con la persona todo el contenido de la review.

## Shared knowledge and design approval

New decisions about applicable patterns, boundaries, contracts, business rules,
consistency and failure behavior are proposed to the user before dependent
implementation. Existing approvals are reused; local coding details remain
within the implementer's discretion. Read-only review remains analysis only.
The coordinating agent checks approval evidence before handing off implementation;
agreement between agents is not user approval. Pending decisions do not block
independent authorized work.

The role includes selected guidance owned by the other plugin as generated,
private references under `skills/architect/references/shared/`. This works without
installing that plugin and does not grant its role or write permissions. Read
only relevant references, rather than loading the entire collection.

Maintenance requires a full repository checkout. Edit the owning specialist's
source, `src/architect.md`, or `shared/decision-protocol.md`, then regenerate **both**
plugins. `scripts/shared_guidance.py` defines ownership and packaging;
`build_agents.py --check` detects source drift. Do not edit generated copies.
Run `python3 -m unittest discover -s scripts/tests -v` from the repository root
for shared-package and client-format checks. Behavioral evaluation and its
limits are recorded in `evals/shared-design-v1/summary.md` at the repository root.

These rules are instructions, not a runtime permission or approval mechanism.
