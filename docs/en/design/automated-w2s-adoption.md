# Architectural lessons from automated-w2s-research

<!-- source-sha256: 18d951cd9087adb7c5c55ad716c8191c883b4467daec905832e5e289e86c787f -->

[简体中文](../../design/automated-w2s-adoption.md)

This project used [safety-research/automated-w2s-research](https://github.com/safety-research/automated-w2s-research) as an architecture reference. The reusable idea is the automated research workflow, not the weak-to-strong task.

## Decision

Do not merge upstream. Adopt suitable general patterns through incremental clean-room implementation without copying source or the heavy runtime.

| Upstream capability | Decision | Local design |
|---|---|---|
| One directory per idea | Adopt | Continue using `reproductions/<paper>/adapter.py` plugins as extension units |
| Shared run configuration | Adopt | `ResearchConfig` controls discovery, implementation, experiments, caching, and reproducibility |
| Idea → train → evaluate loop | Adopt | `research_loop.IterativeResearchLoop` separates adaptive proposal, evaluation, and checkpoint callbacks |
| Layered result caching | Adopt in reduced form | Content-addressed metric cache separated by track and experiment; failures and checkpoints are not cached |
| Agent-readable history | Adopt | Append stage, trial, cache hit, and completion events to `events.jsonl` |
| Remote evaluator with hidden labels | Keep boundary, not code | Adapters select only on validation and evaluate test once; a future separate service can enforce the same boundary |
| Claude Agent SDK loop | Do not merge | Provider-specific and unnecessary for local-first core. Agents can propose through the generic interface. |
| Flask/React console | Defer | Prefer CLI and immutable artifacts until concurrent remote workers are needed |
| Docker/RunPod/S3/VERL runtime | Do not merge | CUDA/Linux-specific stack conflicts with lightweight Mac-first setup |

## Why not merge source

The upstream runtime pins a large CUDA stack with PyTorch, vLLM, FlashAttention, Unsloth, SGLang, Ray/VERL, RunPod, and S3 clients. Launchers and the loop also depend on Anthropic credentials and persistent services. Importing it would make basic local MovieLens work depend on unrelated infrastructure.

The upstream README stated MIT, but the reviewed snapshot had no Git-tracked `LICENSE` file. This project copied no upstream source, implemented general patterns independently, and retains its existing MIT license.

## Extension interface

The loop takes parameter dictionaries and an evaluation callable:

```python
loop = IterativeResearchLoop(
    evaluate=evaluate,
    direction="maximize",
    cache=cache,
    cache_context=context,
)
trials, best = loop.run(proposals, on_trial=checkpoint)
```

Default `proposals` come from deterministic search. `ProposalStrategy.propose(history)` can read successes, failures, and cache hits. `CommandProposer` exposes this through `AUTO_RESEARCH_MANIFEST` and `AUTO_RESEARCH_HISTORY`, so Codex, Claude, or a local agent can propose candidates from papers and actual results without changing execution, caching, reports, or adapters.

## Artifacts and cache

A topic run writes:

```text
runs/<timestamp>/
├── result.json
├── report.md
└── events.jsonl
```

Reusable metrics are in Git-ignored `.auto-research/cache/<track>/<experiment>/`. External experiment commands read cache only with explicit `experiment_revision`, preventing reuse across silent code changes. `force_rerun` skips cache reads. Datasets, raw logs, and checkpoints are never stored in the metrics cache.
