"""Real CUDA ReplaySSM precision checks using a pinned author Triton source tree.

No installation scripts run, and neither FP32 emulation timings nor the
PyTorch reference are advertised as native bandwidth or serving speedups.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import torch

from auto_research.foundation_models.replayssm import gdn_mechanism_suite, mechanism_suite
from auto_research.oct12_public_sources import sha256_file

UPSTREAM_REVISION = "5d3ea597d479ef0c8e9e2eb2845a2adfdb9a8b44"
GDN_FILE_SHA256 = "80311d6654584c633db01f76e3be5bc189fbdfab031c1bc0711757e1cd09eec3"
GDN_JIT_SOURCE_SHA256 = "7f60e87d974bfea4b5095980599043d8a7a615db4ba1b5fdbf7a0c1d0bfc6ab1"
GDN_BOOL_OP_RANGES = [{"line": 122, "column": 7, "end_line": 122,
                       "end_column": 51, "operator": "and", "operands": 3}]


def parenthesize_boolop_chains(source: str, expected_sha256: str) -> tuple[str, dict]:
    """Only parenthesize 3+ item and/or chains; preserve all other source bytes.

    The caller pins the sole permitted author kernel and source hash. This is
    a syntax adapter for Triton 3.3, not a substitute kernel or algorithm. The
    target operands are pure scalar flags; no custom Python truth operators
    occur in the pinned source. Evaluation order and short-circuiting of bool
    flags are tested separately.
    """
    if sha256(source.encode()).hexdigest() != expected_sha256 or not source.isascii():
        raise ValueError("JIT source identity mismatch; no compatibility transformation applied")
    tree = ast.parse(source)
    if (len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef)
            or tree.body[0].name != "_gdn_unf_vf_step_kernel"):
        raise ValueError("compatibility is restricted to the pinned GDN function")
    lines = source.splitlines(keepends=True)
    starts, offset = [], 0
    for line in lines:
        starts.append(offset)
        offset += len(line)

    insertions: dict[int, str] = {}
    ranges = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.BoolOp) or len(node.values) < 3:
            continue
        operator = "and" if isinstance(node.op, ast.And) else "or"
        start = starts[node.lineno - 1] + node.col_offset
        insertions[start] = insertions.get(start, "") + "(" * (len(node.values) - 2)
        for value in node.values[1:-1]:
            end = starts[value.end_lineno - 1] + value.end_col_offset
            insertions[end] = insertions.get(end, "") + ")"
        ranges.append({"line": node.lineno, "column": node.col_offset,
                       "end_line": node.end_lineno, "end_column": node.end_col_offset,
                       "operator": operator, "operands": len(node.values)})
    rewritten = source
    for position in sorted(insertions, reverse=True):
        rewritten = rewritten[:position] + insertions[position] + rewritten[position:]

    class FlattenAssociativeBoolOps(ast.NodeTransformer):
        def visit_BoolOp(self, node):
            self.generic_visit(node)
            values = []
            for child in node.values:
                values.extend(child.values if isinstance(child, ast.BoolOp) and type(child.op) is type(node.op)
                              else [child])
            node.values = values
            return node

    def canonical(text):
        return ast.dump(FlattenAssociativeBoolOps().visit(ast.parse(text)), include_attributes=False)

    if canonical(source) != canonical(rewritten):
        raise ValueError("compatibility changed non-Boolean AST structure")
    if any(isinstance(node, ast.BoolOp) and len(node.values) > 2 for node in ast.walk(ast.parse(rewritten))):
        raise ValueError("compatibility left a chained Boolean operation")
    return rewritten, {"original_jit_source_sha256": expected_sha256,
                       "compiled_jit_source_sha256": sha256(rewritten.encode()).hexdigest(),
                       "function": "_gdn_unf_vf_step_kernel",
                       "transformation": "left-associated parentheses only for 3+ operand and/or chains",
                       "source_ranges_relative_to_jit_function": ranges,
                       "associative_boolean_ast_equivalent": True,
                       "author_file_modified": False}


def prepare_gdn_jit_compatibility(kernel, source_file: Path) -> dict:
    """Guard actual author bytes and reset the JIT cache through its explicit API."""
    if (sha256_file(source_file) != GDN_FILE_SHA256
            or kernel.fn.__module__ != "emulation.gdn_replay_unf_vf"
            or kernel.fn.__name__ != "_gdn_unf_vf_step_kernel"):
        raise ValueError("only the exact pinned author GDN kernel can be adapted")
    rewritten, audit = parenthesize_boolop_chains(kernel.src, GDN_JIT_SOURCE_SHA256)
    if audit["source_ranges_relative_to_jit_function"] != GDN_BOOL_OP_RANGES:
        raise ValueError("pinned author source must contain exactly the known Boolean chain")
    if not callable(getattr(kernel, "_unsafe_update_src", None)):
        raise ValueError("Triton does not expose the required source-update/cache-reset API")
    kernel._unsafe_update_src(rewritten)
    if kernel.src != rewritten or sha256_file(source_file) != GDN_FILE_SHA256:
        raise ValueError("JIT compatibility or author-file immutability check failed")
    return {**audit, "original_author_file_sha256": GDN_FILE_SHA256,
            "native_serving_claim": False}


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
    from emulation.gdn_replay_unf_vf import _gdn_unf_vf_step_kernel
    if GDNReplay.step.__globals__["_gdn_unf_vf_step_kernel"] is not _gdn_unf_vf_step_kernel:
        raise ValueError("GDN API does not use the verified author kernel")
    compatibility = prepare_gdn_jit_compatibility(
        _gdn_unf_vf_step_kernel, upstream / "emulation" / "gdn_replay_unf_vf.py")

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
            "jit_source_compatibility": compatibility,
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
              "dataset_revision": "replayssm-random-input-protocol-v2-gdn-rollback",
              "reference": mechanism_suite(args.seed, "cuda"),
              "reference_gdn": gdn_mechanism_suite(args.seed, "cuda"),
              "author_triton": author_precision_suite(args.upstream, args.steps, args.seed),
              "limitations": ["no model checkpoint or held-out language benchmark",
                               "FP32-storage quantization emulation cannot measure low-bit HBM savings",
                               "native vLLM serving not executed by this entrypoint"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
