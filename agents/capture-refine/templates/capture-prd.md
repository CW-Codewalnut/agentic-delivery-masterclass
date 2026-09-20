# Product behaviour agreement

- Revision / source request:
- Status: `draft_for_engineer_completeness_review|blocked`
- Product owner / Engineering reviewer:

## Evidence register

| Source | Identity | State | Supported claim |
| --- | --- | --- | --- |

`State` is `current|stale|missing|conflicting`.

## Intended behaviour

Actors, permissions, states, validation, failures, recovery, repeated actions, concurrency, and side effects.

## Assumption register

| ID | Assumption | Class | Owner | Effect if wrong |
| --- | --- | --- | --- | --- |

`Class` is `decided|owned_open|engineering_observable`. A residual assumption stays visible here; it is never silent.

## Requirements

| ID | Observable requirement | Source IDs |
| --- | --- | --- |

One observable statement per row. No technology, schema, or algorithm.

## Acceptance criteria

| ID | Requirement | Polarity | Given / when / then | Counterpart | Observation point | Check |
| --- | --- | --- | --- | --- | --- | --- |

`Polarity` is `positive|negative`. Every positive criterion names at least one negative counterpart: refusal, boundary, repeat, conflict, or concurrency. `Observation point` names public behaviour a test can observe, never internal state. `Check` is `behavioural_test|manual_check|instrumented_metric`.

## Non-functional criteria

| Class | Requirement or non-applicability rationale | Threshold | Owner | Check |
| --- | --- | --- | --- | --- |

One row for each of `security`, `privacy`, `accessibility`, `reliability`, `operability`, `auditability`, `compliance`, and `regional`. A `not_applicable` threshold needs a stated reason, not a blank.

## Outcome contract

- Success metric:
- Counter-metric:
- Instrumentation:

## RED list

| Check | Expected failure before the change |
| --- | --- |

Every `behavioural_test` criterion appears here with the failure it must show before the change exists.

## Decisions and gaps

| ID | Question | Owner | Blocking effect | Evidence | Decision/status |
| --- | --- | --- | --- | --- | --- |

`Blocking effect` is `blocking|non_blocking`. A blocking gap keeps the status at `blocked`.

## Design state

`aligned|incomplete|mismatched|absent|not_required`; source revision and flags.

## Engineer completeness

Exact revision, reviewer, outcome, retained Product questions. Completeness is not Product approval.
