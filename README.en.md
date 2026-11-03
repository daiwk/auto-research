# Auto Research

<!-- source-sha256: 5b9fa4cbbfd56c1d9712979533848faacaf1b4120d984b29ebbe5fbb0d481844 -->

[简体中文](README.md) · English

Read research papers, inspect their implementations, and run iterative experiments with public data. Auto Research covers search, advertising, recommendation and LLM applications; foundation models; structured decisions; multimodal models; LLM post-training; and agents.

[![Python quality](https://github.com/daiwk/auto-research/actions/workflows/quality.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/quality.yml)
[![Documentation](https://github.com/daiwk/auto-research/actions/workflows/docs.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/docs.yml)

**[English documentation](https://daiwk.github.io/auto-research/en/) · [English paper catalog](docs/en/papers/index.md) · [Installation and demos](docs/en/setup.md)**

## Explore the library without installing anything

- **Find a paper.** The English catalog lists the research domains and links to original papers and available English write-ups. Older entries without translations are labeled, with the Chinese write-up still available.
- **Learn a method.** The [learning cards](https://daiwk.github.io/auto-research/learning/) cover fundamentals, mechanisms, comparisons, and implementation. The [topic deep dives](https://daiwk.github.io/auto-research/learning/deep-dives/) compare papers across those levels. The learning-card collection is currently in Chinese.
- **Check what was actually measured.** The [public experiment dashboard](https://daiwk.github.io/auto-research/public-experiment-dashboard/) indexes committed results by domain, method, dataset, and metric. It retains negative results and evaluation limits. The site's [video tour](docs/assets/media/site-tour.mp4) demonstrates the Chinese interface.
- **Run your own research.** The [automated research and evolution workflow](docs/auto-research.md) retrieves evidence, executes registered components under a fixed protocol, selects candidates on validation data, and evaluates selected candidates on isolated test data. A retrieved paper is not automatically executable code.

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

To contribute, see [Issues](https://github.com/daiwk/auto-research/issues), [repository instructions](AGENTS.md), and the [bilingual documentation workflow](docs/en/contributing.md). Submit new or updated paper write-ups in Chinese and English together, reuse their source figures and result artifacts, and keep the Chinese learning questions and topic deep dives up to date. The [architecture guide (Chinese)](docs/architecture.md) explains adapter, data-isolation, and evaluation contracts.
