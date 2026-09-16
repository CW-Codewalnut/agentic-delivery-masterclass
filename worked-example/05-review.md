# Independent-style review record

**Target:** repository revision and evidence identities recorded in `evidence/`
**Status:** MERGE CANDIDATE FOR EDUCATIONAL USE
**Reviewer stance:** adversarial evidence review, not a live product approval

## Findings
- The PRD criteria map to twelve executable tests and explicit implementation branches, including direct `placed`, `shipped`, and completed-cancellation/stale-version precedence cases.
- The historical import RED only demonstrates detection of a completely missing implementation. The separate semantic negative control mutates exact replay and demonstrates that the idempotency assertion fails; GREEN shows the unmutated implementation passes all twelve behavior tests.
- Ownership, status cutoff, expected version, request replay, key misuse, repeated intent, and a synchronized same-process race are asserted.
- The lock encloses state update, event append, and idempotency record, so the tested one-process invariant is coherent.

## Confidence boundaries
This does not prove database durability, multi-process exclusion, crash recovery, message-broker delivery, consumer deduplication, payment/refund behavior, security posture, performance, deployment, rollback, or production authorization. “Exactly once” here means one event object appended to one in-memory list under one lock, not exactly-once distributed delivery.

## Decision
Suitable as a runnable masterclass example with the above caveats displayed. Not suitable as a production reference architecture without the production delta in `04-plan.md`.
