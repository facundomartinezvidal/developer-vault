#!/usr/bin/env python3
"""Generate each tool's version of the architect agent from src/architect.md.

Usage:
    python3 scripts/build_agents.py [--check]

--check exits 1 if a generated file is stale (for CI). Edit src/architect.md, never the outputs.

Tools disagree on agent formats, so the one source becomes:
    agents/architect.md                         Claude Code
    com.github.copilot/agents/architect.agent.md  GitHub Copilot CLI
    skills/architect/SKILL.md                   any tool that reads Agent Skills, including Codex plugins
    com.openai.codex/agents/architect.toml      Codex custom agent, which plugins can't ship yet
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTICE = "<!-- Generated from src/architect.md by scripts/build_agents.py. Do not edit. -->\n"


def read_source():
    text = (ROOT / "src/architect.md").read_text(encoding="utf-8")
    match = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n\n(.*)\Z", text, re.S)
    if not match:
        sys.exit("src/architect.md: expected frontmatter with name and description")
    return match.groups()


def yaml_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def toml_agent(name, description, body):
    if "'''" in body:
        sys.exit(f"src/{name}.md: a triple single quote can't go in a TOML literal string")
    return (
        NOTICE.replace("<!-- ", "# ").replace(" -->", "")
        + f"name = {yaml_string(name)}\n"
        + f"description = {yaml_string(description)}\n"
        + f"developer_instructions = '''\n{body}'''\n"
    )


def outputs():
    name, description, body = read_source()
    frontmatter = f"---\nname: {name}\ndescription: {yaml_string(description)}\n---\n\n"
    markdown = frontmatter + NOTICE + "\n" + body
    return {
        "agents/architect.md": markdown,
        "com.github.copilot/agents/architect.agent.md": markdown,
        "skills/architect/SKILL.md": markdown,
        "com.openai.codex/agents/architect.toml": toml_agent(name, description, body),
    }


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for rel, content in outputs().items():
        path = ROOT / rel
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(rel)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(rel)
    if stale:
        sys.exit("Stale, re-run build_agents.py:\n  " + "\n  ".join(stale))


if __name__ == "__main__":
    main()
