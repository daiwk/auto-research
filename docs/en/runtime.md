<!-- source-sha256: c58a64096eb7d46bc2dc1984e75c7e52a22ca821aceb8add54cc7b363c352844 -->

# Runtime environments: Mac, Linux GPU, and Linux CPU

[简体中文](../runtime.md) · [Installation and demos](setup.md)

Three execution paths share the same device selection:

- `auto-research reproduce` covers all PyTorch paper adapters.
- `auto-research evolve` covers RankMixer, HyFormer, and micro-LLM.
- `auto-research run` passes the same device environment variables to custom experiment processes.

The default, `--device auto`, checks for **CUDA, then Apple MPS, then CPU**. If an explicitly requested accelerator is unavailable, the command fails instead of silently falling back to CPU. This keeps experiment timing and reported metrics comparable. Paper reproductions record the device, PyTorch version, platform, and CPU thread count in `result.json`. Evolve records its device settings in its run configuration.

## One-command demo

Run from the repository root:

```bash
./demo.sh
```

The entry point chooses the Mac script on macOS. On Linux it chooses the GPU script if `nvidia-smi -L` works and the CPU script otherwise. To select a platform explicitly, call its script directly:

```bash
./demo-mac.sh
./demo-linux-cpu.sh
./demo-linux-gpu.sh
```

The default `DEMO_PROFILE=quick` trains and evaluates a smaller but real RankMixer experiment on MovieLens-100K. It still runs **three evolution rounds with two candidates per round**. Only the amount of public data and the number of training steps per candidate are reduced. In the report, `g0-t0` is the independent baseline; `g1-*`, `g2-*`, and `g3-*` are the three evolution rounds. You can combine these environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DEMO_PROFILE` | `quick` | `quick` for a fast check; `full` uses the original demo's MovieLens-1M, three generations, six candidates, and three seeds. |
| `DEMO_TRACK` | `recommendation` | `recommendation`, `llm`, `multimodal`, or `checkpoint-vlm`. |
| `DEMO_MULTIMODAL_DATASET` | `visual-shapes` | `visual-shapes` (offline), `fashion-mnist-qa` (lightweight public images), or `cifar10-qa` (natural color images). |
| `DEMO_DEVICE` | Mac: `auto`; GPU: `cuda:0` | Override the device, for example with `cuda:1` or with `cpu` on a Mac. |
| `DEMO_CPU_THREADS` | Auto-detected, at most 16 | PyTorch threads per worker on Linux CPU. |
| `DEMO_WORKERS` | Mac/GPU: 1; CPU: 2 | Number of candidates to run in parallel per generation. |
| `DEMO_VENV` | `.venv-demo-<platform>` | Custom virtual environment directory. |
| `DEMO_REINSTALL` | `0` | Set to `1` to reinstall dependencies. |
| `TORCH_INDEX_URL` | Official CPU index for CPU; PyPI for GPU | Override the PyTorch wheel index. |

Examples:

```bash
DEMO_PROFILE=full ./demo-linux-gpu.sh
DEMO_TRACK=llm ./demo-mac.sh
DEMO_TRACK=multimodal ./demo-mac.sh
DEMO_TRACK=multimodal DEMO_MULTIMODAL_DATASET=fashion-mnist-qa ./demo-mac.sh
DEMO_TRACK=multimodal DEMO_MULTIMODAL_DATASET=cifar10-qa ./demo-linux-gpu.sh
DEMO_TRACK=llm DEMO_PROFILE=full DEMO_DEVICE=cuda:1 ./demo-linux-gpu.sh
DEMO_TRACK=checkpoint-vlm \
DEMO_CHECKPOINT_ANNOTATIONS=data/scienceqa \
DEMO_CHECKPOINT_IMAGE_ROOT=data/scienceqa/images \
DEMO_CHECKPOINT_PATH=checkpoints/smolvlm2-256m \
DEMO_CHECKPOINT_REVISION=067788b187b95ebe7b2e040b3e4299e342e5b8fd \
./demo-linux-gpu.sh
```

Each platform has its own `.venv-demo-*` environment so CPU-only and CUDA builds of PyTorch do not overwrite one another. Before training, the scripts print the resolved device, PyTorch version, CUDA version, and hardware name. A failed preflight stops the experiment. Append evolve arguments to a demo command to override defaults for that run.

## Linux GPU

Use the [official PyTorch installation selector](https://pytorch.org/get-started/locally/) to install a build compatible with your server's driver and CUDA version before installing this project. Do not let the project installation replace the server's existing CUDA build of PyTorch.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip

# Install the matching CUDA build of PyTorch before installing the project.
python -m pip install torch --index-url <CUDA wheel index from the PyTorch selector>
python -m pip install -e .
auto-research-install-runtime --extras neural-recs,llm-evolution,plum

nvidia-smi
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

`auto-research-install-runtime` first runs pip in dry-run mode and reads the resolver report. If the plan would replace the existing PyTorch version, it exits before installing anything. This preserves the development machine's CUDA or vendor-customized build. To allow a replacement intentionally, pass `--allow-torch-change`. Compatible PyTorch 2.7 prerelease and custom builds are supported, but machine-specific build strings are not recorded in documentation or metrics.

Select the first visible GPU:

```bash
auto-research reproduce --paper rankmixer --device cuda:0 --seed 42

auto-research evolve \
  --model rankmixer \
  --dataset movielens-1m \
  --direction "Add LONGER and UniMixer" \
  --device cuda:0 \
  --workers 1 \
  --generations 3 --population 6 --steps 300
```

For LLM evolution, use the LLM model and dataset:

```bash
auto-research evolve \
  --model micro-llm \
  --dataset wikitext-2 \
  --direction "Study architectures, data mixtures, and post-training methods" \
  --device cuda:0 \
  --workers 1 \
  --generations 3 --population 6 --steps 300
```

On a multi-GPU development machine, use `CUDA_VISIBLE_DEVICES` to give separate research jobs separate GPUs. Start with `--workers 1` inside each job so multiple candidates do not fill the same card at once:

```bash
CUDA_VISIBLE_DEVICES=2 auto-research evolve ... --device cuda:0 --workers 1
```

## Retrospective GPU path audit

`scripts/audit_gpu_paths.py` runs paper adapters one at a time in isolated processes. It uses `AUTO_RESEARCH_DEVICE_AUDIT_LOG` to record the caller and resolved CUDA device for each actual `device_for` call. An adapter that finishes without calling the PyTorch device path receives the status `completed_without_device_call`, not a GPU validation pass. Failures and timeouts are recorded per adapter without stopping the rest of the audit:

```bash
PYTHONPATH=src python scripts/audit_gpu_paths.py \
  --dataset-dir data \
  --output runs/gpu-audit/a30.json \
  --timeout-seconds 60 \
  --only-explicit-device-packages \
  --include-concept-demos
```

The command finds problems with device selection, dependencies, and tensor execution. It is not a paper benchmark. Audit JSON, device evidence, checkpoints, and run artifacts stay on the development machine by default. Only reviewed summary findings and reproduction commands are committed. The [A30 GPU audit](gpu-validation.md) covers the full retrospective audit on 2026-08-11, the fixes, and the 62/62 results from actual CUDA execution.

Here, `cuda:0` means the first GPU visible inside the process. In the example with `CUDA_VISIBLE_DEVICES=2`, it corresponds to physical GPU 2.

## Linux CPU

On a CPU machine, install the official CPU wheel and set the thread count explicitly:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e .
auto-research-install-runtime --extras neural-recs,llm-evolution,plum

auto-research reproduce \
  --paper din \
  --device cpu \
  --cpu-threads 16 \
  --seed 42
```

Recommendation and LLM evolution use the same device and thread options:

```bash
auto-research evolve \
  --model micro-llm \
  --dataset wikitext-2 \
  --direction "Study architectures, data mixtures, and post-training methods" \
  --device cpu \
  --cpu-threads 16 \
  --workers 2 \
  --generations 3 --population 4 --steps 100
```

`--cpu-threads` sets the number of PyTorch intra-op threads **per worker**. Do not set it to the total number of machine cores multiplied by the number of workers. On a 32-core machine with two workers, start with 8–12 threads per worker.

## Mac

Keep the default automatic mode on Mac or select MPS explicitly:

```bash
auto-research reproduce --paper din --device mps
auto-research evolve ... --device mps --workers 1
```

Use `--device cpu` when you need to match Linux CPU execution on Mac.

## Environment variable compatibility

The CLI sets these environment variables and passes them to child processes. Existing scripts and custom adapters can reuse the shared runtime:

```bash
export AUTO_RESEARCH_DEVICE=cuda:0
export AUTO_RESEARCH_CPU_THREADS=16
```

Allowed device values are `auto`, `cpu`, `mps`, `cuda`, and `cuda:<index>`.

## Merge gate for new GPU implementations

If an adapter declares `requires_gpu_validation=True`, CI runs `python scripts/validate_gpu_evidence.py`. Run the implementation on a real NVIDIA A100 or A30 before committing a sanitized receipt. The receipt records only the accelerator model, public checkpoint revision, public dataset, command, seed, metrics, and commit. It must not contain hostnames, SSH aliases, usernames, driver strings, or build strings.

Beyond that mandatory gate, [the DCEO CUDA receipt](../gpu-validations/rankmixer-dceo-a30-20260828.json) records actual CUDA smoke tests for the DCEO Evolve operator's forward pass, backward pass, and optimizer step. It does not replace the formal fair CPU comparison on MovieLens.
