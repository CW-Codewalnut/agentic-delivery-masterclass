#!/usr/bin/env python3
"""Run deterministic gate simulations for positive/negative role cases."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def decide(role: str, x: dict) -> dict:
    if role == "capture-refine":
        if not x.get("request_identity"): return {"status":"blocked","reason":"missing_request_identity"}
        if not x.get("relevant_evidence") or not x.get("gaps_have_owners"): return {"status":"blocked","reason":"incomplete_evidence_or_ownership"}
        return {"status":"draft_for_engineer_completeness_review"}
    if role == "design":
        if not x.get("prd_approved") or not x.get("revision_match"): return {"status":"blocked","reason":"stale_or_unapproved_input"}
        if x.get("design_complete"): return {"status":"design_not_required"}
        if x.get("editable_requested") and not x.get("editable_authority"): return {"status":"blocked","reason":"missing_editable_authority"}
        if x.get("policy_blocker") or not x.get("design_review"): return {"status":"blocked","reason":"missing_policy_or_design_review"}
        return {"status":"ready","mode":"authorised_editable_source" if x.get("editable_authority") else "specification_only"}
    if role == "planner":
        if x.get("business_ambiguity"): return {"status":"blocked","reason":"return_business_ambiguity"}
        if not x.get("prd_approved") or x.get("design_status") not in {"ready","design_not_required"} or not x.get("revision_match"): return {"status":"blocked","reason":"unaligned_inputs"}
        return {"status":"ready_for_build"} if x.get("engineering_acceptance") else {"status":"blocked","reason":"engineering_acceptance_missing"}
    if role == "builder":
        if not x.get("change_authority"): return {"status":"blocked","reason":"missing_change_authority"}
        if x.get("plan_status") != "ready_for_build" or not x.get("causal_red"): return {"status":"blocked","reason":"plan_or_red_gate"}
        if x.get("material_deviation"): return {"status":"blocked","reason":"return_material_deviation"}
        return {"status":"built_for_test"} if x.get("exact_result") else {"status":"blocked","reason":"missing_result_identity"}
    if role == "tester":
        if not x.get("exact_target") or x.get("material_drift"): return {"status":"blocked","reason":"target_identity_or_drift"}
        if not x.get("expectation_approved"): return {"status":"blocked","reason":"return_unknown_expectation"}
        if x.get("negative_control") != "intended_assertion": return {"status":"blocked","reason":"wrong_cause_negative_control"}
        return {"status":"tested"}
    if role == "reviewer":
        if not x.get("exact_target"): return {"status":"blocked","reason":"missing_target_identity"}
        if not x.get("matching_inputs") or not x.get("independent") or not x.get("evidence_complete"): return {"status":"blocked","reason":"intake_not_reviewable"}
        return {"status":"changes_requested" if x.get("blocking_findings") else "merge_candidate"}
    if role == "curator":
        if not x.get("safe_provenance"): return {"status":"blocked","reason":"unsafe_provenance"}
        if not x.get("bounded_claim") or not x.get("owner") or not x.get("contribution_path"): return {"status":"blocked","reason":"ungoverned_claim"}
        return {"status":"accepted" if x.get("adopted") else "proposed"}
    raise KeyError(role)


def main() -> None:
    source = ROOT / "tests/scenarios/seven-role-cases.json"
    suite = json.loads(source.read_text())
    results = []
    failures = []
    roles = set()
    polarity = {}
    for case in suite["cases"]:
        actual = decide(case["role"], case["input"])
        passed = actual == case["expect"]
        results.append({"id":case["id"],"role":case["role"],"expected":case["expect"],"actual":actual,"passed":passed})
        roles.add(case["role"])
        polarity.setdefault(case["role"], set()).add("positive" if case["id"].endswith("positive") else "negative")
        if not passed: failures.append(case["id"])
    if roles != {"capture-refine","design","planner","builder","tester","reviewer","curator"}:
        failures.append("role-coverage")
    if any(v != {"positive","negative"} for v in polarity.values()): failures.append("polarity-coverage")
    report = {"classification":suite["classification"],"actual_agent_execution":False,"cross_model_review":False,"summary":{"cases":len(results),"passed":sum(r["passed"] for r in results),"failed":len(failures)},"results":results}
    out = ROOT / "docs/audit/scenario-results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["summary"], sort_keys=True))
    if failures: raise SystemExit("failed: " + ", ".join(failures))


if __name__ == "__main__":
    main()
