# November 12, 2026: Same-Announcement Backfills and Eight Mechanism Kernels

<!-- source-sha256: 4343439df043f0f8258809fc895e33140787c124db862d0950f6e4b6049740ba -->

[简体中文](../../../research-audits/nov12-components/README.md)

This bounded delivery contains **eight low-cost L1 components**: six from the same **November 11** announcement and two historical backfills triggered by Google's official site, **not eight first releases today**. CPU execution covers eight components × three seeds; a real single A100 covers three components × three seeds. Seven full systems/experiments are **not reproduced because of high cost; review DONE**. APMD is theoretical, so large-scale empirical reproduction is not applicable rather than an invented cost deferral.

The review watermark remains **November 9, 2026**. This delivery does not close the entire November 10–12 window or turn 956 source identities into new-paper counts or implementation tasks.

## Fixed Deliverables and Exact Fidelity Boundaries

| Paper / source | What actually executes locally | Full pipeline not implemented |
| --- | --- | --- |
| [Agent Gym](../../../agent-research/2608.15591-agent-gym/README-en.md), Google, first published 2026-08-16 | CPU: eight deterministic predicates, scope/priority exclusion, merged continuation/patch and actual 3→2→1 JSON updates; target/collateral and explicit SME approval contracts | Real actor, LLM rule discovery/investigation, semantic correction, automatic promotion; approval parameters do not authenticate human identity |
| [BATS](../../../agent-research/2511.17006-bats/README-en.md), Google collaboration, first published 2025-11-21 | CPU: per-tool budgets, unified token/tool cost, external SUCCESS/CONTINUE/PIVOT transitions; usage survives pivots and any exhausted tool stops execution | Semantic planning/verification/summaries, web tools, answer judge; external SUCCESS is not gold accuracy |
| [BOPD](../../../post-training/2611.13680-bopd/README-en.md), same-announcement backfill | CPU + A100: same-prefix full-vocabulary FKL with trajectory-equal reduction; frozen intermediate teacher, exact initial-parameter/buffer student reset, fresh optimizer | Stage I/II LLM rollouts, reference prompts, paper clipping, complete OPD trainer; the author-linked empty repository is not released training code |
| [APMD / reference reset](../../../post-training/2611.14467-apmd-reference-reset/README-en.md), same-announcement backfill | CPU: exact finite-distribution mirror steps, repeated reference resets, Kimi/Rebel squared-loss identities | LLM/PPO sampling loops, proofs of all theorems, general Transformer convergence; large empirical status is `not_applicable_theory_only` |
| [LCS reference OPD](../../../post-training/2611.13135-lcs-reference-opd/README-en.md), same-announcement backfill | CPU: exact LCS dynamic programming, two explicit normalizers, full action-sequence deduplication of same-task successes, independent argmax, failure-only reduction | Real teacher-reference collection, student environment rollouts, OPD loss/trainer/environment; references belong only to the training teacher |
| [REAL Loss](../../../foundation-models/2611.14399-real-loss/README-en.md), same-announcement backfill | CPU + A100: target-sampled q/p clipped path weights, last-step marginalization, fixed-gamma normalization, CE mixture, actual gradients and counterexample checks | Large target/drafter training, authentication of trajectory sampling provenance, speculative serving/throughput |
| [C²-Routing](../../../multimodal-models/2611.14469-c2-routing/README-en.md), same-announcement backfill | CPU: four-state joint-correctness risk H−B, validation dataset-macro cost ratio, immutable acceptance/full-image fallback policy | Image/text features, crop localization, trained selection/risk heads, real VQA; no test-time answer access or threshold fitting |
| [OnlyAct](../../../multimodal-models/2611.14420-onlyact/README-en.md), same-announcement backfill | CPU + A100: pooling/frozen projection of externally joint-encoded two-frame tokens, symmetric InfoNCE over all 3N candidates, same-video nonoverlap hard-negative contract | V-JEPA 2, LoRA, scene swapping/RAFT, video world models, or real action-disentanglement capability |

Each paper page retains original publication/review versions, bylines, upstream-code status, equations, original figures, negative controls, Chinese/reviewed-English prose, and four-level learning questions. Topic deep dives compare actual mechanisms. Original v1 dates take precedence: Google's older CATS description maps to BATS's 2025 first release, and reviewing Agent Gym v3 does not turn its August debut into a November paper.

Per-paper definitions and cost evidence are in the [fixed scope](../../../research-audits/nov12-components/task-scope.json), [primary-source receipts](../../../research-audits/nov12-components/primary-source-receipts.json), and reviews for [Agent](../../../research-audits/nov12-components/agent-review.json), [post-training](../../../research-audits/nov12-components/post-training-review.json), and [foundation/multimodal](../../../research-audits/nov12-components/foundation-review.json). Review locations cover bylines, defining mechanisms, and configurations; they are not whole-paper verification claims.

## Actual Execution: L1, Not Model Capability

- [Preflight](../../../research-audits/nov12-components/preflight.json): seeds 42/43/44, at most 180 seconds per run; no model/evaluation-data downloads, API calls, or pretrained-model calls.
- [Frozen source and proof](../../../research-audits/nov12-components/frozen-sources.json), [raw CPU](../../../research-audits/nov12-components/raw-cpu.json), and [raw CUDA](../../../research-audits/nov12-components/raw-cuda.json) bind the same actual source. CPU: eight × three; A100: three × three.
- A100 receipts: [BOPD](../../../gpu-validations/bopd-a100-20261112.json), [REAL Loss](../../../gpu-validations/real-loss-a100-20261112.json), and [OnlyAct](../../../gpu-validations/onlyact-a100-20261112.json).

The CUDA mechanism runner took approximately **1.37 seconds** in total. This times small-tensor/kernel execution, excluding research, transfer, and environment startup; it is not paper-training time. Inputs are explicit small tensors, finite policies, and contract fixtures without real checkpoints. Tests reject device changes, missing seeds, source drift, and promotion from diagnostics to formal comparisons.

All results retain `diagnostic_only=true`, `evaluation_tier=l1_mechanism`, and `formal_comparison=false`. Multiple seeds on a synthetic contract are not independent capability samples. Registering local operators is not unified executable Evolve integration: `promotion_eligible=false` and `evolve_integrated=false` remain in force.

## Full-System Cost and Theory Status

Seven full systems/experiments are not reproduced based on public configurations or material unresolved cost. There are no large downloads, cost probes, or automatic retries. Examples include BOPD's multi-GPU two-stage long rollouts, LCS's reported approximately 4,500 A100 GPU-hours, REAL's 140K-step multi-loss/serving matrix, and OnlyAct's video preprocessing and multiple world-model experiments. Millisecond gradient kernels do not replace those pipelines.

**APMD is separate:** it is theoretical. The finite-policy numerical kernel is implemented, but no large empirical protocol is provided to reproduce. Its status is `not_applicable_theory_only`, neither high-cost deferral nor a claim that all theorems were locally proved.

## Industrial Source Conflict: Unconfirmed, Not Altered or Accused

The [fixed SAM-D2Q record](../../../research-audits/nov12-components/industrial-source-exception.json) preserves the reported quantified AliExpress Search A/B and control descriptions. However, its training signals date to **August–November 2025**, while its A/B dates are **June 8–28, 2025**, without an explanation of the corresponding model versions.

This is **unconfirmed version/timeline correspondence**, not an allegation of fabrication. Neither year may be silently changed, and the earlier production model cannot be assumed to be the later-trained system. The non-blocking protocol exception is not catalogued, implemented, counted among the eight, or promoted to confirmed qualifying production evidence. Author clarification or a revised source can reopen it.

## Source Coverage and Remaining Review Boundaries

The [announcement index](../../../research-audits/nov12-components/announcement-index.json) records eight arXiv category `new` pages still showing November 11. Cross-lists and replacements produce **956 distinct source identities**. A `new` repository label means no matching repository record, **not 903 qualifying new papers, unfinished deliveries, or automatic tasks**. Unselected identities have not thereby received method review.

The [source differences](../../../research-audits/nov12-components/source-coverage.json) compare bounded Google first/last pages, Meta's curated home, and DeepMind's landing page. No added visible links does not establish no new papers institution-wide. Meta's main directory returned unavailable content; its alternative results page was readable via web rendering, but direct capture timed out and mixed historical years prevent chronological exhaustion claims. GSLM2 is already catalogued, not another new model. Watermark, coverage limits, and implementation evidence remain independent; the watermark stays November 9.

## Fresh Clones and Maintainer Source-Byte Rechecks

After installing repository dependencies, a fresh clone can validate **committed** scope/coverage/hash links, frozen source, actual executions, and GPU receipts without network access or original-paper caches:

```bash
PYTHONPATH=src python scripts/record_nov12_components.py --check
PYTHONPATH=src python -m pytest -q tests/test_nov12_evidence.py
```

This does not claim to reread original HTML/PDF bytes. Maintainers retaining this batch's `.cache/nov12-components/` captures can additionally run:

```bash
PYTHONPATH=src python scripts/record_nov12_components.py --check --recheck-source-captures
```

Initial ledger admission requires original-byte checks. Later default checks stay portable; explicit source rechecking fails for missing files or mismatched hashes rather than silently claiming success. Neither mode advances the watermark or reruns full paper experiments.
