#!/usr/bin/env python3
"""Run the real Capture & Refine agent through the Claude Code CLI.

This is an --agent-command adapter for scripts/run_capture_e2e.py. It reads one
case on stdin, renders the agent's own prompt from ROLE.md and its owned skills,
gives the model the evidence the case names, and returns the transcript.

The adapter handles transport only. It never repairs the PRD, never rewrites a
question, and never supplies a section the model left out. A repaired artefact
would make the graders test this file instead of the agent, so a missing or
empty section fails closed.

Usage:
  python3 scripts/run_capture_e2e.py \
    --agent-command "python3 scripts/agent_adapters/capture_refine_claude.py --model haiku"
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RENDERER = ROOT / "scripts/render_agent_prompt.py"
MARKERS = ("===SKILLS===", "===QUESTIONS===", "===PRD===")
BULLET = re.compile(r"^\s*(?:[-*]|\d+[.)])\s*")

TASK = """
===TASK===

You are the Capture & Refine agent above. Follow the orchestration order in
ROLE.md, apply the owned skills, and produce the output shape in
templates/capture-prd.md.

No human is available in this run. You cannot ask a question and wait. Record
the questions you would ask, in the order you would ask them, and then write
the PRD from the evidence you were given plus the gaps that remain open.

Rules you must keep:
- Use the template's exact section headings and exact table column names.
- One question per line. Exactly one question mark per line. Never bundle two.
- An owned Product decision with no named owner stays an open gap. Do not decide it.
- A blocking gap holds the status at `blocked`.
- Name no technology, schema, or algorithm in a requirement or a criterion.

Reply in exactly this envelope and nothing else after it:

===SKILLS===
<one owned skill name per line, in the order you opened them>
===QUESTIONS===
<one question per line>
===PRD===
<the complete PRD markdown>
===END===
"""


def parse_response(text: str) -> dict:
    """Split the model's reply into a transcript. Transport only, no repair."""
    for marker in MARKERS:
        if marker not in text:
            raise ValueError(f"model reply is missing {marker}")
    _, remainder = text.split(MARKERS[0], 1)
    skills_block, remainder = remainder.split(MARKERS[1], 1)
    questions_block, prd_block = remainder.split(MARKERS[2], 1)
    prd_block = prd_block.split("===END===", 1)[0]

    def listed(block: str) -> list[str]:
        lines = [BULLET.sub("", line).strip().strip("`") for line in block.splitlines()]
        return [line for line in lines if line]

    prd = prd_block.strip("\n")
    lines = prd.splitlines()
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
        while lines and not lines[-1].strip():
            lines.pop()
        if lines and lines[-1].strip() == "```":
            lines.pop()
        prd = "\n".join(lines)
    prd = prd.strip("\n")
    if not prd.strip():
        raise ValueError("model reply carried an empty PRD")
    return {
        "skills_opened": listed(skills_block),
        "questions": listed(questions_block),
        "prd": prd,
    }


def evidence(case: dict) -> str:
    """Give the model the repository evidence the case names, and nothing else."""
    blocks = []
    for relative in case.get("source_paths", []):
        path = ROOT / relative
        if not path.is_file():
            blocks.append(f"<!-- {relative}: named by the case but absent from the repository -->")
            continue
        blocks.append(f"<!-- evidence: {relative} -->\n{path.read_text()}")
    return "\n\n---\n\n".join(blocks) if blocks else "No repository evidence was supplied with this request."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="model id or alias passed to claude -p")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--save-raw-dir",
        type=Path,
        help="directory for each case's unparsed model reply, named <case-id>.raw.txt",
    )
    args = parser.parse_args()
    case = json.load(sys.stdin)

    rendered = subprocess.run(
        ["python3", str(RENDERER), case.get("agent", "capture-refine"), "--all-skills"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout

    request = (
        f"{rendered}\n{TASK}\n"
        f"===REQUEST===\n{case['request']}\n\n"
        f"===SUPPLIED SOURCES===\n" + "\n".join(f"- {s}" for s in case.get("supplied_sources", [])) + "\n\n"
        f"===NAMED POLICY OWNERS===\n"
        + ("\n".join(f"- {o}" for o in case.get("named_policy_owners", [])) or "- none named")
        + f"\n\n===EVIDENCE===\n{evidence(case)}\n"
    )

    result = subprocess.run(
        ["claude", "-p", "--model", args.model],
        input=request, cwd=ROOT, capture_output=True, text=True, timeout=args.timeout,
    )
    if args.save_raw_dir:
        args.save_raw_dir.mkdir(parents=True, exist_ok=True)
        (args.save_raw_dir / f"{case['id']}.raw.txt").write_text(result.stdout)
    if result.returncode:
        raise SystemExit(f"{case['id']}: claude exited {result.returncode}: {result.stderr[:800]}")

    transcript = parse_response(result.stdout)
    transcript.update(
        case=case["id"],
        agent=case.get("agent", "capture-refine"),
        execution=f"live claude -p run, model {args.model}",
        model=args.model,
        prompt_bytes=len(request.encode()),
    )
    print(json.dumps(transcript, indent=2))


if __name__ == "__main__":
    main()
