#!/usr/bin/env python3
"""Keep the architect agent from editing anything but design documents."""
import json
import sys
import tempfile
from pathlib import Path

AGENT = "architect:architect"
DESIGN_DOCUMENTS = {".md", ".mmd"}

event = json.load(sys.stdin)

if event.get("agent_type") != AGENT:
    sys.exit(0)  # Another agent or the main conversation: not our business.

path = event.get("tool_input", {}).get("file_path", "")
if Path(path).suffix.lower() in DESIGN_DOCUMENTS:
    sys.exit(0)  # An ADR, plan or diagram: allowed.

target = Path(path).resolve()
project = Path(event.get("cwd") or ".").resolve()
temporary = Path(tempfile.gettempdir()).resolve()
if path and target.is_relative_to(temporary) and not target.is_relative_to(project):
    sys.exit(0)  # A throwaway prototype outside the project: allowed.

print(
    f"architect only writes design documents (.md, .mmd), not {path or 'this file'}. "
    "Put the change in the plan for the developer agent, or prototype it in a temporary directory outside the project.",
    file=sys.stderr,
)
sys.exit(2)  # Exit code 2 blocks the tool call and shows the message to the agent.
