#!/usr/bin/env python3
"""Render a portable prompt with explicitly selected supporting skills."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Render one role, its router, selected skills, and output template."
    )
    ap.add_argument("agent")
    ap.add_argument(
        "--skill",
        action="append",
        default=[],
        help="supporting skill name to include; repeat for each applicable skill",
    )
    ap.add_argument(
        "--all-skills",
        action="store_true",
        help="include every supporting skill for this agent",
    )
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    manifest = json.loads((ROOT / "agent-system/manifest.json").read_text())
    agents = {agent["id"]: agent for agent in manifest["agents"]}
    if args.agent not in agents:
        raise SystemExit(f"unknown agent {args.agent!r}; choose: {', '.join(agents)}")
    if args.all_skills and args.skill:
        raise SystemExit("choose explicit --skill values or --all-skills, not both")
    if not args.all_skills and not args.skill:
        raise SystemExit("select at least one supporting skill with --skill, or use --all-skills")

    agent = agents[args.agent]
    available = {Path(path).parent.name: path for path in agent["skills"]}
    unknown = sorted(set(args.skill) - set(available))
    if unknown:
        raise SystemExit(
            f"skills not available to {args.agent}: {', '.join(unknown)}; "
            f"choose from: {', '.join(available)}"
        )
    if args.all_skills:
        selected = list(agent["skills"])
    else:
        selected = [available[name] for name in args.skill]

    paths = [
        "agent-system/CONCEPTS.md",
        "agent-system/AUTHORITY.md",
        agent["role"],
        agent["umbrella_skill"],
        *selected,
        agent["template"],
    ]
    selection = ", ".join(Path(path).parent.name for path in selected) or "none"
    preamble = (
        "# Portable agent prompt\n\n"
        f"- Agent: `{args.agent}`\n"
        f"- Included supporting skills: {selection}\n\n"
        "The router names other possible skills. Only the supporting skills listed above are loaded in this bundle. "
        "Render again with the applicable `--skill` values if the case changes.\n"
    )
    sections = [preamble]
    sections.extend(
        f"<!-- source: {path} -->\n{(ROOT / path).read_text().strip()}" for path in paths
    )
    sections.append(
        "<!-- project context -->\n# Project context\n\n"
        "Replace this section with repository-specific policy, architecture, vocabulary, evidence, tools, and authority. "
        "This placeholder is not evidence or permission."
    )
    rendered = "\n\n---\n\n".join(sections) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
        print(
            f"rendered {args.agent}: {args.output} "
            f"({len(selected)} supporting skills, {len(rendered.encode())} bytes)"
        )
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
