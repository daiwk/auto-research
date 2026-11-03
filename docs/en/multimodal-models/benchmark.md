# Unified multimodal model evaluation protocol

<!-- source-sha256: bdb4edda69a68a9c133e43cdbd3a9242a1bf16dee75ab1930243445780f5d4aa -->

[简体中文](../../multimodal-models/benchmark.md)

## L0: Local mechanism checks

`visual-shapes` asks about colors, shapes, and positions in real pixel images. Report:

- Accuracy on original images.
- Accuracy on shuffled images and `visual_dependency_delta`.
- Accuracy on blank images and `blank_image_delta`.
- Parameter count, device, training steps, seed, and connector.

Fitness is:

$$
F=\operatorname{accuracy}+0.25\max(0,\operatorname{accuracy}-\operatorname{accuracy}_{shuffle}).
$$

## L1: Small-scale public natural-image experiments

`fashion-mnist-qa` and `cifar10-qa` use the same multimodal interface to ask for image categories, covering lightweight clothing images and 32×32 color natural images, respectively. Both reserve 1,000 validation and 1,000 test examples. Initial downloads verify official MD5 hashes per file; cached runs can be completely offline. Report original, shuffled, and blank images. If the visual dependency delta is close to zero, do not attribute higher accuracy to the connector.

## L2: Standard public benchmarks

MR3 adds a standalone `multimodal-eval` command without reducing open-ended QA and image–text retrieval to fixed-category classification. The evaluator consumes public annotations and model predictions only. It can score this project's micro-VLM, any Hugging Face checkpoint, or a remote inference service without changing metrics.

MR6 adds `multimodal-retrieval-predict`, which loads real public CLIP/SigLIP-style checkpoints, batch-encodes images and captions, and computes exact positive ranks in both directions on GPU. Saving full rankings for COCO 5K would produce about 125 million IDs, so the prediction files store only the top 10 and the exact first-positive rank. Recall@1/5/10 and median rank are unchanged, and an independent scorer can audit the files.

| Benchmark | Annotation format | Required metrics |
|---|---|---|
| ScienceQA | Official directory with `problems.json` and `pid_splits.json` | Accuracy, image/text slices, parse rate |
| POPE | Official JSONL with `question_id` and `label` per row; converted `answer` also supported | Accuracy, precision, recall, F1, yes ratio, parse rate |
| COCO/Flickr30K retrieval | Karpathy JSON with `images[].sentences[]` | I2T/T2I Recall@1/5/10, median rank, mean recall |
| Video-MME-v2 | Official Parquet/JSONL and MP4 | Three-seed accuracy, sample standard deviation, 95% CI, parse rate |
| ESC-50 / ESC-10 | Official metadata CSV and WAV | CLAP zero-shot top-1/top-5, cache fingerprint |

See [public checkpoint evaluation for video and audio](video-audio.md) for real checkpoint commands, preparation scripts, and subset limits.

ScienceQA random-baseline pipeline check:

```bash
auto-research multimodal-eval \
  --benchmark scienceqa \
  --annotations data/scienceqa \
  --baseline random --seeds 42,43,44
```

Real predictions use the same protocol. `{seed}` expands to three separate prediction files:

```bash
auto-research multimodal-eval \
  --benchmark pope \
  --annotations data/pope/coco_pope_random.jsonl \
  --predictions 'runs/pope/predictions-seed{seed}.jsonl' \
  --seeds 42,43,44
```

### Generate predictions directly from a public checkpoint

`multimodal-predict` sets `do_sample=false`, appends one JSONL record per completed example, and skips existing IDs when rerun at the same path. An online machine resolves `main` to an immutable Hugging Face commit. An isolated machine can use a presynced snapshot at any path while recording the official model ID and commit explicitly:

```bash
auto-research multimodal-predict \
  --benchmark scienceqa \
  --annotations data/scienceqa \
  --image-root data/scienceqa/images \
  --output runs/scienceqa/predictions.jsonl \
  --model-id HuggingFaceTB/SmolVLM2-256M-Video-Instruct \
  --model-revision 067788b187b95ebe7b2e040b3e4299e342e5b8fd \
  --checkpoint-path checkpoints/smolvlm2-256m \
  --maximum-examples 500 --batch-size 8 --device cuda --offline

auto-research multimodal-eval \
  --benchmark scienceqa --annotations data/scienceqa \
  --predictions runs/scienceqa/predictions.jsonl \
  --maximum-examples 500 --seeds 42
```

Without `--checkpoint-path --offline`, the predictor downloads from `--model-id`. The `predictions.jsonl.metadata.json` sidecar records revision, prompting and decoding, device, and resume counts. Do not commit weights or complete predictions.

`--batch-size` defaults to 1 for compatibility with unknown checkpoints. For formal GPU evaluation, start at 8 and increase gradually. The predictor temporarily left-pads decoder-only VLM prompts to prevent short examples from continuing after PAD tokens. If a batch runs out of memory, reduce it and resume from saved IDs in the same output file.

Image–text retrieval has a separate prediction command:

```bash
auto-research multimodal-retrieval-predict \
  --benchmark coco-retrieval \
  --annotations data/coco/dataset_coco.json \
  --image-root data/coco/images \
  --output runs/coco/clip-predictions.jsonl \
  --model-id openai/clip-vit-base-patch32 \
  --checkpoint-path checkpoints/clip-vit-base-patch32 \
  --batch-size 64 --score-batch-size 256 --device cuda --offline

auto-research multimodal-eval \
  --benchmark coco-retrieval \
  --annotations data/coco/dataset_coco.json \
  --predictions runs/coco/clip-predictions.jsonl \
  --seeds 42 --device cuda
```

The same command supports `flickr30k-retrieval`. Prediction metadata records only the public model ID, immutable revision, generic platform and device, elapsed time, and peak GPU memory. It excludes hostnames, OS distribution versions, internal PyTorch builds, and local absolute paths.

The same script can batch four task types from configured datasets. It skips missing configurations and requires at least one task:

```bash
SCIENCEQA_ROOT=data/scienceqa \
POPE_ANNOTATIONS=data/pope/coco_pope_adversarial.json \
POPE_IMAGE_ROOT=data/coco/val2014 \
COCO_ANNOTATIONS=data/coco/dataset_coco.json \
COCO_IMAGE_ROOT=data/coco \
VLM_CHECKPOINT_PATH=checkpoints/smolvlm2-256m \
RETRIEVAL_CHECKPOINT_PATH=checkpoints/clip-vit-base-patch32 \
DEVICE=cuda ./scripts/run-multimodal-checkpoint-matrix.sh
```

By default the script does not truncate official splits. Generative predictions are resumable. Images, checkpoints, per-example predictions, and full rankings remain in `runs/`; Git stores only final aggregates and recipes.

### Multi-round evolve with a real checkpoint

`vlm-checkpoint` does not train or copy weights. It searches prompt templates, hints, image prescaling, and deterministic decoding budgets on the official ScienceQA **validation** set with the same loaded checkpoint. Only after all rounds does the controller run the initial baseline and the champion once each on **test**, avoiding test leakage:

```bash
auto-research evolve \
  --model vlm-checkpoint --dataset scienceqa \
  --direction "Compare prompt templates, hints, image resolution, and decoding budget" \
  --checkpoint-model-id HuggingFaceTB/SmolVLM2-256M-Video-Instruct \
  --checkpoint-revision 067788b187b95ebe7b2e040b3e4299e342e5b8fd \
  --checkpoint-path checkpoints/smolvlm2-256m \
  --checkpoint-annotations data/scienceqa \
  --checkpoint-image-root data/scienceqa/images \
  --maximum-examples 500 --generations 3 --population 4 \
  --workers 1 --seeds 42 --device cuda --offline
```

Local data must include `pid_splits.json`, `problems.json`, `images/val/`, and `images/test/`. Test images alone suffice for `multimodal-predict --split test`, not for leakage-free evolution. The single-GPU default `--workers 1` loads the checkpoint once. Each additional isolated worker loads its own model; set `--gpu-slots` and `--gpu-memory-per-trial-mb` accordingly.

Per-trial reports record immutable model revision, actual CUDA device, accuracy, image/text accuracy, parse rate, per-example latency, and peak GPU memory. Checkpoints, individual predictions, and `runs/` are not tracked in Git.

On 2026-08-11, an NVIDIA A30 engineering smoke used SmolVLM2-256M revision `067788b187b95ebe7b2e040b3e4299e342e5b8fd`. Two generations with two candidates plus an independent baseline produced five CUDA trials. Peak GPU memory was about 852.6–853.5 MiB; parse rate was 1.0. The temporary two-question split had 0.5 accuracy, and the initial recipe remained champion. The questions are real ScienceQA image/text examples, but the run checks checkpoint loading, validation-to-test flow, and reporting only. It is **not** an official benchmark or a basis for comparing recipe quality; formal comparisons require all official validation/test images. See [exact per-trial results](../../experiments/a30-vlm-checkpoint-smoke-20260811.json).

ScienceQA/POPE prediction rows:

```json
{"id": "question-id", "prediction": "yes / no / A / choice text"}
```

Retrieval predictions must include both directions. Manually supplied full rankings remain supported. Checkpoint prediction uses this compact format:

```json
{"image_id": "10", "ranked_text_ids": ["100", "101"], "relevant_text_rank": 1}
{"text_id": "100", "ranked_image_ids": ["10", "20"], "relevant_image_rank": 1}
```

Random baselines validate annotation parsing, metrics, and multi-seed aggregation, not VLM capability. Preserve the checkpoint, prompt, image preprocessing, and seed for real results. Obtain data from the original [ScienceQA](https://github.com/lupantech/ScienceQA), [POPE](https://github.com/RUCAIBox/POPE), [COCO](https://cocodataset.org/), and [Flickr30K](https://shannon.cs.illinois.edu/DenotationGraph/) releases. The repository does not include images, archives, or checkpoints.

## Formal multi-seed CIFAR-10 run

Fix architecture and training budget. Use validation for diagnostics and test for isolated reporting only:

```bash
auto-research multimodal-eval \
  --benchmark cifar10-qa --architecture micro_vlm_query \
  --steps 300 --maximum-examples 5000 --dimensions 192 \
  --batch-size 32 --seeds 42,43,44
```

The run directory includes machine-readable `metrics.json` and a Chinese `report.md`. Formal comparisons require three or more seeds and report the mean, sample standard deviation, and 95% CI radius.

The repository ran this recipe on official CIFAR-10 with three CPU seeds. Test accuracy was **19.43% ± 0.25 points**, versus 10.43% on shuffled and 10.00% on blank images. See [CIFAR-10 metrics](../../multimodal-models/metrics/cifar10-qa-seeds42-44.json).

## Executed ScienceQA and POPE checkpoint results

MR6 ran the same SmolVLM2-256M revision on all 4,241 official ScienceQA test examples: **54.92%** accuracy, **62.82% / 47.75%** image/text accuracy, **100%** coverage, and **99.95%** parse rate. This is a single deterministic checkpoint run, not a formal multi-seed comparison. See [ScienceQA metrics](../../multimodal-models/metrics/scienceqa-smolvlm2-256m-full.json).

On all 3,000 official POPE COCO adversarial examples, the same checkpoint achieved **75.17%** accuracy, **95.76%** precision, **52.67%** recall, **67.96%** F1, **27.50%** yes ratio, and **100%** parse rate. Accuracy is affected by a bias toward no; interpret it alongside recall, F1, and yes ratio. See [POPE metrics](../../multimodal-models/metrics/pope-adversarial-smolvlm2-256m-full.json).

### Historical fixed subset

On one A30, SmolVLM2-256M commit `067788b…` achieved deterministic zero-shot **56.80%** accuracy, **62.87% / 51.33%** image/text accuracy, and **99.80%** parse rate on the fixed first 500 official test examples. This verifies real checkpoint → resumable prediction → independent scoring, not a full test leaderboard or multi-seed stability. See [configuration and data fingerprint](../../multimodal-models/metrics/scienceqa-smolvlm2-256m-500.json).

## Evidence levels

| Level | Data | Supported conclusion |
|---|---|---|
| L1 | Fashion-MNIST / CIFAR-10 object QA | Small-scale experiments on real public images |
| L2 | ScienceQA, POPE, COCO/Flickr retrieval | Auditable public-benchmark results with real checkpoints; label fixed subsets explicitly |
| L3 | Full `lmms-eval` tasks and same-budget cross-checkpoint matrices | Standard VLM capability and efficiency comparisons |

## MR7: Cross-checkpoint matrix

MR7 turns the single-checkpoint run into a resumable matrix. Each cell fixes the benchmark, example cap, seed, and batch fallbacks. OOM falls back only to configured batch sizes, reusing saved predictions. Group generative VLMs and retrieval encoders by `family / benchmark` rather than one leaderboard.

A cached, immutable official `SmolVLM2-256M-Video-Instruct` revision completed a local real-pixel POPE smoke cell through model loading, generation, normalization, scoring, state files, and Markdown reports. This checks execution, not model quality. Cross-checkpoint comparisons need the same public split and budget; smoke examples do not substitute for them.

```bash
auto-research multimodal-matrix \
  --config configs/multimodal-checkpoint-matrix.example.json \
  --output-dir runs/multimodal-matrix \
  --device cuda
```

`matrix.json` contains revisions, performance, latency, and peak GPU memory. `report.md` contains comparable tables within a family. Configuration paths are local; data and checkpoints are not committed.

## MR8: Fair full-split matrix

MR8 runs the MR7 pipeline for real L3 comparisons. The generative group fixes prompt, hint, deterministic decoding, example order, and generation length for SmolVLM2 256M, 500M, and 2.2B. The retrieval group fixes COCO Karpathy test 5K, image preprocessing, and exact full-corpus bidirectional ranking for CLIP ViT-B/32 and SigLIP2 Base P16-224. All checkpoints use immutable 40-character revisions. Since objectives and output spaces differ, compare within each `family / benchmark`, not across groups.

Prepare public COCO annotations and images with checksum verification:

```bash
./scripts/prepare-coco-retrieval.sh data/coco
```

The script checks the Stanford Karpathy annotation SHA-256 and COCO val2014 ZIP MD5, extracts only the 5,000 test images, and deletes the temporary ZIP to avoid retaining all of val2014 for a 5K run.

See the [full matrix configuration](https://github.com/daiwk/auto-research/blob/main/configs/multimodal-checkpoint-matrix.mr8.json). Online runs need no `checkpoint_path`; offline machines set the snapshot path in a local configuration copy for each cell:

```bash
auto-research multimodal-matrix \
  --config configs/multimodal-checkpoint-matrix.mr8.json \
  --output-dir runs/multimodal-matrix-mr8 \
  --seed 42 --device cuda --offline
```

The executor rejects inconsistent splits, sample counts, prompts, hints, image sizes, or decoding budgets within a group. State files hash the complete config and seed with SHA-256, preventing accidental reuse after protocol changes. Git stores auditable aggregates, immutable revisions, and commands, not checkpoints, COCO images, or per-example predictions.

### Executed results

On 2026-08-13, all eight cells completed on one NVIDIA A30. These deterministic fixed-seed inference results compare immutable checkpoints; they are not multi-seed training confidence intervals. See [structured MR8 metrics](../../multimodal-models/metrics/checkpoint-matrix-mr8-full.json).

All 4,241 ScienceQA test examples:

| checkpoint | accuracy | image / text accuracy | sec/example | peak GPU memory |
|---|---:|---:|---:|---:|
| SmolVLM2-256M | 54.92% | 62.82% / 47.75% | 0.188 | 0.96 GiB |
| SmolVLM2-500M | 65.03% | 75.06% / 55.94% | 0.206 | 1.41 GiB |
| SmolVLM2-2.2B | **79.60%** | **88.25% / 71.76%** | 0.185 | 6.12 GiB |

500M improves by 10.12 points over 256M; 2.2B improves by 24.69 points. Generation can stop early, so lower measured seconds per example for 2.2B does not imply that its underlying model is faster than smaller models.

All 3,000 POPE COCO adversarial examples:

| checkpoint | accuracy | precision / recall / F1 | yes ratio | sec/example |
|---|---:|---:|---:|---:|
| SmolVLM2-256M | 75.13% | 95.75% / 52.60% / 67.90% | 27.47% | 0.316 |
| SmolVLM2-500M | 80.93% | 79.04% / **84.20%** / 81.54% | 53.27% | 0.325 |
| SmolVLM2-2.2B | **83.33%** | 85.31% / 80.53% / **82.85%** | 47.20% | 0.362 |

500M alleviates the 256M model's no bias. 2.2B improves accuracy and F1 again, but has lower recall than 500M. Scaling does not improve every behavior metric monotonically.

COCO Karpathy test 5K (5,000 images and 25,010 captions):

| checkpoint | I→T R@1/5/10 | T→I R@1/5/10 | mean recall | peak GPU memory |
|---|---:|---:|---:|---:|
| CLIP ViT-B/32 | 50.30 / 74.94 / 83.46 | 30.46 / 55.93 / 66.91 | 60.33% | 0.53 GiB |
| SigLIP2 Base P16-224 | **65.26 / 85.92 / 91.66** | **48.84 / 72.96 / 81.06** | **74.29%** | 1.23 GiB |

SigLIP2 mean recall exceeds CLIP by 13.95 points with about 2.31 times peak GPU memory. The run uncovered a silent compatibility issue: SigLIP/SigLIP2 pools at the final text position, so dynamic padding changes a caption representation according to the longest text in the batch. The erroneous run had only 14.16% mean recall. Prediction now uses checkpoint `max_length`, covered by a regression test; the invalid run is excluded from final metrics.

## Official lmms-eval interface

The optional upstream `lmms-eval 0.7.2` integration launches via argv rather than a shell string and stores the complete request. MR9 no longer treats process exit as completion: it must find and parse upstream `*_results.json` before writing `summary.json`. That summary records public model ID, immutable model/upstream revision, task version, valid example counts, scalar metrics, and fixed budget, omitting hostnames and local absolute paths.

Audit the command with a dry run:

```bash
pip install -e '.[lmms-eval]'
auto-research multimodal-lmms-eval \
  --model qwen2_5_vl \
  --model-args pretrained=Qwen/Qwen2.5-VL-3B-Instruct,device_map=auto \
  --public-model-id Qwen/Qwen2.5-VL-3B-Instruct \
  --model-revision <40-character-hugging-face-commit> \
  --upstream-revision cb45ac4d4a667ea5ef89c7a148bff69b3489b981 \
  --tasks mme,mmmu_val \
  --limit 8 \
  --output-dir runs/lmms-eval/qwen25vl \
  --dry-run
```

Removing `--dry-run` downloads tasks and runs inference. Upstream owns task templates and scoring; this repository provides auditable invocation, run directories, and unified matrix aggregation.

### MR9: Real L3 standard task

MR9 pins `lmms-eval 0.7.2` source commit `cb45ac4d4a667ea5ef89c7a148bff69b3489b981`. The PyPI wheel omits extensionless task templates, so formal reruns use a full source checkout. Its generic Hugging Face adapter also incorrectly loads SmolVLM as a base model without `generate()`. A minimal compatibility patch leaves task prompts, generation budget, and scorer unchanged:

```bash
git clone --branch v0.7.2 https://github.com/EvolvingLMMs-Lab/lmms-eval.git third_party/lmms-eval
python scripts/patch_lmms_eval_smolvlm.py third_party/lmms-eval
python -m pip install -e third_party/lmms-eval

auto-research multimodal-lmms-eval \
  --model huggingface \
  --model-args pretrained=checkpoints/smolvlm2-2.2b,device_map=auto \
  --public-model-id HuggingFaceTB/SmolVLM2-2.2B-Instruct \
  --model-revision 482adb537c021c86670beed01cd58990d01e72e4 \
  --upstream-revision cb45ac4d4a667ea5ef89c7a148bff69b3489b981 \
  --tasks scienceqa_img --batch-size 1 --seed 42 \
  --output-dir runs/lmms-eval/smolvlm2-2.2b-scienceqa-img --device cuda
```

Upstream `scienceqa_img` contains only 2,017 image questions. The repository's L2 `scienceqa` test has all 4,241 image/text examples, so these accuracies are not directly comparable. On restricted networks, pre-download the official `lmms-lab/ScienceQA` snapshot and point the task to identical local Parquet; this changes only the data location, not questions, prompts, or scoring.

On 2026-08-13, the complete 2,017-example task ran on one NVIDIA A30: **87.21% ± 0.74 points** upstream exact match (1,759 correct), 4,422 generated tokens in 462.90 seconds, averaging 9.55 tokens/s. This is single-checkpoint deterministic inference, not a formal multi-seed training comparison. See [structured MR9 evidence](../../multimodal-models/metrics/lmms-eval-mr9-scienceqa-img.json). Per-question JSONL, public Parquet, and checkpoints were not committed.

A gain observed only at L0 is not evidence of general vision–language capability.
