# Run paper experiments and automated research

<!-- source-sha256: 134e3467b73cc30aa29256d167d32373db551ec587c6ff3d4abb8c127a073c16 -->

[简体中文](../readme_experiments.md)

[Project README](project-readme.md) · [Documentation home](index.md)

Complete [installation and data setup](setup.md) first. These are full command examples for each workflow. Check the relevant guide for model and data costs before running them.

## Run paper reproductions

Adapter keys are listed dynamically from the registry:

```bash
auto-research list
auto-research reproduce --help
```

Run one paper or all papers:

```bash
auto-research reproduce --paper memento --seed 42
auto-research reproduce --paper sasrec --seed 42
auto-research reproduce --paper hstu --seed 42
auto-research reproduce --paper transact-v2 --seed 42
auto-research reproduce --paper pinfm --seed 42
auto-research reproduce --paper m6rec --seed 42
auto-research reproduce --paper kar --seed 42
auto-research reproduce --paper bahe --seed 42
auto-research reproduce --paper beque --seed 42
auto-research reproduce --paper precise --seed 42
auto-research reproduce --paper pinrec --seed 42
auto-research reproduce --paper genrank --seed 42
auto-research reproduce --paper learn --seed 42
auto-research reproduce --paper notellm --seed 42
auto-research reproduce --paper onerec-v2 --seed 42
auto-research reproduce --paper self-evolving-rec --seed 42
auto-research reproduce --paper prompt-generation --seed 42
auto-research reproduce --paper univa --seed 42
auto-research reproduce --paper pinterest-ads-llm --seed 42
auto-research reproduce --paper lwgr --seed 42
auto-research reproduce --paper sigma --seed 42
auto-research reproduce --paper s-grec --seed 42
auto-research reproduce --paper all --seed 42

# Include this only when you explicitly want the older concept demos.
auto-research reproduce --paper all --include-concept-demos --seed 42
```

Use common filters, three seeds, and a resumable state file for a formal batch comparison:

```bash
auto-research reproduce --paper all --track recommendation --topic ranking \
  --fidelity full_pipeline --seeds 42,43,44 --workers 3 \
  --state-file runs/reproductions/ranking-state.json
```

New results use schema v2, recording the paper manifest, L0–L3 tier, code commit, environment, budget, and seed. Multiseed batches also report mean, standard deviation, and 95% confidence intervals. One seed is only a smoke test and cannot establish stable improvement.

`--budget smoke|standard` is enforced, not just a label. Each adapter runs in a separate process with a 5- or 60-minute hard deadline. A timeout terminates the process and returns a failure. Override explicitly with `--budget-seconds`. `paper-specific` follows the adapter's declared schedule without a common deadline.

Each paper run is written to a separate immutable directory:

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── result.json   # machine-readable source of record
└── report.md     # adapter-rendered conclusions
```

`data/` and `runs/` are not tracked by default. Reviewed durable conclusions belong in `docs/reproductions/<arxiv-id>-<adapter>/README.md` and its English companion.

## Run model evolution

Built-in bases include RankMixer and HyFormer for recommendation and `micro-llm`, which can train from scratch on Mac, Linux GPU, or Linux CPU. MovieLens-1M is recommended for formal recommendation experiments.

Distinguish three candidate sources:

- Runtime search follows `--direction`. Discovered papers without a repository implementation remain `evidence-only` and do not execute.
- Any paper architecture or algorithm that enters training is already implemented, tested, and mapped in this repository.
- Evolution combines allowlisted operators and mutates hyperparameters to create new engineering hypotheses. It does not execute arbitrary code from PDFs. An optional `--candidate-generator-command` writes externally proposed results to an isolated candidate area for validation. Explicit `candidate promote --approve` is required before those candidates can register as executable operators in later runs.

See [where candidates come from](model-evolution.md#candidate-sources) for examples, offline mode, and report provenance.

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "Add LONGER, UniMixer, and related efficient Transformer architectures" \
  --workers 3 \
  --generations 3 \
  --population 4 \
  --steps 100 \
  --papers 8 \
  --benchmark-suite public \
  --fitness-metric public_composite \
  --seeds 42,43,44
```

The direction constrains both retrieval and the executable architecture space. Each generation compares paper-inspired structures and training parameters in parallel; validation drives the next decision. Mapped options include LONGER, UniMixer, WHALE, TMallGS, Long-History Transformer, RAMP, and combinations. Papers found online without safe operator mappings stay in the evidence pool.

The public MovieLens suite fixes overall, long-history, long-tail-target, recent-only, and restricted-personalization slices. `public_composite` selects candidates by equal-weighted NDCG across these slices. Use `--fitness-metric primary` to select on overall NDCG only or `--benchmark-suite core` to skip the extra slices.

`--benchmark-suite unirank --fitness-metric unirank_composite` adds chronological pointwise AUC and log loss for ranking research. See [UniRank integration](unirank.md) for the protocol, five official datasets, and the limits of the full runner.

Outputs in `runs/evolution/<model>-<timestamp>/` include machine-readable JSON, a Chinese Markdown report, and an HTML dashboard. See the [model evolution guide](model-evolution.md).

Three rounds of research over LLM architectures, pretraining data, and post-training:

```bash
auto-research evolve \
  --model micro-llm \
  --dataset wikitext-2 \
  --direction "Study efficient LLM architectures, data mixtures, and SFT/NEFTune post-training" \
  --generations 3 \
  --population 6 \
  --workers 1 \
  --steps 300 \
  --papers 8 \
  --benchmark-suite public \
  --fitness-metric public_composite \
  --seeds 42
```

The default `micro-llm` has about 12M–16M parameters. WikiText-2, Tiny Shakespeare, Stanford Alpaca, official GSM8K, and the BPE tokenizer are downloaded or built and cached in `data/`. Round 1 compares only architecture; round 2 compares data recipes; round 3 compares SFT, NEFTune, DynamicRubric, and Off-Context GRPO. The public suite also records Alpaca preference accuracy and GSM8K candidate Pass@1. See the [model evolution guide](model-evolution.md) for definitions.

Agents and generative recommendation share the multi-round controller. Agent axes include memory, planner, tool policy, critic, trainable policy, and recovery. `genrec` combines context, catalog heads, reward, and distillation on a genuine retained MovieLens-1M catalog with mandatory full-catalog evaluation:

```bash
auto-research evolve --model agent --dataset evomem-mini \
  --direction "Combine Agent Lightning policy, cross-episode memory, and Reflexion recovery" \
  --generations 3 --population 8 --seeds 42,43,44

auto-research evolve --model genrec --dataset movielens-1m \
  --direction "Combine context, reward, and distillation from Netflix/JD GenRec and OxygenREC-v2" \
  --generations 3 --population 8 --steps 100 --seeds 42,43,44
```

Agent mechanism regressions and capability comparisons run at different tiers. L1 mini-suites only test mechanisms. L2.1 hides reference answers, plans, and routes from the interface, removes guides, and separates train, validation, and test when comparing planning, recovery, and cost:

```bash
auto-research agent-capability \
  --methods long-context,react,reflexion,agent-g2,ahead,auso \
  --train-episodes 36 --episodes 60 --seeds 42,43,44
```

See the [L2.1 isolated agent evaluation and evolution guide](agent-research/capability-benchmark.md) for the protocol and fixed three-seed results.

The same evaluation can serve as the Agent Evolve validation and test objective. The controller searches nine component axes and promotes on validation only. It runs isolated test evaluation after all generations finish:

```bash
auto-research evolve --model agent --dataset toolroute-l2.1 \
  --direction "Combine memory, planner, tools, critic, policy, recovery, reflection, verifier, and context compression" \
  --generations 3 --population 9 --workers 3 \
  --agent-episodes 60 --seeds 42,43,44
```

Promote selected methods from a one-seed mechanism check to formal three-seed evidence via the resumable entry point:

```bash
auto-research promote-evidence --dataset-dir data --seeds 42,43,44
```

Defaults cover RankMixer, Switch Transformer, GRPO, and Agent Lightning. Output includes per-seed success/failure, mean, standard deviation, and 95% confidence intervals. Fewer than three successful seeds prohibits a stable improvement claim. See [three-seed evidence promotion](model-evolution.md#three-seed-evidence-promotion).

## Run a topic research loop

LLM example:

```bash
auto-research run \
  --topic "efficient post-training and preference optimization" \
  --track llm \
  --trials 8 \
  --papers 8
```

Recommendation example:

```bash
auto-research run \
  --topic "ranking loss and hard negative sampling" \
  --track recommendation \
  --trials 8 \
  --papers 8
```

General outputs are `runs/<timestamp>/report.md`, `result.json`, and `events.jsonl`. Built-in low-cost experiments verify the pipeline and screen hypotheses quickly; they are not paper-specific adapters.

Completed trials reuse scalar metrics from `.auto-research/cache/` when experiment revision, data directory, seed, and parameters match. `--force-rerun` bypasses the cache. For external code, set `experiment_revision` to enable caching and update it after code or data-protocol changes.

## Connect a real external experiment

Generate a configuration:

```bash
auto-research init research.json --track recommendation
```

Set implementation and training commands and the search space:

```json
{
  "topic": "new retrieval loss",
  "track": "recommendation",
  "max_papers": 10,
  "max_trials": 6,
  "implementation_command": ["codex", "exec", "Read AUTO_RESEARCH_MANIFEST and implement the selected hypothesis"],
  "proposal_command": ["python", "experiments/propose_next.py"],
  "experiment_command": ["python", "experiments/train.py"],
  "search_space": {
    "learning_rate": [0.0001, 0.0003],
    "architecture": ["baseline", "candidate"]
  },
  "metric_name": "validation_loss",
  "direction": "minimize",
  "experiment_revision": "retrieval-loss-v1",
  "timeout_seconds": 3600
}
```

The implementation command receives the paper manifest through `AUTO_RESEARCH_MANIFEST`. Each training command receives the trial parameters through `AUTO_RESEARCH_PARAMS`. Its final line must be metrics JSON, for example:

```json
{"validation_loss": 1.234}
```

An optional `proposal_command` receives `AUTO_RESEARCH_MANIFEST` and `AUTO_RESEARCH_HISTORY` each round. Its final line returns `{"params": {...}}` or `{"stop": true}`. The agent can use prior successes, failures, and cached results to choose the next parameters. Without it, search follows the deterministic configuration.
