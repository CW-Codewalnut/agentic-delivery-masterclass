# PRD — customer order cancellation

**Work item:** SHOWCASE-OC-1
**Status:** APPROVED FOR SYNTHETIC EXAMPLE
**Revision:** 1
**Owner:** fictional Order Experience product owner

## Outcome
An owning customer can stop an order before fulfilment begins and can safely retry without creating duplicate cancellation effects.

## Scope
In: customer action, ownership check, lifecycle cutoff, expected-version check, request-key replay, one cancellation event. Out: payment/refund, inventory, notifications, staff override, persistence, APIs, deployment.

## Requirements
- **FR-1 [REQ-1, D1, D2]:** The owning customer may cancel an order in `placed` or `confirmed`.
- **FR-2 [D3]:** An order at `fulfilment_started` or `shipped` remains unchanged and returns `too_late`.
- **FR-3 [D4, D5, D6]:** Exact request replay returns its original result; key misuse conflicts; later intent does not duplicate the event. For an already-cancelled order, `already_cancelled` takes precedence over a stale expected version.
- **FR-4 [D7]:** For an order not already cancelled, a supplied stale expected version returns `version_conflict` without mutation.
- **FR-5 [D8]:** Concurrent valid attempts cause one transition and one event.

## Acceptance criteria
- **AC-1:** Given an owned confirmed order, when its owner cancels at version 1, then status is `cancelled`, version is 2, and one event exists.
- **AC-2:** Given an order owned by someone else, when an actor requests cancellation, then result is `not_owner` and state/events do not change.
- **AC-3:** Given fulfilment has started, when the owner requests cancellation, then result is `too_late` and state/events do not change.
- **AC-4:** Given a completed request, when its exact key and request are retried, then the original result is returned and no additional event exists.
- **AC-5:** Given a used key, when a different request reuses it, then the call reports an idempotency conflict.
- **AC-6:** Given a cancelled order, when a new request key is used, then result is `already_cancelled` and no additional event exists, including when the later request supplies the pre-cancellation expected version.
- **AC-7:** Given an unknown order, cancellation returns `not_found` with no event.
- **AC-8:** Given expected version 99 and actual version 1, cancellation returns `version_conflict` without mutation.
- **AC-9:** Given twelve simultaneous valid attempts, exactly one returns `cancelled`, eleven return `already_cancelled`, one event exists, and version increments once.

## Approval boundary
This approval is fictional metadata for the worked example. It does not authenticate a person or authorize production implementation.
