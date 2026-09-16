# Curation record

**Status:** proposed learning set
**Owners:** skill maintainer, fictional domain owner, and product backlog owner respectively

| Finding | Classification | Destination | Status |
| --- | --- | --- | --- |
| Repeated actions need a request-identity decision. | reusable method | Capture & Refine skill | accepted in this pack |
| Race questions must name side effects that occur once. | reusable method | Planner/Tester skills | accepted in this pack |
| `placed` and `confirmed` are cancellable. | illustrative domain policy | domain context | accepted only for example v1 |
| Durable outbox and unique key constraint are needed for a production candidate. | engineering proposal | future product plan | proposed, not implemented |
| Payment/refund coupling remains undecided. | product gap | future Capture & Refine pass | open |

## Next-use check
On the next state-changing feature, verify the refinement record asks both “what identifies a retry?” and “what happens when valid requests race?” Then inspect whether acceptance criteria cover state and side effects, not only response codes.
