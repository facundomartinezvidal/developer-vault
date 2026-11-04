"""Checks for isolation and fail-closed evaluation accounting, not model wording."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('eval_suite', Path(__file__).parents[1] / 'eval_suite.py')
suite = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(suite)


class EvaluationAccounting(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'plugin'
        self.output = Path(self.tmp.name) / 'evaluation'
        for name in ['sample', 'architect']:
            folder = self.root / 'skills' / name
            folder.mkdir(parents=True)
            (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Test interface reviews.\n---\n\nUse evidence.\n')
            case_root = self.root / ('evals' if name == 'architect' else f'skills/{name}/evals')
            case = case_root / 'case-one'
            (case / 'graders').mkdir(parents=True)
            (case / 'case.yaml').write_text('schema_version: "1.1"\nname: case-one\n')
            (case / 'prompt.md').write_text('---\ntags: []\n---\nReview this.\n')
            (case / 'graders/01-critical.md').write_text('---\ntype: llm\nweight: 1\n---\nCRITICAL: Preserve the stated guarantee.\n')
        self.patch_root = patch.object(suite, 'ROOT', self.root)
        self.patch_specialists = patch.object(suite, 'SPECIALISTS', ['sample'])
        self.patch_root.start()
        self.patch_specialists.start()
        self.addCleanup(self.patch_root.stop)
        self.addCleanup(self.patch_specialists.stop)

    def prepare_answers(self):
        suite.prepare(self.output)
        for run in suite.load(self.output):
            (self.output / 'runs' / run['id'] / 'answer.md').write_text('An answer.\n')
        suite.blind(self.output)

    def grade(self, passed=True):
        mapping = json.loads((self.output / 'mapping.json').read_text())
        for skill in ['sample', 'architect']:
            labels = mapping[f'{skill}/case-one']
            data = {'cases': {'case-one': {label: {'total': int(passed), 'results': [{'criterion': '01-critical', 'pass': passed, 'reason': 'The guarantee is addressed.'}]} for label in labels}}}
            (self.output / 'grading' / skill / 'grades.json').write_text(json.dumps(data))

    def test_context_excludes_criteria_and_original_cases_survive(self):
        suite.prepare(self.output)
        self.assertFalse(list((self.output / 'contexts').rglob('graders')))
        self.assertFalse(list((self.output / 'contexts').rglob('evals')))
        self.assertTrue((self.root / 'skills/sample/evals/case-one/graders/01-critical.md').exists())
        baseline = suite.load(self.output)[0]
        self.assertIsNone(baseline['context'])

    def test_blind_rejects_missing_response(self):
        suite.prepare(self.output)
        with self.assertRaisesRegex(AssertionError, 'missing answer'):
            suite.blind(self.output)
        self.assertFalse((self.output / 'grading').exists())

    def test_report_rejects_critical_failure(self):
        self.prepare_answers()
        self.grade(False)
        with self.assertRaisesRegex(SystemExit, 'Critical'):
            suite.report(self.output)
        data = json.loads((self.output / 'summary.json').read_text())
        self.assertFalse(data['all_with_skill_critical_pass'])

    def test_report_rejects_incomplete_criteria(self):
        self.prepare_answers()
        self.grade()
        path = self.output / 'grading/sample/grades.json'
        data = json.loads(path.read_text())
        data['cases']['case-one']['A']['results'] = []
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(AssertionError, 'criteria'):
            suite.report(self.output)

    def test_report_rejects_missing_run_coverage(self):
        self.prepare_answers()
        self.grade()
        path = self.output / 'mapping.json'
        mapping = json.loads(path.read_text())
        del mapping['architect/case-one']
        path.write_text(json.dumps(mapping))
        with self.assertRaisesRegex(AssertionError, 'coverage'):
            suite.report(self.output)

    def test_report_rejects_changed_request(self):
        self.prepare_answers()
        self.grade()
        (self.output / 'runs/001/request.txt').write_text('A different request')
        with self.assertRaisesRegex(AssertionError, 'request changed'):
            suite.report(self.output)

    def test_report_accepts_complete_evidence(self):
        self.prepare_answers()
        self.grade()
        suite.report(self.output)
        data = json.loads((self.output / 'summary.json').read_text())
        self.assertEqual(3, len(data['runs']))
        self.assertTrue(data['all_with_skill_critical_pass'])


if __name__ == '__main__':
    unittest.main()
