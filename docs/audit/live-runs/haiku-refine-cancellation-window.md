# Live runs: Haiku on the Capture & Refine cases

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

---

# Second run, and what run-to-run variance looks like

A later run covered both cases. Two facts from it are unaffected by any tooling change, because they come from graders the change did not touch.

- On the **same** case, `refine-cancellation-window`, the agent asked 11 questions. The first run asked 6.
- The same case scored `design_state` as absent in the second run and `not_required` in the first. The second reply gave no value the grader could read.

The second run's own finding count is **not** comparable to the first run's 18. It overlapped a change to the checker, and its reply for that case was lost to a defect in the adapter, so it cannot be re-graded. That defect is fixed: `--save-raw-dir` now writes one file per case, where the single `--save-raw` path let the second case overwrite the first.

## What Haiku held steady on, across both runs and both cases

These are the judgements that matter most, and they did not wobble.

- `prd_status`: `blocked` for the vague request, `draft_for_engineer_completeness_review` for the evidenced one. Correct both times.
- `does_not_decide_unowned_policy`: it never promoted an open Product decision into a requirement.
- `one_question_at_a_time`: no bundled question in any run.
- `first_skill` and `declared_skills`: it entered at `capture-intake-and-gaps` and opened no skill it does not own.
- `no_forbidden_claim`: it never claimed approval or build readiness.

## The vague case, and a third defect it exposed

On `vague-export-request` the agent raised eight blocking gaps and set the status to `blocked`. That is the right shape. It wrote `*unassigned*` as the owner of every one of them.

The checker passed all eight. A placeholder is not an owner, so that was a false green in the checker: the gaps table was syntactically complete and semantically unowned. Owners are now checked against a placeholder list, and the same reply scores 10 findings where it previously scored 2 and passed the ownership rule.

The agent also dropped "Completeness is not Product approval" from that reply, which `authority_boundary` caught. That one is a real agent failure, not a tooling defect.

## Honest limit on all of this

Two runs of one model on two cases is a spot check. It is not a measurement. A claim about whether a smaller model produces similar output needs several runs per model per case and a reported spread per grader. Nothing here supports a claim about Haiku as a model.
