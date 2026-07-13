# automated-w2s-research architecture adoption

This project reviewed [safety-research/automated-w2s-research](https://github.com/safety-research/automated-w2s-research) as an architectural reference. The useful overlap is the research workflow, not the weak-to-strong task itself.

## Decision

Use a clean-room, incremental refactor instead of merging the repository.

| Upstream capability | Decision | Local implementation |
|---|---|---|
| One directory per research idea | Adopt | Existing `reproductions/<paper>/adapter.py` plugins remain the unit of extension |
| Unified run configuration | Adopt | `ResearchConfig` owns discovery, implementation, experiment, cache and reproducibility settings |
| Iterative idea → train → evaluate loop | Adopt | `research_loop.IterativeResearchLoop` separates adaptive proposals from evaluation and checkpoint callbacks |
| Hierarchical result cache | Adopt in a smaller form | Content-addressed, track/experiment-scoped metric cache; failed trials and checkpoints are never cached |
| Agent-visible research history | Adopt | Append-only `events.jsonl` records stages, trials, cache hits and completion |
| Hidden-label remote evaluator | Preserve as a boundary, not copied | Paper adapters must select on validation and evaluate test once; a future evaluator service can implement the same boundary |
| Claude Agent SDK loop | Do not merge | Provider-specific and unnecessary for the local-first core; agent-generated proposals can later plug into the proposal interface |
| Flask/React dashboard | Defer | CLI and immutable artifacts remain the primary interface until concurrent remote workers justify a service |
| Docker/RunPod/S3/VERL stack | Do not merge | CUDA/Linux-specific dependencies conflict with the current Mac-first and lightweight installation goals |

## Why a source merge was rejected

The upstream environment pins a large CUDA training stack including PyTorch, vLLM, FlashAttention, Unsloth, SGLang, Ray/VERL, RunPod and S3 clients. Its launcher and autonomous loop also assume Anthropic credentials and a server process. Importing that tree would make a basic local MovieLens experiment depend on infrastructure unrelated to the project goal.

The upstream README declares MIT licensing, but the reviewed repository snapshot does not contain a tracked `LICENSE` file. No upstream source code is copied. This refactor independently implements the general architecture patterns above and keeps this repository's existing MIT license.

## Extension seam

The loop consumes an iterable of parameter dictionaries and an evaluator callable:

```python
loop = IterativeResearchLoop(
    evaluate=evaluate,
    direction="maximize",
    cache=cache,
    cache_context=context,
)
trials, best = loop.run(proposals, on_trial=checkpoint)
```

By default `proposals` comes from the deterministic search space. `ProposalStrategy.propose(history)` receives every prior success, failure and cache hit. The built-in `CommandProposer` exposes this interface through `AUTO_RESEARCH_MANIFEST` and `AUTO_RESEARCH_HISTORY`, so Codex, Claude or a local agent can generate the next candidate from papers plus measured outcomes without changing experiment execution, caching, reporting, or paper adapters.

## Artifact and cache boundaries

Each topic run now contains:

```text
runs/<timestamp>/
├── result.json
├── report.md
└── events.jsonl
```

Reusable metric cache entries live under `.auto-research/cache/<track>/<experiment>/` and are ignored by Git. Custom commands are cached only when `experiment_revision` is set, preventing silent reuse after experiment code changes. `force_rerun` bypasses cache reads. Datasets, raw logs and model checkpoints remain outside the metric cache.
