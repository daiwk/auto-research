#!/usr/bin/env bash
# Run actual checkpoint mechanisms sequentially; no fake rewards or test tuning.
set -euo pipefail
: "${PYTHON:=python}"
: "${STUDENT_PATH:?provide local public student checkpoint}"
: "${TEACHER_PATH:?provide local public teacher checkpoint}"
: "${STUDENT_ID:?provide public model ID}"
: "${TEACHER_ID:?provide public model ID}"
: "${STUDENT_REVISION:?provide immutable revision}"
: "${TEACHER_REVISION:?provide immutable revision}"
: "${DATASET_REVISION:?provide immutable public dataset revision}"
: "${TRAIN_PATH:?provide public training JSONL}"
: "${VALIDATION_PATH:?provide disjoint public validation JSONL}"
export PYTHONPATH=src OMP_NUM_THREADS=1
for objective in dial-opd meta-opd semi-opd residual-advantage grpo-dropout co-ra; do
    steps=2
    tokens=128
    group=2
    if [[ "$objective" == grpo-dropout || "$objective" == co-ra ]]; then
        steps=10
        tokens=512
        group=4
    fi
    "$PYTHON" scripts/run_oct10_post_training.py --objective "$objective" \
      --student-path "$STUDENT_PATH" --student-id "$STUDENT_ID" --student-revision "$STUDENT_REVISION" \
      --teacher-path "$TEACHER_PATH" --teacher-id "$TEACHER_ID" --teacher-revision "$TEACHER_REVISION" \
      --train-path "$TRAIN_PATH" --validation-path "$VALIDATION_PATH" --dataset-revision "$DATASET_REVISION" \
      --output-dir "${OUTPUT_ROOT:-runs/oct10/current}/$objective-42" \
      --seed 42 --steps "$steps" --max-tokens "$tokens" --group "$group" --validation-examples 2
done
