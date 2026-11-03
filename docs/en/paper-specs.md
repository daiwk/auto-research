# Declarative paper implementation specifications

<!-- source-sha256: 1e84b7d27da02bebafaf9b390c3585394d5b04a14f5faf6fc50dcc92a02acba7 -->

[简体中文](../paper-specs.md) · English

Every registered adapter has a `paper.yaml` alongside it. The file uses JSON-compatible YAML: YAML tools can read it, and Python's standard library is sufficient for deterministic validation. All adapters have migrated; older papers no longer rely on a separate manual synchronization process.

## What a single specification contains

`paper.yaml` records the paper link, organization, exact arXiv v1 publication date, upstream code status, track and topics, local code and documentation paths, reproduction fidelity, evaluation tier, public datasets, baselines, metrics, the mechanisms actually implemented, and optional Evolve operators. CI cross-checks the specification against the registry and documentation so organization names, dates, paths, and metrics do not drift between indexes.

```json
{
  "schema_version": 1,
  "key": "rankmixer",
  "arxiv_id": "2507.15551",
  "paper_url": "https://arxiv.org/abs/2507.15551",
  "organization": "ByteDance",
  "published": "2025-07-21",
  "upstream_code": "not released / not found",
  "datasets": ["movielens-100k"],
  "baseline": "DIN",
  "metrics": ["ndcg_at_10"]
}
```

## Generate, validate, and scaffold

```bash
# Synchronize all specifications from the current registry and READMEs
PYTHONPATH=src python scripts/manage_paper_specs.py generate

# Used in CI: check for stale bytes, then validate semantics
PYTHONPATH=src python scripts/manage_paper_specs.py check
PYTHONPATH=src python scripts/manage_paper_specs.py validate

# Scaffold a new adapter from a reviewed spec; refuse to overwrite an existing directory
PYTHONPATH=src python scripts/manage_paper_specs.py scaffold \
  --spec paper.yaml \
  --destination src/auto_research/reproductions/new_paper
```

The scaffold creates only `adapter.py`, `experiment.py`, and the specification file. It does not generate fictitious training results. Before registering the adapter, implement the paper's mechanism and add the public-data experiment and documentation tests.
