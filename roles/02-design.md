# 02 — Design

## Mission
Translate an approved product agreement into a reviewable interaction specification covering every relevant user-visible state before implementation planning begins.

## Starts with
- the exact approved PRD revision and its evidence register;
- unresolved design questions explicitly marked as such;
- product design standards and accessibility constraints; and
- a named designer and product decision owner.

## Method
1. Confirm the PRD revision and reject stale or unapproved input.
2. Model the journey from entry point through initial, loading, success, empty, invalid, failure, retry, cancellation, permission-denied, and offline states as applicable.
3. Specify content, interaction, focus order, announcements, destructive-action safeguards, and recovery paths.
4. Link each design decision to a requirement or raise a product question back to Capture & Refine.
5. Conduct design review and record covered states, open gaps, owner, decision, and revision.

## Produces
- state model and interaction notes;
- accessible content and behaviour specification;
- design decision log and coverage matrix; and
- `ready`, `incomplete`, `conflicting`, or `blocked` design status bound to the PRD revision.

## Ownership and status
Design owns interaction intent and design readiness. Product owns any changed policy. Planner may consume only `ready`; `incomplete` or `conflicting` remains with Design or returns to Capture & Refine if product intent changed.

## Stop gates
Stop when the PRD is unapproved or stale, a material product decision is missing, relevant failure/accessibility states are unspecified, or two sources conflict. Do not silently invent policy and do not produce engineering tasks.

## Worked-example checkpoint
For order cancellation, the confirmation explains the cutoff, the pending state disables repeat activation, success announces cancellation, `too_late` preserves the order and points to fulfilment help, and an unknown outcome permits a safe retry with the same request key.

## Limits
A design-ready decision is not implementation approval, test evidence, or proof that the interface works. It is a version-bound design contract handed to Planner.
