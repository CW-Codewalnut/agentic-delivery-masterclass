---
name: capture-intake-and-gaps
description: Use when a product request must be checked against relevant prior PRDs, behavioural tests, or current code before drafting requirements.
---

# capture-intake-and-gaps

## Inputs
Request identity and supplied sources; repository access; known Product and Engineering owners.

## Procedure
1. Pin the request and each source separately; label unavailable, stale, or conflicting evidence.
2. Search only for prior decisions, tests, and code that establish current behaviour or reveal a direct dependency.
3. Classify each statement as supplied fact, observed behaviour, proposal, or open decision.
4. List missing actors, permissions, states, validation, failure, recovery, repeated-action, and side-effect decisions with owner and blocking effect.

## Output
An evidence register, prior-decision impact list, and owned gap register.

## Stop condition
Stop when the request identity is missing or evidence conflicts in a way that prevents a truthful draft. Return broad architecture questions to Planner.
