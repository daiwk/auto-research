#!/usr/bin/env bash
set -euo pipefail

PYTHON="${PYTHON:-python3}"
DEVICE="${DEVICE:-auto}"
OUTPUT_ROOT="${OUTPUT_ROOT:-runs/multimodal-checkpoint-matrix}"
VLM_MODEL_ID="${VLM_MODEL_ID:-HuggingFaceTB/SmolVLM2-256M-Video-Instruct}"
VLM_REVISION="${VLM_REVISION:-main}"
VLM_BATCH_SIZE="${VLM_BATCH_SIZE:-8}"
RETRIEVAL_MODEL_ID="${RETRIEVAL_MODEL_ID:-openai/clip-vit-base-patch32}"
RETRIEVAL_REVISION="${RETRIEVAL_REVISION:-main}"

mkdir -p "$OUTPUT_ROOT"
ran=0

checkpoint_args=()
if [[ -n "${VLM_CHECKPOINT_PATH:-}" ]]; then
  checkpoint_args+=(--checkpoint-path "$VLM_CHECKPOINT_PATH" --offline)
fi

retrieval_args=()
if [[ -n "${RETRIEVAL_CHECKPOINT_PATH:-}" ]]; then
  retrieval_args+=(--checkpoint-path "$RETRIEVAL_CHECKPOINT_PATH" --offline)
fi

if [[ -n "${SCIENCEQA_ROOT:-}" ]]; then
  "$PYTHON" -m auto_research.cli multimodal-predict \
    --benchmark scienceqa --annotations "$SCIENCEQA_ROOT" \
    --image-root "$SCIENCEQA_ROOT/images" \
    --output "$OUTPUT_ROOT/scienceqa.jsonl" \
    --model-id "$VLM_MODEL_ID" --model-revision "$VLM_REVISION" \
    --batch-size "$VLM_BATCH_SIZE" \
    --device "$DEVICE" "${checkpoint_args[@]}"
  "$PYTHON" -m auto_research.cli multimodal-eval \
    --benchmark scienceqa --annotations "$SCIENCEQA_ROOT" \
    --predictions "$OUTPUT_ROOT/scienceqa.jsonl" --seeds 42 \
    --output-dir "$OUTPUT_ROOT/reports" --device "$DEVICE"
  ran=1
fi

if [[ -n "${POPE_ANNOTATIONS:-}" && -n "${POPE_IMAGE_ROOT:-}" ]]; then
  "$PYTHON" -m auto_research.cli multimodal-predict \
    --benchmark pope --annotations "$POPE_ANNOTATIONS" \
    --image-root "$POPE_IMAGE_ROOT" --output "$OUTPUT_ROOT/pope.jsonl" \
    --model-id "$VLM_MODEL_ID" --model-revision "$VLM_REVISION" \
    --batch-size "$VLM_BATCH_SIZE" \
    --device "$DEVICE" "${checkpoint_args[@]}"
  "$PYTHON" -m auto_research.cli multimodal-eval \
    --benchmark pope --annotations "$POPE_ANNOTATIONS" \
    --predictions "$OUTPUT_ROOT/pope.jsonl" --seeds 42 \
    --output-dir "$OUTPUT_ROOT/reports" --device "$DEVICE"
  ran=1
fi

run_retrieval() {
  local benchmark="$1"
  local annotations="$2"
  local image_root="$3"
  local name="$4"
  "$PYTHON" -m auto_research.cli multimodal-retrieval-predict \
    --benchmark "$benchmark" --annotations "$annotations" \
    --image-root "$image_root" --output "$OUTPUT_ROOT/$name.jsonl" \
    --model-id "$RETRIEVAL_MODEL_ID" --model-revision "$RETRIEVAL_REVISION" \
    --device "$DEVICE" "${retrieval_args[@]}"
  "$PYTHON" -m auto_research.cli multimodal-eval \
    --benchmark "$benchmark" --annotations "$annotations" \
    --predictions "$OUTPUT_ROOT/$name.jsonl" --seeds 42 \
    --output-dir "$OUTPUT_ROOT/reports" --device "$DEVICE"
  ran=1
}

if [[ -n "${COCO_ANNOTATIONS:-}" && -n "${COCO_IMAGE_ROOT:-}" ]]; then
  run_retrieval coco-retrieval "$COCO_ANNOTATIONS" "$COCO_IMAGE_ROOT" coco
fi

if [[ -n "${FLICKR30K_ANNOTATIONS:-}" && -n "${FLICKR30K_IMAGE_ROOT:-}" ]]; then
  run_retrieval flickr30k-retrieval \
    "$FLICKR30K_ANNOTATIONS" "$FLICKR30K_IMAGE_ROOT" flickr30k
fi

if [[ "$ran" -eq 0 ]]; then
  echo "Configure at least one public dataset root; see docs/multimodal-models/benchmark.md" >&2
  exit 2
fi

echo "Checkpoint matrix completed: $OUTPUT_ROOT"
