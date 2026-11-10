# October 16–November 9 review reconciliation (in progress)

<!-- source-sha256: 5cc05a2127d63d316bff30ca8f79a0ec7f7212631982a4de526fd728deb3f821 -->

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

## November 10 continuation

The same batch gained **70** original-source dispositions, bringing its total to **119**, including **73** full experiments not reproduced due to cost.
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

## What remains open

See `counts` and `pending_bucket_counts` in the [deduplicated inventory and receipts](../../../research-audits/nov09-review-closure/review-inventory.json).
The inventory preserves pending arXiv IDs, observed versions, tracks, Shanghai dates, and first-pass buckets.
In the frozen capture (November 9, 18:23 Shanghai time), **4,941** in-window identities and **221** late-index records still need review.
An empty `pending_revisions` list closes the previously identified revisions, not revisions indexed later.
The end-of-day supplement adds **113** candidates without final decisions. Late indexing and later source corrections are subject to the stated coverage limits.
Manual, industrial, priority, low-signal, and broad-query hits in this inventory are **pending**, not automatic rejections.
Late-index overlap and revisions of known papers are tracked separately. Source exceptions require real retrieval attempts
and do not replace unread candidates. Directory matches are not proof of authorship.

Only completed dispositions enter the ledger. Unread candidates are not marked deferred, too costly, or reviewed.
The watermark can advance only after the remaining dispositions and exception reconciliation pass the existing audit.
