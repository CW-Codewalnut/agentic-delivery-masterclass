# From request to confidence — seven-role showcase

A generic, client-safe masterclass content pack showing how one ambiguous order-cancellation request moves through **Capture & Refine → Design → Planner → Builder → Tester → Reviewer → Curator**.

## What is real
The Markdown files and Python implementation are complete repository artifacts. The unit tests execute with Python's standard library. RED and GREEN logs were captured from actual commands and are retained under `worked-example/evidence/`.

## What is illustrative
The order policy, owners, approvals, design decision, role handoffs, and review narrative are synthetic teaching material. They are not live autonomous-agent runs, client policy, human authentication, production adoption, or release evidence.

## Explore
- `roles/` — responsibilities, inputs, outputs, ownership, status, stop gates, and limits for all seven roles.
- `skills/` — portable methods; one substantive skill per role.
- `domain/order-cancellation.md` — fictional business policy kept separate from reusable method.
- `worked-example/` — intake through curation, runnable code, and execution evidence.
- `tests/` — twelve behavior and race tests.
- `docs/worked-example.md` — route and command.
- `docs/traceability.md` — requirement-to-artifact and evidence map.

## Reproduce, build, and verify

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci
npx playwright install chromium
.venv/bin/python scripts/build_experience.py
.venv/bin/python scripts/verify_source_parity.py --source-root .
python3 -m unittest discover -s tests -v
npm test
.venv/bin/python scripts/render_pdf_qa.py presentation/Masterclass-Experience.pdf
```

The content example itself uses only Python's standard library. Deck generation and QA require Python 3, LibreOffice (`soffice`), Node.js/npm, Chromium for Playwright, and the pinned Python/npm dependencies above. The build writes the offline experience to `web/index.html`, the deck to `presentation/`, and self-contained relative downloads to `web/downloads/`.

## Atomicity and idempotency boundary
The example's lock makes request-key lookup, state mutation, event append, and result recording atomic only for threads sharing one in-memory store. It does not survive restart or coordinate multiple processes. A production design needs durable uniqueness, transaction boundaries, outbox/delivery handling, consumer deduplication, crash testing, and reconciliation.

## Confidence statement
Passing tests support the specific in-process assertions in the test file. They do not support claims about production security, durability, payments, distributed delivery, deployment, rollback, service levels, or release readiness.
