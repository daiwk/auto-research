# Foundation model research

<!-- source-sha256: 123c5b88e19d87ca6c69cc09d8af619cb2564456870f2f51bb4002bfa28d8219 -->

[简体中文](../../foundation-models/README.md)

Recent scaled mechanism experiment: [KITE/SST two-tower and three-seed WikiText-2 results](../experiments/sep28-three-mechanisms.md). This is a CPU diagnostic, not a reproduction of the 67B paper setup.

Foundation model research covers core model behavior before post-training and during inference: architecture, pretraining data and optimization, multimodal representations, long context, and inference efficiency. Paper write-ups remain at stable URLs. This catalog provides a new way to browse them without breaking old links.

## Research scope

| Direction | Main questions | Current public evaluation |
|---|---|---|
| Architecture | MoE, state spaces, conditional memory, recursion, and residual paths | WikiText-2 perplexity, parameter count, training stability |
| Attention and long context | Sparse/gated attention, positional encodings, KV compression | Perplexity, attention edges, KV footprint, long-context tasks |
| Pretraining and data | Data cleaning, selection, mixture, and optimization | Matched-token/step perplexity and task metrics |
| Multimodal foundations | Visual tokens, cross-modal retrieval, and shared representations | Public multimodal benchmarks or auditable scaled experiments |
| Inference and system efficiency | Dynamic compute, quantization, and speculative decoding | Quality, latency, throughput, peak memory, and compression |

## Browse

- [Methods index](catalog.md): Foundation-model papers, institutions, dates, author code, and local entry points.
- [By institution, company, or university](catalog/by-organization.md): Grouped by the first author's first listed affiliation.
- [By topic](catalog/by-topic.md): Direction → method family → paper.
- [By year](catalog/by-year.md): Newest first within each year by original publication date.
- [Paper lineage and limits](lineage.md): Covered research lines, completed capabilities, and reproduction limits.
- [Shared evaluation protocol](benchmark.md): Comparable quality, compute, and fidelity.
- [Scaling-law budget grid](scaling-law.md): Resumable model-size by data-budget experiments with per-point errors and fit limits.
- [System One / Jev](../system-one/README.md): Typed decisions, adjacent open implementations, Banking77 calibration, and executable Evolve operators.

## Recent implementations

- [RD-AttnRes](../../reproductions/2608.01075-rd-attnres/README-en.md) learns separate QK and V depth routing over the same Block AttnRes residual sources. It is integrated into micro-LLM Evolve, with the 30-step negative result retained.
- [MACRO](../../reproductions/2608.05872-macro/README-en.md) and [HiLP](../../reproductions/2608.05806-hilp/README-en.md) add dynamic layer routing and hierarchical latent prediction, respectively, and are integrated into micro-LLM Evolve.
- [QEvict](../../reproductions/2608.05326-qevict/README-en.md), [BaKron](../../reproductions/2608.06291-bakron/README-en.md), and [DBLast](../../reproductions/2608.05448-dblast/README-en.md) cover recoverable KV eviction, second-order Kronecker quantization, and correlated-block speculative drafting. Each has a standalone adapter and fixed metrics.

## Boundaries with post-training and applications

- DPO, GRPO, OPD, and reward models belong in [LLM post-training](../post-training/README.md).
- LLM features, generative retrieval, and multimodal content applications in industry belong in [search, ads, recommendation, and LLM applications](../reproductions/industrial.md).
- Planning, tools, memory, and environment interaction belong in [agent research](../agent-research/README.md).
- A genuinely cross-domain paper can appear in several indexes but has one stable write-up and one set of local metrics.

## Relationship to Auto Research

Network operators, data strategies, and efficiency methods that pass actual training and testing can enter micro-LLM Evolve. Discovered papers without implementations are evidence only; they do not produce unchecked training code at runtime.

```mermaid
flowchart LR
  P["Papers and public implementations"] --> A["Trainable adapters"]
  A --> G["Architecture, data, and efficiency genome"]
  G --> E["Matched-budget parallel experiments"]
  E --> V["Validation selection"]
  V --> G
  V --> T["Isolated test and research report"]
```
