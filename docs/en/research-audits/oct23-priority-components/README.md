# October 23, 2026: Recent announcement and Google-priority backfill

<!-- source-sha256: 150b60d5a3974a280fc6b89576fa2c24872e4d4ab68a8ca66f1ba294f3546248 -->

[简体中文](../../../research-audits/oct23-priority-components/README.md)

This fixed batch includes **eight low-cost components and one high-cost reference**. Components passed frozen-source three-seed acceptance: OpenAttention, MoEZip, AOPD, GIFT, and PAIR ran on a real A100; Gemma protocol, Jev-DLC, and finite-policy RKL ran on CPU. Status is `bounded_scope_complete`. The global watermark remains **2026-10-15**; this is not announcement-wide or window-wide full-text closure.

Frozen source: `f3fbc6db4db084a2a6a4ee754f9a3d9e5b606ac7`. Eight CPU diagnostics took about 9.56 seconds and five CUDA diagnostics about 1.73 seconds, excluding connection and sync, not full training times. [Raw CPU](../../../research-audits/oct23-priority-components/raw-cpu.json), [raw CUDA](../../../research-audits/oct23-priority-components/raw-cuda.json), and [proof](../../../research-audits/oct23-priority-components/frozen-sources.json) bind metrics and five sanitized receipts. `scripts/build_oct23_priority_artifacts.py --check` verifies raw hashes, exact seeds, fixed checks/metrics, catalog boundaries, and receipts offline; labels cannot upgrade evidence.

## Fixed scope

| Paper | Bounded work | Classification and limits |
| --- | --- | --- |
| [Google Gemma four-arm protocol](../../../foundation-models/2609.30716-gemma-priority-protocol/README-en.md) | Four arms, common holdout, BCa/TOST, and fixed author-log recomputation | September 25 backfill; CPU protocol, not new inference |
| [OpenAttention](../../../foundation-models/2610.30951-openattention/README-en.md) | Single-head tensor mechanism | Cross-list; not full LLM or CUDA kernel performance |
| [MoEZip](../../../foundation-models/2610.30206-moezip/README-en.md) | Routing-aware KV selection | Cross-list; fixed routing does not stand in for the full model |
| [AOPD](../../../post-training/2610.31563-aopd/README-en.md) | Original advantage and distillation loss | Cross-list; no full rollout or LLM training |
| [GIFT](../../../post-training/2610.30796-gift/README-en.md) | Gradient-informed distillation filtering | Paper-specific method and resources; not full reasoning RL |
| [PAIR](../../../recommendation-components/2610.30941-pair/README-en.md) | Intent and preference scoring interface | Industrial offline/online evidence separate from local mechanisms |
| [Jev-DLC](../../../system-one/2610.31521-jev-dlc/README-en.md) | Typed feedback decision updates | CPU mechanism, no large Jev checkpoint |
| [Google collaboration RKL](../../../foundation-models/2610.30844-rkl-policy-distillation/README-en.md) | Complete Algorithm 1 for finite MDP | Google coauthor priority; not ordinary token rKL or LLM training |
| [OneLatent](../../../recommendation-components/2610.30675-onelatent/README-en.md) | Original methods, online evidence, and cost references | Full experiments too costly, not reproduced (review DONE), no retry |

The [fixed scope](../../../research-audits/oct23-priority-components/task-scope.json) and paper blocks record exact v1 times, primary first-author affiliations, code/license/revision, and stable keys. New URLs, new/cross-list entries, true first publication, backfill, and revisions are distinct. Gemma reruns and RKL LLM experiments retain their specific `full_experiment_status` rather than being forced into the high-cost category.

## Sources and limits

[Source receipt](../../../research-audits/oct23-priority-components/source-coverage.json): eight October 23 arXiv announcements, 1,260 category entries and 916 identities; 499 new, 287 cross-list, and 474 replacement entries. These are not 916 new or fully reviewed papers. Exact v1 times were checked individually for selected work.

Google returned 29 pages/428 records and five new URLs versus the last successful 423-record capture; the failed intervening capture was not an empty catalog. Meta six pages/144 records and DeepMind nine/265 had no bounded URL difference, not zero organization-wide publications. Failed captures must report unknown/null.

| New Google catalog entry | Disposition |
| --- | --- |
| Words Speak Louder Than Order | Full text confirmed sole Google author; September 25 backfill included as protocol |
| Stakes-Adaptive Verification and Origin-Traced Rollback | Official TDC12058 public October 8; full text returned 403/HTML, not a PDF. Non-blocking archive exception without claims of method review or invented implementation |
| Regional Policies for Memory Tiering Systems | REGENT virtual-address-region memory tiers are outside this LLM/recommendation/Agent scope; no fabricated first-publication time |
| π-Flux Tuning of Quantum Paramagnetism... | Condensed-matter quantum physics, out of scope |
| Nature of the bosonic edge phase... | Condensed-matter quantum physics, out of scope |

RKL's Google collaboration was found through an independent full-text author check, without requiring a catalog entry or abstract affiliation. Targeted checks do not exhaust all coauthors. Do not recount ALPS, ASTEROID, CORD, CSD, Jev multi-correct options, AW-0, Right On Q, or FineSID, or count MemoProAgent v2 as a new paper.

Four other boundaries: Adobe LARA (2610.30423) reports observational production stratification, not confirmed controlled quantified A/B or approved full-traffic comparison. baseVultra (2610.30154) announcement/ID conflicts with the linked v1 August 23 date; do not force it into the day count. DConstrain (2610.30920) author information was unavailable and Verbalizing Activation Differences (2610.30934) lacks explicit affiliations; Google/Meta links are unknown, not disproven. None is automatically queued.

Four targeted post-training checks stay outside execution scope. MCPD (2610.30880) reports 4×A100 80GB and 1h36m for 100 steps; too costly, not reproduced, review DONE. Route-and-Generate (2610.30351) leaves the mean undefined at `n_f=0` without located source. IRAH (2610.30167) cannot omit LLM reflective mutation and meta-learning warmup while preserving its core. HERD (2610.31401) reports 25 stages and 10,723 seconds; the paper's `arr` branch linked by the official README was not obtained and main is not a substitute. The last three do not claim completed review or expensive execution and are not automatically implemented or retried. See JSON for dates, resources, code, and unknowns.

## Separate generation and acceptance

```bash
python scripts/build_oct23_source_audit.py /tmp/oct23-source-delta
python -m pytest tests/test_oct23_source_audit.py tests/test_gemma_priority_protocol.py
```

The source builder reads actual receipts, prior coverage, and the independent catalog to produce pending scope and append a discovery batch. It rejects an existing batch to preserve later acceptance. It does not go online, execute models, write runtime/metrics, or move watermarks. A separate curator finalization recorded frozen-source/GPU acceptance, not model capability from CPU multiseed checks.
