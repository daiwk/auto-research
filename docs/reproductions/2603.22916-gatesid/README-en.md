# GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation

<!-- source-sha256: d38a5d7bffe2c47d2a4df6b31da3e87b2df0afe53dac5ac1f41b3057f32b0da7 -->

[简体中文](README.md)

> **Fidelity: core mechanism.** Paper online outcomes, local public-data results, and omissions are reported separately.

## Paper information

| Field | Details |
|---|---|
| Paper | [arXiv 2603.22916](https://arxiv.org/abs/2603.22916) |
| Organization | Alibaba International Digital Commerce |
| First public release | 2026-03-24 (arXiv v1) |
| Authors' code | The paper did not provide official or author code when checked on 2026-08-24. |
| Adapter / method | `gatesid` |
| Local reproduction code | [`src/auto_research/reproductions/gatesid/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/gatesid/) |

## Original paper

### Motivation and method

Shared attention fuses semantic and collaborative behaviors. A cold-start-aware gate adjusts contrastive alignment: new items lean on semantics while popular items retain collaborative signals.

```mermaid
flowchart LR
 A["Semantic and collaborative sequences"] --> B["GFSA and GRCA"] --> C["Cold-start ranking"]
```

<!-- paper-figure:start -->
### Key figure from the paper

[![GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation — Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2603.22916v2/gatesidv3_cropped.png)

> **Figure 2:** Core architecture, modules, and connections. From the [original paper](https://arxiv.org/abs/2603.22916); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equations

$$
z_i=g_i z_i^{sem}+(1-g_i)z_i^{coll},\quad g_i=\sigma(Wx_i)
$$

### Paper results

Online GMV rose **+2.60%** with 20% traffic over two weeks (Section 3.4). The private paper protocol is not directly comparable with local MovieLens measurements.

## Local reproduction

> **Local comparison:** The baseline is the shared transition + content scorer. The treatment adds only gatesid on the same users, items, full-catalog candidates, and seed.

MovieLens-100K, 220 users and 360 items, seed 42: NDCG@10 0.0540 → **0.0729 (+34.95%)**; Hit@10 0.1091 → 0.1273. Validation selects mixture weights only; the test set is not used for tuning.

```bash
auto-research reproduce --paper gatesid --dataset-dir data --seed 42
```

See the [fixed metrics](metrics/public-seed42.json).

## Reproduction boundaries

The core mechanism runs on MovieLens-100K with the same split, fixed full-catalog candidates, and seed. Private features, the production foundation model, and online traffic are unavailable. The implementation has independent model state and scoring and retains negative results. Local changes and paper A/B gains are reported separately.
