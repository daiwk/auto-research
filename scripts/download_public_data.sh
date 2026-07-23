#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_ROOT="${AUTO_RESEARCH_DATA_DIR:-${ROOT}/data}"
DATASET="${1:-all}"

download() {
  local url="$1"
  local target="$2"
  mkdir -p "$(dirname "${target}")"
  if [[ ! -s "${target}" ]]; then
    curl -L --fail --retry 3 "${url}" -o "${target}"
  fi
}

if [[ "${DATASET}" == "gsm8k" || "${DATASET}" == "all" ]]; then
  download \
    "https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/train.jsonl" \
    "${DATA_ROOT}/gsm8k/train.jsonl"
  download \
    "https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl" \
    "${DATA_ROOT}/gsm8k/test.jsonl"
fi

if [[ "${DATASET}" == "alpaca" || "${DATASET}" == "all" ]]; then
  download \
    "https://raw.githubusercontent.com/tatsu-lab/stanford_alpaca/main/alpaca_data.json" \
    "${DATA_ROOT}/alpaca/alpaca_data.json"
fi

if [[ "${DATASET}" != "gsm8k" && "${DATASET}" != "alpaca" && "${DATASET}" != "all" ]]; then
  echo "unknown dataset: ${DATASET}; supported: gsm8k, alpaca, all" >&2
  exit 2
fi
