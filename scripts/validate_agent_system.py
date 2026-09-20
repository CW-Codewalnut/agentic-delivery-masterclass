#!/usr/bin/env python3
"""Validate the canonical agent-first system and its documentation."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE = re.compile(r"(?:/Users/|/workspace/)")
BANNED = ("reusable methods", "working methods", "Open method")
ROLE_HEADINGS = (
    "## Outcome",
    "## Decision owned",
    "## Trigger and inputs",
    "## Orchestration",
    "## Decision gates",
    "## Handoff and return owner",
    "## Stop boundaries",
    "## Completion criterion",
    "## Authority limit",
    "## Linked dependencies",
)


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    block = text.split("---\n", 2)[1]
    data = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def outside_generated_catalogue(text: str) -> str:
    start = "<!-- BEGIN GENERATED AGENT CATALOGUE -->"
    end = "<!-- END GENERATED AGENT CATALOGUE -->"
    if start not in text or end not in text:
        return text
    before, remainder = text.split(start, 1)
    _, after = remainder.split(end, 1)
    return before + after


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    manifest_path = root / "agents/manifest.json"
    if not manifest_path.is_file():
        raise SystemExit("missing agents/manifest.json")
    manifest = json.loads(manifest_path.read_text())
    agents = manifest["agents"]
    ids = {agent["id"] for agent in agents}
    agents_by_id = {agent["id"]: agent for agent in agents}
    if len(agents) != 7 or len(ids) != 7:
        errors.append("manifest must declare seven unique agents")

    declared_roles = {agent["role"] for agent in agents}
    declared_skills = {skill for agent in agents for skill in agent["skills"]}
    declared_templates = {agent["template"] for agent in agents}
    actual_roles = {str(path.relative_to(root)) for path in (root / "agents").glob("*/ROLE.md")}
    actual_skills = {str(path.relative_to(root)) for path in (root / "agents").glob("*/skills/*/SKILL.md")}
    actual_templates = {str(path.relative_to(root)) for path in (root / "agents").glob("*/templates/*.md")}
    if declared_roles != actual_roles:
        errors.append(f"role membership mismatch: declared={len(declared_roles)} actual={len(actual_roles)}")
    if declared_skills != actual_skills:
        errors.append(f"skill membership/orphan mismatch: declared={len(declared_skills)} actual={len(actual_skills)}")
    if declared_templates != actual_templates:
        errors.append(f"template membership mismatch: declared={len(declared_templates)} actual={len(actual_templates)}")
    if (len(actual_roles), len(actual_skills), len(actual_templates)) != (7, 27, 7):
        errors.append("canonical inventory must be 7 roles, 27 skills, and 7 templates")
    if (root / "agent-system").exists():
        errors.append("obsolete agent-system canonical tree still exists")
    if list((root / "agents").rglob("workflow.md")) or list((root / "agents").rglob("WORKFLOW.md")):
        errors.append("workflow.md duplicates ROLE.md orchestration")

    skill_counts = {skill: sum(skill in agent["skills"] for agent in agents) for skill in declared_skills}
    if any(count != 1 for count in skill_counts.values()):
        errors.append("each canonical skill must belong to exactly one agent")

    for agent in agents:
        expected_prefix = f"agents/{agent['id']}/"
        owned_paths = [agent["role"], *agent["skills"], agent["template"]]
        if any(not path.startswith(expected_prefix) for path in owned_paths):
            errors.append(f"{agent['id']}: all role, skill, and template paths must be agent-owned")
        role_path = root / agent["role"]
        role_text = role_path.read_text()
        for heading in ROLE_HEADINGS:
            if heading not in role_text:
                errors.append(f"{agent['role']}: missing {heading}")
        for skill in agent["skills"]:
            relative = str(Path(skill).relative_to(Path(expected_prefix)))
            if f"]({relative})" not in role_text:
                errors.append(f"{agent['role']}: does not orchestrate linked skill {skill}")
        template_relative = str(Path(agent["template"]).relative_to(Path(expected_prefix)))
        if f"]({template_relative})" not in role_text:
            errors.append(f"{agent['role']}: missing linked output template")

    for relative in sorted(actual_skills):
        text = (root / relative).read_text()
        metadata = frontmatter(text)
        if metadata.get("name") != Path(relative).parent.name:
            errors.append(f"{relative}: frontmatter name mismatch")
        if not metadata.get("description", "").startswith("Use when "):
            errors.append(f"{relative}: description needs a concrete 'Use when' trigger")
        if "## Inputs" not in text or "## Output" not in text:
            errors.append(f"{relative}: missing Inputs or Output")
        if "## Procedure" not in text or "## Stop condition" not in text:
            errors.append(f"{relative}: missing Procedure or Stop condition")

    docs = [
        root / "README.md",
        *sorted((root / "agents").rglob("*.md")),
        *sorted((root / "docs/agent-system").glob("*.md")),
        *sorted((root / "docs/examples").glob("*.md")),
        *sorted((root / "docs/audit").glob("*.md")),
        *sorted((root / "docs/research").glob("*.md")),
        *sorted((root / "shared").glob("*.md")),
    ]
    for path in docs:
        text = path.read_text()
        relative = str(path.relative_to(root))
        if ABSOLUTE.search(text):
            errors.append(f"{relative}: host-specific absolute path")
        for phrase in BANNED:
            if phrase.lower() in text.lower():
                errors.append(f"{relative}: banned label {phrase!r}")
        link_text = outside_generated_catalogue(text) if path == root / "README.md" else text
        for target in LINK.findall(link_text):
            clean = target.split("#", 1)[0]
            if not clean or "://" in clean or clean.startswith("mailto:"):
                continue
            if not (path.parent / clean).resolve().exists():
                errors.append(f"{relative}: broken link {target}")

    # Shared skills tier. A vendored file is a verbatim third-party copy, so it is
    # checked for provenance and integrity and never for the house shape: editing
    # one to fit this repository's style would end the claim that it is verbatim.
    shared_skills = manifest.get("shared_skills", [])
    actual_shared = {
        str(path.relative_to(root)) for path in (root / "shared/skills").glob("*/SKILL.md")
    } if (root / "shared/skills").is_dir() else set()
    declared_shared = {entry["path"] for entry in shared_skills}
    if declared_shared != actual_shared:
        errors.append(
            f"shared skill membership/orphan mismatch: declared={len(declared_shared)} "
            f"actual={len(actual_shared)}"
        )
    shared_names = [entry["name"] for entry in shared_skills]
    if len(shared_names) != len(set(shared_names)):
        errors.append("shared skill names must be unique")
    for entry in shared_skills:
        name = entry["name"]
        if not entry["path"].startswith("shared/skills/") or Path(entry["path"]).parent.name != name:
            errors.append(f"shared/{name}: path must be shared/skills/{name}/SKILL.md")
        if len(entry["agents"]) < 2:
            errors.append(f"shared/{name}: fewer than two agents; it belongs to one agent's folder")
        for agent_id in entry["agents"]:
            if agent_id not in ids:
                errors.append(f"shared/{name}: unknown agent {agent_id}")
                continue
            role_text = (root / agents_by_id[agent_id]["role"]).read_text()
            if f"shared/skills/{name}/SKILL.md" not in role_text:
                errors.append(f"{agents_by_id[agent_id]['role']}: does not orchestrate shared {name}")
        if entry.get("verbatim"):
            provenance = entry.get("provenance", {})
            missing = [
                key for key in ("source", "repository", "commit", "licence", "licence_file", "sha256")
                if not provenance.get(key)
            ]
            if missing:
                errors.append(f"shared/{name}: provenance missing {', '.join(missing)}")
                continue
            if not (root / provenance["licence_file"]).is_file():
                errors.append(f"shared/{name}: licence file {provenance['licence_file']} is absent")
            digest = hashlib.sha256((root / entry["path"]).read_bytes()).hexdigest()
            if digest != provenance["sha256"]:
                errors.append(
                    f"shared/{name}: vendored file changed; re-pin upstream instead of editing it"
                )
    if shared_skills and not (root / "shared/ATTRIBUTION.md").is_file():
        errors.append("shared/ATTRIBUTION.md is required when the tier declares a shared skill")

    audit = json.loads((root / "docs/audit/skill-inventory.json").read_text())
    counts = audit["counts"]
    if (counts["total"], counts["umbrella"], counts["supporting"]) != (51, 7, 44):
        errors.append(f"unexpected source audit counts: {counts}")
    if counts["canonical_total"] != len(actual_roles) + len(actual_skills):
        errors.append(f"canonical migration count mismatch: {counts['canonical_total']}")
    mapping = json.loads((root / "docs/audit/legacy-to-canonical.json").read_text())
    if len(mapping) != 51:
        errors.append("legacy map must cover all 51 source skills")
    for target in mapping.values():
        if not (root / target).is_file():
            errors.append(f"legacy map target missing: {target}")

    scenario = json.loads((root / "tests/scenarios/seven-role-cases.json").read_text())
    cases = scenario["cases"]
    for agent_id in ids:
        case_ids = {case["id"] for case in cases if case["role"] == agent_id}
        if not any(case_id.endswith("positive") for case_id in case_ids) or not any(case_id.endswith("negative") for case_id in case_ids):
            errors.append(f"{agent_id}: missing positive or negative scenario")

    readme_check = subprocess.run(
        ["python3", "scripts/render_readme_agents.py", "--check"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if readme_check.returncode:
        errors.append(readme_check.stderr.strip() or readme_check.stdout.strip() or "README source parity failed")

    summary = {
        "agents": len(agents),
        "roles": len(actual_roles),
        "skills": len(actual_skills),
        "templates": len(actual_templates),
        "shared_skills": len(shared_skills),
        "legacy_mappings": len(mapping),
        "scenario_cases": len(cases),
        "readme_source_parity": readme_check.returncode == 0,
        "errors": len(errors),
    }
    print(json.dumps(summary, sort_keys=True))
    if errors:
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
