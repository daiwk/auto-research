# October 21: Google-priority backfill and low-cost components

<!-- source-sha256: 57684de36c11e3fff28557cb44267459d19e320a2841e87d823bf092f9f08a85 -->

[简体中文](../../../research-audits/oct21-priority-backfill/README.md)

This is not a new day's announcement. The eight arXiv categories still show October 21; the 1,126 deduplicated identities match PR #218. Of four previously undelivered entries, two are Google-related June/August backfills and two are follow-ups from the same announcement. This is neither four papers newly published within hours nor complete review of the window.

## Fixed scope

| Paper | Affiliation and date | Deliverable and boundary |
| --- | --- | --- |
| [MICE](../../../multimodal-models/2606.31278-mice/README-en.md) | First author at Modena and Reggio Emilia; Google coauthors; June 30 | Instance masks, log bias, and joint attention; not the full FLUX editor |
| [Grounding AI Agents in Contracts](../../../agent-research/2608.17177-spec-driven-tests/README-en.md) | Google first author; August 17 | Specification before tests; fixed/buggy dual execution protocol; no LLM or private defects |
| [FLINT](../../../foundation-models/2610.27273-flint/README-en.md) | UIUC first author; October 19 | Fixed-budget latent pooling, two residuals, and projected MaxSim; no trained retriever or PLAID |
| [System One multimodal reranking](../../../multimodal-models/2610.28435-system-one-rerank/README-en.md) | Aalto first author; October 20 | One real small-VLM forward pass for score readout and order preservation; not the 27B evaluation or decision tuning |

Costs were assessed from paper configurations before launching. Full experiments are **not reproduced (review DONE)**, with no automatic retries or large-model training queue. All components are L1 mechanism/interface diagnostics and cannot be promoted. Generated data and multiple seeds do not establish capability comparisons. Three CUDA paths require real A100/A30 receipts; the CPU spec protocol does not.

## Google and Meta source recheck

- DeepMind: nine pages and 265 records, unchanged since the prior capture. This is a bounded catalog diff, not exhaustive web coverage.
- Google's year catalog and Meta's catalog timed out. These are unavailable-source exceptions; `new_directory_urls=null` means unknown, **not zero**. Do not reimplement RPL, Muse Glimmer, or other existing entries.
- We individually checked Google's yearless homepage and three entries tagged 2027: two surveys and one Android privacy-interaction study, with no qualifying new model algorithm in scope. A 2027 venue tag cannot rule out 2026 first publication. Configuration adds at most two cross-year latest pages alongside the main 2026 catalog; tests expose truncation.
- We did not review all 1,126 identities again. UIBK-Embedding and other out-of-scope items are not falsely marked DONE. The global watermark remains **2026-10-15**.

See [sources and limits](../../../research-audits/oct21-priority-backfill/source-coverage.json) and [scope and costs for the four papers](../../../research-audits/oct21-priority-backfill/task-scope.json). SHA-256 binds captures; unavailable sources cannot prove no additions via empty diffs.

## Reruns and evidence

```bash
PYTHONPATH=src python scripts/run_oct21_priority_backfill.py \
  --device cpu --components spec-driven-tests --output runs/spec-protocol.json
PYTHONPATH=src python scripts/run_oct21_priority_backfill.py \
  --device cuda --components mice,flint --output runs/attention-pooling.json
PYTHONPATH=src python scripts/build_oct21_priority_artifacts.py --check
```

Multimodal reranking additionally needs a pinned public checkpoint cache, ID, revision, and download-provenance manifest. The runner emits declarations and measured data; admission verifies Git commit-to-blob proof, receipt, raw digest, recipe, checkpoint, three seeds, and metric binding. Reject nonexistent or incorrect commits, changed source, and receipts borrowed from another paper. See the [frozen source proof](../../../research-audits/oct21-priority-backfill/frozen-sources.json).

Temporary dependencies, source copies, PDF renders, and static builds from this round were cleaned after delivery. Shared public model caches, existing experiments, failures, and unrelated user files were preserved.
