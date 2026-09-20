#!/usr/bin/env python3
"""Replay stub for the Capture & Refine end-to-end harness.

This is not a model. It reads a case on stdin and replays the recorded
transcript for that case, so the --agent-command path stays tested in a suite
that makes no model call. A real run replaces this command; the results file
records whichever command produced the transcripts.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RECORDED = Path(__file__).resolve().parent / "recorded"
ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--probe",
        type=Path,
        help="record any harness scratch path inside the repository, for the no-pollution test",
    )
    args = parser.parse_args()
    case = json.load(sys.stdin)
    if args.probe:
        args.probe.parent.mkdir(parents=True, exist_ok=True)
        args.probe.write_text(json.dumps(sorted(p.name for p in ROOT.glob(".e2e*"))))
    transcript = RECORDED / f"{case['id']}.json"
    if not transcript.is_file():
        raise SystemExit(f"no recorded transcript for case {case['id']}")
    sys.stdout.write(transcript.read_text())


if __name__ == "__main__":
    main()
