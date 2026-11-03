# Google/Meta historical leads and two affordable components (2026-10-21)

<!-- source-sha256: 02d54a9617efcdf7facc66d2a47d05b55229b5e9ae6aab7a09bfa1da963b448b -->

[简体中文](../../../research-audits/google-meta-closeout-20261021/README.md)

> Later update: This page and the machine records for 39 leads preserve the original review snapshot. The [subsequent component delivery](../google16-components-20261021/README.md) implemented bounded affordable paths for 16 accepted opportunities. Use that batch for current component status, not the historical undelivered count. Full experiments remain separately marked not reproduced.

This round covers 39 official Google leads, nine previously verified Google/Meta full-experiment decisions, the requested SpecGuard and Video Encoders components, and ledger/classifier fixes. It is not a new all-domain scan and did not close the other 497 earlier accepted candidates en masse.

## Review outcomes

| Scope | Outcome | What it does not mean |
| --- | --- | --- |
| 39 unique 2026 Google-source IDs | 16 core/evaluation opportunities, 14 full-experiment cost/resource closures, nine scope closures | The 16 were not implemented in this snapshot and are not new commitments |
| Nine verified Google/Meta original experiments | Eight too costly and one private production setting not reproducible, each recorded | Closing full experiments is not component delivery |
| SpecGuard / Video Encoders | Independent L1 components and actual CUDA evidence | Not full paper benchmarks, production gains, or Evolve promotion |
| October 15 acceptance field | Restored visibility of 14 explicitly accepted, unimplemented observations | No modification of frozen register or invented acceptances |

Keep separate [human-readable review](google39-report.md), [machine records](../../../research-audits/google-meta-closeout-20261021/google39-reviews.json), [current reconciliation](../../../research-audits/google-meta-closeout-20261021/current-state.json), and [cost/scope](../../../research-audits/google-meta-closeout-20261021/task-scope.json). Each entry records actual sections, primary URL, organization role, public code, cost basis, and receipt hash. `full_article_read=false`: focused checks are not paragraph-by-paragraph reading.

Retrieval from Google's official catalog does not mean Google first authorship. SpecGuard's first author is from MATS, with a Google DeepMind coauthor. Video Encoders has co-first authors from Stanford and Vast Intelligence Lab; the DeepMind author was an adviser only. Other coauthor and catalog relationships are separately recorded.

AI-Propeller's 0.23% production Ext-TSP result is retained, but allocation groups and explicit full traffic are unconfirmed. Missing A/B in the abstract is not a reason to miss it, and a production-related metric does not automatically pass strict A/B. General mechanisms among the 39 and industrial recommendation eligibility are separate; core acceptance does not waive industrial evidence.

## Two components and their limits

- [SpecGuard](../../../agent-research/2610.09159-specguard/README-en.md): real models independently generate specification and tests, generate a connector, and use the real Lean 4.24.0 kernel. Three custom micro-suite categories and no gold specifications. Logic compilation does not establish semantic fidelity; retain failed and `inconclusive`, not “no conflict.” Small-model A100 runs generated six times and 425 tokens; all three tasks were inconclusive at Spec and produced zero certificates. Test/connector stages were not reached with real models, and no larger model was substituted. Five fixed Lean assertion categories passed separately.
- [Video Encoders](../../../foundation-models/2610.06616-video-encoder-selection/README-en.md): Appendix I conditional token selector with frozen SmolVLM image tokens and question embeddings. Preserve source positions and intermediate streams at the same indexes. Uniform quotas and scene proxy explicitly replace unreleased inputs, not a full SITE allocator or learned refiner. On A100 select 32 of 256 with all three alignment errors zero; no video QA or end-to-end speed measurement.

Use existing pinned public model caches and under 1 MB public animated sample, no new large model download. SpecGuard capped at 18 calls, 8,000 new tokens, and 600 seconds. Video selection does not train or decode language. Bind frozen commit, actual executed source hash, public model/sample revisions, and sanitized CUDA receipts. Multiple seeds or receipts are not stable capability evidence.

## Ledger and classifier fixes

| Field/state | Meaning |
| --- | --- |
| `new` | No substantive review yet, not necessarily today's publication |
| `accepted-unimplemented` | Structured acceptance without implementation; not automatically queued |
| `review-deferred` | Deferred, not accepted; prose such as “next batch” or “pending” is not acceptance |
| `catalogued` | Catalog record exists; see `implementation_status` for component/interface/full distinction |
| `reviewed` | Explicit scope/cost/source disposition, not implemented code |
| `full_experiment_resolution` | Separate original full experiment decision; can coexist with `component_only` |

Do not infer commitments from free text; support structured October 15 acceptance. Foundation navigation recovered 39 catalogued entries from a handwritten allowlist (including this video component and 38 unchanged implementations). Institution/topic/year views must each match all 166 manifest keys and fail if a classification is missing. Generic `known` or “read methods” cannot hide accepted-unimplemented. Explicit cost closures do not reopen. Source exceptions need actual access failures; private data or environments instead retain paper resource evidence. Later explicit cost/component decisions remain visible.

Do not rewrite snapshots. Original 521 mixed 490 accepted and 31 deferred while missing another 14 acceptances. Keep frozen reconciliation and use current state for rolling counts. Current 513 accepted-unimplemented opportunities = 497 existing + 16 new, not 513 implementation tasks. Historical `review-deferred` records are unaccepted observations, not new backlog. Only the specified 39 and nine received substantive new closure. No global watermark movement or historical Google/Meta completeness. The old priority list still has 15 `new` observations (nine pre-2026 references and six prior P2/scope routes), outside the 39 and not treated as method-reviewed. Their identities remain in the original reconciliation; dates cannot close review.

## Reproduce the checks

```bash
PYTHONPATH=src python scripts/sync_google_meta_closeout.py --check
PYTHONPATH=src python scripts/audit_historical_priority_backfill.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
python -m pytest
```

`sync_google_meta_closeout.py` appends 62 observations only: 39 new reviews, 14 field repairs, and nine experiment/component decisions. ID groups do not overlap. Historical records remain intact.
