---
name: tester-adversarial-behaviour
description: Use when executing acceptance and risk checks across behaviour, side effects, repeats, failures, and concurrency.
---

# tester-adversarial-behaviour

## Inputs
Evidence plan, restored exact target, stable fixtures, and declared process/store/integration boundary.

## Procedure
1. Exercise success and applicable refusal/error states through public seams.
2. Assert output, persisted state/version, every required side effect, and every forbidden mutation.
3. Exercise exact replay, changed-key repetition, stale state, partial failure, and recovery where relevant.
4. Synchronise concurrency attempts when race behaviour matters; report only the topology actually observed.

## Output
Revision-bound receipts for each case with command, exit, assertions, evidence locator, and topology limit.

## Stop condition
Do not generalise one-process or in-memory results to distributed, durable, or production behaviour.
