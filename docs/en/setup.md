# Installation, datasets, and demos

<!-- source-sha256: e54239447dddde2c750eb5f86cfb439fbd237fbbdd2db0154ecd4cc4bc18da08 -->

[简体中文](../readme_setup.md) · English · [English home](index.md)

You can browse the [paper catalog](papers/index.md) without installing anything. Use the steps below to run the CLI or an experiment on macOS or Linux with Python 3.11 or later.

## Install the CLI

`auto-research` is an entry point provided by this repository, not a separately distributed program. Install it in a virtual environment from the repository root:

```bash
git clone https://github.com/daiwk/auto-research.git
cd auto-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

auto-research --help
auto-research list
auto-research evolve --help
```

Editable installation (`-e`) uses the checked-out Python source directly. Activate the environment in each new shell or invoke `.venv/bin/auto-research` explicitly.

Install only the extras for your planned experiment:

```bash
# Neural recommenders, model evolution, and distillation experiments
auto-research-install-runtime --extras neural-recs

# Local decoder-only LLM evolution
auto-research-install-runtime --extras llm-evolution

# PLUM and PRECISE checkpoint-backed LLM stages
auto-research-install-runtime --extras plum

# Optional development and test dependencies
python -m pip install -e '.[dev]'
```

The runtime installer previews the dependency plan and refuses to change the installed PyTorch version unless explicitly allowed. See the [runtime guide](runtime.md) for CPU-only and driver-compatible CUDA builds.

## Choose the device and data

For training commands that accept `--device`, use `auto`, `cpu`, `mps`, `cuda`, or `cuda:<index>`. Auto-detection tries CUDA, then Apple MPS, then CPU; explicitly requesting an unavailable device is an error. On Linux CPU, `--cpu-threads` controls the PyTorch thread count.

```bash
# Linux CPU; install neural-recs first
auto-research reproduce --paper din --device cpu --cpu-threads 16 --seed 42

# Apple Metal Performance Shaders
auto-research reproduce --paper din --device mps --seed 42

# One CUDA device
auto-research reproduce --paper din --device cuda:0 --seed 42
auto-research evolve --model rankmixer --dataset movielens-1m \
  --direction "Add LONGER and UniMixer" --device cuda:0 --workers 1
```

Recommendation adapters can fetch MovieLens through their data loader. For experiments that use GSM8K or Stanford Alpaca, download the public sources to the Git-ignored `data/` directory:

```bash
scripts/download_public_data.sh all
auto-research reproduce --paper off-context-grpo --dataset-dir data --seed 42
auto-research reproduce --paper dynamic-rubric --dataset-dir data --seed 42
```

The script also accepts `gsm8k` or `alpaca` individually. Supported adapters download other public datasets, such as Tiny Shakespeare, MovieLens, Amazon Beauty, and KuaiRand-Pure, as needed and reuse their local caches. Public data is not a substitute for the paper's private production logs; local results must identify the actual data source.

## Run a demo

From the repository root:

```bash
# Auto-select macOS, Linux CPU, or Linux GPU
./demo.sh

# Or choose explicitly
./demo-mac.sh
./demo-linux-cpu.sh
./demo-linux-gpu.sh

# Small offline smoke tests; activate the installed CLI environment first
./demo-post-training.sh
./demo-agent.sh
```

The platform demo creates an isolated `.venv-demo-*` environment on first use and reuses it later. Its default is a small but real RankMixer evolution run on MovieLens-100K: three rounds, two candidates per round, and a separate baseline. It writes results to `runs/demo-<platform>-recommendation/`. For Linux GPU, use `TORCH_INDEX_URL` if you need a specific PyTorch wheel index.

```bash
# Full recommendation profile: MovieLens-1M, three rounds, six candidates, three seeds
DEMO_PROFILE=full ./demo.sh

# Small decoder-only language model: architecture, data, and post-training
DEMO_TRACK=llm ./demo.sh

# Multimodal evolution using the local synthetic demo
DEMO_TRACK=multimodal ./demo.sh

# Full micro-LLM profile on Linux GPU
DEMO_TRACK=llm DEMO_PROFILE=full ./demo-linux-gpu.sh
```

The post-training smoke test runs Lightning OPD on `arithmetic-smoke`; the agent smoke test defaults to U-Mem on `evomem-mini`. These quick paths do not require pretrained checkpoint downloads. They validate the specific local mechanism, not the paper's full capability. For alternatives see the [post-training](../post-training/README.md) and [agent](../agent-research/README.md) guides (Chinese).

## Run a controlled comparison

The evolution controller also supports post-training and agent search. For example:

```bash
auto-research evolve --model post-training --dataset arithmetic-smoke \
  --direction "Compare GRPO, DPO, and OPD with learning rate and group size" \
  --generations 3 --population 6 --maximum-examples 512 --seeds 42,43,44

auto-research evolve --model post-training --dataset arithmetic-generate \
  --direction "Compare IPO, SimPO, LUSPO, and a boundary curriculum" \
  --generations 3 --population 4 --workers 2 --seeds 42,43,44

auto-research evolve --model agent --dataset evomem-mini \
  --direction "Evolve memory, planner, tool policy, and critic together" \
  --generations 3 --population 8 --agent-episodes 240 --seeds 42,43,44

auto-research evolve --model agent --dataset swebench-local \
  --direction "Combine MetaGPT SOP, CRITIC, Agent Lightning, and code ACI" \
  --generations 3 --population 5 --workers 2 --agent-episodes 12
```

These runs select on validation, keep test separate, record parent/child genomes and failed trials, and produce an HTML report. The [evolution guide](model-evolution.md) documents the full argument set.

## Checkpoint and benchmark paths

These examples are not zero-download smoke tests. Check the paper's dependencies, public data revisions, and compute budget before running them:

```bash
# CIFAR-10 evaluation; first dataset download is approximately 163 MB
auto-research multimodal-eval --benchmark cifar10-qa \
  --architecture micro_vlm_query --steps 300 --seeds 42,43,44

# Real video/audio evaluation requires an official media subset and a checkpoint
auto-research multimodal-video-eval --help
auto-research multimodal-audio-eval --help

# Agent policy training and real code-executor comparison
auto-research agent-policy-train --steps 10 \
  --train-episodes 10 --validation-episodes 4 --test-episodes 4 \
  --seeds 42,43,44 --device cuda
auto-research agent-matrix --episodes 12 --seeds 42,43,44

# Official LeRobot SmolVLA flow-matching example, with data and checkpoints ready
auto-research embodied-post-train --dataset-root data/svla_so100_pickplace \
  --checkpoint-path checkpoints/smolvla_base \
  --vlm-checkpoint-path checkpoints/SmolVLM2-500M-Video-Instruct \
  --offline --steps 1 --device cuda
```

See the [video and audio evaluation guide (Chinese)](../multimodal-models/video-audio.md) for checkpoint revisions, fixed data subsets, and A30 evidence.

Do not commit downloaded data, checkpoints, or temporary `runs/` outputs. Commit the reviewed, reproducible command, revisions, stable JSON metrics, and evaluation limits. When a full run is beyond the single-GPU or local budget, mark it **not reproduced** instead of turning a reduced mechanism test into a claim about the full paper.
