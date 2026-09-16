# Design specification — cancellation states

**Status:** ready for synthetic example
**Bound to:** SHOWCASE-OC-1 PRD revision 1
**Owner:** showcase Design role

| State | Visible behaviour | Action/focus/accessibility |
| --- | --- | --- |
| Eligible | “Cancel order” available to owner. | Button is keyboard reachable and named with order context. |
| Confirm | Explain cancellation cutoff and consequence. | Initial focus on heading; Cancel and Keep order are distinct. |
| Pending | “Cancelling order…” | Disable repeat activation; announce polite progress. |
| Success | “Order cancelled.” | Focus status heading; announce success once. |
| Too late | “Fulfilment has started; this order can no longer be cancelled.” | Preserve order; offer fulfilment help route. |
| Already cancelled | “This order is already cancelled.” This completed outcome is shown instead of a stale-version warning. | No destructive action; show current status. |
| Not owner/not found | The teaching harness exposes typed codes, not customer copy. | Production disclosure policy remains unresolved. |
| Version conflict | “Order changed. Refresh and review its current status.” | Focus message, offer refresh. |
| Unknown transport result | “We could not confirm the result. Retry is safe.” | Retry reuses the same request key. |

## Readiness decision
The states needed by the executable example are represented. Payment/refund, offline persistence, responsive visuals, localization, and production error-disclosure copy are excluded, so this is not production design readiness.
