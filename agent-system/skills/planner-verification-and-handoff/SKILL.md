---
name: planner-verification-and-handoff
description: Use when a plan needs test, observability, migration, rollout, rollback, and Engineering acceptance.
---

# planner-verification-and-handoff

## Inputs
Impact map, increments, risks, environment/deployment constraints, and Engineering owner.

## Procedure
1. Map each requirement, invariant, and high risk to a check or signal, expected result, and evidence artifact.
2. When data or compatibility changes, define migration order, coexistence window, abort signals, rollback, and reconciliation.
3. Record performance, security, reliability, and operability limits rather than claiming them from unit tests.
4. Issue the exact plan for Engineering review; preserve assumptions and unresolved owners.

## Output
An accepted `ready_for_build`, changes-requested, or blocked handoff bound to PRD, Design, repo scope, and plan revision.

## Stop condition
Engineering acceptance does not grant Builder mutation authority.
