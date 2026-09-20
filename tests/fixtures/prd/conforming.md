# Product behaviour agreement

- Revision / source request: SHOWCASE-OC-1 revision 3
- Status: `draft_for_engineer_completeness_review`
- Product owner / Engineering reviewer: fictional Order Experience product owner / fictional staff engineer

## Evidence register

| Source | Identity | State | Supported claim |
| --- | --- | --- | --- |
| REQ-1 | synthetic intake, revision 1 | current | customers ask to stop an order |
| DEC-1 | `worked-example/01-decisions.md` | current | owner, states, replay, and race policy |
| DOM-1 | `domain/order-cancellation.md` | current | lifecycle terms and cutoff policy |
| TEST-1 | `tests/test_order_cancellation.py` | current | executable assertions for the behaviour |

## Intended behaviour

An owning customer stops an order before fulfilment begins. The order moves from `placed` or `confirmed` to `cancelled`. Every other actor is refused. Every attempt after the cutoff is refused. A repeat of the same intent returns the first outcome and adds no second effect. Concurrent valid attempts produce one transition and one event.

## Assumption register

| ID | Assumption | Class | Owner | Effect if wrong |
| --- | --- | --- | --- | --- |
| AS-1 | cancellation emits no payment or refund effect in this scope | decided | product owner | scope grows to payment reversal |
| AS-2 | the order store serialises decision and mutation for one order | engineering_observable | staff engineer | the race criterion cannot hold |
| AS-3 | staff override is out of scope for this revision | owned_open | product owner | a second actor class enters the permission model |

## Requirements

| ID | Observable requirement | Source IDs |
| --- | --- | --- |
| FR-1 | The owning customer cancels an order that is `placed` or `confirmed`. | REQ-1, DEC-1, DOM-1 |
| FR-2 | An order at `fulfilment_started` or `shipped` stays unchanged and reports `too_late`. | DEC-1, DOM-1 |
| FR-3 | A repeat of the same request returns the first outcome and adds no second event. | DEC-1, TEST-1 |
| FR-4 | A stale expected version is refused without any change to the order. | DEC-1, TEST-1 |
| FR-5 | Concurrent valid attempts produce one transition and one event. | DEC-1, TEST-1 |

## Acceptance criteria

| ID | Requirement | Polarity | Given / when / then | Counterpart | Observation point | Check |
| --- | --- | --- | --- | --- | --- | --- |
| AC-1 | FR-1 | positive | Given an owned order at `confirmed` and version 1, when its owner cancels it, then the status is `cancelled`, the version is 2, and one cancellation event exists. | AC-2, AC-3, AC-8 | returned outcome, order status, order version, and event count | behavioural_test |
| AC-2 | FR-1 | negative | Given an order owned by another customer, when an actor asks to cancel it, then the outcome is `not_owner` and the status, version, and event count do not change. | AC-1 | returned outcome, order status, order version, and event count | behavioural_test |
| AC-3 | FR-2 | negative | Given an order at `fulfilment_started`, when its owner asks to cancel it, then the outcome is `too_late` and the status, version, and event count do not change. | AC-1 | returned outcome, order status, order version, and event count | behavioural_test |
| AC-4 | FR-3 | negative | Given a completed cancellation request, when the same request key and body are sent again, then the first outcome is returned and the event count does not change. | AC-1 | returned outcome and event count | behavioural_test |
| AC-5 | FR-3 | negative | Given a used request key, when a different request body reuses that key, then the outcome reports a request-key conflict and the event count does not change. | AC-4 | returned outcome and event count | behavioural_test |
| AC-6 | FR-3 | negative | Given a cancelled order, when a new request key asks to cancel it again, then the outcome is `already_cancelled` and the event count does not change. | AC-9 | returned outcome and event count | behavioural_test |
| AC-7 | FR-1 | negative | Given an order identifier that no order uses, when an actor asks to cancel it, then the outcome is `not_found` and no event exists. | AC-1 | returned outcome and event count | behavioural_test |
| AC-8 | FR-4 | negative | Given an order at version 1, when a request supplies expected version 99, then the outcome is `version_conflict` and the status, version, and event count do not change. | AC-1 | returned outcome, order status, order version, and event count | behavioural_test |
| AC-9 | FR-5 | positive | Given twelve simultaneous valid attempts on one eligible order, when they all run, then one returns `cancelled`, eleven return `already_cancelled`, one event exists, and the version rises once. | AC-6 | returned outcomes, order version, and event count | behavioural_test |

## Non-functional criteria

| Class | Requirement or non-applicability rationale | Threshold | Owner | Check |
| --- | --- | --- | --- | --- |
| security | Only the owning customer changes the order. Every other actor is refused. | 0 successful cancellations by a non-owner | product owner | behavioural_test |
| privacy | The cancellation event carries the order identifier, the actor identifier, and the time. It carries no other customer data. | 0 additional personal fields in the event | product owner | behavioural_test |
| accessibility | not_applicable in this revision. The scope holds no user interface, no rendered state, and no keyboard or screen-reader surface. | not_applicable | design owner | manual_check |
| reliability | One eligible order produces one cancellation transition and one cancellation event. | 1 transition and 1 event per order | staff engineer | behavioural_test |
| operability | Every request returns one named outcome from the agreed outcome set. | 100 percent of requests return a named outcome | staff engineer | behavioural_test |
| auditability | One cancellation event records the actor, the order, and the time, and it is never rewritten. | 1 immutable event per cancelled order | staff engineer | behavioural_test |
| compliance | The cancellation event is retained for the order retention period agreed with the records owner. | retained for the order retention period | records owner | manual_check |
| regional | not_applicable in this revision. The synthetic example runs in one region and stores no cross-border copy. | not_applicable | product owner | manual_check |

## Outcome contract

- Success metric: share of cancellation attempts that return a named outcome, target 100 percent.
- Counter-metric: duplicate cancellation events per cancelled order, target 0.
- Instrumentation: each attempt records the actor, the order, the returned outcome, and the resulting event count.

## RED list

| Check | Expected failure before the change |
| --- | --- |
| AC-1 | the owner cannot cancel; no `cancelled` status and no event appear |
| AC-2 | a non-owner changes the order, so the unchanged-state assertion fails |
| AC-3 | an order after the cutoff still cancels, so the `too_late` assertion fails |
| AC-4 | the repeat creates a second event, so the event-count assertion fails |
| AC-5 | the reused key returns a success, so the conflict assertion fails |
| AC-6 | the second intent creates a second event, so the event-count assertion fails |
| AC-7 | an unknown order returns a success, so the `not_found` assertion fails |
| AC-8 | a stale expected version still mutates, so the unchanged-state assertion fails |
| AC-9 | twelve attempts create more than one event, so the single-event assertion fails |

## Decisions and gaps

| ID | Question | Owner | Blocking effect | Evidence | Decision/status |
| --- | --- | --- | --- | --- | --- |
| GAP-1 | Who executes the refund after a cancellation? | product owner | non_blocking | none yet | open, excluded from this revision |
| GAP-2 | Which notification does the customer receive? | product owner | non_blocking | none yet | open, excluded from this revision |

## Design state

`not_required`; the revision holds no user interface surface, so no design revision is named.

## Engineer completeness

Exact revision SHOWCASE-OC-1 revision 3. Reviewer: fictional staff engineer. Outcome: completeness confirmed. Retained Product questions: GAP-1 and GAP-2. Completeness is not Product approval.
