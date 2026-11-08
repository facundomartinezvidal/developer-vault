"""Each plugin ships two manifests; installs pick up updates only when versions match and move together."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PLUGINS = sorted(p for p in (REPO / 'plugins').iterdir() if (p / '.claude-plugin/plugin.json').is_file())


class PluginManifests(unittest.TestCase):
    def test_manifest_versions_match(self):
        for plugin in PLUGINS:
            claude = json.loads((plugin / '.claude-plugin/plugin.json').read_text())
            generic = json.loads((plugin / 'plugin.json').read_text())
            self.assertEqual(claude['version'], generic['version'], plugin.name)

    def test_every_plugin_is_in_both_marketplaces(self):
        names = {p.name for p in PLUGINS}
        claude = {p['name'] for p in json.loads((REPO / '.claude-plugin/marketplace.json').read_text())['plugins']}
        codex = {p['name'] for p in json.loads((REPO / '.agents/plugins/marketplace.json').read_text())['plugins']}
        self.assertEqual(names, claude)
        self.assertEqual(names, codex)

    def test_license_is_present(self):
        self.assertTrue((REPO / 'LICENSE').is_file())


if __name__ == '__main__':
    unittest.main()
