# October 21, 2026: Follow-up to the same announcement, not a new publication round

<!-- source-sha256: c644817cf3103bb12c8873cd247836674579d158ba3ea1780d9e6fc33e24c1e3 -->

[简体中文](../../../research-audits/oct21-followup/README.md)

After [PR #217](https://github.com/daiwk/auto-research/pull/217) merged, we reread the announcements for eight arXiv categories and the official Google, Meta, and DeepMind catalogs. The catalogs yielded no new URLs and the announcement date did not change. This round addresses recent candidates not yet in the library, not papers newly published within a few hours.

## Fixed deliverables

| Paper | Scope | Full experiment |
| --- | --- | --- |
| A2D / Ask-to-Distill | Top-K union distribution, compatibility weights, and distillation formula and gradients | Not reproduced |
| Projected Distillation | Verified minimal-edit masks, diff-local DPO, and self-correct SFT | Not reproduced |
| Stratified Sparse Attention | Algorithm 1 adaptive heavy/residual allocation, deduplicated sampling, and inclusion-probability correction | Not reproduced |
| RACE | Paired-dimension selection preserving original RoPE frequencies, value subspaces, and native projection folding | Not reproduced |
| Agent S4 | Binary tournaments, lineage, feedback boundaries, and candidate-pool controller; no invented GUI/LLM interface | Not reproduced |
| Google ResidencyRL | Historical discovery, v1 on 2026-08-07; internal multi-turn Gemini GRPO | Not reproduced; no executable substitute |

The five components are L1 synthetic mechanism/controller diagnostics only: `diagnostic_only=true`, `promotion_eligible=false`, and `evolve_integrated=false`. Fixtures provide candidate programs or projected text; no generator was run. PyTorch attention references are not the paper's high-performance CUDA kernels or serving throughput.

## Cost and verification

We screened costs before starting. Every full experiment is **too costly and not reproduced (review DONE)**, with no automatic retries or training queue. No model weights or large datasets were downloaded. Four CUDA components ran from frozen source on one physical NVIDIA A100 with seeds 42/43/44; see the [GPU receipt](../../../gpu-validations/ask-to-distill-a100-20261021-followup.json). The CPU controller also ran from the same frozen commit. Per-paper metrics, source SHAs, raw artifact hashes, and offline-verifiable Git proofs distinguish execution from documentation; a GPU availability check is not execution.

Cross-review strengthened receipt binding: metrics, paper key, code commit, source SHA, seeds, data recipe, and metrics path must all match; tampering fails. The source baseline is bound to the last actual capture SHA to prevent bad input from being reported as no additions.

The [fixed scope and cost rationale](../../../research-audits/oct21-followup/task-scope.json), [actual source diff](../../../research-audits/oct21-followup/source-coverage.json), and [offline-verifiable frozen source proof](../../../research-audits/oct21-followup/frozen-sources.json) record selection, sources, and execution. Individual pages retain authors' code release status; an inaccessible URL does not justify inventing a usable repository or revision.

## Coverage limits

The 29 Google pages, six scoped Meta pages, and nine DeepMind pages are bounded checks, not exhaustive site coverage. Fully parsing announcements is not full-text review. Five recent discoveries and one August backfill are counted separately. **The cross-domain review watermark remains 2026-10-15**; selected deliveries do not close the entire window.

JEV reranking candidate 2610.28435 was outside this round and remains only a candidate in this record. Previously unconfirmed ASHF had no new primary source, so a repeated scan does not reopen it or justify inventing an algorithm.

```bash
PYTHONPATH=src python scripts/build_oct21_followup_artifacts.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
PYTHONPATH=src python -m pytest tests/test_oct21_followup_evidence.py
```
