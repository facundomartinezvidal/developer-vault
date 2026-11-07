"""Package shared instructions from their owning sources, without eval material.

Imported by plugin generators. Copies are private references under the role skill,
so each plugin remains usable without installing the other one. No symlinks or
cross-plugin runtime imports are needed. Run plugin build_agents.py --check in CI.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHARED = {
    'architect': ('developer', ('design-patterns', 'api-design', 'testing',
                                'relational-databases', 'secure-coding', 'production-readiness')),
    'developer': ('architect', ('clean-architecture', 'domain-driven-design',
                                'software-design', 'threat-modeling')),
}
TOKEN = '{{SHARED_DECISION_PROTOCOL}}'


def expand_protocol(body, repo=REPO):
    if body.count(TOKEN) != 1:
        raise ValueError('Each role source must include the decision protocol exactly once')
    return body.replace(TOKEN, (repo / 'shared/decision-protocol.md').read_text().strip())


def expand_language(body, repo=REPO):
    token = '{{UBIQUITOUS_LANGUAGE}}'
    if body.count(token) != 1:
        raise ValueError('Each role source must include the language guidance exactly once')
    return body.replace(token, (repo / 'shared/ubiquitous-language.md').read_text().strip())


def shared_outputs(role, repo=REPO):
    owner, names = SHARED[role]
    outputs = {}
    for name in names:
        source = repo / 'plugins' / owner / 'skills' / name
        for path in sorted(source.rglob('*')):
            relative = path.relative_to(source)
            if not path.is_file() or any(part in {'evals', '__pycache__'} for part in relative.parts):
                continue
            if path.is_symlink():
                raise ValueError(f'Shared guidance must be regular files: {path}')
            target = Path('skills') / role / 'references/shared' / name / relative
            outputs[str(target)] = path.read_text(encoding='utf-8')
        if not (source / 'SKILL.md').is_file():
            raise ValueError(f'Missing owning skill: {source}')
    return outputs


def unexpected_shared_files(plugin, expected):
    """Reject leftovers instead of shipping removed or renamed source material."""
    root = plugin / 'skills' / plugin.name / 'references/shared'
    return [str(p.relative_to(plugin)) for p in root.rglob('*')
            if p.is_file() and str(p.relative_to(plugin)) not in expected]
