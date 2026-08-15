from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "delta-bags"
SKILL_FILE = SKILL_DIR / "SKILL.md"


class SkillStructureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contents = SKILL_FILE.read_text(encoding="utf-8")

    def test_frontmatter_is_portable_and_named_for_directory(self) -> None:
        parts = self.contents.split("---", 2)
        self.assertEqual(parts[0], "")
        self.assertEqual(len(parts), 3)
        fields = {
            line.split(":", 1)[0]: line.split(":", 1)[1].strip()
            for line in parts[1].splitlines()
            if ":" in line
        }
        self.assertEqual(set(fields), {"name", "description", "license"})
        self.assertEqual(fields["name"], SKILL_DIR.name)
        self.assertIn("Delta Air Lines", fields["description"])
        self.assertEqual(fields["license"], "MIT")

    def test_skill_has_no_scaffold_markers(self) -> None:
        self.assertNotIn("TODO", self.contents)
        self.assertLess(len(self.contents.splitlines()), 500)

    def test_relative_markdown_links_exist(self) -> None:
        links = re.findall(r"\[[^]]+\]\(([^)]+)\)", self.contents)
        local_links = [link for link in links if "://" not in link and not link.startswith("#")]
        self.assertTrue(local_links)
        for link in local_links:
            with self.subTest(link=link):
                self.assertTrue((SKILL_DIR / link).is_file())

    def test_openai_metadata_mentions_skill(self) -> None:
        metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Delta Bags"', metadata)
        self.assertIn("$delta-bags", metadata)

    def test_distribution_manifests_share_identity_and_version(self) -> None:
        claude_manifest = json.loads(
            (REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        claude_marketplace = json.loads(
            (REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        codex_manifest = json.loads(
            (REPO_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

        for manifest in (claude_manifest, codex_manifest):
            self.assertEqual(manifest["name"], SKILL_DIR.name)
            self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
            self.assertEqual(
                manifest["repository"],
                "https://github.com/thisiszinger/delta-bags-skill",
            )

        self.assertEqual(claude_manifest["version"], codex_manifest["version"])
        self.assertEqual(codex_manifest["skills"], "./skills/")
        self.assertTrue((REPO_ROOT / codex_manifest["skills"]).is_dir())

        self.assertEqual(claude_marketplace["name"], "delta-bags-skill")
        self.assertEqual(len(claude_marketplace["plugins"]), 1)
        marketplace_plugin = claude_marketplace["plugins"][0]
        self.assertEqual(marketplace_plugin["name"], claude_manifest["name"])
        self.assertEqual(marketplace_plugin["version"], claude_manifest["version"])
        self.assertEqual(marketplace_plugin["source"], "./")


if __name__ == "__main__":
    unittest.main()
