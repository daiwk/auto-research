# ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest

<!-- source-sha256: ed00e55584024a71b36b3bfd33795fac8ec276a98a8670f651e2395af8a29ef0 -->

[简体中文](README.md)

> **Fidelity: core mechanism.** Paper online outcomes, local public-data results, and omissions are reported separately.

## Paper information

| Field | Details |
|---|---|
| Paper | [arXiv 2602.09194](https://arxiv.org/abs/2602.09194) |
| Organization | Pinterest |
| First public release | 2026-02-09 (arXiv v1) |
| Authors' code | The paper did not provide official or author code when checked on 2026-08-24. |
| Adapter / method | `ml-dcn` |
| Local reproduction code | [`src/auto_research/reproductions/ml_dcn/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/ml_dcn/) |

## Original paper

### Motivation and method

Replace DCNv2's full-dimensional crosses with low-rank crosses of adjustable internal width. A learned mask selects cross channels, increasing capacity at the same FLOPs.

```mermaid
flowchart LR
 A["Sparse features"] --> B["Masked low-rank cross"] --> C["Ads CTR"]
```

<!-- paper-figure:start -->
### Key figure from the paper

[![ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest — Figure 1](assets/paper-figure-01.png)](https://arxiv.org/html/2602.09194v1/figures/mldcn.png)

> **Figure 1:** Core architecture, modules, and connections. From the [original paper](https://arxiv.org/abs/2602.09194); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equations

$$
x_{l+1}=x_l+x_0\odot[U_l(V_l(x_l\odot m_l))]+b_l
$$

### Paper results

Production A/B reports **platform-wide CTR +1.89%** at neutral cost (Section 4.2, Table 6). The private paper protocol is not directly comparable with local MovieLens measurements.

## Local reproduction

> **Local comparison:** The baseline is the shared transition + content scorer. The treatment adds only ml-dcn on the same users, items, full-catalog candidates, and seed.

MovieLens-100K, 220 users and 360 items, seed 42: NDCG@10 0.0540 → **0.0529 (-2.08%)**; Hit@10 0.1091 → 0.1091. Validation selects mixture weights only; the test set is not used for tuning.

```bash
auto-research reproduce --paper ml-dcn --dataset-dir data --seed 42
```

See the [fixed metrics](metrics/public-seed42.json).

## Reproduction boundaries

The core mechanism runs on MovieLens-100K with the same split, fixed full-catalog candidates, and seed. Private features, the production foundation model, and online traffic are unavailable. The implementation has independent model state and scoring and retains negative results. Local changes and paper A/B gains are reported separately.
