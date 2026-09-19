#!/usr/bin/env python3
"""Audit the 51 proposed legacy skills and emit review artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

UMBRELLAS = {"capture-refine", "design", "planner", "builder", "tester", "reviewer", "curator"}
MAP = {
    "capture-refine": "capture-refine", "design": "design", "planner": "planner", "builder": "builder", "tester": "tester", "reviewer": "reviewer", "curator": "curator",
    "capture-request-review": "capture-intake-and-gaps", "capture-prior-prd-impact": "capture-intake-and-gaps", "capture-architecture-constraints": "capture-intake-and-gaps", "capture-gap-analysis": "capture-intake-and-gaps",
    "capture-engineer-interview": "capture-engineer-interview", "capture-prd-composition": "capture-prd-handoff", "capture-engineer-completeness-handoff": "capture-prd-handoff",
    "design-input-revision-gate": "design-input-readiness", "design-requirement-state-model": "design-state-interaction-spec", "design-accessibility-interaction-spec": "design-state-interaction-spec", "design-source-of-truth-composition": "design-source-readiness", "design-coverage-conflict-review": "design-source-readiness", "design-readiness-handoff": "design-source-readiness",
    "planner-input-alignment-gate": "planner-impact-and-invariants", "planner-repository-impact-map": "planner-impact-and-invariants", "planner-invariant-consistency-design": "planner-impact-and-invariants", "planner-increment-task-sequencing": "planner-delivery-slices", "planner-test-observability-plan": "planner-verification-and-handoff", "planner-migration-rollout-rollback": "planner-verification-and-handoff", "planner-engineer-review-handoff": "planner-verification-and-handoff",
    "builder-authority-baseline-gate": "builder-baseline-and-red", "builder-criterion-red-proof": "builder-baseline-and-red", "builder-scoped-implementation": "builder-bounded-change", "builder-migration-config-safety": "builder-verification-and-deviation", "builder-verification-receipt": "builder-verification-and-deviation", "builder-deviation-escalation": "builder-verification-and-deviation",
    "tester-evidence-plan": "tester-evidence-and-negative-control", "tester-negative-control": "tester-evidence-and-negative-control", "tester-behaviour-side-effect-checks": "tester-adversarial-behaviour", "tester-concurrency-boundary-checks": "tester-adversarial-behaviour", "tester-defect-reproduction": "tester-defect-and-handoff", "tester-coverage-classification-handoff": "tester-defect-and-handoff",
    "reviewer-revision-evidence-pin": "reviewer-revision-and-acceptance", "reviewer-acceptance-trace": "reviewer-revision-and-acceptance", "reviewer-security-consistency-audit": "reviewer-risk-and-false-green", "reviewer-false-green-attack": "reviewer-risk-and-false-green", "reviewer-merge-release-separation": "reviewer-decision-and-recheck", "reviewer-delta-recheck": "reviewer-decision-and-recheck",
    "curator-finding-provenance": "curator-provenance-and-classification", "curator-learning-classification": "curator-provenance-and-classification", "curator-destination-routing": "curator-proposal-and-history", "curator-proposal-governance": "curator-proposal-and-history", "curator-version-history-maintenance": "curator-proposal-and-history", "curator-next-use-evaluation": "curator-next-use-evaluation",
}
CONTRIBUTION = {
    "request-review": "separates supplied request material from relevant repository evidence",
    "prior-prd-impact": "finds changed or conflicting prior product decisions",
    "architecture-constraints": "captures only current-system constraints needed to state product behaviour safely",
    "gap-analysis": "turns missing behaviour into owned product decisions",
    "engineer-interview": "records engineering evidence without converting it to Product policy",
    "prd-composition": "writes traceable requirements and acceptance criteria",
    "engineer-completeness-handoff": "binds Engineering completeness to an exact PRD revision",
    "input-revision-gate": "rejects stale, unapproved, mismatched, or unauthorised Design inputs",
    "requirement-state-model": "maps requirements to visible states and transitions",
    "accessibility-interaction-spec": "specifies content, focus, keyboard, announcements, and recovery",
    "source-of-truth-composition": "separates specification-only output from authorised editable-source mutation",
    "coverage-conflict-review": "finds uncovered states and Product-policy conflicts",
    "readiness-handoff": "binds Design readiness to exact Product and Design revisions",
    "input-alignment-gate": "aligns Product, Design, repository scope, and owners",
    "repository-impact-map": "maps affected seams, contracts, data, and owners",
    "invariant-consistency-design": "states invariants and real consistency boundaries",
    "increment-task-sequencing": "creates dependency-ordered, independently provable increments",
    "test-observability-plan": "maps requirements and risks to checks and operator signals",
    "migration-rollout-rollback": "defines compatibility, rollout, abort, rollback, and reconciliation",
    "engineer-review-handoff": "binds Engineering acceptance to an exact plan revision",
    "authority-baseline-gate": "pins change authority, base identity, environment, and baseline",
    "criterion-red-proof": "requires a criterion-level causal RED",
    "scoped-implementation": "keeps one implementation increment inside accepted scope",
    "migration-config-safety": "guards authorised migration and configuration changes",
    "verification-receipt": "binds fresh checks to the exact result",
    "deviation-escalation": "returns material deviations to their decision owner",
    "evidence-plan": "maps claims to observable assertions and limits",
    "negative-control": "proves the harness detects a semantic defect",
    "behaviour-side-effect-checks": "checks outputs, persisted state, side effects, and forbidden mutations",
    "concurrency-boundary-checks": "tests contention while naming the observed topology boundary",
    "defect-reproduction": "reduces failures to revision-bound reproducers",
    "coverage-classification-handoff": "classifies every claim before Reviewer handoff",
    "revision-evidence-pin": "pins target bytes, upstream revisions, independence, and cutoff",
    "acceptance-trace": "traces criterion sub-claims across intent, implementation, and proof",
    "security-consistency-audit": "reviews authorisation, lifecycle, consistency, and disclosure",
    "false-green-attack": "asks which defects could leave evidence green",
    "merge-release-separation": "separates merge recommendation from release confidence",
    "delta-recheck": "invalidates and reruns evidence after material changes",
    "finding-provenance": "binds a narrow learning claim to safe immutable evidence",
    "learning-classification": "separates skill guidance, repository context, product work, and local detail",
    "destination-routing": "selects one governed home and owner",
    "proposal-governance": "keeps updates proposed until explicit adoption",
    "version-history-maintenance": "retains accepted, rejected, and superseded history",
    "next-use-evaluation": "requires an observed future use before claiming benefit",
}


def contribution(name: str) -> str:
    if name in UMBRELLAS:
        return f"routes the {name} role across its conditional skills and handoff gate"
    for suffix, text in CONTRIBUTION.items():
        if name.endswith(suffix):
            return text
    raise KeyError(name)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--out", default=Path("docs/audit"), type=Path)
    args = ap.parse_args()
    files = sorted((args.source / "skills").glob("*/SKILL.md"))
    if len(files) != 51:
        raise SystemExit(f"expected 51 source skills, found {len(files)}")
    if set(p.parent.name for p in files) != set(MAP):
        missing = set(MAP) - {p.parent.name for p in files}
        extra = {p.parent.name for p in files} - set(MAP)
        raise SystemExit(f"mapping mismatch missing={sorted(missing)} extra={sorted(extra)}")

    role_boundary = re.compile(r"^This is a skill, not an agent role or authority grant\.", re.M)
    records = []
    repeated = 0
    for path in files:
        name = path.parent.name
        text = path.read_text()
        has_boilerplate = bool(role_boundary.search(text))
        repeated += has_boilerplate
        target = MAP[name]
        merged = name != target and sum(1 for value in MAP.values() if value == target) > 1
        decision = "rewrite" if name in UMBRELLAS or name == target else "merge"
        duplicate = (
            "Repeated role/context/tool/iterative-flow paragraph adds no file-specific behaviour. "
            + ("The orchestration is retained as a shorter router." if name in UMBRELLAS else f"Its distinct rule is retained in `{target}`; overlapping inputs, outputs, stops, and authority prose are consolidated there.")
        )
        records.append({
            "source_file": f"skills/{name}/SKILL.md",
            "name": name,
            "kind": "umbrella" if name in UMBRELLAS else "supporting",
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "word_count": len(text.split()),
            "specific_behavioural_contribution": contribution(name),
            "no_op_or_duplication": duplicate,
            "decision": decision,
            "canonical_replacement": f"agent-system/skills/{target}/SKILL.md",
            "repeated_role_boundary_boilerplate": has_boilerplate,
        })

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    inventory = {
        "source": "unpublished local proposal at live-main base d819bff2a9443eaae854665f7e24c940450d8172",
        "counts": {"total": len(records), "umbrella": sum(r["kind"] == "umbrella" for r in records), "supporting": sum(r["kind"] == "supporting" for r in records), "repeated_role_boundary_paragraphs": repeated, "canonical_total": len(set(MAP.values())), "canonical_umbrella": 7, "canonical_supporting": len(set(MAP.values())) - 7},
        "records": records,
    }
    (out / "skill-inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
    mapping = {r["source_file"]: r["canonical_replacement"] for r in records}
    (out / "legacy-to-canonical.json").write_text(json.dumps(mapping, indent=2) + "\n")

    groups = Counter(MAP.values())
    lines = ["# Skill audit findings", "", "## Result", "", f"Audited all **{len(records)}** files: 7 umbrella and 44 supporting skills. The source repeated the same long role/context/tool paragraph in **{repeated} supporting skills**. The canonical set keeps 7 short routers and consolidates 44 supporting files into 21 skills; every source file has an old-to-new mapping.", "", "This is a document audit. It identifies duplication and weak information hierarchy by inspection; it does not prove model behaviour. Simulated role scenarios are reported separately.", "", "## Decision by file", "", "| Source | Contribution retained | Duplication/no-op finding | Decision | Canonical path |", "|---|---|---|---|---|"]
    for r in records:
        source = f"`{r['source_file']}`"
        canonical = f"`{r['canonical_replacement']}`"
        lines.append(f"| {source} | {r['specific_behavioural_contribution']} | repeated generic role/tool boundary; overlapping schema in group of {groups[MAP[r['name']]]} | {r['decision']} | {canonical} |")
    lines += ["", "## What changed", "", "- Role authority and cross-cutting semantics moved to one role file plus `CONCEPTS.md` and `AUTHORITY.md`.", "- Routers now decide which skill to open; they no longer restate each supporting skill.", "- Supporting skills keep trigger, inputs, ordered procedure, checkable output, and stop condition only.", "- Closely coupled fragments were merged where using one without the other produced an incomplete artifact.", "- Safety gates, revision identity, human authority, negative controls, false-green attacks, and confidence boundaries were retained.", "", "## Limits", "", "The audit does not claim the final prompts outperform the source under live model execution. The repository includes deterministic structural checks and simulated positive/negative gate scenarios; independent content review and model evaluations remain future work."]
    (out / "skill-audit.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(inventory["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
