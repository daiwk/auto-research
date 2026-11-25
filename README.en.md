# Auto Research: 410+ AI Paper Implementations, Public Experiment Audits & Automated Model Evolution

<!-- source-sha256: b0e39389672678022b80a90c60e003dc3170d86ff4de4b9354b1e1f58ecc072d -->

[简体中文](README.md) · English

> **Go beyond reading papers—verify them with executable code and public data.**  
> Spanning **Search, Ads & Recommendation (RecSys), Foundation Models, LLM Post-Training, Agents, Multimodal Models, and Structured Decisions**. Auto Research brings together **410+ standardized paper adapters, 4-layer interactive learning cards, cross-paper deep dives, multi-seed public experiment dashboards (retaining negative results)**, and **multi-generation automated model evolution**.

[![Python quality](https://github.com/daiwk/auto-research/actions/workflows/quality.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/quality.yml)
[![Documentation](https://github.com/daiwk/auto-research/actions/workflows/docs.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/docs.yml)

🌐 **[English documentation](https://daiwk.github.io/auto-research/en/) · [English paper catalog (410+)](docs/en/papers/index.md) · [Learning cards](docs/en/learning/index.md) · [Topic deep dives](docs/en/learning/deep-dives/index.md) · [Public experiment dashboard](docs/en/public-experiment-dashboard.md) · [Installation and demos](docs/en/setup.md)**

⭐ *If you find our paper implementations, 4-layer learning cards, or experiment audits helpful, please give this repository a **Star** to stay updated!*

## Key Highlights

1. **Strict Reproduction Fidelity Tiers (No Fake Reproductions)**: The repository currently registers **410** paper adapters, strictly distinguishing between `full_pipeline`, `core_mechanism`, and heuristic `concept_demo` implementations. Proxy scoring functions or fixed heuristics are never passed off as paper reproductions.
2. **Production A/B Evidence Audits & Negative Results Retained**: Industrial RecSys papers are audited for real production traffic and online A/B metrics. Local public-data experiments follow L0–L3 evaluation tiers and multi-seed statistics (fewer than 3 seeds are labeled as smoke tests and cannot claim stable gains), **transparently preserving negative results and non-reproduced boundaries**.
3. **4-Layer Q&A Cards & Cross-Paper Deep Dives**: Every paper is broken down into interactive Q&A cards across four progressive layers (*Fundamentals → Core Mechanism → Method Comparison → Implementation Details*), paired with topic-level deep dives that incrementally compare trade-offs across papers.
4. **Safe, Data-Isolated Automated Model Evolution (`evolve` & `run`)**: Evolve models across recommendation (`RankMixer`, `HyFormer`, `GenRec`), `micro-llm` (architecture, data mixture, SFT, GRPO), and Agents using tested whitelist operators—selecting candidates strictly on validation splits before running isolated test evaluations.

## Explore the library without installing anything

- **Find a paper.** The English catalog links to original publications and bilingual project write-ups across all six research domains.
- **Learn a method.** The [English learning cards](docs/en/learning/index.md) cover fundamentals, mechanisms, comparisons, and implementation. [Topic deep dives](docs/en/learning/deep-dives/index.md) compare papers across those levels.
- **Check what was actually measured.** The [public experiment dashboard](docs/en/public-experiment-dashboard.md) indexes committed results by domain, method, dataset, and metric. It retains negative results and evaluation limits. The site's [video tour](docs/assets/media/site-tour.mp4) demonstrates the Chinese interface.
- **Run your own research.** The [automated research and evolution workflow](docs/en/auto-research.md) retrieves evidence, executes registered components under a fixed protocol, selects candidates on validation data, and evaluates selected candidates on isolated test data. A retrieved paper is not automatically executable code.

The repository maintains a registry of paper adapters. A paper listing, an executable mechanism diagnostic, and a capability-level reproduction are different things. Check the paper's own evidence before interpreting a result.

## Start locally

The CLI requires macOS or Linux and Python 3.11 or later.

```bash
git clone https://github.com/daiwk/auto-research.git
cd auto-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
auto-research --help
auto-research list
```

See [Installation, datasets, and demos](docs/en/setup.md) for optional training dependencies, CPU/MPS/CUDA examples, and the smallest demos. Downloads depend on the experiment you choose; subsequent runs can reuse local data and checkpoint caches.

## Evidence and contribution

Results reported by the original paper, including production A/B tests, are distinct from local public-data experiments. A diagnostic can validate a mechanism without reproducing the paper's model or headline result. Full experiments that exceed the project budget are explicitly marked **not reproduced**; this does not place them in a retry queue. New CUDA implementations require evidence from an actual A100 or A30 run.

To contribute, see [Issues](https://github.com/daiwk/auto-research/issues), [repository instructions](AGENTS.md), and the [bilingual documentation workflow](docs/en/contributing.md). Update Chinese and English write-ups and learning material together, sharing original figures and result artifacts. The [architecture guide](docs/en/architecture.md) explains adapter, data-isolation, and evaluation contracts. The [translation coverage report](docs/en/coverage.md) tracks all site pages.


## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=daiwk/auto-research&type=Date)](https://star-history.com/#daiwk/auto-research&Date)
