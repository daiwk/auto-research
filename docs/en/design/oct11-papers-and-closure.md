# 2026-10-11 paper implementation and platform closeout

<!-- source-sha256: 24499e503147db5bcb280d91f2a5c986f3c95f6c01ee8cfbe41bd28ab706b000 -->

[简体中文](../../design/oct11-papers-and-closure.md)

Accepted scope: 12 papers, one OPD diagnostic, and four closeout items covering historical reconciliation, real evaluation evidence, executable Evolve integration, and regression/GPU verification. The papers first appeared on 2026-10-08, not October 11. This page records accepted scope and criteria. Actual status, measurements, and unfinished work are in the [implementation register](../research-audits/oct11-implementation-scope.md); registry entries and formula tests are not delivery.

| Priority | Paper or facility | arXiv | Acceptance focus |
|---|---|---|---|
| P0 | ZIP-SR / ZE-EDEN | 2610.12444 | Low-precision updates, public language modeling, executable optimizer Evolve |
| P0 | VFold | 2610.12338 | Numerical weight-folding contract and actual shared cache |
| P0 | Option-Channel Attack | 2610.12292 | Six strategies, isolated calibration, conditional ASR denominator |
| P0 | ReCal | 2610.11332 | Actual FFN deletion, SFT → OPD, negative results |
| P0 | ZCPO | 2610.12161 | Informative reward groups, real parameter updates, train-only manifest |
| P1 | SparseDecoding | 2610.12327 | Decode calibration and actual CUDA bitmask kernel |
| P1 | V-CoLA | 2610.11251 | Actual delta-state contributions, visual merging, layer exit |
| P1 | Data-Space Iteration | 2610.12102 | Actual alternating teacher, fake, and generator training |
| P1 | OnTrack | 2610.12375 | Streaming alignment, lifecycle, public-trajectory isolation |
| P1 | Memento3 | 2610.11794 | Generative world model, safety interpretation, replay and mismatch |
| P1 | PIVOT | 2610.11167 | Domain few-shot, shared warmup, three recipes |
| P1 | SGUID | 2610.12367 | Live teacher, actual persistence filtering, restore and two retraining rounds |
| P1 diagnostic | OPD Learning Signals | 2610.11247 | Representation, gradients, and occupancy; not capability gains |

## Completion criteria

- Preserve each defining algorithm. Public checkpoint/data paths execute and report scale, diagnostic tier, and untested boundaries.
- Reconcile historical candidates and manifest automatically, without changing frozen decisions or treating acceptance as implementation.
- Evolve operators must execute and reevaluate in the controller. Proposal priors are not copied into fitness.
- Run relevant behavior tests, CI gates, generators, and documentation builds. CUDA paths need real A100/A30 execution and sanitized receipts.
- No gold in agent inputs, fabricated measurements, recreated uv.lock, or edits to the original dirty worktree.
- Submit one PR. Implementation does not automatically advance the review cutoff.
