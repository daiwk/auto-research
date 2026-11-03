# Overlap scan, two real-model implementations and open queue: 2026-10-07

<!-- source-sha256: ab7873b61f79e74bc017de8502cb5f073a100dd63c4795c56984b51cc15a7f7d -->

[简体中文](../recent-paper-scan-20261007.md)

See the [subsequent review closure](../research-audits/oct07-review-closure/README.md) for later repairs and decisions. This is the original snapshot; subsequent date and monthly-ID queries have separate receipts.

## Delivered and measured

[FrugalEvo](../agent-research/2610.03675-frugalevo/README-en.md) and [Sentry](../agent-research/2610.02994-sentry/README-en.md) add standalone controllers and public checkpoint paths. Both first published **October 2**; these are earlier leads, not today's publications. Separate per-paper metrics and A100 receipts, no unified Evolve integration claim. Five other methods were reviewed but not implemented, and newly surfaced Airbnb SIFT and Google TEE-FL are evidence-backed pending items only.

**1,271 tests passed**, plus strict docs, specification, format and platform audit. Both ran real three-seed checkpoint tests on A100 and underperformed controls: Sentry EM 29.17% vs 41.67%; FrugalEvo mean best radius sum 2.32222 vs weak-only 2.40000. [GPU receipt](../gpu-validations/oct07-agent-search-a100.json) establishes execution, not paper-scale gains or Evolve promotion.

## Coverage

October 1–7, 2026; four live arXiv tracks returned, but some hit the per-query 400 cap and official sources timed out. coverage_complete=false and last complete watermark **2026-10-02**; retain October 1 overlap. No DeepXiv.

| Track | Title hits | Unrecorded in window | Capped / total queries |
|---|---:|---:|---:|
| Industrial/LLM | 39 | 31 | 5 / 22 |
| Foundation/multimodal | 453 | 398 | 8 / 8 |
| Post-training | 200 | 164 | 7 / 8 |
| Agent/RSI/Jev | 434 | 381 | 8 / 8 |

Cross-track deduplication leaves 1,010 hits including implemented, outside-window and unreviewed items, not eligible new papers. [Title pool](../research-audits/oct07-title-pool.json), [query coverage](../research-audits/oct07-query-coverage.json), [official sources](../research-audits/oct07-official-source-coverage.json) and [48-title agent triage](../research-audits/oct07-agent-48-triage.md). Prior 48 are unrecorded October 2–6 titles, plus 69 October 1 overlap and 28 earlier leads. All 48 received title/abstract triage, not full-text review.

Three Google Research and two Meta pages timed out; DeepMind nine pages and 265 entries read with limited identity matching, still partial. Manual Google review recovered a paper despite an empty automatic queue. Meta checks found recent AI-assisted math (not a model-training method) and existing MaD-RL (no duplicate); not a complete Meta audit.

## Industrial evidence

| Priority | Paper | Verified evidence | Decision |
|---|---|---|---|
| P0 Google | [Toward provably private learning from federated data](https://arxiv.org/abs/2609.31494), first Sep 25; [official announcement](https://research.google/blog/toward-provably-private-learning-from-federated-data/) Oct 2 | §5.3 3.5 million devices per arm, privacy budget about one-third, input UX unchanged, training two months→three weeks | Historical qualifying backfill, not implemented; TEE attestation, KMS, DP and reproducible builds are essential; CUDA simulation cannot establish privacy |
| P0 Airbnb | [SIFT](https://arxiv.org/abs/2610.07810), first Oct 6 | PDF p7 §8.2/Table 4 randomized ID split: recommendation filter clicks +20%, booking guardrail +0.03% nonsignificant. Hotel expansion p8/Table 6 reports +0.76% market total uncanceled bookings | Recent qualifying lead, not implemented; no equivalent public itinerary/filter/numeric capacity labels |

## Five verified mechanisms, still open

| Paper | Defining mechanism | Remaining acceptance |
|---|---|---|
| [Dynamic Expert Pruning](https://arxiv.org/html/2610.02951v1) | Per-layer prompt predictor, REAP calibration, BCE and soft-mask KD, sparse residency and differential loads | Real MoE and workflow traces, trained predictor, quality/peak memory/loading; not dense masking or estimates |
| [RC-OPD](https://arxiv.org/html/2610.03515v1) | First error repair, student continuation, local multi-round success distillation and fallback; B.6 per-vocabulary upper clipping, not ordinary KL | [Author repo](https://github.com/Starrylay/RC-OPD) has evaluation and checkpoint only; real diagnosis, continuation/training, leak-free control, not a loss stub |
| [Recursive Harness Self-Improvement](https://arxiv.org/html/2610.03548v1) | Fixed verifier, live/candidate isolation, same-cohort effectiveness/difficulty/cost gates and at most three failures before fallback | Real generator/verifiable tasks, rejection and full cost logs; special zero-accuracy rule, no random difficulty |
| [Pivot-SD](https://arxiv.org/html/2610.03665v1) | Frozen masked-diffusion trajectory, masked entropy-drop pivot; CE for success and pivot-only unlikelihood for failure | Precommit masks and training with real LLaDA/Dream plus independent benchmarks; not autoregressive Qwen entropy |
| [KV²](https://arxiv.org/html/2610.03198v1) | Block proxy selects reconstruction queries, reconstructs after full KV, per-head attention and global compression | KeyDiff, real KV/positions, CUDA reconstruction and long-context quality/latency/memory; no implementation/receipt yet |

Prioritize feasible Google TEE-FL and SIFT public mapping without invented online labels; then RC-OPD and KV² paths, and models/environments for the other three. Continue targeted full text and failed-source recovery before advancing. The [roadmap](../research-roadmap.md) is the single live TODO list.
