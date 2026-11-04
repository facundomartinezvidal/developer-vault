#!/usr/bin/env python3
"""Render exact Mermaid fences with an explicitly supplied Mermaid CLI.

No packages are downloaded and no diagram source is rewritten. SVG/PNG and a
machine-readable render report remain in --output for subsequent visual review.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+', type=Path)
    parser.add_argument('--mmdc', required=True, type=Path)
    parser.add_argument('--puppeteer-config', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sources = sorted({p.resolve() for item in args.inputs for p in (item.rglob('*.md') if item.is_dir() else [item])})
    results = []
    for source in sources:
        for index, match in enumerate(re.finditer(r'^```mermaid[^\n]*\n(.*?)^```\s*$', source.read_text(), re.M | re.S), 1):
            label = f'{len(results) + 1:03d}'
            diagram = args.output / f'{label}.mmd'
            diagram.write_text(match[1])
            item = {'source': str(source), 'fence': index, 'diagram': str(diagram), 'outputs': []}
            for extension in ['svg', 'png']:
                dest = args.output / f'{label}.{extension}'
                command = [str(args.mmdc), '-i', str(diagram), '-o', str(dest), '-b', 'white']
                if args.puppeteer_config:
                    command += ['-p', str(args.puppeteer_config)]
                completed = subprocess.run(command, capture_output=True, text=True, timeout=90)
                item['outputs'].append({'path': str(dest), 'returncode': completed.returncode, 'message': (completed.stdout + completed.stderr)[-3000:]})
            item['rendered'] = all(x['returncode'] == 0 and Path(x['path']).is_file() for x in item['outputs'])
            results.append(item)
            print(label, 'OK' if item['rendered'] else 'FAILED', source, 'fence', index, flush=True)
    (args.output / 'render-report.json').write_text(json.dumps({'visual_review_performed': False, 'diagrams': results}, indent=2))
    if not results:
        raise SystemExit('No Mermaid diagrams found; no rendering was validated')
    if any(not item['rendered'] for item in results):
        raise SystemExit('Some diagrams failed; see render-report.json')


if __name__ == '__main__':
    main()
