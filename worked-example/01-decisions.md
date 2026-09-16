# Capture & Refine decision record

**Status:** agreed for synthetic example
**Decision owner:** fictional Order Experience product owner
**Engineer reviewer:** showcase engineering role
**Applies to:** SHOWCASE-OC-1 revision 1

| ID | Atomic question | Decision | Why it matters |
| --- | --- | --- | --- |
| D1 | Who may use this route? | Only the owning customer. | Prevents one customer changing another's order. |
| D2 | Which states are cancellable? | `placed` and `confirmed`. | Defines the fulfilment cutoff. |
| D3 | What happens after fulfilment starts? | Return `too_late`; preserve status. | Makes the race outcome visible and safe. |
| D4 | What does exact retry do? | Return the original result; no second event. | Supports retry after an unknown response. |
| D5 | Can one key identify different requests? | No; raise an idempotency conflict. | Prevents accidental result aliasing. |
| D6 | What does a new key do after cancellation? | Return `already_cancelled`; no second event, even if that later intent supplies a stale expected version. | Keeps the completed, human-visible outcome authoritative and repeated intent harmless. |
| D7 | How is a stale client handled? | For an order not already cancelled, an optional expected version mismatch returns `version_conflict`. | Prevents mutation from stale state while preserving D6 precedence. |
| D8 | What if valid requests race? | Exactly one transition and one cancellation event. | Defines the atomicity invariant. |

## Open product decisions excluded from build
Refund timing, payment reversal, stock release, customer notification, support override, privacy-preserving error disclosure, and production service levels. A real feature cannot claim end-to-end cancellation until owners decide these matters.
