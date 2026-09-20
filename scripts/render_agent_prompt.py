#!/usr/bin/env python3
"""Render a portable prompt with explicitly selected agent-owned skills."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render one orchestrating ROLE.md, selected owned skills, and output template."
    )
    parser.add_argument("agent")
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="owned skill name to include; repeat for each applicable skill",
    )
    parser.add_argument(
        "--all-skills",
        action="store_true",
        help="include every skill owned by this agent",
    )
    parser.add_argument(
        "--shared-skill",
        action="append",
        default=[],
        help="shared skill name to include; only one this agent is declared to use",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads((ROOT / "agents/manifest.json").read_text())
    agents = {agent["id"]: agent for agent in manifest["agents"]}
    if args.agent not in agents:
        raise SystemExit(f"unknown agent {args.agent!r}; choose: {', '.join(agents)}")
    if args.all_skills and args.skill:
        raise SystemExit("choose explicit --skill values or --all-skills, not both")
    if not args.all_skills and not args.skill:
        raise SystemExit("select at least one owned skill with --skill, or use --all-skills")

    agent = agents[args.agent]
    available = {Path(path).parent.name: path for path in agent["skills"]}
    unknown = sorted(set(args.skill) - set(available))
    if unknown:
        raise SystemExit(
            f"skills not owned by {args.agent}: {', '.join(unknown)}; "
            f"choose from: {', '.join(available)}"
        )
    selected = list(agent["skills"]) if args.all_skills else [available[name] for name in args.skill]

    # A shared skill loads only for an agent the manifest declares uses it.
    shared_by_name = {entry["name"]: entry for entry in manifest.get("shared_skills", [])}
    unknown_shared = sorted(set(args.shared_skill) - set(shared_by_name))
    if unknown_shared:
        raise SystemExit(
            f"unknown shared skills: {', '.join(unknown_shared)}; "
            f"choose from: {', '.join(shared_by_name)}"
        )
    not_permitted = sorted(
        name for name in args.shared_skill if args.agent not in shared_by_name[name]["agents"]
    )
    if not_permitted:
        raise SystemExit(
            f"shared skills not declared for {args.agent}: {', '.join(not_permitted)}"
        )
    shared_selected = [shared_by_name[name] for name in args.shared_skill]

    paths = [
        *manifest["shared"],
        agent["role"],
        *selected,
        *(entry["path"] for entry in shared_selected),
        agent["template"],
    ]
    selection = ", ".join(Path(path).parent.name for path in selected)
    shared_lines = ""
    for entry in shared_selected:
        provenance = entry.get("provenance", {})
        if entry.get("verbatim"):
            shared_lines += (
                f"- Included shared skill: `{entry['name']}` — verbatim copy from "
                f"{provenance.get('repository')} at {provenance.get('commit', '')[:8]}, "
                f"{provenance.get('licence')}; notice retained in "
                f"`{provenance.get('licence_file')}`\n"
            )
        else:
            shared_lines += f"- Included shared skill: `{entry['name']}`\n"
    preamble = (
        "# Portable agent prompt\n\n"
        f"- Agent: `{args.agent}`\n"
        f"- Included owned skills: {selection}\n"
        f"{shared_lines}\n"
        "ROLE.md owns routing and names other possible skills. Only the explicitly selected skills are loaded in this bundle. "
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
            f"({len(selected)} owned skills, {len(shared_selected)} shared, "
            f"{len(rendered.encode())} bytes)"
        )
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
