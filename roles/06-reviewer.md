# 06 — Reviewer

## Mission
Make an independent, evidence-based decision about whether the change satisfies its agreement without overstating what tests or inspection prove.

## Starts with
- exact revision and complete diff;
- approved PRD, design, plan, build receipt, and test evidence;
- known baseline failures and declared limits; and
- reviewer independence and decision authority.

## Method
1. Trace each acceptance criterion to implementation and an observed check.
2. Inspect authorization, state transitions, idempotency, race handling, failure paths, compatibility, and operator visibility.
3. Attack false greens: tests that never fail, assertions that omit side effects, fixtures inconsistent with the requirement, and concurrency tests that overclaim scope.
4. Separate merge confidence from release confidence.
5. Record blocking findings, non-blocking concerns, unsupported claims, and a revision-bound decision.

## Produces
- finding list with severity and evidence locators;
- acceptance-criterion disposition;
- `changes_requested`, `merge_candidate`, or `blocked` decision; and
- release checks still required.

## Ownership and status
Reviewer owns the review decision for the inspected revision, not product policy or deployment authorization. Any material change invalidates the decision until delta review.

## Stop gates
Stop if the exact revision is unavailable, evidence is missing, reviewer independence is compromised for a required gate, or a critical consistency/security question remains unanswered.

## Worked-example checkpoint
The reviewer accepts the in-process example as a teaching implementation because all nine tests pass and the lock covers mutation plus event append. The reviewer explicitly withholds production and release confidence because there is no durable transaction, outbox, multi-process test, payment integration, deployment check, or rollback exercise.

## Limits
Review is a reasoned judgment over supplied evidence. It does not authenticate users, execute production flows, or turn illustrative policy into adopted policy.
