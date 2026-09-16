# Presenter cue sheet — 16-scene route

Use alongside `SCRIPT.md`. Scene numbers match `presentation/scene-control-contract.json` and the 16-slide PDF/PPTX. The script is modular: refinement and method explanations are introduced in Acts 1–3, then briefly recalled in Act 4; do not repeat their full wording twice.

## Exact controls
- **Next** / **ArrowRight** / **PageDown** / **Space**: advance one scene.
- **Back** / **ArrowLeft** / **PageUp**: previous scene.
- **Reset** / **Home**: opening scene.
- **Inspect source files** / **F**: source drawer; **Escape** closes it.
- Seven labelled role buttons jump to their scenes; six act buttons jump to their first scene.
- Use native **Tab**, **Shift+Tab**, **Enter** and **Space** for controls. Close the source drawer before slide-navigation shortcuts.

| Scene / deck slide | Show and do | Narration module / land | Recovery |
|---|---|---|---|
| 01 · Faster coding is only the beginning. | Reset. Show the ordinary cancellation request. | Act 1 opening. Faster output is not dependable delivery. | Stay on PDF slide 1. |
| 02 · The request is simple. The behaviour isn’t. | Ask who, when, repeat, failure. Open Capture & Refine role if useful. | Act 1 questions. Do not let implementation choose product policy. | Read the four questions without file navigation. |
| 03 · Turn the request into an agreement. | Inspect source files → intake, decisions, PRD. | Demonstration A from Act 4, introduced here. Prepared decision → observable acceptance. | Open the same files in the repository. |
| 04 · Separate what travels from what belongs here. | Open skill and domain files separately. | Act 3 method/context paragraph. Questions travel; business rules remain product-owned. | Use PDF slide 4 and name the two file paths. |
| 05 · Carry intent through six explicit decisions. | Trace Intent → Build → Prove → Merge → Release → Learn and seven roles. | Act 2. State Design-before-Planner and human gates. | Read role order without clicking. |
| 06 · Four capabilities make the lifecycle dependable. | Name ambiguity reduction, scalable merge confidence, automated release confidence, engineering governance. | Act 3 four capabilities. Distinguish what today's example proves. | Keep capability names exact; shorten examples. |
| 07 · Design makes the behaviour visible before planning the build. | Open Design role/skill and `worked-example/03-design.md`. | Demonstration B. Show refusal and retry experience before tasks. | PDF slide 7. |
| 08 · The plan names the path and the proof. | Open Planner and `worked-example/04-plan.md`. | Demonstration B. Point to one acceptance ID and its test. | README and traceability map. |
| 09 · Build the bounded change — and preserve the agreement. | Open Builder and `worked-example/order_cancellation.py`. | Demonstration B. Local in-memory example, not durable production service. | Do not scroll through dense code; show the contract instead. |
| 10 · Evidence answers a claim — not every possible question. | Open Tester and current evidence; run `python3 -m unittest discover -s tests -v` from checkout. | Demonstration C. Inspect actual result and evidence identity. | If fresh run fails, retain it. Show older captured proof explicitly as older proof. |
| 11 · Why should we trust this change? | Open Reviewer, `worked-example/05-review.md`, traceability. | Demonstration C review + Act 5. No fabricated score or NFR run. | Read one supported claim and one limit. |
| 12 · Ready to merge is not ready to release. | Name production integration, deployment, rollback and operational gates. | Act 5 confidence boundaries. Unassessed is not passed. | Preserve this explanation even when shortening. |
| 13 · One finding can improve three different things. | Open Curator and `worked-example/06-curation.md`; distinguish skill, domain and product changes. | Demonstration D. Maintained learning loop. | Name the three owners and updates without extra navigation. |
| 14 · Scale the method — not uncontrolled access. | Show bounded repositories/data/tools and approvals. | Act 6 governance. Inspection is not deployment authority. | Do not expose any real credentials. |
| 15 · Adopt around one bottleneck, then inspect the result. | Ask audience where changes wait. Name one experiment and success measure. | Act 6 adoption. Measurement is proposed, not a proven productivity result. | Capture the answer for follow-up; no on-stage commitment. |
| 16 · Start with one bottleneck. Improve the next change. | Close and hand back to host. | Act 6 final paragraph. Product + domain + capability improve together. | Reset only after closing. |

## Timing and cut line

Provisional contribution budget: 10 minutes framing, 20 minutes demonstration, 8 minutes confidence and learning, 7 minutes adoption/discussion, **5 minutes contingency**. Exact speech estimate is in `TIMING.md`; measured machine walkthrough is separate in QA. Neither establishes that Ben rehearsed or that the organiser confirmed this slot.

If behind schedule: keep scenes 2–5, 7, 10–13 and 16. Cut optional full-file reading, not the decision boundaries. Use five minutes contingency for a real failure or audience question; never improvise a production demonstration to fill time.
