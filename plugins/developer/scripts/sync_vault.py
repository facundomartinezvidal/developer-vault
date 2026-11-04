#!/usr/bin/env python3
"""Rebuild each skill's vault-backed references/*.md from an Obsidian vault.

Usage:
    python3 scripts/sync_vault.py <path-to-developer-knowledge> [--check]

--check rebuilds in memory and exits 1 if any file on disk is stale (for CI).

Each reference file is a concatenation of whole notes, with Obsidian-only syntax removed:
frontmatter (including deep links into book PDFs) is dropped, [[wikilinks]] become plain
text naming the target reference file when it lives in another one, and "Related" bullets
pointing at notes outside the skill are dropped, since the reader can't follow them.
Blockquotes are dropped too, because they hold verbatim book quotes and the repo is public.
Passages quoted inside paragraphs are reworded through quote_rewrites.py.
Hand-written reference files are not listed in the manifest and are left alone.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quote_rewrites import apply as rewrite_quotes  # noqa: E402
from vault_manifest import SKILLS  # noqa: E402

PLUGIN_DIR = Path(__file__).resolve().parent.parent
TOC_THRESHOLD_LINES = 100
WIKILINK = re.compile(r"\[\[([^\]|#]*)(#[^\]|]*)?(?:\|([^\]]*))?\]\]")


def split_note(text):
    """Return (title, body) with the frontmatter and the H1 removed."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end == -1:
            raise ValueError("unterminated frontmatter")
        text = text[end + 4 :]
    lines = text.strip().splitlines()
    title_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if title_idx is None:
        raise ValueError("no '# ' title")
    body = lines[title_idx + 1 :]
    while body and not body[0].strip():
        body.pop(0)
    return lines[title_idx][2:].strip(), body


def target_of(raw):
    # Inside Markdown tables Obsidian links escape the pipe: [[note\|Label]].
    return raw.strip().rstrip("\\")


def render_links(line, index, current_file):
    def repl(m):
        target, anchor_part, alias = target_of(m.group(1)), m.group(2), m.group(3)
        if not target and anchor_part:  # same-note anchor like [[#Conway's law|...]]
            return alias or anchor_part[1:]
        if alias:
            label = alias.strip()
        elif target in index:
            label = index[target][0]
        else:
            label = target.replace("-", " ")
        if target in index and index[target][1] != current_file:
            return f"{label} (`{index[target][1]}`)"
        return label

    return WIKILINK.sub(repl, line)


def convert_note(body, index, current_file):
    out, in_related, in_code = [], False, False
    for line in body:
        if line.startswith("```"):
            in_code = not in_code
        if in_code or line.startswith("```"):
            out.append(line)
            continue
        if line.startswith(">"):
            continue  # book quotes stay in the private vault: the repo is public
        if line.startswith("**Source:**"):
            out.append(WIKILINK.sub(lambda m: m.group(3) or target_of(m.group(1)), line))
            continue
        if line.startswith("## "):
            was_related = in_related
            in_related = line.strip() == "## Related"
            if in_related and was_related:
                continue  # a note with a duplicated Related heading
        if in_related and line.startswith("- "):
            targets = [target_of(m.group(1)) for m in WIKILINK.finditer(line)]
            if not targets or targets[0] not in index:
                continue
        if line.startswith("#"):
            line = "#" + line  # note headings drop one level under the file's H1
        out.append(render_links(line, index, current_file))
    while out and not out[-1].strip():
        out.pop()
    if out and out[-1].strip() == "### Related":
        out.pop()
    return out


def anchor(title):
    return re.sub(r"\s+", "-", re.sub(r"[^\w\- ]", "", title.lower()).strip())


def build_file(vault, spec, ref_file, index):
    title, intro, notes = spec
    content, titles = [], []
    for rel in notes:
        note_title, body = split_note((vault / rel).read_text(encoding="utf-8"))
        titles.append(note_title)
        content += [f"## {note_title}", ""] + convert_note(body, index, ref_file) + [""]
    head = [f"# {title}", "", intro, ""]
    if len(content) > TOC_THRESHOLD_LINES:
        head += ["## Contents", ""] + [f"- [{t}](#{anchor(t)})" for t in titles] + [""]
    return rewrite_quotes("\n".join(head + content).rstrip() + "\n")


def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    check = "--check" in sys.argv[1:]
    if len(args) != 1:
        sys.exit(__doc__)
    vault = Path(args[0]).expanduser()
    missing = sorted(
        rel
        for refs in SKILLS.values()
        for _, _, notes in refs.values()
        for rel in notes
        if not (vault / rel).is_file()
    )
    if missing:
        sys.exit("Notes not found in the vault:\n  " + "\n  ".join(missing))

    stale = []
    for skill, refs in SKILLS.items():
        index = {}
        for ref_file, (_, _, notes) in refs.items():
            for rel in notes:
                title, _ = split_note((vault / rel).read_text(encoding="utf-8"))
                index[Path(rel).stem] = (title, ref_file)
        out_dir = PLUGIN_DIR / "skills" / skill / "references"
        for ref_file, spec in refs.items():
            text = build_file(vault, spec, ref_file, index)
            path = out_dir / ref_file
            if check:
                if not path.is_file() or path.read_text(encoding="utf-8") != text:
                    stale.append(f"{skill}/references/{ref_file}")
                continue
            out_dir.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"{skill}/references/{ref_file}: {text.count(chr(10))} lines")
    if stale:
        sys.exit("Stale, re-run sync_vault.py:\n  " + "\n  ".join(stale))


if __name__ == "__main__":
    main()
