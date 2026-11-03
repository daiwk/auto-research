# FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators

<!-- source-sha256: f865ae21ea4399ff514e65a5fa17eb15942867e32c66b804b5bbc1e22d0d8d60 -->

[简体中文](README.md)

> **L1 core-mechanism diagnostic.** Executes rollout-state detachment and local-kernel KL, not image flow-map generator training.

## Paper information

| Field | Details |
|---|---|
| Paper | [arXiv 2609.37851](https://arxiv.org/abs/2609.37851) |
| Organization | First-author affiliation: Georgia Institute of Technology |
| First public release | 2026-09-29 (arXiv v1) |
| Authors' code | [Public implementation](https://github.com/ZhiqiLi-CG/Flowmap_OPD_source) |
| Adapter | `flowmap-opd` |
| Local reproduction code | [`src/auto_research/post_training/latest_20261001.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/post_training/latest_20261001.py) |

## Original paper

### Motivation and method

Separate the rollout distribution that produces states from the teacher–student comparison kernel. Rollout supplies states with the correct marginal distribution. On frozen states, the optimization kernel compares flow maps, induced velocities, or instantaneous velocities.

~~~mermaid
flowchart LR
  I[Public input and current state] --> M[FlowMap-OPD mechanism]
  M --> A[Auditable intermediates]
  A --> O[Output or state update]
~~~

<!-- paper-figure:start -->
### Key figure from the paper

[![FlowMap-OPD, Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2609.37851v1/flowmap_opd_teaser.png)

> **Figure 1:** Method overview and components. From the [original paper](https://arxiv.org/abs/2609.37851); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equation

$L(\theta)=\mathbb E_{z\sim\rho^\theta}[\ell(\theta,T;z)]$. The local version detaches rollout states from the computation graph and updates the student only through the local KL kernel.

### Paper results

The paper validates few-step students on ImageNet and consolidation of multiple specialist teachers. The local run checks only rollout/kernel gradient isolation.

## Local reproduction

> **Local comparison:** The baseline disables the mechanism or uses default state, and the treatment enables the core operator. Only invariants and state transitions are checked; cross-model relative change is not applicable.

See the [three-seed diagnostic](metrics/mechanism-seeds42-44.json). `diagnostic_only=true` indicates runnable core transitions, gradients, or scheduling invariants only, not formal capability ranking.

## Reproduction boundaries

Rollout-state detachment and local-kernel KL are implemented. No image flow-map generator was trained.
