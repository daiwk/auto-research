# October 17 supplemental components: scope and cost contract

<!-- source-sha256: 76c3bf4d89c0b31ef059ea2026af6100177db4bd37b6478f765a37f5d17c9ede -->

[简体中文](../../../research-audits/oct17-supplement/README.md)

This is a follow-up to the **October 16 announcement and October 15 v1 dates**, not a new announcement. One approved MR covers nine low-cost components, two evaluation interfaces, and three reference-only papers; delivery does not imply all-source closure or advance the review watermark.

## Accepted scope

| Category | Paper / stable key | Accepted local scope | Full-experiment cost and decision |
| --- | --- | --- | --- |
| Component | Prism-1 / `prism-1` | Independent option blocks, shared positions, odds readout and invariance | 8B/12B, multiple arms and seeds, about 50–85 minutes per H100 run; not reproduced (review DONE) |
| Component | LangDiT / `langdit` | Continuous diffusion denoiser, shortcut-codebook gradients, bounded calibration, and self-conditioning | About 334M, seven sets × 250K updates, 512×1024 tokens per step; not reproduced (review DONE) |
| Component | OPRD / `oprd-reminder` | Teacher-only reminder scope, success NLL/failure reverse KL, shared support, and refresh | 16 H20s, 131072 context, three epochs, and online repository rollouts; not reproduced (review DONE) |
| Component | OpCredit / `opcredit` | BOC support deduplication, FTC potential difference, decision spans, and joint policy loss | Eight RTX5880s, about 2,500 GPU hours, and Freebase serving; not reproduced (review DONE) |
| Component | SSR / `structural-signal-retriever` | Bounded structural signals, IDF inverted retrieval, and deterministic ranking | 8.84M passages, about 124 GiB RAM, and API orchestration; not reproduced (review DONE) |
| Component | RSIFlow / `rsiflow` | Frozen parents, M/H/A interventions, acceptance/rejection, and failure experience | 4B/8B, distributed training, multiple rounds/candidates, 3,000 train and 744 reported tasks; not reproduced (review DONE) |
| Component | LEASH / `leash` | Pooled LDA, task-level OOF calibration, and post-escalation supervision scheduling | 262 OSWorld tasks, weak models and a commercial stronger one, long GUI interaction; not reproduced (review DONE) |
| Component | PROBE / `probe` | Trace verifier, first/repeat rewards, coverage denominator, and deterministic rescoring | 4B auditor/30B target, dual A100s, multiple optimizers and arms; not reproduced (review DONE) |
| Component | Terminal-RSI / `terminal-rsi` | TB-GAE, chunked continuation, FDR/SPR, and family divisor | 27B, 256K, multistage distributed PPO, 3,000 tasks; not reproduced (review DONE) |
| Evaluation interface | GACC-Bench / `gacc-bench` | Isolated compression/retrieval/scoring, budget truncation, reuse, and multi-question statistics | Ten models, multiple budgets, 281 contexts/500 goals/2,571 questions across long-context APIs; not reproduced (review DONE) |
| Evaluation interface | Muon paired-budget / `muon-paired-budget` | Equal-data/equal-time AUC, paired statistics, and tuning-budget regret | Four workloads, 23 candidates, and five matched seeds; not reproduced (review DONE) |
| Reference only | Google Gemini Minecraft / `gemini-minecraft` | Method, one case, figures, and costs | Four agents plus Observer, about 27 hours and 24,000 calls once; too costly, not reproduced (review DONE) |
| Reference only | Hy-Memory / `hy-memory` | OPD, attribution rewards, and memory-write review | 30B-A3B, 128 H20s, 64 windows × eight rollouts; too costly, not reproduced (review DONE) |
| Reference only | Athanor / `athanor` | Research pipeline and resource limits | 32 GPUs × 104 hours, about USD 12,000; too costly, not reproduced (review DONE) |

These are paper configurations, not predicted local times or GPU measurements. Budget assumes one A100 **or** A30, with no large weight or full dataset downloads, long rollouts, or fixture relabeling as capability validation.

## Acceptance contract

- Runnable standalone modules and commands, not registry-only integration or evolve promotion.
- Independent references, negative controls, and failing inputs check decisive mechanisms. Only training targets may use training gold; evaluated agents, compressors, and routers cannot read answers.
- Freeze source before bounded three-seed real A100/A30 runs. Receipts bind command, input identity, commit, and source SHA. No fabricated GPU receipt for CPU components.
- Separate metrics per paper, all `diagnostic_only: true` and `promotion_eligible: false`. Public interface validation does not execute original models.
- Preserve known PROBE judge mistakes and deterministic rescoring differences. Do not attribute Terminal-RSI's main-table gains to TB-GAE without checkpoint evidence.
- Upstream entry points and licensing are separate; do not copy without clear permission. High-cost decisions are terminal and non-blocking.

## Measured execution

Nine components and two interfaces were implemented. Four CUDA components ran bounded seeds 42/43/44 on an **NVIDIA A100-SXM4-80GB**, and seven CPU paths ran the same seeds. Per-paper metrics are not a leaderboard or original benchmark outcomes.

- GPU: Prism-1 independent equivalence/invariance and negative controls; LangDiT gradients and four normalization extremes; OPRD teacher isolation and actual updates; OpCredit independent credit and joint loss plus actual updates.
- CPU: SSR agrees with full scan; Muon rankings can reverse across data and time budgets; RSIFlow keeps failures/rejections; LEASH task-level OOF and 1/4/7 scheduling; PROBE distinguishes repeated hits from deduplicated coverage; Terminal-RSI full chunked continuation; GACC compressor sees no questions/gold and emits an empty unpadded result at zero budget.
- The new OPRD entry uses `oprd-reminder` and internal `--methods oprd`. The old `auto-research reproduce --paper oprd` (2609.08798 reverse distillation) is unchanged.
- LEASH's three counters record executed callbacks, and OPRD refresh counts teacher snapshot refreshes, **not capabilities**. AST inventory was regenerated after boundary review.
- The three references have no runnable algorithms, invented metrics, or GPU passes. Full experiments are terminal not-reproduced, review DONE, without retries.

All 14 include metadata and original figures, with catalogs and dashboard synchronized. 110 targeted mechanism/delivery tests passed; the full suite, Ruff, minimal-dependency entry points, strict docs, paper-spec, metric migration, GPU evidence, and platform audit passed. Final closure rechecks seed failures, aggregation, and frozen commits rather than relying on existing files. This batch does not advance the watermark or prove source exhaustion.
