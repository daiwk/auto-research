# Public video and audio checkpoint evaluation

<!-- source-sha256: 84caa5b76fd3ae134af2eed77f485769dac2b5f52098497e911665a0730ead36 -->

[简体中文](../../multimodal-models/video-audio.md)

This guide covers roadmap items MM-001 and MM-002. Both paths load public checkpoints, read original public benchmark media, and separate per-example predictions from aggregates. Checkpoints, video, audio, and full predictions stay out of Git.

## MM-001: Video-MME-v2 × SmolVLM2

- Checkpoint: `HuggingFaceTB/SmolVLM2-256M-Video-Instruct`, pinned to `067788b187b95ebe7b2e040b3e4299e342e5b8fd`.
- Benchmark: `MME-Benchmarks/Video-MME-v2`, pinned to `6e4bebb03202e1ddbf3d37703e560e51c5aa2d64`.
- Inputs: official Parquet/JSONL and local MP4.
- Outputs: resumable JSONL per seed, accuracy, parse rate, sample standard deviation, and 95% confidence interval.

```bash
python scripts/prepare-media-benchmarks.py video-mme-v2 \
  --output data/video-mme-v2-smoke --videos 1

auto-research multimodal-video-eval \
  --annotations data/video-mme-v2-smoke/test-subset.jsonl \
  --video-root data/video-mme-v2-smoke/videos \
  --model-revision 067788b187b95ebe7b2e040b3e4299e342e5b8fd \
  --checkpoint-path checkpoints/smolvlm2-video \
  --seeds 42,43,44 --maximum-examples 4 --num-frames 32 \
  --output-dir runs/video-mme-v2-smoke --device cuda --offline
```

The preparation script downloads official shards from a pinned Hugging Face revision and extracts only needed MP4s. The first shard is about 2 GB, more reproducible than fetching possibly unavailable or login-gated YouTube clips. If disk or bandwidth is limited, use `--source youtube` explicitly. The script fails if a clip is unavailable rather than substituting another.

Deterministic decoding is the default for checkpoint regression; three seeds can produce identical predictions and zero variance. To study sampling, use `--sample --temperature 0.2`. Deterministic repeats are not training stability evidence. With `--maximum-examples`, the report labels the result as public-benchmark subset smoke, not a full leaderboard run.

The A30 regression covered all four questions for official video `001`, 32 uniform frames with original FPS and timestamps, and 3 deterministic seeds. Parse rate was `1.000`, but the 256M checkpoint missed all four questions (accuracy `0.000`). Media decode, real checkpoint execution, per-item resumption, and reporting work; the small model is not a Video-MME-v2 capability baseline. See the [archive](../../multimodal-models/metrics/video-mme-v2-smolvlm2-a30-4x3.json).

## MM-002: ESC-50/ESC-10 × CLAP

- Checkpoint: `laion/clap-htsat-unfused`, pinned to `8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a`.
- Benchmark: official ESC-50; the faster check uses the more permissively licensed ESC-10 subset.
- Inputs: official WAV and metadata CSV.
- Outputs: zero-shot top-1/top-5, per-example predictions, model/data fingerprints, and cached text embeddings.

```bash
python scripts/prepare-media-benchmarks.py esc10 \
  --output data/esc10 --examples-per-class 3

auto-research multimodal-audio-eval \
  --annotations data/esc10/esc10-subset.csv \
  --audio-root data/esc10/audio \
  --model-revision 8fa0f1c6d0433df6e97c127f64b2a1d6c0dcda8a \
  --checkpoint-path checkpoints/clap \
  --maximum-examples 30 --output-dir runs/esc10-clap \
  --device cuda --offline
```

The text embedding cache binds checkpoint commit, complete label set, and prompt template. Changing any rejects the old cache. Zero-shot ESC-10 subset scores are not full five-fold supervised ESC-50 results.

The A30 regression achieved zero-shot top-1 and top-5 of `1.000` on the fixed 30-item ESC-10 subset. A second run verified per-example resumption and cache hits. The small subset is easy; results verify public WAV loading, real checkpoint execution, cache, and metrics only. See the [archive](../../multimodal-models/metrics/esc10-clap-a30-30.json).

## Isolated development machines

Download pinned Hugging Face snapshots on a connected Mac and transfer the snapshot directory to Linux/GPU. Pass `--checkpoint-path --offline` explicitly to avoid drift from `main` or silent model changes without internet. Code records the public model ID and resolved revision, not machine-specific paths or package build strings.
