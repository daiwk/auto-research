# Architecture and extension points

<!-- source-sha256: c010e38d78286dca4627679b322369206b9588783a54294523deb08da8dc594f -->

[简体中文](../architecture.md) · English

## Stable core

```text
cli.py
 ├── runner.py                       # discovery / implementation / evaluation orchestration
 ├── evolution/                      # model genome / paper mapping / generations / champion test
 │    ├── providers.py               # registrable model / data / evaluator / baseline contracts
 ├── research_loop/
 │    ├── loop.py                    # proposal-independent iterative controller
 │    ├── cache.py                   # content-addressed metric cache
 │    └── journal.py                 # append-only stage/trial event log
 └── reproductions.registry         # reads packaged paper.yaml; loads selected implementations on demand
      ├── base.py                    # PaperMetadata / Adapter / L0-L3
      ├── manifest.py                # normalized paper facts
      ├── schema.py                  # result schema v2 and seed aggregation
      ├── reporting.py               # isolated result.json / report.md
      ├── rec_utils.py               # public sequence-data splits and shared metrics
      └── <paper>/
           ├── adapter.py            # metadata and run/render registration
           ├── algorithm.py/model.py # paper-specific mechanism
           ├── experiment.py         # baseline, validation tuning, and test
           └── report.py             # paper-specific report
```

Topic research and paper reproduction follow the same principle: separate orchestration from paper-specific code. `runner.py` determines the stage order, while `research_loop` handles adaptive proposals, iteration, caching, and audit records. A built-in evaluator, an external experiment command, or a paper adapter executes the actual model training. `ProposalStrategy` can read the existing trial history in each round. `CommandProposer` passes the paper manifest and history through environment variables to an agent command that the user explicitly configures. That command can therefore revise the next round's hypotheses using real results. See the [architecture adoption record (Chinese)](../design/automated-w2s-adoption.md) for the trade-offs and the mapping to automated-w2s-research.

Model evolution is a third, independent entry point. `EvolutionConfig` defines the target model, data, generation count, population, training budget, and seed. Retrieved papers are first mapped to tested architecture operators. These operators are combined with choices such as layer count, dimensions, and optimizer to form a `Genome`. Offspring within a generation share the same data split and budget, and selection across generations uses elitism with a variance penalty. All selection uses validation results; the isolated test set is read only at the end. To add a domain, use an `EvolutionProvider` to register the dataset, retrieval track, baseline genome, and evaluator without changing the generational controller. State is saved atomically after each trial and can be restored with `--resume`.

The shared layer handles only adapter discovery, common data protocols, run directories, and JSON/Markdown persistence. Do not add paper-specific logic to `cli.py` or the shared `reporting.py`. Move logic into `rec_utils.py` only when at least two recommendation adapters actually share it with identical semantics.

`ReproductionAdapter.run` retains the compatible signature `run(dataset_dir: Path, seed: int) -> dict`; `render` turns that dictionary into Markdown. Version 2 of `paper.yaml` declares `evaluation_tier`, datasets, baselines, metrics, default seeds, budgets, and device capabilities. The adapter module only binds the implementation. `PaperManifest` is the normalized view consumed by the CLI, catalog generators, and Evolve; other modules no longer maintain duplicate paper tables. See the [MR-B architecture contract (Chinese)](../design/architecture-mrb.md) for lazy imports, minimal installation, catalog source data, and resuming a scan.

## Evaluation tiers and result protocol

| Tier | Meaning |
| --- | --- |
| L0 | Interface, shape, and formula unit tests |
| L1 | Core-mechanism mini-suite |
| L2 | Real training and controlled comparisons on public datasets |
| L3 | Near-paper core training pipeline, with only reduced scale or replacement of private data |

New runs use result schema v2, which records the manifest, code commit, Python version and platform, data directory, budget, per-seed results, and aggregate statistics. Results from fewer than three independent seeds are smoke tests only and must not be described as stable gains.

```bash
auto-research reproduce --paper all --track recommendation --topic ranking \
  --fidelity full_pipeline --seeds 42,43,44 --workers 3 \
  --state-file runs/reproductions/ranking-state.json
```

Paper code and physical documentation paths use the adapter key and arXiv ID as stable identifiers; changing a classification does not move them. The reading entry points under `docs/reproductions/catalog/` provide indexes by company, topic, and year/month. A new catalog item declares `organization`, `published`, `topics`, and structured `online_ab` in `PaperMetadata`.

## Reproduction fidelity requirements

| Level | Required conditions | Included in `--paper all` by default |
| --- | --- | :---: |
| `full_pipeline` | The core model, training stages, and inference path all execute. Only a smaller model/dataset or replacement of private data modalities is allowed. | Yes |
| `core_mechanism` | The paper's central algorithm executes according to its formulas. Production backbones, private features, or serving infrastructure can be omitted. | Yes |
| `concept_demo` | A heuristic or proxy replaces a core network, loss, training stage, or inference process on which the conclusions depend. | No |

A scoring function that merely produces similar effects, a prior blended in after the backbone, and fixed candidates standing in for an LLM agent are all `concept_demo`. Disclosing the boundary does not make them reproductions. When a concept demo is selected explicitly, the CLI warns and the report lists the missing core components at the top.

## Add a paper

1. Create `src/auto_research/reproductions/<key>/`.
2. Put the paper's formulas or network in `algorithm.py` or `model.py`, and put the data split and controlled experiments in `experiment.py`.
3. Render the metrics the paper actually requires in `report.py`.
4. In `paper.yaml` v2, declare the paper facts, `fidelity`, and runtime contract. Bind the implementation in `adapter.py` with `register(adapter_from_spec(key=..., run=..., render=...))`. The registry discovers the paper from the spec and loads the code only when it runs. Industrial entries still need quantitative `OnlineABEvidence` or a named classic-paper exception.
5. Add algorithm unit tests, a registry discovery test, and any necessary minimal end-to-end tests under `tests/reproductions/`.
6. Record reviewed, durable conclusions in `docs/reproductions/<arxiv-id>-<key>/README.md` and write `metrics/*.json`. Concept-demo metrics must include `diagnostic_only: true`.
7. Add `paper_specs/catalog/<domain>/<key>.json`, then run the manifest and catalog generators to update all three browsing indexes and synchronize the root README. A classic paper specifically requested by the user without A/B evidence must declare a `selection_exception`. Do not add a paper by editing the generated manifest directly.
8. Run `pytest tests/reproductions/test_documentation_catalog.py`. A mismatch between the registry and any documentation entry point, missing sections or metrics in a paper page, or broken internal links will fail the test.

A new paper does not require changes to CLI branches, the shared report renderer, or any other paper's directory.

## Dataset rules

- When the original dataset is public and fits a local Mac, add a cacheable downloader in `datasets.py` and make the adapter use that data by default.
- Prefer the authors' released preprocessing splits. Otherwise, process the official data with the paper's stated k-core, temporal split, and negative-sampling protocols.
- If full training is still too expensive, use a deterministic sample cap. Record the cap, the seed, and differences from the paper protocol in the results.
- If the paper uses only internal company data or a very large model, use public data and a smaller model of the same kind if appropriate. The core forward architecture, training objective, and inference algorithm must still be preserved; otherwise, label it a concept demo.
- `data/` and `runs/` are local caches and are not committed to Git.

## Individual paper documentation contract

Each long-term write-up contains an **Original paper summary** with **Background and main changes**, a redrawn Mermaid architecture diagram, **Core formulas**, and **Reported offline and online results**. Follow that with **Local reproduction**, including the data protocol, results, code mapping, and limitations. If the paper does not report an online A/B test, say so explicitly. Keep paper result tables separate from local ones; do not directly compare incompatible metrics.

Every adapter must appear in the root README, the main paper index, and the company, month, and topic indexes. Each paper directory must contain at least one reviewed `metrics/*.json`. That JSON retains only stable scalars, protocol, and seeds—not checkpoints, raw logs, or data.

New recommendation papers must also meet the [online A/B requirement in the reproduction overview (Chinese)](../reproductions/README.md#selection-policy). The paper itself must disclose real production traffic, quantitative metrics, and a production control group. Offline state of the art, simulator results, or a claim of deployment cannot substitute for that evidence.

## Artifacts

Each run writes to an immutable directory:

```text
runs/reproductions/<arxiv-id>-<key>/<timestamp>/report.md
runs/reproductions/<arxiv-id>-<key>/<timestamp>/result.json
```

`result.json` is the machine-readable source of truth. The paper's renderer produces `report.md`. Do not commit temporary run outputs; transfer only reviewed conclusions into the appropriate paper write-up.

Topic research additionally writes `events.jsonl`, recording the discovery, implementation, experiment, reporting, and completion stages event by event. Each completed trial checkpoints both `result.json` and `report.md`, so interruption does not lose its evidence.

Scalar metrics from completed trials can be stored in `.auto-research/cache/`. The key includes the topic, track, data directory, seed, metric, optimization direction, command, and explicit `experiment_revision`. Failed trials, checkpoints, data, and raw logs are excluded. Caching for external commands is disabled by default if no `experiment_revision` is provided.

## Evaluation rules

Resume behavior, formal-comparison eligibility, retention of negative results, and GPU scheduling all follow the [experiment integrity and runtime contract (Chinese)](../design/experiment-integrity.md). Multi-seed statistics do not automatically upgrade a diagnostic to a higher evaluation tier.

- Temporal recommendation uses per-user chronological train/validation/test splits by default.
- Use only validation results to tune parameters or promote candidates; reserve test for the final report.
- For stochastic training, prefer the mean and standard deviation across multiple seeds.
- Record the paper's online A/B results, local public-data results, and implementation-proxy limitations separately.
- A local metric supports claims only at the adapter's fidelity level. Do not describe a concept-demo metric as validating the paper's effectiveness.
- Keep negative results. Explain possible differences in public data, model scale, or private features in the report.
