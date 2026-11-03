# October 21, 2026: Recent announcement and Google/Meta priority increment

<!-- source-sha256: 14401c69b9cecb2b703cb5a65562834243021feedd8b273d2ff5b708186f02b0 -->

[简体中文](../../../research-audits/oct21-components/README.md)

After verifying PR #216 was merged, we deduplicated the new announcement and official catalog diffs rather than recounting historical implementations. The fixed scope is **eight low-cost components and four high-cost references**; all full experiments were excluded for cost and marked review DONE.

## Deliverables

| Type | Paper | Local coverage and exclusions |
| --- | --- | --- |
| P0 / Meta | [Baseline and Incremental](../../../recommendation-components/2610.27423-baseline-incremental/README-en.md) | CPU two-part value model, logit/raw gates, and hinge; no production ranker or live traffic |
| P0 / Meta collaboration | [RPL](../../../agent-research/2610.24854-rpl/README-en.md) | CPU typed retrieval programs, structural mutations, execution checks, and supervision spans; no arbitrary Python, GRPO/SFT, or neural retrieval |
| P0 / Google collaboration | [OO-Harness](../../../agent-research/2610.28380-oo-harness/README-en.md) | CPU inheritance, strict acceptance, frozen routing, and isolation; not LLM programming or official agent benchmarks |
| P1 / Recommendation | [SPAR](../../../recommendation-components/2610.27898-spar-prefix-balance/README-en.md) | CPU minimum feasible per-parent-prefix moves with a frozen residual codebook; no PATH/Qwen/DPO |
| P1 / Recommendation | [ECHO](../../../recommendation-components/2610.28569-echo-selector-loss/README-en.md) | A100 CE, boundary pairing, teacher detach, padding, and FP16 long-history checks; not full DS/TWIN or live storage |
| P1 / Post-training | [AP-OPD](../../../post-training/2610.28194-ap-opd/README-en.md) | A100 original block jump detection and signed supervised recovery, with real tiny-policy sampling and updates |
| P1 / Post-training | [OPTD](../../../post-training/2610.28048-optd/README-en.md) | A100 cross-layer prediction transfer for fixed candidates, two-sided gradients, and actual appendix scaling |
| P1 / JEPA | [LocaLeJEPA](../../../foundation-models/2610.28458-locale-jepa/README-en.md) | A100 uniform-sphere objective, local clustering and recentering, and small-cluster fallback; no ImageNet encoder training |
| P0 / Google | [Aptamer Lab Loop](../../../agent-research/2610.24806-aptamer-lab-loop/README-en.md) | Reference only: costly physical experiments and multiday feedback not reproduced; no simulation substitute |
| P0 / Meta collaboration / backfill | [ESC](../../../foundation-models/2610.23732-esc/README-en.md) | Reference only: 22B, 177K steps, 6.8e21 FLOPs not reproduced; first published October 14 |
| P1 / Post-training | [Visually Attributable OPD](../../../post-training/2610.26856-vag/README-en.md) | Reference only: full 8×H800 multimodal experiment not reproduced; stable key is distinct from Agent VAG |
| P1 / Agent systems | [Cache Engineering / AKV](../../../agent-research/2610.28577-cache-engineering/README-en.md) | Reference only: no 8×A800 or 120B/230B serving reproduction, and no tensor slicing presented as the system |

All executable paths are L1 synthetic mechanism/interface diagnostics, `diagnostic_only=true`, `promotion_eligible=false`, `evolve_integrated=false`. Multiple seeds do not establish capability or paper reproduction. No pretrained models were called; AP-OPD and OPTD still executed randomly initialized miniature policies.

## Execution and cross-review

Four CUDA components ran on one physical NVIDIA A100 with seeds 42/43/44 and no model, image, or private-data downloads. Four CPU components also reran from committed frozen source. Metrics retain source commit/SHA, recipe fingerprints, and per-seed records. [Offline frozen-source proof](../../../research-audits/oct21-components/frozen-sources.json) does not depend on the old branch or surviving pre-squash objects.

Independent review fixed ECHO FP16 long-history reduction overflow and empty-pair epsilon underflow; RPL silent deduplication of same-ID, different-content inputs; and OO task subclasses/dynamic fields leaking private values to actors or routers. Final A100 diagnostics added 70K FP16 and no-valid-pair cases. CPU regressions cover task/observation subclasses and identity collisions within lists and across retrievers. Earlier raw runs remain in a temporary output directory and do not count as post-fix evidence.

## Source coverage and counts

[Capture receipt](../../../research-audits/oct21-components/source-coverage.json): eight new arXiv category announcements, 29 Google pages, six scoped Meta pages, and nine DeepMind pages. The 1,619 category records contain duplicates and replacements, yielding 1,126 identities—not 1,126 new or fully read papers.

Google added two URLs, Meta one, and DeepMind none; catalog addition is not first publication. Meta RPL appeared there October 20 but v1 is October 17, as is Google's wet-lab loop. Twelve identities entered the library: 11 recent first publications and one historical backfill. Several were announced October 21, not necessarily published that day.

MOSS offered production monitoring and offline repairs but no qualifying online business A/B was verified. Google ASHF lacked a resolvable publication identity or method resources and was archived, not implemented from guesses. Coverage records other out-of-scope candidates and historical ResidencyRL separately, without claims of implementation or exhaustive discovery.

**The cross-domain review watermark stays 2026-10-15.** Fixed deliveries and official diffs do not close October 16–21. Cost decisions are terminal, not queued for implementation or retries, and do not block later watermark advances.

## Verification

```bash
PYTHONPATH=src python scripts/curate_oct21_component_evidence.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
PYTHONPATH=src python -m pytest tests/test_oct21_evidence_contracts.py
```

Initial curation requires real runner artifacts; prefilled pass labels do not generate metrics. Each paper records the source link, exact v1, first-author affiliation, code release, stable key, local path, original figure, and reproduction boundary.
