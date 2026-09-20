"""Level 1 behavioural contract tests for a Capture & Refine PRD.

Each defect is produced by mutating one maintained conforming fixture, so the
fixture stays the single source of the expected shape. Every mutation asserts
that its target text existed exactly once; a mutation that no longer applies
fails loudly instead of passing silently.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check_prd_contract.py"
FIXTURE = ROOT / "tests/fixtures/prd/conforming.md"
TEMPLATE = ROOT / "agents/capture-refine/templates/capture-prd.md"

REQUIRED_SECTIONS = (
    "Evidence register",
    "Intended behaviour",
    "Assumption register",
    "Requirements",
    "Acceptance criteria",
    "Non-functional criteria",
    "Outcome contract",
    "RED list",
    "Decisions and gaps",
    "Design state",
    "Engineer completeness",
)

# (case name, exact text to replace, replacement, expected finding code)
MUTATIONS = (
    (
        "dropped_section_heading",
        "## Evidence register\n",
        "",
        "missing_section",
    ),
    (
        "invented_status_value",
        "Status: `draft_for_engineer_completeness_review`",
        "Status: `ready`",
        "invalid_status",
    ),
    (
        "requirement_without_source",
        "| DEC-1, DOM-1 |",
        "| to be confirmed |",
        "untraced_requirement",
    ),
    (
        "criterion_without_given_when_then",
        "Given an order at `fulfilment_started`, when its owner asks to cancel it, then the outcome is `too_late` and the status, version, and event count do not change.",
        "The order cannot be cancelled after fulfilment starts.",
        "unshaped_criterion",
    ),
    (
        "positive_criterion_paired_with_positive",
        "| AC-6 | returned outcomes, order version, and event count |",
        "| AC-1 | returned outcomes, order version, and event count |",
        "missing_negative_counterpart",
    ),
    (
        "requirement_names_a_technology",
        "A stale expected version is refused without any change to the order.",
        "A stale expected version is refused by a check on the new database column.",
        "implementation_leak",
    ),
    (
        "observation_point_is_internal",
        "| AC-4 | returned outcome and event count |",
        "| AC-4 | the internal state of the idempotency map |",
        "unobservable_criterion",
    ),
    (
        "assumption_without_a_class",
        "engineering_observable",
        "probably fine",
        "unclassified_assumption",
    ),
    (
        "non_functional_class_removed",
        "| auditability | One cancellation event records the actor, the order, and the time, and it is never rewritten. | 1 immutable event per cancelled order | staff engineer | behavioural_test |\n",
        "",
        "nonfunctional_gap",
    ),
    (
        "non_applicability_without_a_rationale",
        "not_applicable in this revision. The scope holds no user interface, no rendered state, and no keyboard or screen-reader surface.",
        "n/a",
        "nonfunctional_gap",
    ),
    (
        "outcome_contract_without_counter_metric",
        "- Counter-metric: duplicate cancellation events per cancelled order, target 0.\n",
        "",
        "missing_outcome_contract",
    ),
    (
        "behavioural_criterion_absent_from_red_list",
        "| AC-7 | an unknown order returns a success, so the `not_found` assertion fails |\n",
        "",
        "missing_red_entry",
    ),
    (
        "gap_without_an_owner",
        "| GAP-1 | Who executes the refund after a cancellation? | product owner | non_blocking | none yet | open, excluded from this revision |",
        "| GAP-1 | Who executes the refund after a cancellation? |  | non_blocking | none yet | open, excluded from this revision |",
        "unowned_gap",
    ),
    (
        "gap_blocking_effect_outside_the_agreed_set",
        "| GAP-1 | Who executes the refund after a cancellation? | product owner | non_blocking | none yet | open, excluded from this revision |",
        "| GAP-1 | Who executes the refund after a cancellation? | product owner | maybe later | none yet | open, excluded from this revision |",
        "invalid_blocking_effect",
    ),
    (
        "gap_owner_is_a_placeholder",
        "| GAP-1 | Who executes the refund after a cancellation? | product owner | non_blocking | none yet | open, excluded from this revision |",
        "| GAP-1 | Who executes the refund after a cancellation? | *unassigned* | non_blocking | none yet | open, excluded from this revision |",
        "unowned_gap",
    ),
    (
        "blocking_gap_left_in_a_reviewable_draft",
        "| GAP-1 | Who executes the refund after a cancellation? | product owner | non_blocking | none yet | open, excluded from this revision |",
        "| GAP-1 | Who executes the refund after a cancellation? | product owner | blocking | none yet | open, excluded from this revision |",
        "status_gap_mismatch",
    ),
    (
        "declared_column_renamed",
        "| ID | Requirement | Polarity | Given / when / then | Counterpart | Observation point | Check |",
        "| ID | Requirement | Kind | Given / when / then | Counterpart | Observation point | Check |",
        "missing_column",
    ),
    (
        "blocked_status_without_a_blocking_gap",
        "Status: `draft_for_engineer_completeness_review`",
        "Status: `blocked`",
        "status_gap_mismatch",
    ),
)


def check(path: Path, shape_only: bool = False) -> dict:
    command = ["python3", str(CHECKER), str(path), "--json"]
    if shape_only:
        command.append("--shape-only")
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if not result.stdout.strip():
        raise AssertionError(f"checker produced no report: {result.stderr}")
    report = json.loads(result.stdout)
    report["exit_code"] = result.returncode
    return report


def codes(report: dict) -> list[str]:
    return [finding["code"] for finding in report["findings"]]


class PrdContractCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conforming = FIXTURE.read_text()

    def test_conforming_prd_satisfies_the_contract(self) -> None:
        report = check(FIXTURE)
        self.assertEqual([], codes(report), report["findings"])
        self.assertEqual(0, report["exit_code"])

    def test_each_seeded_defect_produces_its_own_finding_code(self) -> None:
        for name, find, replace, expected in MUTATIONS:
            with self.subTest(case=name):
                self.assertEqual(
                    1,
                    self.conforming.count(find),
                    f"mutation {name} no longer targets exactly one place",
                )
                mutated = self.conforming.replace(find, replace)
                self.assertNotEqual(self.conforming, mutated)
                with tempfile.TemporaryDirectory() as temp:
                    path = Path(temp) / "mutated.md"
                    path.write_text(mutated)
                    report = check(path)
                self.assertIn(expected, codes(report))
                self.assertEqual(1, report["exit_code"])

    def test_every_finding_code_is_covered_by_a_mutation_or_a_shape_case(self) -> None:
        report = check(FIXTURE)
        declared = set(report["declared_codes"])
        covered = {expected for _, _, _, expected in MUTATIONS}
        # Covered by the empty-document and blank-template cases below, not by a mutation.
        covered.update({"missing_section", "empty_table"})
        self.assertEqual(
            set(),
            declared - covered,
            "a declared finding code has no negative control",
        )

    def test_a_hyphenated_blocking_effect_is_accepted(self) -> None:
        """A live model run wrote "non-blocking". The hyphen carries no meaning."""
        hyphenated = self.conforming.replace("| non_blocking |", "| non-blocking |")
        self.assertNotEqual(self.conforming, hyphenated)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "hyphenated.md"
            path.write_text(hyphenated)
            report = check(path)
        self.assertEqual([], codes(report), report["findings"])
        self.assertEqual(0, report["exit_code"])

    def test_the_eight_classes_are_maintained_in_one_place(self) -> None:
        """They were repeated in two skills, the template, and the checker.

        The checker now reads them from the template, so the skills must not
        restate the list or it will drift again.
        """
        report = check(FIXTURE)
        classes = report["nonfunctional_classes"]
        self.assertEqual(8, len(classes))
        template = TEMPLATE.read_text()
        for name in classes:
            self.assertIn(f"`{name}`", template)
        for skill in ("capture-intake-and-gaps", "capture-acceptance-contract"):
            text = (ROOT / f"agents/capture-refine/skills/{skill}/SKILL.md").read_text()
            restated = [name for name in classes if name in text]
            self.assertLessEqual(
                len(restated), 2, f"{skill} restates the class list: {restated}"
            )

    def test_an_empty_document_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty.md"
            path.write_text("# Product behaviour agreement\n")
            report = check(path)
        self.assertIn("missing_section", codes(report))
        self.assertEqual(1, report["exit_code"])

    def test_template_declares_every_required_section_and_column(self) -> None:
        report = check(TEMPLATE, shape_only=True)
        self.assertEqual([], codes(report), report["findings"])
        self.assertEqual(0, report["exit_code"])
        template = TEMPLATE.read_text()
        for section in REQUIRED_SECTIONS:
            self.assertIn(f"## {section}", template)

    def test_blank_template_body_still_fails_the_full_content_contract(self) -> None:
        report = check(TEMPLATE)
        self.assertNotEqual(0, report["exit_code"])
        self.assertIn("empty_table", codes(report))


if __name__ == "__main__":
    unittest.main()
