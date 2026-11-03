# SMES: scalable sparse experts for multitask learning

<!-- source-sha256: 21e240e5aec57fa97e5f99d3d151ac8c399d512f953dbddc611cc33eba326d1c -->

[简体中文](README.md)

> **Fidelity: core mechanism.** Runs the defining mechanism verifiable on public data. Private data, production models, and serving remain outside scope.

## Paper information

| Field | Details |
|---|---|
| Paper | [arXiv 2602.09386](https://arxiv.org/abs/2602.09386) |
| Organization | Kuaishou Technology |
| First public release | 2026-02-10 (arXiv v1) |
| Authors' code | No public author code was found on 2026-09-05. |
| Adapter / method | `smes` |
| Local reproduction code | [`src/auto_research/reproductions/smes/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/smes/) |

## Original paper

### Motivation and method

Split each task's active experts into a stable subset shared across tasks and an adaptive private subset. Cross-task global load balancing constrains routing, activation count, and expert skew.

```mermaid
flowchart LR
  A["Public behavior and candidates"] --> B["SMES core mechanism"]
  B --> C["Matched-budget method output"]
  A --> D["Common direct baseline"]
  C --> E["Full-catalog ranking and structural diagnostics"]
  D --> E
```

<!-- paper-figure:start -->
### Key figure from the paper

[![SMES: scalable sparse experts for multitask learning — Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2602.09386#page=4)

> **Figure 2:** Core architecture, modules, and connections. From the [original paper](https://arxiv.org/abs/2602.09386); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equations

$$
h_t=\sum_{e\in E_s\cup E_t}g_{t,e}(x)f_e(x),\qquad \mathcal L=\sum_t\mathcal L_t+\lambda\mathcal L_{balance}.
$$

### Paper results

Kuaishou reports online watch time +0.31%, GAUC +0.29%, and around 50% fewer active experts. This is paper evidence, not a local public-data outcome.

## Local reproduction

> **Local comparison:** Under the same full-catalog protocol, baseline NDCG@10 is 0.05401 and SMES NDCG@10 is 0.05359, **-0.78%** relative. The local proxy does not extrapolate to online lift.

See the [three-seed artifact](metrics/public-seeds42-44.json) for complete results, means, standard deviations, and 95% confidence intervals.

```bash
auto-research reproduce --paper smes --dataset-dir data --seeds 42,43,44
```

## Reproduction boundaries

The local run uses a fixed public MovieLens 100K subset and auditable proxies to validate the core computation. It does not reproduce private logs, production models, online traffic assignment, or serving. No claim is made to reproduce absolute paper metrics or online gains.
