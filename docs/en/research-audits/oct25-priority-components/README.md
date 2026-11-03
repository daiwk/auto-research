# October 25, 2026: Meta OPD, Inside-JEPA, and Google historical backfill

<!-- source-sha256: dd8b3cce346b710c87a83cb13296b8ae91c7d4951984a55679c8ba5d4301d715 -->

[简体中文](../../../research-audits/oct25-priority-components/README.md)

Three **low-cost L1 components** passed frozen-source CPU and real single-A100 acceptance over three seeds. Two are same-announcement discoveries and one is historical, **not three October 25 first publications**. The full large-scale experiments are **too costly, not reproduced (review DONE)** and do not enter retry or implementation queues.

## Deliverables and limits

| Paper | Implemented | Not reproduced |
| --- | --- | --- |
| [Meta ME-OPD](../../../post-training/2610.30231-minimal-edit-opd/README-en.md) (P0) | Strict edit masks under a frozen old policy, correct/incorrect branches, and selected-token normalization over the full minibatch; undisclosed task objective explicitly supplied externally | No VLM, teacher, or verifier execution, reference description/solution generation, or math/vision capability claims |
| [Inside-JEPA](../../../foundation-models/2610.31194-inside-jepa/README-en.md) (P1) | Ordered relation states, online-future inverse gradients, EMA 0.996, five-arm controls, and actual AdamW updates | No video backbone, detection/tracking, SSv2/RH20T, or planning evaluation; undisclosed head topology supplied by caller |
| [GroupDPO](../../../post-training/2604.15602-group-dpo/README-en.md) (Google/DeepMind collaboration, historical) | Four exact group objectives, full-group coefficients, positive NLL, and microbatch backward passes; multistep SGD/AdamW gradient equivalence | No 4B–32B LLM, reward model, or online sampling; no measured end-to-end memory or latency claim |

Paper pages include exact v1 times, primary first-author affiliations, author release status, stable keys, code paths, and figure sources and SHA-256. No verified author code means “not found,” not “definitely unreleased.” GroupDPO's canonical identity remains **v1 on 2026-04-17T00:56:59Z**; local code follows September 1 v2, reported separately from first publication.

## Execution

Final frozen commit: `cc8126d359c51676920f8a072b5a46374254e13e`.

- [CPU raw results](../../../research-audits/oct25-priority-components/raw-cpu.json): three components × seeds 42/43/44, about 1.40 seconds.
- [A100 raw results](../../../research-audits/oct25-priority-components/raw-cuda.json): same three components and seeds, about 2.30 seconds.
- [Frozen-source proof](../../../research-audits/oct25-priority-components/frozen-sources.json) binds source hashes, commit, and paths for offline shallow-CI checks.
- Per-paper `metrics/component-cuda-seeds42-44.json` files and three sanitized receipts in `docs/gpu-validations/` remain separate.

Timings exclude connection, syncing, and tests and are **not full training times**. Cross-review found extreme continuous Inside-JEPA controls could overflow squared terms or total loss; explicit rejection and three negative tests were added before rerunning CPU/A100 from the fixed commit. Numerical mechanisms, real gradient updates, and negative controls do not establish pretrained capabilities, formal benchmarks, or evolve promotion.

```bash
python scripts/build_oct25_component_artifacts.py --check
python -m pytest tests/test_oct25_component_evidence.py
```

Acceptance binds exact checks/metrics, bounds, executed device, seeds, frozen source, raw bytes, catalog, per-paper metrics, and scope/ledger identities. Relabeling CPU as CUDA, wrong dates, unaccepted components, and altered promotion flags fail. Cost closure is distinct from acceptance.

## Discovery counts

[Source coverage](../../../research-audits/oct25-priority-components/source-coverage.json): eight arXiv pages still dated **2026-10-23**, 1,260 category records and 916 identities. Version lists and ordering match the prior batch, with zero new identity or version strings; cross-listings, replacements, and first discovery are not new publications. ME-OPD and Inside-JEPA are same-announcement follow-ups; GroupDPO came from a historical conference listing.

Google and Meta catalogs timed out, giving **unknown/null**, not zero. Nine DeepMind pages and 265 records yielded no bounded differences, not exhaustive coverage. [Independent priority review](../../../research-audits/oct25-priority-components/priority-source-review.json) records the successful [official Google EMNLP 2026 page](https://research.google/conferences-and-events/google-at-emnlp-2026/): 31 means listed entries, not new papers, and curl did not retrieve raw HTML, so no hash was invented.

[Title and identity audit](../../../research-audits/oct25-priority-components/google-emnlp-title-identity-audit.json) splits 31 entries into two already listed (including GroupDPO), 25 historical metadata leads (19 from 2026 and six from 2025), and four failed-link or mismatched exceptions. These leads had **no full-text review, qualification, cost evaluation, or implementation acceptance** in this batch and were not queued.

This snapshot remains historical. The later approved [closure of all 25](../../../research-audits/google-emnlp25-closure/README.md) delivered 14 components, eight high-cost not reproduced, and three unaccepted; do not continue counting the old leads as pending.

Other targeted findings in `additional_dispositions`:

- **Meta GenIA**: v1 October 8; changed push time did not change October 9 release HEAD. SAM3D plus geometry, rendering, and test-time optimization were too costly and not reproduced (review DONE); no checkpoint or rendering stack was acquired.
- **GRIP sparse retrieval**: 30 vCPUs, 222 GB RAM, 8.8M–138M passages, and GB-scale indexes; too costly, not reproduced, review DONE. No term-seed heuristic substituted for SparsePiPNN and graph search; distinct from post-training GRIP.
- **Meta AmbiGUI**: official source release verified. The README awaits a citation after publication; no canonical paper identity or first date yet. Record code release only, not a fabricated paper, capability integration, or implementation promise.

**Global review remains 2026-10-15**. Three fixed deliveries do not close October 16–25, conference listings, or full texts. Inaccessible archived methods were not reopened periodically.
