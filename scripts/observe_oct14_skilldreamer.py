#!/usr/bin/env python3
"""Observe the unchanged fixed three-arm SkillDreamer diagnostic, not capability."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import signal
import sys
import time

ALGORITHM_COMMIT = "47f0e9cebc196e15c991d494dc4072367f53043b"
DATA_SHA256 = "8f33a9f7a44067e362458e4daf0eb1ad629a2aac2f44ffefe731e36b19dcb8c1"
MAX_CALLS = 1248
MAX_TOKENS = 319488
MAX_WALL_SECONDS = 14400  # proposed full-seed hard stop, requires main approval
RESOURCE_PATHS = {"model_dir": "/tmp/auto-research-qwen2.5-7b",
                  "encoder_dir": "/tmp/oct14-skill-validation7b-public/minilm",
                  "raw_data": "/tmp/oct14-skill-full7b-public/validation24.jsonl"}
SOURCE_SHA256 = {
    "scripts/run_skilldreamer.py": "9b14997fef987797db879554966dccb6c5699496c4ca8a979cf027b17fbd421e",
    "src/auto_research/reproductions/skilldreamer/algorithm.py": "c31169a7175fd7e005323a1288905427230a2c61fc906257868b147b1c6e2f76",
    "src/auto_research/reproductions/skilldreamer/experiment.py": "5d327072480d34b940d3aebbb4f6a638dffb81fb6c342c09a799ad8eeb8524c8",
    "src/auto_research/reproductions/skilldreamer/gallery.json": "9ff5e28de7d2eb7b3581ef01bbee66b0d201a543033bde6a2aa66da37f687970",
    "src/auto_research/reproductions/near/data.py": "795416bdffeb25880aeaf85b4bfd6480b8677b45cddabe37ba2e49d7bf544eb8",
    "src/auto_research/reproductions/near/experiment.py": "197e3fefad06f1f0e54533b608c5d717e57d0b6a919a105f88eee79447d94399",
    "src/auto_research/reproductions/state_opd/environment.py": "0e9564f9ec540985eb010b1e70f46938acc1bd946041b518d6579253762080e1",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def persist(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".writing")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def fixed_config(config: dict, seed: int) -> dict:
    if type(seed) is not int or seed not in (42, 43, 44):
        raise ValueError("fixed original seeds 42/43/44 required")
    run_config = config.get("run_config", {})
    keys = {"model_dir", "encoder_dir", "raw_data", "device", "max_queries", "max_new_tokens", "top_k", "action_budget"}
    expected = {"max_queries": 24, "max_new_tokens": 256, "top_k": 3, "action_budget": 8}
    if (set(run_config) != keys or run_config.get("device") != "cuda"
            or any(run_config.get(key) != value for key, value in RESOURCE_PATHS.items())
            or any(type(run_config.get(key)) is not int or run_config[key] != value for key, value in expected.items())
            or type(config.get("wall_limit_seconds")) is not int
            or not 0 < config["wall_limit_seconds"] <= MAX_WALL_SECONDS):
        raise ValueError("original complete 24-row three-arm budget and bounded whole-seed wall required")
    return run_config


def source_binding(config: dict) -> dict:
    if config.get("algorithm_commit") != ALGORITHM_COMMIT or config.get("source_sha256") != SOURCE_SHA256:
        raise ValueError("exact fixed 47f algorithm seven-file whitelist required")
    root = Path(config.get("algorithm_source_root", ".")).resolve()
    marker = root / ".source-commit"
    if root.name != "auto-research-oct14-47f0e9ce" or not marker.is_file() or marker.read_text().strip() != ALGORITHM_COMMIT:
        raise ValueError("fixed separately immutable 47f root marker required")
    for name in SOURCE_SHA256:
        if name.startswith("src/") and name.endswith(".py"):
            module = importlib.import_module(name.removeprefix("src/").removesuffix(".py").replace("/", "."))
            if Path(module.__file__).resolve() != root / name:
                raise ValueError("loaded library module differs from fixed algorithm source root")
    if any(sha(root / name) != digest for name, digest in SOURCE_SHA256.items()):
        raise ValueError("actual seven-file source bytes differ")
    commit = config.get("observer_source_commit", "")
    observer_root = Path(config.get("observer_source_root", ".")).resolve()
    actual = Path(__file__).resolve()
    marker = observer_root / ".source-commit"
    if (not re.fullmatch(r"[0-9a-f]{40}", commit)
            or observer_root.name != "auto-research-oct14-" + commit[:8]
            or actual != observer_root / "scripts/observe_oct14_skilldreamer.py"
            or not marker.is_file() or marker.read_text().strip() != commit
            or config.get("observer_source_sha256") != sha(actual)):
        raise ValueError("observer must bind its own independently frozen root/commit/SHA")
    return {"algorithm_commit": ALGORITHM_COMMIT, "executed_source_sha256": SOURCE_SHA256,
            "observer_source": {"commit": commit, "sha256": sha(actual), "immutable_root_bound": True}}


def audit(config: dict, seed: int, *, framework: bool = False) -> dict:
    run_config = fixed_config(config, seed)
    if framework and os.environ.get("CUDA_VISIBLE_DEVICES") != "":
        raise ValueError("CPU framework audit requires CUDA explicitly disabled")
    binding = source_binding(config)
    from auto_research.reproductions.near.experiment import verify_provenance
    model = Path(run_config["model_dir"])
    encoder = Path(run_config["encoder_dir"])
    model_files = ("config.json", "generation_config.json", "merges.txt", "model.safetensors.index.json",
                   "tokenizer.json", "tokenizer_config.json", "vocab.json", *[
                       f"model-{index:05d}-of-00004.safetensors" for index in range(1, 5)])
    encoder_files = ("model.safetensors", "config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "vocab.txt")
    resources = []
    for directory, public_id, revision, files in ((model, "Qwen/Qwen2.5-7B-Instruct", "bb46c15ee4bb56c5b63245ef50fd7637234d6f75", model_files),
            (encoder, "sentence-transformers/all-MiniLM-L6-v2", "1110a243fdf4706b3f48f1d95db1a4f5529b4d41", encoder_files)):
        provenance = json.loads((directory / "provenance.json").read_text())
        if set(provenance.get("files", {})) != set(files):
            raise ValueError("exact original public resource file whitelist required")
        resources.append(verify_provenance(directory, public_id, revision, files))
    raw = Path(run_config["raw_data"])
    dataset = json.loads((raw.parent / "provenance.json").read_text())
    if (sha(raw) != DATA_SHA256 or dataset.get("files", {}).get(raw.name) != DATA_SHA256
            or dataset.get("public_id") != "openai/grade-school-math"
            or dataset.get("revision") != "3101c7d5072418e28b9008a6636bde82a006892c"
            or dataset.get("source_split") != "train" or dataset.get("official_test_opened") is not False
            or len(raw.read_bytes().splitlines()) != 24):
        raise ValueError("byte-identical original 24 train-derived rows required; no content-based selection")
    report = {**binding, "seed": seed, "run_config": run_config, "run_config_sha256": canonical(run_config),
              "dataset": dataset, "checkpoint": resources[0], "encoder": resources[1],
              "limits": {"model_calls": MAX_CALLS, "output_tokens": MAX_TOKENS,
                         "wall_seconds": config["wall_limit_seconds"]},
              "audit_reads_question_or_gold_contents": False,
              "gold_visible_to_policy": False, "diagnostic_only": True, "promotion_eligible": False}
    if framework:
        from transformers import AutoConfig, AutoTokenizer
        from auto_research.reproductions.near.data import FrozenMiniLM
        import numpy as np
        model_config = AutoConfig.from_pretrained(str(model), local_files_only=True)
        tokenizer = AutoTokenizer.from_pretrained(str(model), local_files_only=True)
        values, _ = FrozenMiniLM(encoder, "cpu").encode(["Fixed resource CPU audit only."])
        if (model_config.model_type != "qwen2" or not tokenizer.apply_chat_template(
                [{"role": "user", "content": "CPU schema audit."}], tokenize=False, add_generation_prompt=True)
                or values.shape != (1, 384) or not np.isfinite(values).all()):
            raise ValueError("CPU config/tokenizer/encoder contract failed")
        report["cpu_framework_checks"] = {"qwen_config_tokenizer": True, "minilm_finite_shape": [1, 384], "cuda_executed": False}
    return report


@contextmanager
def hard_wall(seconds: int):
    if not hasattr(signal, "SIGALRM") or signal.getitimer(signal.ITIMER_REAL)[0] != 0:
        raise RuntimeError("exclusive Unix real-time deadline required")
    previous = signal.getsignal(signal.SIGALRM)

    def expired(signum, frame):
        raise TimeoutError("fixed full-seed hard wall exhausted")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def run(config: dict, seed: int, directory: Path, *, invocation: list[str], config_file_sha256: str) -> dict:
    fixed_config(config, seed)
    if not re.fullmatch(r"[0-9a-f]{64}", config_file_sha256):
        raise ValueError("actual invocation config bytes SHA required")
    if directory.exists():
        raise FileExistsError("immutable observer attempt already exists")
    directory.mkdir(parents=True)
    trace = directory / "trace.jsonl"
    trace.touch()
    record = {"status": "starting", "seed": seed, "diagnostic_only": True, "promotion_eligible": False,
              "command": invocation, "execution_config_sha256": config_file_sha256,
              "instrumentation": {"original_call_forwarded_unchanged": False,
                  "temporary_call_instrumentation": False, "restored_after_run": False},
              "calls_attempted": 0, "generation_responses": 0, "generated_tokens": 0}
    persist(directory / "observer.json", record)
    start = time.monotonic()
    torch, generator_type, original = None, None, None
    try:
        with hard_wall(config["wall_limit_seconds"]):
            record["audit"] = audit(config, seed)
            import torch
            from auto_research.reproductions.skilldreamer.experiment import LocalGenerator, run_skilldreamer
            if not torch.cuda.is_available() or not torch.cuda.get_device_name(0).startswith("NVIDIA A100"):
                raise RuntimeError("actual granted NVIDIA A100 required")
            torch.cuda.set_device(0)
            torch.cuda.reset_peak_memory_stats(0)
            record["accelerator"] = {"vendor": "NVIDIA", "model": torch.cuda.get_device_name(0)}
            generator_type, original = LocalGenerator, LocalGenerator.__call__

            def traced_generate(generator, *args, **kwargs):
                if record["calls_attempted"] >= MAX_CALLS:
                    raise RuntimeError("original full-seed call upper bound exhausted")
                record["calls_attempted"] += 1
                call = record["calls_attempted"]
                prompt = args[0] if args else kwargs.get("prompt")
                with trace.open("a") as stream:
                    stream.write(json.dumps({"event": "generation_attempt", "call": call, "prompt": prompt}, ensure_ascii=False) + "\n")
                before = generator.generated_tokens
                try:
                    record["instrumentation"]["original_call_forwarded_unchanged"] = True
                    response = original(generator, *args, **kwargs)  # no sampling, arguments or response rewrite
                except Exception as exc:
                    with trace.open("a") as stream:
                        stream.write(json.dumps({"event": "generation_error", "call": call,
                                                 "type": type(exc).__name__, "message": str(exc)}) + "\n")
                    raise
                generated = generator.generated_tokens - before
                record["generation_responses"] += 1
                record["generated_tokens"] += generated
                with trace.open("a") as stream:
                    stream.write(json.dumps({"event": "generation_response", "call": call,
                                             "response": response, "generated_tokens": generated}, ensure_ascii=False) + "\n")
                persist(directory / "observer.json", record)
                if generated > 256 or record["generated_tokens"] > MAX_TOKENS:
                    raise RuntimeError("original output-token upper bound exceeded")
                return response

            generator_type.__call__ = traced_generate
            record["instrumentation"]["temporary_call_instrumentation"] = True
            record["status"] = "running"
            result = run_skilldreamer(config["run_config"], seed)  # original three-arm evaluator, gold outside policy
            torch.cuda.synchronize()
            record["peak_gpu_memory_allocated_bytes"] = torch.cuda.max_memory_allocated(0)
            record["peak_gpu_memory_reserved_bytes"] = torch.cuda.max_memory_reserved(0)
            record["wall_seconds"] = time.monotonic() - start
            if (record["generation_responses"] != sum(row["model_calls"] for row in result["variants"].values())
                    or record["generated_tokens"] != sum(row["generated_tokens"] for row in result["variants"].values())):
                raise RuntimeError("observer counters differ from original actual summaries")
            if (not all(type(record[key]) is int and record[key] > 0 for key in
                        ("peak_gpu_memory_allocated_bytes", "peak_gpu_memory_reserved_bytes"))
                    or record["peak_gpu_memory_reserved_bytes"] < record["peak_gpu_memory_allocated_bytes"]):
                raise RuntimeError("actual positive allocator allocated/reserved peaks required")
            persist(directory / f"seed{seed}.json", result)
            record.update(status="completed_original_three_arm_diagnostic", raw_sha256=sha(directory / f"seed{seed}.json"),
                          trace_sha256=sha(trace), exit_code=0)
            persist(directory / "observer.json", record)
            return record
    except Exception as exc:
        record.update(status="timed_out" if isinstance(exc, TimeoutError) else "failed",
                      failure={"type": type(exc).__name__, "message": str(exc)},
                      wall_seconds=time.monotonic() - start, trace_sha256=sha(trace), exit_code=1)
        # No synchronization on failure: external wall guard must also be able
        # to stop a blocking CUDA call. Retain partial actual trace/counters.
        if torch is not None and "accelerator" in record:
            try:
                record["peak_gpu_memory_allocated_bytes"] = torch.cuda.max_memory_allocated(0)
                record["peak_gpu_memory_reserved_bytes"] = torch.cuda.max_memory_reserved(0)
            except Exception as peak_error:
                record["allocator_observation_failure"] = {"type": type(peak_error).__name__, "message": str(peak_error)}
        persist(directory / "observer.json", record)
        raise
    finally:
        if generator_type is not None:
            generator_type.__call__ = original
            record["instrumentation"]["restored_after_run"] = generator_type.__call__ is original
            persist(directory / "observer.json", record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.audit:
        print(json.dumps(audit(config, args.seed, framework=True), ensure_ascii=False, indent=2))
    elif args.output is None:
        parser.error("--output is required for an explicitly granted GPU run")
    else:
        print(json.dumps(run(config, args.seed, args.output, invocation=[sys.executable, *sys.argv],
                             config_file_sha256=sha(args.config)), ensure_ascii=False, indent=2))
