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
            if run['skill'] == 'architect':
                self.write_trace(run['id'])
        suite.blind(self.output)

    def write_trace(self, run_id):
        transcript = Path(self.tmp.name) / f'{run_id}.jsonl'
        calls = [{'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'architect:sample'}},
                 {'type': 'tool_use', 'name': 'Write', 'input': {'file_path': 'plan.md'}},
                 {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'cd bundle/skills; cat software-design/SKILL.md'}},
                 {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': '/b/skills/threat-modeling/SKILL.md'}}]
        transcript.write_text(json.dumps({'type': 'assistant', 'message': {'content': calls}}) + '\n')
        suite.trace(self.output, run_id, transcript)

    def add_fixture(self, immutable=True):
        case = self.root / 'evals/case-one'
        (case / 'files').mkdir()
        (case / 'files/service.py').write_text('x = 1\n')
        (case / 'case.yaml').write_text(f'schema_version: "1.1"\nname: case-one\nfixtures_immutable: {str(immutable).lower()}\n')

    def architect_run(self):
        return next(r for r in suite.load(self.output) if r['skill'] == 'architect')

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

    def test_trace_records_skills_and_write_attempts(self):
        suite.prepare(self.output)
        run_id = self.architect_run()['id']
        self.write_trace(run_id)
        data = json.loads((self.output / 'runs' / run_id / 'trace.json').read_text())
        self.assertEqual(['architect:sample'], data['skills_loaded'])
        self.assertEqual(['plan.md'], data['file_writes_attempted'])
        self.assertEqual(['software-design', 'threat-modeling'], data['skill_files_read'])

    def test_blind_requires_trace_for_agent_cases(self):
        suite.prepare(self.output)
        for run in suite.load(self.output):
            (self.output / 'runs' / run['id'] / 'answer.md').write_text('An answer.\n')
        with self.assertRaisesRegex(AssertionError, 'missing trace'):
            suite.blind(self.output)

    def test_blind_hides_trace_from_comparisons_but_not_agent_cases(self):
        self.prepare_answers()
        self.assertFalse(list((self.output / 'grading/sample').rglob('trace.json')))
        self.assertTrue(list((self.output / 'grading/architect').rglob('trace.json')))

    def test_report_rejects_changed_immutable_fixture(self):
        self.add_fixture()
        self.prepare_answers()
        self.grade()
        (self.output / 'runs' / self.architect_run()['id'] / 'service.py').write_text('x = 2\n')
        with self.assertRaisesRegex(SystemExit, 'changed: service.py'):
            suite.report(self.output)

    def test_report_rejects_added_code_in_immutable_run(self):
        self.add_fixture()
        self.prepare_answers()
        self.grade()
        (self.output / 'runs' / self.architect_run()['id'] / 'pricing.py').write_text('y = 1\n')
        with self.assertRaisesRegex(SystemExit, 'added: pricing.py'):
            suite.report(self.output)

    def test_report_allows_documents_and_caches_in_immutable_run(self):
        self.add_fixture()
        self.prepare_answers()
        self.grade()
        work = self.output / 'runs' / self.architect_run()['id']
        (work / 'plan.md').write_text('# Plan\n')
        (work / '__pycache__').mkdir()
        (work / '__pycache__/service.pyc').write_text('cache')
        suite.report(self.output)

    def test_report_allows_edits_when_fixtures_may_change(self):
        self.add_fixture(immutable=False)
        self.prepare_answers()
        self.grade()
        (self.output / 'runs' / self.architect_run()['id'] / 'service.py').write_text('x = 2\n')
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
