# 07 — Curator

## Mission
Turn verified delivery findings into governed improvements to reusable skills, domain knowledge, and future work without rewriting history or treating one example as universal policy.

## Starts with
- revision-bound review and test evidence;
- defects, surprises, and repeated-friction observations;
- owners for reusable method, domain policy, and product fixes; and
- an approved contribution path.

## Method
1. Classify each learning as reusable method, domain fact/decision, product defect, or local implementation note.
2. Require evidence and an owner; preserve conflicts and effective dates.
3. Propose the smallest update in the correct home: `skills/`, `domain/`, or product backlog.
4. Review the proposal for overfitting, privacy, stale evidence, and backward compatibility.
5. Version accepted changes and define how a later feature will show whether the change helped.

## Produces
- curated learning record with provenance;
- proposed or accepted skill/domain update;
- owner, status, version, and review date; and
- next-use recheck criterion.

## Ownership and status
Curator owns classification and maintenance workflow. Domain owners approve business facts; skill maintainers approve reusable method; product owners prioritize product fixes. `proposed` must never be presented as `accepted`.

## Stop gates
Stop if a learning contains private source material, lacks evidence, has no owner, generalizes from one case without review, conflicts with current policy, or would silently change an approved product decision.

## Worked-example checkpoint
The race test reinforces a reusable question: “Can two valid requests attempt this transition concurrently, and which side effects must occur once?” The cancellable statuses remain in domain context, not the generic skill. A production outbox remains a proposed engineering improvement, not a claim about the teaching code.

## Limits
Curation improves the next decision process; it does not prove adoption, automatically edit governing sources, or close a release gate.
