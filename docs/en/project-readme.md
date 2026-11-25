# Auto Research: 410+ AI Paper Implementations, Public Experiment Audits & Automated Model Evolution

<!-- source-sha256: b83c6c3efa57cb6db5e82321872a857b42486565afa0a8ed1eed70fb25b3328b -->

[简体中文](../project-readme.md)

[English README on GitHub](https://github.com/daiwk/auto-research/blob/main/README.en.md) · [English documentation](index.md)

> **Go beyond reading papers—verify them with executable code and public data.**  
> Spanning **Search, Ads & Recommendation (RecSys), Foundation Models, LLM Post-Training, Agents, Multimodal Models, and Structured Decisions**. Auto Research brings together **410+ standardized paper adapters, 4-layer interactive learning cards, cross-paper deep dives, multi-seed public experiment dashboards (retaining negative results)**, and **multi-generation automated model evolution**.

[![Python quality](https://github.com/daiwk/auto-research/actions/workflows/quality.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/quality.yml)
[![Documentation](https://github.com/daiwk/auto-research/actions/workflows/docs.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/docs.yml)

**[Open the site](index.md) · [Learn paper by paper](learning/index.md) · [Research library](research-library.md) · [Topic deep dives](learning/deep-dives/index.md) · [Experiment dashboard](public-experiment-dashboard.md)**

⭐ *If you often use the site's learning cards, code implementations, or experiment comparisons, give the repository a **Star** to find the latest updates again.*

## Key Highlights

1. **Strict Reproduction Fidelity Tiers (No Fake Reproductions)**: The repository currently registers **410** paper adapters, strictly distinguishing between `full_pipeline`, `core_mechanism`, and heuristic `concept_demo` implementations. Proxy scoring functions or fixed heuristics are never passed off as paper reproductions.
2. **Production A/B Evidence Audits & Negative Results Retained**: Industrial RecSys papers are audited for real production traffic and online A/B metrics. Local public-data experiments follow L0–L3 evaluation tiers and multi-seed statistics (fewer than 3 seeds are labeled as smoke tests and cannot claim stable gains), **transparently preserving negative results and non-reproduced boundaries**.
3. **4-Layer Q&A Cards & Cross-Paper Deep Dives**: Every paper is broken down into interactive Q&A cards across four progressive layers (*Fundamentals → Core Mechanism → Method Comparison → Implementation Details*), paired with topic-level deep dives that compare trade-offs across papers and are checked and updated as new papers are added.
4. **Safe, Data-Isolated Automated Model Evolution (`evolve` & `run`)**: Evolve models across recommendation (`RankMixer`, `HyFormer`, `GenRec`), `micro-llm` (architecture, data mixture, SFT, GRPO), and Agents using tested whitelist operators—selecting candidates strictly on validation splits before running isolated test evaluations.

## Take a tour of the site

Browse papers by topic, expand questions and answers, and check experiment evidence in the site without installing anything. The animation uses footage from the live site and takes less than a minute.

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="../../assets/media/site-tour-poster.webp">
  <img src="../../assets/media/site-tour.webp" alt="Site tour: paper search, four levels of questions, illustrative examples and sources, recent additions, and the public experiment dashboard" width="1080">
</picture>

[Watch the pausable MP4](../assets/media/site-tour.mp4) · [Tour content and production](assets/media/README.md)

## What you can do

| Task | Where to go | What you will find |
|---|---|---|
| Find related papers | [Paper implementation and evaluation](research-library.md) | Browse by domain, institution, topic, and date. Read write-ups with equations and code. |
| Work through one paper | [Learning cards](learning/index.md) | Basics → core mechanism → method comparison → implementation details. Expand answers, examples, and sources as needed. |
| Compare papers on a topic | [Topic deep dives](learning/deep-dives/index.md) | Mechanism comparisons, trade-offs, and cross-paper Q&A. Each card is updated as relevant papers arrive. |
| Pick up where you left off | [Recent questions](learning/recent.md) | Questions added to both recent and older papers, with filters for topic and learning level. |
| Interpret an experiment | [Public experiment dashboard](public-experiment-dashboard.md) | Data, baselines, metrics, seeds, and verification tiers, with negative results and reproduction limits retained. |
| Run a research experiment | [Automated research and evolution](auto-research.md) | Execute implemented paper components, select candidates on validation, then evaluate on the isolated test split. |

The repository registers **410** paper adapters. Cataloged papers, mechanism diagnostics, and full capability reproductions are labeled separately. Check each paper's evidence for its actual status.

## Start locally

Browsing the site requires no installation. To run the CLI, use macOS or Linux with Python 3.11+:

```bash
git clone https://github.com/daiwk/auto-research.git
cd auto-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
auto-research --help
auto-research list
```

For training dependencies, public data, and platform-specific demos, see [Installation and demos](setup.md). The selected task downloads the resources it needs and reuses local caches by default.

## Go further

| Guide | Contents |
|---|---|
| [Installation, data, and demos](setup.md) | Optional dependencies, Mac/MPS, Linux CPU/CUDA, data preparation, and one-command examples |
| [Experiments and automated research](readme_experiments.md) | Single and batch reproductions, model evolution, topic research, and external experiments |
| [Development and evidence conventions](readme_development.md) | Source structure, extension points, tests, PRs, and interpretation of experiments |
| [Delivery and audit record](readme_updates.md) | Historical batches, verified results, failures, and unfinished scope |
| [Architecture and extension](architecture.md) | Adapters, data isolation, fidelity, and evaluation contracts |
| [Documentation maintenance](getting-started.md) | Local preview, authoring questions, generation, and publishing |

## Contributing and maintenance

Questions, documentation corrections, and new paper components are welcome. See [Issues](https://github.com/daiwk/auto-research/issues) and the [commit history](https://github.com/daiwk/auto-research/commits/main/). Read [AGENTS.md](https://github.com/daiwk/auto-research/blob/main/AGENTS.md) before working with a coding assistant.

CI checks the Python contracts and documentation build. New papers need synchronized metadata, source and cost boundaries, all four question levels, and an update to the relevant topic deep dive. Experiments retain commands, versions, metrics, and failures. New CUDA implementations also require evidence from a real GPU run.

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=daiwk/auto-research&type=Date)](https://star-history.com/#daiwk/auto-research&Date)
