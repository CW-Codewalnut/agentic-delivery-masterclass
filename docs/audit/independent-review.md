# Independent consolidation review

## Review scope

Reviewed the seven canonical roles, routers, supporting skills, prompt renderer, validator, archive builder, README, all 44 legacy supporting skills, and seven legacy role proposals. The published `web/`, `presentation/`, root `roles/`, root `skills/`, and `worked-example/` surfaces were held unchanged.

## Material findings and corrections

1. **The three-skills-per-agent shape was driving the design.** Migration/configuration safety, concurrency testing, and post-decision history had been folded into always-used skills despite having separate triggers, authority gates, and stop conditions. They are separate skills now. Planner, Builder, Tester, and Curator each expose four supporting skills; the other roles remain at three because their merged procedures form one continuous artifact.
2. **Behavioural compression had removed decision-changing detail.** Restored prior-decision conflict handling and enterprise gaps in Capture; action availability, focus restoration, keyboard traps, announcement deduplication, responsive/localisation/motion treatment, component deviation, source read-back, and accidental-drift review in Design; idempotency fingerprints, expected-version semantics, durable/distributed boundaries, executable proof, and operator signals in Planner; secret/mixed-version/recovery safety in Builder; explicit topology limits in Tester; assertion-level deletion attacks and evidence rejection in Reviewer; and mixed-record splitting plus append-only governed history in Curator.
3. **The renderer defeated progressive disclosure.** It always included every supporting skill, omitted the output template, and therefore made the router selection mostly decorative. It now requires explicit repeatable `--skill` selections (or an intentional `--all-skills`) and includes the selected role, router, skills, and template. Invalid cross-role skill names fail closed.
4. **The repository claimed one canonical source while shipping a destructive embedded generator.** `scripts/build_refined_agent_system.py` could delete and recreate `agent-system/`, overwriting direct contributions. It was removed. Canonical files are edited directly and validated.
5. **Fresh-clone onboarding was not fresh-clone safe.** The main verification block invoked a legacy audit requiring an unpublished sibling proposal, and the README asserted a Python floor not demonstrated by the evidence. Ordinary-checkout commands are now separate from the maintainer-only legacy audit; the README claims only Python 3 standard-library use and records tested execution through the delivery receipt.
6. **The opening read like an internal provenance note.** The README now opens with the user value and first runnable command. Snapshot provenance, research attribution, licensing, and audit limitations remain available lower in the document rather than occupying the entry path.

## Manual bounded behaviour probes

These are one independent model's document-guided judgments, not repeated-run or multi-provider benchmark results.

| Case | Skills selected | Observed decision | Behavioural value exercised |
|---|---|---|---|
| A plan adds a nullable column, backfills it, then makes it required while old and new workers coexist. | Planner impact/invariants, delivery slices, migration/rollout, verification/handoff. | The plan must name expand/migrate/contract order, mixed-version compatibility, restartable backfill, abort signals, and the distinction between code rollback and data reversal. It cannot reach `ready_for_build` with unknown consumers or no recovery path. | The migration branch now fires independently instead of being buried in a generic final handoff.
| A cancellation race passes with twelve threads sharing one in-memory store and is described as “exactly once.” | Tester evidence/negative control, adversarial behaviour, concurrency boundaries, defect/handoff. | Evidence may support the one-process/store result only. Multi-worker exclusion, database isolation, crash recovery, publication, delivery, and consumer deduplication remain unassessed. | The topology boundary survives consolidation and blocks production generalisation.
| A learning proposal file exists, but no maintainer decision is supplied. | Curator provenance/classification and proposal; version history is not selected. | Status remains `proposed`; no accepted history event or adoption claim is created. | Separating post-decision history prevents file placement from being mistaken for acceptance.
| A request says only “customers can cancel orders.” | Capture intake/gaps. | Lifecycle eligibility, ownership, retry identity, concurrency, side effects, disclosure, recovery, and applicable privacy/audit concerns remain owned questions; current code or an engineer preference cannot decide Product policy. | Restored gap categories change the questions asked, rather than merely adding documentation detail.
| A review suite is green but checks event count, not payload or persisted idempotency record. | Reviewer revision/acceptance and risk/false-green. | The reviewer applies deletion attacks and marks payload and record persistence unassessed; overall green cannot support those sub-claims. | Restored assertion-level attack behaviour catches a plausible false green.

The probes show that the revised text contains and routes the intended decisions in representative cases. They do **not** establish invocation reliability, output quality across models, or improvement over the legacy prompts.

## Remaining human decisions

- Choose and add the repository's license before redistribution.
- Decide whether the canonical `agent-system/` should replace or feed the unchanged published site/masterclass snapshot.
- Run repeated, blinded model evaluations across representative hosts/providers before claiming behavioural improvement.
- Supply host-specific skill discovery, project context, tools, credentials, and authority boundaries for deployment.
