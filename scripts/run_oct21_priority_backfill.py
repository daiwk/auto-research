"""Frozen affordable-component diagnostics, never a full-paper benchmark."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    "spec-driven-tests": "src/auto_research/agent_research/spec_driven_tests.py",
    "flint": "src/auto_research/foundation_models/flint.py",
    "mice": "src/auto_research/multimodal/mice.py",
    "system-one-rerank": "src/auto_research/multimodal/system_one_rerank.py",
}


def spec_diagnostic(seed):
    from auto_research.agent_research.spec_driven_tests import (
        Condition, Contract, Execution, FixedSourceView, GeneratedSuite, Specification,
        evaluate, generate, pass_detect_at_k,
    )
    rng, order, visible = random.Random(seed), [], []
    offset = rng.randrange(1, 10)
    fixed, buggy = f"return x + {offset}", f"return x - {offset}"

    def extract(view):
        order.append("specification")
        visible.append(asdict(view))
        return Specification((Contract("shift", "Add an offset", (),
            (Condition(f"output is input plus {offset}"),), ("check zero",)),))

    def synthesize(view, spec):
        order.append("test")
        visible.append(asdict(view))
        return GeneratedSuite("check zero")

    view = FixedSourceView(fixed)
    object.__setattr__(view, "buggy_source", buggy)
    spec, suite = generate(view, extract, synthesize)
    calls = []

    def executor(source, tests):
        # Deterministic fixture executor, not Python source execution or an LLM.
        calls.append((source, tests))
        return Execution(True, source == fixed, () if source == fixed else ("zero",))

    detected = evaluate(suite, fixed, buggy, executor)
    build_failure = evaluate(suite, fixed, buggy,
        lambda source, _: Execution(source == fixed, source == fixed))
    tamper = evaluate(GeneratedSuite("check zero", ("source.py",)), fixed, buggy,
        lambda *_: (_ for _ in ()).throw(AssertionError("protected source must not execute")))
    checks = {"phase_order": order == ["specification", "test"],
        "public_view_only": all(set(v) == {"source", "requirements", "existing_tests"} for v in visible),
        "same_suite_fixed_then_buggy": calls == [(fixed, suite.code), (buggy, suite.code)],
        "build_failure_not_detection": not build_failure.detects_bug and build_failure.passes_fixed,
        "protected_modification_discarded": not tamper.valid,
        "structured_spec_written": "### Preconditions" in spec.markdown(),
        "observed_k_aggregation": pass_detect_at_k(((build_failure, detected),), 2)["detect_at_k"] == 1}
    return {"seed": seed, "metrics": {"protocol_cases": 3, "dual_execution_calls": len(calls),
        "actual_llm_calls": 0, "buggy_fields_exposed": 0, "build_errors_counted_as_detections": 0}, "checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), required=True)
    parser.add_argument("--components", required=True)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--source-commit")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-id")
    parser.add_argument("--checkpoint-revision")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    components = args.components.split(",")
    seeds = [int(v) for v in args.seeds.split(",")]
    if (not components or len(components) != len(set(components)) or set(components) - MODULES.keys()
            or seeds != [42, 43, 44] or args.output.exists()):
        parser.error("unique known components, fixed seeds42-44 and new output required")
    if args.device == "cuda" and "spec-driven-tests" in components:
        parser.error("spec-driven-tests is explicitly CPU-only")
    commit = args.source_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("full source commit required")
    source_paths = ["scripts/run_oct21_priority_backfill.py", *[MODULES[k] for k in components]]
    accelerator = "CPU"
    if args.device == "cuda":
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError("real CUDA required; no CPU fallback")
        accelerator = torch.cuda.get_device_name(0)
        if not any(name in accelerator for name in ("A100", "A30")):
            raise RuntimeError("A100/A30 evidence required")
    model = processor = None
    checkpoint = {"public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False}
    if "system-one-rerank" in components:
        if not args.checkpoint or not args.checkpoint_id or not args.checkpoint_revision:
            parser.error("pinned public checkpoint path/id/revision required")
        manifest = json.loads((args.checkpoint / "provenance.json").read_text())
        if (manifest["public_id"] != args.checkpoint_id or manifest["revision"] != args.checkpoint_revision
                or not manifest.get("files") or "model.safetensors" not in manifest["files"]):
            raise ValueError("checkpoint provenance must bind public identity/revision and weights")
        for name, expected in manifest["files"].items():
            path = args.checkpoint / name
            if Path(name).is_absolute() or ".." in Path(name).parts or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError("public checkpoint file hash mismatch")
        from transformers import AutoModelForImageTextToText, AutoProcessor
        import torch
        processor = AutoProcessor.from_pretrained(args.checkpoint, local_files_only=True, trust_remote_code=False)
        model = AutoModelForImageTextToText.from_pretrained(args.checkpoint, local_files_only=True,
            trust_remote_code=False, torch_dtype=torch.float32).to(args.device).eval()
        files = {p.relative_to(args.checkpoint).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in args.checkpoint.rglob("*") if p.is_file() and p.suffix in {".json", ".safetensors", ".txt"}}
        if not any(p.endswith(".safetensors") for p in files):
            raise ValueError("checkpoint weights must be hashed")
        checkpoint = {"public_id": args.checkpoint_id, "revision": args.checkpoint_revision,
                      "pretrained": True, "files_sha256": files}
    rows = {}
    for key in components:
        if key == "spec-driven-tests":
            run = spec_diagnostic
        elif key == "flint":
            from auto_research.foundation_models.flint import diagnostic
            run = lambda seed: diagnostic(seed, args.device)
        elif key == "mice":
            from auto_research.multimodal.mice import diagnostic
            run = lambda seed: diagnostic(seed, args.device)
        else:
            from auto_research.multimodal.system_one_rerank import diagnostic
            run = lambda seed: diagnostic(seed, args.device, model, processor)
        values = [run(seed) for seed in seeds]
        if any(not r["checks"] or not all(v is True for v in r["checks"].values()) for r in values):
            raise AssertionError(f"defining component checks failed: {key}")
        rows[key] = {"per_seed": values}
    payload = {"schema_version": 2, "device": args.device, "seeds": seeds, "accelerator": accelerator,
        "code_commit": commit, "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths},
        "checkpoint": checkpoint, "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "formal_comparison": False, "full_experiment_status": "not_reproduced_high_cost", "components": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"components": components, "device": args.device, "seeds": seeds}))


if __name__ == "__main__":
    main()
