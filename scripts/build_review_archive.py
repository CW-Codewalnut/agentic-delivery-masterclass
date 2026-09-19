#!/usr/bin/env python3
"""Create and smoke-test a deterministic agent-first review archive."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist/seven-agent-system.zip"
INCLUDE_DIRS = (
    "agents",
    "docs/agent-system",
    "docs/examples",
    "docs/audit",
    "docs/research",
    "tests/scenarios",
)
INCLUDE_FILES = (
    "README.md",
    "scripts/audit_legacy_skills.py",
    "scripts/build_review_archive.py",
    "scripts/render_agent_prompt.py",
    "scripts/render_readme_agents.py",
    "scripts/run_scenario_checks.py",
    "scripts/validate_agent_system.py",
)
EXCLUDE_NAMES = {"__pycache__", ".DS_Store", "archive-receipt.json"}


def paths() -> list[Path]:
    result = [ROOT / path for path in INCLUDE_FILES]
    for folder in INCLUDE_DIRS:
        result.extend(
            path
            for path in (ROOT / folder).rglob("*")
            if path.is_file() and not any(part in EXCLUDE_NAMES for part in path.parts)
        )
    return sorted(set(result), key=lambda path: str(path.relative_to(ROOT)))


def rejected(command: list[str], cwd: Path) -> bool:
    return subprocess.run(command, cwd=cwd, capture_output=True).returncode != 0


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    selected = paths()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in selected:
            info = zipfile.ZipInfo(str(path.relative_to(ROOT)))
            info.date_time = (2026, 9, 19, 0, 0, 0)
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    OUT.with_suffix(".zip.sha256").write_text(f"{digest}  {OUT.name}\n")

    with tempfile.TemporaryDirectory() as temp:
        extracted = Path(temp)
        with zipfile.ZipFile(OUT) as archive:
            archive.extractall(extracted)
        subprocess.run(
            ["python3", "scripts/render_readme_agents.py", "--check"],
            cwd=extracted,
            check=True,
        )
        subprocess.run(
            ["python3", "scripts/validate_agent_system.py", "--root", str(extracted)],
            cwd=extracted,
            check=True,
        )
        rendered = extracted / "capture-refine-agent.md"
        subprocess.run(
            [
                "python3",
                "scripts/render_agent_prompt.py",
                "capture-refine",
                "--skill",
                "capture-intake-and-gaps",
                "--output",
                str(rendered),
            ],
            cwd=extracted,
            check=True,
        )
        if rendered.stat().st_size < 1000:
            raise SystemExit("rendered onboarding prompt unexpectedly small")
        if not rejected(
            ["python3", "scripts/render_agent_prompt.py", "capture-refine"], extracted
        ):
            raise SystemExit("empty skill selection was not rejected")
        if not rejected(
            [
                "python3",
                "scripts/render_agent_prompt.py",
                "capture-refine",
                "--skill",
                "reviewer-risk-and-false-green",
            ],
            extracted,
        ):
            raise SystemExit("cross-agent skill selection was not rejected")

    receipt = {
        "archive": str(OUT.relative_to(ROOT)),
        "sha256": digest,
        "files": len(selected),
        "layout": "agents/<agent>/{ROLE.md,skills/,templates/}",
        "inventory": {"agents": 7, "roles": 7, "skills": 25, "templates": 7},
        "fresh_extraction_validation": True,
        "fresh_extraction_readme_source_parity": True,
        "fresh_extraction_selected_render": True,
        "fresh_extraction_empty_selection_rejected": True,
        "fresh_extraction_cross_agent_selection_rejected": True,
    }
    (ROOT / "docs/audit/archive-receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n"
    )
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
