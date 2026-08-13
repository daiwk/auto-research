#!/usr/bin/env bash
set -euo pipefail

DATA_ROOT="${1:-data/coco}"
SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CAPTIONS_URL="https://cs.stanford.edu/people/karpathy/deepimagesent/caption_datasets.zip"
IMAGES_URL="http://images.cocodataset.org/zips/val2014.zip"
CAPTIONS_SHA256="4cfd70132527b80933105e5829dc9034eaab9573482e2e680abbab6130244817"
VAL2014_MD5="a3d79f5ed8d289b7a7554ce06a5782b3"

verify_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    echo "$1  $2" | sha256sum --check
  else
    echo "$1  $2" | shasum -a 256 --check
  fi
}

verify_md5() {
  if command -v md5sum >/dev/null 2>&1; then
    echo "$1  $2" | md5sum --check
  else
    [[ "$(md5 -q "$2")" == "$1" ]]
  fi
}

mkdir -p "$DATA_ROOT"

if [[ ! -f "$DATA_ROOT/dataset_coco.json" ]]; then
  curl --fail --location --continue-at - \
    --output "$DATA_ROOT/caption_datasets.zip" "$CAPTIONS_URL"
  verify_sha256 "$CAPTIONS_SHA256" "$DATA_ROOT/caption_datasets.zip"
  unzip -o -j "$DATA_ROOT/caption_datasets.zip" dataset_coco.json -d "$DATA_ROOT"
fi

if [[ ! -d "$DATA_ROOT/val2014" ]]; then
  curl --fail --location --continue-at - \
    --output "$DATA_ROOT/val2014.zip" "$IMAGES_URL"
  verify_md5 "$VAL2014_MD5" "$DATA_ROOT/val2014.zip"
  python3 "$SCRIPT_ROOT/extract_coco_karpathy_test.py" \
    --annotations "$DATA_ROOT/dataset_coco.json" \
    --archive "$DATA_ROOT/val2014.zip" --output "$DATA_ROOT"
  rm "$DATA_ROOT/val2014.zip"
fi

echo "COCO Karpathy retrieval data ready under $DATA_ROOT"
