# Traceability and evidence map

**Status:** complete for educational repository scope
**Evidence owner:** Tester role
**Decision owner:** Reviewer role
**Executable target:** `worked-example/order_cancellation.py`

| Criterion | Decision/source | Design | Implementation | Test |
| --- | --- | --- | --- | --- |
| AC-1 owner cancels eligible order; one version/event | D1, D2, D8 | Eligible, Pending, Success | `cancel`, cancellable statuses, locked mutation | `test_owner_can_cancel_before_fulfilment`; direct `placed` branch: `test_owner_can_cancel_placed_order` |
| AC-2 non-owner cannot mutate | D1 | Not owner/not found | `_decide`: `NOT_OWNER` | `test_non_owner_is_refused_without_mutation` |
| AC-3 fulfilment cutoff preserves state | D2, D3 | Too late | `_decide`: `TOO_LATE` | `test_fulfilment_started_is_too_late`; direct `shipped` branch: `test_shipped_is_too_late` |
| AC-4 exact replay returns original result once | D4 | Unknown result/retry | idempotency record lookup | `test_same_idempotency_key_replays_result_without_second_event` |
| AC-5 key cannot identify another request | D5 | not applicable | request fingerprint conflict | `test_reusing_key_for_different_request_is_a_conflict` |
| AC-6 new intent after success is harmless; completed outcome precedes stale version | D6, D7 | Already cancelled | `_decide`: `ALREADY_CANCELLED` before expected-version check | `test_new_key_after_cancellation_reports_existing_outcome`; `test_already_cancelled_precedes_stale_version_for_new_intent` |
| AC-7 unknown order | lifecycle policy | Not owner/not found | `_decide`: `NOT_FOUND` | `test_unknown_order_is_not_found` |
| AC-8 stale version does not mutate | D7 | Version conflict | expected-version check under lock | `test_stale_expected_version_is_rejected` |
| AC-9 one race winner and one event | D8 | Pending/Success | store lock around decision, mutation, event, record | `test_concurrent_requests_emit_exactly_one_cancellation_event` |

## Content contract evidence
`tests/test_content_contract.py` verifies all seven role filenames and order, mandatory role contract sections, seven separate substantive skills with inputs/steps/outputs/stop gates/examples, separate domain policy, and absence of private-name or local-absolute-path markers in public materials.

## RED/GREEN provenance
- `worked-example/evidence/red.txt` retains the historical pre-implementation failure: missing `order_cancellation` module, exit 1. It proves only that the suite detects a completely missing implementation.
- `worked-example/evidence/reproduce_idempotency_negative_control.py` reproducibly mutates exact replay in a disposable copy. `semantic-red.txt` records the resulting focused assertion failure, exit 1, plus SHA-256 identities for the reproducer, unmutated implementation, and behavior tests.
- `worked-example/evidence/green.txt` records the final command result: 16 tests, exit 0; `verification.txt` retains the full output.

The logs are repository-safe transcriptions of command output. The historical RED traceback's machine-specific absolute frame path was replaced with a relative test path; the exception type/message, command, and exit code are unchanged. The semantic reproducer itself emits only a relative frame path.

## Claim boundary
The evidence supports the behavior asserted in one Python 3.9 process. It leaves durability, multiple workers, crash recovery, external side-effect delivery, performance, security assessment, integrations, deployment, rollback, and release readiness unassessed.
