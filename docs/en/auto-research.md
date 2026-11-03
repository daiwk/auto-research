# Auto Research

<!-- source-sha256: 2a264cf839f54964404f638733d838d4219d0ac499911e3fb4b707c5beeea5cd -->

[简体中文](../auto-research.md)

Auto Research turns a research question into a traceable, reproducible chain of experiments. It is not tied to recommendation, LLMs, or agents. Domain adapters supply the object of study, mutations, training or execution entry points, and an evaluator. The shared research loop handles evidence from papers, parallel experiments, selection, multiple rounds, and reporting.

## Two entry points

| Entry point | Inputs | Automated steps | Best suited to |
|---|---|---|---|
| Topic research | Topic, domain, number of papers, and trial count | Paper search, parameter proposals, individual trials, caching, and reports | Exploring a broad research question or integrating a custom experiment |
| Directed evolution | Existing system, data or environment, and a natural-language direction | Paper search, mutations, parallel experiments, champion evolution, and isolated testing | Iteratively improving a model, training recipe, or agent policy |

[See domain adapters and current support (Chinese)](../evolution-domains.md).

Recursive self-improvement (RSI) spans models, post-training, and agents. It does not duplicate the paper library. The [RSI topic guide (Chinese)](../evolution/recursive-self-improvement.md) explains which feedback can carry over to the next round, what has been implemented, and how to test for sustained improvement.

The shared [Auto Research Platform P1 (Chinese)](../research-platform-p1.md) provides local, SSH, and Slurm execution; versioned protocols for fair comparison; proposals derived from papers; paired statistical decisions; and a record of negative results.

The [long-running research portfolio controller (Chinese)](../evolution/research-portfolio.md) manages multiple research ideas in parallel, isolates failures, recovers after restarts, and maintains two layers of experience memory. It wraps existing adapters, trainers, and evaluators. It does not treat suggestions written in natural language as executable operators.

## Where candidates come from

Directed evolution does not generate an implementation on the spot after discovering a paper. It separates paper discovery from code execution:

- **Paper evidence:** Search arXiv for the requested direction, or use the repository's built-in manifest offline. A newly discovered paper without a local implementation is marked `evidence-only` and appears only in the report.
- **Executable operators:** Only architectures or algorithms implemented, tested, and mapped to a paper in the repository can be trained.
- **Composition and tuning:** The controller can compose compatible implemented operators or vary layer count, dimensions, learning rate, and similar settings. These are new engineering hypotheses, not unreviewed algorithm code generated on demand.

[See examples of how papers, operators, and compositions relate](model-evolution.md#candidate-sources).

## Topic research

```bash
auto-research run \
  --topic "ranking loss and hard negative sampling" \
  --track recommendation \
  --trials 8 \
  --papers 8
```

The system records the papers it finds, each trial's configuration and metrics, the current best result, and reasons for failure. The built-in low-cost experiments verify that the pipeline runs. For a full study, use a configuration file to plug in your own implementation and experiment commands, metric direction, and search space.

Use `--track llm` for LLM research and `--track recommendation` for recommendation, search, and advertising. Custom domains can supply an experiment command and search space. Add `--offline` when network access is unavailable; existing cache entries are reused. Post-training and agents have dedicated evolution adapters.

## Directed model evolution

This example asks the system to add LONGER, UniMixer, and related efficient Transformer architectures to RankMixer. It keeps the original query text for reproducibility.

```bash
auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "把 LONGER、UniMixer 及相关高效 Transformer 结构加入 RankMixer" \
  --generations 3 \
  --population 6 \
  --workers 3 \
  --steps 300 \
  --papers 8 \
  --benchmark-suite public \
  --fitness-metric public_composite \
  --seeds 42,43,44
```

The first round fixes hyperparameters and compares architectures only. From the second round, the controller tunes layer count, dimensions, learning rate, optimizer, and batch size around the champion. Trials in the same generation run in separate processes. Validation determines which candidates advance; the test split is used only after all rounds finish.

[See the full model evolution protocol, data scale, and architecture operators](model-evolution.md).

The LLM track uses `micro-llm + WikiText-2`. Round 1 compares architectures such as GQA, RoPE/RMSNorm/SwiGLU, and parallel blocks. Round 2 compares pretraining data recipes. Round 3 compares SFT, NEFTune, DynamicRubric, and Off-Context GRPO. The public suite also uses fixed evaluations for Alpaca response preference and GSM8K candidate Pass@1. The default model has roughly 12M–16M parameters and can be trained from scratch on Apple Silicon.

The post-training and agent tracks first search for papers and then map them to tested operators in the repository. Post-training searches over objective, learning rate, group size, and budget. Agent research searches over memory, planner, tool policy, critic, and capacity. Both record paper sources, parent and child genomes, advancement on validation, and isolated tests.

## Research artifacts

Each run is saved separately, without overwriting previous experiments:

```text
runs/<research-id>/
├── result.json     # Configuration, paper evidence, metrics, and best result
├── report.md       # Reviewable research findings
└── events.jsonl    # Events by stage and trial

runs/evolution/<model>-<timestamp>/
├── result.json     # Architecture genome, lineage, and complete metrics
├── report.md       # Chinese report covering the evolution rounds
└── index.html      # Research dashboard you can open directly
```

## Safety and auditability

- Papers discovered online but not implemented remain evidence-only. The system does not execute arbitrary generated code.
- Candidate selection uses only validation data. Do not inspect the test split early to choose a candidate.
- Reports record data truncation, evaluation cohorts, seeds, training budgets, and failed trials.
- Keep checkpoints, public datasets, and raw runs local rather than committing them to Git. Document stable metrics and reproduction methods instead.
