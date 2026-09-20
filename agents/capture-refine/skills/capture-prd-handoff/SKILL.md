---
name: capture-prd-handoff
description: Use when the acceptance contract is complete enough to bind an exact PRD revision and send it for engineer completeness review.
---

# capture-prd-handoff

## Inputs
The acceptance contract, the evidence and gap registers, the interview record, and Product/Design owner identities.

## Procedure
1. Bind the draft to an exact revision identifier, and name the Product owner and the Engineering reviewer.
2. Keep every open decision in the body with its owner and blocking effect. Never move one into a note or an appendix.
3. Compare the UI requirements with the identified design revision, and record `aligned`, `incomplete`, `mismatched`, `absent`, or `not_required` against that revision.
4. Give the exact revision to Engineering and record the outcome: completeness confirmed, changes requested, or blocked.
5. State that Product approval is pending unless it was separately supplied. Completeness is not approval.

## Output
A revision-bound PRD and an engineer completeness receipt naming the exact revision, the reviewer, the outcome, and every retained Product question.

## Stop condition
Stop when a blocking gap has no owner. A material revision invalidates the earlier completeness receipt, so the receipt is reissued against the new revision. End before Product approval or implementation planning.
