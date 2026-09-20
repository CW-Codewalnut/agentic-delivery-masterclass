---
name: capture-grill-and-decide
description: Use when a request or a draft PRD still holds an ambiguity, a silent assumption, or an unowned decision that no test could fail on.
---

# capture-grill-and-decide

## Inputs
The supplied request, the source and gap registers, and the named Product and Engineering owners.

## Procedure
1. Restate the request as one sentence of observable behaviour. Stop and ask when you cannot.
2. List every assumption you would have to make to write one acceptance criterion. Classify each as `decided`, `owned_open`, or `engineering_observable`, and name its owner.
3. Ask one decision-shaped question at a time. Give the candidate answers and the consequence of each. Never bundle two questions into one.
4. Attack the draft requirement by requirement. For each, name the actor, precondition, state, and observable outcome that is still unstated. A requirement no test could fail on is not yet a requirement.
5. Reject wording that names a technology, a schema, or an algorithm. Rewrite it as observable behaviour, or route it to Planner as an architecture question.
6. Apply the no-op test to every answer. Discard an answer that changes no requirement, no criterion, and no gap.
7. Recheck after each material answer. An answer that changes a `decided` item invalidates every criterion that cites it.
8. Leave each residual assumption visible in the assumption register with its owner and its effect if wrong. Never resolve an owned Product decision by preference.

## Output
A decision ledger of asked questions and recorded answers, an assumption register with every residual assumption classified and owned, and a routed list of architecture or design wording removed from the draft.

## Stop condition
Stop when the next answer needs Product policy that has no named owner, when the request has no stable identity, or when every remaining ambiguity is non-blocking and recorded.
