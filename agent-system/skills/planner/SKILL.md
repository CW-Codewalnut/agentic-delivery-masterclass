---
name: planner
description: Use when approved behaviour needs an architecture, risk, slicing, and proof plan before implementation.
---

# Planner router

## Inputs
Read the role contract at [`../../roles/planner.md`](../../roles/planner.md) and the exact work artifacts it requires.

## Route
1. Open `planner-impact-and-invariants` before selecting implementation structure.
2. Open `planner-delivery-slices` after contracts and boundaries are known.
3. Open `planner-migration-rollout` only when data, interfaces, configuration, deployment order, or rollback behaviour changes.
4. Open `planner-verification-and-handoff` for proof, observability, and Engineering review.

## Output
Return business or interaction ambiguity; finish with accepted ready_for_build or blocked.
