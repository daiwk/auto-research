"""Real CUDA ReplaySSM precision checks using a pinned author Triton source tree.

No installation scripts run, and neither FP32 emulation timings nor the
PyTorch reference are advertised as native bandwidth or serving speedups.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import torch

from auto_research.foundation_models.replayssm import mechanism_suite
from auto_research.oct12_public_sources import sha256_file

UPSTREAM_REVISION = "5d3ea597d479ef0c8e9e2eb2845a2adfdb9a8b44"


def author_precision_suite(upstream: Path, steps: int, seed: int) -> dict:
    if not torch.cuda.is_available():
        raise RuntimeError("author Triton execution requires a real NVIDIA CUDA device")
    revision = subprocess.check_output(["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    if revision != UPSTREAM_REVISION:
        raise ValueError("author source revision mismatch")
    changes = subprocess.check_output(
        ["git", "-C", str(upstream), "status", "--porcelain", "--untracked-files=all", "--", "emulation"],
        text=True).strip()
    if changes:
        raise ValueError("author emulation source has uncommitted changes")
    if "Apache License" not in (upstream / "LICENSE").read_text():
        raise ValueError("expected upstream Apache license")
    sys.path.insert(0, str(upstream))
    import emulation
    if not Path(emulation.__file__).resolve().is_relative_to(upstream.resolve()):
        raise ValueError("imported emulation package is not from the verified author source")
    from emulation import GDNReplay, Mamba2Replay

    torch.manual_seed(seed)
    metrics = {}
    modes = ("s32_rs", "tp8_hi32", "tp4_hi16_sr", "f4_sr_rs")
    for architecture in ("mamba2", "gdn"):
        state = torch.randn(2, 4, 128, 128, device="cuda") * 0.1
        cls = Mamba2Replay if architecture == "mamba2" else GDNReplay
        runners = {mode: cls(state, 2, mode) for mode in modes}
        histories = {mode: [] for mode in modes}
        for _ in range(steps):
            if architecture == "mamba2":
                args = (torch.randn(2, 4, 128, device="cuda", dtype=torch.bfloat16),
                        torch.full((2, 4), -3., device="cuda"),
                        torch.randn(2, 2, 128, device="cuda", dtype=torch.bfloat16),
                        torch.randn(2, 2, 128, device="cuda", dtype=torch.bfloat16),
                        -torch.ones(4, device="cuda"), torch.ones(4, device="cuda"),
                        torch.zeros(4, device="cuda"))
            else:
                args = (torch.randn(2, 1024, device="cuda", dtype=torch.bfloat16),
                        torch.full((2, 4), -3., device="cuda"),
                        torch.zeros(2, 4, device="cuda"), torch.zeros(4, device="cuda"),
                        torch.zeros(4, device="cuda"))
            for mode, runner in runners.items():
                histories[mode].append(runner.step(*args).clone())
        torch.cuda.synchronize()
        reference = torch.stack(histories["s32_rs"])
        for mode, runner in runners.items():
            output = torch.stack(histories[mode])
            metrics[f"{architecture}/{mode}/output_rmse"] = float((output - reference).square().mean().sqrt())
            metrics[f"{architecture}/{mode}/anchor_rmse"] = float((runner.state_hi - runners["s32_rs"].state_hi).square().mean().sqrt())
            if not torch.isfinite(output).all() or runner.steps.tolist() != [steps, steps]:
                raise RuntimeError("nonfinite output or wrong window progression")
        # Independent same-unrounded-state casts: low read must not inherit HP rounding.
        rounded, exact = cls(state, 2, "tp4_hi16_sr"), cls(state, 2, "tp4_hi32")
        rounded.step(*args)
        exact.step(*args)
        torch.testing.assert_close(rounded.state_lo, exact.state_lo, atol=0, rtol=0)
        if torch.equal(rounded.state_hi, exact.state_hi):
            raise RuntimeError("precision-independence check did not exercise rounding")
        metrics[f"{architecture}/independent_read_cast_passed"] = True
    return {"metrics": metrics, "upstream_revision": revision,
            "upstream_source_files_sha256": {
                name: sha256_file(upstream / "emulation" / name)
                for name in ("__init__.py", "api.py", "modes.py", "quant_tl.py", "mamba2_replay.py", "gdn_replay_unf_vf.py")},
            "accelerator": torch.cuda.get_device_name(), "steps": steps,
            "storage_format": "dequantized FP32", "native_bandwidth_speedup_claim": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=48)
    args = parser.parse_args()
    if args.steps < 17:
        parser.error("at least 17 steps required to exercise checkpoint refresh")
    report = {"paper": "2610.13778", "seed": args.seed, "diagnostic_only": True,
              "promotion_eligible": False, "fidelity": "core_mechanism",
              "evaluation_tier": "l1_mechanism", "dataset": "seeded random recurrent inputs",
              "dataset_revision": "replayssm-random-input-protocol-v1",
              "reference": mechanism_suite(args.seed, "cuda"),
              "author_triton": author_precision_suite(args.upstream, args.steps, args.seed),
              "limitations": ["no model checkpoint or held-out language benchmark",
                               "FP32-storage quantization emulation cannot measure low-bit HBM savings",
                               "native vLLM serving not executed by this entrypoint"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
