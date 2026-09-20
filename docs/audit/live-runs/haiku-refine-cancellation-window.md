# Live run: Haiku on `refine-cancellation-window`

**Classification:** one live `claude -p --model haiku` run, graded by the deterministic Level 2 graders. No model judged the result. One run is evidence about one run, never about a model.

**Command:** `scripts/agent_adapters/capture_refine_claude.py --model haiku`
**Prompt:** `render_agent_prompt.py capture-refine --all-skills`, plus the four evidence files the case names in `source_paths`.

## What the agent produced

- Skills opened, in order: `capture-intake-and-gaps`, `capture-grill-and-decide`, `capture-acceptance-contract`, `capture-prd-handoff`. It skipped `capture-engineer-interview`, which is correct: the evidence already answered the engineering-observable questions.
- Six questions, one question mark each, none bundled.
- A complete PRD with every required section, 10 requirements, 22 acceptance criteria, 11 positive and 11 negative, and all eight non-functional classes.

## Contract findings: 18, all real

| Code | Count | What it caught |
| --- | --- | --- |
| `missing_red_entry` | 12 | 22 criteria are marked `behavioural_test`, but the RED list holds only 8 rows. Fourteen criteria carry no expected failure, so they cannot drive a test. |
| `missing_negative_counterpart` | 4 | AC-9 names its counterpart as `all`; AC-21 names `(unique)`. Neither is an identifier. AC-14 and AC-15 are both marked `positive` and paired with each other, but AC-15 is the retry case and is a repeat, not a positive. |
| `unshaped_criterion` | 2 | AC-11 and AC-13 read "Given cancellation request that fails, then order version is unchanged". There is no `when`, and "a request that fails" is not a state. |

## What this run changed in the repository

The run found two defects in the test tooling, not in the agent.

1. **The harness wrote scratch state inside the working tree.** `run_capture_e2e.py` created `.e2e-work/` at the repository root before the loop and assumed it survived an arbitrary agent command. It did not, and the first run died in `contract_findings`. Scratch state now lives in a `tempfile` directory outside the tree. `tests/test_capture_e2e.py` locks the invariant with a probe that fails if any `.e2e*` path exists mid-run.
2. **One hyphen produced fifteen misdiagnosed findings.** The agent wrote `non-blocking` where the template says `non_blocking`. Every gap had a named owner, but the checker reported `unowned_gap` fifteen times and buried the eighteen real findings. Agreed-set values now normalise, and a missing owner is separated from an unrecognised value, so the message names the real fault.

Both defects were reproduced by a failing test before the fix.
