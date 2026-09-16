# Worked example — intake

**Work item:** SHOWCASE-OC-1
**Status:** refined in a prepared, synthetic walkthrough
**Owner:** fictional Order Experience product owner
**Implementation owner:** showcase Builder role
**Evidence class:** illustrative repository artifact; not a live agent run

## Raw request
> Allow customers to cancel an order.

## Known boundary
Customer self-service cancellation only. Staff override, refund execution, payment reversal, inventory release, notification delivery, and deployment are excluded.

## Initial unknowns
Who may cancel; which statuses remain cancellable; what a repeat does; how stale clients behave; what concurrent requests do; and whether cancellation side effects occur once.

## Source register

| ID | Source | Classification | Supports |
| --- | --- | --- | --- |
| REQ-1 | this synthetic intake | requested | customer cancellation outcome |
| DEC-1 | `01-decisions.md` | decided | owner, states, replay, race policy |
| DOM-1 | `../domain/order-cancellation.md` | decided | terms and lifecycle policy |
| TEST-1 | `../tests/test_order_cancellation.py` | observed test artifact | executable assertions |
| IMPL-1 | `order_cancellation.py` | observed implementation artifact | teaching implementation |

Absence of a payment or notification source is recorded as an exclusion/unknown, not evidence that those concerns do not exist.
