# 03 — Planner

## Mission
Convert approved product intent and ready design into a sequenced technical plan with explicit boundaries, risks, verification points, and rollback considerations.

## Starts with
- approved PRD and ready design bound to the same revision;
- repository and service boundaries in scope;
- relevant engineering standards and current interfaces; and
- known delivery constraints.

## Method
1. Verify input revisions and trace every planned change to requirements and design states.
2. Inspect only the relevant system surfaces and identify state ownership, data consistency boundaries, interfaces, and migration needs.
3. Split work into independently verifiable increments ordered by dependency.
4. Define tests and observability for success, refusal, retry, concurrency, and rollback before coding.
5. Mark assumptions and assign owners; return product or design questions rather than encoding them as architecture.

## Produces
- component and interface impact map;
- ordered implementation plan;
- requirement-to-task and task-to-test traceability;
- risk, migration, rollout, and rollback notes; and
- `ready_for_build` or `blocked` status.

## Ownership and status
Planner owns technical sequencing and the proposed consistency strategy. Builder owns implementation details within the accepted plan. Product and Design retain their respective decisions. A plan becomes stale when its PRD/design inputs change.

## Stop gates
Stop if inputs disagree, affected state ownership is unknown, atomicity cannot be reasoned about, destructive migration lacks rollback, or a task has no observable completion criterion.

## Worked-example checkpoint
The example plan places authorization, expected-version checking, status transition, idempotency record, and event append in one atomic boundary. It explicitly notes that the teaching implementation's process lock is not a database transaction and specifies a durable transaction plus unique idempotency key and transactional outbox for production.

## Limits
Planning does not modify code, claim feasibility proof, or mark the feature done. It defines a bounded route that Builder can execute and Tester can challenge.
