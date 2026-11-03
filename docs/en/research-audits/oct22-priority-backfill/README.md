# October 22: Google and Meta priority recheck

<!-- source-sha256: 6de7bb1365b536bec76bbef7c865554bbdd24bc5f4f195a5fe4110a57fd06eab -->

[简体中文](../../../research-audits/oct22-priority-backfill/README.md)

The eight arXiv categories still show **the same October 21 announcement**. Its 1,126 deduplicated identities and version records match PR #219, with no newly confirmed first publication or revision. These discoveries and release updates came from official repositories; they are not several new papers published within hours.

## Fixed deliverables

| Item | Source and classification | Low-cost delivery and limits |
| --- | --- | --- |
| [DeepSEA](../../../foundation-models/2610.26155-deepsea/README-en.md) | Google Research, first author Jiuzhou Han; October 19, same-announcement follow-up | External prediction scorer for five tasks, public-input projection, and coverage checks. Verified schema for 3,250 official MGSM rows in 13 languages; did not generate model predictions |
| [LogAct](../../../agent-research/2604.07988-logact/README-en.md) | Meta, first author Mahesh Balakrishnan; April 9 historical discovery | Local SQLite intent→vote→decision→execution/result protocol, crash recovery, and real small filesystem/database effects; not an LLM agent or distributed consensus |
| [ProPerAgent](../../../agent-research/2610.22671-proper-agent/README-en.md) | New official author repository, not a paper revision | Corrected code link, pinned revision, and CC-BY-NC-4.0 license. Inference/evaluation and GRPO entry points exist; complete training data and post-trained checkpoints are unreleased, so local evidence is unchanged |
| [SWE-sweep](https://swesweep.com/paper) | Meta FAIR; non-blocking archived exception | Report and site dates differ, exact first-publication date unconfirmed. The pinned repository LICENSE remains review-only. Source was not copied or executed and no implementation was claimed |

Both new components are **CPU-only L1 mechanism/interface diagnostics**, with zero model calls and no evolve promotion. No CUDA path was added or upgraded, so no A100/A30 receipt was invented. Three seeds validate contracts, not multilingual model or agent capabilities.

## Cost and data boundaries

- DeepSEA's full model matrix, five-task inference over 13 languages, and MetricX-24 were too costly; **full experiments not reproduced (review DONE)**. Local WMT24 chrF follows the authors' public scorer and is not MetricX-24. MetricX requests explicitly fail; chrF edge cases were compared with pinned SacreBLEU 2.5.1.
- Official DeepSEA datasets were only checked for pinned hashes, counts, and allowlisted projections. No text or gold was committed or used in training, selection, or evolve. Metric cards show contracts and recovery counts, not model accuracy from answer-bearing fixtures.
- Full LogAct LLM semantic voting, AgentDojo/swarm, and multi-host backend experiments were too costly; **not reproduced (review DONE)**. Logs alone cannot guarantee exactly-once external actions. Uncertain actions are not replayed by default, and external executors must honor explicit idempotence.
- SWE-sweep covers 100 repositories, 4,068 defects, and seven LMs. Table 24 (physical page 39) reports per-repository medians of 0.3–1.6 hours and a maximum of 5.5 hours across four shown configurations. **Full experiments not reproduced (review DONE)**; license and date exceptions are archived, non-blocking, and not automatically retried.

## Coverage and uncertainty

Item/version diffs across the eight categories were zero. The bounded DeepMind comparison covered nine pages and 265 records with zero additions. Google year and Meta catalogs timed out, so their diffs are **unknown, not zero**. Official repositories and author lists supported these four entries, not exhaustive organization-wide or full-text coverage.

The global watermark remains **2026-10-15**. A bounded recheck with two components does not close the full window. See [source receipt](../../../research-audits/oct22-priority-backfill/source-coverage.json), [cost and exceptions](../../../research-audits/oct22-priority-backfill/task-scope.json), and [official MGSM schema receipt without text](../../../research-audits/oct22-priority-backfill/deepsea-official-schema.json).

## Rerun

```bash
PYTHONPATH=src python scripts/run_oct22_priority_components.py \
  --output runs/oct22-cpu-contracts.json
PYTHONPATH=src python scripts/build_oct22_priority_artifacts.py --check
```

The runner requires a real matching Git commit and rejects uncommitted or modified source. Formal evidence retains [portable source proof](../../../research-audits/oct22-priority-backfill/frozen-sources.json), three-seed metrics, and negative controls. Optional `--mgsm-archive` checks the official archive hash and schema without downloading or printing answers.

Temporary dependencies, PDF renders, and site builds were cleaned after delivery. Receipts, failed runs, reusable public caches, and unrelated user files were retained.
