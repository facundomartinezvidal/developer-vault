#!/usr/bin/env python3
"""Validate recorded grades and summarize text product evals. Never invokes models."""
import argparse
import hashlib
import json
from pathlib import Path


def summarize(cases, runs, grades):
    by_case = {case['id']: case for case in cases}
    if len(by_case) != len(cases):
        raise ValueError('duplicate case')
    by_run = {run['id']: run for run in runs}
    by_grade = {grade['id']: grade for grade in grades}
    if len(by_run) != len(runs) or len(by_grade) != len(grades):
        raise ValueError('duplicate run or grade')
    if set(by_run) != set(by_grade):
        raise ValueError('missing or unexpected run grades')
    results = []
    for run in runs:
        expected = by_case[run['case']]['criteria']
        actual = by_grade[run['id']]['criteria']
        if len({c['id'] for c in actual}) != len(actual):
            raise ValueError('duplicate criterion')
        if {c['id'] for c in expected} != {c['id'] for c in actual}:
            raise ValueError('missing or unexpected criteria')
        for criterion in actual:
            if type(criterion['passed']) is not bool or not criterion['evidence'].strip():
                raise ValueError('criterion needs boolean result and evidence')
        failed = {c['id'] for c in actual if not c['passed']}
        results.append({
            'id': run['id'], 'case': run['case'], 'trial': run['trial'],
            'passed': not failed,
            'criteria_passed': len(actual) - len(failed), 'criteria_total': len(actual),
            'critical_failures': [c['id'] for c in expected if c['critical'] and c['id'] in failed],
            'failed': sorted(failed), 'words': run.get('words'),
        })
    first = [r for r in results if r['trial'] == 1]
    repeated = [r for r in results if r['case'] == 'collaborative-review']
    return {
        'runs': results,
        'sessions_passed': sum(r['passed'] for r in results), 'sessions_total': len(results),
        'first_trial_cases_passed': sum(r['passed'] for r in first), 'first_trial_cases_total': len(first),
        'criteria_passed': sum(r['criteria_passed'] for r in results),
        'criteria_total': sum(r['criteria_total'] for r in results),
        'critical_failures': sum(len(r['critical_failures']) for r in results),
        'collaborative_pass_all_3_observed': all(r['passed'] for r in repeated) if len(repeated) == 3 else None,
        'pass_at_3_suite': None,
        'limits': ['First-trial fraction is descriptive for these fixtures, not a population estimate.',
                   'pass@3 for suite unavailable: most cases have one trial.',
                   'No baseline comparison or client installation verification.',
                   'Independent model grading still needs human security/communication review.'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifacts', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    cases = json.loads((root / 'cases.json').read_text())['cases']
    manifest = json.loads((args.artifacts / 'manifest.json').read_text())
    for path, digest in manifest.get('fixture_sha256', {}).items():
        if hashlib.sha256((args.artifacts / path).read_bytes()).hexdigest() != digest:
            raise ValueError('fixture differs from frozen manifest')
    if hashlib.sha256((root / 'cases.json').read_bytes()).hexdigest() != manifest['rubric_sha256']:
        raise ValueError('base rubric differs from frozen manifest')
    runs = manifest['runs']
    grades = json.loads((args.artifacts / 'judge/grades.json').read_text())['runs']
    extra = args.artifacts / 'integration-manifest.json'
    if extra.exists():
        integration = json.loads(extra.read_text())
        if hashlib.sha256((root / 'integration.json').read_bytes()).hexdigest() != integration['rubric_sha256']:
            raise ValueError('integration rubric differs from frozen manifest')
        integration_dir = args.artifacts / 'delegated-coordination-1'
        for path, digest in integration['fixture_sha256'].items():
            if hashlib.sha256((integration_dir / path).read_bytes()).hexdigest() != digest:
                raise ValueError('integration fixture differs from frozen manifest')
        if hashlib.sha256((integration_dir / 'delegation.json').read_bytes()).hexdigest() != integration['delegation_sha256']:
            raise ValueError('delegation record differs from recorded hash')
        cases += json.loads((root / 'integration.json').read_text())['cases']
        runs += integration['runs']
        grades += json.loads((args.artifacts / 'judge/integration-grades.json').read_text())['runs']
    for run in runs:
        transcript = args.artifacts / run['id'] / 'transcript.json'
        if hashlib.sha256(transcript.read_bytes()).hexdigest() != run['response_sha256']:
            raise ValueError('response differs from recorded hash')
        responses = json.loads(transcript.read_text())['responses']
        if len(responses) != run['turns']:
            raise ValueError('incomplete conversation')
    result = summarize(cases, runs, grades)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Sessions: {result['sessions_passed']}/{result['sessions_total']}; "
          f"criteria: {result['criteria_passed']}/{result['criteria_total']}; "
          f"critical failures: {result['critical_failures']}")


if __name__ == '__main__':
    main()
