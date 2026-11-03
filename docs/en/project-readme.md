# Auto Research

<!-- source-sha256: fda2622d113efb2162685bae62ce18667c96af5ac1ec80104c5b19cbf4839f2f -->

[简体中文](../project-readme.md)

[English README on GitHub](https://github.com/daiwk/auto-research/blob/main/README.en.md) · [English documentation](index.md)

Understand papers, inspect their implementations, and iterate on research with public data. The project covers search, ads and recommendation, foundation models, LLM post-training, agents, multimodal models, and structured decisions.

[![Python quality](https://github.com/daiwk/auto-research/actions/workflows/quality.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/quality.yml)
[![Documentation](https://github.com/daiwk/auto-research/actions/workflows/docs.yml/badge.svg)](https://github.com/daiwk/auto-research/actions/workflows/docs.yml)

**[Open the site](index.md) · [Learn paper by paper](learning/index.md) · [Research library](research-library.md) · [Experiment dashboard](public-experiment-dashboard.md)**

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

<details>
<summary>Star History</summary>

<a href="https://www.star-history.com/?repos=daiwk%2Fauto-research&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=daiwk/auto-research&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=daiwk/auto-research&type=date&theme=light&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=daiwk/auto-research&type=date&legend=top-left" />
 </picture>
</a>

</details>
