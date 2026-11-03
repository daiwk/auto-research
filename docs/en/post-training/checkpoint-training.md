# Post-training real checkpoints

<!-- source-sha256: 68fa9ca2602830016d0a74ad944f341ab21e7592d7007ef6838e04be5f0ab4d0 -->

[简体中文](../../post-training/checkpoint-training.md)

The `post-train` command keeps its lightweight, auditable mechanism experiments. `checkpoint-post-train` is a separate L2/L3 path that loads a pinned public pretrained causal LM and updates parameters on public data.

## Pinned model and data

| Resource | Revision | Use and license |
| --- | --- | --- |
| `HuggingFaceTB/SmolLM2-135M-Instruct` | `12fd25f77366fa6b3b4b768ec3050bf629380bac` | Apache-2.0; loads on Mac, Linux CPU, and a single GPU |
| OpenAI GSM8K | The repository's existing official JSONL download protocol | SFT and three-seed unrestricted generation |
| `HuggingFaceH4/ultrafeedback_binarized` | `292c16329d921287c4166934cac1a6ad1e13a6c5` | MIT; matched chosen/rejected comparison for DPO and ORPO |

## Three runnable paths

```bash
# GSM8K: actual generation, pinned checkpoint, 3 seeds
auto-research checkpoint-post-train \
  --objective sft --dataset gsm8k \
  --steps 20 --maximum-examples 64 --evaluation-examples 16 \
  --seeds 42,43,44 --device cuda

# UltraFeedback: DPO and ORPO with the same model, data, and budget
auto-research checkpoint-post-train \
  --objective dpo --dataset ultrafeedback \
  --steps 20 --batch-size 2 --gradient-accumulation 2 \
  --mixed-precision auto --device cuda

auto-research checkpoint-post-train \
  --objective orpo --dataset ultrafeedback \
  --steps 20 --batch-size 2 --gradient-accumulation 2 \
  --mixed-precision auto --device cuda
```

DPO uses a frozen reference. ORPO is reference-free and adds an odds preference term to chosen NLL. Both report held-out preference accuracy under the same tokenizer, length, batch, and step budgets. Defaults use pinned `train_prefs` and `test_prefs`, not a tail of the training split. For offline use, pass `--preference-data-path DIR` containing `train.jsonl` and `test.jsonl` exported from the pinned revision, with `prompt`, `chosen`, and `rejected` on each line.

## GPU execution and resumption

- A30 selects BF16 by default, with FP16 fallback if BF16 is unavailable. CPU and Mac use FP32.
- Real batching, gradient accumulation, clipping, and safetensors checkpoints are supported.
- `--save-every N` saves model, tokenizer, optimizer, and exact step.
- `--resume-from runs/.../checkpoint-N` restores weights and optimizer state rather than restarting.
- Checkpoints and data stay local; MRs retain metrics and reproduction commands.

`metrics.json` records model/data revisions, licenses, device, mixed precision, resume step, and three-seed means and standard deviations. Reduced steps are an engineering smoke test, not a stable gain.
