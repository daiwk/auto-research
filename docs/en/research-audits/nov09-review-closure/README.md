# October 16–November 9 review reconciliation (in progress)

<!-- source-sha256: f178e4737908afb9197e8f815e1f9607b2d3e70f7dd6dda5b073076e1b8b18f4 -->

This batch reconciles discovery coverage and completes selected priority source reviews.
**Individual decisions are not yet complete for the entire window.** The official
[review watermark](../../../paper-discovery-watermark.json) remains **October 15, 2026**.
November 9 is the requested end date and the upper bound of this discovery window, not a completed watermark.
No training, GPU probes, or new implementations were performed.

## Discovery and priority evidence completed

We reused three real GitHub discovery runs: [October 22](https://github.com/daiwk/auto-research/actions/runs/39731868655),
[October 29](https://github.com/daiwk/auto-research/actions/runs/40832864995), and
[November 9](https://github.com/daiwk/auto-research/actions/runs/42582487347).
The 24 outputs cover four tracks, two recall modes, the requested dates, and the October and November identifier months.
The receipt preserves the original bounds, counts, runs, and hashes. The final run's foundation-model `LLM`
late-index query stopped at its 2,000-result cap. We preserved that receipt and exhausted two real replacement queries:
**2,098** October and **368** November results, with no cache fallback. The CI capture of the
[official arXiv listing](https://arxiv.org/list/cs.AI/new) had updated to November 9. Announcement date,
original v1 submission, reviewed version, and review time remain separate.

The [Google/Meta review](../../../research-audits/nov09-review-closure/priority-primary-reviews.json) records the directory scope,
individual changes, and original-source decisions. [Meta Axia](https://arxiv.org/pdf/2611.05643v1) §6 ties online metrics
to live-traffic A/B and incumbent production configurations, which is not evidence of an open reproduction.
[Google Busy Beaver](https://arxiv.org/html/2610.22603v1), [TURTLE](https://arxiv.org/html/2610.27307v2),
[Muir](https://arxiv.org/pdf/2611.08376v1), and [VERID](https://arxiv.org/pdf/2610.32755v1)
have specific source and resource findings. The [industrial review](../../../research-audits/nov09-review-closure/industrial-primary-reviews.json)
separates passing production evidence, offline-only studies, historical backfills, and access exceptions.
The [additional reviews](../../../research-audits/nov09-review-closure/additional-primary-reviews.json)
cover FP4 decoding, RSI, and OPD. Reviews cover the cited sections, not necessarily the entire paper.
When the cost is supported by evidence, the full experiment is **not reproduced (review DONE)**, with no automatic retry or implementation queue.

## November 10: first continuation

The first continuation added **70** original-source dispositions, bringing that snapshot to **119**, including **73** full experiments not reproduced due to cost.
Some first releases predate the window or belong to the end-of-day supplement, so the 70 cannot all be subtracted from the frozen in-window queue.

- The [priority and industrial follow-up](../../../research-audits/nov09-review-closure/supplemental-priority-reviews.json)
  checked Google and Meta affiliations against the papers. [Kuaishou WISE](https://arxiv.org/html/2611.06777v2)
  and [Walmart BehaveRec](https://arxiv.org/html/2610.36239v1) report production A/B tests in the body.
  [Meta's creator-exposure study](https://arxiv.org/html/2610.38155v1) compares simulation with production distributions; it does not pass the live-evidence gate.
- All **17** previously flagged [revisions](../../../research-audits/nov09-review-closure/revision-primary-reviews.json)
  were checked against fixed HTML or PDF versions. The version baseline was updated without upgrading implementation status.
  See also the [late-index original-source decisions](../../../research-audits/nov09-review-closure/late-index-primary-reviews.json)
  and [targeted method reviews](../../../research-audits/nov09-review-closure/continued-primary-reviews.json).
- The [late-index date reconciliation](../../../research-audits/nov09-review-closure/late-index-scope.json)
  found **395** of the original 624 records had only pre-cutoff dates and no later signals in the pinned captures.
  The [title and abstract screen](../../../research-audits/nov09-review-closure/abstract-scope-screen.json)
  resolved **33** explicit cross-domain matches. Both are window-scope decisions, not entries in the substantive review ledger.
- The [official Atom end-of-day receipt](../../../research-audits/nov09-review-closure/nov09-tail-source-receipt.json)
  identified **122** first releases between 18:23:24 Shanghai time and midnight that the frozen capture did not contain.
  **Nine** have decisions, including [TS-GEAR's production A/B test](https://arxiv.org/html/2611.12180v1#S4.SS3),
  [RecoGEM's production latency comparison](https://arxiv.org/html/2611.12296v1#S5.SS6), and the reuse of a prior experiment
  in the [rewritten AgentOPSD paper](https://arxiv.org/html/2611.12587v1).

## Title and abstract follow-up

This pass added **142** original-source dispositions, including **68** full experiments not reproduced due to cost.
The same ledger now has **261** dispositions, including **141** cost closures.

The [in-window routing artifact](../../../research-audits/nov09-review-closure/continued-in-window-routing.json)
reduces 22,220 captured observations to 4,941 versioned identities. The
[late-index and end-of-day follow-up](../../../research-audits/nov09-review-closure/continued-late-tail-triage.json) covers 334 more.
Normalized titles and abstracts did not establish exact cross-ID duplicates. Organization names in abstracts can be references,
models, or benchmarks, so they are search leads, not proof of affiliation. Routing does not substitute for original-source review.
An additional [46 in-window](../../../research-audits/nov09-review-closure/continued-in-window-scope.json) and **80** overlap records
were excluded based on their explicit subject and abstract, for this window only.

- **Google and Meta:** The [first](../../../research-audits/nov09-review-closure/continued-google-meta-reviews.json),
  [second](../../../research-audits/nov09-review-closure/continued-google-meta-followup-reviews.json), and
  [third](../../../research-audits/nov09-review-closure/continued-google-meta-third-pass-reviews.json) passes checked author leads against
  pinned originals: 51 dispositions, 15 with verified research participation by Google or Meta.
  [Accelerated Dataflow](https://arxiv.org/html/2610.22731v2) has Google authors
  and multi-worker load tests. [Meta PRISM](https://arxiv.org/html/2610.39175v1) uses online training, but evaluates effect on
  held-out production logs, not in a live A/B test.
- **Industrial evidence:** The [first](../../../research-audits/nov09-review-closure/continued-industrial-reviews.json) and
  [second](../../../research-audits/nov09-review-closure/continued-industrial-secondary-reviews.json) passes checked 58 pinned papers.
  [Tencent TGR-EvoDAG](https://arxiv.org/html/2610.32326v1) reports a 14-day A/B test on 5% of production traffic.
  Production impact, live logs, offline replay, simulations, and leaderboards are recorded separately.
- **Methods and evaluation:** See [selected methods](../../../research-audits/nov09-review-closure/continued-method-primary-reviews.json),
  [institution and production signals](../../../research-audits/nov09-review-closure/continued-signal-primary-reviews.json), and
  [late-index and end-of-day originals](../../../research-audits/nov09-review-closure/continued-late-tail-primary-reviews.json).
  Original experiments with evidenced prohibitive costs are not reproduced and their reviews are complete.
  Affordable core components accepted for consideration were not implemented or run in this review.

## What remains open

See `counts` and `pending_in_window_counts_by_title_abstract_route` in the [deduplicated inventory and receipts](../../../research-audits/nov09-review-closure/review-inventory.json).
The inventory preserves pending arXiv IDs, versions, tracks, and Shanghai dates, and counts the frozen window, late-index overlap, and end-of-day supplement separately.
**4,773** in-window identities, **169** late-index records, and **65** end-of-day records remain undecided.
An empty `pending_revisions` list closes the previously identified revisions, not revisions indexed later.
Manual, industrial, priority, low-signal, and broad-query hits in this inventory are **pending**, not automatic rejections.
Late-index overlap and revisions of known papers are tracked separately. Source exceptions require real retrieval attempts
and do not replace unread candidates. Directory matches are not proof of authorship.

Only completed dispositions enter the ledger. Unread candidates are not marked deferred, too costly, or reviewed.
The watermark can advance only after the remaining dispositions and exception reconciliation pass the existing audit.
