# Paper discovery and coverage audit

<!-- source-sha256: d407c640a18fd246444a90aed7316cfa7cc0074f31534c44e690c5fca1057bb8 -->

[简体中文](../paper-discovery-audit.md)

The latest completed window in this snapshot is [2026-10-13 to 2026-10-15](research-audits/oct15-review-closure/README.md). First releases, historical discoveries, and revisions are counted separately. High-cost candidates are explicitly not reproduced and their reviews are complete. See the [unified status](../paper-discovery-watermark.json) for the current date, coverage, cutoff, and exceptions.

The [October 16–November 9 reconciliation](research-audits/nov09-review-closure/README.md) records four tracks and two recall modes, replaces a capped query, and adds priority source decisions. All 17 previously flagged revisions were checked. In-window and late-index candidates and the remainder of November 9 after the capture cutoff remain open; **the watermark has not advanced**.

The latest bounded implementation batch is [2026-10-26](research-audits/oct26-components/README.md). Eight low-cost L1 components passed same-source CPU and real A100 checks with three seeds. Eight high-cost papers were documented without reproduction and are review DONE. Google and Meta were checked first. New announcements, recent source backfill, and historical catalog backfill are counted separately. This is distinct from closing an entire review window: announcement entries are not new papers, and the batch does not move the watermark automatically. The [roadmap](research-roadmap.md) retains previous batches.

The [Harness² and Google/Meta backfill](research-audits/harness2-priority-repair/README.md) fixed a historical filtering gap. **An older date or a previous ledger appearance does not mean method and cost review are complete.** Frozen records are preserved, but date-screening labels such as `historical_first_publication` no longer imply reviewed deduplication. Accepted but undelivered items are separately labeled `implementation-pending`. Explicit high-cost no-reproduction and source exceptions remain terminal and are not retried automatically. This correction does not claim full historical coverage or move the review watermark by itself.

The [2026-10-21 reconciliation](research-audits/historical-backlog-reconciliation-20261021/README.md) checked the earlier 54/521 counts by identity and delivery evidence. The 521 count included 31 deferred-after-review items and omitted 14 accepted candidates: the true source observation was 504 accepted-but-undelivered candidates, not 504 automatic implementation tasks. The 54 official-source leads were classified by first release and document type into 39 pending 2026 reviews, nine older references, and six non-implementation dispositions. The new report separates Google/Meta priority items and final decisions not to reproduce full experiments. At that snapshot it had not yet rewritten the original ledger or classifier; old script outputs are not the current queue.

See the [2026-10-01 to 2026-10-07 closeout](research-audits/oct07-review-closure/README.md) for the full candidate list, individual reviews, and supplemental retrieval receipts. Date-window and identifier-month retrievals have separate records. Google's official catalog is read to its declared page count with over-budget pagination noted. Verify paper identity and release dates after reading the catalog. Unverifiable entries are not reviewed papers.

## Review watermark, coverage, and archived exceptions: 2026-10-10

The user retired the strict source-exhaustiveness watermark. Progress no longer depends on proving that every page or source on the web has been found. The unified status has three parts:

- **Review watermark:** Complete both retrieval channels for all four tracks in a fixed window and give every retrieved candidate a terminal disposition. Check Google/Meta official entries for scope, identity, and dates. After actual attempts, unresolved entries can be archived publicly.
- **Coverage:** State the window, domains, channels, official pages and record counts, and limitations. It is not a claim of sitewide or web-wide exhaustiveness.
- **Archived exceptions:** Archive unverifiable identities/dates, unavailable full text, and pagination uncertainty after actual attempts. They do not block the watermark, count as accepted or implemented, or require automatic retries.

Track implementation independently. `accepted/deferred` is not implementation completion, and watermark movement does not change evidence tiers. The current state excludes `source_exhaustiveness_watermark`; the audit rejects reintroducing it. Old receipts are historical snapshots.

### High cost, not reproduced: Review complete (clarified 2026-10-15)

If the paper's configuration or an existing measurement exceeds reasonable costs on one A100/A30 or a Mac, record the cost basis and mark **too expensive, not reproduced**. The item is **review DONE**, not an unfinished GPU TODO. It does not block the batch or review watermark and does not enter automatic rerun, implementation, or executable evolve queues. Code, metrics, and GPU receipts are not needed to close this review. Reopen reproduction only if the user explicitly requests it after seeing the cost.

For ledger compatibility retain terminal `status: deferred` and existing catalog `deferred_high_cost`. New decisions may add `resolution: not_reproduced_high_cost` to distinguish explicit no-reproduction from ordinary follow-up candidates:

```json
{
  "id": "2610.20174",
  "priority": "P1",
  "status": "deferred",
  "resolution": "not_reproduced_high_cost",
  "reason": "Too expensive to reproduce: published training uses 2 nodes with 8 H800s each; only one A100/A30 is available locally.",
  "cost_assessment": {
    "source_url": "https://arxiv.org/html/2610.20174v1",
    "basis": "Published training corpus and training hardware paragraphs",
    "scale": "7B model, multidomain expert training and merging, 74K preference pairs",
    "available_resource": "One A100 or A30, or a local Mac",
    "cost_type": "published_configuration_not_local_measurement"
  }
}
```

This closes the review for that candidate without claiming implementation or verified capability. It does not excuse unread candidates or incomplete retrieval. Advance the watermark after normal coverage and disposition checks even when high-cost items are not reproduced.

Use [paper-discovery-watermark.json](../paper-discovery-watermark.json) for current status, the [October 15 acceptance report](research-audits/oct15-review-closure/README.md) for individual source checks, and [nonblocking exceptions](../research-audits/oct15-review-closure/exception-archive.json) for the archive. Preserve older watermark snapshots without rewriting them as current conclusions.

Exceptions are limited to unresolved identity or date, unavailable full text, and unprovable catalog pagination coverage. Record the URL, original reason, attempts, scope screening, and reopening conditions. They do not count as accepted. “Unread,” capped queries, or confirmed in-window but unreviewed entries are not exceptions. Google/Meta priority, online A/B or full rollout, implementation, and GPU validation requirements remain unchanged.

When arXiv identity is confirmed but bounded HTML/PDF reads actually fail, keep the paper in the candidate register. `source_exceptions` records versions, failed URLs and errors, and reopening conditions, linked to archive entries. Status is `archived_source_exception`, not accepted, full text read, or implemented. Abstract-only evidence does not bypass full-text acceptance.

`python scripts/audit_paper_coverage.py --strict` checks the unified file and artifacts. It rejects missing channels, failed/capped queries, unreviewed candidates, ignored items without attempts, in-window papers mislabeled historical, and bounded acceptance described as exhaustive or implemented. Keep an overlap window for the next scan. Reopen exceptions when official metadata/full text changes or an independent source surfaces new evidence. Preserve original reasons and sources; do not retry unchanged exceptions each round.

By default `scripts/discover_papers.py` reads the unified archive. Unknown identities matching source URL, title, and date enter `archived_items`, not the active queue. New sources, title changes, or added dates reopen entries. Identified arXiv candidates are unaffected, and archival does not make `coverage_complete` exhaustive.

Earlier misses came from incremental discovery without a complete candidate workflow, not one missing keyword. Search scope, four tracks, online evidence, code availability, deduplication against existing work, and explicit exclusions were not reconciled in a machine-checkable ledger. A batch answered what it found, not what remained unprocessed in the fixed window.

Since 2026-08-08, each new batch follows this workflow:

1. **Freeze scope:** Record search cutoff, time window, industrial search/ads/recommendation and LLM applications, foundation models, post-training, agents, each track's subtopics, and P0/P1 rules. Global batches declare `scope_kind: global` and `required_subtopics`. A few results per domain do not establish coverage.
2. **Combine discovery routes:** arXiv categories/queries; institutions including Google, Meta, ByteDance, Alibaba, and Kuaishou; related work and citation chains; author pages and official repositories.
3. **Archive evidence:** Industrial papers need quantitative online A/B or user-approved full rollout. Other domains need public benchmarks, same-budget controls, code status, and locally executable core mechanisms.
4. **Deduplicate stably:** Match arXiv IDs, formal publication IDs, and normalized titles. Cross-check adapter, post-training, agent, and evolve mutation registries.
5. **Assign terminal dispositions:** Each ledger item ends as `implemented`, `deferred`, or `rejected`; deferred and rejected need reasons. Unresolved P0/P1 items prevent completion.
6. **Verify implementation:** Require code paths, method-specific telemetry, stable metrics, a complete Chinese write-up, original key figures, catalog placement, applicable evolve mappings, and tests.
7. **Audit closure:** Run `python scripts/audit_paper_coverage.py --strict` and the full tests. The PR describes counts and reasons for implementation, deferral, and exclusion.

## Google and Meta priority

Google (including Google DeepMind and YouTube) and Meta (including Instagram) have highest priority for industrial search, advertising, recommendation, and LLM applications. An in-scope paper with quantitative online A/B or user-approved statistically significant explicit full rollout is P0, even if another paper covers the same subtopic.

Institution-priority batches use `scope_kind: institution-priority` and record each organization's product/institution queries, all matched candidate IDs, and each candidate's affiliation, evidence threshold, P0 rationale, and final disposition.

The strict audit checks those fields and candidate closure. arXiv API lacks author affiliations. Check first-page affiliations and search full text for A/B, live launch, full traffic, and fully deployed. TokenMinds (Google/YouTube) and SlimPer (Meta/Instagram) triggered the 2026-08-09 correction.

Separate candidate recall from evidence decisions. First form the candidate set by **affiliation and search/ads/recommendation or LLM application topic**, then read PDF/HTML full text. A/B wording in an abstract is not a recall filter. Abstracts, titles, and API metadata alone cannot justify rejecting online evidence. Institution-priority runs must declare `candidate_discovery_gate: affiliation-and-topic`, `abstract_online_evidence_required: false`, and `full_text_review_required: true` and record evidence sections and wording, or strict audit fails. SlimPer is the regression example: its abstract says deployment gains; §4.3 describes A/B, full traffic, and statistical significance.

The [machine ledger](../paper-discovery-ledger.json) converts search results into auditable dispositions; it does not replace search. Append batches, never overwrite them.

The [2026-08-08 all-domain gap audit](full-domain-gap-review-20260808.md) corrected the claim that closing a local batch meant no omissions and recorded the next P0/P1 queue.

The 2026-08-24 scan expanded to 2026-01-01 through 2026-08-24. See the [initial historical scan](recent-paper-scan-20260824.md) and [fixed batches](paper-audits/2026-historical-scan-plan.md) for the 3,906-candidate machine ledger, 404-paper full-text list, and B00–B11 plan. All 331 previously unresolved full-text candidates received dispositions: 55 P0, 273 retained P2, and three unavailable. See the [historical audit](paper-audits/2026-historical-fulltext-review.md).

Those historical batches closed. Daily incremental scanning resumed 2026-08-25; see [the first scan](recent-paper-scan-20260825.md) for exclusions and four implementations. Candidates without a terminal state do not disappear on the next scan.

The [2026-09-27 four-track overlap](recent-paper-scan-20260927.md) restored arXiv pagination, but Google/Meta publication pages failed. New industrial P0 and cross-domain P1 reviews went to the [roadmap](research-roadmap.md). Under that historical policy, the all-source watermark stayed fixed pending supplemental source and individual decisions.

The [2026-08-26 scan](recent-paper-scan-20260826.md) deduplicated 363 submissions across five arXiv categories and performed high-priority full-text checks. Additions were TAGR, WeMM-Embedding, two post-training methods, and four agent methods. No Google/Meta entry passed that reverse search; TAGR alone passed the quantitative industrial bar.

## 2026-08-13 GenRec correction

Netflix GenRec (arXiv 2608.10257) appeared on 2026-08-10 but the old pipeline used strict AND across long queries, read only eight hits per query, and audited only discovered candidates. In-window records could be lost before review.

The fix unions nine topic-query groups, priority-institution searches, and up to 200 paginated results per group; deduplicate by canonical arXiv ID and preserve `matched_queries`. Full-text evidence follows retrieval. No A/B in the abstract is not a rejection. Daily Actions emits 14 days of `paper-candidates.json` as a pending-review artifact, not accepted industrial evidence. Foundation, post-training, and agent tracks have separate query matrices.

```bash
PYTHONPATH=src python scripts/discover_papers.py \
  --track recommendation \
  --lookback-days 14 \
  --page-size 50 \
  --maximum-results-per-query 200 \
  --cross-source-config configs/paper-discovery-sources.json \
  --output paper-candidates.json
```

Institution queries are supplemental because arXiv API has no structured affiliation. Check Google/Meta first-page affiliations and official sources, then full text.

Since 2026-10-07, main retrieval uses `--recall-mode submission-window`, passing the fixed window to arXiv rather than locally filtering the first N hits across history. Also run `--recall-mode late-index` with separate checkpoint/output to retain older dates with newer identifier months. Daily Actions publishes both sets for review of their union. Both channels allow 2,000 hits per query to avoid the previously observed 200-hit cutoff; any remaining cap prevents watermark movement.

Late-index limits ID months server-side with `id:YYMM.*` and unions months across boundaries. No lower submission-date bound removes old submissions with new IDs. Completing configured date queries does not establish full-text review or exhaustive source coverage.

The daily task diffs candidates against the manifest and historical ledger, then shows Google/Meta priority, other new candidates, and processed candidates in the Actions summary. Netflix and other institutions remain in recall without priority alerts. The [roadmap](research-roadmap.md) tracks implementation.

## Cross-source recall and recording dispositions

The scheduled job also reads [the source configuration](https://github.com/daiwk/auto-research/blob/main/configs/paper-discovery-sources.json): official Google Research, Google DeepMind, and Meta AI publications; RecSys/SIGIR conference pages; and Google/Meta research GitHub organizations. It supports author pages and Semantic Scholar references/citations with `--snowball-seeds`. Hits preserve source name/type/URL, known affiliation, direct/reference/citation relation, snowball seed arXiv ID, and individual source failures so a failed page cannot silently reduce coverage.

The artifact is still a review queue. After manual full-text review, record decisions:

```json
{
  "source_artifact": "paper-candidates-recommendation.json",
  "decisions": [
    {"id": "2608.12345", "priority": "P0", "status": "rejected", "reason": "The full text has no quantitative online evidence"}
  ]
}
```

Then apply and audit them:

```bash
PYTHONPATH=src python scripts/record_discovery_review.py \
  --artifact paper-candidates-recommendation.json \
  --decisions review-decisions.json \
  --batch review-20260820-recommendation

python scripts/audit_paper_coverage.py --strict \
  --pending-artifact paper-candidates-recommendation.json
```

Every `new` candidate needs `implemented`, `rejected`, or `deferred`. Strict audit checks the pending artifact and ledger together; unresolved candidates fail instead of disappearing into the next round.
