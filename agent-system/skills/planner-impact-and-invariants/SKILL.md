---
name: planner-impact-and-invariants
description: Use when an approved change needs repository impact, reuse, contract, and consistency decisions before tasks are written.
---

# planner-impact-and-invariants

## Inputs
Aligned PRD/Design revisions, authorised repo scope, repo rules, and service/data ownership.

## Procedure
1. Inspect existing seams, contracts, data owners, and similar paths before proposing new structures.
2. Map directly affected components, interfaces, schemas, security boundaries, and operational owners.
3. State invariants and where atomicity, uniqueness, ordering, or idempotency actually hold.
4. Separate verified facts, design choices, risks, and business questions; return business ambiguity.

## Output
An impact map, reuse decision, contract changes, invariants, and stated consistency limits.

## Stop condition
Stop when required repositories are unavailable, input revisions mismatch, or a business rule would be guessed.
