import importlib.util
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('shared_guidance', ROOT / 'scripts/shared_guidance.py')
guidance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guidance)


class SharedGuidanceTest(unittest.TestCase):
    def test_each_plugin_packages_complete_guidance_without_other_plugin(self):
        for role, (_, names) in guidance.SHARED.items():
            outputs = guidance.shared_outputs(role)
            with tempfile.TemporaryDirectory() as folder:
                isolated = Path(folder)
                for name, content in outputs.items():
                    target = isolated / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(content)
                self.assertFalse(any('evals' in Path(name).parts for name in outputs))
                for name in names:
                    source = isolated / 'skills' / role / 'references/shared' / name / 'SKILL.md'
                    self.assertTrue(source.is_file())
                    for ref in set(re.findall(r'(?:references|assets)/[\w./-]+\.\w+', source.read_text())):
                        self.assertTrue((source.parent / ref).is_file(), (role, name, ref))

    def test_build_checks_detect_changed_owning_source(self):
        # A minimal repository exercises the real generator/check path, not word matching.
        import shutil
        with tempfile.TemporaryDirectory() as folder:
            isolated = Path(folder)
            for name in ('scripts/shared_guidance.py', 'shared/decision-protocol.md',
                         'plugins/architect/scripts/build_agents.py', 'plugins/architect/src/architect.md'):
                target = isolated / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            for name in guidance.SHARED['architect'][1]:
                target = isolated / 'plugins/developer/skills' / name / 'SKILL.md'
                target.parent.mkdir(parents=True)
                target.write_text('Original guidance\n')
            script = isolated / 'plugins/architect/scripts/build_agents.py'
            subprocess.run(['python3', str(script)], check=True, capture_output=True)
            subprocess.run(['python3', str(script), '--check'], check=True, capture_output=True)
            source = isolated / 'plugins/developer/skills/design-patterns/SKILL.md'
            source.write_text('Changed guidance\n')
            result = subprocess.run(['python3', str(script), '--check'], capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('design-patterns/SKILL.md', result.stderr)

    def test_all_client_formats_embed_same_protocol_and_valid_codex_toml(self):
        import tomllib
        protocol = (ROOT / 'shared/decision-protocol.md').read_text().strip()
        for role in guidance.SHARED:
            plugin = ROOT / 'plugins' / role
            for path in (plugin / f'agents/{role}.md',
                         plugin / f'com.github.copilot/agents/{role}.agent.md',
                         plugin / f'skills/{role}/SKILL.md'):
                self.assertEqual(1, path.read_text().count(protocol))
                self.assertNotIn(guidance.TOKEN, path.read_text())
            data = tomllib.loads((plugin / f'com.openai.codex/agents/{role}.toml').read_text())
            self.assertEqual(1, data['developer_instructions'].count(protocol))

    def test_rejects_unknown_leftover_reference_files(self):
        with tempfile.TemporaryDirectory() as folder:
            plugin = Path(folder) / 'architect'
            stray = plugin / 'skills/architect/references/shared/old/SKILL.md'
            stray.parent.mkdir(parents=True)
            stray.write_text('Obsolete\n')
            self.assertEqual(['skills/architect/references/shared/old/SKILL.md'],
                             guidance.unexpected_shared_files(plugin, {}))


if __name__ == '__main__':
    unittest.main()
