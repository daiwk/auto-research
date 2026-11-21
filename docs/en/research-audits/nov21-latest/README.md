<!-- source-sha256: 7538711bd15d70e89ad66e0fc51817dd8880ad729198faaff7872a3410aaaa69 -->
# November21 scan and overlapping selections

[简体中文](../../../research-audits/nov21-latest/README.md)

Seven selections: six from the previous bulletin pool (five first appeared on November19, and MV-JEPA on November18), plus Meta MemLife, a September30 historical backfill surfaced by official repository events. None was published today. Current bulletins remain dated November20; this metadata capture verified no November20–21 first release.

## Scope and evidence

The 883 overlapping metadata records and 1081 bulletin identities are recall pools. The bulletin identity delta is 0; none is an implementation-backlog count. This finite intake is not all-source exhaustion, and the review watermark stays at November15.

Google/Meta received priority. Meta's whole-page ranking paper explicitly reports offline referee estimates; A100 timing is batch-amortized, not online latency. No quantified production A/B was verified, so the recommendation gate is not silently waived. Google's new Duplex blog does not independently specify a new public paper algorithm. Unavailable directories remain source exceptions.

Of56 official-directory captures,54 are source exceptions. Two DeepMind responses were gzip-compressed; their original bytes and initial receipts were retained before offline reparsing. The Google directory comparison is incomplete, so unobserved baseline links are not labeled removed. Repository pushes are recall signals, never publication dates.

Seven low-cost L1 components ran on CPU with three seeds; MV-JEPA additionally ran on a real A100. Full training, generation campaigns and production-system experiments are high-cost, not reproduced, review DONE, with no automatic retry. Component evidence is not complete model/agent capability or Evolve promotion. ForeSpark's existing terminal high-cost review was not reopened merely because its repository was pushed.

## Complete list

| Domain | Paper | First publication | Local delivery |
| --- | --- | --- | --- |
| foundation-models | [FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models](../../../foundation-models/2611.26020-frontier-replay/README-en.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [MV-JEPA: Post-Training Video Encoders for Cross-View Understanding](../../../foundation-models/2611.25172-mv-jepa/README-en.md) | 2026-11-18 | l1_mechanism |
| agent-research | [Sage-Evolve-Preview: Adaptive Observation for Post-Training Self-Improvement](../../../agent-research/2611.26132-sage-evolve/README-en.md) | 2026-11-19 | l1_mechanism |
| agent-research | [MemFolder: Structure-Guided Memory Folding for Efficient Agent Memory Management](../../../agent-research/2611.26427-memfolder/README-en.md) | 2026-11-19 | l1_mechanism |
| post-training | [Decision-Focused Reinforcement Learning for LLM Post-Training](../../../post-training/2611.25597-dfrl/README-en.md) | 2026-11-19 | l1_mechanism |
| foundation-models | [Sequential Anytime Valid Tests for Efficient Inference-Time Alignment](../../../foundation-models/2611.26413-e-rwsc/README-en.md) | 2026-11-19 | l1_mechanism |
| agent-research | [MemLife: Curating and Reasoning over Long-Term Egocentric Video Memories](../../../agent-research/2609.40195-memlife/README-en.md) | 2026-09-30 | l1_mechanism |
