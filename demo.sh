#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM="${DEMO_PLATFORM:-auto}"

if [[ "$PLATFORM" == "auto" ]]; then
  case "$(uname -s)" in
    Darwin)
      PLATFORM="mac"
      ;;
    Linux)
      if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1; then
        PLATFORM="linux-gpu"
      else
        PLATFORM="linux-cpu"
      fi
      ;;
    *)
      echo "Unsupported operating system: $(uname -s)" >&2
      exit 2
      ;;
  esac
fi

case "$PLATFORM" in
  mac)
    exec bash "$ROOT_DIR/demo-mac.sh" "$@"
    ;;
  linux-cpu)
    exec bash "$ROOT_DIR/demo-linux-cpu.sh" "$@"
    ;;
  linux-gpu)
    exec bash "$ROOT_DIR/demo-linux-gpu.sh" "$@"
    ;;
  *)
    echo "DEMO_PLATFORM must be auto, mac, linux-cpu or linux-gpu" >&2
    exit 2
    ;;
esac
