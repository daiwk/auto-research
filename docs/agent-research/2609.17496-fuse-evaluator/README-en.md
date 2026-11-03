# Verifiable Social Reasoning for LLM Assistants

<!-- source-sha256: d671cea8c8daefd92800ec9b34b94b2f627505aa4b348240afd5d4a99300ef11 -->

[简体中文](README.md)

> **L1 core-mechanism diagnostic.** Runs only the observation-safe evaluation state machine; does not call 12 external LLMs.

## Paper information

| Field | Details |
|---|---|
| Paper | [Verifiable Social Reasoning for LLM Assistants](https://arxiv.org/abs/2609.17496) |
| Organization | First-author affiliations: Google Research / Hebrew University of Jerusalem / University of Cambridge |
| First public release | 2026-09-15 (arXiv v1) |
| Authors' code | No public author repository was found as of 2026-09-16. |
| Adapter / method | `fuse-evaluator` |
| Local reproduction code | [`src/auto_research/agent_research/latest_20260916.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260916.py) |

## Original paper

### Motivation and method

Multi-agent simulations with verifiable hidden motivations evaluate user retelling, framing bias, and social reasoning.

The local reference kernel retains decisive gates, weights, or state transitions and exposes auditable intermediates so related methods can be compared at a common budget.

~~~mermaid
flowchart LR
  I[Public input and current state] --> M[fuse-evaluator mechanism]
  M --> A[Auditable intermediates]
  A --> O[Output or state update]
~~~

<!-- paper-figure:start -->
### Key figure from the paper

[![Verifiable Social Reasoning for LLM Assistants, Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.17496v1/assets/viz1.png)

> **Figure 1:** Overview of the paper's method and its key components. From the [original paper](https://arxiv.org/abs/2609.17496); copyright remains with the authors. Click the image for the source.
<!-- paper-figure:end -->

### Core computation

The implementation preserves the paper's decisive state transitions and reports weights, gates, depth, stages, or cache statistics. Fixed budgets and three seeds check mechanism invariants only, not paper-scale training.

### Paper results

The paper's capability, speed, or cost findings are original evidence only. Local metrics are not directly compared with them or extrapolated to online gains.

## Local reproduction

See the [three-seed results](metrics/mechanism-seeds42-44.json). The common receipt marks `diagnostic_only=true`, so the public dashboard does not treat it as a full capability improvement.

### Reproduction boundaries

The local run executes only an observation-safe evaluation state machine and does not call 12 external LLMs.
