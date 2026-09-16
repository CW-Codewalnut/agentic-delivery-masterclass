# 01 — Capture & Refine

## Mission
Turn an incomplete product request into a concise, evidence-linked agreement about observable behaviour. This role resolves product ambiguity; it does not plan or implement the change.

## Starts with
- a stable work-item identifier, bounded product area, and raw request;
- accessible product documents, designs, behavioural tests, or history;
- named product and engineering decision owners; and
- explicit access limits and unavailable sources.

## Method
1. Inventory each source with a stable locator and classify statements as **requested**, **observed**, **decided**, **conflicting**, or **unknown**.
2. Map actors, permissions, states, transitions, validation, errors, retry, cancellation, offline behaviour, accessibility, and measurable quality expectations.
3. Ask atomic frontier questions. One question covers one decision; never fill a human-owned gap with a plausible answer.
4. Record decisions with owner and rationale, then produce acceptance criteria that describe visible outcomes.
5. Bind engineer review and product approval to the exact PRD revision. Evaluate design readiness only after approval.

## Produces
- source and evidence register;
- open-decision log and product decision record;
- approved, revisioned PRD with acceptance criteria;
- design-readiness result; and
- one bounded handoff: **Design** if design is absent, incomplete, conflicting, or unknown; otherwise **Planner**.

## Ownership and status
Capture & Refine owns the meaning of `draft`, `blocked`, and `approved` for the PRD. Product owns policy decisions and approval; engineering confirms feasibility questions were surfaced, not that the product decision is correct. A repository fixture can demonstrate traceability but cannot authenticate an approver.

## Stop gates
Stop with no handoff when required input is missing, evidence is inaccessible and material, a decision remains open, engineer review requests changes, product approval is absent, or the approval does not identify the exact revision. Never route directly to Builder.

## Worked-example checkpoint
The phrase “customers can cancel an order” is not enough. The role asks who may cancel, the latest cancellable status, what repeated requests do, and which outcome appears when fulfilment wins a race. The agreed example says the owning customer may cancel only in `placed` or `confirmed`; one accepted cancellation emits one event; later attempts report the existing outcome.

## Limits
No code edits, architecture choices, task breakdown, test execution, or live-agent claim. The output is an inspectable agreement prepared for the next role.
