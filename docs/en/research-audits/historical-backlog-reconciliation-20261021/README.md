# Reconciliation of historical candidates and actual delivery gaps (2026-10-21)

<!-- source-sha256: ecc7224e9b325e946dcfbb09410720204eff58061f271fb6d2633f814c427b9a -->

[简体中文](../../../research-audits/historical-backlog-reconciliation-20261021/README.md)

> Frozen reconciliation at merge commit `8357f497`, not rolling status. See the [Google/Meta closeout](../google-meta-closeout-20261021/README.md) for later ledger/classifier fixes, 39 reviews, and two components. Counts such as 521/504 retain the historical meaning, not a current implementation queue. Rerun historical commands in a separate checkout of that commit.

## Correcting the previous status

“Historical work is all done” was inaccurate. Selected fixed implementation batches and bounded review dispositions were complete, not every historical candidate. Mixing review watermark, batch closure, candidate acceptance, and code delivery caused the confusion. Reporting 54 and 521 as remaining work before reconciliation was also misleading.

We deduplicated paper identities and compared three frozen review registers, 55 ledger batches, the manifest, docs, and actual implementation searches. Google and Meta received priority checks via official author blocks and resource configurations. **No training, model or data download, or GPU work.** Only reports and reproducibility materials were added; the original ledger, watermark, and classifier were unchanged.

## Reconciled counts

| Original figure | Composition | Correct meaning |
|---|---|---|
| 521 “old undelivered” | 490 structured acceptances and 31 deferred-after-review leads | Not 521 approved tasks. No duplicate IDs or already-cataloged items found in that set |
| 14 missed by old count | Oct15 register explicitly accepted but unimplemented; incomplete ledger fields caused reviewed classification | Include in acceptance reconciliation. Reading full text is not delivery |
| 504 accepted, undelivered | 490 + 14 | Repository observation: accepted, no current catalog entry or delivered terminal outcome in original ledger. Not 504 approved or low-cost implementations |
| 54 “pending verification” | 39 substantive 2026 review leads, nine 2024/2025 references, six P2/scope/type dispositions | All Google/DeepMind official leads, not accepted tasks. Meta count in this set is zero |

Three frozen registers merge to **534 accepted identities: 26 with catalog/docs, four with explicit cost dispositions, and 504 without catalog or terminal outcome**. The 26 establish documentation, not uniformly full capability reproduction. Existing L1 diagnostics are not queued again.

## Cost dispositions

Of the **nine** complete experiments on the Google/Meta priority shortlist, eight were closed as too costly and one as unavailable private production. Each decision follows source/configuration review, not a blanket high-cost label. Seven were among the 504 acceptances and two among the 31 deferred leads.

- **497** old accepted candidates still lack a full-experiment disposition and need cost/scope review or delivery. They are not known affordable and not automatically queued.
- The other seven closed full experiments still have undelivered standalone components. Assess each low-cost component separately; closing the full experiment is not code delivery.
- **29** unaccepted deferred leads remain without an implementation claim or commitment.
- **39** 2026 Google leads need substantive method/evidence review, not coding.
- Nine 2024/2025 references and six P2/non-implementation leads stay separate. Old date is neither a quality judgment nor evidence of method review.

**The old ledger still displays 521** because it was not changed here. This report recomputes dispositions. Ledger/classifier synchronization is separate and must not reopen experiments already closed. Full experiments and low-cost components are separate axes.

## Google and Meta priority items

| Paper | Affiliation or role | Actual gap and cost decision |
|---|---|---|
| SpecGuard `2610.09159` | First author MATS, Google DeepMind coauthor | **Priority affordable candidate:** Real model to Lean specification, independent tests, and real kernel on a few tasks. Unimplemented. Full benchmark/repeat matrix not reproduced |
| Video Encoders `2610.06616` | Google DeepMind advisor, not first-author affiliation | **Priority affordable candidate:** Original training-free selection-only path. Unimplemented. 96 A100-hour refiner and full benchmarks not reproduced |
| Gumbel Straight Flow `2610.00497` | Google DeepMind involvement | Separately assess actual small-vocabulary teacher/student core; unimplemented. Million-step training not reproduced |
| Growing→Looping `2602.16490` | Google collaboration | Separately scope real small-model growing/looping; unimplemented. 200B/400B-token training not reproduced |
| TrustMI `2610.06064` | Meta collaboration | Assess small-model steering separately; unimplemented. Full six-model, 70B and 120B-judge matrix not reproduced |
| Flow / AutoRepair `2610.07289` | Google | Internal code, CI, and production data unavailable; full reproduction closed. Public APR needs separate scope, not a Google production replication |
| Knossos / Ariadne `2610.04721` | Meta coauthorship | Unimplemented. Original 4×A100 multistage training not reproduced; importing graph results is not core training |
| MIMESIS `2610.09484` | Meta / NYU | Unimplemented. 32×A100 for about 4.8 days and 16-GPU dual RL not reproduced; a fixed simulator is not the defining algorithm |
| VISTA `2510.15831` | Google collaboration, 2025 historical item | Unimplemented. About 0.7M text tokens and 28 videos per round, partly private tasks; full experiment not reproduced. Orchestration fixtures do not reproduce the core |

See [nine priority entries](priority-google-meta.md) for source locations, author code, and boundaries, and [formal dispositions](../../../research-audits/historical-backlog-reconciliation-20261021/data/this-audit-dispositions.json). These are verified priority cases, **not exhaustive affiliation checks**. Many legacy candidates lack complete author caches. Label unconfirmed affiliation; use of Gemini or Llama is not authorship evidence.

## Complete lists

- [Foundation models: 212 accepted-undelivered observations](accepted-foundation-model.md)
- [Agents: 206](accepted-agent.md)
- [Post-training: 85](accepted-post-training.md)
- [Recommendation: 1](accepted-recommendation.md)
- [31 deferred leads, including two full-experiment closures](deferred-candidates.md)
- [The original 54 official leads split 39/9/6](google-source-leads.md)
- [Machine reconciliation, source SHA-256, and register pointers](../../../research-audits/historical-backlog-reconciliation-20261021/reconciliation.json)

The seven closed full experiments among the 504 are marked in the tables, not disguised as pending full runs.

## Why earlier reporting was misleading

1. **Delivery scope was overstated.** B00–B11 covers 74 fixed papers and H01–H07 covers 55. Those roadmaps did not include all historical candidates. Oct07 itself lists 494 accepted pending implementation.
2. **Review was conflated with implementation.** Previously a ledger appearance meant reviewed, and inherited known status hid earlier acceptances.
3. **Free-text heuristics remained unstable.** “Keep as next-batch reference” and “verify next batch” counted as implementation-pending. Fourteen Oct15 acceptances were missed because resolution and unimplemented status were not recognized.
4. **Catalog year, newly found sources, and first release were mixed.** Nine of the 54 precede 2026, plus scope/type exclusions. `2511.02767` was misdated once; official v1 was 2025-11-04, not 2026-04-23.

These are reporting and counting errors, not finished code with unchecked boxes. No evidence supports bulk promotion to implemented.

## Recompute and scope

```bash
PYTHONPATH=src python docs/research-audits/historical-backlog-reconciliation-20261021/audit.py --check
```

See [interactive audit.ipynb](../../../research-audits/historical-backlog-reconciliation-20261021/audit.ipynb). The audit uses checkout `d1b4851b`: 55 batches and 4,943 ledger rows across 4,821 identities. None of 113 duplicate ledger identities occurred in the original 521. No normalized-title duplicates in scope; shared acronyms do not justify merging papers. No claim of rereading all 504 full texts, exhausting affiliations, or moving the October 15 watermark.

Evidence: [Oct07 snapshot](../oct07-review-closure/README.md), [Oct12 scope](../oct12-review-closure/README.md), [Oct15 delivery](../2026-10-15-review-closeout.md), [H01–H07 scope](../../paper-audits/2026-historical-p0-implementation-roadmap.md), and [B00–B11 scope](../../paper-audits/2026-historical-scan-plan.md). Independent checks: [global](../../../research-audits/historical-backlog-reconciliation-20261021/data/global-review.json), [Google](../../../research-audits/historical-backlog-reconciliation-20261021/data/google-review.json), [Meta](../../../research-audits/historical-backlog-reconciliation-20261021/data/meta-review.json), and [official v1 dates](../../../research-audits/historical-backlog-reconciliation-20261021/data/date-checks.json).

Recomputation, notebook assertions, Ruff, and links across eight reports passed. Cleaned about 371 MiB of temporary site output and 844 KiB of duplicate JSON/old Sources output. Retained about 1.4 MiB of auditable reports, registers, and official Sources artifacts; shared weights and data untouched.
