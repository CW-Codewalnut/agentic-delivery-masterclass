#!/usr/bin/env python3
"""Build the canonical seven-agent skill system from reviewed definitions."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "agent-system"

ROLES = {
    "capture-refine": {
        "title": "Capture & Refine",
        "decision": "Own agreement on intended product behaviour: actors, permissions, lifecycle states, validation, errors, recovery, and observable outcomes.",
        "starts": "A named request plus only relevant prior PRDs, behavioural tests, and code needed to establish current product behaviour. Broad architecture exploration is outside this remit.",
        "does": [
            "Separate supplied facts, repository evidence, proposed behaviour, and open product decisions.",
            "Ask the engineer focused questions about completeness and current behaviour; retain answers as engineering evidence, not product policy.",
            "Produce acceptance criteria and a decision register with owners and blocking effect.",
        ],
        "returns": "Architecture choices go to Planner. Missing product policy goes to the Product decision owner. Missing or incomplete interaction design is flagged for Design rather than repaired here.",
        "complete": "An exact PRD revision is ready for engineer completeness review, with every gap visible. Engineer completeness means the document is reviewable; it is not Product approval.",
        "never": "No architecture plan, code or design edits, product approval, implementation authority, or release claim.",
        "skills": ["capture-intake-and-gaps", "capture-engineer-interview", "capture-prd-handoff"],
    },
    "design": {
        "title": "Design",
        "decision": "Own explicit interaction behaviour when approved design is absent or incomplete: states, transitions, content, accessibility, responsive behaviour, and recovery.",
        "starts": "An exact product-approved PRD revision and its design-gap record. If approved design already covers the work, record that Design is not required and stop.",
        "does": [
            "Map each applicable requirement to visible states and transitions; explain non-applicability.",
            "Specify actions, copy, focus, keyboard, announcements, destructive safeguards, and recovery.",
            "Edit an identified design source only when an authorised integration and exact target are supplied; otherwise produce an honest specification-only artifact.",
        ],
        "returns": "Policy changes return to Product. Unknown implementation constraints return to Planner. A screenshot is evidence of appearance, not an editable source or approval.",
        "complete": "A named Design owner has reviewed the exact source revision or specification, all blocking gaps are resolved, and the readiness record is bound to the PRD revision.",
        "never": "No fake Figma mutation or approval, code edits, implementation plan, inferred policy, or readiness claim from a screenshot alone.",
        "skills": ["design-input-readiness", "design-state-interaction-spec", "design-source-readiness"],
    },
    "planner": {
        "title": "Planner",
        "decision": "Own the implementation approach: architecture and reuse, contracts, data and consistency, migration, risk, delivery slices, observability, and proof.",
        "starts": "Matching approved product and ready Design revisions, or an explicit record that Design is not required, plus the authorised repository/service scope.",
        "does": [
            "Inspect current interfaces and reuse points before proposing new ones.",
            "Define invariants, consistency boundaries, compatibility, rollback, and operational limits.",
            "Sequence independently provable vertical increments, each with dependencies and evidence.",
        ],
        "returns": "Business ambiguity returns to Product; interaction ambiguity returns to Design. Neither becomes an architectural assumption.",
        "complete": "Engineering accepts the exact plan revision and its assumptions. The handoff names changed surfaces, risks, checks, rollback, and any remaining blocker.",
        "never": "Read-only planning: no source, migration, configuration, infrastructure, approval, or deployment mutation.",
        "skills": ["planner-impact-and-invariants", "planner-delivery-slices", "planner-verification-and-handoff"],
    },
    "builder": {
        "title": "Builder",
        "decision": "Own faithful implementation of one accepted, authorised scope and the exact identity of the resulting change.",
        "starts": "A revision-bound accepted plan, explicit repository/change authority, base revision, repository rules, proof commands, and known baseline failures.",
        "does": [
            "Establish a criterion-level causal RED before implementation where the seam permits it.",
            "Implement the smallest coherent increment and use test feedback to drive the next step.",
            "Record the exact diff, fresh checks, baseline failures, and every deviation.",
        ],
        "returns": "Any scope, policy, Design, invariant, migration, or authority deviation returns to its owner before work continues.",
        "complete": "The authorised increment has an exact result identity, causal evidence, fresh verification, and a truthful Tester handoff.",
        "never": "No self-approval, expectation changes merely to obtain green, scope expansion, merge, deployment, or release.",
        "skills": ["builder-baseline-and-red", "builder-bounded-change", "builder-verification-and-deviation"],
    },
    "tester": {
        "title": "Tester",
        "decision": "Own independent, adversarial evidence about whether one exact implementation satisfies approved acceptance within a declared environment boundary.",
        "starts": "Canonical criteria and risks plus a Builder receipt that identifies exact target bytes, environment, commands, fixtures, and baseline failures.",
        "does": [
            "Plan observable assertions and a meaningful negative control before treating green as evidence.",
            "Exercise success, refusal, repeated-action, side-effect, concurrency, and failure boundaries where applicable.",
            "Bind every supported, failed, blocked, or unassessed claim to exact evidence.",
        ],
        "returns": "Unknown expected behaviour returns to its decision owner. Tester does not rewrite the expectation or fixture policy to make a test pass.",
        "complete": "Reviewer receives reproducible commands, exact target/environment identity, defects, coverage classifications, and confidence limits.",
        "never": "No implementation repair without separate Builder authority, approval, merge, deployment, release, or production generalisation.",
        "skills": ["tester-evidence-and-negative-control", "tester-adversarial-behaviour", "tester-defect-and-handoff"],
    },
    "reviewer": {
        "title": "Reviewer",
        "decision": "Own the judgment that approved intent, implementation, and proof are mutually consistent and sufficient for a bounded recommendation.",
        "starts": "One exact result identity, complete diff, matching upstream revisions, Builder receipt, Tester evidence, reviewer identity, independence disclosure, and evidence cutoff.",
        "does": [
            "Trace every criterion sub-claim across intent, implementation, and observed assertions.",
            "Attack false greens and inspect security, consistency, lifecycle, and disclosure risks.",
            "Separate merge recommendation from release confidence and invalidate stale decisions after material deltas.",
        ],
        "returns": "Unknown policy, Design intent, or accepted risk returns to the named human owner; it is not silently resolved in review.",
        "complete": "The exact revision has a finding set, unsupported-claim list, recheck conditions, and `changes_requested`, `merge_candidate`, or `blocked` recommendation.",
        "never": "A recommendation is not merge authority. No merge, deployment, release, publication, or risk acceptance.",
        "skills": ["reviewer-revision-and-acceptance", "reviewer-risk-and-false-green", "reviewer-decision-and-recheck"],
    },
    "curator": {
        "title": "Curator",
        "decision": "Own governed learning from proven evidence: decide whether a finding belongs in a skill, repository context, product backlog, or nowhere.",
        "starts": "Revision-bound review evidence, provenance and confidentiality, current destination versions, known conflicts, and a named adoption authority.",
        "does": [
            "Bound the claim, preserve counterexamples, and exclude private or unsupported material.",
            "Route skill guidance separately from repository-specific context and one-off implementation detail.",
            "Prepare the smallest versioned proposal and define a next-use evaluation before claiming benefit.",
        ],
        "returns": "Disputed meaning, unsafe provenance, or unknown adoption authority returns to its owner. Proposals remain proposals until explicitly accepted.",
        "complete": "The record has one governed destination, evidence, version, owner decision state, retained history, and an evaluation trigger.",
        "never": "No autonomous publication, history rewriting, universal claim from one case, product prioritisation, or adoption claim from file placement.",
        "skills": ["curator-provenance-and-classification", "curator-proposal-and-history", "curator-next-use-evaluation"],
    },
}

SUPPORT = {
"capture-intake-and-gaps": ("Use when a product request must be checked against relevant prior PRDs, behavioural tests, or current code before drafting requirements.", "Request identity and supplied sources; repository access; known Product and Engineering owners.", ["Pin the request and each source separately; label unavailable, stale, or conflicting evidence.", "Search only for prior decisions, tests, and code that establish current behaviour or reveal a direct dependency.", "Classify each statement as supplied fact, observed behaviour, proposal, or open decision.", "List missing actors, permissions, states, validation, failure, recovery, repeated-action, and side-effect decisions with owner and blocking effect."], "An evidence register, prior-decision impact list, and owned gap register.", "Stop when the request identity is missing or evidence conflicts in a way that prevents a truthful draft. Return broad architecture questions to Planner."),
"capture-engineer-interview": ("Use when the gap register contains engineering-observable questions needed for PRD completeness.", "Gap register, inspected evidence, and a named engineer.", ["Ask one decision-shaped question at a time, starting with blockers.", "Record the answer, rationale, cited evidence, confidence, and follow-up verbatim enough to audit.", "Classify an answer as current-system evidence, feasibility input, proposal, or product-policy question.", "Recheck affected gaps after each material answer; never promote engineering preference to approved product behaviour."], "An ordered interview record and updated gap register.", "Stop when the next answer requires Product policy, Design intent, or repository evidence not yet inspected."),
"capture-prd-handoff": ("Use when evidence and interviews are ready to become a revision-bound PRD for engineer completeness review.", "Evidence register, gap register, interview record, and Product/Design owner identities.", ["Write observable requirements and stable acceptance criteria without prescribing architecture.", "Map each criterion to existing evidence, a needed behavioural check, or an explicit manual check.", "Keep open decisions in the body with owner and blocking effect; do not hide them in notes.", "Compare UI requirements with the identified design revision and record absent, incomplete, mismatched, aligned, or not-required status.", "Give the exact revision to Engineering; record completeness confirmed, changes requested, or blocked."], "A revision-bound PRD and engineer completeness receipt that explicitly says Product approval is pending unless separately supplied.", "A material revision invalidates the earlier completeness receipt. End before Product approval or implementation planning."),
"design-input-readiness": ("Use when deciding whether Design work is required and whether its approved product inputs are current enough to begin.", "Exact approved PRD, design-gap register, source identity if any, and named Design/Product owners.", ["Verify PRD approval identity and revision match.", "Classify existing design as complete, incomplete, conflicting, absent, or not required with rationale.", "Resolve whether the task is specification-only or authorised editable-source work; pin target and permission for the latter.", "List unresolved policy decisions and mark blocking effect."], "A start, no-design-needed, or blocked decision bound to exact revisions and capability mode.", "Stop on unapproved/stale Product input, blocking policy, unknown owner, conflicting source revisions, or requested mutation without exact target and authority."),
"design-state-interaction-spec": ("Use when approved behaviour needs a state-complete, accessible interaction specification.", "Applicable requirements, current journey, project components, platform/accessibility/localisation constraints.", ["Enumerate entry, loading, empty, confirmation, pending, success, refusal, partial failure, unknown outcome, recovery, and repeated-action states; justify exclusions.", "For each state define visible copy, available actions, transition guards, focus destination, keyboard path, announcement, and recovery.", "Map every state and transition back to requirement IDs.", "Route any newly exposed policy choice to Product instead of selecting copy that decides it."], "A requirement-linked state/transition and interaction contract with explicit non-applicable states.", "Stop when policy determines a transition or disclosure and no approved decision exists."),
"design-source-readiness": ("Use when composing design changes, reviewing coverage, and preparing the exact Design handoff.", "Input-gate record, interaction specification, identified source or specification-only mode, and review owners.", ["In specification-only mode, write frame/component changes and do not imply a design file changed.", "In editable mode, mutate only the pinned authorised source and record the resulting revision.", "Compare every requirement and state against the produced artifact; record gaps and conflicts.", "Collect human Design review for the exact revision and Product review for any policy change."], "A readiness record: ready, incomplete, conflicting, blocked, or design-not-required, all bound to exact revisions.", "A screenshot cannot satisfy editable-source identity. Only ready or design-not-required output may enter planning."),
"planner-impact-and-invariants": ("Use when an approved change needs repository impact, reuse, contract, and consistency decisions before tasks are written.", "Aligned PRD/Design revisions, authorised repo scope, repo rules, and service/data ownership.", ["Inspect existing seams, contracts, data owners, and similar paths before proposing new structures.", "Map directly affected components, interfaces, schemas, security boundaries, and operational owners.", "State invariants and where atomicity, uniqueness, ordering, or idempotency actually hold.", "Separate verified facts, design choices, risks, and business questions; return business ambiguity."], "An impact map, reuse decision, contract changes, invariants, and stated consistency limits.", "Stop when required repositories are unavailable, input revisions mismatch, or a business rule would be guessed."),
"planner-delivery-slices": ("Use when a technical approach must become dependency-ordered, independently provable implementation increments.", "Impact/invariant record, accepted scope, and delivery constraints.", ["Prefer narrow vertical slices that cross needed layers and produce observable behaviour.", "Give each slice blockers, changed surfaces, owner, criterion links, pre-proof or RED, GREEN proof, and safe stop.", "Use expand-migrate-contract for wide compatibility changes that cannot land as one green slice.", "Keep Product or Design decisions outside technical tasks and route them back."], "A dependency graph of reviewable increments sized for one bounded implementation context.", "Stop when a slice cannot be verified independently and no explicit integration boundary is accepted."),
"planner-verification-and-handoff": ("Use when a plan needs test, observability, migration, rollout, rollback, and Engineering acceptance.", "Impact map, increments, risks, environment/deployment constraints, and Engineering owner.", ["Map each requirement, invariant, and high risk to a check or signal, expected result, and evidence artifact.", "When data or compatibility changes, define migration order, coexistence window, abort signals, rollback, and reconciliation.", "Record performance, security, reliability, and operability limits rather than claiming them from unit tests.", "Issue the exact plan for Engineering review; preserve assumptions and unresolved owners."], "An accepted `ready_for_build`, changes-requested, or blocked handoff bound to PRD, Design, repo scope, and plan revision.", "Engineering acceptance does not grant Builder mutation authority."),
"builder-baseline-and-red": ("Use when starting an authorised implementation increment and proving the target behaviour is not already satisfied.", "Accepted plan, explicit change authority, base revision, repository rules, criterion, environment, and proof seam.", ["Verify authority covers every intended code, test, migration, and configuration surface.", "Run baseline checks and separate pre-existing failures from the criterion.", "Write or select one public-seam check for the criterion; run it before implementation.", "Accept RED only when it fails for the intended missing or wrong behaviour, not import, syntax, harness, or unrelated failure."], "A pinned baseline and causal RED receipt with command, exit, failure, target, and criterion.", "Stop on missing authority, dirty/unknown base, unusable environment, unrelated RED, or already-green criterion that lacks an explained evidence path."),
"builder-bounded-change": ("Use when implementing one approved increment from a causal RED or equivalent agreed pre-proof.", "Pinned baseline/RED receipt, one plan increment, and repository instructions.", ["Change only surfaces named by the increment and authority.", "Implement only enough to satisfy the criterion and preserve accepted invariants.", "Run the focused check after each coherent change; use the failure to choose the next edit.", "Record any newly required scope, policy, Design, contract, migration, or configuration change as a deviation instead of absorbing it."], "A minimal diff for one increment, focused GREEN, and an exact deviation list.", "Stop before any change outside authority or accepted plan. Do not weaken the expectation merely to obtain green."),
"builder-verification-and-deviation": ("Use when an increment is green and needs exact verification, deviation handling, and Tester intake.", "Exact diff/result identity, focused evidence, baseline, broader proof commands, and deviation list.", ["Run fresh focused and agreed broader checks against the exact result; capture commands, exits, environment, and evidence.", "Verify changed-file inventory against authority and restore unrelated generated churn.", "Route every material deviation to its named owner; continue only with revised plan and authority.", "Record migration/config safety or explicit non-applicability, rollback limits, known failures, and unexecuted checks."], "A `built_for_test` or blocked receipt with exact target identity and complete evidence limits.", "Builder cannot approve independent quality, merge, deploy, or release its own result."),
"tester-evidence-and-negative-control": ("Use when planning independent evidence and proving that the chosen checks can detect wrong behaviour.", "Exact target, approved criteria/risks, Builder receipt, environment topology, fixtures, and baseline.", ["Reject incomplete or mismatched target identity before execution.", "Map each claim to observable output, persisted state, side effects, forbidden mutations, and environment needs.", "Run a disposable semantic negative control that changes the behaviour under test and must fail at the intended assertion.", "Restore and verify target identity before normal execution."], "An evidence plan and negative-control receipt that distinguishes semantic failure from harness failure.", "Stop on target drift, policy-conflicting fixtures, wrong-cause failure, or a check that cannot detect the claimed defect."),
"tester-adversarial-behaviour": ("Use when executing acceptance and risk checks across behaviour, side effects, repeats, failures, and concurrency.", "Evidence plan, restored exact target, stable fixtures, and declared process/store/integration boundary.", ["Exercise success and applicable refusal/error states through public seams.", "Assert output, persisted state/version, every required side effect, and every forbidden mutation.", "Exercise exact replay, changed-key repetition, stale state, partial failure, and recovery where relevant.", "Synchronise concurrency attempts when race behaviour matters; report only the topology actually observed."], "Revision-bound receipts for each case with command, exit, assertions, evidence locator, and topology limit.", "Do not generalise one-process or in-memory results to distributed, durable, or production behaviour."),
"tester-defect-and-handoff": ("Use when failures need minimal reproduction and all claims need coverage classification for Reviewer.", "Execution receipts, exact target/environment identity, and material-delta record.", ["Reduce each failure to the smallest reproducer that still demonstrates the acceptance or risk breach.", "Record expected, actual, preconditions, command, exit, and target identity.", "After a repair, require a new exact target and rerun the reproducer plus affected evidence.", "Classify every claim supported, failed, blocked, or unassessed; list confidence limits."], "A `tested`, `failed`, or blocked Reviewer handoff with reproducible defects and claim-level evidence.", "A changed expectation needs owner approval; a changed target invalidates earlier evidence until rerun."),
"reviewer-revision-and-acceptance": ("Use when beginning an independent review of one exact result against approved intent.", "Exact target/diff, matching PRD/Design/Plan, Builder and Tester receipts, reviewer identity, independence, authority, and cutoff.", ["Pin every artifact identity and reject stale, truncated, or mismatched evidence.", "Split each acceptance criterion into observable sub-claims.", "For each sub-claim compare approved intent, implementation path, executed assertion, and stated limit.", "Classify supported, failed, blocked, or unassessed without inheriting upstream status."], "A reviewable/blocked intake decision and complete acceptance trace.", "Stop when exact bytes, independence, authority, or required upstream revisions cannot be established."),
"reviewer-risk-and-false-green": ("Use when review evidence must be challenged for security, consistency, lifecycle, and false-green gaps.", "Acceptance trace, diff, tests, negative-control evidence, topology, and risk boundaries.", ["Inspect authorisation, disclosure, state transitions, stale writes, idempotency, event/state consistency, and relevant failure recovery.", "Ask what implementation, payload, state, or topology defect could remain while the suite stays green.", "Check whether the negative control failed at the intended assertion and whether fresh GREEN used the restored exact target.", "Write findings with locator, consequence, remediation, owner path, and recheck condition."], "A risk finding set and unsupported-claim list, with hard evidence separated from judgment calls.", "Do not convert missing proof into an implementation defect; label it unassessed or blocked as appropriate."),
"reviewer-decision-and-recheck": ("Use when issuing or updating a bounded review recommendation after evidence is complete or changes.", "Acceptance/risk findings, target identity, evidence cutoff, release constraints, and material-delta list.", ["Issue changes_requested, merge_candidate, or blocked for the exact target and inspected scope.", "Keep merge recommendation separate from deployment/release gaps and human authority.", "For each later code, test, fixture, environment, or evidence delta, decide whether it is material and rerun affected checks.", "Supersede the old receipt rather than silently editing its history."], "A revision-bound recommendation, release-gap register, and delta/recheck record.", "Recommendation never grants merge, deployment, release, publication, or risk acceptance."),
"curator-provenance-and-classification": ("Use when a delivery finding may become guidance, repository context, product work, or an excluded one-off.", "Exact review evidence, narrow candidate claim, confidentiality/reuse rights, counterexamples, and dispute state.", ["Bind the claim to immutable evidence and state what is not proved.", "Exclude identifying, private, prohibited, disputed, or unsupported content before routing.", "Classify as skill guidance, repository/domain context, product change, local note, or excluded.", "Test generality with a counterexample; narrow the claim until it survives or keep it local."], "A privacy-safe, bounded finding with classification rationale and excluded details.", "Stop on ambiguous source rights, mutable identity, unresolved dispute, or unsafe provenance."),
"curator-proposal-and-history": ("Use when a classified finding needs one governed destination, a minimal proposal, and an approval-gated history.", "Classified finding, current destination version, conflicts, contribution path, and named authority.", ["Choose one destination controlled by the authority for that class.", "Deduplicate against current guidance and preserve conflicting decisions.", "Draft the smallest versioned change that alters behaviour; leave repository facts out of skills and skill guidance out of project context.", "Record proposed, accepted, rejected, or superseded only from an authentic owner decision; append history rather than rewrite it."], "A versioned proposal/decision record with destination, diff, owner, rationale, and retained history.", "File creation or installation is not adoption. Stop when owner or governed contribution path is unknown."),
"curator-next-use-evaluation": ("Use when a proposed or accepted learning needs a future test before anyone claims it improved delivery.", "Exact proposal/version, intended trigger, baseline, eligible future work, and measurement owner.", ["Name the next situation that should trigger the skill or context.", "Define the observable behaviour expected to change and a comparable baseline.", "Exclude cases where the guidance should not fire.", "After use, record helped, no_change, harmed, or inconclusive with evidence; do not use document volume as benefit."], "A next-use evaluation plan and, after real use, an evidence-bound result.", "No benefit claim before an eligible use is observed; a failed evaluation returns the update for revision or rejection."),
}

UMBRELLA = {
"capture-refine": ("Use when an ambiguous product request needs a reviewable PRD without drifting into architecture or implementation.", ["Open `capture-intake-and-gaps` to establish evidence and decisions.", "Open `capture-engineer-interview` only for engineering-observable gaps.", "Open `capture-prd-handoff` when the gap register is explicit enough to draft."], "Finish at engineer completeness review; Product approval remains separate."),
"design": ("Use when approved interaction design is absent, incomplete, or conflicts with an approved PRD.", ["Open `design-input-readiness` first; stop if Design is not required or inputs are blocked.", "Open `design-state-interaction-spec` for uncovered behaviour.", "Open `design-source-readiness` for source composition, coverage review, and the exact handoff."], "Finish only with ready, design-not-required, incomplete, conflicting, or blocked status bound to exact revisions."),
"planner": ("Use when approved behaviour needs an architecture, risk, slicing, and proof plan before implementation.", ["Open `planner-impact-and-invariants` before selecting implementation structure.", "Open `planner-delivery-slices` after contracts and boundaries are known.", "Open `planner-verification-and-handoff` for risks, migration, observability, and Engineering review."], "Return business or interaction ambiguity; finish with accepted ready_for_build or blocked."),
"builder": ("Use when one accepted technical increment has explicit change authority and must be implemented with causal evidence.", ["Open `builder-baseline-and-red` before editing.", "Open `builder-bounded-change` for one approved increment.", "Open `builder-verification-and-deviation` before Tester handoff or whenever scope changes."], "Finish with exact built_for_test evidence or blocked; never self-release."),
"tester": ("Use when an exact built target needs independent adversarial acceptance evidence.", ["Open `tester-evidence-and-negative-control` before trusting green.", "Open `tester-adversarial-behaviour` for applicable acceptance and risk boundaries.", "Open `tester-defect-and-handoff` for failures, reruns, and Reviewer intake."], "Finish with tested, failed, or blocked and classify every claim."),
"reviewer": ("Use when an exact change needs an independent judgment across intent, implementation, and proof.", ["Open `reviewer-revision-and-acceptance` to pin evidence and trace criteria.", "Open `reviewer-risk-and-false-green` to challenge sufficiency.", "Open `reviewer-decision-and-recheck` to issue or supersede the recommendation."], "Finish with changes_requested, merge_candidate, or blocked; recommendation is not merge."),
"curator": ("Use when proven delivery evidence may justify a governed skill or repository-context update.", ["Open `curator-provenance-and-classification` before generalising.", "Open `curator-proposal-and-history` to route and govern the smallest update.", "Open `curator-next-use-evaluation` before claiming the update helps."], "Finish with blocked, proposed, accepted, rejected, or superseded plus an evaluation state."),
}

TEMPLATES = {
"capture-prd.md": """# Product behaviour agreement\n\n- Revision / source request:\n- Status: `draft_for_engineer_completeness_review|blocked`\n- Product owner / Engineering reviewer:\n\n## Evidence register\n| Source | Identity | Current/stale/missing/conflicting | Supported claim |\n|---|---|---|---|\n\n## Intended behaviour\nActors, permissions, states, validation, failures, recovery, repeated actions, and side effects.\n\n## Requirements and acceptance\n| ID | Observable requirement | Acceptance criterion | Evidence/check |\n|---|---|---|---|\n\n## Decisions and gaps\n| ID | Question | Owner | Blocking effect | Evidence | Decision/status |\n|---|---|---|---|---|---|\n\n## Design state\n`aligned|incomplete|mismatched|absent|not_required`; source revision and flags.\n\n## Engineer completeness\nExact revision, reviewer, outcome, retained Product questions. Completeness is not Product approval.\n""",
"design-readiness.md": """# Design readiness\n\n- PRD revision / Design source revision:\n- Mode: `specification_only|authorised_editable_source|not_required`\n- Status: `ready|design_not_required|incomplete|conflicting|blocked`\n\n## Requirement and state coverage\n| Requirement | States/transitions | Interaction locator | Disposition |\n|---|---|---|---|\n\n## Accessible interaction\n| State | Copy/actions | Focus/keyboard | Announcement | Recovery |\n|---|---|---|---|---|\n\n## Source result\nExact editable revision if actually changed; otherwise the structured change specification.\n\n## Decisions and reviews\nGaps, conflicts, Design owner receipt, and Product receipt for policy changes.\n""",
"planner-handoff.md": """# Technical plan handoff\n\n- PRD / Design / repository revisions:\n- Plan revision / Engineering owner:\n- Status: `ready_for_build|blocked`\n\n## Impact, reuse, contracts, and invariants\n| Surface | Existing seam/reuse | Contract/change | Invariant/risk | Evidence |\n|---|---|---|---|---|\n\n## Delivery slices\n| Order | Increment | Blocked by | Criterion | Changed surfaces | RED/pre-proof | GREEN/proof | Safe stop |\n|---|---|---|---|---|---|---|---|\n\n## Verification and operation\nChecks, signals, migration, compatibility, rollout, rollback, reconciliation, and unproved limits.\n\n## Engineering receipt\nExact plan revision, decision, assumptions, and separate Builder authority state.\n""",
"builder-receipt.md": """# Build receipt\n\n- Plan / PRD / Design revisions:\n- Authority receipt / repository / base / result identity:\n- Status: `built_for_test|blocked`\n\n## Changed behaviour and inventory\n| Criterion | Before/after | Path | Diff/hash | Authority match |\n|---|---|---|---|---|\n\n## RED and verification\n| Check | Command | Exit | Exact target | Meaning/evidence |\n|---|---|---|---|---|\n\n## Migration/config, deviations, and limits\nApplicability, safety/rollback, baseline failures, owner decisions, and unexecuted checks.\n\n## Tester intake\nExact artifact, environment/fixtures, topology boundary, and completeness.\n""",
"tester-evidence.md": """# Test evidence\n\n- Exact target / Builder receipt / environment and topology:\n- Status: `tested|failed|blocked`\n\n## Evidence plan and negative control\n| Claim | Observable assertion and side effects | Negative control | Environment |\n|---|---|---|---|\n\n## Results and defects\n| Case/defect | Expected | Actual | Command/exit | Evidence | Rerun identity |\n|---|---|---|---|---|---|\n\n## Coverage\n| Claim | `supported|failed|blocked|unassessed` | Evidence | Limit |\n|---|---|---|---|\n\n## Reviewer handoff\nMaterial-delta rule, exact artifacts, defects, and confidence boundary.\n""",
"reviewer-decision.md": """# Review decision\n\n- Exact target / upstream revisions / reviewer independence / cutoff:\n- Status: `changes_requested|merge_candidate|blocked`\n\n## Acceptance trace\n| Sub-claim | Intent | Implementation | Observed proof | Disposition/limit |\n|---|---|---|---|---|\n\n## Findings and false-green attack\n| Severity | Locator | Consequence | Remediation | Owner/recheck |\n|---|---|---|---|---|\n\n## Recommendation and release gaps\nBounded merge recommendation, unsupported claims, separate release gaps, human authorities.\n\n## Delta recheck\nMaterial changes, affected claims, reruns, and superseding receipt.\n""",
"curator-learning.md": """# Governed learning record\n\n- Evidence identity / cutoff / confidentiality:\n- Status: `blocked|proposed|accepted|rejected|superseded`\n- Version / owner / destination:\n\n## Bounded finding and classification\nClaim, non-claims, counterexample, dispute state, and `skill|repository_context|product_change|local_note|excluded`.\n\n## Smallest update and history\nCurrent version, proposed diff, conflicts, owner decision, rationale, effective/review dates, retained prior states.\n\n## Next-use evaluation\nTrigger, excluded cases, observable behaviour, baseline, measure, owner, and `pending|helped|no_change|harmed|inconclusive`.\n""",
}


def role_text(key: str, data: dict) -> str:
    links = "\n".join(f"- [`{s}`](../skills/{s}/SKILL.md)" for s in data["skills"])
    actions = "\n".join(f"- {x}" for x in data["does"])
    return f"""# {data['title']}\n\n## Decision owned\n{data['decision']}\n\n## Start boundary\n{data['starts']}\n\n## Work\n{actions}\n\n## Return path\n{data['returns']}\n\n## Completion criterion\n{data['complete']}\n\n## Authority limit\n{data['never']}\n\n## Skills\n{links}\n\nShared role/skill/context/tool semantics live in [`../CONCEPTS.md`](../CONCEPTS.md); permissions are declared in [`../AUTHORITY.md`](../AUTHORITY.md).\n"""


def skill_text(name: str, description: str, inputs: str, steps: list[str], output: str, stop: str) -> str:
    numbered = "\n".join(f"{i}. {step}" for i, step in enumerate(steps, 1))
    return f"""---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\n## Inputs\n{inputs}\n\n## Procedure\n{numbered}\n\n## Output\n{output}\n\n## Stop condition\n{stop}\n"""


def umbrella_text(name: str, description: str, routes: list[str], complete: str) -> str:
    role = ROLES[name]
    items = "\n".join(f"{i}. {route}" for i, route in enumerate(routes, 1))
    return f"""---\nname: {name}\ndescription: {description}\n---\n\n# {role['title']} router\n\n## Inputs\nRead the role contract at [`../../roles/{name}.md`](../../roles/{name}.md) and the exact work artifacts it requires.\n\n## Route\n{items}\n\n## Output\n{complete}\n"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "roles").mkdir(parents=True)
    (OUT / "skills").mkdir()
    (OUT / "templates").mkdir()
    (OUT / "example").mkdir()

    (OUT / "CONCEPTS.md").write_text("""# Role, skill, project context, and tool\n\n- A **role** owns decisions, handoffs, and limits.\n- A **skill** changes behaviour for a specific trigger. Open only the skills the case needs.\n- **Project context** is repository-specific policy, architecture, vocabulary, and evidence. Keep it outside skills so guidance remains portable and project facts stay local.\n- A **tool** executes an action. Availability does not grant permission, approval, or decision authority.\n\nWork is iterative. A changed input can return to an earlier role; Design can be skipped when approved design is complete; several roles may work concurrently when their inputs and authority do not conflict.\n""")
    (OUT / "AUTHORITY.md").write_text("""# Authority and tools\n\nThis repository defines behaviour, not runtime permissions. A host must separately provide tools and least-privilege authority.\n\n| Role | Default posture | Mutation requires | Never implied by output |\n|---|---|---|---|\n| Capture & Refine | read requirements and relevant repository evidence | none in this role | Product approval |\n| Design | read; specification-only by default | exact editable target, integration, and human authority | Design approval |\n| Planner | read repository and operational context | none in this role | implementation authority |\n| Builder | local scoped mutation | exact repo/base/surfaces and human authority | merge or release |\n| Tester | independent read/execute in isolated target | separate Builder authority for repairs | approval |\n| Reviewer | independent read/execute | none in this role | merge or release |\n| Curator | read and propose | governed contribution approval for accepted update | adoption or publication |\n\nCredentials, network access, external messages, merges, deployments, and releases remain host-controlled.\n""")

    agents = []
    for key, data in ROLES.items():
        role_path = OUT / "roles" / f"{key}.md"
        role_path.write_text(role_text(key, data))
        desc, routes, complete = UMBRELLA[key]
        skill_dir = OUT / "skills" / key
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(umbrella_text(key, desc, routes, complete))
        agents.append({"id": key, "role": str(role_path.relative_to(ROOT)), "umbrella_skill": str((skill_dir / "SKILL.md").relative_to(ROOT)), "skills": [f"agent-system/skills/{s}/SKILL.md" for s in data["skills"]], "template": f"agent-system/templates/{ {'capture-refine':'capture-prd','design':'design-readiness','planner':'planner-handoff','builder':'builder-receipt','tester':'tester-evidence','reviewer':'reviewer-decision','curator':'curator-learning'}[key] }.md"})

    for name, (desc, inputs, steps, output, stop) in SUPPORT.items():
        d = OUT / "skills" / name
        d.mkdir()
        (d / "SKILL.md").write_text(skill_text(name, desc, inputs, steps, output, stop))

    for name, content in TEMPLATES.items():
        (OUT / "templates" / name).write_text(content)

    example = """# One request, conditional handoffs\n\nThis is an illustrative trace, not a live agent execution or approval record.\n\n1. **Request:** “Let customers cancel an order.”\n2. **Capture & Refine:** inspects only the prior order-state PRD, cancellation tests, and relevant service path. It records eligible states, ownership, repeat requests, race behaviour, disclosure, and side effects as open decisions. Engineering confirms the document is complete; Product separately approves a revision.\n3. **Design (conditional):** the approved design shows only the happy path, so Design specifies pending, success, too-late, already-cancelled, conflict, unknown-result, keyboard, focus, announcement, and safe-retry states. Without editable-source authority it emits a specification, not a claimed Figma revision. A Design owner approves the exact specification.\n4. **Planner:** reuses the existing order transition seam, defines one-winner and idempotency invariants, identifies the transaction/outbox boundary, and writes vertical slices with checks and rollback. A newly discovered refund-policy ambiguity returns to Product before the plan can be accepted.\n5. **Builder:** after a revised accepted plan and explicit repository authority, proves the first criterion red, implements one slice, runs focused and broader checks, and hands Tester an exact result identity. A needed schema change outside scope is returned instead of absorbed.\n6. **Tester:** uses an isolated semantic negative control, then challenges ownership, lifecycle refusal, exact replay, changed-key repetition, stale state, partial failure, and synchronised contention. It reports the exact one-process boundary and leaves multi-worker durability unassessed.\n7. **Reviewer:** traces intent, implementation, and assertions; attacks event-payload and topology false greens; then recommends `merge_candidate` for the bounded change while keeping deployment and release gaps separate. A human retains merge authority.\n8. **Curator:** classifies “exact result identity is required before evidence review” as a skill proposal, keeps cancellable order states in repository context, routes a durable-outbox need to product work, and defines a next-use check. Nothing is called adopted without an owner decision.\n\nThe trace loops or skips roles as evidence requires; it is not a seven-step release process.\n"""
    (OUT / "example" / "request-to-handoffs.md").write_text(example)

    manifest = {
        "schema_version": 1,
        "canonical_root": "agent-system",
        "published_snapshot": {"paths": ["roles", "skills", "worked-example", "web", "presentation"], "policy": "Preserved from main; not canonical for revised agents."},
        "agents": agents,
        "shared": ["agent-system/CONCEPTS.md", "agent-system/AUTHORITY.md"],
        "example": "agent-system/example/request-to-handoffs.md",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
