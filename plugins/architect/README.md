# architect

A software architecture agent and six skills, usable from Claude Code and GitHub Copilot CLI.

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
- Static validation: create a virtual environment, install `requirements-dev.txt`, then run `python scripts/eval_suite.py validate` from this folder. It checks all seven skill entrypoints, referenced files, case metadata, fixtures, criteria and generated agent freshness. Run `python -m unittest discover -s scripts/tests -v` for evaluation-accounting checks.
- Behavioral evaluation: `python scripts/eval_suite.py prepare --output /tmp/architect-evaluation` creates fresh workspaces and snapshots without exposing criteria to solvers. Use independent model sessions with identical requests for each variant. Give each solver only its run directory and optional context path; save its response as `answer.md` and the requested artifacts inside that workspace. This is instruction-based isolation, not an OS access boundary.
- Once answers exist, `python scripts/eval_suite.py blind --output /tmp/architect-evaluation` creates randomized A/B packages. Independent judges receive only their `grading/<skill>` directory, apply each criterion with evidence, and write `grades.json` as `{"cases":{"case-name":{"A":{"results":[{"criterion":"criterion-id","pass":true,"reason":"evidence"}],"total":1},"B":{...}}}}`. The agent-only cases have one label. `python scripts/eval_suite.py report --output /tmp/architect-evaluation` checks completeness and fails on critical with-skill errors; inspect other failures and limitations before interpreting totals. `--skill <name>` can limit blind packaging to a completed skill.
- Diagram rendering: `python scripts/render_mermaid.py <markdown-file-or-folder> --mmdc <path-to-mmdc> --output /tmp/architect-diagrams` renders the exact Mermaid fences to SVG and PNG and records tool failures. Supply `--puppeteer-config <file>` when a local browser is needed. It downloads nothing. Inspect the rendered images separately; rendering is not visual review.
- The scripts do not invoke or bill models. `claude plugin eval` is a separate billed workflow, not required for these checks. Evaluation status, known limits and maintenance rules are in `AGENTS.md`.
- Add `--check` to either script in CI to catch stale output.
