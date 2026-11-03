# Development and Research Evidence Conventions

<!-- source-sha256: e990073267813b9031b63b703948db9f28ca32a238bc14f37acacabd4adce590 -->

[简体中文](../readme_development.md)

[Project home](project-readme.md) · [Documentation site](https://daiwk.github.io/auto-research/)

## Code structure

```text
src/auto_research/
├── cli.py                         # run / reproduce / publish entry points
├── runner.py                      # research-stage orchestration
├── research_loop/                 # iteration controller, metric cache, event log
├── evolution/                     # multi-generation recommendation and micro-LLM evolution
├── post_training/                 # OPD, RL, preferences, process rewards
├── agent_research/                # agent memory, planning, and tool evaluation
├── datasets.py                    # public data downloads and cache
├── papers.py                      # arXiv discovery
└── reproductions/
    ├── base.py                    # stable adapter interface
    ├── registry.py                # automatically discover */adapter.py
    ├── reporting.py               # isolated JSON/Markdown artifacts
    ├── rec_utils.py               # shared sequence splits and metrics
    ├── llm_rec_data.py            # shared CTR text data and AUC
    ├── sequence_training.py       # all-position training and full-catalog evaluation
    └── <paper>/
        ├── adapter.py             # paper metadata and registration
        ├── model.py               # paper-specific model or algorithm
        ├── experiment.py          # baselines, tuning, evaluation
        └── report.py              # paper-specific Markdown report

docs/reproductions/<arxiv-id>-<adapter>/README.md
docs/reproductions/catalog/          # stable organization, topic, and time navigation
tests/reproductions/
```

New papers do not require CLI changes: the registry discovers folders containing `adapter.py`. See [Architecture and extension](architecture.md).

Repository constraints for coding assistants are in the root `AGENTS.md`. See [GPT-6 Astra collaboration](../astra-collaboration.md) for tasks, completion evidence, and validation scope.

## Learning material for new papers

Each paper needs questions at four levels: fundamentals, mechanism, comparison, and implementation. Assign it to a learning subtopic. Update its [topic deep dive](../learning/deep-dives/index.md) by comparing the new mechanism with existing examples, revising analyses or cross-paper questions where needed, and appending the date, papers, and what changed or why the prior distinction still holds. Keep question IDs and history stable. Neither the paper Q&A nor deep dive should simply repeat the abstract.

Authored deep dives are in `docs/learning/deep-dives/*.json`. `reviewed_papers` must match topic membership; `updates` must cover new identities, its latest date must match `updated`, and every update's `source_revisions` records each involved README's SHA256. Re-review and append an update after older mechanisms or reproduction boundaries change. The generator renders authored material; it does not make semantic comparisons. Missing classifications, cards, or updates fail the documentation release check.

```bash
python scripts/generate_learning_cards.py --require-questions --require-deep-dives
python scripts/generate_learning_cards.py --check --require-questions --require-deep-dives
```

The idea isolation, unified configuration, iterative research, and caching draw from [automated-w2s-research](https://github.com/safety-research/automated-w2s-research); the Claude/Flask/RunPod/VERL stack was not incorporated. See the [architecture adoption record](../design/automated-w2s-adoption.md).

## Submit a GitHub PR

```bash
brew install gh
gh auth login

auto-research publish runs/<timestamp>/report.md \
  --title "research: evaluate retrieval loss"
```

The publishing command requires a checkout without unrelated edits. If needed it creates an `agent/...` branch from `main` or `master`, stages only the requested report, commits, pushes, and opens a draft PR. Add `--ready` to open a non-draft PR.

## Interpreting experiments

- Determine recency from arXiv `submittedDate` and record actual retrieval date.
- Replacing private data, reducing model size, or omitting production infrastructure can be acceptable scale reductions. Replacing the defining architecture, objective, or inference path requires a **concept demonstration, not a paper reproduction** label.
- JSON and Markdown outputs record `reproduction_fidelity`. Default `--paper all` skips concept demonstrations.
- Keep paper online A/B and local offline metrics separate.
- Retain gains, regressions, and instability across seeds. Select parameters on validation only.

## Tests

```bash
python -m pytest
```

Tests cover adapter discovery, defining paper mechanisms, artifact isolation, and the common research loop.
