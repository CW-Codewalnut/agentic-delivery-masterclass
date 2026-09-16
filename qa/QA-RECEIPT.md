# Experience QA receipt

- Source revision: content commit `2355a44` merged into `main` before this readiness pass.
- Fresh build: 16 HTML scenes, 16-slide PPTX, 16-page PDF, and five relative download copies generated from the current source.
- Strict source parity: 33/33 embedded files equal disk content and SHA-256; zero missing and zero mismatches (`qa/source-parity.json`). Browser QA expanded and compared every file tab, not only the first.
- Automated tests: **26 passed, 0 failed** — 16 Python unit/content-contract tests and 10 Playwright screen/interaction tests.
- Guided route: all 16 scenes; all seven roles; all six exact act labels; next, back, reset, Home, arrow navigation, and disabled final Next state passed.
- Drawer accessibility: dialog semantics, keyboard open/close, focus trap in both directions, and focus restoration passed.
- Accessibility: screen and print-media axe checks passed with zero WCAG 2.0/2.1 A/AA and WCAG 2.2 AA violations.
- Runtime integrity: the full guided route plus all source tabs produced zero console, page, or failed-network errors.
- Offline route: `file://` navigation and all five relative download targets passed. PDF, PPTX, script, cue sheet, and timing download bytes match their canonical files.
- Responsive/layout: all 16 projector-size scenes had zero measured overflow; mobile horizontal overflow, final-content reachability, and the prior overlay/state screenshot sequence passed.
- PDF: 16/16 pages rasterised and individually inspected at full rendered size; zero clipping, overlap, unreadable-text, broken-layout, or visual defects (`qa/pdf-visual-inspection.json`).
- Automated route execution: **3135.83 ms**, recorded separately in `qa/automated-route-timing.json`. This is machine execution, not a human speech or rehearsal duration.
- Human timing remains explicitly estimated: 1,408 script words; 9.39–10.83 minutes at 150–130 wpm; 50-minute facilitation budget is provisional; no human rehearsal has been performed.

## Artifact hashes

- HTML SHA-256: `8ac68e79ecd034798de747e930d2a2f9fee9174d62a4cd22c5ce3fb3b740deaa`
- PPTX SHA-256: `08b0aa25e2c632f75b7b7d08ada1e0a61605879ae05d32b31908c787b1bfe69f`
- PDF SHA-256: `2aa7573f61262b32da4d06284a9bc8af868b3c85a12c14f295e6022714f38fd0`

## Boundaries

- The experience is labelled **Prepared walkthrough — not a live agent run**.
- The NFR X-ray and merge score remain aspirational, not executed proof.
- Axe evidence does not establish PDF/UA conformance.
- Visual PDF inspection is a rendering/layout check, not assistive-technology certification.
- No publication, push, or hosting was performed from this worktree.
