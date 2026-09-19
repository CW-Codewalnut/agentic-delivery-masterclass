---
name: design-state-interaction-spec
description: Use when approved behaviour needs a state-complete, accessible interaction specification.
---

# design-state-interaction-spec

## Inputs
Applicable requirements, current journey, project components, platform/accessibility/localisation constraints.

## Procedure
1. Enumerate entry, loading, empty, confirmation, pending, success, refusal, partial failure, unknown outcome, recovery, and repeated-action states; justify exclusions.
2. For each state define visible copy, available actions, transition guards, focus destination, keyboard path, announcement, and recovery.
3. Map every state and transition back to requirement IDs.
4. Route any newly exposed policy choice to Product instead of selecting copy that decides it.

## Output
A requirement-linked state/transition and interaction contract with explicit non-applicable states.

## Stop condition
Stop when policy determines a transition or disclosure and no approved decision exists.
