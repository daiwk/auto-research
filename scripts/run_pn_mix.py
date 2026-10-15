#!/usr/bin/env python3
"""Bounded CPU/CUDA PN-Mix reference-cache validation, without downloads."""

from __future__ import annotations

import argparse
from contextlib import nullcontext
import json
from pathlib import Path

from auto_research.reproductions.pn_mix.cache import PNMixConfig
from auto_research.reproductions.pn_mix.experiment import run_diagnostic
from auto_research.runtime import exclusive_file_lock


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--prefill-tokens", type=int, default=384)
    parser.add_argument("--decode-tokens", type=int, default=64)
    parser.add_argument("--group-size", type=int, default=128)
    parser.add_argument("--residual-size", type=int, default=128)
    parser.add_argument("--sink-tokens", type=int, default=32)
    parser.add_argument("--high-ratio", type=float, default=0.5)
    parser.add_argument("--value-bits", type=int, choices=(2, 4, 16), default=2)
    parser.add_argument("--pair-layout", choices=("adjacent", "split"), default="adjacent")
    parser.add_argument("--checkpoint", type=Path, help="existing offline Llama/SmolLM2 directory")
    parser.add_argument("--checkpoint-id", help="public Hugging Face namespace/model")
    parser.add_argument("--checkpoint-revision", help="immutable public 40-hex checkpoint revision")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    def ensure_new_output():
        if args.output and (args.output.exists() or args.output.is_symlink()):
            raise FileExistsError(f"refusing to overwrite existing PN-Mix output: {args.output}")

    ensure_new_output()  # Reject before allocating a model or touching a GPU.
    with exclusive_file_lock(args.output) if args.output else nullcontext():
        ensure_new_output()  # Re-check after obtaining the nonblocking writer lock.
        result = run_diagnostic(
            seed=args.seed,
            device=args.device,
            prefill_tokens=args.prefill_tokens,
            decode_tokens=args.decode_tokens,
            config=PNMixConfig(
                high_ratio=args.high_ratio,
                group_size=args.group_size,
                residual_size=args.residual_size,
                sink_tokens=args.sink_tokens,
                value_bits=args.value_bits,
                pair_layout=args.pair_layout,
            ),
            checkpoint=args.checkpoint,
            checkpoint_id=args.checkpoint_id,
            checkpoint_revision=args.checkpoint_revision,
        )
        serialized = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(serialized)
    print(serialized, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
