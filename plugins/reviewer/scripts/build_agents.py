#!/usr/bin/env python3
"""Generate each tool's agents and role skills from src/*.md.

Usage:
    python3 scripts/build_agents.py [--check]

--check exits 1 if a generated file is stale (for CI). Edit src/<name>.md, never the outputs.

Tools disagree on agent formats, so each source becomes:
    agents/<name>.md                         Claude Code
    com.github.copilot/agents/<name>.agent.md  GitHub Copilot CLI
    skills/<name>/SKILL.md                   any tool that reads Agent Skills, including Codex plugins
    com.openai.codex/agents/<name>.toml      Codex custom agent, which plugins can't ship yet
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTICE = "<!-- Generated from src/{name}.md by scripts/build_agents.py. Do not edit. -->\n"


def read_source(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n\n(.*)\Z", text, re.S)
    if not match:
        sys.exit(f"{path}: expected frontmatter with name and description")
    if match.group(1) != path.stem:
        sys.exit(f"{path}: name must match source filename")
    return match.groups()


def yaml_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def toml_agent(name, description, body):
    if "'''" in body:
        sys.exit(f"src/{name}.md: a triple single quote can't go in a TOML literal string")
    return (
        NOTICE.format(name=name).replace("<!-- ", "# ").replace(" -->", "")
        + f"name = {yaml_string(name)}\n"
        + f"description = {yaml_string(description)}\n"
        + f"developer_instructions = '''\n{body}'''\n"
    )


def outputs():
    generated = {}
    for source in sorted((ROOT / "src").glob("*.md")):
        name, description, body = read_source(source)
        frontmatter = f"---\nname: {name}\ndescription: {yaml_string(description)}\n---\n\n"
        markdown = frontmatter + NOTICE.format(name=name) + "\n" + body
        generated.update({
            f"agents/{name}.md": markdown,
            f"com.github.copilot/agents/{name}.agent.md": markdown,
            f"skills/{name}/SKILL.md": markdown,
            f"com.openai.codex/agents/{name}.toml": toml_agent(name, description, body),
        })
    return generated


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
