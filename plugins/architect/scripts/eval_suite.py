#!/usr/bin/env python3
"""Validate skills and prepare instruction-isolated, blind behavioral evaluations.

This script never calls a model. Solvers receive one run directory and an optional
context path, never the manifest or grading directories. Isolation is procedural,
not an OS sandbox. Reports require evidence-backed grades from independent judges.
"""
import argparse
import hashlib
import json
import random
import re
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPECIALISTS = sorted(p.name for p in (ROOT / 'skills').iterdir() if (p / 'SKILL.md').exists() and p.name != 'architect')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n?(.*)', text, re.S)
    if not match:
        raise ValueError(f'{path}: missing frontmatter')
    data = yaml.safe_load(match[1])
    if not isinstance(data, dict):
        raise ValueError(f'{path}: frontmatter must be a mapping')
    return data, match[2].strip()


def cases(skill):
    folder = ROOT / ('evals' if skill == 'architect' else f'skills/{skill}/evals')
    return sorted(p for p in folder.iterdir() if p.is_dir() and (p / 'case.yaml').exists())


def validate():
    count = 0
    for skill in SPECIALISTS + ['architect']:
        folder = ROOT / 'skills' / skill
        data, body = frontmatter(folder / 'SKILL.md')
        assert data['name'] == skill, f'{skill}: name mismatch'
        assert isinstance(data['description'], str) and 0 < len(data['description']) <= 1024, f'{skill}: description length'
        assert len((folder / 'SKILL.md').read_text().splitlines()) < 500, f'{skill}: length'
        assert '[TODO:' not in body, f'{skill}: unfinished scaffold'
        assert not re.search(r'!\[\[|\[\[', body), f'{skill}: Obsidian syntax'
        for ref in set(re.findall(r'(?:references|assets)/[\w./-]+\.\w+', body)):
            assert (folder / ref).is_file(), f'{skill}: missing {ref}'
        for case in cases(skill):
            metadata = yaml.safe_load((case / 'case.yaml').read_text())
            assert metadata['name'] == case.name and metadata['schema_version'] == '1.1', f'{case}: metadata'
            _, prompt = frontmatter(case / 'prompt.md')
            assert prompt, f'{case}: empty prompt'
            inputs = re.search(r'^Input files: (.+)$', prompt, re.M)
            if inputs:
                for name in inputs[1].split(', '):
                    assert (case / 'files' / name).is_file(), f'{case}: missing fixture {name}'
            graders = sorted((case / 'graders').glob('*.md'))
            assert graders, f'{case}: missing criteria'
            for grader in graders:
                gd, criterion = frontmatter(grader)
                assert gd['type'] == 'llm' and gd['weight'] == 1 and criterion, f'{grader}: invalid criterion'
            count += 1
        print(f'{skill}: valid ({len(cases(skill))} cases)')
    subprocess.run(['python3', str(ROOT / 'scripts/build_agents.py'), '--check'], check=True)
    print(f'{len(SPECIALISTS) + 1} skills, {count} cases; generated agents current')


def copy_context(src, dest):
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns('evals', '__pycache__'))


def prepare(output):
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    records = []
    for skill in SPECIALISTS + ['architect']:
        for case in cases(skill):
            _, prompt = frontmatter(case / 'prompt.md')
            criteria = []
            for path in sorted((case / 'graders').glob('*.md')):
                _, body = frontmatter(path)
                criteria.append({'id': path.stem, 'text': body, 'critical': bool(re.search(r'\bCRITICAL\b', body)), 'sha256': digest(path)})
            variants = ['with-skill'] if skill == 'architect' else ['without-skill', 'with-skill']
            for variant in variants:
                run_id = f'{len(records) + 1:03d}'
                work = output / 'runs' / run_id
                work.mkdir(parents=True)
                (work / 'request.txt').write_text(prompt)
                if (case / 'files').exists():
                    shutil.copytree(case / 'files', work, dirs_exist_ok=True)
                context = None
                if variant == 'with-skill':
                    context = output / 'contexts' / run_id
                    if skill == 'architect':
                        for name in SPECIALISTS + ['architect']:
                            copy_context(ROOT / 'skills' / name, context / 'skills' / name)
                        context = context / 'skills' / 'architect' / 'SKILL.md'
                    else:
                        copy_context(ROOT / 'skills' / skill, context)
                        context = context / 'SKILL.md'
                records.append({'id': run_id, 'skill': skill, 'case': case.name, 'variant': variant,
                                'context': str(context) if context else None,
                                'skill_sha256': digest(ROOT / 'skills' / skill / 'SKILL.md'),
                                'context_files': {str(p.relative_to(output / 'contexts' / run_id)): digest(p) for p in (output / 'contexts' / run_id).rglob('*') if p.is_file()} if context else {},
                                'request_sha256': digest(work / 'request.txt'), 'criteria': criteria,
                                'fixtures': {str(p.relative_to(work)): digest(p) for p in work.rglob('*') if p.is_file() and p.name != 'request.txt'}})
    (output / 'manifest.json').write_text(json.dumps({'isolation': 'instruction-scoped independent sessions, not OS enforcement', 'runs': records}, indent=2))
    print(f'{output}: {len(records)} runs prepared; no models called')


def load(output):
    return json.loads((output / 'manifest.json').read_text())['runs']


def blind(output, selected_skill=None):
    records = load(output)
    selected = [r for r in records if selected_skill is None or r['skill'] == selected_skill]
    for run in selected:
        work = output / 'runs' / run['id']
        assert (work / 'answer.md').is_file(), f'missing answer: {work}'
        assert digest(work / 'request.txt') == run['request_sha256'], f'request mutated: {work}'
    mapping_path = output / 'mapping.json'
    mapping = json.loads(mapping_path.read_text()) if mapping_path.exists() else {}
    for skill in ([selected_skill] if selected_skill else SPECIALISTS + ['architect']):
        target = output / 'grading' / skill
        target.mkdir(parents=True, exist_ok=False)
        groups = {}
        for run in records:
            if run['skill'] == skill:
                groups.setdefault(run['case'], []).append(run)
        for case, runs in groups.items():
            random.SystemRandom().shuffle(runs)
            case_dir = target / case
            case_dir.mkdir()
            (case_dir / 'request.txt').write_text((output / 'runs' / runs[0]['id'] / 'request.txt').read_text())
            (case_dir / 'criteria.json').write_text(json.dumps(runs[0]['criteria'], indent=2))
            mapping[f'{skill}/{case}'] = {}
            for label, run in zip('AB', runs):
                work = output / 'runs' / run['id']
                assert (work / 'answer.md').is_file(), f'missing answer: {work}'
                assert digest(work / 'request.txt') == run['request_sha256'], f'request mutated: {work}'
                shutil.copytree(work, case_dir / label, ignore=shutil.ignore_patterns('request.txt'))
                mapping[f'{skill}/{case}'][label] = run['id']
    (output / 'mapping.json').write_text(json.dumps(mapping, indent=2))
    print('Blind artifacts prepared; judges receive only one grading/<skill> directory')


def report(output):
    raw_records = load(output)
    records = {r['id']: r for r in raw_records}
    assert records and len(records) == len(raw_records), 'empty or duplicate run manifest'
    mapping = json.loads((output / 'mapping.json').read_text())
    mapped_ids = [run_id for labels in mapping.values() for run_id in labels.values()]
    assert len(mapped_ids) == len(set(mapped_ids)) and set(mapped_ids) == set(records), 'incomplete or duplicate run coverage'
    for key, labels in mapping.items():
        for run_id in labels.values():
            run = records[run_id]
            assert key == f"{run['skill']}/{run['case']}", f'{key}: mismatched run identity'
    result = {'limitations': ['Model-judged behavioral examples, not a guarantee on arbitrary tasks.', 'No claim of native client invocation or stability from one run.', 'Critical failures are separate from coverage totals.'], 'runs': []}
    for key, labels in mapping.items():
        skill, case = key.split('/')
        grades = json.loads((output / 'grading' / skill / 'grades.json').read_text())['cases'][case]
        for label, run_id in labels.items():
            run = records[run_id]
            items = grades[label]['results']
            expected = {c['id'] for c in run['criteria']}
            assert {x['criterion'] for x in items} == expected and len(items) == len(expected), f'{key}/{label}: missing/duplicate criteria'
            assert all(type(x['pass']) is bool and x['reason'].strip() for x in items), f'{key}/{label}: invalid grades'
            total = sum(x['pass'] for x in items)
            assert total == grades[label]['total'], f'{key}/{label}: wrong total'
            critical_ids = {c['id'] for c in run['criteria'] if c['critical']}
            critical_failures = [x for x in items if x['criterion'] in critical_ids and not x['pass']]
            work = output / 'runs' / run_id
            assert digest(work / 'request.txt') == run['request_sha256'], f'{work}: request changed'
            for name, expected_hash in run.get('context_files', {}).items():
                assert digest(output / 'contexts' / run_id / name) == expected_hash, f'{run_id}: context mutated: {name}'
            answer_words = len((work / 'answer.md').read_text().split())
            artifact_words = sum(len(p.read_text().split()) for p in work.rglob('*.md') if p.name not in {'answer.md'} and str(p.relative_to(work)) not in run['fixtures'])
            result['runs'].append({**run, 'label': label, 'score': total, 'out_of': len(items), 'critical_failures': critical_failures, 'grades': items, 'words': answer_words + artifact_words, 'answer_sha256': digest(work / 'answer.md')})
    result['all_with_skill_critical_pass'] = all(not r['critical_failures'] for r in result['runs'] if r['variant'] == 'with-skill')
    (output / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    for skill in SPECIALISTS + ['architect']:
        for variant in ['with-skill', 'without-skill']:
            group = [r for r in result['runs'] if r['skill'] == skill and r['variant'] == variant]
            if group:
                print(skill, variant, f"{sum(r['score'] for r in group)}/{sum(r['out_of'] for r in group)}", 'critical failures:', sum(len(r['critical_failures']) for r in group))
    if not result['all_with_skill_critical_pass']:
        raise SystemExit('Critical with-skill failures remain')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'prepare', 'blind', 'report'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--skill', choices=SPECIALISTS + ['architect'], help='Limit blind preparation to one completed skill')
    args = parser.parse_args()
    if args.command == 'validate':
        validate()
    else:
        if args.output is None:
            parser.error('--output is required')
        if args.command == 'blind':
            blind(args.output, args.skill)
        else:
            if args.skill:
                parser.error('--skill applies only to blind')
            {'prepare': prepare, 'report': report}[args.command](args.output)


if __name__ == '__main__':
    main()
