from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLE_FILES = [
    "01-capture-refine.md",
    "02-design.md",
    "03-planner.md",
    "04-builder.md",
    "05-tester.md",
    "06-reviewer.md",
    "07-curator.md",
]
SKILLS = ["capture-refine", "design", "planner", "builder", "tester", "reviewer", "curator"]
PUBLIC_DIRS = [
    ROOT / "roles",
    ROOT / "skills",
    ROOT / "domain",
    ROOT / "worked-example",
    ROOT / "docs",
    ROOT / "tests",
]
PUBLIC_FILES = [ROOT / "README.md"]


class ContentContractTests(unittest.TestCase):
    def test_all_roles_exist_in_required_order_and_define_contract(self) -> None:
        self.assertEqual(ROLE_FILES, [path.name for path in sorted((ROOT / "roles").glob("*.md"))])
        for filename in ROLE_FILES:
            text = (ROOT / "roles" / filename).read_text()
            for section in ("## Mission", "## Starts with", "## Produces", "## Ownership and status", "## Stop gates"):
                self.assertIn(section, text, f"{filename} missing {section}")

    def test_each_role_has_a_substantive_separate_skill(self) -> None:
        for skill in SKILLS:
            path = ROOT / "skills" / skill / "SKILL.md"
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))
            text = path.read_text()
            for section in ("## Inputs", "## Steps", "## Outputs", "## Stop gates", "## Example"):
                self.assertIn(section, text, f"{skill} missing {section}")
            self.assertGreaterEqual(len(text.splitlines()), 25)

    def test_domain_policy_is_separate_from_skills(self) -> None:
        domain = (ROOT / "domain" / "order-cancellation.md").read_text()
        self.assertIn("## Lifecycle policy", domain)
        self.assertIn("## Atomicity caveat", domain)
        generic_capture_skill = (ROOT / "skills" / "capture-refine" / "SKILL.md").read_text()
        self.assertNotIn("Only the owning customer", generic_capture_skill)

    def test_public_material_has_no_private_or_absolute_path_markers(self) -> None:
        forbidden = (
            "/" + "Users" + "/",
            "Sa" + "bre",
            "sa" + "bre",
            "Code" + "walnut",
        )
        paths = list(PUBLIC_FILES)
        for directory in PUBLIC_DIRS:
            paths.extend(path for path in directory.rglob("*") if path.is_file())
        for path in paths:
            if path.suffix in {".md", ".py", ".txt"}:
                text = path.read_text()
                for marker in forbidden:
                    self.assertNotIn(marker, text, f"{marker!r} found in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    unittest.main()
