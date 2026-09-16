#!/usr/bin/env python3
"""Remove machine-specific absolute paths from Playwright's JSON receipt."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "qa" / "playwright-results.json"


def sanitize(value):
    if isinstance(value, dict):
        return {key: sanitize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, str):
        value = value.replace(str(ROOT), "$REPO")
        if value.startswith("/") and ("playwright" in value.lower() or "node" in value.lower()):
            return Path(value).name
    return value


if REPORT.is_file():
    data = sanitize(json.loads(REPORT.read_text(encoding="utf-8")))
    REPORT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"sanitized {REPORT.relative_to(ROOT)}")
