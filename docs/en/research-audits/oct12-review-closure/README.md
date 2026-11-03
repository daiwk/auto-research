# Review through October 12, 2026: coverage, backfill, and exceptions

<!-- source-sha256: d20ffdca1b970e70d3681df7ca1b89d254e166a4dfdbf47ac36f1a5227525bc0 -->

[简体中文](../../../research-audits/oct12-review-closure/README.md)

The [central status](../../../paper-discovery-watermark.json) review watermark advanced to **2026-10-12**. Four tracks, two channels, per-ID dispositions, and official sources and exceptions passed `audit_paper_coverage.py --strict`. This closes a defined review window, not the entire web or all implementations. Search began at 12:55 Shanghai time on October 12, 2026 and covered October 8–12 plus announcement overlap and month-number backfill. It does not claim late-day, unpublished, or unindexed October 12 material. The next scan overlaps from October 11.

## Counts

| Item | Count | Meaning |
|---|---:|---|
| Deduplicated IDs across eight query groups | 1,597 | Four research tracks, each with submission-window and late-index channels |
| Inherited reviewed records | 1,019 | Not newly published items or new full-text reads |
| Newly reviewed query records | 578 | Each has an actual disposition; unavailable papers are deferred, not accepted as full-text reviews |
| Directed discoveries outside queries | 10 | Nine papers from the 16 frozen entries plus conditional ECC; not added to query recall |
| Inherited records outside current queries | 3 | Prior proof retained rather than silently deleting them |
| Full register | 1,610 | 520 accepted, 618 deferred after review, 424 rejected/out of scope, 48 already recorded |

See [paper-register.json](../../../research-audits/oct12-review-closure/paper-register.json) for reasons, full-text SHA, reading locations, and inherited sources. Acceptance adds a paper to the suitable implementation queue; it does not mean full original-model/environment reproduction. [Implementation reconciliation](implementation-status.md) independently checks catalog, executable registration, and GPU evidence. It does not infer capability gains from acceptance. See [batch scope](../../../design/oct12-papers-and-review.md) for acceptance of the 16 frozen implementations.

## Full-text review evidence

- [12 industrial recommendation/search/ads items](../../../research-audits/oct12-review-closure/recommendation-reviews.json): method, production experiments, and limits recorded separately.
- [105 post-training items](../../../research-audits/oct12-review-closure/post-training-reviews.json): public objectives and evaluation boundaries. Google LES was explicitly deferred, not rejected for missing abstract A/B language.
- [139 primary foundation-model items and four prior cross-checks](../../../research-audits/oct12-review-closure/foundation-model-reviews.json), plus [the other 119](../../../research-audits/oct12-review-closure/foundation-tail-reviews.json).
- [203 Agent items](../../../research-audits/oct12-review-closure/agent-reviews.json): 203 abstracts, 198 bounded full-text checks, five unavailable full texts explicitly deferred.
- Independent frozen shortlist sources: [four post-training papers](../../../research-audits/oct12-review-closure/frozen-post-training-reviews.json), [six Agent/Jev papers](../../../research-audits/oct12-review-closure/frozen-agent-reviews.json), and [five foundation/multimodal papers](../../../research-audits/oct12-review-closure/frozen-foundation-reviews.json). FORTE is included in the 12 industrial entries.
- [Conditional ECC](../../../research-audits/oct12-review-closure/ecc-review.json): real online click evidence confirmed, but private logs, unpublished code, and a commercial image backend defer implementation outside the current 16.

Reading scope is marked per entry: decisive methods and experiment passages, not every paragraph and appendix. Code links are evidence to verify, not proof that a dependency or web shell is a complete author implementation.

## Official institutional sources

| Source | Catalog scope | Actual verification |
|---|---|---|
| Google Research | 28 pages, 406 entries | Inherited proof for 398 URLs; individually checked eight genuinely new URLs for identity and date; excluded Preview/JavaScript noise |
| Meta | Six pages, 144 entries | Identical prior URL set; refreshed pagination and inherited decisions without recounting new papers |
| Google DeepMind | Nine pages, 265 entries | Official dates checked individually and predate the window; not 265 full algorithm rereads |

Receipts: [Google](../../../research-audits/oct12-review-closure/google-source-review.json), [Meta](../../../research-audits/oct12-review-closure/meta-source-review.json), [DeepMind](../../../research-audits/oct12-review-closure/google-deepmind-source-review.json), and [Google new-entry verification](../../../research-audits/oct12-review-closure/google-new-entry-decisions.json). Google/Meta arXiv affiliations were also traced from manuscripts, not institutional catalogs alone. Production experiments in the body take priority; omission of A/B from an abstract is not a rejection reason.

The [33 archived exceptions](../../../research-audits/oct12-review-closure/exception-archive.json) are non-blocking and reopen only with new evidence. Do not archive confirmed in-window unread candidates to evade review. The strict source-exhaustion watermark is retired; `all_sources_exhaustive=false` and `implementation_complete=false` remain unchanged.

## Follow-up candidates

Keep individual rationale for new qualifying leads separate from the 16 accepted implementation commitments. Google/Meta Self-Preservation, MetaEncoder, and X-AgentRed, and industrial LLM-BlockFE need distinct data, evaluation, or safe execution boundaries. Verify by priority in later batches; do not advertise unimplemented candidates as capability implementations.
