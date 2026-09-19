# Delivery report

## Scope

- Corrected the reviewed source from `237d4eec3547aeaf65a6abc6a0d537aab879a85a` in a new owned worktree and local branch.
- Replaced the split `agent-system/roles` and `agent-system/skills` canonical tree with seven agent-owned folders under `agents/`.
- Preserved `web/`, `presentation/`, root `roles/`, root `skills/`, and `worked-example/` as the unchanged historical compatibility snapshot.
- Did not push, open a pull request, deploy, or publish.

## Structural correction

- Each `agents/<agent>/` now owns `ROLE.md`, nested `skills/<skill>/SKILL.md`, and its template.
- All seven `ROLE.md` files directly orchestrate skill triggers, ordering, skips, decision gates, handoffs, return owners, stop boundaries, and authority limits.
- Removed all seven redundant umbrella router skills and the obsolete `agent-system/` tree without removing any of the 25 substantive supporting skills.
- Kept shared semantics and authority policy once under `docs/agent-system/`, explicitly linked by every role.
- Updated `agents/manifest.json` and all 51 legacy migration mappings: seven old umbrella skills now map to owning `ROLE.md` files; 44 old supporting skills map to the 25 nested canonical skills.

## README and tooling

- README now leads with the conditional workflow and seven GitHub-native agent toggles.
- Each toggle shows ownership links, a Mermaid role-to-skill/template map, and nested readable copies of the actual `ROLE.md` and `SKILL.md` source text.
- `scripts/render_readme_agents.py` deterministically renders only the generated README catalogue from canonical sources; `--check` detects drift and never writes role or skill source.
- Prompt rendering now reads `agents/manifest.json`, includes the orchestrating role plus explicitly selected owned skills and template, and rejects empty, unknown, or cross-agent selections.
- Validation and archive tooling enforce the agent-first inventory and absence of router/workflow duplication.

## Verification

| Command/check | Result |
|---|---|
| `python3 --version` | Python 3.9.6 |
| `python3 scripts/run_scenario_checks.py` | 14/14 deterministic cases passed |
| `python3 scripts/render_readme_agents.py --check` | README matches all 7 roles and 25 skills |
| `python3 scripts/validate_agent_system.py` | 7 agents, 7 roles, 25 skills, 7 templates, 51 mappings, 14 scenarios, 0 errors |
| explicit Planner render | ROLE.md + 3 selected skills + template present; unselected migration skill absent; 10,450 bytes |
| renderer negative controls | empty, cross-agent, and unknown-agent selections all rejected with exit 1 |
| `python3 -m unittest discover -s tests -v` | 21/21 tests passed |
| maintained-script compilation | passed |
| protected compatibility-snapshot diff | no changes under `web/`, `presentation/`, root `roles/`, root `skills/`, or `worked-example/` |
| `python3 scripts/build_review_archive.py` | 58-file archive; fresh extraction validation, README parity, selected render, and both selection rejections passed |
| archive inventory | 7 roles, 25 skills, obsolete `agent-system/` root absent |

## Evidence limits and remaining decisions

- Structural validation, deterministic scenarios, renderer controls, tests, and fresh-extraction checks were executed. They do not establish model quality or invocation reliability.
- Repeated-run and cross-provider model evaluation remains unperformed.
- The historical published site/masterclass snapshot remains a compatibility surface; maintainers still need to decide how it should consume canonical `agents/` content.
- A project license still needs to be chosen before redistribution.
- Host-specific context, tools, credentials, and runtime authority remain deployment concerns.
