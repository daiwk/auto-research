#!/usr/bin/env python3
"""Train UxSID and three matched ablations with an actual frozen public encoder."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.reproductions.uxsid.experiment import ENCODER_ID, ENCODER_REVISION, render, run_uxsid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=Path("data"))
    parser.add_argument("--encoder-path", type=Path)
    parser.add_argument("--encoder-id", default=ENCODER_ID)
    parser.add_argument("--encoder-revision", default=ENCODER_REVISION)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--max-users", type=int)
    parser.add_argument("--max-history", type=int, default=256)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("previous evidence is immutable; choose a fresh output directory")
    torch_threads = 4
    import torch
    torch.set_num_threads(torch_threads)
    result = run_uxsid(args.dataset_dir, args.seed, device=args.device,
                       encoder_path=args.encoder_path, encoder_id=args.encoder_id,
                       encoder_revision=args.encoder_revision, epochs=args.epochs,
                       batch_size=args.batch_size, max_users=args.max_users, max_history=args.max_history)
    args.output.mkdir(parents=True)
    (args.output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (args.output / "report.md").write_text(render(result))
    print(json.dumps({"method": result["method"], "selected": result["validation_selected_variant"],
                      "cache": result["cache"], "diagnostic_only": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
