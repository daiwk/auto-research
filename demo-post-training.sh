#!/usr/bin/env bash
set -euo pipefail

DEVICE="${AUTO_RESEARCH_DEVICE:-auto}"

auto-research post-train \
  --algorithm lightning-opd \
  --dataset arithmetic-smoke \
  --steps "${STEPS:-100}" \
  --maximum-examples "${MAXIMUM_EXAMPLES:-512}" \
  --seed "${SEED:-42}" \
  --device "$DEVICE"
