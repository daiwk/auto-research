# Paper implementation and evaluation library

<!-- source-sha256: ac40d5f6fbe0db6a313bdd00aa3eeeff0c5f9367a7208142b4811205aec9dea2 -->

[简体中文](../research-library.md) · [English paper catalog](papers/index.md)

Start with the [cross-domain paper lineage and coverage gaps (Chinese)](../research-lineage.md) to see which foundational lines of work are covered and which candidates have not yet met the bar for implementation. The historical scan is complete; discovery is now incremental. The [historical full-text audit closeout (Chinese)](../paper-audits/2026-historical-fulltext-review.md), [fixed roadmap for historical P0 implementations (Chinese)](../paper-audits/2026-historical-p0-implementation-roadmap.md), dated scan lists, and completed TODOs remain available for traceability, but are no longer in the main navigation.

The [public experiment dashboard](public-experiment-dashboard.md) shows committed results and lets readers search by domain, method, dataset, and metric. Temporary local experiments do not appear on the public site.

Paper implementation is a research workflow, not a single application domain. The repository uses common requirements for paper information, implementation, data, and metrics across search, advertising, recommendation, foundation models, structured decisions, multimodal models, LLM post-training, and agents. Mature implementations can join [Auto Research and evolution](auto-research.md) as mutations, training objectives, or evaluators.

[Recursive self-improvement (RSI; Chinese)](../evolution/recursive-self-improvement.md) is a cross-cutting index for post-training, agents, and automatic evolution. It does not change the domain of an individual paper or the source of truth for its metrics.

## Six built-in research domains

### Search, advertising, recommendation, and LLM applications

This domain covers industrial recommendation, search, advertising, generative recommendation, and applications that combine LLMs with these systems. It requires real online A/B evidence and uses public data, fair baselines, and a common basis for local comparisons.

- [Industrial paper implementation library (Chinese)](../reproductions/industrial.md)
- Browse [by company](../reproductions/catalog/by-company.md), [by topic](../reproductions/catalog/by-topic.md), or [by month](../reproductions/catalog/by-month.md) (Chinese)

### Foundation models

This domain covers architectures, pretraining data and optimization, multimodal representations, long context, and inference efficiency. Production A/B tests are not required. Papers must have credible public benchmarks, explicit training budgets, and verifiable methods. Local results must state the model scale and the limitations introduced by the available environment.

- [Foundation model research overview (Chinese)](../foundation-models/README.md)
- Browse [by organization, company, or university](../foundation-models/catalog/by-organization.md), [by topic](../foundation-models/catalog/by-topic.md), or [by year](../foundation-models/catalog/by-year.md) (Chinese)
- [Unified foundation model evaluation protocol (Chinese)](../foundation-models/benchmark.md)

### Structured decisions / System One

This domain covers typed questions, classification over dynamic candidate sets, probability calibration, confidence, selective prediction, and structured scoring. Jev is an important product in this area, but it is not the entire domain. Official hosted models, paper methods, and independent community implementations are labeled separately.

- [Structured decisions research overview (Chinese)](../system-one/README.md)
- [Method index](../system-one/catalog.md), [by organization, company, or university](../system-one/catalog/by-organization.md), [by topic](../system-one/catalog/by-topic.md), and [by year](../system-one/catalog/by-year.md) (Chinese)
- [Jev and open implementations (Chinese)](../system-one/implementations.md)
- [Unified evaluation protocol (Chinese)](../system-one/benchmark.md)

### Multimodal models

This domain covers shared representations for images, video, audio, and language, along with cross-modal retrieval and multimodal reasoning. It uses public checkpoints, auditable data slices, and metrics specific to multimodal tasks.

- [Multimodal research overview (Chinese)](../multimodal-models/README.md)
- [Multimodal method index (Chinese)](../multimodal-models/catalog.md)
- [Unified multimodal evaluation protocol (Chinese)](../multimodal-models/benchmark.md)

### LLM post-training

This domain covers preference learning, RLHF/RLVR, on-policy distillation, reward and credit assignment, and training stability. A unified candidate and free-generation protocol separates mechanism checks from actual generation.

- [LLM post-training research overview (Chinese)](../post-training/README.md)
- [Post-training method index (Chinese)](../post-training/catalog.md)
- [Unified post-training evaluation protocol (Chinese)](../post-training/benchmark.md)

### Agents

This domain covers long-term memory, planning and reflection, tool use, multi-agent collaboration, and self-improvement. The current priority is locally repeatable mechanisms and mini-suites, with real LLM executors and full benchmarks introduced incrementally.

- [Agent paper research overview (Chinese)](../agent-research/README.md)
- [Agent method index (Chinese)](../agent-research/catalog.md)
- [Unified agent evaluation protocol (Chinese)](../agent-research/benchmark.md)

## Common requirements for paper pages

Each paper page must include:

1. The paper link, company or institution, first public release date, and original authors' code.
2. The local adapter and implementation directory.
3. Background, main changes, an architecture diagram, and core equations.
4. Offline and online results reported by the paper, and the baselines actually used for comparison.
5. The local public-data protocol, stable metrics, run commands, and failed results.
6. The fidelity limits of the implementation relative to the paper.

Selection criteria can vary by domain, but results cannot be mixed across evidence types. Industrial A/B tests, public benchmarks, and local mechanism checks are labeled separately.

## Common metric storage

For each paper, the files beside its detail page are the single source of truth for traceable metrics:

```text
docs/<domain>/<paper-directory>/metrics/<dataset>-seed<seed>.json
```

- Search, advertising, and recommendation use `docs/reproductions/<paper-directory>/metrics/`. Foundation models use the corresponding detail-page directory or a public experiment directory.
- Structured decisions use `docs/system-one/metrics/`.
- LLM post-training uses `docs/post-training/<paper-directory>/metrics/`.
- Agents use `docs/agent-research/<paper-directory>/metrics/`.
- Each file must record the seed, evaluation tier, claim policy, manifest reference, and data provenance.
- Checkpoints, full traces, and temporary runs stay in local `runs/` and are not committed to GitHub.

`docs/experiments/` contains only snapshots comparing multiple methods under the same protocol; these snapshots produce the unified comparison tables. They do not replace per-paper metrics, and must not combine incomparable datasets, budgets, or domains into a single dated batch. Record a new paper's results in its own `metrics/` directory first. Build aggregate views from these individual results when cross-method comparisons are needed.

## Relationship to automatic evolution

```mermaid
flowchart LR
    P["Paper implementation"] --> C["Reusable components"]
    C --> M["Mutation / training objective"]
    C --> E["Evaluator / benchmark"]
    M --> A["Auto Research"]
    E --> A
    A --> X["Parallel experiments and multi-round evolution"]
    X --> R["Write stable findings back to the paper library"]
```

Paper implementation first asks, “Do we understand the method correctly, and can it run?” Automatic evolution then asks, “When we combine these methods in the current system, which configuration performs better on the given data and budget?”
