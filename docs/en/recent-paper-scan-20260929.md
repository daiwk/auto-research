# September 29 overlap scan and RSI review

<!-- source-sha256: 26369dad23ffb1ea97f69a5c81261725131d209a9f5e19f3643813dc047fd288 -->

[简体中文](../recent-paper-scan-20260929.md)

## Coverage and source repairs

Four tracks, September 20–29, 2026 with announcement overlap, up to 50 per query, deduplicated against adapters and audits. New means search hit not yet recorded or terminally reviewed, not published on September 29 or eligible. Late indexing remains in scope.

| Track | Hits | Unaudited | Implemented | Audited |
|---|---:|---:|---:|---:|
| Search/ads/recommendation and LLM | 141 | 109 | 20 | 12 |
| Foundation | 336 | 331 | 5 | 0 |
| Post-training | 252 | 215 | 11 | 26 |
| Agent | 296 | 292 | 1 | 3 |

No arXiv cache fallback, but no cross-source watermark advance. Google Research, Google DeepMind and Meta AI main pages could be fetched but produced zero IDs, as did RecSys; SIGIR was configured as a PDF for an HTML regex. Google/Meta GitHub first yielded 8/2 IDs, then HTTP 403 during verification. The scanner now records arxiv_ids_extracted, no_arxiv_ids and coverage_complete and fails on incompatible PDFs. Rescan correctly reported incomplete coverage; official detail paging and structured feeds still needed.

### First repair pass

[Google Research](https://research.google/pubs/) and [Meta AI](https://ai.meta.com/global_search/?content_types%5B0%5D=publication&page=1) listings now supply titles/details; bounded reverse arXiv lookup accepts only exact unique identities. Meta listing dates help cross-month recall. Preserve unmatched titles, links, page counts and query failures in JSON. Old 2025 RecSys HTML and SIGIR PDF are removed only from daily configuration, not historical audit. Trial counts 184/1048/542/950, Google 3 pages ~45 entries, Meta 2 pages ~48 entries, partial; DeepMind no_arxiv_ids. Early trials predate final ranking/date rules and are not final counts. [Meta MaD-RL](https://ai.meta.com/research/publications/mad-rl-matching-distributions-for-calibrating-llms-with-reinforcement-learning/) matches [2609.31644](https://arxiv.org/abs/2609.31644), proving discovery not reproduction. Full paging, DeepMind details, current venues and unmatched entries still needed; cross_source.coverage_complete stays false.

### Official venues and pagination

Added [Google DeepMind](https://deepmind.google/research/publications/) titles/details/dates, RecSys 2026 poster [page 1](https://recsys.acm.org/recsys26/posters-1/), [page 2](https://recsys.acm.org/recsys26/posters-2/), [page 3](https://recsys.acm.org/recsys26/posters-3/) and the [SIGIR 2026 list](https://sigir2026.org/en-AU/pages/program/accepted-papers). Initial parse: 30 DeepMind homepage entries, RecSys 46/44/42 and SIGIR 667 deduplicated titles across tracks. SIGIR links to the list, RecSys to an accordion. These are list counts, not new or eligible papers. Venue dates are not publication dates; arXiv citations do not establish poster identity. Decompress gzip responses by header. The initial sources were partial and identity lookups capped.

DeepMind's /research/publications/page/N/ now enumerates up to a configured cap; nine observed pages held 30/30/30/30/30/30/30/30/24 entries, not deduplicated or judged eligible. Eight [RecSys program](https://recsys.acm.org/recsys26/recsys-26-program/) session pages returned 14/13/14/14/14/12/13/14 entries, potentially duplicating posters. Daily paper-official-review-<track>.json queues unmatched titles, links and affiliations, Google/Meta first. Shared normalized titles group review, not automatic identity. Exact manifest-title matches avoid duplicates. Actions GitHub API sends repository-scoped GITHUB_TOKEN only to HTTPS api.github.com. Paging failures are explicit while successes remain. Google Research timed out in source-only verification; Meta/GitHub availability also varies. Unmatched identity, first affiliation and full-text evidence still need review; coverage remains false.

### September 30 failure and fix

The [first merged workflow](https://github.com/daiwk/auto-research/actions/runs/36600018480) hit HTTP 429 on all four tracks without candidate artifacts, not zero candidates. Four parallel jobs broke the [legacy arXiv rule](https://info.arxiv.org/help/api/tou.html) of one connection and at most one request per three seconds despite per-client delay. Serialize tracks, throttle globally, and allow up to five scanner retries without converting failures to empty results. The [repair validation](https://github.com/daiwk/auto-research/actions/runs/36601663347) succeeded live on four tracks, zero fallback and arxiv_transport.coverage_complete true.

| Track | Hits | Unaudited | Implemented | Audited | Official identities pending |
|---|---:|---:|---:|---:|---:|
| Industrial/LLM | 184 | 127 | 22 | 35 | 1192 |
| Foundation | 1048 | 951 | 20 | 77 | 357 |
| Post-training | 542 | 450 | 22 | 70 | 352 |
| Agent | 950 | 846 | 19 | 85 | 355 |

All still have cross_source.coverage_complete false. Four industrial Google/Meta machine hits are keyword false positives. MaD-RL identity is established but post-training admission is separate.

## Full-text decisions

- [FLVM, Google/YouTube](https://arxiv.org/abs/2609.32839), September 26 v1, P0. §4 reports 14-day Shorts A/B primary viewer enjoyment +2.67%. [KuaiRand-Pure concept reproduction](../reproductions/2609.32839-flvm/README-en.md) uses real consumption/feedback and temporal splits, not satisfaction surveys or production features. Three seeds do not reproduce online lift; priority tagging missed the real affiliation.
- [RRSI](https://arxiv.org/abs/2609.24972): recursive harness proposals/selection need fixed tasks, budget and independent regression/OOD; no adapter.
- [RSIBench-Data](https://arxiv.org/abs/2607.25886): test using training feedback to improve post-training data; needs public tasks and leak prevention, not integrated.

[RSI](../evolution/recursive-self-improvement.md) is a cross-track experimental loop, not a seventh metric index or changed paper classification. [Recursive OPSD](../reproductions/2609.30652-recursive-opsd/README-en.md) remains a small three-seed mechanism diagnostic. [KuaFu](../reproductions/2609.31045-kuafu/README-en.md) and Recursive OPSD still need P0 scale/baseline work; no fabricated training or zero-advantage RL success. Machine p2-deferred-review is not rejection; read Google/Meta affiliations and deployment evidence. Continue overlap from September 20 until source and candidate disposition close.
