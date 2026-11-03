# Multimodal foundation model research

<!-- source-sha256: c25670d79437dcfacea665fb6e32b4e2ce8f1d8bfd58fe330c12f0b3e6e7b20f -->

[简体中文](../../multimodal-models/README.md)

Recent scaled mechanism experiment: [DeltaS state-drift KV eviction](../experiments/sep28-three-mechanisms.md). The real hybrid video model is not integrated.

This domain covers vision–language foundations, training data, cross-modal connectors, and visual post-training. The first stage provides `micro-vlm` training from scratch on Mac, Linux CPU, and GPU. New paper operators enter Evolve only after actual image experiments and tests.

## Current capabilities

- [EmbeddingGemma 2](../../multimodal-models/embeddinggemma2/README-en.md): Budget-bounded retrieval with the official pinned image–text checkpoint, mask pooling, and MRL. No pretraining reproduction or Evolve claim.
- `visual-shapes`: Fully offline color, shape, and location QA images.
- `fashion-mnist-qa`: About 30MB of public clothing images for quick Mac/CPU runs.
- `cifar10-qa`: Official CIFAR-10 natural images with MD5-verified cache and fixed stratified validation/test.
- Six connectors: `micro_vlm_linear`, `micro_vlm_mlp`, `micro_vlm_query`, `micro_vlm_qformer`, `micro_vlm_gated`, and `micro_vlm_pixelshuffle`.
- Standalone CLIP, BLIP-2, LLaVA, SigLIP 2, and SmolVLM adapters, and composable `objective:siglip2`.
- Required original, shuffled, and blank image accuracy to check visual reliance.
- `multimodal-predict`: Actual public VLM checkpoints for ScienceQA/POPE, immutable revisions, offline snapshots, and per-item resumption.
- `multimodal-retrieval-predict`: Actual CLIP/SigLIP-like checkpoints and compact auditable bidirectional COCO/Flickr ranks.
- `vlm-checkpoint`: Search prompts, hints, preprocessing, and decoding budgets on ScienceQA validation with a frozen real model; isolate final test.
- Framework-independent L2 ScienceQA, POPE, and COCO/Flickr scorers with fixed subsets, three seeds, 95% intervals, and auditable predictions.
- `multimodal-lmms-eval`: Pinned upstream L3 tasks with normalized, path-free schema-v2 results, task versions, example counts, and efficiency metrics.
- `multimodal-video-eval`: Pinned SmolVLM2 on Video-MME-v2 with three seeds, item-level resumption, and intervals.
- `multimodal-audio-eval`: Real WAV zero-shot ESC-50/ESC-10 with pinned CLAP and validated text-embedding cache.
- `embodied-post-train`: Audits public LeRobot episodes and calls official `lerobot-train` for SmolVLA flow-matching post-training.
- Shared multi-round controller, isolated test, and dashboard with recommendation, micro-LLM, post-training, and agents.

```bash
python -m pip install -e '.[multimodal]'

auto-research evolve \
  --model micro-vlm \
  --dataset visual-shapes \
  --direction "Compare LLaVA, BLIP-2, SigLIP 2, and SmolVLM operators and check that predictions use the image" \
  --offline --generations 2 --population 3 --steps 60 \
  --llm-dimensions 96 --llm-batch-size 16 --seeds 42
```

See the [shared evaluation protocol](benchmark.md) for the fixed three-seed CIFAR-10 run and ScienceQA, POPE, and retrieval prediction formats. Predictors load checkpoints and save outputs. Scorers see only annotations and predictions. Random baselines check the pipeline only.

Public clothing images (first download about 30MB; later runs can use `--offline`):

```bash
auto-research evolve \
  --model micro-vlm --dataset fashion-mnist-qa \
  --direction "Compare connectors on real clothing images and test visual dependence" \
  --generations 2 --population 3 --steps 100 \
  --maximum-examples 2000 --seeds 42
```

Color natural images (initial download about 163MB):

```bash
auto-research evolve \
  --model micro-vlm --dataset cifar10-qa \
  --direction "Compare connectors on real images and test visual dependence" \
  --generations 2 --population 3 --steps 100 \
  --maximum-examples 2000 --seeds 42
```

## Browse

- [Method index](catalog.md)
- [By institution](catalog/by-organization.md) · [By topic](catalog/by-topic.md) · [By year](catalog/by-year.md)
- [Lineage and gaps](lineage.md)
- [Shared evaluation protocol](benchmark.md)
- [Video and audio checkpoint evaluation](video-audio.md)
- [Embodied multimodal post-training](embodied.md)

## Verified L1 results

Fashion-MNIST uses 2,000 train / 1,000 validation / 1,000 test, seed 42, and 150 steps per candidate. Query connector validation accuracy is **0.5010**, up 7.7 points from the linear connector's 0.4240. Isolated test is **0.4850**, while shuffled and blank controls reach 0.1070 and 0.1000. See [structured results](../../multimodal-models/metrics/fashion-mnist-qa-seed42.json).

CIFAR-10 uses 5,000 train / 1,000 validation / 1,000 test, a query connector, 300 steps, and seeds 42/43/44. Validation is **20.00% ± 1.28 points**; isolated test is **19.43% ± 0.25 points**; shuffled and blank images give 10.43% and 10.00%. This demonstrates image dependence at L1 object QA, not open-ended VQA. See [per-seed results, mean, sample SD, and 95% CI](../../multimodal-models/metrics/cifar10-qa-seeds42-44.json).

## Paper-level public image experiments

All use real Fashion-MNIST pixels, 2,000 training samples, and seed 42. Author results and local scaled experiments are separate.

| Mechanism | Fair baseline | Local test | Visual dependence or efficiency |
|---|---:|---:|---|
| CLIP symmetric contrastive | Uniform retrieval 10.0% | **72.0%** | Shuffled images 10.3% |
| LLaVA two-layer MLP projector | Linear connector 46.8% | **43.4%** | -3.4 points; negative result retained |
| BLIP-2 four-query Q-Former | Linear connector 46.8% | **41.5%** | -5.3 points; tokens 16 → 4 |
| SigLIP 2 sigmoid and masked view | Uniform retrieval 10.0% | **66.9%** | Shuffled images 10.8% |
| SmolVLM pixel shuffle | Linear connector 46.8% | **65.8%** | +19.0 points; tokens 16 → 4 |
| GAS MoT + NEP | Understanding-only 61.1% | **63.5%** | +2.4 points; 0% deployed parameter overhead |

See the [method index](catalog.md) for equations, paper results and figures, commands, and limits.

## Real public-checkpoint results

MR6 ran pinned `SmolVLM2-256M-Video-Instruct` on the **full 4,241-item ScienceQA test split**. Deterministic zero-shot accuracy was **54.92%**, image/text **62.82% / 47.75%**, coverage **100%**, and parse rate **99.95%**. This is one checkpoint on the full split, not a multiseed model comparison. See [aggregates](../../multimodal-models/metrics/scienceqa-smolvlm2-256m-full.json).

On all 3,000 official POPE COCO adversarial examples, the same checkpoint reached **75.17%** accuracy and **95.76% / 52.67% / 67.96%** precision/recall/F1, with **100%** parsing. The **27.50%** yes rate reveals a bias toward no, so accuracy alone is insufficient. See [POPE results](../../multimodal-models/metrics/pope-adversarial-smolvlm2-256m-full.json).

MR8 compared SmolVLM2 256M/500M/2.2B on full ScienceQA and POPE under a shared 16-token generation budget, and CLIP ViT-B/32 against SigLIP2 Base P16-224 on COCO Karpathy test 5K. ScienceQA accuracy: **54.92% / 65.03% / 79.60%**. POPE F1: **67.90% / 81.54% / 82.85%**. COCO mean recall for SigLIP2 and CLIP: **74.29% / 60.33%**. See the [protocol](benchmark.md) for fairness, efficiency, anomalies, and scope.

MR9 used upstream `lmms-eval 0.7.2` on all 2,017 `scienceqa_img` examples with SmolVLM2-2.2B, exact match **87.21% ± 0.74 points**. This is a different sample set from the local 4,241 mixed image/text scorer, so do not compare directly. See the [protocol](benchmark.md) for pinned upstream revision, compatibility patch, efficiency metrics, and commands.

An earlier fixed first-500 ScienceQA test subset with `SmolVLM2-256M-Video-Instruct`, commit `067788b187b95ebe7b2e040b3e4299e342e5b8fd`, reached **56.80%** deterministic zero-shot accuracy, **62.87% / 51.33%** image/text, and **99.80%** parsing. The model first loaded and passed single-image smoke on Apple Silicon Mac CPU, then evaluated on a single NVIDIA GPU. This is a fixed-subset checkpoint result kept to compare protocol continuity across MR4 and MR6. See [structured evidence](../../multimodal-models/metrics/scienceqa-smolvlm2-256m-500.json).

## Limits

`visual-shapes` is L0. Fashion-MNIST and CIFAR-10 are scaled public-image L1 tests. None demonstrates open-ended VQA. Real ScienceQA/POPE checkpoint generation and public scorers are L2; COCO/Flickr have real predictors and scorers. MR7 added a resumable matched-budget checkpoint matrix and optional `lmms-eval` backend. MR8 added pinned full ScienceQA, POPE, and COCO Karpathy test 5K configs with preflight budget checks. Checkpoints and public datasets are not committed. Full suites remain L3. Scaled paper-adapter L1 tests are not general VLM capability evidence.
