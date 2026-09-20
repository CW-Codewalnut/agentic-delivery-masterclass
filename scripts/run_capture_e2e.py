#!/usr/bin/env python3
"""Grade Capture & Refine behaviour end to end, from a vague request to a PRD.

The harness never decides the outcome itself. It reads what the agent produced
and applies deterministic graders. No model judges the result, so a pass means
the artefact satisfied a stated rule, not that a grader liked it.

Execution sources, one of which is required:
  --transcript-dir DIR   grade transcripts recorded earlier
  --agent-command CMD    run CMD once per case; the case JSON arrives on stdin
                         and the transcript JSON must return on stdout

With neither source the harness refuses to report a result.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check_prd_contract.py"
MANIFEST = ROOT / "agents/manifest.json"

DECLARED_GRADERS = (
    "prd_contract",
    "prd_status",
    "one_question_at_a_time",
    "enough_questions",
    "does_not_decide_unowned_policy",
    "required_gap_topics",
    "design_state",
    "no_forbidden_claim",
    "authority_boundary",
    "first_skill",
    "declared_skills",
)
AUTHORITY_SENTENCE = "completeness is not product approval"


def owned_skills(agent_id: str) -> set[str]:
    manifest = json.loads(MANIFEST.read_text())
    for agent in manifest["agents"]:
        if agent["id"] == agent_id:
            return {Path(path).parent.name for path in agent["skills"]}
    raise SystemExit(f"unknown agent {agent_id}")


def section(prd: str, heading: str) -> str:
    """Return one '## heading' block, so a grader never matches the wrong place."""
    lines = prd.splitlines()
    collected: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            inside = line[3:].strip() == heading
            continue
        if inside:
            collected.append(line)
    return "\n".join(collected)


def status_of(prd: str) -> str:
    for line in prd.splitlines():
        if line.strip().startswith("- Status:"):
            return line.split(":", 1)[1].strip().strip("`")
    return ""


def contract_findings(prd: str, work: Path) -> list[dict]:
    work.mkdir(parents=True, exist_ok=True)
    path = work / "graded.md"
    path.write_text(prd)
    result = subprocess.run(
        ["python3", str(CHECKER), str(path), "--json"], cwd=ROOT, capture_output=True, text=True
    )
    if not result.stdout.strip():
        raise SystemExit(f"contract checker produced no report: {result.stderr}")
    return json.loads(result.stdout)["findings"]


def grade(case: dict, transcript: dict, work: Path) -> dict[str, dict]:
    expect = case["expect"]
    prd = transcript["prd"]
    questions = transcript.get("questions", [])
    skills = transcript.get("skills_opened", [])
    results: dict[str, dict] = {}

    def record(name: str, passed: bool, detail: str) -> None:
        results[name] = {"passed": bool(passed), "detail": detail}

    findings = contract_findings(prd, work)
    wanted_pass = expect.get("prd_contract", "pass") == "pass"
    record(
        "prd_contract",
        (not findings) == wanted_pass,
        f"{len(findings)} findings: " + ", ".join(sorted({f['code'] for f in findings})),
    )

    actual_status = status_of(prd)
    record(
        "prd_status",
        actual_status == expect["prd_status"],
        f"status is {actual_status!r}, the case expects {expect['prd_status']!r}",
    )

    bundled = [q for q in questions if q.count("?") != 1]
    record(
        "one_question_at_a_time",
        not bundled,
        f"{len(bundled)} question(s) carry more or fewer than one question mark",
    )

    minimum = expect.get("min_questions", 1)
    record(
        "enough_questions",
        len(questions) >= minimum,
        f"asked {len(questions)}, the case expects at least {minimum}",
    )

    requirements = section(prd, "Requirements").lower()
    decided = [topic for topic in expect.get("must_not_decide", []) if topic.lower() in requirements]
    record(
        "does_not_decide_unowned_policy",
        not decided,
        "decided as a requirement: " + ", ".join(decided) if decided else "no unowned policy was decided",
    )

    gaps = section(prd, "Decisions and gaps").lower()
    absent = [topic for topic in expect.get("required_gap_topics", []) if topic.lower() not in gaps]
    record(
        "required_gap_topics",
        not absent,
        "absent from the gap table: " + ", ".join(absent) if absent else "every required topic is a visible gap",
    )

    design = section(prd, "Design state")
    allowed = expect.get("design_state_in", [])
    stated = re.findall(r"`([a-z_]+)`", design)
    record(
        "design_state",
        bool(stated) and stated[0] in allowed,
        f"design state is {stated[:1]}, the case allows {allowed}",
    )

    lowered = prd.lower()
    claimed = [claim for claim in expect.get("forbidden_claims", []) if claim.lower() in lowered]
    record(
        "no_forbidden_claim",
        not claimed,
        "claimed: " + ", ".join(claimed) if claimed else "no authority claim beyond the role",
    )

    record(
        "authority_boundary",
        AUTHORITY_SENTENCE in lowered,
        "the PRD must still say completeness is not Product approval",
    )

    expected_first = expect.get("first_skill")
    record(
        "first_skill",
        bool(skills) and skills[0] == expected_first,
        f"opened {skills[:1]} first, the case expects {expected_first!r}",
    )

    owned = owned_skills(case.get("agent", transcript.get("agent", "capture-refine")))
    foreign = [skill for skill in skills if skill not in owned]
    record(
        "declared_skills",
        not foreign,
        "not owned by this agent: " + ", ".join(foreign) if foreign else "every opened skill is agent-owned",
    )
    return results


def load_transcript(case: dict, args: argparse.Namespace) -> dict:
    if args.agent_command:
        result = subprocess.run(
            shlex.split(args.agent_command),
            input=json.dumps(case),
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode or not result.stdout.strip():
            raise SystemExit(f"{case['id']}: agent command produced no transcript: {result.stderr}")
        transcript = json.loads(result.stdout)
    else:
        path = args.transcript_dir / f"{case['id']}.json"
        if not path.is_file():
            raise SystemExit(f"{case['id']}: no transcript at {path}")
        transcript = json.loads(path.read_text())
    if "prd" not in transcript:
        if "prd_path" not in transcript:
            raise SystemExit(f"{case['id']}: transcript carries neither prd nor prd_path")
        transcript["prd"] = (ROOT / transcript["prd_path"]).read_text()
    return transcript


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "tests/e2e/capture-refine/cases")
    parser.add_argument("--transcript-dir", type=Path)
    parser.add_argument("--agent-command")
    parser.add_argument("--case", action="append", help="grade only these case ids")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.transcript_dir and not args.agent_command:
        print(
            "refusing to report a result: no execution source. "
            "Pass --transcript-dir or --agent-command.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if args.transcript_dir and args.agent_command:
        raise SystemExit("choose one execution source, not both")

    cases = [json.loads(path.read_text()) for path in sorted(args.cases.glob("*.json"))]
    if args.case:
        cases = [case for case in cases if case["id"] in set(args.case)]
    if not cases:
        raise SystemExit("no cases selected")

    # Scratch state stays outside the working tree. An agent command runs
    # arbitrary code in the repository, and `git add -A` would pick it up.
    results = []
    failed = 0
    with tempfile.TemporaryDirectory(prefix="capture-e2e-") as work_dir:
        work = Path(work_dir)
        for case in cases:
            transcript = load_transcript(case, args)
            graders = grade(case, transcript, work)
            case_failed = [name for name, check in graders.items() if not check["passed"]]
            failed += bool(case_failed)
            results.append(
                {
                    "case": case["id"],
                    "request": case["request"],
                    "passed": not case_failed,
                    "failed_graders": case_failed,
                    "graders": graders,
                }
            )

    report = {
        "classification": "graded agent output; every grader is deterministic, no model judges the result",
        "agent_execution": bool(args.agent_command),
        "execution_source": "agent_command" if args.agent_command else "recorded_transcript",
        "command": args.agent_command or "",
        "judge_model": "none",
        "declared_graders": list(DECLARED_GRADERS),
        "summary": {"cases": len(results), "passed": len(results) - failed, "failed": failed},
        "results": results,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(json.dumps(report["summary"], sort_keys=True))
        for case in results:
            for name in case["failed_graders"]:
                print(f"FAIL\t{case['case']}\t{name}\t{case['graders'][name]['detail']}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
