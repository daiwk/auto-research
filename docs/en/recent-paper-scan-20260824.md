# 2026 historical paper scan and implementation through August 24

<!-- source-sha256: 0bfaf9c0b4cc9d419eedcd784393c94a32e1a223856abc694aa9d0895916a761 -->

[简体中文](../recent-paper-scan-20260824.md)

The requested frozen window was expanded to **January 1–August 24, 2026** across industrial search/ads/recommendation and LLM applications, foundation models, LLM post-training and agents. The multi-query matrix and cross-source configuration deduplicate canonical arXiv IDs. Industrial work requires quantified online A/B or explicit full-traffic deployment; Google/Meta affiliation checks receive first priority.

- [Historical scan and B00–B11 batches](../paper-audits/2026-historical-scan-plan.md): 404 full-text candidates and 70 fixed follow-up implementations.
- [Machine-readable candidates](../paper-audits/2026-historical-candidates.json): all 3,906 deduplicated new candidates with query hits, screen buckets and planning states.

## Reproducible scan

Run once per track:

```bash
PYTHONPATH=src python scripts/discover_papers.py \
  --track <recommendation|foundation-model|post-training|agent> \
  --date-from 2026-01-01 \
  --date-to 2026-08-24 \
  --page-size 50 \
  --maximum-results-per-query 200 \
  --cross-source-config configs/paper-discovery-sources.json \
  --output paper-candidates.json
```

| Track | Deduplicated candidates | New | Full-text review |
|---|---:|---:|---:|
| Industrial search/ads/recommendation and LLM applications | 716 | 627 | 237 |
| Foundation models | 1,319 | 1,303 | 42 |
| LLM post-training | 1,121 | 1,092 | 73 |
| Agents | 1,245 | 1,221 | 57 |

Broad queries retrieve many adjacent papers. Across four tracks there were 4,401 hits, 4,050 canonical papers, 3,906 not yet closed and 404 selected for full-text review. Hits do not establish eligibility.

## B00: First verified and implemented batch

| Track | Paper | Eligibility evidence | Local result |
|---|---|---|---|
| Industrial recommendation | [OneModel](../reproductions/2608.18606-onemodel/README.md) | Quantified A/B on three Xiaohongshu surfaces | Scene-aware MovieLens-1M proxy did not beat shared sequential baseline; negative result retained |
| Foundation | [RARE](../reproductions/2608.21236-rare/README-en.md) | Independently testable MoE steering/routing decoupling | Route agreement 82.37%→100%, with target steering retained |
| Post-training | [GCPO](../post-training/2608.11674-gcpo/README-en.md) | Rollout-RL subspace diagnostics and constraints, composable in Evolve | Arithmetic proxy final accuracy 63.28%, primary-direction overlap removed 99.56% |
| Agent | [AUSO](../agent-research/2608.21292-auso/README-en.md) | Action-level JSD for skill internalization/exploration/use; author code public | PlanBench mini-suite retains success and reduces context cost 9.09% |
| Industrial recommendation | [ClockRoPE](../reproductions/2607.26369-clockrope/README-en.md) | Quantified YouTube/Google DeepMind A/B in full text | MovieLens-100K NDCG@10 −2.30%; negative result retained |
| Industrial recommendation | [OneShot](../reproductions/2607.27475-oneshot-index/README-en.md) | Meta/Instagram full rollout with online metrics | MovieLens-100K NDCG@10 −7.70%; negative result retained |
| Industrial recommendation | [NEXT](../reproductions/2607.24789-next-vlm/README-en.md) | Meta multi-week A/B with about 100 million users | MovieLens-1M NDCG@10 +20.33% single-seed diagnostic |
| Agent | [AgentX](../agent-research/2606.26859-agentx/README-en.md) | Kuaishou three-week production self-iteration loop | PlanBench-mini: 12 completed loops and 108 knowledge reuses |

Detail pages record paper metadata, author code status, local adapter/path, original figures, equations and distinct paper vs fixed local results. OneModel illustrates why implementing a mechanism and reproducing production lift are separate claims.

## Google/Meta priority checks

Affiliation queries also found 2608.18531, 2608.15780 and 2608.15424. Full-text or topic review did not establish eligibility under the industrial online-evidence standard. Missing A/B in an abstract is not a reason for rejection.

## Fixed follow-up batches

B01–B06 cover industrial generative recommendation, multimodal methods, search, ads, mixed ranking, long-term value and SIDs. B07 covers foundations, long context, KV cache and A/B/n tooling. B08–B09 cover OPD, rubrics, external rollouts and multi-reward RL. B10–B11 cover agentic RL, long-horizon credit, memory, tool planning and self-evolution. Exact IDs are frozen in the [batch plan](../paper-audits/2026-historical-scan-plan.md).

The other 331 full-text candidates were not rejected by default: they stay in the full-text review backlog until evidence supports rejection, deferral or promotion to a fixed batch. At this recorded stage, incremental-only scanning was to resume after B01–B11 and that backlog closed.
