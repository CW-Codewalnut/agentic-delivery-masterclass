# Research note: Matt Pocock's skills

Research was pinned to [`mattpocock/skills@c55ee46073ed923f86ce59a5eb3b6d895095d1b7`](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7) on 2026-09-19. The repository declares the [MIT License](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/LICENSE).

Files inspected:

- [`writing-for-agents`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/writing-for-agents/SKILL.md)
- [`grilling`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grilling/SKILL.md)
- [`tdd`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/tdd/SKILL.md)
- [`code-review`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/code-review/SKILL.md)
- [`to-spec`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/to-spec/SKILL.md)
- [`to-tickets`](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/to-tickets/SKILL.md)

## Ideas applied

- Strong trigger descriptions decide when a skill should be opened.
- A skill earns its place by changing behaviour relative to a default response.
- Ordered actions need checkable completion criteria.
- One meaning should have one maintained source; branch-specific detail belongs behind a pointer.
- Tests should observe public behaviour, include meaningful RED, and avoid implementation coupling.
- Delivery tickets should be narrow vertical slices with explicit blocking edges.
- Review should keep intent/spec findings distinct from implementation/standards findings.

## Where each idea now sits

| Source idea | Canonical place in this repository |
| --- | --- |
| A strong trigger decides when a skill opens | every `description` starts with `Use when`, checked by `scripts/validate_agent_system.py` |
| A skill earns its place by changing behaviour | `capture-grill-and-decide` step 6 applies the no-op test to each answer; a skill that changes no requirement, criterion, or gap is discarded |
| Interrogate before accepting | `capture-grill-and-decide` asks one decision-shaped question at a time and never bundles two |
| A spec is testable, unambiguous, and free of implementation | `capture-acceptance-contract`, enforced by `scripts/check_prd_contract.py` |
| Tests observe public behaviour and include a meaningful RED | the `Observation point` and expected-failure rules in the PRD contract, and the seeded-defect suites in `docs/agent-system/TESTING.md` |
| Delivery slices are narrow with explicit blocking edges | `planner-delivery-slices`, fed by paired criteria from `capture-acceptance-contract` |
| Review keeps spec findings apart from implementation findings | `reviewer-revision-and-acceptance` and `reviewer-risk-and-false-green` |

The revised files use those design principles but do not copy source prose, templates, or implementation. Matt Pocock and the `mattpocock/skills` contributors have not reviewed or endorsed this repository. The original source remains under its own MIT license.

No exact “no-op” quotation is attributed here. The source itself contains a section titled **Pruning** that defines its no-op test; the pinned link above is the evidence.
