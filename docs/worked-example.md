# Worked example guide

The repository follows one synthetic request through all seven roles in the required order:

1. Capture & Refine: `worked-example/00-intake.md`, `01-decisions.md`, `02-prd.md`
2. Design: `worked-example/03-design.md`
3. Planner: `worked-example/04-plan.md`
4. Builder: `worked-example/order_cancellation.py`
5. Tester: `tests/test_order_cancellation.py`, `worked-example/evidence/`
6. Reviewer: `worked-example/05-review.md`
7. Curator: `worked-example/06-curation.md`

Run from repository root:

```sh
python3 -m unittest discover -s tests -v
```

Reproduce the expected semantic RED without editing the repository:

```sh
python3 worked-example/evidence/reproduce_idempotency_negative_control.py
```

That command exits 1 because its disposable mutation removes exact-result replay; `worked-example/evidence/semantic-red.txt` binds the retained result to SHA-256 proof identities. The older `red.txt` remains a separate historical missing-implementation receipt.

The example uses only the Python standard library. It is a prepared, inspectable walkthrough—not a recording of autonomous agents. Read `domain/order-cancellation.md` before interpreting statuses, idempotency, or atomicity. The implementation demonstrates one-process behavior and deliberately documents the production delta.
