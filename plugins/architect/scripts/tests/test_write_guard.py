import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parents[2] / 'hooks' / 'architect_write_guard.py'


def run_guard(tool_input, agent='architect:architect', cwd='/r'):
    event = {'tool_input': tool_input, 'cwd': cwd}
    if agent:
        event['agent_type'] = agent
    return subprocess.run([sys.executable, str(GUARD)], input=json.dumps(event), capture_output=True, text=True)


class WriteGuardTests(unittest.TestCase):
    def test_architect_cannot_write_code_or_config(self):
        for path in ['/r/src/billing.py', '/r/Dockerfile', '/r/pyproject.toml']:
            result = run_guard({'file_path': path})
            self.assertEqual(result.returncode, 2, path)
            self.assertIn('design documents', result.stderr)

    def test_architect_cannot_edit_a_notebook(self):
        self.assertEqual(run_guard({'notebook_path': '/r/a.ipynb'}).returncode, 2)

    def test_architect_can_write_design_documents(self):
        for path in ['/r/docs/adr/0003.md', '/r/flow.MMD']:
            self.assertEqual(run_guard({'file_path': path}).returncode, 0, path)

    def test_architect_can_prototype_in_a_temporary_directory(self):
        prototype = Path(tempfile.gettempdir()) / 'prototype' / 'pricing.py'
        self.assertEqual(run_guard({'file_path': str(prototype)}).returncode, 0)

    def test_temporary_directory_does_not_cover_a_project_inside_it(self):
        project = Path(tempfile.gettempdir()) / 'project'
        result = run_guard({'file_path': str(project / 'billing.py')}, cwd=str(project))
        self.assertEqual(result.returncode, 2)

    def test_other_agents_are_not_affected(self):
        for agent in ['developer:developer', None]:
            self.assertEqual(run_guard({'file_path': '/r/src/billing.py'}, agent).returncode, 0)


if __name__ == '__main__':
    unittest.main()
