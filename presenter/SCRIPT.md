# From intent to evidence — presenter script

**Ben Sheridan-Edwards · Fractional CTO / CodeWalnut**

## How to use this script

This is suggested spoken wording and demonstration choreography, not a record of Ben rehearsing. The worked order-cancellation policy is illustrative. The runnable implementation is a bounded teaching example, not a production service. Role and skill files describe responsibilities and reusable methods; opening them does not run seven autonomous agents.

Use the interactive presentation as the audience surface. Keep this script separate. The role sequence is **Capture & Refine → Design → Planner → Builder → Tester → Reviewer → Curator**. The six acts are the organising narrative; the seven roles are the practical workflow inside it.

Working allocation: **50 minutes, provisional for Ben's contribution**, distinct from the overall 90-minute masterclass described in the event outline. Suggested allocation: opening and operating model 10 minutes; worked demonstration 20; evidence and learning 8; adoption and audience discussion 7; recovery contingency 5. This is a facilitation budget, not measured speech duration. Automated walkthrough timing must be reported separately from estimated narration.

## Before the audience arrives

- Open the published presentation and download its offline HTML, deck PDF and PPTX. Confirm the exact revision against the readiness receipt.
- Keep a local repository checkout and terminal ready. Run the README verification command before the session; keep the real output visible, not a replacement transcript.
- Open the first scene, close any expanded files and use Reset. Make sure browser zoom suits the projector.
- Keep the PDF ready on the equivalent opening slide. If network access fails, use offline HTML first, then PDF. Neither fallback needs credentials.
- No production account, private repository, customer record or client transcript belongs on screen. Do not enter API keys or launch a live coding agent during this prepared route.

---

## Act 1 — AI Has Accelerated Coding, Not Software Delivery

**Show:** Opening and ambiguity scenes. The request: “Let customers cancel their orders.”

**Say:**

“Let us start with a request that sounds perfectly ordinary: let customers cancel their orders. We could put that into a coding assistant and get an implementation very quickly. But before we do, tell me what it means.

Can I cancel your order? Can I cancel mine once someone has started packing it? If the connection drops and I press the button again, do we send another cancellation event? If we cancel the order but the next step fails, what should the customer see?

Those are not typing problems. They are decisions about the product. Faster coding does not make the decisions disappear; it can simply move the ambiguity into code faster.

And requirements are only the first place this happens. Intent can get lost between product and design, between design and a technical plan, and between the code that was built and the evidence a reviewer actually sees. We can create more pull requests without creating more capacity to judge them.

So the question today is not just how much code an agent can produce. It is how we carry an agreed outcome through delivery, inspect the evidence and improve the next change.”

**Do:** Pause after each of the four questions. Invite one audience answer about the fulfilment boundary. Do not silently promote that answer into the sample's approved policy.

**Land:** The bottleneck is agreement and dependable delivery, not typing alone.

**Recover:** “We will use a deliberately small policy today. It is an example we can inspect, not a claim about how your business must work.”

## Act 2 — Reimagining the Lifecycle, From Code Generation to Confidence

**Show:** Lifecycle and seven-role journey.

**Say:**

“Nattu's lifecycle takes us through intent, build, prove, merge, release and learn. I want to make that practical. Here is a set of responsibilities that can support that lifecycle.

Capture and Refine helps us agree the behaviour. Design works out the experience and the important system decisions before we plan the implementation. The Planner turns that agreement into an executable sequence. The Builder implements within the agreed boundary. The Tester challenges the result. The Reviewer decides what the evidence supports. The Curator turns what we learned into a reviewed improvement for the next change.

These are roles, not necessarily seven products or seven people. One person may hold several responsibilities. An assistant may help with them. The important thing is that the input, output and authority at each handoff are explicit.

Notice that Design comes before Planner. We do not want a very detailed implementation plan for an experience nobody has agreed. And notice that a green test does not grant permission to deploy. Merge confidence and release confidence need different evidence.”

**Do:** Trace the sequence left to right. Point out the human decision at refinement, the design handoff and the review gate. Explain that the four journey chapters group the story; they do not replace the lifecycle or the four capabilities.

**Land:** Persistent artefacts carry intent across responsibilities; a long conversation is not the handoff contract.

**Recover:** If navigation becomes distracting, stay on the journey diagram and name only input, output and stop condition for each role.

## Act 3 — The Four Capabilities of an Agentic SDLC

**Show:** Capability overview, then the separation between reusable skill and domain context.

**Say:**

“The four capabilities are ambiguity reduction, scalable merge confidence, automated release confidence and engineering governance.

Ambiguity reduction is about making the missing decisions visible early. Scalable merge confidence is about bringing together the change, its requirements and relevant evidence so that review is not dependent on somebody reconstructing everything from scratch. Automated release confidence adds evidence about the actual environment and operational path. Governance tells us what the system is allowed to do, who can approve a transition and what we can inspect afterwards.

Today we will go deepest on refinement, the handoffs and the evidence-based review of one small change. We are not going to pretend that a local example proves a production release.

There is a useful distinction behind all four capabilities. A skill is a reusable method: ask about ownership, retries, failures and observable outcomes. Domain context contains the answers for this product: the order states, the fulfilment boundary and the approved policy.

If we bury the business answers inside every prompt, they drift. If we give an agent generic skills without the business context, it can ask sensible questions and still build the wrong thing. We need both, with owners and versions.”

**Do:** Expand the Capture & Refine role, then its full skill file, then the separate domain file. Show real file contents, not only the summary cards. Close each expansion before moving on.

**Land:** The method can travel between products. The business policy usually cannot.

**Recover:** “The files are also in the repository and offline pack. If this panel does not open, I will show the same source there.”

## Act 4 — From Theory to Practice, One Change Travels Through the SDLC

### Demonstration A — Capture & Refine

**Show:** Request, clarification, illustrative product decision and agreed acceptance criteria.

**Say:**

“Now we follow one change. This is a prepared walkthrough backed by real files and an executable example. It is not a live conversation with seven agents.

The request is short. The important question is consequential: what should happen when fulfilment has already started? We do not let the agent invent the answer. We expose the alternatives and record the decision in the example's product context.

The agreement then becomes observable behaviour. An eligible owner can cancel. An ineligible state is refused. A repeated request must not create another business effect. A different user cannot cancel someone else's order. The implementation and tests need to point back to these behaviours.

The useful output is not a bigger document. It is a smaller space for misunderstanding.”

**Do:** Open the worked request and refinement artefacts, point to the recorded decision, then open the acceptance criteria. Ask the audience which negative case they would otherwise have missed.

**Land:** Product authority supplies the policy; the agent makes the decision and evidence gaps easier to see.

**Recover:** If a question exposes a policy beyond the example, record it as an extension rather than improvising a claim that it is implemented.

### Demonstration B — Design → Planner → Builder

**Show:** Design artefact, implementation plan and executable source.

**Say:**

“Design is the bridge between the agreement and the work. What does the customer see when cancellation is allowed? What do they see when it is refused? What does the system need to preserve if a request is repeated?

Only then do we plan. The plan names the pieces to change, the checks we will run and the things we are deliberately not claiming. The Builder is not being asked to invent the feature from a vague headline. It receives a contract.

In this example we keep the implementation small enough to read. That is a teaching choice. Real payment providers, warehouses, distributed transactions and production identity systems bring additional contracts and failure modes. A local example must not borrow their credibility.”

**Do:** Navigate Design, Planner, Builder in that order. Expand each full role file and the associated worked artefact. Point to one acceptance identifier as it travels from agreement to plan and test.

**Land:** The handoff preserves decisions and constraints; the Builder does not silently become product owner or release approver.

**Recover:** If the code is too dense on the projector, stop scrolling. Show the named behaviour and the matching test instead; offer the repository for deeper inspection.

### Demonstration C — Tester → Reviewer

**Show:** Test source and actual captured verification evidence; optionally rerun the documented command locally.

**Say:**

“Now we change the question. We are no longer asking what we produced. We are asking what we can support with evidence.

The test source is visible. The recorded results identify the run and the files tested. If we rerun the command now, that is a fresh deterministic test run, not a live agent build.

A good test needs to be capable of finding the defect. Our semantic negative control deliberately removes the exact-replay return in a temporary copy. The assertion then fails because the retry no longer returns its original result. The unmodified implementation passes. That is a controlled mutation, not a historical production incident. The older import-failure log is retained separately and proves only that the module was missing at that earlier step.

The Reviewer then looks at the agreement, the implementation, the tests and the unassessed risks together. It can recommend acceptance within this scope, request changes or say that evidence is missing. It cannot turn ‘not tested’ into ‘passed’.

A merge-readiness number, if a product provides one, is a summary to investigate. We are not manufacturing a score here, and we are not presenting this example as a live MergeFlow report.”

**Do:** Read the verification command from the repository README, run it in the local checkout and wait for the actual exit. Show a named test and its acceptance mapping. Open the review artefact and limits. Do not read only the final green line.

**Land:** Evidence is specific to a claim, revision and environment.

**Recover:** If the command fails, do not conceal it. Say: “This fresh run did not pass. Here is the previously captured evidence with its identity; this run needs investigation.” Continue with the recorded example, not a false live-success claim.

### Demonstration D — Curator

**Show:** Curation artefact and the reusable skill improvement.

**Say:**

“Suppose our earlier requirement forgot repeated requests. The lesson has three destinations. The product rule belongs in domain context, after product approval. The implementation defect belongs in a scoped change. The better question belongs in a reusable skill.

Those are different updates with different owners. Curation does not mean copying every incident into every prompt. We choose the transferable lesson, review the proposed change and check that it improves another case without carrying the first product's policy into it.

This is how one delivered feature improves more than the product. It can improve our understanding and the method we use next time.”

**Do:** Open the curation decision. Identify the skill change, separate domain update and proposed product action. Return to Capture & Refine to close the loop.

**Land:** Learning becomes a maintained, reviewed asset rather than a memory in one person's chat.

**Recover:** If the audience asks who owns this in their organisation, propose an engineering maintainer and product-domain owner; do not assign real people without their agreement.

## Act 5 — Closing the Confidence Gaps, What Changed?

**Show:** Before/after evidence map and confidence boundaries.

**Say:**

“Go back to the original request. We have not made uncertainty vanish. We have made it visible and manageable.

Ambiguity became explicit questions and decisions. Handover loss became inspectable artefacts. Review gained a clear basis for its judgement. A missing retry question became a proposed improvement to the next refinement.

But the boundaries matter. These local tests do not prove a production deployment, a payment integration, operational rollback or the performance of an organisation. We have not measured a productivity improvement by showing a polished demonstration.

A useful evidence view separates supported, unassessed and stale. Supported means the relevant evidence exists for this claim. Unassessed means we have no conclusion. Stale means a previous result is no longer enough for the current change.

That distinction is more useful to a leader than a confident ‘done’ message.”

**Do:** Name one supported local behaviour, one unassessed release concern and one reason a test result becomes stale. Use the actual evidence matrix, not invented percentages.

**Land:** Merge confidence is not release confidence, and a demonstration is not a measured business outcome.

**Recover:** If time is short, retain this boundary explanation and shorten the code inspection instead.

## Act 6 — From Masterclass to Enterprise Adoption

**Show:** One-bottleneck adoption plan, ownership and measurement.

**Say:**

“You do not need to introduce seven agents across the company on Monday. Choose one bottleneck and one real change.

Agree the desired outcome and the evidence before the trial. Give the workflow a bounded set of repositories, data and tools. Keep approval for business decisions, access changes and release with the appropriate people. Name who maintains the skills and who owns the product context.

Then measure the result honestly: time waiting for clarification, review rounds, failed checks, hands-on correction, elapsed time, cost and accepted quality. Compare like with like. If the work simply moves from coding into correction, that is not the outcome we wanted.

The next step might be a hands-on practice programme or a selected enterprise opportunity. The discipline is the same: start with one bottleneck, prove the value and expand from evidence.

The lasting advantage is not one impressive prompt. It is a team that can carry intent through delivery, inspect why it trusts the result and improve its method every time.”

**Do:** Ask: “Where does a change spend most of its time waiting in your team?” Capture one bottleneck, a proposed owner and an evidence-of-done. Hand back to the event host for programme details rather than inventing commercial commitments.

**Land:** One bounded experiment, explicit owners and a recurring contribution/review ritual.

**Recover:** Leave five minutes unallocated for navigation, questions or an interrupted test. If unused, use it for audience discussion, not an unprepared live build.

---

## Recovery ladder

1. **Network unavailable:** use downloaded standalone HTML. State that this is the same prepared walkthrough.
2. **Browser interaction fails:** use matching PDF/PPTX and repository files. Do not claim the failed control worked.
3. **Fresh test fails:** retain the real failure; show versioned earlier proof with its stated scope. Never manufacture a green result.
4. **Product question exceeds policy:** identify it as an open decision and show where it would enter refinement.
5. **Time running short:** preserve refinement, Design-before-Planner, one real test, evidence limits and learning loop. Reduce optional full-file reading.
6. **Asked for a live agent:** explain that a live run needs separate tool/data permissions and a defined acceptance gate. This presentation demonstrates an inspectable operating method, not unrestricted autonomy.
