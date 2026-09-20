# How this system tests its own agents

Two levels test the Capture & Refine agent. They answer different questions, so they stay separate.

| Level | Question it answers | Determinism | Where it runs |
| --- | --- | --- | --- |
| 1. Artifact contract | Could a behavioural test fail on this PRD? | deterministic | the fast suite, on every change |
| 2. Behavioural end to end | Did the agent turn a vague request into a conforming PRD without inventing Product policy? | the agent run is not deterministic; every grader is | an opt-in run, graded by the fast suite |

## Level 1: the PRD acceptance contract

[`scripts/check_prd_contract.py`](../../scripts/check_prd_contract.py) reads one PRD and reports findings. It has two profiles.

- A draft offered for completeness review must satisfy the whole contract.
- A `blocked` draft must name the blocking gap that blocks it, and it is never forced to invent the agreement it is blocked on.

The contract asks one question: could a behavioural test fail on this document? Every finding names the exact place that stops a test being written. The rules are:

- every requirement cites a source identifier;
- every criterion is shaped `Given <state>, when <action>, then <observable outcome>`;
- every positive criterion names at least one negative counterpart, so refusal, boundary, repeat, conflict, and concurrency cannot be skipped;
- every criterion names a public observation point, never internal state;
- every `behavioural_test` criterion appears in the expected-failure list;
- all eight non-functional classes carry a threshold and an owner, or a stated reason for non-applicability;
- the outcome contract names a success metric, a counter-metric, and the instrumentation both need;
- every gap carries an owner and a blocking effect, and a blocking gap holds the status at `blocked`;
- no requirement or criterion names a technology, a schema, or an algorithm.

[`tests/test_prd_contract.py`](../../tests/test_prd_contract.py) proves the checker by seeding one defect at a time into [`tests/fixtures/prd/conforming.md`](../../tests/fixtures/prd/conforming.md). Each mutation asserts that its target text existed exactly once, so a mutation that stopped applying fails loudly instead of passing silently. A coverage test fails when any declared finding code has no negative control.

## Level 2: behavioural end to end

[`scripts/run_capture_e2e.py`](../../scripts/run_capture_e2e.py) grades what the agent produced. It never decides the outcome itself, and no model judges the result.

A case in [`tests/e2e/capture-refine/cases/`](../../tests/e2e/capture-refine/cases/) holds a deliberately vague request and the behaviour expected of the agent. Eleven deterministic graders then read the transcript and the PRD:

`prd_contract`, `prd_status`, `one_question_at_a_time`, `enough_questions`, `does_not_decide_unowned_policy`, `required_gap_topics`, `design_state`, `no_forbidden_claim`, `authority_boundary`, `first_skill`, and `declared_skills`.

The harness needs an execution source and refuses to report a result without one:

```
python3 scripts/run_capture_e2e.py --transcript-dir tests/e2e/capture-refine/recorded
python3 scripts/run_capture_e2e.py --agent-command "<command that runs the agent>"
```

An `--agent-command` receives the case JSON on stdin and must return the transcript JSON on stdout. The results file records which source produced the transcripts, so a recorded run is never reported as a live one. [`tests/e2e/capture-refine/stub_agent.py`](../../tests/e2e/capture-refine/stub_agent.py) replays recorded transcripts, which keeps the command path tested in a suite that makes no model call. It is a replay stub, not a model.

### Running it against a real model

[`scripts/agent_adapters/capture_refine_claude.py`](../../scripts/agent_adapters/capture_refine_claude.py) is a live adapter. It renders the agent's own prompt with `render_agent_prompt.py --all-skills`, gives the model only the evidence the case names in `source_paths`, and calls `claude -p --model <model>`.

```
python3 scripts/run_capture_e2e.py \
  --agent-command "python3 scripts/agent_adapters/capture_refine_claude.py --model haiku"
```

The adapter does transport only. It never repairs the PRD, never rewrites a question, and never supplies a section the model left out; a missing or empty section fails closed. A repairing adapter would make the graders test the adapter instead of the agent. [`tests/test_capture_agent_adapter.py`](../../tests/test_capture_agent_adapter.py) proves that with seven cases and no model call, including one that asserts a malformed PRD passes through unrepaired.

A live run is not deterministic. Two runs of one model can score differently, so a single pass is evidence about one run, never about the model.

[`tests/test_capture_e2e.py`](../../tests/test_capture_e2e.py) proves the graders the same way Level 1 proves the checker: eleven seeded transcript defects, one per grader, plus a coverage test that fails when a grader has no negative control.

## What these tests do not prove

[`scripts/run_scenario_checks.py`](../../scripts/run_scenario_checks.py) simulates the gate decisions in Python. It proves the simulation, not the agent, and it says so in its own output. Level 2 is the honest agent test.

Every Level 2 grader that reads text matches wording, never meaning. A live run raised the permission gap as "data belonging to other users" and scored a miss, because the grader looked for the word "permission". A required topic is now a list of acceptable wordings, which widens the match but does not change its nature. An agent that raises the right gap in wording nobody listed still scores a miss, and an agent that uses the word without raising the gap still scores a pass. Semantic grading needs a judge, and this harness deliberately has none. Read a topic grader as a vocabulary proxy, not as proof.

Level 2 grades artefacts against stated rules. A pass means the PRD satisfied the contract and the agent stayed inside its authority. It does not prove the wording is good, the Product decisions are right, or the behaviour is worth building. Those stay human decisions on an exact revision.
