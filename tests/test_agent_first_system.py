from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AGENTS = {
    "capture-refine": 3,
    "design": 3,
    "planner": 4,
    "builder": 4,
    "tester": 4,
    "reviewer": 3,
    "curator": 4,
}


class AgentFirstSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "agents/manifest.json").read_text())
        cls.agents = {agent["id"]: agent for agent in cls.manifest["agents"]}

    def test_all_seven_agent_folders_own_role_skills_and_template(self) -> None:
        self.assertEqual(set(EXPECTED_AGENTS), set(self.agents))
        self.assertEqual(set(EXPECTED_AGENTS), {path.name for path in (ROOT / "agents").iterdir() if path.is_dir()})
        for agent_id, expected_skills in EXPECTED_AGENTS.items():
            agent = self.agents[agent_id]
            prefix = f"agents/{agent_id}/"
            self.assertTrue(agent["role"].startswith(prefix))
            self.assertTrue(agent["template"].startswith(prefix))
            self.assertEqual(expected_skills, len(agent["skills"]))
            self.assertTrue(all(path.startswith(prefix) for path in agent["skills"]))
            self.assertTrue((ROOT / agent["role"]).is_file())
            self.assertTrue((ROOT / agent["template"]).is_file())
            self.assertTrue(all((ROOT / path).is_file() for path in agent["skills"]))
        self.assertEqual(25, sum(len(agent["skills"]) for agent in self.agents.values()))

    def test_roles_orchestrate_every_owned_skill_and_no_router_or_workflow_exists(self) -> None:
        for agent in self.agents.values():
            role = (ROOT / agent["role"]).read_text()
            for heading in (
                "## Trigger and inputs",
                "## Orchestration",
                "## Decision gates",
                "## Handoff and return owner",
                "## Stop boundaries",
            ):
                self.assertIn(heading, role)
            for skill in agent["skills"]:
                relative = Path(skill).relative_to(Path(agent["role"]).parent)
                self.assertIn(f"]({relative})", role)
        self.assertFalse((ROOT / "agent-system").exists())
        self.assertEqual([], list((ROOT / "agents").rglob("workflow.md")))
        self.assertEqual([], [path for path in (ROOT / "agents").rglob("SKILL.md") if path.parent.name in EXPECTED_AGENTS])

    def test_readme_embedded_sources_match_canonical_files(self) -> None:
        result = subprocess.run(
            ["python3", "scripts/render_readme_agents.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        readme = (ROOT / "README.md").read_text()
        self.assertEqual(7, readme.count("Actual <code>ROLE.md</code> text"))
        self.assertEqual(25, readme.count("/SKILL.md</code> text"))

    def test_selected_prompt_contains_role_owned_skill_and_template_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "prompt.md"
            result = subprocess.run(
                [
                    "python3",
                    "scripts/render_agent_prompt.py",
                    "planner",
                    "--skill",
                    "planner-impact-and-invariants",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            rendered = output.read_text()
            self.assertIn("<!-- source: agents/planner/ROLE.md -->", rendered)
            self.assertIn("<!-- source: agents/planner/skills/planner-impact-and-invariants/SKILL.md -->", rendered)
            self.assertIn("<!-- source: agents/planner/templates/planner-handoff.md -->", rendered)
            self.assertNotIn("planner-delivery-slices/SKILL.md -->", rendered)
            self.assertNotIn("router", rendered.lower())

    def test_prompt_selection_fails_closed(self) -> None:
        cases = (
            ["python3", "scripts/render_agent_prompt.py", "capture-refine"],
            [
                "python3",
                "scripts/render_agent_prompt.py",
                "capture-refine",
                "--skill",
                "reviewer-risk-and-false-green",
            ],
            ["python3", "scripts/render_agent_prompt.py", "unknown", "--all-skills"],
        )
        for command in cases:
            with self.subTest(command=command):
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
