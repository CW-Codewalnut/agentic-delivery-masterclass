#!/usr/bin/env python3
"""Check a Capture & Refine PRD against the behavioural acceptance contract.

The contract is structural and semantic, not stylistic. It asks one question:
could a behavioural test fail on this document? Every finding names the exact
place that stops a test being written.

Modes:
  default      full content contract, used on a drafted PRD
  --shape-only headings and table columns only, used on the blank template
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ID = re.compile(r"\b[A-Z]{2,}-\d+\b")
PRIVATE_MARKER = re.compile(
    r"\b(internal state|private (?:field|method|function)|implementation detail"
    r"|in-?memory (?:map|dict)|internal (?:map|dict|field|counter))\b",
    re.IGNORECASE,
)
# A live run wrote "*unassigned*" on every gap and the checker passed them all.
# A placeholder is not an owner, and accepting one is a false green.
PLACEHOLDER_OWNER = re.compile(
    r"^(?:unassigned|unowned|tbd|to_?be_?(?:confirmed|decided|named)|none|n/?a"
    r"|unknown|not_?(?:named|assigned|set|yet)|nobody|open|pending|\?+)$",
    re.IGNORECASE,
)
LEAK_TERMS = (
    "redis", "postgres", "postgresql", "mysql", "mongodb", "dynamodb", "cassandra",
    "kafka", "rabbitmq", "sqs", "s3 bucket", "lambda", "kubernetes", "docker",
    "graphql", "grpc", "microservice", "stored procedure", "database column",
    "db column", "database index", "schema migration", "cache layer", "cron job",
    "websocket", "b-tree", "hash map", "linked list", "orm",
)
STATUSES = ("draft_for_engineer_completeness_review", "blocked")
POLARITIES = ("positive", "negative")
CHECK_TYPES = ("behavioural_test", "manual_check", "instrumented_metric")
BLOCKING_EFFECTS = ("blocking", "non_blocking")
NONFUNCTIONAL_CLASSES = (
    "security", "privacy", "accessibility", "reliability",
    "operability", "auditability", "compliance", "regional",
)
OUTCOME_KEYS = ("Success metric", "Counter-metric", "Instrumentation")
MIN_RATIONALE = 40

# Every table the contract reads: section heading -> required leading columns.
TABLES = {
    "Evidence register": ("Source", "Identity", "State", "Supported claim"),
    "Assumption register": ("ID", "Assumption", "Class", "Owner", "Effect if wrong"),
    "Requirements": ("ID", "Observable requirement", "Source IDs"),
    "Acceptance criteria": (
        "ID", "Requirement", "Polarity", "Given / when / then",
        "Counterpart", "Observation point", "Check",
    ),
    "Non-functional criteria": (
        "Class", "Requirement or non-applicability rationale", "Threshold", "Owner", "Check",
    ),
    "RED list": ("Check", "Expected failure before the change"),
    "Decisions and gaps": (
        "ID", "Question", "Owner", "Blocking effect", "Evidence", "Decision/status",
    ),
}
REQUIRED_SECTIONS = (
    "Evidence register", "Intended behaviour", "Assumption register", "Requirements",
    "Acceptance criteria", "Non-functional criteria", "Outcome contract", "RED list",
    "Decisions and gaps", "Design state", "Engineer completeness",
)
DECLARED_CODES = (
    "missing_section", "invalid_status", "missing_column", "empty_table",
    "untraced_requirement", "unshaped_criterion", "invalid_polarity",
    "invalid_check_type", "missing_negative_counterpart", "unknown_counterpart",
    "unknown_requirement", "duplicate_id", "implementation_leak",
    "unobservable_criterion", "unclassified_assumption", "missing_nonfunctional_class",
    "missing_nonfunctional_rationale", "missing_outcome_contract",
    "missing_red_entry", "unowned_gap", "invalid_blocking_effect",
    "status_conflicts_blocking_gap",
    "blocked_without_blocking_gap",
)

# A blocked draft must not invent the agreement it is blocked on. These tables may
# stay empty while a blocking gap is open; every other rule still applies.
RELAXED_WHEN_BLOCKED = (
    "Requirements", "Acceptance criteria", "Non-functional criteria", "RED list",
)


class Report:
    def __init__(self) -> None:
        self.findings: list[dict[str, str]] = []

    def add(self, code: str, location: str, detail: str) -> None:
        self.findings.append({"code": code, "location": location, "detail": detail})


def sections(text: str) -> dict[str, list[str]]:
    """Split the document into '## heading' blocks, preserving line order."""
    found: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            found.setdefault(current, [])
        elif current is not None:
            found[current].append(line)
    return found


def rows(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    """Return a markdown table's header cells and body rows."""
    table = [line for line in lines if line.strip().startswith("|")]
    table = [line for line in table if set(line.replace("|", "").strip()) - set("- :")]
    if not table:
        return [], []
    def cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]
    return cells(table[0]), [cells(line) for line in table[1:]]


def cell(row: list[str], header: list[str], column: str) -> str:
    return row[header.index(column)] if column in header and header.index(column) < len(row) else ""


def token(value: str) -> str:
    """Normalise an agreed-set value. A hyphen instead of an underscore carries
    no meaning, and a live model run showed one hyphen cascading into fifteen
    findings that hid the real ones."""
    return value.strip().lower().replace("-", "_")


def leaks(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in LEAK_TERMS if term in lowered]


def check_shape(text: str, report: Report) -> dict[str, list[str]]:
    blocks = sections(text)
    for name in REQUIRED_SECTIONS:
        if name not in blocks:
            report.add("missing_section", name, "the contract requires this section")
    for name, columns in TABLES.items():
        if name not in blocks:
            continue
        header, _ = rows(blocks[name])
        for column in columns:
            if column not in header:
                report.add("missing_column", f"{name}/{column}", "declared column is absent")
    outcome = "\n".join(blocks.get("Outcome contract", []))
    for key in OUTCOME_KEYS:
        if f"{key}:" not in outcome:
            report.add("missing_outcome_contract", f"Outcome contract/{key}", "key is absent")
    return blocks


def check_content(text: str, blocks: dict[str, list[str]], report: Report) -> None:
    status = ""
    for line in text.splitlines():
        if line.strip().startswith("- Status:"):
            status = line.split(":", 1)[1].strip().strip("`")
            break
    if status not in STATUSES:
        report.add("invalid_status", "Status", f"{status!r} is not one of {STATUSES}")

    blocked = status == "blocked"
    for name in TABLES:
        if blocked and name in RELAXED_WHEN_BLOCKED:
            continue
        if name in blocks and not rows(blocks[name])[1]:
            report.add("empty_table", name, "the contract needs at least one row")

    requirement_header, requirement_rows = rows(blocks.get("Requirements", []))
    requirement_ids: list[str] = []
    for row in requirement_rows:
        rid = cell(row, requirement_header, "ID")
        requirement_ids.append(rid)
        statement = cell(row, requirement_header, "Observable requirement")
        if not ID.search(cell(row, requirement_header, "Source IDs")):
            report.add("untraced_requirement", rid, "no source identifier is cited")
        for term in leaks(statement):
            report.add("implementation_leak", rid, f"names the implementation term {term!r}")
    duplicates = {rid for rid in requirement_ids if requirement_ids.count(rid) > 1}

    criterion_header, criterion_rows = rows(blocks.get("Acceptance criteria", []))
    criteria: dict[str, dict[str, str]] = {}
    order: list[str] = []
    for row in criterion_rows:
        cid = cell(row, criterion_header, "ID")
        if cid in criteria:
            duplicates.add(cid)
        criteria[cid] = {column: cell(row, criterion_header, column) for column in criterion_header}
        order.append(cid)
    for cid in sorted(duplicates):
        report.add("duplicate_id", cid, "one identifier must name one row")

    for cid in order:
        row = criteria[cid]
        statement = row.get("Given / when / then", "")
        lowered = statement.lower()
        if not (lowered.startswith("given ") and " when " in lowered and " then " in lowered):
            report.add("unshaped_criterion", cid, "not shaped as given / when / then")
        polarity = row.get("Polarity", "")
        if polarity not in POLARITIES:
            report.add("invalid_polarity", cid, f"{polarity!r} is not one of {POLARITIES}")
        if row.get("Check", "") not in CHECK_TYPES:
            report.add("invalid_check_type", cid, f"{row.get('Check')!r} is not one of {CHECK_TYPES}")
        requirement = row.get("Requirement", "")
        if requirement and requirement not in requirement_ids:
            report.add("unknown_requirement", cid, f"cites unknown requirement {requirement!r}")
        observation = row.get("Observation point", "")
        if not observation or PRIVATE_MARKER.search(observation):
            report.add("unobservable_criterion", cid, f"observation point {observation!r} is not public behaviour")
        for term in leaks(statement):
            report.add("implementation_leak", cid, f"names the implementation term {term!r}")
        counterparts = ID.findall(row.get("Counterpart", ""))
        unknown = [ref for ref in counterparts if ref not in criteria]
        for ref in unknown:
            report.add("unknown_counterpart", cid, f"counterpart {ref} does not exist")
        if polarity == "positive":
            negatives = [
                ref for ref in counterparts
                if ref in criteria and criteria[ref].get("Polarity") == "negative"
            ]
            if not negatives:
                report.add(
                    "missing_negative_counterpart",
                    cid,
                    "a positive criterion needs a refusal, boundary, repeat, conflict, or race counterpart",
                )

    assumption_header, assumption_rows = rows(blocks.get("Assumption register", []))
    for row in assumption_rows:
        aid = cell(row, assumption_header, "ID")
        if cell(row, assumption_header, "Class") not in ("decided", "owned_open", "engineering_observable"):
            report.add("unclassified_assumption", aid, "class must be decided, owned_open, or engineering_observable")

    nf_header, nf_rows = rows(blocks.get("Non-functional criteria", []))
    seen_classes = set()
    for row in nf_rows:
        name = cell(row, nf_header, "Class").lower()
        seen_classes.add(name)
        rationale = cell(row, nf_header, "Requirement or non-applicability rationale")
        threshold = cell(row, nf_header, "Threshold")
        if threshold == "not_applicable" and len(rationale) < MIN_RATIONALE:
            report.add("missing_nonfunctional_rationale", name, "non-applicability needs a stated reason")
        if not threshold or not rationale:
            report.add("missing_nonfunctional_rationale", name, "requirement and threshold are both required")
    for name in NONFUNCTIONAL_CLASSES:
        if not blocked and name not in seen_classes:
            report.add("missing_nonfunctional_class", name, "each class needs a criterion or a stated reason")

    outcome = "\n".join(blocks.get("Outcome contract", []))
    for key in OUTCOME_KEYS:
        value = ""
        for line in outcome.splitlines():
            if f"{key}:" in line:
                value = line.split(":", 1)[1].strip()
        if not value and not blocked:
            report.add("missing_outcome_contract", key, "key is absent or has no value")

    red_header, red_rows = rows(blocks.get("RED list", []))
    red_checks = {cell(row, red_header, "Check") for row in red_rows}
    for cid in order:
        if not blocked and criteria[cid].get("Check") == "behavioural_test" and cid not in red_checks:
            report.add("missing_red_entry", cid, "a behavioural criterion needs its expected failure")

    gap_header, gap_rows = rows(blocks.get("Decisions and gaps", []))
    blocking = False
    for row in gap_rows:
        gid = cell(row, gap_header, "ID")
        effect = token(cell(row, gap_header, "Blocking effect"))
        owner = cell(row, gap_header, "Owner").strip(" *_`")
        if not owner or PLACEHOLDER_OWNER.match(owner.replace(" ", "_")):
            report.add("unowned_gap", gid, f"owner {owner!r} names nobody who can decide")
        if effect not in BLOCKING_EFFECTS:
            report.add(
                "invalid_blocking_effect", gid, f"{effect!r} is not one of {BLOCKING_EFFECTS}"
            )
        if effect == "blocking":
            blocking = True
    if blocking and status == "draft_for_engineer_completeness_review":
        report.add(
            "status_conflicts_blocking_gap",
            "Status",
            "a blocking gap cannot sit in a draft offered for completeness review",
        )
    if blocked and not blocking:
        report.add(
            "blocked_without_blocking_gap",
            "Status",
            "a blocked draft must name the blocking gap that blocks it",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--shape-only", action="store_true", help="check headings and columns only")
    parser.add_argument("--json", action="store_true", help="emit the machine-readable report")
    args = parser.parse_args()
    text = args.path.read_text()
    report = Report()
    blocks = check_shape(text, report)
    if not args.shape_only:
        check_content(text, blocks, report)
    payload = {
        "path": str(args.path),
        "mode": "shape_only" if args.shape_only else "full",
        "declared_codes": list(DECLARED_CODES),
        "findings": report.findings,
        "summary": {"findings": len(report.findings)},
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload["summary"], sort_keys=True))
        for finding in report.findings:
            print(f"{finding['code']}\t{finding['location']}\t{finding['detail']}")
    raise SystemExit(1 if report.findings else 0)


if __name__ == "__main__":
    main()
