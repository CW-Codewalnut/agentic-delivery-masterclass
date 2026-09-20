#!/usr/bin/env python3
"""Replay stub for the Capture & Refine end-to-end harness.

This is not a model. It reads a case on stdin and replays the recorded
transcript for that case, so the --agent-command path stays tested in a suite
that makes no model call. A real run replaces this command; the results file
records whichever command produced the transcripts.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RECORDED = Path(__file__).resolve().parent / "recorded"


def main() -> None:
    case = json.load(sys.stdin)
    transcript = RECORDED / f"{case['id']}.json"
    if not transcript.is_file():
        raise SystemExit(f"no recorded transcript for case {case['id']}")
    sys.stdout.write(transcript.read_text())


if __name__ == "__main__":
    main()
