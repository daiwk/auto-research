# HPGR: hierarchical preference-aware generative recommendation

<!-- source-sha256: f3830a2b527f296dca599a8a40d618b56e859d9bda7e4077ce4796f27f2626f7 -->

[简体中文](README.md)

> **Fidelity: core mechanism.** Runs the defining mechanism verifiable on public data. Private data, production models, and serving remain outside scope.

## Paper information

| Field | Details |
|---|---|
| Paper | [arXiv 2603.00980](https://arxiv.org/abs/2603.00980) |
| Organization | Harbin Institute of Technology |
| First public release | 2026-03-01 (arXiv v1) |
| Authors' code | No public author code was found on 2026-09-05. |
| Adapter / method | `hpgr` |
| Local reproduction code | [`src/auto_research/reproductions/hpgr/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/hpgr/) |

## Original paper

### Motivation and method

Learn hierarchical behavior with session-based masked item modeling. At fine-tuning, preference-guided sparse attention retains only events most relevant to current intent, reducing noise and computation in flattened long sequences.

```mermaid
flowchart LR
  A["Public behavior and candidates"] --> B["HPGR core mechanism"]
  B --> C["Matched-budget method output"]
  A --> D["Common direct baseline"]
  C --> E["Full-catalog ranking and structural diagnostics"]
  D --> E
```

<!-- paper-figure:start -->
### Key figure from the paper

[![HPGR: hierarchical preference-aware generative recommendation — Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2603.00980v1/architecture.png)

> **Figure 2:** Core architecture, modules, and connections. From the [original paper](https://arxiv.org/abs/2603.00980); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equations

$$
u=\sum_s\alpha_s\operatorname{Pool}(H_s),\qquad \mathcal A=\operatorname{TopK}_j\langle u,h_j\rangle.
$$

### Paper results

An industrial AppGallery online A/B test reports eCPM +1.99%. This is paper evidence, not a local public-data outcome.

## Local reproduction

> **Local comparison:** Under the same full-catalog protocol, baseline NDCG@10 is 0.05401 and HPGR NDCG@10 is 0.05467, **+1.23%** relative. The local proxy does not extrapolate to online lift.

See the [three-seed artifact](metrics/public-seeds42-44.json) for complete results, means, standard deviations, and 95% confidence intervals.

```bash
auto-research reproduce --paper hpgr --dataset-dir data --seeds 42,43,44
```

## Reproduction boundaries

The local run uses a public MovieLens-1M subset and auditable proxies to validate the core computation. It does not reproduce private logs, production models, online traffic assignment, or serving. No claim is made to reproduce absolute paper metrics or online gains.
