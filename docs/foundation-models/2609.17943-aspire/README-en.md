# ASPIRE: Asynchronous Batch Self-Speculative Decoding

<!-- source-sha256: b4529bb7f1eb1a90b0b9963066b54079641eb107ba34c6f586ded0b8474c6de4 -->

[简体中文](README.md)

> L1 batch-aware scheduler and refresh gate, not an integrated vLLM serving engine.

## Paper information

| Field | Details |
|---|---|
| Paper | [ASPIRE: Asynchronous Batch Self-Speculative Decoding](https://arxiv.org/abs/2609.17943) |
| Institution | University of Southern California (first author). |
| First public release | 2026-09-16 (arXiv v1) |
| Author code | No public author repository found as of 2026-09-19. |
| Local adapter or method key | `aspire` |
| Local reproduction code | [`src/auto_research/foundation_latest_20260919.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/foundation_latest_20260919.py) |

## Paper method and evidence

Choose each request's draft length from online acceptance and current batch cost. Periodic full-attention refresh corrects the self-speculative state.

```mermaid
flowchart LR
  A[Online acceptance and batch cost] --> D[Per-request draft length]
  D --> R[Refresh gate]
  R --> F[Periodic full-attention correction]
```

<!-- paper-figure:start -->
### Original paper figure

[![ASPIRE paper figure](assets/paper-figure-01.png)](https://arxiv.org/html/2609.17943v1/method.png)

Figure 2 shows request-level draft scheduling and refresh. From the [original paper](https://arxiv.org/abs/2609.17943); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equation

The reference exposes schedule, gate, and state updates in the metrics; variables and invariants are tested.

### Reported results

Paper serving, benchmark, and training results are not local measurements.

## Local reproduction

[Three-seed mechanism results](metrics/mechanism-seeds42-44.json) are diagnostic_only=true. Fixed-budget fixtures verify the defining operator and auditable intermediate states; they are not a benchmark, production result, or capability-ranking entry. The CUDA path ran on a real NVIDIA A100; see sanitized receipts under `docs/gpu-validations/`. No vLLM engine modification or paper throughput claim.
