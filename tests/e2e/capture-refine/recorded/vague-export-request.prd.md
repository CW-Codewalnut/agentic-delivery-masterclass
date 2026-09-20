# Product behaviour agreement

- Revision / source request: none; the request arrived as a chat message with no ticket identity
- Status: `blocked`
- Product owner / Engineering reviewer: not named / not named

## Evidence register

| Source | Identity | State | Supported claim |
| --- | --- | --- | --- |
| REQ-1 | product chat message, no ticket and no revision | missing | some customers ask to take their data out |

## Intended behaviour

Not yet statable. The request names no actor, no record set, no destination, and no lifecycle. Any behaviour written now would be an invented Product decision.

## Assumption register

| ID | Assumption | Class | Owner | Effect if wrong |
| --- | --- | --- | --- | --- |
| AS-1 | the word stuff names records the customer already sees | owned_open | product owner | the record set and the permission model both change |
| AS-2 | a generated export file follows the account retention period | owned_open | records owner | the retention rule and the compliance criterion both change |

## Requirements

| ID | Observable requirement | Source IDs |
| --- | --- | --- |
| FR-1 | A signed-in customer starts an export of a named record set and later collects the result. | REQ-1 |

## Acceptance criteria

| ID | Requirement | Polarity | Given / when / then | Counterpart | Observation point | Check |
| --- | --- | --- | --- | --- | --- | --- |

No criterion can be written while GAP-1 to GAP-4 stay open. A criterion written now would encode an assumption, not an agreement.

## Non-functional criteria

| Class | Requirement or non-applicability rationale | Threshold | Owner | Check |
| --- | --- | --- | --- | --- |

The privacy, compliance, and regional classes all depend on GAP-3, so no threshold is stated yet.

## Outcome contract

- Success metric:
- Counter-metric:
- Instrumentation:

## RED list

| Check | Expected failure before the change |
| --- | --- |

## Decisions and gaps

| ID | Question | Owner | Blocking effect | Evidence | Decision/status |
| --- | --- | --- | --- | --- | --- |
| GAP-1 | Which ticket gives this request a stable identity and revision? | requester | blocking | none | open |
| GAP-2 | Which records does the word stuff name? | product owner | blocking | none | open |
| GAP-3 | Who holds permission to export records that belong to another person? | product owner | blocking | none | open |
| GAP-4 | What retention period applies to a generated export file? | records owner | blocking | none | open |

## Design state

`absent`; no design revision is named and no surface is described.

## Engineer completeness

Not offered. The draft is blocked, so no exact revision goes to completeness review. Completeness is not Product approval.
