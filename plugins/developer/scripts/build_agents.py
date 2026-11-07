#!/usr/bin/env python3
"""Generate each tool's version of the developer agent from src/developer.md.

Usage:
    python3 scripts/build_agents.py [--check]

--check exits 1 if a generated file is stale (for CI). Edit src/developer.md, never the outputs.

Tools disagree on agent formats, so the one source becomes:
    agents/developer.md                         Claude Code
    com.github.copilot/agents/developer.agent.md  GitHub Copilot CLI
    skills/developer/SKILL.md                   any tool that reads Agent Skills, including Codex plugins
    com.openai.codex/agents/developer.toml      Codex custom agent, which plugins can't ship yet
"""

import re
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = runpy.run_path(str(ROOT.parent.parent / "scripts/shared_guidance.py"))
NOTICE = "<!-- Generated from src/developer.md by scripts/build_agents.py. Do not edit. -->\n"


def read_source():
    text = (ROOT / "src/developer.md").read_text(encoding="utf-8")
    match = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n\n(.*)\Z", text, re.S)
    if not match:
        sys.exit("src/developer.md: expected frontmatter with name and description")
    name, description, body = match.groups()
    return name, description, SHARED["expand_protocol"](body)


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
        **SHARED["shared_outputs"]("developer"),
        "agents/developer.md": markdown,
        "com.github.copilot/agents/developer.agent.md": markdown,
        "skills/developer/SKILL.md": markdown,
        "com.openai.codex/agents/developer.toml": toml_agent(name, description, body),
    }


def main():
    check = "--check" in sys.argv[1:]
    generated = outputs()
    stale = SHARED["unexpected_shared_files"](ROOT, generated)
    if stale:
        sys.exit("Unexpected shared files; review and remove obsolete generated copies:\n" + "\n".join(stale))
    for rel, content in generated.items():
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
