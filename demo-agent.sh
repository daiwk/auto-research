#!/usr/bin/env bash
set -euo pipefail

auto-research agent-eval \
  --method "${METHOD:-u-mem}" \
  --benchmark "${BENCHMARK:-evomem-mini}" \
  --episodes "${EPISODES:-120}" \
  --memory-size "${MEMORY_SIZE:-24}" \
  --seed "${SEED:-42}"
