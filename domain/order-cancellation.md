# Order cancellation domain context

**Status:** illustrative, agreed for this showcase only
**Owner:** fictional Order Experience product owner
**Version:** 1.0
**Scope:** customer-initiated cancellation before fulfilment
**Not evidence of:** any named client's policy, implementation, adoption, or production behaviour

## Purpose
This file contains product-specific meaning. The role and skill files contain reusable method. Moving these rules into a generic skill would incorrectly make one fictional product's policy universal.

## Terms
- **Owning customer:** the authenticated customer whose identifier is attached to the order.
- **Placed:** the order has been accepted but not confirmed for fulfilment.
- **Confirmed:** the order is accepted and remains before fulfilment work starts.
- **Fulfilment started:** picking, preparation, or equivalent execution has begun.
- **Cancellation:** a transition that prevents further order fulfilment in this example.
- **Request key:** a caller-generated idempotency key identifying one cancellation intent.
- **Expected version:** an optional last-seen order version used to reject a stale write.

## Lifecycle policy

| Current status | Owner may request cancellation | Outcome |
| --- | --- | --- |
| `placed` | yes | transition to `cancelled` |
| `confirmed` | yes | transition to `cancelled` |
| `fulfilment_started` | no | `too_late`; status unchanged |
| `shipped` | no | `too_late`; status unchanged |
| `cancelled` | no new transition | `already_cancelled`; status unchanged |

Only the owning customer may use this customer route. An unknown order returns `not_found`. This teaching policy uses a distinct `not_owner` result for clarity; a production threat model may intentionally conceal order existence, which would require a new product/security decision.

## Idempotency and concurrency agreement
1. A request key identifies the tuple `(order_id, actor_id, expected_version)`.
2. Retrying the same tuple and key returns the original result and creates no additional event.
3. Reusing a key for a different tuple is a conflict.
4. A new key after cancellation returns `already_cancelled` and creates no additional event, even when it supplies an expected version older than the completed cancellation. This human-visible completed outcome takes precedence over `version_conflict`.
5. If valid requests race, exactly one transition and one `order.cancelled` event occur; other attempts observe `already_cancelled`.
6. Authorization, completed-cancellation, and expected-version checks happen in that precedence order against state inside the same atomic boundary as mutation.

## Observable result codes
`cancelled`, `already_cancelled`, `not_found`, `not_owner`, `too_late`, and `version_conflict`. Callers must branch on codes, not prose.

## Event contract
The example event contains `event_type`, `order_id`, and `resulting_version`. It deliberately excludes payment, personal data, and notification payloads. A production contract would need an event identifier, timestamp, schema version, durable publication state, retention policy, and consumer compatibility review.

## Explicit exclusions and unknowns
- Payment authorization reversal, refund timing, fees, stock release, loyalty effects, tax documents, notifications, and customer support override are outside this implementation.
- No service-level objective or throughput target is claimed.
- No production identity, authorization, database, broker, or deployment is exercised.
- Whether cancellation and payment reversal must share one distributed transaction is unresolved and must be decided for a real product.

## Atomicity caveat
The example stores orders, events, and request-key records in memory under one `RLock`. This is atomic only for threads sharing one store in one process and disappears on restart. A production design normally needs a durable database transaction, a uniqueness constraint over the scoped request key, an expected-version or row-lock strategy, and a transactional outbox or equivalent. Event delivery may be at least once, so consumers still need deduplication.

## Change control
A proposed domain change records owner, rationale, source, effective version, affected criteria, and conflict status. Only the fictional product owner can mark it accepted for this showcase. Generic skills may ask about statuses and races; they must not hard-code these status choices.
