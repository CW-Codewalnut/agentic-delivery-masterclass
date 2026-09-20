"""Tests for the shared skills tier.

A shared skill is opened by two or more agents. A vendored one is a verbatim
third-party copy, so these tests check provenance and integrity rather than the
house shape: editing a vendored file to fit this repository's style would end
the claim that it is verbatim, which is the only claim that makes the copy
auditable.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "agents/manifest.json").read_text())
SHARED = MANIFEST["shared_skills"]
AGENT_IDS = {agent["id"] for agent in MANIFEST["agents"]}
RENDERER = "scripts/render_agent_prompt.py"


class SharedSkillTierTests(unittest.TestCase):
    def test_every_shared_skill_is_declared_and_present(self) -> None:
        self.assertTrue(SHARED, "the tier must declare at least one shared skill")
        names = [entry["name"] for entry in SHARED]
        self.assertEqual(len(names), len(set(names)), "shared skill names must be unique")
        for entry in SHARED:
            path = ROOT / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            self.assertTrue(entry["path"].startswith("shared/skills/"))
            self.assertEqual(entry["name"], path.parent.name)

    def test_a_shared_skill_serves_at_least_two_real_agents(self) -> None:
        """One agent means it belongs in that agent's own folder, not here."""
        for entry in SHARED:
            with self.subTest(skill=entry["name"]):
                agents = entry["agents"]
                self.assertGreaterEqual(len(agents), 2, "one agent means agent-owned")
                self.assertEqual(len(agents), len(set(agents)))
                self.assertEqual(set(), set(agents) - AGENT_IDS, "unknown agent id")

    def test_a_vendored_copy_records_its_provenance(self) -> None:
        for entry in SHARED:
            if not entry.get("verbatim"):
                continue
            with self.subTest(skill=entry["name"]):
                provenance = entry["provenance"]
                for key in ("source", "repository", "commit", "licence", "licence_file", "sha256"):
                    self.assertTrue(provenance.get(key), f"{key} is required")
                self.assertRegex(provenance["commit"], r"^[0-9a-f]{40}$")
                self.assertIn(provenance["commit"], provenance["source"])
                self.assertTrue((ROOT / provenance["licence_file"]).is_file())

    def test_a_vendored_copy_still_matches_its_recorded_hash(self) -> None:
        """Any hand edit to a vendored file fails here. Re-pin upstream instead."""
        for entry in SHARED:
            if not entry.get("verbatim"):
                continue
            with self.subTest(skill=entry["name"]):
                digest = hashlib.sha256((ROOT / entry["path"]).read_bytes()).hexdigest()
                self.assertEqual(entry["provenance"]["sha256"], digest)

    def test_the_retained_licence_carries_its_notice(self) -> None:
        licence = (ROOT / "shared/LICENSE-mattpocock-skills").read_text()
        self.assertIn("MIT License", licence)
        self.assertIn("Copyright (c)", licence)
        self.assertIn("The above copyright notice and this permission notice", licence)

    def test_the_attribution_states_the_copy_is_verbatim(self) -> None:
        text = (ROOT / "shared/ATTRIBUTION.md").read_text()
        self.assertIn("verbatim", text)
        self.assertIn("have not reviewed or endorsed", text)
        for entry in SHARED:
            if entry.get("verbatim"):
                self.assertIn(entry["provenance"]["commit"][:8], text)

    def test_the_research_note_no_longer_claims_nothing_was_copied(self) -> None:
        """The note said no source prose was copied. Two files now are copies."""
        text = (ROOT / "docs/research/matt-pocock-skills.md").read_text()
        self.assertNotIn("do not copy source prose", text)
        self.assertIn("shared/ATTRIBUTION.md", text)

    def test_each_using_role_orchestrates_the_shared_skill(self) -> None:
        agents = {agent["id"]: agent for agent in MANIFEST["agents"]}
        for entry in SHARED:
            for agent_id in entry["agents"]:
                with self.subTest(skill=entry["name"], agent=agent_id):
                    role = (ROOT / agents[agent_id]["role"]).read_text()
                    self.assertIn(f"shared/skills/{entry['name']}/SKILL.md", role)

    def test_a_vendored_skill_is_not_held_to_the_house_shape(self) -> None:
        """Documents the deliberate asymmetry, so nobody 'fixes' it later."""
        for entry in SHARED:
            if not entry.get("verbatim"):
                continue
            text = (ROOT / entry["path"]).read_text()
            self.assertFalse(text.startswith("---\nname: %s\ndescription: Use when " % entry["name"]))

    def test_renderer_includes_a_shared_skill_only_for_a_permitted_agent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "prompt.md"
            result = subprocess.run(
                ["python3", RENDERER, "tester", "--skill", "tester-adversarial-behaviour",
                 "--shared-skill", "tdd", "--output", str(output)],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            rendered = output.read_text()
            self.assertIn("<!-- source: shared/skills/tdd/SKILL.md -->", rendered)
            self.assertIn("shared/LICENSE-mattpocock-skills", rendered)

    def test_renderer_refuses_a_shared_skill_the_agent_does_not_use(self) -> None:
        cases = (
            ["python3", RENDERER, "design", "--skill", "design-input-readiness",
             "--shared-skill", "tdd"],
            ["python3", RENDERER, "tester", "--skill", "tester-adversarial-behaviour",
             "--shared-skill", "not-a-shared-skill"],
        )
        for command in cases:
            with self.subTest(command=command[-1]):
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
