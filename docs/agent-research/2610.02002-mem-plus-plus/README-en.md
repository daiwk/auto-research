# Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents

<!-- source-sha256: 7451ca1d55f90a1c8807fc64076c57e45ab4b0b8a131b64f982f3d32d5e6a138 -->

[简体中文](README.md)

> L1 complete writes, temporal filtering and hybrid retrieval; no OrgMemBench or external embedding service.

## Paper information

| Field | Details |
|---|---|
| Paper | [arXiv 2610.02002](https://arxiv.org/abs/2610.02002) |
| Institution | The University of Texas at Austin (first author). |
| First public release | 2026-10-01 (arXiv v1) |
| Author code | [AIDAChip-Inc/mem-plus-plus](https://github.com/AIDAChip-Inc/mem-plus-plus). |
| Local adapter or method key | `mem-plus-plus` |
| Local reproduction code | [`src/auto_research/agent_research/latest_20261002.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20261002.py) |

## Paper method and evidence

Keep full documents, dates, and authors; do not irreversibly summarize at write time. At retrieval, filter by the question's as-of date before fusing lexical and semantic scores.

```mermaid
flowchart LR
  D[Store complete document and metadata] --> F[Filter by question time]
  F --> R[Combine lexical and semantic ranking]
```

<!-- paper-figure:start -->
### Original paper figure

[![Mem++ paper figure](assets/paper-figure-01.png)](https://arxiv.org/pdf/2610.02002)

The original figure documents the memory protocol. From the [original paper](https://arxiv.org/abs/2610.02002); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equation

$score(d,q)=BM25(d,q)+sim(e_d,e_q)$, eligible only if $time(d)\le time(q)$.

### Reported results

The paper reports +8.0–13.1 points over the strongest memory baseline on OrgMemBench and +2.6 for gpt-4.1-mini versus RAG.

## Local reproduction

[Three-seed mechanism results](metrics/mechanism-seeds42-44.json) are diagnostic_only=true. Fixed-budget fixtures verify the defining operator and auditable intermediate states; they are not a benchmark, production result, or capability-ranking entry. The comparator is the disabled/default operator.
