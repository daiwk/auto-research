# October 16–November 9 review reconciliation (in progress)

<!-- source-sha256: 68b6aa69c276a42b3106bcb8c614d7270f272460592299ad301888a00da058b2 -->

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
That snapshot had **261** dispositions, including **141** cost closures; the next section records the subsequent increment.

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

## November 11: batch dispositions under the approved selection rule

The user approved a **not selected for this window** disposition when the title and abstract explicitly establish
an application report, repeated evaluation, or perspective without a new independently reproducible algorithm or public benchmark.
The [selection policy](../../../research-audits/nov09-review-closure/batch-terminal-policy.json) does not authorize rejecting a new method
because of low priority, missing code, or absent A/B wording in its abstract. Abstract screening is not full-text or cost review.

This increment resolved **648** of the original **5,007** pending identities: **286** reviews of necessary original-source sections
and **362** individually evidenced title/abstract dispositions. The same ledger now contains **547** original-source decisions,
including **231** full experiments not reproduced due to cost, with no automatic retry or implementation assignment.
Of the new original-source decisions, **143** accept bounded cores or protocols without implementing them, and **90** decline
the original full experiment based on its resource configuration. The remainder concern unavailable specialist resources,
out-of-scope subjects, unselected application reports, or an unmet industrial live-evidence gate. No training, experiments, or GPU runs occurred.

- **Priority sources:** The [first](../../../research-audits/nov09-review-closure/batch-terminal-priority-reviews.json) and
  [second](../../../research-audits/nov09-review-closure/batch-terminal-priority-followup-reviews.json) sets verify affiliations and method/experiment configurations.
  Newly verified sources include [Google's randomized pre-visit clinical trial](../../../research-audits/nov09-review-closure/batch-terminal-google-clinical-review.json),
  [Google Urania](../../../research-audits/nov09-review-closure/batch-terminal-google-urania-review.json), and
  [SPELUNKA with a Google coauthor](https://arxiv.org/html/2610.23979v2).
  The clinical trial is not a recommender CTR A/B test; Urania's private-conversation distribution analysis is not a new image-generation model.
- **Production evidence:** [Seven deployment leads](../../../research-audits/nov09-review-closure/batch-terminal-production-reviews.json)
  and [another production experience report](../../../research-audits/nov09-review-closure/batch-terminal-production-b-review.json)
  distinguish randomized A/B, post-launch observation, trace replay, and incumbent production baselines.
  DoorDash's use of feature flags for A/B testing does not establish a randomized experiment for the cleanup method.
  Volvo's new configuration had not been released to testers at interview time.
- **Overlap and tail:** The [first](../../../research-audits/nov09-review-closure/batch-terminal-overlap-primary-reviews.json) and
  [second late-index sets](../../../research-audits/nov09-review-closure/batch-terminal-late-secondary-reviews.json) resolve the remaining **169** records;
  the [end-of-day set](../../../research-audits/nov09-review-closure/batch-terminal-tail-primary-reviews.json) resolves the remaining **65**.
  Official fixed-version PDFs were read when HTML was unavailable. Failed downloads were not relabeled high cost.
- **Metadata decisions and corrections:** [Group A](../../../research-audits/nov09-review-closure/batch-terminal-scope-a.json) retains **177** dispositions,
  and [group B](../../../research-audits/nov09-review-closure/batch-terminal-scope-b.json) retains **185**.
  Each preserves the version, capture hash, title/abstract witnesses, and individual reason. These window-only records do not enter the substantive global ledger.
  Independent checks withdrew **27** overbroad exclusions: [three received original-source decisions](../../../research-audits/nov09-review-closure/batch-terminal-insurance-review.json),
  and [24 returned to pending](../../../research-audits/nov09-review-closure/batch-terminal-corrections-b-reviews.json).
  A specialist application or negative result alone does not establish the absence of an independent algorithm.

Official directories retain bounded coverage claims. A changed DeepMind homepage count has not been mapped to two specific paper identities;
current access limitations for Google's year-filtered page and Meta's entry point are recorded in the priority-source receipt.
None establishes whole-site exhaustion.

## What remains open

See `counts` and `pending_in_window_counts_by_title_abstract_route` in the [deduplicated inventory and receipts](../../../research-audits/nov09-review-closure/review-inventory.json).
The inventory preserves pending arXiv IDs, versions, tracks, and Shanghai dates, and counts the frozen window, late-index overlap, and end-of-day supplement separately.
**4,359** in-window identities remain undecided. Both the identified late-index and end-of-day pending queues are now **zero**.
An empty `pending_revisions` list closes the previously identified revisions, not revisions indexed later.
Manual, industrial, priority, low-signal, and broad-query hits in this inventory are **pending**, not automatic rejections.
Late-index overlap and revisions of known papers are tracked separately. Source exceptions require real retrieval attempts
and do not replace unread candidates. Directory matches are not proof of authorship.

Only completed dispositions enter the ledger. Unread candidates are not marked deferred, too costly, or reviewed.
Many remaining records explicitly propose new algorithms or benchmarks; they cannot be closed under the rule for reports without new methods.
No authorization has been received to close every non-priority P2 merely as unselected, so that broader policy has not been applied.
The watermark can advance only after the remaining dispositions and exception reconciliation pass the existing audit.
**This increment has not advanced the watermark to November 9.**
