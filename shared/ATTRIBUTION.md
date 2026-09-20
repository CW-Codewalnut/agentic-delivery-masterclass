# Shared skills and their provenance

A skill lives here only when two or more agents open it. A skill one agent opens belongs in that agent's own folder, and `scripts/validate_agent_system.py` fails when a shared skill declares fewer than two agents.

## Vendored from `mattpocock/skills`

`skills/tdd/` and `skills/code-review/` are **verbatim copies**. They are not paraphrases, and they are not rewritten to this repository's house shape.

- Source repository: [`mattpocock/skills`](https://github.com/mattpocock/skills), pinned at commit [`c55ee460`](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7).
- Licence: MIT. The copyright and permission notice is retained verbatim in [`LICENSE-mattpocock-skills`](LICENSE-mattpocock-skills), as that licence requires.
- Copyright (c) 2026 Matt Pocock.

`agents/manifest.json` records each file's source URL, commit, and SHA-256. The test suite recomputes those hashes, so any edit to a vendored file fails. To take a newer upstream version, fetch it at a new pinned commit and update the recorded hash. Do not hand-edit the file.

Matt Pocock and the `mattpocock/skills` contributors have not reviewed or endorsed this repository.

## Why these files keep their own shape

Every skill under `agents/` must start its `description` with `Use when ` and must carry `## Inputs`, `## Procedure`, `## Output`, and `## Stop condition`. No vendored file satisfies those rules, and none was changed to. Editing a copy to fit a house style would end the claim that it is verbatim, which is the only claim that makes the copy auditable. The validator therefore checks a vendored file's provenance and integrity, and never its shape.

## What is not vendored, and why

Four other files were read at the same commit and left out.

| File | Why not |
| --- | --- |
| `grilling` | `capture-refine` already owns `capture-grill-and-decide`, derived from this idea. Vendoring both would leave one of them changing nothing. |
| `to-spec` | Overlaps `capture-acceptance-contract`, which already produces the testable acceptance set. |
| `to-tickets` | Overlaps `planner-delivery-slices`, which already cuts slices with blocking edges. |
| `writing-for-agents` | Only Curator authors documents an agent consumes, so one agent opens it. That makes it agent-owned, not shared. |

[`../docs/research/matt-pocock-skills.md`](../docs/research/matt-pocock-skills.md) records which design ideas from those four are already applied, and where.
