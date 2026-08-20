#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e '.[post-training-gpu]'

auto-research evolve \
  --model reasoning-checkpoint \
  --dataset gsm8k-generate \
  --direction "比较 1/2/4/8 次采样、self-consistency verifier 与动态早停" \
  --generations 2 --population 4 --maximum-examples 16 \
  --seeds 42,43,44 --workers 1 --gpu-slots 1 --device cuda

auto-research checkpoint-post-train \
  --objective sft --dataset gsm8k \
  --steps 4 --batch-size 2 --gradient-accumulation 2 \
  --maximum-examples 16 --evaluation-examples 4 \
  --save-every 2 --seeds 42,43,44 --device cuda

echo "Smoke 完成。正式实验请提高 steps/maximum-examples/evaluation-examples。"
