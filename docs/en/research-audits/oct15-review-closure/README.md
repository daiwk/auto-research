# Review closeout: 2026-10-13 to 2026-10-15

<!-- source-sha256: 4505149a2fa51a4867874000f37fb516bd71ec6175cf719e8aa076aedeea4295 -->

[简体中文](../../../research-audits/oct15-review-closure/README.md)

The review watermark advanced to **2026-10-15**. This is a bounded review as of the [recorded cutoff](../../../paper-discovery-watermark.json), not coverage of later hours, the entire web, every official page, or full implementation. This MR reviewed and checked evidence only: no training, GPU probes, large weight downloads, or algorithms.

High-cost candidates are **too expensive, not reproduced (review DONE)**. The original configuration, cost basis, and single-GPU budget remain visible. Do not enqueue them for retries, implementation, or executable evolve. Cost not cheaply determinable from read-only evidence is distinct from a paper reporting multiple GPUs or hours; neither is a local measurement. Affordable candidates were accepted for review, **not implemented**. Later work needs a small faithful acceptance scope.

## What was processed?

<!-- closure-summary:start -->
| Item | Count | Meaning |
|---|---:|---|
| Deduplicated configured retrieval identities | 3,742 | Not qualifying papers or full-text reads |
| Newly registered first releases in window | 794 | arXiv published date, not announcement or catalog date |
| Newly registered historical/overlap identities | 1,320 | Date/scope routing or separately checked historical discoveries |
| Existing identities | 1,628 | Inherited decisions, not new full-text reviews |
| Latest versions of known identities checked separately | 11 | Included in existing identities, not additive |
| Official non-arXiv identities | 2 | CATWILD and Meta AutoformBench; no fabricated arXiv ID or release date |
| High cost, not reproduced, review complete | 383 | Includes priority backfills/revisions, not pending training |
| Affordable review acceptances | 14 | Not implemented; no new experiments or automatic execution |
| Nonblocking source exceptions | 37 | Official date, identity, or pagination and two bounded full-text exceptions |
| New implementations or GPU training | 0 | Review completion is not implementation |

Cutoff: `2026-10-15T15:39:55+08:00`. The [register](../../../research-audits/oct15-review-closure/paper-register.json) has 3,744 unique identities.
<!-- closure-summary:end -->

Broad queries include math, clinical, and conventional control out-of-scope papers. The 794 are previously unregistered and first released in-window; one more in-window item already existed and is not counted twice. Historical or overlap cases may receive identity/date/abstract routing only. Each record states its actual reading mode: abstract screen, specific method/evaluation/resource passages, or inherited decision, not complete paper reading.

- [Readable priority decisions](priority-decisions.md): Per-paper reasons, costs, and version limits.
- [Deduplicated register](../../../research-audits/oct15-review-closure/paper-register.json): All identities, dispositions, receipts, and full-text exceptions.
- Domain decisions: [search, ads, and recommendation](../../../research-audits/oct15-review-closure/recommendation-reviews.json), [foundation and multimodal](../../../research-audits/oct15-review-closure/foundation-model-reviews.json), [post-training](../../../research-audits/oct15-review-closure/post-training-reviews.json), [agents and RSI](../../../research-audits/oct15-review-closure/agent-reviews.json).
- [Independent priority review](../../../research-audits/oct15-review-closure/root-priority-reviews.json) and [new-version review](../../../research-audits/oct15-review-closure/revision-reviews.json).
- [Nonblocking exceptions](../../../research-audits/oct15-review-closure/exception-archive.json) and [implementation reconciliation](implementation-status.md).

## Retrieval closure

Four tracks each use submission-date and late-index ID-month retrieval: eight receipts. Reuse the completed coverage of the [actual scan run](https://github.com/daiwk/auto-research/actions/runs/38689269736) and explicitly derive the October 13–15 review subset. **The original window was not narrowed to imply a new query.** Receipts retain artifact name, SHA-256, original window, actual query bounds, and filter rules. Repeated abstracts are omitted; dates, versions, hits, and metadata fingerprints are kept per ID.

The wide foundation-model LLM query spanning September and October hit its cap. A real October-ID-only rerun with a 4,000 cap and 100-page size exhausted **1,088** unique identities. Both original and replacement receipts remain. These are not first-release or qualifying-paper counts. All eight final receipts have no unresolved caps, failures, or cache fallback.

| Track | Submission-window receipt | Late-index receipt |
|---|---|---|
| Recommendation | [submission](../../../research-audits/oct15-review-closure/recommendation-submission-window-retrieval.json) | [late-index](../../../research-audits/oct15-review-closure/recommendation-late-index-retrieval.json) |
| Foundation | [submission](../../../research-audits/oct15-review-closure/foundation-model-submission-window-retrieval.json) | [late-index](../../../research-audits/oct15-review-closure/foundation-model-late-index-retrieval.json) |
| Post-training | [submission](../../../research-audits/oct15-review-closure/post-training-submission-window-retrieval.json) | [late-index](../../../research-audits/oct15-review-closure/post-training-late-index-retrieval.json) |
| Agents | [submission](../../../research-audits/oct15-review-closure/agent-submission-window-retrieval.json) | [late-index](../../../research-audits/oct15-review-closure/agent-late-index-retrieval.json) |

## Google, Meta, and official catalogs

Google/Meta remain highest priority. Recall by affiliation/topic first, then check production A/B or full traffic in the full text. Abstracts need not mention A/B. Treat new catalog URLs, existing URLs, older first releases, and revisions separately.

| Official scope | Pages | Records | New detail URLs | Inherited records |
|---|---:|---:|---:|---:|
| [Google](../../../research-audits/oct15-review-closure/google-source-review.json) | 28 | 412 | 7 | 405 |
| [Meta](../../../research-audits/oct15-review-closure/meta-source-review.json) | 6 | 144 | 11 | 133 |
| [Google DeepMind](../../../research-audits/oct15-review-closure/google-deepmind-source-review.json) | 9 | 265 | 0 | 265 |

Existing URLs with matching normalized titles inherit decisions. Rechecking listing dates is not rereading 803 papers. Meta coverage is first six pages only, not exhaustive pagination. Catalog updates, manuscript dates, software citation dates, and first public release are distinct.

- **Google G→W→L cascade:** Training stability and AUC/RMSE comparisons, no quantitative business A/B for this method. Affiliation does not waive the threshold.
- **CASI:** Production A/B qualifies, but replay and full training resources are private and single-GPU cost uncertain. P0, not reproduced, review complete.
- **DRanker:** First released October 11, a historical backfill. Global A/B and later holdout are disclosed; hundreds of millions of private examples are not a public reproduction.
- **PsyBer-Agent / AdCoEvo:** Fixed-backend human/simulated-user agreement and AuctionNet simulation, respectively, not production recommendation A/B.
- **Meta AutoformBench:** Distinct from the same-named document-understanding paper. Official October 13, manuscript October 5, and software citation September 30 have different meanings, so first release remains an exception. USD 200 is a per-task cap, not actual cost for every item. The full 341-task, nine-agent study was not reproduced.
- **Human-Guided Agentic EHR:** PDF methods and limits reviewed. No claimed new architecture or standalone capability benchmark. Clinical case study, not a new algorithm.

## Revisions do not upgrade old implementations

[Eleven latest-version reviews](../../../research-audits/oct15-review-closure/revision-reviews.json) are separate from new papers. Without a semantic old-version baseline, state which current passages were checked, not an invented exact algorithm diff.

- **Dice Roll v2:** Acknowledges synthetic coverage and error-count issues and retracts fixed repetition tiers. Run a pilot and estimate counts from variance components. No repository implementation; retain the old snapshot with correction rather than repeating the old advice.
- **SPARK v2 / SpecRoll v1:** Low-rank logit correction is not a rename of the fast/slow path. The [old write-up](../../../post-training/2608.04962-specroll/README-en.md) covers v1 only, not v2.
- **Rubric Dropout v2, RIDE v2, UniRec v5:** Latest methods, resources, and limits recorded separately. Older L1 and small public runs do not establish revised systems or production lift.

The [version baseline](../../../paper-discovery-versions.json) records 434 items. For 383 in this batch it records historical identity, date, observed version, and bounded cost/source information only. **Not 434 complete algorithm reviews.** Same versions do not requeue solely because old full-text baselines are absent. New versions and metadata evidence can reopen review.

## Exceptions and next scan

For inaccessible full text retain version, URL, actual HTML/PDF error, or bounded read limit. Do not mark it read. Unknown identity/date/pagination and full-text exceptions are nonblocking archival items. Unread candidates, capped queries, and absent decisions cannot disappear this way. Reopen source exceptions only on independent evidence; high-cost reproduction needs explicit user approval after cost disclosure.

The next scan overlaps from **October 14** through a new cutoff. The October 15 closeout stops at its recorded time; later submissions, announcements, or index arrivals belong to the overlap. Keep first releases, historical discoveries, and revisions separate.

See [delivery and validation](../2026-10-15-review-closeout.md). Machine checks include `python scripts/audit_paper_coverage.py --strict`, receipt regressions, independent implementation reconciliation, and strict docs build.
