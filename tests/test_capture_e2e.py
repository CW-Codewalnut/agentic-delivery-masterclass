"""Level 2 behavioural end-to-end tests for the Capture & Refine agent.

The harness grades what the agent produced, not what a helper script decided.
Every grader is deterministic: no model judges the result. The fast suite proves
the graders by seeding one defect at a time into a recorded transcript, so a
grader that stopped working fails here instead of passing a real run.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_capture_e2e.py"
CASES = ROOT / "tests/e2e/capture-refine/cases"
RECORDED = ROOT / "tests/e2e/capture-refine/recorded"
STUB = ROOT / "tests/e2e/capture-refine/stub_agent.py"
REFINE = "refine-cancellation-window"


def run(*args: str) -> dict:
    result = subprocess.run(
        ["python3", str(RUNNER), *args, "--json"], cwd=ROOT, capture_output=True, text=True
    )
    payload = {"exit_code": result.returncode, "stderr": result.stderr, "stdout": result.stdout}
    if result.stdout.strip():
        try:
            payload["report"] = json.loads(result.stdout)
        except json.JSONDecodeError:
            payload["report"] = None
    return payload


def failed_graders(report: dict, case_id: str) -> list[str]:
    for case in report["results"]:
        if case["case"] == case_id:
            return [name for name, check in case["graders"].items() if not check["passed"]]
    raise AssertionError(f"case {case_id} absent from the report")


# Each mutation seeds one defect. (name, mutate, expected failing grader)
def bundled_questions(transcript: dict, prd: str) -> tuple[dict, str | None]:
    transcript["questions"][0] = "Who may cancel? Which states stay cancellable?"
    return transcript, None


def too_few_questions(transcript: dict, prd: str) -> tuple[dict, str | None]:
    transcript["questions"] = transcript["questions"][:1]
    return transcript, None


def wrong_first_skill(transcript: dict, prd: str) -> tuple[dict, str | None]:
    transcript["skills_opened"].insert(0, "capture-prd-handoff")
    return transcript, None


def undeclared_skill(transcript: dict, prd: str) -> tuple[dict, str | None]:
    transcript["skills_opened"].append("capture-architecture-choice")
    return transcript, None


def wrong_status(transcript: dict, prd: str) -> tuple[dict, str | None]:
    return transcript, prd.replace(
        "Status: `draft_for_engineer_completeness_review`", "Status: `blocked`"
    )


def forbidden_claim(transcript: dict, prd: str) -> tuple[dict, str | None]:
    return transcript, prd + "\nThis revision is ready to build.\n"


def overstates_design_state(transcript: dict, prd: str) -> tuple[dict, str | None]:
    return transcript, prd.replace("`not_required`; the revision holds", "`aligned`; the revision holds")


def drops_the_authority_boundary(transcript: dict, prd: str) -> tuple[dict, str | None]:
    return transcript, prd.replace(" Completeness is not Product approval.", "")


def breaks_the_prd_contract(transcript: dict, prd: str) -> tuple[dict, str | None]:
    row = "| AC-7 | an unknown order returns a success, so the `not_found` assertion fails |\n"
    return transcript, prd.replace(row, "")


MUTATIONS = (
    ("bundled_two_questions_into_one", bundled_questions, "one_question_at_a_time"),
    ("asked_almost_nothing", too_few_questions, "enough_questions"),
    ("drafted_before_intake", wrong_first_skill, "first_skill"),
    ("opened_a_skill_it_does_not_own", undeclared_skill, "declared_skills"),
    ("reported_the_wrong_status", wrong_status, "prd_status"),
    ("claimed_the_work_is_ready", forbidden_claim, "no_forbidden_claim"),
    ("overstated_the_design_state", overstates_design_state, "design_state"),
    ("dropped_the_authority_boundary", drops_the_authority_boundary, "authority_boundary"),
    ("broke_the_prd_contract", breaks_the_prd_contract, "prd_contract"),
)


class CaptureEndToEndTests(unittest.TestCase):
    def test_runner_fails_closed_without_an_execution_source(self) -> None:
        outcome = run("--cases", str(CASES))
        self.assertNotEqual(0, outcome["exit_code"])
        self.assertIn("execution source", (outcome["stderr"] + outcome["stdout"]).lower())

    def test_recorded_transcripts_pass_every_grader(self) -> None:
        outcome = run("--cases", str(CASES), "--transcript-dir", str(RECORDED))
        self.assertEqual(0, outcome["exit_code"], outcome["stdout"] + outcome["stderr"])
        report = outcome["report"]
        self.assertEqual(2, report["summary"]["cases"])
        self.assertEqual(0, report["summary"]["failed"])
        for case in report["results"]:
            for name, check in case["graders"].items():
                self.assertTrue(check["passed"], f"{case['case']}/{name}: {check['detail']}")

    def test_recorded_run_records_an_honest_classification(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "results.json"
            outcome = run(
                "--cases", str(CASES),
                "--transcript-dir", str(RECORDED),
                "--output", str(output),
            )
            self.assertEqual(0, outcome["exit_code"])
            report = json.loads(output.read_text())
        self.assertFalse(report["agent_execution"])
        self.assertEqual("recorded_transcript", report["execution_source"])
        self.assertEqual("none", report["judge_model"])
        self.assertIn("deterministic", report["classification"])

    def test_agent_command_path_is_wired_and_labelled(self) -> None:
        outcome = run(
            "--cases", str(CASES),
            "--agent-command", f"python3 {STUB}",
        )
        self.assertEqual(0, outcome["exit_code"], outcome["stdout"] + outcome["stderr"])
        report = outcome["report"]
        self.assertTrue(report["agent_execution"])
        self.assertEqual("agent_command", report["execution_source"])
        self.assertIn("stub_agent.py", report["command"])
        self.assertEqual("none", report["judge_model"])

    def test_each_seeded_transcript_defect_fails_its_own_grader(self) -> None:
        recorded = json.loads((RECORDED / f"{REFINE}.json").read_text())
        source_prd = (ROOT / recorded["prd_path"]).read_text()
        for name, mutate, expected in MUTATIONS:
            with self.subTest(case=name):
                transcript, prd = mutate(json.loads(json.dumps(recorded)), source_prd)
                if prd is not None:
                    self.assertNotEqual(source_prd, prd, f"mutation {name} changed nothing")
                    transcript.pop("prd_path", None)
                    transcript["prd"] = prd
                else:
                    self.assertNotEqual(recorded, transcript, f"mutation {name} changed nothing")
                with tempfile.TemporaryDirectory() as temp:
                    directory = Path(temp) / "transcripts"
                    directory.mkdir()
                    for path in RECORDED.glob("*.json"):
                        shutil.copy(path, directory / path.name)
                    (directory / f"{REFINE}.json").write_text(json.dumps(transcript, indent=2))
                    outcome = run(
                        "--cases", str(CASES),
                        "--transcript-dir", str(directory),
                        "--case", REFINE,
                    )
                self.assertNotEqual(0, outcome["exit_code"], f"{name} was not caught")
                self.assertIn(expected, failed_graders(outcome["report"], REFINE))

    def test_every_declared_grader_has_a_negative_control(self) -> None:
        outcome = run("--cases", str(CASES), "--transcript-dir", str(RECORDED))
        declared = set(outcome["report"]["declared_graders"])
        covered = {expected for _, _, expected in MUTATIONS}
        self.assertEqual(set(), declared - covered, "a declared grader has no negative control")

    def test_harness_creates_no_scratch_path_inside_the_repository(self) -> None:
        """A live run deleted the harness's in-repo scratch directory mid-run.

        Scratch state belongs outside the working tree: an agent command runs
        arbitrary code in the repository, and `git add -A` would pick the
        directory up.
        """
        with tempfile.TemporaryDirectory() as temp:
            probe = Path(temp) / "probe.json"
            outcome = run(
                "--cases", str(CASES),
                "--case", REFINE,
                "--agent-command", f"python3 {STUB} --probe {probe}",
            )
            self.assertEqual(0, outcome["exit_code"], outcome["stdout"] + outcome["stderr"])
            self.assertEqual([], json.loads(probe.read_text()))

    def test_a_missing_transcript_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            outcome = run("--cases", str(CASES), "--transcript-dir", temp)
        self.assertNotEqual(0, outcome["exit_code"])


if __name__ == "__main__":
    unittest.main()
