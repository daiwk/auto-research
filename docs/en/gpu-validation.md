<!-- source-sha256: 0b37b92e57b4b94bda12adfeb3d9b93db98bdc1c093ecf4802c4a47a0afb1337 -->

# Retrospective A30 GPU validation

[简体中文](../gpu-validation.md) · [Runtime environments](runtime.md)

This page records the engineering audit of the repository's GPU paths on 2026-08-11. It asks whether the code runs in a real CUDA environment. It does not replace paper benchmarks or turn a single-seed, reduced-step smoke test into a conclusion about model quality.

## Environment and criteria

| Item | Value |
|---|---|
| Host | User-provided single-GPU Linux development environment |
| GPU | One NVIDIA A30, 24 GB |
| CUDA | 12.8 |
| Data | Locally available public data including MovieLens, Amazon Beauty, and MiniOneRec |
| Pass criteria | The adapter finishes successfully and the evidence log records at least one actual `device_for` call that resolved to CUDA. |

The scanner inspects only an adapter's own implementation file. A flat adapter in a shared directory is no longer misclassified as a GPU adapter because an unrelated module in that directory uses PyTorch. Fixing that boundary reduced the 92 reported paths, which included 30 false positives, to **62** explicitly GPU-enabled paths.

## Results

- Valid GPU adapters: **62**. Final `gpu_pass`: **62/62**. Remaining failures or timeouts: **0**.
- The first pass had 41 successes, 15 failures, and 6 timeouts. For each failure, the necessary public data or local model cache was prepared and the code repaired. Timeout cases were rerun on the same data with a reduced-step smoke test or a longer hard timeout.
- The sum of the 62 successful runtimes was approximately 1,926.8 seconds. This excludes failed attempts during diagnosis and is not a throughput benchmark.
- Checkpoints, model caches, per-adapter raw JSONL, and training artifacts remain on the development machine, not in Git.

Adapters that passed:

<details>
<summary>Show all 62 adapters</summary>

`akt-rec`, `argus`, `asarl`, `bahe`, `barge`, `beque`, `ccformer`, `cobra`,
`core-relevance`, `cross-domain-kd`, `data-orchestra`, `degr`, `g2rec`, `genrank`,
`gr4ad`, `gryphon-v2`, `gzip-sparse-attention`, `kar`, `leadre`, `learn`,
`llm-ad-retrieval`, `lsvcr`, `lum`, `lwgr`, `m6rec`, `minimax-sparse-attention`,
`mixformer`, `mm-llm`, `mobius-rope`, `mosaic`, `msd`, `notellm`, `onerec`,
`onerec-v2`, `onetrans`, `open-web-ufm`, `oxygenrec-v2`, `pinequalizer`,
`pinterest-ads-llm`, `plum`, `precise`, `prompt-generation`, `rankmixer`,
`rec-distill`, `recap`, `recgpt-mobile`, `recgpt-v3`, `rocs`, `s-grec`,
`saviorrec`, `self-evolving-rec`, `seral`, `sessionrec`, `sigma`, `slimper`,
`sort-gen`, `tiger`, `tokenminds`, `uame`, `unir2`, `univa`, `windowed-mtp`.

</details>

## Issues found and fixed

| Path | Issue | Fix and A30 result |
|---|---|---|
| RecGPT-Mobile | Weight-only INT8 reconstructed weights as FP32, which did not match the BF16 activations used in matrix multiplication. | Match the reconstructed weights and bias to the activations' device and dtype. Passed in 124.1 seconds. |
| PLUM | The server's PyTorch build had no CPU LAPACK, so Transformers' covariance initialization for the expanded vocabulary failed. Default training was also too large for a smoke test. | Fall back to standard initialization only for explicit LAPACK errors. Keep all four branches in the smoke test but reduce SID/CPT/SFT steps. Passed in 370.2 seconds. |
| M6Rec / BAHE / LEARN | An older BERT-tiny configuration lacked `model_type`, so Transformers 5 Auto classes could not infer it. | Use the `BertModel` and `BertTokenizer` classes the implementations already depended on. All three passed. |
| BAHE | `BertLayer` returns different types in Transformers 4 and 5. The old `[0]` indexing dropped the batch dimension in v5. | Extract hidden states consistently from tuple or tensor results and reject old caches with the wrong dimensions. Passed in 5.2 seconds. |
| LWGR | The cuDNN GRU hidden state was not contiguous. There was no explicit conversion at the BF16 LLM and FP32 recommender boundary. | Make the hidden state contiguous and convert LLM input and output explicitly across dtypes. Passed in 9.6 seconds. |
| AKT-Rec / S-GRec / SIGMA | BF16 checkpoint hidden states went directly into an FP32 auxiliary head. | Convert explicitly at the checkpoint-to-task-head boundary. All three passed. |
| RECAP | The formal 80/60/45-step path exceeded the standard smoke timeout. | Use 1/1/1 steps for smoke only; keep formal parameters unchanged. Passed in 238.3 seconds. |
| GPU scanner | The shared `reproductions/` directory made 30 non-GPU adapters inherit unrelated hooks. | Scan only a flat adapter's own file. The final valid set had 62 entries. |

## Representative Evolve workflows

Beyond paper adapters, the audit used the same A30 to validate four broad categories of GPU workflow in the shared multi-round controller. The table includes representative runs and later checks:

| Workflow | Engineering smoke result |
|---|---|
| RankMixer / MovieLens | The baseline and two candidates completed. The LONGER candidate had validation NDCG@10 of `0.01145`. This was a truncated smoke run. |
| micro-LLM / WikiText-2 | GQA was the winning candidate, with validation perplexity `254.498` and instruction loss `5.521`. |
| micro-VLM / visual-shapes | Validation accuracy `0.325`. The run checked the image connector and CUDA training path. |
| post-training / arithmetic | The IPO free-generation path completed, with accuracy `0`. This only shows that training, generation, and scoring ran. |
| real VLM checkpoint / ScienceQA | All five SmolVLM2-256M trials completed. See the [shared multimodal evaluation protocol (Chinese)](../multimodal-models/benchmark.md). |
| real causal LM / reasoning budget | Both the baseline and the two-sample candidate finished on a pinned SmolLM2-135M revision. The candidate generated 152 tokens and scored accuracy `0`. The run checked budget, latency, cost constraints, and reporting. |
| real causal LM / GSM8K SFT | A one-step BF16 parameter update completed. After resuming from `checkpoint-1`, only step 2 ran, with `resumed_from_step=1`. |
| real causal LM / UltraFeedback | DPO and ORPO each completed one update using fixed public train/test preference subsets. Held-out accuracy was `0` for both. These were engineering smoke tests only. |
| micro-LLM / scaling-law | All four model, data, and step-budget points completed on CUDA. Loss went from `6.8678` to `6.5692`, with log-RMSE `0.002153`. This was an FM-002 engineering smoke test only. |

The [2026-08-20 follow-up record](../experiments/a30-reasoning-posttraining-smoke-20260820.json) provides structured results for the reasoning and post-training checks. The checkpoint and public data subsets are not committed to Git. The JSON retains only the versions, command settings, and metrics needed to reproduce the checks.

The [FM-002 Mac/A30 results](../experiments/fm002-scaling-law-mac-seed42.json) cover both execution paths.

## Reproducing the audit

On a single GPU, run shards sequentially so large-model adapters do not compete for memory:

```bash
for shard in 0 1 2; do
  PYTHONPATH=src python scripts/audit_gpu_paths.py \
    --dataset-dir data \
    --output "runs/gpu-audit/a30-shard-${shard}.json" \
    --timeout-seconds 600 \
    --only-explicit-device-packages \
    --include-concept-demos \
    --shards 3 --shard-index "${shard}"
done
```

For an LLM adapter, prepare the checkpoint named in its README first. On a development machine without external network access, set `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`. If you need to reduce steps, use only the adapter's documented `AUTO_RESEARCH_*` smoke-test environment variables. Do not carry these overrides into formal paper reproductions.
