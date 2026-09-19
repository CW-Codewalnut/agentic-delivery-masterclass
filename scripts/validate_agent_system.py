#!/usr/bin/env python3
"""Validate the canonical agent system and its documentation."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE = re.compile(r"(?:/Users/|/workspace/)")
BANNED = ("reusable methods", "working methods", "Open method")
ROLE_HEADINGS = ("## Decision owned", "## Start boundary", "## Work", "## Return path", "## Completion criterion", "## Authority limit", "## Skills")


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    block = text.split("---\n", 2)[1]
    data = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    root = args.root.resolve()
    errors = []
    manifest_path = root / "agent-system/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    agents = manifest["agents"]
    if len(agents) != 7 or len({a["id"] for a in agents}) != 7:
        errors.append("manifest must declare seven unique agents")

    declared_roles = {a["role"] for a in agents}
    declared_skills = {a["umbrella_skill"] for a in agents}
    declared_support = {s for a in agents for s in a["skills"]}
    declared_templates = {a["template"] for a in agents}
    actual_roles = {str(p.relative_to(root)) for p in (root / "agent-system/roles").glob("*.md")}
    actual_skills = {str(p.relative_to(root)) for p in (root / "agent-system/skills").glob("*/SKILL.md")}
    actual_templates = {str(p.relative_to(root)) for p in (root / "agent-system/templates").glob("*.md")}
    if declared_roles != actual_roles: errors.append(f"role membership mismatch: declared={len(declared_roles)} actual={len(actual_roles)}")
    if declared_skills | declared_support != actual_skills: errors.append(f"skill membership/orphan mismatch: declared={len(declared_skills | declared_support)} actual={len(actual_skills)}")
    if len(declared_skills) != 7 or len(declared_support) != 21: errors.append("expected 7 umbrella and 21 supporting skills")
    if declared_templates != actual_templates or len(actual_templates) != 7: errors.append("template membership mismatch")

    support_counts = {s: sum(s in a["skills"] for a in agents) for s in declared_support}
    if any(v != 1 for v in support_counts.values()): errors.append("each supporting skill must belong to exactly one role")

    for agent in agents:
        role = root / agent["role"]
        text = role.read_text()
        for heading in ROLE_HEADINGS:
            if heading not in text: errors.append(f"{agent['role']}: missing {heading}")
        for path in [agent["umbrella_skill"], *agent["skills"], agent["template"]]:
            if not (root / path).is_file(): errors.append(f"missing manifest path: {path}")

    for rel in sorted(actual_skills):
        text = (root / rel).read_text()
        fm = frontmatter(text)
        if fm.get("name") != Path(rel).parent.name: errors.append(f"{rel}: frontmatter name mismatch")
        if not fm.get("description", "").startswith("Use when "): errors.append(f"{rel}: description needs a concrete 'Use when' trigger")
        if "## Inputs" not in text or "## Output" not in text: errors.append(f"{rel}: missing Inputs or Output")
        is_umbrella = rel in declared_skills
        if is_umbrella and "## Route" not in text: errors.append(f"{rel}: umbrella missing Route")
        if not is_umbrella and ("## Procedure" not in text or "## Stop condition" not in text): errors.append(f"{rel}: support skill missing Procedure or Stop condition")

    docs = [root / "README.md", *sorted((root / "agent-system").rglob("*.md")), *sorted((root / "docs/audit").glob("*.md")), *sorted((root / "docs/research").glob("*.md"))]
    for path in docs:
        text = path.read_text()
        rel = str(path.relative_to(root))
        if ABSOLUTE.search(text): errors.append(f"{rel}: host-specific absolute path")
        for phrase in BANNED:
            if phrase.lower() in text.lower(): errors.append(f"{rel}: banned label {phrase!r}")
        for target in LINK.findall(text):
            clean = target.split("#", 1)[0]
            if not clean or "://" in clean or clean.startswith("mailto:"):
                continue
            if not (path.parent / clean).resolve().exists(): errors.append(f"{rel}: broken link {target}")

    audit = json.loads((root / "docs/audit/skill-inventory.json").read_text())
    counts = audit["counts"]
    if (counts["total"], counts["umbrella"], counts["supporting"], counts["canonical_total"]) != (51, 7, 44, 28):
        errors.append(f"unexpected audit counts: {counts}")
    mapping = json.loads((root / "docs/audit/legacy-to-canonical.json").read_text())
    if len(mapping) != 51: errors.append("legacy map must cover all 51 source skills")
    for target in mapping.values():
        if not (root / target).is_file(): errors.append(f"legacy map target missing: {target}")

    scenario = json.loads((root / "tests/scenarios/seven-role-cases.json").read_text())
    cases = scenario["cases"]
    for agent in {a["id"] for a in agents}:
        ids = {c["id"] for c in cases if c["role"] == agent}
        if not any(i.endswith("positive") for i in ids) or not any(i.endswith("negative") for i in ids): errors.append(f"{agent}: missing positive or negative scenario")

    summary = {"agents":len(agents),"roles":len(actual_roles),"umbrella_skills":len(declared_skills),"supporting_skills":len(declared_support),"templates":len(actual_templates),"legacy_mappings":len(mapping),"scenario_cases":len(cases),"errors":len(errors)}
    print(json.dumps(summary, sort_keys=True))
    if errors:
        for error in errors: print("ERROR", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
