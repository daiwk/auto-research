# Historical priority-source reconciliation: usage and boundaries

<!-- source-sha256: b4547404276461bb51983652567322cdb7b8ab059f39854f7b1584da3069ea58 -->

[简体中文](../../../research-audits/nov13-history-repair/history-reconciliation.md)

No new identities in recent announcements, or no new links on the first and last institutional pages, **does not establish that historical institutional papers have been reviewed**. A separate historical inventory retains explicit arXiv identities from registered institutional/event, project, or author sources and reconciles them against the canonical manifest and substantive method/cost dispositions. The default configuration includes the Google Research 2026, cross-year, DeepMind, and Meta institutional listings, plus [Google at COLM 2026](https://research.google/conferences-and-events/google-at-colm-2026/). Generic decisions do not hard-code ScientistTwo, its identity, or a particular conference.

## Automatic output during routine discovery

Use the existing command and source registry; this is not a separate backfill step that can silently be forgotten:

```bash
PYTHONPATH=src python scripts/discover_papers.py \
  --track agent \
  --start-date 2026-11-12 --end-date 2026-11-13 \
  --cross-source-config configs/paper-discovery-sources.json \
  --output paper-candidates-agent.json
```

This also writes `paper-candidates-agent-historical-review.json` by default. The full report remains embedded in `cross_source.historical_review` in the main artifact. Override the separate path with `--historical-review-output PATH`. Without `--output`, the report is included in the main JSON printed to standard output rather than silently omitted.

The optional source property `historical_inventory=true` reuses `DiscoverySource`, existing pagination budgets, and identity extraction. Each successful page retains its actual URL, capture time, `decoded_text_sha256`, decoded UTF-8 byte count, and any version explicitly present in the original link. This hash identifies decoded text supplied to the extractor, **not an unexplained claim about original network bytes**. Raw HTTP/file receipts may be archived separately. An institutional source alone does not establish authorship of every linked reference.

| Default historical source | Maximum listing pages | Title lookups | Detail lookups |
| --- | ---: | ---: | ---: |
| Google Research 2026 listing | 40 | 5 | 12 |
| Google Research cross-year listing | 2 | 3 | 6 |
| Google DeepMind listing | 20 | 5 | 12 |
| Meta publications listing | 6 | 5 | 12 |
| Google COLM 2026 event page | 1 | 0 | 0 |

These are **existing configured limits**, not claims that every page succeeded or every method was reviewed. Adding the historical flag to the four existing institutional sources only retains identities from pages already fetched; it adds no pagination, detail budget, or additional historical crawl. A source can end early, fail partially, or exceed its budget. A PDF response, empty shell, or page without extractable identities cannot establish coverage merely through HTTP success. Pagination/capture gaps become explicit historical-report exceptions, while detail-lookup errors remain in the main source artifact. If the paper's original text later proves unavailable, record actual read attempts and use the existing source-exception policy. An indexed identity is not verified methodology.

Historical identities are not discarded by the recent-publication date filter. Only source-recalled Google/Meta historical identities needing substantive review reopen priority original-source review. Ordinary old P2 selections, explicit cost closures, source archives, and known catalog identities do not thereby become new implementation tasks. Industrial search/ads/recommendation still requires original-text online evidence; the A/B gate is unchanged.

## Offline recomputation without a web cache

A saved main discovery artifact contains the source inventory. After installing repository dependencies, a normal clone can reconcile it offline:

```bash
PYTHONPATH=src python scripts/reconcile_priority_history.py \
  --artifact paper-candidates-agent.json \
  --source-config configs/paper-discovery-sources.json \
  --manifest docs/research-manifest.json \
  --ledger docs/paper-discovery-ledger.json \
  --output priority-history-agent.json
```

A separate source artifact with top-level `source_stats` is also accepted. This command makes no network requests, rereads no `.cache` web pages, downloads no weights, performs no training, and changes neither the ledger nor watermark. It recomputes against the **current** manifest and ledger, so later cataloging or substantive closure can change results. Preserve earlier artifacts; recomputation is not a fresh web capture.

## Review, cataloging, and implementation are separate dimensions

| Reconciliation status | Meaning and follow-up |
| --- | --- |
| `needs-review` | An exact priority-source identity lacks an identifiable substantive closure. It requires `priority-fulltext-review`, not acceptance or automatic implementation |
| `catalogued` | The same explicit arXiv identity exists in the canonical manifest. Similar titles or URL slugs do not establish identity or create duplicate implementations |
| `reviewed` | Retain substantive review or an explicit high-cost no-reproduction disposition. A completed cost review is not algorithm implementation or validated capability |
| `accepted-unimplemented` | Original-source review accepted the opportunity, but implementation is not delivered. This record adds no automatic execution authorization |
| `archived-exception` | Retain an existing unverifiable-source archive without pretending the method was verified or retrying it automatically |

Date triage, `historical_first_publication`, a generic `known` label, and window-only P2 selection cannot alone replace priority-institution method/cost review. Regression tests cover ScientistTwo missing→needs-review, old P2→priority original review, and explicit high-cost DONE remaining closed. `method_review_completed` is true only when structured original-text locations exist; cost/source closure remains separate.

`source_identity_count` counts bounded source identities, **not new qualifying papers, accepted items, or an implementation backlog**. The report never starts reproductions or registers Evolve operators. It keeps `automatic_implementation_queue=false` and `automatic_retry=false` and does not advance the review watermark.

## Disclose coverage and exceptions

This reconciles configured sources and captured pages, **not exhaustive Google/Meta history**. An uncaptured configured source, actual access failure, over-budget pagination, a page without fixed identities, or an identity without a capture witness receives an explicit `exceptions` entry. An uncovered item with `attempted=false` is not an archive following a real attempt. Unavailable sources must not be presented as zero additions or reviewed methods.

Register additional institutional blogs, conferences/events, projects, or author pages in the same registry, preserving traceable URLs, institutional leads, the historical flag, and bounded pagination. Priority signals still require verification against original author affiliations. New revisions, independent institutional evidence, or author clarification can reopen cases under existing rules; inexpensive fixtures must not bypass cost or GPU-validation gates.

Alongside existing main candidate JSONs, workflows should upload `paper-candidates-*-historical-review.json`, or the explicit custom output path. Present source reconciliation and implementation deliverables separately.
