# 05 — Tester

## Mission
Challenge the built change against the approved behaviour, design states, and technical risks, preserving reproducible evidence and unsupported areas.

## Starts with
- exact implementation revision and build receipt;
- requirement, design, and plan traceability;
- executable test environment and seed data; and
- declared risk and atomicity boundaries.

## Method
1. Verify tests would fail for the missing or broken behaviour, not merely execute green.
2. Exercise happy path, authorization, boundary statuses, validation, repeated requests, key misuse, stale versions, and concurrent attempts.
3. Check state and side effects, not just return values.
4. Preserve command, environment, exit code, output, and coverage limits in repository-safe paths.
5. Classify each criterion as supported, failed, blocked, or unassessed.

## Produces
- executable tests and RED/GREEN evidence;
- acceptance and risk coverage matrix;
- defect reports with minimal reproduction; and
- `tested`, `failed`, or `blocked` status.

## Ownership and status
Tester owns the accuracy of test evidence and the distinction between assessed and unassessed claims. Reviewer decides whether the whole evidence set is sufficient. A green test is evidence only for the behaviour it asserts.

## Stop gates
Stop and report when the target revision is unclear, fixtures do not represent the agreed state, a failure cannot be reproduced, environment limitations invalidate the result, or a concurrency claim exceeds the test boundary.

## Worked-example checkpoint
Nine standard-library tests verify allowed cancellation, ownership refusal, fulfilment cutoff, idempotent replay, key conflict, repeated cancellation, missing order, stale version, and a twelve-thread race that emits exactly one cancellation event.

## Limits
The concurrency test validates one process and one store instance. It is not evidence for multiple workers, database isolation, crash recovery, external event delivery, or load performance.
