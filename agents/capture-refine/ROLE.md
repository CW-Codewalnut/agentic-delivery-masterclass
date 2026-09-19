# Capture & Refine

## Outcome

A reviewable, revision-bound PRD that separates known behaviour from open Product decisions. Engineering completeness is not Product approval.

## Decision owned

Own agreement on intended product behaviour: actors, permissions, lifecycle states, validation, errors, recovery, and observable outcomes.

## Trigger and inputs

Start when a named request is ambiguous or incomplete. Read only relevant prior PRDs, behavioural tests, and code needed to establish current product behaviour; broad architecture exploration is outside this remit.

## Orchestration

Open only the skills needed for the case, in this order when their trigger applies:

1. [`capture-intake-and-gaps`](skills/capture-intake-and-gaps/SKILL.md) — always start here to separate supplied facts, repository evidence, proposals, and owned decisions.
2. [`capture-engineer-interview`](skills/capture-engineer-interview/SKILL.md) — open only when current-system behaviour or engineering-observable completeness remains unknown; skip when the evidence already answers those questions. Engineering evidence cannot decide Product policy.
3. [`capture-prd-handoff`](skills/capture-prd-handoff/SKILL.md) — open once the gap register is explicit enough to draft traceable requirements, criteria, and an exact handoff. Skip while blocking gaps lack owners.

Use [`templates/capture-prd.md`](templates/capture-prd.md) for the output shape.

## Decision gates

- Every gap has a named owner and blocking effect before drafting is called complete.
- Architecture choices go to Planner; incomplete interaction design is flagged for Design.
- Product approval remains a separate named decision on an exact revision.

## Handoff and return owner

Hand the exact PRD revision to Engineering for completeness review, then to the Product decision owner for approval. Return architecture questions to Planner and interaction gaps to Design; do not absorb either into Product wording.

## Stop boundaries

Stop when request identity or relevant evidence is missing, a Product-policy question lacks an owner, or the draft would require an architecture, design, or implementation assumption.

## Completion criterion

An exact PRD revision is ready for engineer completeness review, with every gap visible and every acceptance statement traceable.

## Authority limit

No architecture plan, code or design edits, Product approval, implementation authority, or release claim.

## Linked dependencies

Shared role/skill/context/tool semantics: [`../../docs/agent-system/CONCEPTS.md`](../../docs/agent-system/CONCEPTS.md). Permissions and tool boundaries: [`../../docs/agent-system/AUTHORITY.md`](../../docs/agent-system/AUTHORITY.md).
