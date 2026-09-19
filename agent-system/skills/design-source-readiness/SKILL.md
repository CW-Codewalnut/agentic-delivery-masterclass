---
name: design-source-readiness
description: Use when composing design changes, reviewing coverage, and preparing the exact Design handoff.
---

# design-source-readiness

## Inputs
Input-gate record, interaction specification, identified source or specification-only mode, and review owners.

## Procedure
1. In specification-only mode, write frame/component changes and do not imply a design file changed.
2. In editable mode, mutate only the pinned authorised source and record the resulting revision.
3. Compare every requirement and state against the produced artifact; record gaps and conflicts.
4. Collect human Design review for the exact revision and Product review for any policy change.

## Output
A readiness record: ready, incomplete, conflicting, blocked, or design-not-required, all bound to exact revisions.

## Stop condition
A screenshot cannot satisfy editable-source identity. Only ready or design-not-required output may enter planning.
