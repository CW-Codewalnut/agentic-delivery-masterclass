---
name: capture-acceptance-contract
description: Use when agreed behaviour must become a testable acceptance set and an expected-failure list before any plan, design, or code exists.
---

# capture-acceptance-contract

## Inputs
Agreed behaviour, the decision ledger, the assumption register, the evidence register, and the named threshold owners.

## Procedure
1. Write each requirement as one observable statement with an identifier, and cite the source identifiers that support it.
2. Write each acceptance criterion as `Given <state>, when <action>, then <observable outcome>`. Keep one behaviour in one criterion.
3. Name at least one negative counterpart for every positive criterion: refusal, boundary, repeat, conflict, or concurrency. Record the pairing on both rows.
4. State the observation point for each criterion. Name public behaviour a test can observe, never internal state, a private field, or an implementation detail.
5. Mark each criterion `behavioural_test`, `manual_check`, or `instrumented_metric`, and say which existing evidence already covers it.
6. Derive the expected-failure list. For every `behavioural_test` criterion, state the failure it must show before the change exists. A criterion with no expected failure cannot drive a test.
7. Write one non-functional criterion for each class the output template lists. Give a threshold and an owner, or give a stated reason for non-applicability. A blank is not a reason.
8. Write the outcome contract: the success metric, the counter-metric that would expose harm, and the instrumentation both metrics need.
9. Recheck traceability in both directions. Every criterion cites a requirement, and every requirement carries at least one criterion.

## Output
A traceable requirement set, paired positive and negative acceptance criteria with observation points, an expected-failure list, non-functional criteria with thresholds and owners, and the outcome contract.

## Stop condition
Stop when a criterion has no observable outcome, when a threshold has no owner, or when stating the criterion would require an architecture, design, or implementation choice.
