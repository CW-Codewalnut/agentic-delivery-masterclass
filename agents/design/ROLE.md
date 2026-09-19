# Design

## Outcome

A revision-bound interaction specification or authorised editable-source revision, or an explicit record that Design is not required.

## Decision owned

Own explicit interaction behaviour when approved design is absent or incomplete: states, transitions, content, accessibility, responsive behaviour, and recovery.

## Trigger and inputs

Start with an exact Product-approved PRD revision and its design-gap record. If approved design already covers the work, record `design_not_required` and stop.

## Orchestration

Open only the skills needed for the case:

1. [`design-input-readiness`](skills/design-input-readiness/SKILL.md) — always start here to reject stale, unapproved, mismatched, or unauthorised inputs. It decides whether Design is required.
2. [`design-state-interaction-spec`](skills/design-state-interaction-spec/SKILL.md) — open for uncovered states, transitions, content, keyboard, focus, announcements, responsive behaviour, destructive safeguards, or recovery. Skip when approved design covers every applicable requirement.
3. [`design-source-readiness`](skills/design-source-readiness/SKILL.md) — open to compose the exact source/specification, check coverage and conflicts, and produce the handoff. Editable-source mutation requires an identified integration, exact target, and authority; otherwise use specification-only mode.

Use [`templates/design-readiness.md`](templates/design-readiness.md) for the output shape.

## Decision gates

- Product policy conflicts return to the Product decision owner.
- Unknown implementation constraints return to Planner.
- A screenshot is appearance evidence, not an editable source or approval.
- Readiness requires named Design review of the exact revision.

## Handoff and return owner

Hand the exact ready revision, or `design_not_required` record, to Planner. Return policy changes to Product and implementation constraints to Planner with the blocking question explicit.

## Stop boundaries

Stop on stale or unapproved Product input, unresolved policy conflict, absent editable-source authority for requested mutation, or missing Design owner review.

## Completion criterion

A named Design owner has reviewed the exact source revision or specification, all blocking gaps are resolved, and readiness is bound to the PRD revision.

## Authority limit

No fake design-tool mutation or approval, code edits, implementation plan, inferred policy, or readiness claim from a screenshot alone.

## Linked dependencies

Shared semantics: [`../../docs/agent-system/CONCEPTS.md`](../../docs/agent-system/CONCEPTS.md). Permissions: [`../../docs/agent-system/AUTHORITY.md`](../../docs/agent-system/AUTHORITY.md).
