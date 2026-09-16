# Technical plan

**Status:** implemented for teaching example
**Inputs:** PRD revision 1 and design specification

## Invariants
- Only owner can mutate.
- Only `placed`/`confirmed` can transition.
- Mutation increments version once.
- One accepted transition appends one cancellation event.
- Same key and fingerprint replay exactly; different fingerprint conflicts.
- Version and lifecycle checks occur inside the mutation lock.

## Tasks and proof
1. Define typed order statuses, result codes, immutable records, and store. Proof: import through test suite.
2. Implement lock-scoped replay, checks, transition, event append, and result recording. Proof: AC-1–AC-8 tests.
3. Synchronize twelve callers and assert exactly-once state/event invariant. Proof: AC-9.
4. Preserve the historical missing-implementation RED, a reproducible semantic idempotency negative control, and final GREEN. Proof: `evidence/red.txt`, `evidence/semantic-red.txt`, its reproducer, and `evidence/green.txt`.

## Atomic boundary
The in-memory store owns one re-entrant lock. The idempotency lookup, state read, checks, write, event append, and result record execute while holding it. This is deterministic for threads sharing that store.

## Production delta
Replace process memory with a durable transaction; enforce request-key uniqueness in storage; use optimistic version or row locking; write an outbox row in the same transaction; publish and acknowledge separately; make consumers idempotent; test crash points and multi-worker races; add reconciliation and observability.

## Rollback
The example has no deployment or migration. A production rollback must not reverse already accepted cancellations blindly; it would require compatibility and reconciliation planning.
