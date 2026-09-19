---
name: reviewer-risk-and-false-green
description: Use when review evidence must be challenged for security, consistency, lifecycle, and false-green gaps.
---

# reviewer-risk-and-false-green

## Inputs
Acceptance trace, diff, tests, negative-control evidence, topology, and risk boundaries.

## Procedure
1. Inspect authorisation, disclosure, state transitions, stale writes, idempotency, event/state consistency, and relevant failure recovery.
2. Ask what implementation, payload, state, or topology defect could remain while the suite stays green.
3. Check whether the negative control failed at the intended assertion and whether fresh GREEN used the restored exact target.
4. Write findings with locator, consequence, remediation, owner path, and recheck condition.

## Output
A risk finding set and unsupported-claim list, with hard evidence separated from judgment calls.

## Stop condition
Do not convert missing proof into an implementation defect; label it unassessed or blocked as appropriate.
