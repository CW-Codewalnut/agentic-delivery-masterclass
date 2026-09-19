#!/usr/bin/env python3
"""Render one portable agent prompt bundle; no runtime installation implied."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("agent")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    manifest = json.loads((ROOT / "agent-system/manifest.json").read_text())
    agents = {a["id"]: a for a in manifest["agents"]}
    if args.agent not in agents:
        raise SystemExit(f"unknown agent {args.agent!r}; choose: {', '.join(agents)}")
    agent = agents[args.agent]
    paths = ["agent-system/CONCEPTS.md", "agent-system/AUTHORITY.md", agent["role"], agent["umbrella_skill"], *agent["skills"]]
    sections = [f"<!-- source: {path} -->\n{(ROOT / path).read_text().strip()}" for path in paths]
    sections.append("<!-- project context -->\n# Project context\n\nSupply repository-specific policy, architecture, vocabulary, evidence, tools, and authority here. Do not treat this placeholder as evidence.")
    rendered = "\n\n---\n\n".join(sections) + "\n"
    if args.output:
        args.output.write_text(rendered)
        print(f"rendered {args.agent}: {args.output} ({len(rendered.encode())} bytes)")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
