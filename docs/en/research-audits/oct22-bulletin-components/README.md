# October 22 announcement: Scoped components and high-cost documentation

<!-- source-sha256: 394429320715aac3c6d10027ca06145baa1e1eab7aade5480c2e2a3d93f87b1f -->

[简体中文](../../../research-audits/oct22-bulletin-components/README.md)

The eight arXiv categories actually displayed **2026-10-22**. This differs from the preceding October 21 announcement, but announcement dates do not equal v1 first-release dates. Nor does a daily-list difference mean hundreds of additional qualifying papers. This page covers the fixed eight-paper scope and one existing metadata update; **it does not claim full-text closure of the announcement**.

## Delivery status

Five low-cost L1 components completed scoped implementation and three-seed contract checks. ALPS, ASTEROID, CORD, and CSD ran on a real A100; JEV is a CPU scoring protocol. Frozen source: `d767be53ac5a8a79f2b02aa23db0fcf3773ae588`. CPU diagnostics took about 2.53 s in total, and CUDA diagnostics about 2.73 s, excluding connection and synchronization. These are not full-experiment durations. The [evidence validator](https://github.com/daiwk/auto-research/blob/main/scripts/build_oct22_bulletin_artifacts.py) binds actual metrics, source proof, and GPU receipts. Three high-cost papers completed method and cost review; **full experiments were not reproduced (review DONE)**. This closes only the scoped deliverables. Scan counts are not actual capability runs.

| Fixed item | Exact v1 time (UTC) | Affiliation and scope |
| --- | --- | --- |
| [ALPS](../../../foundation-models/2610.30120-alps/README-en.md) | 10-21 17:57:11 | First author at UCSC, Google coauthors. Cross-crop geometry queries, overlap masks, frozen-teacher normalization, and per-image MSE interface. L1 A100 passed. |
| [ASTEROID](../../../agent-research/2610.30105-asteroid/README-en.md) | 10-21 17:50:31 | First author at UW, Meta collaborators. Asymmetric on-policy distillation, causal history, and expert trajectory interface. L1 A100 passed. |
| [CORD](../../../post-training/2610.29965-cord/README-en.md) | 10-21 16:19:22 | First author at CUHK, Tencent collaboration. Joint RL/distillation conflicting-gradient operator. L1 A100 passed. |
| [CSD](../../../post-training/2610.28895-csd/README-en.md) | 10-20 20:18:46 | NVIDIA. Shared events across tokenizers, residual mass, and distillation objective. L1 A100 passed. |
| [JEV with multiple correct options](../../../system-one/2610.29217-jev-multicorrect/README-en.md) | 10-21 05:18:35 | Probability allocation and external scoring for multiple correct options. L1 CPU passed without claiming to load a large JEV model. |
| [AW-0](../../../multimodal-models/2610.30136-aw0/README-en.md) | 10-21 17:59:56 | UC Berkeley / NVIDIA / UPenn. Three experts jointly generate code, video, and actions. The 48-H100 and real-robot matrix is too expensive and not reproduced. |
| [Right On Q](../../../foundation-models/2610.29378-right-on-q/README-en.md) | 10-21 08:03:24 | First author at UMich, Meta AI collaboration. On-policy distillation on long traces after quantization calibration. Too expensive to reproduce in full. |
| [FineSID](../../../recommendation-components/2610.29138-finesid/README-en.md) | 10-21 03:19:02 | Industrial CTR stagewise learning from content to relevance to personalization. Method, online evidence, and cost documentation only; full experiment not reproduced. |

The prior retrieval cutoff was **2026-10-21 17:53:03 UTC**. Only ALPS and AW-0 first appeared after it. The other six **entered this announcement**, not first publication in the last few hours, and do not create a whole new historical backlog. See the [fixed scope](../../../research-audits/oct22-bulletin-components/task-scope.json) for identities, categories, institutions, and costs, and individual paper pages for source and implementation boundaries.

The existing [ProPerAgent](../../../agent-research/2610.22671-proper-agent/README-en.md) appeared as `2610.22671v2` with title **MemoProAgent**. Keep stable key `proper-agent`, treating this as a v2/source metadata update. Do not create a duplicate, count it among the eight papers, or claim new training or stronger evidence.

## Source counts: What do 964 and 934 mean?

Raw retrieval ran from **2026-10-22 02:38:56.955358 through 02:39:40.251785 UTC**. Displayed counts, parsed counts, and all three partition counts agree in all eight categories:

| Category | All entries | New | Cross-list | Replacement |
| --- | ---: | ---: | ---: | ---: |
| cs.AI | 370 | 63 | 148 | 159 |
| cs.CL | 221 | 89 | 48 | 84 |
| cs.CV | 212 | 121 | 17 | 74 |
| cs.IR | 34 | 17 | 8 | 9 |
| cs.LG | 379 | 137 | 103 | 139 |
| cs.RO | 120 | 69 | 9 | 42 |
| cs.SD | 25 | 18 | 3 | 4 |
| eess.AS | 17 | 6 | 7 | 4 |
| Total | **1,378** | **520** | **343** | **515** |

A paper can appear in multiple categories, and can be new in one but cross-listed in another. Stripping version suffixes yields **964 unique identities**. There are 520 unique new-partition, 285 cross-list, and 349 replacement identities; these sets overlap and cannot be added.

The [prior snapshot](../../../research-audits/oct22-priority-backfill/source-coverage.json) had 1,126 identities, with 30 in common. **934** identities entered this daily snapshot and 1,096 left. Daily announcements are not a cumulative paper library:

- **934 is neither 934 first releases nor 934 eligible unimplemented papers.** It includes new announcements, cross-lists, replacements, and identities absent from the prior snapshot.
- Literal version-string difference is 964, not 964 confirmed revisions. Some baseline strings had no version suffix, so check papers individually before assigning revision changes.
- The 520 new-partition identities are announcement classifications. They do not imply October 22 v1 dates or successful full-text review of all 520.
- This batch checks methods and resources for eight fixed papers and follows up existing `proper-agent` v2. Other fetched records do not automatically become implementation tasks or count as complete.

See [coverage records](../../../research-audits/oct22-bulletin-components/source-coverage.json) for counts, category/version identities, page SHA-256, and fetch receipts. Raw retrieval JSON SHA-256: `681b1c01a198a8bb4d229830f17cf5e8ce7548ff54acff030e068a7f61cbac17`. This page does not copy all abstracts or commit benchmark text or gold.

## Google/Meta priority and coverage limits

Google's 2026 catalog and Meta's publication catalog timed out, so differences are **unknown / null**, not zero. The unfiltered Google Research homepage and official repositories received limited supplementary checks. An unchanged homepage cannot replace a failed catalog scan, and absence of Google in an abstract cannot rule out collaboration. ALPS's Google coauthors and ASTEROID and Right On Q's Meta collaborators were verified in author listings; grouping still follows first-author affiliation.

DeepMind yielded nine pages and 265 entries with no difference in the bounded catalog. This says only that the successfully fetched pages did not change, not that all organization papers or repositories were exhausted. ALPS, AW-0, and others were cross-checked from arXiv and official author repositories without requiring prior catalog appearance.

**The global review watermark stays 2026-10-15.** Complete retrieval of eight announcements is not complete full-text review. Eight scoped deliverables do not close the full October 16–22 window. Passing components cannot turn failed Google/Meta sources, unread papers, and unaccepted candidates into exhaustive coverage.

## Cost and acceptance rules

Evaluate full models, long trajectories, multi-GPU runs, and actual robotics under the project cost threshold. Expensive full experiments reach the terminal status **review DONE / not reproduced**, not perpetual retries. Real GPU verification of low-cost components establishes scoped formula, gradient, or protocol behavior only, not full original results.

The batch stays L1, `diagnostic_only=true`, `promotion_eligible=false`, and `evolve_integrated=false`. Four GPU receipts bind frozen source and actual three-seed A100 runs. The ledger moved from `accepted-unimplemented` to scoped `component_only` acceptance. Separate paper metrics and local diagnostics; a fixture or externally supplied correct prediction scoring 1.0 is not model success.

## Recompute audit records

```bash
PYTHONPATH=src python scripts/build_oct22_bulletin_source_audit.py /path/to/fixed-capture
PYTHONPATH=src python -m pytest tests/test_oct22_bulletin_source_audit.py
```

This script uses no network or models, executes no upstream code, and changes neither runners/curator nor the watermark. It verifies actual announcements and partition completeness for eight categories, strips abstracts, records source identities, initializes five pending components and three terminal cost-only entries, and appends only the current ledger scope. **It refuses to overwrite an existing same-name batch**, preventing a rerun from resetting completed GPU or integration acceptance and leaving prior batches unchanged.

Recheck later acceptance offline with `scripts/build_oct22_bulletin_artifacts.py --check`. `--finalize` updates only this batch after real evidence passes, without scanning or training again.
