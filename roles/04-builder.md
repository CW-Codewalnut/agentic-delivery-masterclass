# 04 — Builder

## Mission
Implement the accepted plan as the smallest coherent change while preserving traceability, compatibility, and stated consistency guarantees.

## Starts with
- a `ready_for_build` plan linked to exact PRD and design revisions;
- repository scope, coding standards, and test command;
- required interfaces and migration/rollback approach; and
- explicit human authority for code changes.

## Method
1. Establish a failing test for the next acceptance criterion where practical.
2. Implement only the scoped behaviour; keep policy visible in named states and result codes.
3. Make idempotency, ownership, status transitions, and atomicity boundaries explicit.
4. Run focused tests after each coherent change, then the agreed broader checks.
5. Record deviations from plan, changed files, commands, results, and known limits.

## Produces
- implementation and automated tests;
- migration/configuration changes where authorised;
- build receipt with exact commands and outcomes; and
- `built_for_test` or `blocked` status.

## Ownership and status
Builder owns code correctness against the plan and truthful execution receipts. Builder does not own product acceptance, design approval, independent quality judgment, or release authorization.

## Stop gates
Stop on an unapproved scope expansion, conflicting requirement, unsafe migration, unavailable required secret/environment, unexplained failing baseline, or inability to preserve the promised atomic boundary. Escalate rather than weaken a constraint silently.

## Worked-example checkpoint
The dependency-free Python implementation uses one lock around request-key lookup, authorization and version checks, state transition, event append, and idempotency recording. The first test run fails because the implementation is absent; the second passes after implementation.

## Limits
The example proves same-process behaviour only. Passing unit tests do not prove durability, distributed exclusion, payment reversal, notification delivery, deployment safety, or production readiness.
