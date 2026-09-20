"""Tests for the live Capture & Refine adapter's envelope parsing.

The adapter's one job is transport: it turns a model's reply into a transcript
the harness can grade. It must never repair the PRD, because a repaired PRD
would make the graders test the adapter instead of the agent. These tests run
with no model call.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "scripts/agent_adapters/capture_refine_claude.py"

spec = importlib.util.spec_from_file_location("capture_refine_claude", ADAPTER)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

WELL_FORMED = """Here is my work.

===SKILLS===
capture-intake-and-gaps
- capture-grill-and-decide
===QUESTIONS===
1. Which order states stay cancellable?
- Who may cancel an order?
===PRD===
# Product behaviour agreement

- Status: `blocked`
===END===
"""


class AdapterParsingTests(unittest.TestCase):
    def test_parses_skills_questions_and_prd(self) -> None:
        parsed = adapter.parse_response(WELL_FORMED)
        self.assertEqual(
            ["capture-intake-and-gaps", "capture-grill-and-decide"], parsed["skills_opened"]
        )
        self.assertEqual(
            ["Which order states stay cancellable?", "Who may cancel an order?"],
            parsed["questions"],
        )
        self.assertEqual("# Product behaviour agreement\n\n- Status: `blocked`", parsed["prd"])

    def test_passes_a_malformed_prd_through_unrepaired(self) -> None:
        broken = WELL_FORMED.replace("- Status: `blocked`", "- Status: `totally fine`")
        parsed = adapter.parse_response(broken)
        self.assertIn("- Status: `totally fine`", parsed["prd"])

    def test_keeps_a_bundled_question_verbatim(self) -> None:
        bundled = WELL_FORMED.replace(
            "Who may cancel an order?", "Who may cancel? Which states are eligible?"
        )
        parsed = adapter.parse_response(bundled)
        self.assertIn("Who may cancel? Which states are eligible?", parsed["questions"])

    def test_strips_one_outer_code_fence_around_the_prd(self) -> None:
        fenced = WELL_FORMED.replace(
            "===PRD===\n# Product behaviour agreement",
            "===PRD===\n```markdown\n# Product behaviour agreement",
        ).replace("- Status: `blocked`\n===END===", "- Status: `blocked`\n```\n===END===")
        parsed = adapter.parse_response(fenced)
        self.assertTrue(parsed["prd"].startswith("# Product behaviour agreement"))
        self.assertNotIn("```markdown", parsed["prd"])

    def test_reads_to_end_of_text_without_an_end_marker(self) -> None:
        parsed = adapter.parse_response(WELL_FORMED.replace("===END===\n", ""))
        self.assertEqual("# Product behaviour agreement\n\n- Status: `blocked`", parsed["prd"])

    def test_a_missing_section_fails_closed(self) -> None:
        for marker in ("===PRD===", "===QUESTIONS===", "===SKILLS==="):
            with self.subTest(marker=marker):
                with self.assertRaises(ValueError) as caught:
                    adapter.parse_response(WELL_FORMED.replace(marker, "===NOPE==="))
                self.assertIn(marker, str(caught.exception))

    def test_an_empty_prd_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            adapter.parse_response(WELL_FORMED.replace("# Product behaviour agreement\n\n- Status: `blocked`\n", ""))


if __name__ == "__main__":
    unittest.main()
