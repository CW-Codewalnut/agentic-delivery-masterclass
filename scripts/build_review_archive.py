#!/usr/bin/env python3
"""Create and smoke-test a deterministic review archive."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist/seven-agent-system.zip"
INCLUDE_DIRS = ("agent-system", "docs/audit", "docs/research", "tests/scenarios")
INCLUDE_FILES = (
    "README.md",
    "scripts/audit_legacy_skills.py",
    "scripts/build_refined_agent_system.py",
    "scripts/build_review_archive.py",
    "scripts/render_agent_prompt.py",
    "scripts/run_scenario_checks.py",
    "scripts/validate_agent_system.py",
)
EXCLUDE_NAMES = {"__pycache__", ".DS_Store", "archive-receipt.json"}


def paths() -> list[Path]:
    result = [ROOT / x for x in INCLUDE_FILES]
    for folder in INCLUDE_DIRS:
        result.extend(p for p in (ROOT / folder).rglob("*") if p.is_file() and not any(part in EXCLUDE_NAMES for part in p.parts))
    return sorted(set(result), key=lambda p: str(p.relative_to(ROOT)))


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    selected = paths()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in selected:
            info = zipfile.ZipInfo(str(path.relative_to(ROOT)))
            info.date_time = (2026, 9, 19, 0, 0, 0)
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    (OUT.with_suffix(".zip.sha256")).write_text(f"{digest}  {OUT.name}\n")
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(OUT) as zf: zf.extractall(td)
        subprocess.run(["python3", "scripts/validate_agent_system.py", "--root", td], cwd=td, check=True)
        rendered = Path(td) / "capture-refine-agent.md"
        subprocess.run(["python3", "scripts/render_agent_prompt.py", "capture-refine", "--output", str(rendered)], cwd=td, check=True)
        if rendered.stat().st_size < 1000: raise SystemExit("rendered onboarding prompt unexpectedly small")
    receipt = {"archive":str(OUT.relative_to(ROOT)),"sha256":digest,"files":len(selected),"fresh_extraction_validation":True,"fresh_extraction_capture_render":True}
    (ROOT / "docs/audit/archive-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
