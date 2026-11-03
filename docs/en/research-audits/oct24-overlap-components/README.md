# October 24, 2026: Same-announcement backfill and the Google PLE protocol

<!-- source-sha256: 10ab8fd85de144e2d9a7f360f7b04520189d9e5fcc11bcf65f83119c484f26c1 -->

[简体中文](../../../research-audits/oct24-overlap-components/README.md)

All **four low-cost components** in this fixed batch passed frozen-source acceptance over three seeds. TTR-Compressor, UserArena OPTD, and MOER ran on one real A100; Google PLE used a CPU offline protocol. **This is backfill from the October 23 announcement, not four October 24 first publications.** Global review still ends at 2026-10-15, with no claim that all papers or institutions in the window were covered.

## Deliverables

| Paper | Implemented | Not reproduced |
| --- | --- | --- |
| [Google PLE](../../../agent-research/2610.30537-physical-engineering-exam/README-en.md) (P0) | Scoring supplied decisions, fingerprinting public configuration, auditing provenance and safety, and aggregating three external runs | No engineering tasks, physical graders, models, or containers were executed; not official benchmark capability integration |
| [TTR-Compressor](../../../foundation-models/2610.31574-ttr-compressor/README-en.md) (P1) | Normalized keys, original token scalar targets, positive diagonal ridge, dual Cholesky, and outer gradients | No convolution, multi-head sparse integration, pretraining, or full vision-language model |
| [UserArena OPTD](../../../post-training/2610.30932-userarena-optd/README-en.md) (P1) | Tokenwise geometric trust region, full-vocabulary JSD, and independent gold-prefix grounding | No intent extractor, user simulator, shopping environment, or official data evaluation |
| [MOER](../../../post-training/2610.30873-moer/README-en.md) (P1) | Mixed-group advantages, prefix annealing, single-candidate rollback, and exact mixed-policy loss | No expert solution generation, verifier, LLM training, or capability comparison |

Exact v1 dates, first-author primary affiliations, pinned upstream revisions, and licenses appear on individual pages and in the [fixed scope](../../../research-audits/oct24-overlap-components/task-scope.json). Google PLE uses `physical-engineering-exam`, distinct from recommendation PLE. Its repository's October 23 29-dev/56-hidden protocol release is separate from the October 21 paper.

Full experiments exceed a single A100/A30 or local Mac budget and are **not reproduced (review DONE)**. We did not download weights or large data, run expensive cost probes, or enqueue retries or implementations. Standalone losses and protocols do not establish model capability or qualify for automatic evolve promotion.

## Actual verification

Frozen source: `7b78ce1dbfc4006fbc81fdb181c3ead45aeb2457`.

- [Raw CPU results](../../../research-audits/oct24-overlap-components/raw-cpu.json): four components × three seeds; about 4.91 seconds for execution.
- [Raw A100 results](../../../research-audits/oct24-overlap-components/raw-cuda.json): three components × three seeds; about 1.58 seconds.
- [Frozen-source proof](../../../research-audits/oct24-overlap-components/frozen-sources.json) binds source SHA to the Git commit for offline verification in shallow CI clones.
- Individual `metrics/` files and three sanitized receipts in `docs/gpu-validations/` retain results without SSH aliases, hostnames, users, or driver/build strings.

Timings exclude connection, sync, and test time and are **not full training times**. Random-tensor losses, gradients, and negative controls support L1 mechanism claims only. PLE given external scores validate aggregation, not engineering-design performance.

```bash
python scripts/build_oct24_component_artifacts.py --check
python -m pytest tests/test_oct24_component_evidence.py
```

The offline curator verifies exact check/metric sets, numeric bounds, three seeds, CPU/CUDA identities, raw-byte hashes, executable catalog entries, per-paper metrics, receipts, and scope/ledger identities. Missing entries, empty sets, wrong IDs, and CPU masquerading as GPU fail. Source building is separate from execution; duplicate batches cannot overwrite later acceptance.

## Sources and unknowns

The [source receipt](../../../research-audits/oct24-overlap-components/source-coverage.json) records eight official arXiv pages still dated **2026-10-23**: 1,260 category entries, 916 identities, with 499 new, 287 cross-list, and 474 replacement entries. Category version lists and ordering were unchanged from the previous capture; zero added identities/version strings. Cross-listing and replacements are not new papers; all four actual v1 dates predate the previous capture.

Initial and independent repeat requests for Google and Meta timed out, so catalog diffs are **unknown/null**, not zero. HTTP 428 on Google's unfiltered homepage is not a successful 29-page capture. DeepMind returned 9/9 pages and 265 records, unchanged within the bounded URL/title/date comparison, not an exhaustive site audit.

Google PLE was independently found through `google-research/ple` and its author list; first author Rujun Han at Google Cloud AI Research qualified for priority regardless of catalog listing. Meta PARQ revision `a8ce7364a4b30a881129a359f1a312069a0417c3` concerns row-wise bucketization maintenance. [2503.15748](https://arxiv.org/abs/2503.15748) first appeared 2025-03-19 and is neither a new paper nor a new arXiv version here. The pinned LICENSE is MIT despite automated classification.

ReflectPO (2610.30933) and RIPPLE (2610.31276) are in `additional_dispositions`: respectively 8×H800 long-trajectory training and a 27B actor with learned recovery and semantic attribution. Full runs are too costly and not reproduced (review DONE). No author-method repository was found in checked sources; no unverified code, heuristic core replacement, or automatic queue. Cost closure is not algorithm delivery or confirmation of unknowns.

Archived exceptions such as inaccessible full texts are not periodically retried. Catalog checks sought new increments, not reopening old dispositions. Continue reporting announcement dates, first publications, revisions, and historical backfills separately.
