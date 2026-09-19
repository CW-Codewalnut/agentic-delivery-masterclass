# Delivery report

## Scope delivered

- Started from fetched live `origin/main` at `d819bff2a9443eaae854665f7e24c940450d8172` in a new owned worktree.
- Read the unpublished proposal as source only; did not modify it.
- Audited every source skill: 7 routers and 44 supporting files.
- Replaced 44 repeated role/context/tool paragraphs with one shared concepts document and one authority document.
- Produced 7 concise role contracts, 7 routers, and 21 consolidated supporting skills. No source skill was silently dropped; the 51-entry map resolves every old path to a canonical path.
- Preserved the existing published-site sources and masterclass snapshot unchanged.
- Rewrote the root README around onboarding, conditional handoffs, exact paths, evidence limits, portability, contribution rules, and pinned attribution.
- Built a deterministic review archive and exercised it from a fresh extraction.

## Review paths

- Canonical system: `agent-system/`
- Manifest: `agent-system/manifest.json`
- README: `README.md`
- File-by-file audit: `docs/audit/skill-inventory.json`
- Readable findings: `docs/audit/skill-audit.md`
- Old-to-new map: `docs/audit/legacy-to-canonical.json`
- Scenario cases/results: `tests/scenarios/seven-role-cases.json`, `docs/audit/scenario-results.json`
- Matt Pocock research/attribution: `docs/research/matt-pocock-skills.md`
- Archive: `dist/seven-agent-system.zip`
- Archive receipt and checksum: `docs/audit/archive-receipt.json`, `dist/seven-agent-system.zip.sha256`

## Verification run

| Command | Result |
|---|---|
| `python3 scripts/run_scenario_checks.py` | 14/14 deterministic cases passed; one positive and one refusal/return case per role |
| `python3 scripts/validate_agent_system.py` | 7 roles, 7 routers, 21 supporting skills, 7 templates, 51 legacy mappings, 14 scenarios, 0 errors |
| `python3 scripts/render_agent_prompt.py capture-refine --output /tmp/capture-refine-agent.md` | rendered portable Capture & Refine bundle; 7,679 bytes after final pruning |
| `python3 scripts/build_review_archive.py` | 59-file archive; fresh-extraction validation and Capture render both passed |
| `shasum -a 256 -c seven-agent-system.zip.sha256` from `dist/` | archive checksum passed |
| `python3 -m unittest discover -s tests -v` | 16/16 existing repository tests passed |
| `python3 -m py_compile ...` for all new Python scripts | passed |
| `git diff --check` | passed |
| duplicate-paragraph scan across canonical skills | 0 repeated paragraph groups over 100 characters |
| diff check for `web/`, `presentation/`, `roles/`, `skills/`, `worked-example/` | no changes |

## Evidence classification

- **Actual execution:** structural validator, Markdown-link checks, manifest/orphan checks, renderer, archive checksum/extraction smoke, Python compilation, and existing unit tests.
- **Simulated:** the 14 role scenarios use deterministic policy functions. They exercise the intended gates but are not language-model behaviour evaluations.
- **Static review:** the 51-file contribution and duplication audit.
- **Not performed:** live multi-model agent runs, independent cross-model content review, provider/runtime installation, browser/site rebuild, push, pull request, deployment, or publication.

## Remaining gaps and decisions

1. Independent model evaluation is still needed to establish behavioural improvement over the source prompts; this work does not claim that keyword or structural checks prove model quality.
2. A maintainer must decide whether and how the canonical `agent-system/` replaces or feeds the unchanged published snapshot. The current site exposes seven root skill cards while the revised canonical set contains 7 routers plus 21 supporting skills; a future site sync must reconcile that count and navigation deliberately.
3. The repository did not declare a project license at the audited main revision. Matt Pocock's MIT license covers his source, not this repository; maintainers should add or clarify the project license before redistribution.
4. Host-specific skill discovery, permissions, credentials, and tool schemas remain integration work. The renderer creates a prompt bundle but does not claim runtime registration.
5. Human Product, Design, Engineering, merge, release, and adoption decisions remain outside these artifacts.
