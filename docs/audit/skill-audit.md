# Skill audit findings

## Result

Audited all **51** files: 7 legacy umbrella routers and 44 supporting skills. The source repeated the same long role/context/tool paragraph in **44 supporting skills**. The canonical set absorbs the 7 routing layers into agent-owned ROLE.md files and consolidates 44 supporting files into 25 skills; every source file has an old-to-new mapping.

The count is an outcome, not a target: migration/configuration safety, concurrency testing, and post-decision history remain separate because they have distinct triggers and stop conditions.

This is a document audit. It identifies duplication and weak information hierarchy by inspection; it does not prove model behaviour. Simulated role scenarios are reported separately.

## Decision by file

| Source | Contribution retained | Duplication/no-op finding | Decision | Canonical path |
|---|---|---|---|---|
| `skills/builder/SKILL.md` | routes the builder role across its conditional skills and handoff gate | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/builder/ROLE.md` |
| `skills/builder-authority-baseline-gate/SKILL.md` | pins change authority, base identity, environment, and baseline | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/builder/skills/builder-baseline-and-red/SKILL.md` |
| `skills/builder-criterion-red-proof/SKILL.md` | requires a criterion-level causal RED | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/builder/skills/builder-baseline-and-red/SKILL.md` |
| `skills/builder-deviation-escalation/SKILL.md` | returns material deviations to their decision owner | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/builder/skills/builder-verification-and-deviation/SKILL.md` |
| `skills/builder-migration-config-safety/SKILL.md` | guards authorised migration and configuration changes | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/builder/skills/builder-migration-config-safety/SKILL.md` |
| `skills/builder-scoped-implementation/SKILL.md` | keeps one implementation increment inside accepted scope | repeated generic role/tool boundary; overlapping schema in group of 1 | merge | `agents/builder/skills/builder-bounded-change/SKILL.md` |
| `skills/builder-verification-receipt/SKILL.md` | binds fresh checks to the exact result | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/builder/skills/builder-verification-and-deviation/SKILL.md` |
| `skills/capture-architecture-constraints/SKILL.md` | captures only current-system constraints needed to state product behaviour safely | repeated generic role/tool boundary; overlapping schema in group of 4 | merge | `agents/capture-refine/skills/capture-intake-and-gaps/SKILL.md` |
| `skills/capture-engineer-completeness-handoff/SKILL.md` | binds Engineering completeness to an exact PRD revision | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/capture-refine/skills/capture-prd-handoff/SKILL.md` |
| `skills/capture-engineer-interview/SKILL.md` | records engineering evidence without converting it to Product policy | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/capture-refine/skills/capture-engineer-interview/SKILL.md` |
| `skills/capture-gap-analysis/SKILL.md` | turns missing behaviour into owned product decisions | repeated generic role/tool boundary; overlapping schema in group of 4 | merge | `agents/capture-refine/skills/capture-intake-and-gaps/SKILL.md` |
| `skills/capture-prd-composition/SKILL.md` | writes traceable requirements and acceptance criteria | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/capture-refine/skills/capture-prd-handoff/SKILL.md` |
| `skills/capture-prior-prd-impact/SKILL.md` | finds changed or conflicting prior product decisions | repeated generic role/tool boundary; overlapping schema in group of 4 | merge | `agents/capture-refine/skills/capture-intake-and-gaps/SKILL.md` |
| `skills/capture-refine/SKILL.md` | routes the capture-refine role across its conditional skills and handoff gate | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/capture-refine/ROLE.md` |
| `skills/capture-request-review/SKILL.md` | separates supplied request material from relevant repository evidence | repeated generic role/tool boundary; overlapping schema in group of 4 | merge | `agents/capture-refine/skills/capture-intake-and-gaps/SKILL.md` |
| `skills/curator/SKILL.md` | routes the curator role across its conditional skills and handoff gate | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/curator/ROLE.md` |
| `skills/curator-destination-routing/SKILL.md` | selects one governed home and owner | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/curator/skills/curator-proposal-and-history/SKILL.md` |
| `skills/curator-finding-provenance/SKILL.md` | binds a narrow learning claim to safe immutable evidence | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/curator/skills/curator-provenance-and-classification/SKILL.md` |
| `skills/curator-learning-classification/SKILL.md` | separates skill guidance, repository context, product work, and local detail | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/curator/skills/curator-provenance-and-classification/SKILL.md` |
| `skills/curator-next-use-evaluation/SKILL.md` | requires an observed future use before claiming benefit | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/curator/skills/curator-next-use-evaluation/SKILL.md` |
| `skills/curator-proposal-governance/SKILL.md` | keeps updates proposed until explicit adoption | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/curator/skills/curator-proposal-and-history/SKILL.md` |
| `skills/curator-version-history-maintenance/SKILL.md` | retains accepted, rejected, and superseded history | repeated generic role/tool boundary; overlapping schema in group of 1 | merge | `agents/curator/skills/curator-version-history/SKILL.md` |
| `skills/design/SKILL.md` | routes the design role across its conditional skills and handoff gate | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/design/ROLE.md` |
| `skills/design-accessibility-interaction-spec/SKILL.md` | specifies content, focus, keyboard, announcements, and recovery | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/design/skills/design-state-interaction-spec/SKILL.md` |
| `skills/design-coverage-conflict-review/SKILL.md` | finds uncovered states and Product-policy conflicts | repeated generic role/tool boundary; overlapping schema in group of 3 | merge | `agents/design/skills/design-source-readiness/SKILL.md` |
| `skills/design-input-revision-gate/SKILL.md` | rejects stale, unapproved, mismatched, or unauthorised Design inputs | repeated generic role/tool boundary; overlapping schema in group of 1 | merge | `agents/design/skills/design-input-readiness/SKILL.md` |
| `skills/design-readiness-handoff/SKILL.md` | binds Design readiness to exact Product and Design revisions | repeated generic role/tool boundary; overlapping schema in group of 3 | merge | `agents/design/skills/design-source-readiness/SKILL.md` |
| `skills/design-requirement-state-model/SKILL.md` | maps requirements to visible states and transitions | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/design/skills/design-state-interaction-spec/SKILL.md` |
| `skills/design-source-of-truth-composition/SKILL.md` | separates specification-only output from authorised editable-source mutation | repeated generic role/tool boundary; overlapping schema in group of 3 | merge | `agents/design/skills/design-source-readiness/SKILL.md` |
| `skills/planner/SKILL.md` | routes the planner role across its conditional skills and handoff gate | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/planner/ROLE.md` |
| `skills/planner-engineer-review-handoff/SKILL.md` | binds Engineering acceptance to an exact plan revision | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/planner/skills/planner-verification-and-handoff/SKILL.md` |
| `skills/planner-increment-task-sequencing/SKILL.md` | creates dependency-ordered, independently provable increments | repeated generic role/tool boundary; overlapping schema in group of 1 | merge | `agents/planner/skills/planner-delivery-slices/SKILL.md` |
| `skills/planner-input-alignment-gate/SKILL.md` | aligns Product, Design, repository scope, and owners | repeated generic role/tool boundary; overlapping schema in group of 3 | merge | `agents/planner/skills/planner-impact-and-invariants/SKILL.md` |
| `skills/planner-invariant-consistency-design/SKILL.md` | states invariants and real consistency boundaries | repeated generic role/tool boundary; overlapping schema in group of 3 | merge | `agents/planner/skills/planner-impact-and-invariants/SKILL.md` |
| `skills/planner-migration-rollout-rollback/SKILL.md` | defines compatibility, rollout, abort, rollback, and reconciliation | repeated generic role/tool boundary; overlapping schema in group of 1 | merge | `agents/planner/skills/planner-migration-rollout/SKILL.md` |
| `skills/planner-repository-impact-map/SKILL.md` | maps affected seams, contracts, data, and owners | repeated generic role/tool boundary; overlapping schema in group of 3 | merge | `agents/planner/skills/planner-impact-and-invariants/SKILL.md` |
| `skills/planner-test-observability-plan/SKILL.md` | maps requirements and risks to checks and operator signals | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/planner/skills/planner-verification-and-handoff/SKILL.md` |
| `skills/reviewer/SKILL.md` | routes the reviewer role across its conditional skills and handoff gate | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/reviewer/ROLE.md` |
| `skills/reviewer-acceptance-trace/SKILL.md` | traces criterion sub-claims across intent, implementation, and proof | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/reviewer/skills/reviewer-revision-and-acceptance/SKILL.md` |
| `skills/reviewer-delta-recheck/SKILL.md` | invalidates and reruns evidence after material changes | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/reviewer/skills/reviewer-decision-and-recheck/SKILL.md` |
| `skills/reviewer-false-green-attack/SKILL.md` | asks which defects could leave evidence green | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/reviewer/skills/reviewer-risk-and-false-green/SKILL.md` |
| `skills/reviewer-merge-release-separation/SKILL.md` | separates merge recommendation from release confidence | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/reviewer/skills/reviewer-decision-and-recheck/SKILL.md` |
| `skills/reviewer-revision-evidence-pin/SKILL.md` | pins target bytes, upstream revisions, independence, and cutoff | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/reviewer/skills/reviewer-revision-and-acceptance/SKILL.md` |
| `skills/reviewer-security-consistency-audit/SKILL.md` | reviews authorisation, lifecycle, consistency, and disclosure | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/reviewer/skills/reviewer-risk-and-false-green/SKILL.md` |
| `skills/tester/SKILL.md` | routes the tester role across its conditional skills and handoff gate | repeated generic role/tool boundary; overlapping schema in group of 1 | rewrite | `agents/tester/ROLE.md` |
| `skills/tester-behaviour-side-effect-checks/SKILL.md` | checks outputs, persisted state, side effects, and forbidden mutations | repeated generic role/tool boundary; overlapping schema in group of 1 | merge | `agents/tester/skills/tester-adversarial-behaviour/SKILL.md` |
| `skills/tester-concurrency-boundary-checks/SKILL.md` | tests contention while naming the observed topology boundary | repeated generic role/tool boundary; overlapping schema in group of 1 | merge | `agents/tester/skills/tester-concurrency-boundaries/SKILL.md` |
| `skills/tester-coverage-classification-handoff/SKILL.md` | classifies every claim before Reviewer handoff | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/tester/skills/tester-defect-and-handoff/SKILL.md` |
| `skills/tester-defect-reproduction/SKILL.md` | reduces failures to revision-bound reproducers | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/tester/skills/tester-defect-and-handoff/SKILL.md` |
| `skills/tester-evidence-plan/SKILL.md` | maps claims to observable assertions and limits | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/tester/skills/tester-evidence-and-negative-control/SKILL.md` |
| `skills/tester-negative-control/SKILL.md` | proves the harness detects a semantic defect | repeated generic role/tool boundary; overlapping schema in group of 2 | merge | `agents/tester/skills/tester-evidence-and-negative-control/SKILL.md` |

## What changed

- Each agent owns one folder containing ROLE.md, nested skills, and its template.
- ROLE.md owns skill selection, skips, decision gates, handoffs, return owners, and stop boundaries; the separate router layer was removed.
- Shared semantics remain single-source in `docs/agent-system/CONCEPTS.md` and `AUTHORITY.md`, linked from every role.
- Supporting skills keep trigger, inputs, ordered procedure, checkable output, and stop condition only.
- Closely coupled fragments were merged where using one without the other produced an incomplete artifact.
- Safety gates, revision identity, human authority, negative controls, false-green attacks, and confidence boundaries were retained.

## Limits

The audit does not claim the final prompts outperform the source under live model execution. The repository includes deterministic structural checks and simulated positive/negative gate scenarios; independent content review and model evaluations remain future work.
