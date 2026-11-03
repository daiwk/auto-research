# Shared evaluation protocol for search, ads, recommendation, and LLM applications

<!-- source-sha256: 739ed1d6b5469db413b35589ddb4498d30079e6566df35e75c247e0822351470 -->

[简体中文](../../reproductions/benchmark.md)

This protocol standardizes splits, baselines, metrics, and reporting. It does not rank every paper against DIN. Compare only on **matched data, candidate sets, budgets, and objectives**, and report the paper's online A/B separately.

## Evaluation tiers

| Task | Example methods | Default public data | Main metrics |
|---|---|---|---|
| Full-catalog retrieval or ranking | DIN, SASRec, generative retrieval, LLM-assisted recommendation | MovieLens-100K/1M, Amazon 5-core | Recall/Hit@K, NDCG@K |
| CTR/CVR and multitask learning | DeepFM, ESMM, MMoE, PLE, TWICE | Impression/conversion tasks from public interactions | AUC, log loss, task averages |
| Freshness and exploration | PinCLIP, Pinequalizer, YouTube Freshness | Timestamped MovieLens splits | Fresh-item Hit/NDCG, head share, overall quality |
| Long-term value and ad decisions | SWAG, GrowthGR, Causal Retrieval | Auditable windows or logged-policy proxies | Value/uplift proxies, constraints, ranking quality |
| Blending and page decisions | SORT-Gen, Memento, DeGRe, DRL-PUT | Public interaction lists or logged-policy proxies | List value, diversity, constraint satisfaction, ranking quality |
| Content understanding, moderation, and risk | MM-LLM, CORE, ASARL, RAMP | Public multimodal, relevance, or missing-field proxies | Relevance, precision/recall, false positives, quality and privacy guardrails |

## Common recommendation protocol

### Data and split

1. Sort interactions by user and time.
2. Default to leave-two-out: penultimate item for validation and last item for test.
3. Training reads only earlier history; validation and test must not leak.
4. Rank every eligible item, rather than inflating results with a small random candidate set containing one positive.
5. Controls and treatments share users, items, candidate sets, splits, and seeds.

The shared DIN setup uses MovieLens-100K, full-catalog ranking, and seeds 42/43/44. SERAL, LEADRE, COBRA, ARGUS, GR4AD, and MM-LLM historically used the same DIN NDCG@10 of `0.02167`. Cross-domain KD used a different target split with DIN `0.05518`. Do not directly compare the two.

### Metrics

$$
\operatorname{NDCG@K}
=\frac{1}{|\mathcal U|}
\sum_{u\in\mathcal U}
\frac{\sum_{r=1}^{K}(2^{rel_{u,r}}-1)/\log_2(r+1)}
{\operatorname{IDCG@K}_u}.
$$

- `Hit/Recall@K` measures whether the positive appears in the first K.
- `NDCG@K` accounts for hit and position.
- `fresh Hit/NDCG` is calculated only for new items.
- `head share` guards against exposure concentration; a decrease does not establish better overall results.
- AUC and log loss are for pointwise CTR/CVR, not a shared ranking with full-catalog NDCG.

## Content understanding, moderation, and risk

Distinguish improvements in content representations from downstream ranking lift, holding content corpus, interaction split, candidates, and seeds fixed. Moderation and risk methods must report main task metrics plus:

- Positive and negative precision and recall, with thresholds.
- False-positive and false-negative rates and distributions by content cohort.
- Guardrails on CTR, revenue, coverage, and other business metrics.
- Limits of dataset review, human review, and privacy proxies relative to production.

PPL, long context, and system performance are covered by the [foundation-model evaluation protocol](../foundation-models/benchmark.md).

## Local baseline selection

Every paper write-up must specify:

> **Local control:** What is the baseline, what changes in the treatment, and how much does the main metric change?

Prefer:

1. A direct baseline from the paper that can be implemented locally.
2. The closest implemented architecture for the same task.
3. A mechanism-isolating baseline.

DIN is not mandatory for every paper. Comparing ad bidding, delayed CVR, list blending, or risk control against DIN produces uninterpretable percentages. Use same-objective baselines and state them clearly.

## Online evidence and local experiments

| Evidence | What it supports | What it does not support |
|---|---|---|
| Paper's online A/B | Business change on the paper's traffic and product | The same gain in the local reproduction |
| Paper's offline result | Author model on the specified data or benchmark | Replacement for an online business outcome |
| Local public-data run | Executable adapter core and direction under the public protocol | Full replication of private production data |
| Local negative result | Gain did not transfer under this data, budget, and implementation | Universal refutation of the paper |

System-level A/B, such as Melo, needs separate attribution at the product level. Full-traffic papers such as TWICE must retain original metric names. Expected revenue, conversion, and standard ranking NDCG are not interchangeable.

## Reproducible artifacts

For each adapter retain an independent write-up, fixed-seed `metrics/*.json`, complete metadata and upstream code status, key original figures and their sources, the adapter key, local code path, commands, and fidelity limits.

Common verification commands:

```bash
PYTHONPATH=src pytest -q tests/reproductions
PYTHONPATH=src pytest -q tests/reproductions/test_documentation_catalog.py
python -m mkdocs build --strict
```

Retain positive, negative, and unstable multiseed results when experiments change. Keep checkpoints local and out of GitHub.
