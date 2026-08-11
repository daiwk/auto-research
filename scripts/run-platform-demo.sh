#!/usr/bin/env bash
set -euo pipefail

PLATFORM="${1:?usage: run-platform-demo.sh mac|linux-cpu|linux-gpu}"
shift
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE="${DEMO_PROFILE:-quick}"
TRACK="${DEMO_TRACK:-recommendation}"
MULTIMODAL_DATASET="${DEMO_MULTIMODAL_DATASET:-visual-shapes}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${DEMO_VENV:-$ROOT_DIR/.venv-demo-$PLATFORM}"

case "$PLATFORM" in
  mac)
    DEVICE="${DEMO_DEVICE:-auto}"
    DEFAULT_WORKERS=1
    ;;
  linux-cpu)
    DEVICE="cpu"
    DEFAULT_WORKERS=2
    ;;
  linux-gpu)
    DEVICE="${DEMO_DEVICE:-cuda:0}"
    DEFAULT_WORKERS=1
    if ! command -v nvidia-smi >/dev/null 2>&1; then
      echo "nvidia-smi was not found; use demo-linux-cpu.sh on a CPU host." >&2
      exit 2
    fi
    ;;
  *)
    echo "platform must be mac, linux-cpu or linux-gpu" >&2
    exit 2
    ;;
esac

if [[ "$PROFILE" != "quick" && "$PROFILE" != "full" ]]; then
  echo "DEMO_PROFILE must be quick or full" >&2
  exit 2
fi
if [[ "$TRACK" != "recommendation" && "$TRACK" != "llm" && "$TRACK" != "multimodal" && "$TRACK" != "checkpoint-vlm" ]]; then
  echo "DEMO_TRACK must be recommendation, llm, multimodal or checkpoint-vlm" >&2
  exit 2
fi

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi
PYTHON="$VENV_DIR/bin/python"

if [[ ! -x "$VENV_DIR/bin/auto-research" || "${DEMO_REINSTALL:-0}" == "1" ]]; then
  "$PYTHON" -m pip install -U pip
  if [[ "$PLATFORM" == "linux-cpu" ]]; then
    "$PYTHON" -m pip install 'torch>=2.7,<3' \
      --index-url "${TORCH_INDEX_URL:-https://download.pytorch.org/whl/cpu}"
  elif [[ "$PLATFORM" == "linux-gpu" ]]; then
    if [[ -n "${TORCH_INDEX_URL:-}" ]]; then
      "$PYTHON" -m pip install 'torch>=2.7,<3' --index-url "$TORCH_INDEX_URL"
    else
      "$PYTHON" -m pip install 'torch>=2.7,<3'
    fi
  fi
  "$PYTHON" -m pip install -e "$ROOT_DIR[neural-recs,llm-evolution,multimodal]"
fi

CPU_THREADS=""
if [[ "$PLATFORM" == "linux-cpu" ]]; then
  DETECTED_THREADS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"
  if (( DETECTED_THREADS > 16 )); then
    DETECTED_THREADS=16
  fi
  CPU_THREADS="${DEMO_CPU_THREADS:-$DETECTED_THREADS}"
fi

export AUTO_RESEARCH_DEVICE="$DEVICE"
if [[ -n "$CPU_THREADS" ]]; then
  export AUTO_RESEARCH_CPU_THREADS="$CPU_THREADS"
fi

"$PYTHON" - <<'PY'
import json
import torch
from auto_research.runtime import runtime_summary

try:
    print("Resolved runtime:")
    print(json.dumps(runtime_summary(torch), ensure_ascii=False, indent=2))
except Exception as exc:
    raise SystemExit(
        f"Runtime check failed: {exc}\n"
        "For Linux GPU, install the PyTorch wheel matching the server CUDA driver. "
        "Set TORCH_INDEX_URL and rerun with DEMO_REINSTALL=1 if needed."
    )
PY

WORKERS="${DEMO_WORKERS:-$DEFAULT_WORKERS}"
COMMON_ARGS=(
  --device "$DEVICE"
  --workers "$WORKERS"
  --output-dir "$ROOT_DIR/runs/demo-$PLATFORM-$TRACK"
)
if [[ -n "$CPU_THREADS" ]]; then
  COMMON_ARGS+=(--cpu-threads "$CPU_THREADS")
fi

if [[ "$TRACK" == "recommendation" ]]; then
  COMMAND=(
    "$VENV_DIR/bin/auto-research" evolve
    --model rankmixer
    --direction "把 LONGER、UniMixer 及相关高效 Transformer 结构加入 RankMixer，比较长序列压缩、可学习 token mixing 及其组合"
  )
  if [[ "$PROFILE" == "quick" ]]; then
    COMMAND+=(
      --dataset movielens-100k
      --generations 3 --population 2 --steps 10 --papers 4 --seeds 42
      --maximum-users 220 --maximum-items 360 --evaluation-users 100
    )
  else
    COMMAND+=(
      --dataset movielens-1m
      --generations 3 --population 6 --steps 300 --papers 8 --seeds 42,43,44
    )
  fi
elif [[ "$TRACK" == "llm" ]]; then
  COMMAND=(
    "$VENV_DIR/bin/auto-research" evolve
    --model micro-llm
    --dataset wikitext-2
    --direction "调研高效 LLM 结构、训练数据配比和 SFT/NEFTune 后训练方法"
  )
  if [[ "$PROFILE" == "quick" ]]; then
    COMMAND+=(
      --generations 3 --population 4 --steps 40 --papers 6 --seeds 42
      --maximum-train-tokens 200000 --maximum-eval-tokens 50000
      --vocab-size 1024 --llm-dimensions 128 --llm-layers 2
      --llm-batch-size 4 --llm-sequence-length 128
    )
  else
    COMMAND+=(
      --generations 3 --population 6 --steps 300 --papers 8 --seeds 42,43,44
    )
  fi
elif [[ "$TRACK" == "multimodal" ]]; then
  COMMAND=(
    "$VENV_DIR/bin/auto-research" evolve
    --model micro-vlm
    --dataset "$MULTIMODAL_DATASET"
    --direction "比较线性、MLP 和 query connector，要求模型真实使用视觉输入"
  )
  if [[ "$MULTIMODAL_DATASET" == "visual-shapes" ]]; then
    COMMAND+=(--offline)
  elif [[ "$MULTIMODAL_DATASET" != "cifar10-qa" && "$MULTIMODAL_DATASET" != "fashion-mnist-qa" ]]; then
    echo "DEMO_MULTIMODAL_DATASET must be visual-shapes, fashion-mnist-qa or cifar10-qa" >&2
    exit 2
  fi
  if [[ "$PROFILE" == "quick" ]]; then
    COMMAND+=(
      --generations 2 --population 3 --steps 60 --papers 3 --seeds 42
      --llm-dimensions 96 --llm-layers 2 --llm-batch-size 16
      --maximum-examples 512
    )
  else
    COMMAND+=(
      --generations 3 --population 3 --steps 300 --papers 6 --seeds 42,43,44
      --llm-dimensions 192 --llm-layers 4 --llm-batch-size 32
    )
  fi
else
  : "${DEMO_CHECKPOINT_ANNOTATIONS:?set DEMO_CHECKPOINT_ANNOTATIONS to the ScienceQA directory}"
  : "${DEMO_CHECKPOINT_IMAGE_ROOT:?set DEMO_CHECKPOINT_IMAGE_ROOT to the ScienceQA image root}"
  COMMAND=(
    "$VENV_DIR/bin/auto-research" evolve
    --model vlm-checkpoint --dataset scienceqa
    --direction "比较提示模板、hint、图像分辨率和解码预算"
    --checkpoint-model-id "${DEMO_CHECKPOINT_MODEL_ID:-HuggingFaceTB/SmolVLM2-256M-Video-Instruct}"
    --checkpoint-revision "${DEMO_CHECKPOINT_REVISION:-main}"
    --checkpoint-annotations "$DEMO_CHECKPOINT_ANNOTATIONS"
    --checkpoint-image-root "$DEMO_CHECKPOINT_IMAGE_ROOT"
  )
  if [[ -n "${DEMO_CHECKPOINT_PATH:-}" ]]; then
    COMMAND+=(--checkpoint-path "$DEMO_CHECKPOINT_PATH" --offline)
  fi
  if [[ "$PROFILE" == "quick" ]]; then
    COMMAND+=(--generations 2 --population 2 --steps 1 --papers 3 --seeds 42 --maximum-examples 32)
  else
    COMMAND+=(--generations 3 --population 4 --steps 1 --papers 6 --seeds 42 --maximum-examples 500)
  fi
fi

echo "Starting $TRACK demo ($PROFILE) on $PLATFORM..."
if [[ "$TRACK" == "multimodal" ]]; then
  echo "Plan: $MULTIMODAL_DATASET image-question baseline plus connector evolution with shuffled/blank-image controls."
elif [[ "$TRACK" == "checkpoint-vlm" ]]; then
  echo "Plan: frozen public VLM checkpoint, validation-only inference-recipe evolution, then isolated test."
elif [[ "$PROFILE" == "quick" ]]; then
  echo "Plan: 3 evolution rounds x 2 candidates; the baseline is a separate experiment."
else
  echo "Plan: 3 evolution rounds x 6 candidates; the baseline is a separate experiment."
fi
echo "Artifacts will be written under runs/demo-$PLATFORM-$TRACK/"
exec "${COMMAND[@]}" "${COMMON_ARGS[@]}" "$@"
