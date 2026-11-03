# A100 Evidence for Promoting Higher-Fidelity Mechanisms

<!-- source-sha256: 441890822ac034ce39381dd0b399ef814f57e84fc85900c25c924cc6295ecb53 -->

[简体中文](../evidence-promotion.md)

This page records the real-checkpoint, three-seed experiments from 2026-08-28. The aim was to make candidates that run on public data and fixed revisions available to Evolve, not to guarantee positive gains. All experiments ran on one **NVIDIA A100**. The repository preserves commands, public revisions, and scalar results, not weights, caches, raw generations, or machine identifiers.

## Common protocol

- Seeds `42,43,44` independently reload and train from the same public base checkpoint.
- Use validation to select checkpoints or recipes; never select on the fixed test split.
- Report means, sample standard deviations, and 95% confidence intervals. Preserve negative results when improvement is not stable.
- Evolve can use artifacts only as proposal priors. The current evaluator must retrain and score.

## Results

| Direction | Public models and data | Main result | Interpretation |
| --- | --- | --- | --- |
| Multimodal feature distillation | SmolVLM2-256M + CLIP ViT-B/32; POPE/COCO, 320 train / 160 test | CKA `0.3494 → 0.3466`; neighbor overlap@5 `0.2642 → 0.2596` | No stable gain; disabled the degenerate label-count kNN |
| Agent Lightning policy bridge | SmolLM2-135M-Instruct; nine disjoint code-task families | Test joint success `0.5000 → 0.5000` | Bridge runs, but this is not SWE-bench generalization |
| DPO | SmolLM2-135M-Instruct; UltraFeedback, 64 train / 24 test | Preference accuracy `0.3333 → 0.3333`; margin `-49.0417 → -48.8472` | Accuracy unchanged; margin confidence interval does not support stable gains |
| ORPO | Same as above | Preference accuracy `0.3333 → 0.3333`; margin `-49.0417 → -48.3889` | Accuracy unchanged; margin increase is specific to this small budget |

Machine-readable artifacts:

- [MLLMCLIP, three seeds](../reproductions/2608.25575-mllmclip/metrics/pope-checkpoint-a100-seeds42-44.json)
- [Agent Lightning, three seeds](../experiments/a100-promotion/agent-lightning-seeds42-44.json)
- [DPO / UltraFeedback, three seeds](../experiments/a100-promotion/dpo-ultrafeedback-seeds42-44.json)
- [ORPO / UltraFeedback, three seeds](../experiments/a100-promotion/orpo-ultrafeedback-seeds42-44.json)

Sanitized GPU receipts: [MLLMCLIP](../gpu-validations/mllmclip-a100-20260828.json), [Agent Lightning](../gpu-validations/agent-lightning-policy-a100-20260828.json), [DPO](../gpu-validations/checkpoint-dpo-a100-20260828.json), and [ORPO](../gpu-validations/checkpoint-orpo-a100-20260828.json).

## Why keep these operators in Evolve?

A negative result at a fixed small budget rules out an automatic gain from copying the method as-is, not a gain under other data, learning rates, depths, or compositions. Artifacts move the operator earlier in the proposal queue only; Evolve reevaluates it under the current validation/test protocol. Old numbers are not new-task evidence.
