#!/usr/bin/env bash
# One device, sequential bounded diagnostics; no model/data download.
set -euo pipefail
cd "$(dirname "$0")/.."
PUBLIC_DIR=${1:?Supply the directory containing the two declared public inputs}
CODE_COMMIT=${2:?Supply the exact exported code commit}
export PYTHONPATH=src OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p runs/oct16-p0p1
timeout 180 python scripts/run_oct16_recommendation_components.py \
  --csv "$PUBLIC_DIR/kuairand-prefix.csv" --device cuda --seeds 42,43,44 \
  --output runs/oct16-p0p1/recommendation.json
timeout 180 python scripts/run_oct16_foundation_components.py \
  --papers rope-relay,cots --device cuda --seeds 42,43,44 --code-commit "$CODE_COMMIT" \
  --output runs/oct16-p0p1/foundation.json
timeout 180 python scripts/run_oct16_post_components.py \
  --corpus-path "$PUBLIC_DIR/hamlet.txt" --corpus-id gutenberg:1524 \
  --corpus-revision sha256:31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784 \
  --corpus-sha256 31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784 \
  --device cuda --seeds 42,43,44 --output runs/oct16-p0p1/post-training.json
python scripts/record_oct16_executed_sources.py --commit "$CODE_COMMIT" \
  --output runs/oct16-p0p1/executed-source.json
