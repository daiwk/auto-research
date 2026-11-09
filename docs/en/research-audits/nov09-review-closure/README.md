# October 16–November 9 review reconciliation (in progress)

<!-- source-sha256: 855a25f59221e81bcfc7e8801d52d48c9bc5028de6f0e5aaa2f0a94425bc4b21 -->

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

## What remains open

See `counts` and `pending_bucket_counts` in the [deduplicated inventory and receipts](../../../research-audits/nov09-review-closure/review-inventory.json).
The inventory preserves pending arXiv IDs, observed versions, tracks, Shanghai dates, and first-pass buckets.
Manual, industrial, priority, low-signal, and broad-query hits in this inventory are **pending**, not automatic rejections.
Late-index overlap and revisions of known papers are tracked separately. Source exceptions require real retrieval attempts
and do not replace unread candidates. Directory matches are not proof of authorship.

Only completed dispositions enter the ledger. Unread candidates are not marked deferred, too costly, or reviewed.
The watermark can advance only after the remaining dispositions, version checks, and exception reconciliation pass the existing strict audit.
