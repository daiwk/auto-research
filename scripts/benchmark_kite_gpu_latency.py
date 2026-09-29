"""CUDA-only KITE/SST microbenchmark for prefill and one-token decode.

Randomly initialized width-32 models and procedural tokens isolate the
architecture's kernel path. This is not the paper's 67B MoE/quality result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

import torch

from auto_research.foundation_models.kite_sst import SmallSST


def _latency_ms(call, *, repeats: int) -> float:
    for _ in range(3):
        call()
    torch.cuda.synchronize()
    elapsed = []
    for _ in range(repeats):
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
        call()
        end.record()
        end.synchronize()
        elapsed.append(start.elapsed_time(end))
    return median(elapsed)


def run(*, seeds: tuple[int, ...] = (42, 43, 44),
        context_lengths: tuple[int, ...] = (32, 128, 256),
        repeats: int = 20) -> dict:
    if not torch.cuda.is_available():
        raise RuntimeError("KITE CUDA benchmark requires a real NVIDIA device")
    if not seeds or len(set(seeds)) != len(seeds) or not context_lengths or repeats < 1:
        raise ValueError("nonempty unique seeds, contexts and positive repeats required")
    if min(context_lengths) < 2 or max(context_lengths) >= 512:
        raise ValueError("context lengths must be in [2, 511]")
    torch.backends.cuda.matmul.allow_tf32 = False
    rows = []
    for seed in seeds:
        torch.manual_seed(seed)
        sst = SmallSST(256, width=32, layers=2, max_positions=512).cuda().eval()
        sst.expand()
        dense = SmallSST(256, width=32, layers=4, max_positions=512).cuda().eval()
        for context in context_lengths:
            generator = torch.Generator().manual_seed(seed + context)
            prompt = torch.randint(0, 256, (1, context), generator=generator).cuda()
            next_token = torch.randint(0, 256, (1, 1), generator=generator).cuda()
            with torch.inference_mode():
                full_logits, _ = sst(prompt)
                last_logits, sst_past = sst(prompt, last_only=True)
                if not torch.allclose(full_logits[:, -1:], last_logits, atol=1e-5, rtol=1e-5):
                    raise AssertionError("SST prefill skip changed last-token logits")
                _, dense_past = dense(prompt)
                rows.append({
                    "seed": seed, "context_tokens": context,
                    "sst_prefill_full_ms": _latency_ms(lambda: sst(prompt), repeats=repeats),
                    "sst_prefill_last_only_ms": _latency_ms(
                        lambda: sst(prompt, last_only=True), repeats=repeats,
                    ),
                    "sst_decode_one_ms": _latency_ms(
                        lambda: sst(next_token, past=sst_past), repeats=repeats,
                    ),
                    "dense_prefill_ms": _latency_ms(lambda: dense(prompt), repeats=repeats),
                    "dense_decode_one_ms": _latency_ms(
                        lambda: dense(next_token, past=dense_past), repeats=repeats,
                    ),
                    "last_logit_max_abs_error": float((full_logits[:, -1:] - last_logits).abs().max()),
                })
    return {
        "schema_version": 1,
        "paper": "KITE arXiv:2609.27294",
        "diagnostic_only": True,
        "paper_result_reproduced": False,
        "device": torch.cuda.get_device_name(0),
        "model": "random width-32 dense 2+2 SST versus 4-layer dense control",
        "tokens": "procedural uniform byte IDs; no language quality claim",
        "repeats": repeats,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--context-lengths", default="32,128,256")
    parser.add_argument("--repeats", type=int, default=20)
    args = parser.parse_args()
    result = run(
        seeds=tuple(int(value) for value in args.seeds.split(",")),
        context_lengths=tuple(int(value) for value in args.context_lengths.split(",")),
        repeats=args.repeats,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
