# LLM post-training: lineage and gaps

<!-- source-sha256: dc94268724a415462b625982cd12ee27bdf1b7022fa23280a64110a18dd65100 -->

[简体中文](../../post-training/lineage.md)

This audit distinguishes the main implemented lineages, P1 additions worth considering, and methods whose names alone would not constitute reproductions. Priorities reflect historical influence, mechanism differences, public code or data, and local verifiability. The latest scope review for this page was **2026-08-08**.

## Lineage coverage

| Lineage | Representative methods | Status | Repository coverage |
|---|---|---|---|
| Classic RLHF | PPO-RLHF, RLOO, ReMax | Implemented | Critic-based, leave-one-out, and greedy-baseline approaches |
| Pairwise preferences | DPO | Implemented | Reference-relative pairwise objective |
| Unpaired / single-stage preferences | KTO, ORPO | Implemented | Individual binary feedback; SFT plus odds ratio |
| Group-relative reasoning RL | GRPO, DAPO, GSPO | Implemented | Group advantage, asymmetric token clipping, sequence clipping |
| Training–rollout mismatch correction | TIS, IcePop, Online IcePop, KPop | Implemented | One-sided truncation, fixed two-sided mask, one update per on-policy batch, adaptive binary-KL mask |
| On-policy / context distillation | GKD, MiniLLM, OPSD, OPCD, Lightning OPD, Relay-OPD, VAD | Implemented | Student trajectories, reverse KL, privileged-context self-distillation, internalization of contextual capability, offline teacher cache, limited teacher takeover, target reconstruction via visual evidence attribution |
| Multi-objective RL, process rewards, and distribution preservation | GPRL, TCR, CoRT, ReCo | Implemented | Per-dimension rewards, checklist residuals, counterfactual token credit, response/variance reweighting |
| Free-generation preference optimization | IPO, SimPO | Implemented | Token-level sequence probability, reference-relative and reference-free approaches |
| Length and capability boundaries | LUSPO, CoBA-RL | Implemented | Length-unbiased sequence RL, dynamic curriculum boundaries, and teacher triggering |
| AI-feedback safety alignment | Constitutional AI | Implemented | Explicit principles, self-critique and revision, AI preference |
| Reward-ranked SFT | RRHF, RAFT | Implemented | Full-ranking constraints and top-response filtering of online samples |
| Sequence calibration and controllable SFT | SLiC-HF, SteerLM | Implemented | Preference margins; multi-attribute conditional SFT |
| Self-play alignment | SPIN | Implemented | Previous-policy negatives and iterative opponent refresh |
| AI feedback and process supervision | RLAIF, Let's Verify, Math-Shepherd | Implemented | Order-debiased AI labels, active step annotation, and automatic labels from Monte Carlo continuations |
| Self-rewarding and zero-data curricula | Self-Rewarding, Absolute Zero, SPIRAL | Implemented | Self-judged preferences, task proposer/verifier, self-play language games |
| Test-time / intrinsic RL | TTRL, INTUITOR | Implemented | Majority-consensus pseudo-labels; intrinsic self-certainty reward |
| Off-policy and sequence stability | LUFFY, CISPO, ConSPO | Implemented | Mixed support, token IS clipping, and length-normalized contrastive sequence objective |
| Asynchrony, MoE, and entropy stability | Stabilizing RL, Missing Old Logits, STARE | Implemented | Routing Replay, old-logit semantics and EWMA repair, and surprisal-quantile feedback toward target entropy |

## Static capability closeout

All 11 P0 methods identified in the second-level topic audit are implemented: RLAIF, Let's Verify Step by Step, Math-Shepherd, Self-Rewarding LM, LUFFY, TTRL, Absolute Zero, INTUITOR, CISPO, SPIRAL, and ConSPO. Each objective runs through the unified candidate-policy trainer and evolve genome. See the [all-domain gap audit](../full-domain-gap-review-20260808.md) for evidence, fixed-seed metrics, and deduplication.

The three P1 items from that audit are also closed: Stabilizing RL with LLMs, Missing Old Logits, and STARE.

The four previously tracked platform capabilities are complete:

- [PR #113](https://github.com/daiwk/auto-research/pull/113) moved L2 to a pinned SmolLM2 revision, connected UltraFeedback, and added batching, gradient accumulation, mixed precision, safe checkpointing, and optimizer resume.
- [PR #115](https://github.com/daiwk/auto-research/pull/115) added dual pass@k/teacher caching for CoBA-RL, a pinned Qwen2.5 teacher revision, actual call rates, and token cost.
- [PR #116](https://github.com/daiwk/auto-research/pull/116) made data, objective, teacher, rollout, accumulation, and precision inheritable composition axes for post-training evolve.
- [PR #117](https://github.com/daiwk/auto-research/pull/117) enrolled representative methods in a resumable three-seed evidence-promotion protocol.

No static P0 or P1 items remain. Scaling public rollouts or adding methods belongs to a new research batch and must be registered under the same-budget, multi-seed, checkpoint-free metric contract.

## Conclusion

The repository covers RLHF, AI-feedback safety alignment, direct and full-ranking preferences, reward selection, sequence calibration, multi-attribute conditional SFT, self-play, single-sample and single-stage preferences, group-relative reasoning RL, distillation, multi-objective and process rewards, free-generation preferences, and capability boundaries. Keep L1 candidate and L2 free-generation evaluation separate; the two accuracies do not belong in one comparison table.

This review closed the OPSD and OPCD gaps. OPSD uses the student itself as an on-policy teacher with privileged solution context. OPCD distills experience or system prompts from a context-conditioned teacher into a context-free student. Both now run in the unified post-training genome rather than only as standalone reproductions.
