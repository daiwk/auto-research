# October 18: Announcement-overlap backfill and low-cost component acceptance

<!-- source-sha256: f6d8370d5148ddb2b2d36545bcfe2e484bf218e29363577b458856a476c43165 -->

[简体中文](../../../research-audits/oct18-components/README.md)

This round covers **16 low-cost components/protocols and three high-cost references**, not 19 first publications on October 18 or all-source closure. The papers' v1 dates were October 14–15 and they appeared in the October 16 announcement. Merging the earlier selection did not complete the announcement's full-text review.

## Scope

| Track | Papers | Delivery boundary |
| --- | --- | --- |
| Foundation P0 | Memory Mosaics+ / Open-world AI, 2610.20782 | Associative memory, recent exclusion, and two-stage normalization |
| Agent P0 | Meta Diviner, 2610.21281 | Typed evidence, point-in-time snapshots, hypothesis ledger, and human review updates |
| Foundation P1 | MJev-Spatial, 2610.22276; vision AdaLoop, 2610.21323; SoftCache, 2610.22369; RR-VLM, 2610.22075 | Candidate scoring, vision loops, cache timesteps, shared-parameter loops, and distillation interfaces |
| Post-training P1 | TAG, 2610.21404; MRTPO, 2610.21439; token-level teacher selection, 2610.21234; IG-OPD, 2610.20664; RSHD, 2610.21018 | Real small operators, objectives, and constrained replay interfaces |
| Agent / RSI P1 | TORSI, 2610.20665; ARIA, 2610.20780; CODA, 2610.20845; MemScope, 2610.21170; JevAgentHarness, 2610.21412 | Clocks, continuation constraints, skill-perturbation audits, local patch rollback, and shadow calibration/fallback |
| High-cost references | EgoJEPA, 2610.20904; ORL, 2610.20687; Remote KV tiers, 2610.21500 | Original deliverable: Chinese method, figures, code status, and cost decisions only; no capability implementation or experimental metrics |

**Every full experiment was too costly and not run (review DONE).** The 16 components receive bounded mechanism checks. Seeds 42/43/44 do not turn constructed-input diagnostics into public benchmark capability comparisons. No new checkpoint or dataset downloads, multi-GPU runs, long rollouts, or commercial API experiments.

## Acceptance contract

- CUDA paths must run on one real A100 or A30, with no silent CPU fallback. Keep commits, hashes, per-seed outcomes, and sanitized receipts.
- CPU protocol paths must execute transitions, fault injection, independent references, and negative controls; static registry labels are insufficient.
- Evaluated policies cannot read gold. Isolate training-only verifier/note context. Validation governs acceptance, not test.
- All components are diagnostic and cannot become promotable evolve operators. High-cost decisions are terminal, without automatic retries.
- Diviner production outcomes are observational cohort associations, not randomized A/B. Memory Mosaics+ has Meta-affiliated authors working in a personal capacity; it is not a Meta production model.
- Keep paper figures, original Chinese detail, metadata, all three catalog views, metrics, and code synchronized; reference-only papers get no fabricated metrics or receipts.

## Sources and exceptions

Fully parsed six October 16 announcements (cs.AI/CL/IR/LG/CV/RO): 1,615 category records, 1,153 cross-category identities. Announcement recall is not per-paper full-text coverage. Relevant titles and abstracts were routed, and selected methods, configurations, and code verified.

Terminal requests to Google's official catalog timed out. Browser search exposed some details and Meta's homepage, not exhaustive catalogs. DeepMind's homepage showed no additions relative to the previous capture. Exceptions remain exceptions rather than “no new papers”; **the review watermark and prior coverage snapshot did not advance**.

Full-text review of RecSoup (2610.21220) and embedding privacy analysis (2610.21713) found no qualifying quantified real production-user A/B, so neither enters the industrial implementation queue. AbridgeKV (2610.20641) v1 is October 7, a historical backfill. SkillNEO development and final tasks overlap and do not support evolve generalization.

## Runs and evidence

Entry points: `scripts/run_oct18_foundation_components.py`, `scripts/run_oct18_post_components.py`, and `scripts/run_oct18_agent_components.py`. Individual pages hold commands and results. `scripts/curate_oct18_component_evidence.py` rechecks source, seeds, and statistics and rejects failures, partial results, omitted seeds, or invented aggregates.

Ten CUDA components ran on one NVIDIA A100 with seeds 42/43/44 and six CPU components/protocols ran the same seeds. Three references have no run outputs. Per-paper metrics keep constructed inputs, independent formulas, and negative controls; real receipts are in `docs/gpu-validations/`. These are not public task scores or full-paper evidence.

Cross-review corrected zero-probability behavior for FP16 hard teacher routing and SoftCache skipped-step statistics after time-grid redistribution. Both CUDA groups were rerun on frozen source. Input fingerprints bind recipe version, source hash, and seeds rather than inventing a dataset download.

[Frozen source proof](../../../research-audits/oct18-components/frozen-sources.json) retains public Git commits and necessary tree objects without weights, data, or source blobs. Acceptance checked real Git objects; persistent checks recompute commit-to-tree-to-file Git hashes and SHA-256 offline, including after shallow clones, squash merges, and old branch deletion. Proof identifies code, not GPU execution.
