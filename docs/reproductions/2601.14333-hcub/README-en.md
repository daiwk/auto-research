# HCUB: hierarchical contextual uplift bandit

<!-- source-sha256: 38f22a70607cef9005ccb838db5d5ae6cfd87043538506da35235854912efdb6 -->

[简体中文](README.md)

> **Fidelity: core mechanism.** Runs the defining mechanism verifiable on public data. Private data, production models, and serving remain outside scope.

## Paper information

| Field | Details |
|---|---|
| Paper | [arXiv 2601.14333](https://arxiv.org/abs/2601.14333) |
| Organization | Dream11 |
| First public release | 2026-01-20 (arXiv v1) |
| Authors' code | No public author code was found when checked on 2026-09-05. |
| Adapter / method | `hcub` |
| Local reproduction code | [`src/auto_research/reproductions/hcub/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/hcub/) |

## Original paper

### Motivation and method

Choose granularity dynamically in a user and system context tree. Sparse child nodes inherit reward from parents to improve cold starts. The policy directly estimates action uplift instead of just fitting observed absolute clicks.

```mermaid
flowchart LR
  A["Public behavior and candidates"] --> B["HCUB core mechanism"]
  B --> C["Matched-budget method output"]
  A --> D["Common direct baseline"]
  C --> E["Full-catalog ranking and structural diagnostics"]
  D --> E
```

<!-- paper-figure:start -->
### Key figure from the paper

[![HCUB: hierarchical contextual uplift bandit — Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2601.14333v1/g290.png)

> **Figure 2:** Overview of the paper's method and key components. From the [original paper](https://arxiv.org/abs/2601.14333); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equations

$$
a_t=\arg\max_a\hat\tau(a\mid c_t)+\beta U(a,c_t),\qquad R(c)=\eta R_{local}+(1-\eta)R_{parent}.
$$

### Paper results

Dream11 reports online revenue +0.51%, engagement +0.42%, and about 4%–5% lower offline regret. This is paper evidence, not a local public-data outcome.

## Local reproduction

> **Local comparison:** Under the same full-catalog MovieLens protocol, baseline NDCG@10 is 0.05401 and treatment NDCG@10 is 0.04886, **-9.53%** relative. The local proxy and production task differ, so there is no extrapolation to online lift.

See the [three-seed artifact](metrics/public-seeds42-44.json) for complete results, means, standard deviations, and 95% confidence intervals.

```bash
auto-research reproduce --paper hcub --dataset-dir data --seeds 42,43,44
```

## Reproduction boundaries

The local run uses a fixed public MovieLens 100K subset and auditable proxies to check the core computation only. It does not reproduce private logs, the production foundation model, online traffic assignment, or serving. There is no claim to reproduce absolute paper metrics or online gains.
