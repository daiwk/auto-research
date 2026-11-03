# MR-B: registries, commands, discovery, and paper specifications

<!-- source-sha256: 514b4493fe33915f9c7bd44ae247bddb933a0b31095824e666ef9edfa89f4b2f -->

[简体中文](../../design/architecture-mrb.md)

This follows MR-A without adding papers or changing algorithms or evidence grades. Command names, flags, adapter keys, and paper URLs stay intact. Uncommitted original-workspace changes are outside the migration.

## Scope and acceptance

| Original issue | Implementation | Acceptance |
|---|---|---|
| Registry loaded every model | Packaged specs provide metadata; run/render resolve selected implementations; Agent loads by method | List, manifest, and full parser work without PyTorch; only selected adapter imports |
| Coupled CLI and unusable minimal install | Per-command parsers/handlers, lazy public exports, optional-dependency messages | Base-only wheel/independent CI; existing command regressions |
| Network success treated as coverage | Page persistence, query/window/budget identities, retained pages on failure, independent queries continue | Resume, reject configuration drift; cache and caps cannot mean complete |
| Spec was only a generated copy | paper.yaml v2 drives runtime; catalog facts by domain/key; manifest derived only | 371 runtime contracts and 736 catalog records preserve semantics; no inference from local docs |
| Dated batch files became permanent boundaries | Move related definitions to stable mechanisms modules and retain compatibility exports | Old imports, behavior, and tests preserved |

## The only metadata editing entry points

An adapter's `paper.yaml` v2 owns metadata and evaluation contracts. `adapter.py` binds only `run` and `render`; it no longer runs a mini-suite to guess metrics or infers devices/budgets from README or metrics. Runtime-specific declarations go under `execution`, without duplicating shared title, identity, topic, fidelity, data, or metrics. Some historical display dates/affiliations are more complete than old runtime declarations; both meanings survive migration. Historical `mechanisms` do not imply fidelity; use fidelity and omitted_core_components.

Catalog facts live in `src/auto_research/paper_specs/catalog/<domain>/<key>.json`. Reproductions reference spec keys, deriving runtime fields from paper.yaml; other domains keep reviewed facts in their own records. `docs/research-manifest.json` and Markdown indexes are rebuildable products. Generators no longer depend on their previous output. Old `latest_*_catalog.py` modules are compatibility views; explicit compatibility overrides are not inputs to new generators.

New papers still require algorithms, evaluation, and documentation; specs alone are not implementation. `manage_paper_specs.py check/validate` and generation gates check specs, paths, duplicate keys, and contracts.

## Three independent scan statuses

1. **Transport:** requests succeeded, failed, or fell back to cache.
2. **Query coverage:** every configured query was exhausted; reaching maximum-results is capped even if all pages succeeded.
3. **Full-text review:** identity, body experiments, and production evidence were checked. Download success does not advance the human review watermark.

On 2026-10-07 discovery gained two independent channels. Default `submission-window` constrains submission dates at the API for a fixed window. `--recall-mode late-index` uses API `id:YYMM.*` and local identifier-month filtering without submission dates, finding older publication dates indexed later. Daily jobs retain both outputs and separate checkpoints. Exhausting the first channel does not replace late-index or official-source review. Capped broad queries leave explicit gaps; increase budget or supplement official sources. Coverage is limited to this matrix, not the entire web or implementation of every eligible paper.

```bash
python scripts/discover_papers.py --track agent \
  --start-date 2026-10-01 --end-date 2026-10-07 \
  --checkpoint-dir .cache/discovery/agent-oct07 \
  --output runs/agent-candidates.json
# To resume, keep the same window, query matrix, and budget, then add --resume.
# For late-index recall, use --recall-mode late-index and separate checkpoint/output.
```

Each successful page atomically stores cursor and candidates. Query failure retains earlier pages and does not block others. Cached pages provide leads, not verified cursor progress. Resume checks full scan identity. Without `--resume`, a new scan ID prevents stale window-page reuse. Actions upload progress for diagnostics without reusing it as next day's results.

## Install and migration limits

`pip install .` with base dependencies provides help, catalog, protocols, and manifest generation. Training still requires documented extras; lazy imports cannot make missing dependencies succeed. Wheel specs and catalog resources do not require the cloned docs directory.

Source changes trigger MR-A experiment identity checks. Old runs remain readable but their scores cannot be reused across versions. Moving modules preserves algorithms; actual NVIDIA execution is still required for GPU regressions.

## Acceptance results (2026-10-07)

- Full suite: 1,251 passed; after extracting entry declarations, targeted Agent/MR-B tests: 124 passed.
- 371 adapter runtime contracts and 736 public catalog records preserved meaning; catalog/dashboard generation did not drift.
- AST comparison: 364 algorithm definitions unchanged; eight adapter factories only changed spec binding.
- Built the wheel and installed only project plus NumPy in an isolated environment, without PyTorch/Transformers. Parser, catalog, manifest, and initialization passed; CI added an independent minimal-install job.
- NVIDIA A100 public MovieLens-100k ran DIN/mean-pooling (seeds 42/43/44, three steps each), lazy adapters in independent processes, `reproduce`, and RPTune/CARM CUDA forward/backward. All 13 device resolutions were CUDA. The [sanitized receipt](../../gpu-validations/architecture-mrb-a100-20261007.json) pins source and data. Short training verifies execution, not paper-level gains.
- Ruff, spec checks, metric schemas, platform integrity, GPU evidence, and strict docs passed.

Legacy dated files provide compatibility exports only. New algorithms belong in stable mechanism modules with domain specs, not appended to historical batches. These regressions do not replace full-scale paper reproductions.
