# One request, conditional handoffs

This is an illustrative trace, not a live agent execution or approval record.

1. **Request:** “Let customers cancel an order.”
2. **Capture & Refine:** inspects only the prior order-state PRD, cancellation tests, and relevant service path. It records eligible states, ownership, repeat requests, race behaviour, disclosure, and side effects as open decisions. Engineering confirms the document is complete; Product separately approves a revision.
3. **Design (conditional):** the approved design shows only the happy path, so Design specifies pending, success, too-late, already-cancelled, conflict, unknown-result, keyboard, focus, announcement, and safe-retry states. Without editable-source authority it emits a specification, not a claimed Figma revision. A Design owner approves the exact specification.
4. **Planner:** reuses the existing order transition seam, defines one-winner and idempotency invariants, identifies the transaction/outbox boundary, and writes vertical slices with checks and rollback. A newly discovered refund-policy ambiguity returns to Product before the plan can be accepted.
5. **Builder:** after a revised accepted plan and explicit repository authority, proves the first criterion red, implements one slice, runs focused and broader checks, and hands Tester an exact result identity. A needed schema change outside scope is returned instead of absorbed.
6. **Tester:** uses an isolated semantic negative control, then challenges ownership, lifecycle refusal, exact replay, changed-key repetition, stale state, partial failure, and synchronised contention. It reports the exact one-process boundary and leaves multi-worker durability unassessed.
7. **Reviewer:** traces intent, implementation, and assertions; attacks event-payload and topology false greens; then recommends `merge_candidate` for the bounded change while keeping deployment and release gaps separate. A human retains merge authority.
8. **Curator:** classifies “exact result identity is required before evidence review” as a skill proposal, keeps cancellable order states in repository context, routes a durable-outbox need to product work, and defines a next-use check. Nothing is called adopted without an owner decision.

The trace loops or skips roles as evidence requires; it is not a seven-step release process.
