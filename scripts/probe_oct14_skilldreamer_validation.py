#!/usr/bin/env python3
"""Question-only fixed validation format probe, never a capability receipt."""
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
import time

VALIDATION_IDS = ("13", "1", "4", "6", "23", "21", "14", "15")
ALGORITHM_COMMIT = "47f0e9cebc196e15c991d494dc4072367f53043b"
MODEL_REVISION = "bb46c15ee4bb56c5b63245ef50fd7637234d6f75"
ENCODER_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
QUESTIONS_SHA256 = "6a3213a1941882e4d0787b903df170452f13ea13f52ad9dbc4e6cb6e418eca5e"
SOURCE_SHA256 = {
    "skilldreamer/algorithm.py": "c31169a7175fd7e005323a1288905427230a2c61fc906257868b147b1c6e2f76",
    "skilldreamer/experiment.py": "5d327072480d34b940d3aebbb4f6a638dffb81fb6c342c09a799ad8eeb8524c8",
    "skilldreamer/gallery.json": "9ff5e28de7d2eb7b3581ef01bbee66b0d201a543033bde6a2aa66da37f687970",
    "near/data.py": "795416bdffeb25880aeaf85b4bfd6480b8677b45cddabe37ba2e49d7bf544eb8",
    "near/experiment.py": "197e3fefad06f1f0e54533b608c5d717e57d0b6a919a105f88eee79447d94399",
    "state_opd/environment.py": "0e9564f9ec540985eb010b1e70f46938acc1bd946041b518d6579253762080e1",
}


def runner_binding(config: dict) -> dict:
    commit = config.get("probe_source_commit", "")
    root = Path(config.get("probe_source_root", ".")).resolve()
    actual = Path(__file__).resolve()
    if (not re.fullmatch(r"[0-9a-f]{40}", commit) or root.name != "auto-research-oct14-" + commit[:8]
            or actual != root / "scripts/probe_oct14_skilldreamer_validation.py"
            or not (root / ".source-commit").is_file()
            or (root / ".source-commit").read_text().strip() != commit):
        raise ValueError("probe runner must execute from its independently frozen immutable source root")
    digest = hashlib.sha256(actual.read_bytes()).hexdigest()
    if config.get("probe_source_sha256") != digest:
        raise ValueError("probe runner source checksum differs")
    return {"commit": commit, "sha256": digest, "immutable_root_bound": True}


@contextmanager
def hard_wall(seconds: float):
    """Unix signal deadline interrupts one blocking generation, not only boundaries."""
    if not hasattr(signal, "SIGALRM") or signal.getitimer(signal.ITIMER_REAL)[0] != 0:
        raise RuntimeError("exclusive Unix real-time deadline required")
    previous = signal.getsignal(signal.SIGALRM)

    def expired(signum, frame):
        raise TimeoutError("fixed validation total hard wall limit exhausted")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def persist(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".writing")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def questions_only(path: Path) -> tuple[list[dict], dict]:
    content = path.read_bytes()
    source = json.loads((path.parent / "provenance.json").read_text())
    if (hashlib.sha256(content).hexdigest() != QUESTIONS_SHA256
            or source.get("files", {}).get(path.name) != QUESTIONS_SHA256
            or source.get("public_id") != "openai/grade-school-math"
            or source.get("revision") != "3101c7d5072418e28b9008a6636bde82a006892c"
            or source.get("source_split") != "train"
            or source.get("parent_24_rows_sha256") != "8f33a9f7a44067e362458e4daf0eb1ad629a2aac2f44ffefe731e36b19dcb8c1"
            or source.get("validation_ids") != list(VALIDATION_IDS)
            or source.get("scope") != "fixed_original_validation_only"
            or source.get("gold_present") is not False or source.get("scorer_present") is not False
            or source.get("evaluation_ids_used") is not False or source.get("official_test_opened") is not False):
        raise ValueError("verified fixed validation-only question provenance required")
    rows = [json.loads(line) for line in content.splitlines() if line.strip()]
    if (len(rows) != 8 or [row.get("id") for row in rows] != list(VALIDATION_IDS)
            or any(set(row) != {"id", "question"} or not isinstance(row["question"], str)
                   or not row["question"].strip() for row in rows)):
        raise ValueError("exact eight validation id/question records required; gold and other fields forbidden")
    return rows, source


def fixed_budget(config: dict) -> None:
    required = {"seed": 42, "max_new_tokens": 256, "action_budget": 8, "top_k": 3,
                "question_limit": 8, "calls_limit_per_episode": 30, "calls_limit_total": 240,
                "total_wall_limit_seconds": 600}
    if (any(type(config.get(name)) is not int or config[name] != value for name, value in required.items())
            or config.get("device") != "cuda" or config.get("algorithm_commit") != ALGORITHM_COMMIT):
        raise ValueError("fixed original algorithm, seed, token/action/retrieval/call/wall budget required")


def algorithm_binding(config: dict) -> dict:
    expected = config.get("source_sha256", {})
    if config.get("algorithm_commit") != ALGORITHM_COMMIT or expected != SOURCE_SHA256:
        raise ValueError("complete fixed algorithm commit and six-file source whitelist required")
    root = Path(config.get("algorithm_source_root", ".")).resolve()
    marker = root / ".source-commit"
    if (root.name != "auto-research-oct14-47f0e9ce" or not marker.is_file()
            or marker.read_text().strip() != ALGORITHM_COMMIT):
        raise ValueError("algorithm must use its separately frozen immutable 47f0e9ce source root")
    modules = {name: importlib.import_module("auto_research.reproductions." + name.removesuffix(".py").replace("/", "."))
               for name in expected if name.endswith(".py")}
    if any(Path(module.__file__).resolve() != root / "src/auto_research/reproductions" / name
           for name, module in modules.items()):
        raise ValueError("loaded algorithm modules must match the fixed immutable source root")
    actual = {name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() for name, module in modules.items()}
    actual["skilldreamer/gallery.json"] = hashlib.sha256(
        Path(modules["skilldreamer/algorithm.py"].__file__).with_name("gallery.json").read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("loaded library source differs from the fixed 47f0e9ce algorithm archive")
    return actual


def audit(config: dict, *, framework: bool = False) -> dict:
    if framework and os.environ.get("CUDA_VISIBLE_DEVICES") != "":
        raise ValueError("CPU audit requires CUDA explicitly disabled")
    fixed_budget(config)
    runner = runner_binding(config)
    actual = algorithm_binding(config)
    rows, input_source = questions_only(Path(config["questions_file"]))
    from auto_research.reproductions.near.experiment import verify_provenance
    model_dir, encoder_dir = Path(config["model_dir"]), Path(config["encoder_dir"])
    resources = []
    model_files = ("config.json", "generation_config.json", "merges.txt", "model.safetensors.index.json",
                   "tokenizer.json", "tokenizer_config.json", "vocab.json", *[
                       f"model-{index:05d}-of-00004.safetensors" for index in range(1, 5)])
    encoder_files = ("model.safetensors", "config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "vocab.txt")
    for directory, public_id, revision, files in ((model_dir, "Qwen/Qwen2.5-7B-Instruct", MODEL_REVISION, model_files),
            (encoder_dir, "sentence-transformers/all-MiniLM-L6-v2", ENCODER_REVISION, encoder_files)):
        source = json.loads((directory / "provenance.json").read_text())
        if set(source.get("files", {})) != set(files):
            raise ValueError("exact public checkpoint file whitelist required")
        resources.append(verify_provenance(directory, public_id, revision, files))
    report = {"mode": "cpu_audit" if framework else "resource_and_source_audit", "questions": len(rows),
              "validation_ids": list(VALIDATION_IDS), "input": input_source, "checkpoint": resources[0], "encoder": resources[1],
              "algorithm_commit": ALGORITHM_COMMIT, "source_sha256": actual,
              "probe_source": runner,
              "gold_present": False, "scorer_present": False, "evaluation_ids_used": False,
              "capability_receipt": False, "budget": {key: config[key] for key in
                  ("seed", "max_new_tokens", "action_budget", "top_k", "question_limit", "calls_limit_per_episode",
                   "calls_limit_total", "total_wall_limit_seconds")}}
    if framework:
        from transformers import AutoConfig, AutoTokenizer
        from auto_research.reproductions.near.data import FrozenMiniLM
        import numpy as np
        model_config = AutoConfig.from_pretrained(str(model_dir), local_files_only=True)
        tokenizer = AutoTokenizer.from_pretrained(str(model_dir), local_files_only=True)
        text = tokenizer.apply_chat_template([{"role": "user", "content": "Schema audit only."}],
                                             tokenize=False, add_generation_prompt=True)
        encoded, _ = FrozenMiniLM(encoder_dir, "cpu").encode(["Validation formatting audit only."])
        if model_config.model_type != "qwen2" or not text or encoded.shape != (1, 384) or not np.isfinite(encoded).all():
            raise ValueError("CPU tokenizer/config/frozen encoder contract failed")
        report["cpu_framework_checks"] = {"qwen_config_tokenizer": True, "minilm_finite_shape": [1, 384], "cuda_executed": False}
    return report


def _execute_probe(config: dict, output: Path) -> dict:
    start = time.monotonic()
    protocol = audit(config)
    from auto_research.reproductions.skilldreamer.experiment import LocalGenerator
    from auto_research.reproductions.skilldreamer.algorithm import Skill, prospective_skills, hybrid_retrieval, execute_agent
    from auto_research.reproductions.near.data import FrozenMiniLM
    import auto_research.reproductions.skilldreamer.algorithm as algorithm
    rows, _ = questions_only(Path(config["questions_file"]))
    generate = LocalGenerator(Path(config["model_dir"]), "cuda", config["seed"], 256)
    encoder = FrozenMiniLM(Path(config["encoder_dir"]), "cuda")
    gallery = [Skill(**row) for row in json.loads(Path(algorithm.__file__).with_name("gallery.json").read_text())]
    trace = output.with_suffix(".trace.jsonl")
    episodes, attempts, current_id = [], 0, None
    embedding_batches = []

    def traced_generate(prompt):
        nonlocal attempts
        if time.monotonic() - start >= 600:
            raise TimeoutError("fixed validation total wall limit exhausted")
        if attempts >= 240:
            raise RuntimeError("original total generation call bound exhausted")
        attempts += 1
        with trace.open("a") as handle:
            handle.write(json.dumps({"id": current_id, "call": attempts, "event": "generation_attempt", "prompt": prompt}, ensure_ascii=False) + "\n")
        response = generate(prompt)
        with trace.open("a") as handle:
            handle.write(json.dumps({"id": current_id, "call": attempts, "event": "generation_response", "response": response}, ensure_ascii=False) + "\n")
        return response

    def encode(texts):
        values, _ = encoder.encode(texts)
        embedding_batches.append({"id": current_id, "texts": len(texts), "shape": list(values.shape)})
        return values

    result = {"scope": "fixed_validation_format_probe", "status": "running", "diagnostic_only": True,
              "promotion_eligible": False, "capability_receipt": False, "protocol": protocol,
              "episodes": episodes, "embedding_batches": embedding_batches, "trace": trace.name}
    partial = output.with_suffix(".partial.json")
    persist(partial, result)
    for row in rows:
        current_id = row["id"]
        generate.torch.manual_seed(config["seed"] + int(current_id))
        calls_before, tokens_before = generate.calls, generate.generated_tokens
        stage = {"psg_completed": False, "hsr_executed": False}
        try:
            pseudo, anchors = prospective_skills(row["question"], traced_generate)
            stage["psg_completed"] = True
            candidates = hybrid_retrieval(row["question"], pseudo, anchors, gallery, encode, top_k=3)
            stage["hsr_executed"] = True
            outcome = execute_agent(row["question"], traced_generate, candidates, mode="skilldreamer", action_budget=8)
            outcome.update({"psg_completed": True, "hsr_executed": True, "pseudo_count": len(pseudo),
                            "anchors": anchors, "retrieved_skills": [skill.id for skill in candidates]})
        except ValueError as exc:
            outcome = {"failure": str(exc), **stage,
                       "loaded_skills": [], "capability_checks": [], "executed_actions": 0}
        outcome.update({"id": current_id, "model_calls_including_psg": generate.calls - calls_before,
                        "generated_tokens_including_psg": generate.generated_tokens - tokens_before})
        if outcome["model_calls_including_psg"] > 30:
            raise RuntimeError("original per-episode generation call bound exceeded")
        episodes.append(outcome)
        result["wall_seconds"] = time.monotonic() - start
        persist(partial, result)
    if time.monotonic() - start > 600:
        raise TimeoutError("fixed validation total wall limit exhausted")
    result.update({"status": "completed_validation_probe", "model_calls": generate.calls,
                   "generated_tokens": generate.generated_tokens, "wall_seconds": time.monotonic() - start,
                   "execution_checks": {"psg_episodes": sum(row["psg_completed"] for row in episodes),
                       "hsr_episodes": sum(row["hsr_executed"] for row in episodes),
                       "actual_csi_assessments": sum(len(row["capability_checks"]) for row in episodes),
                       "loaded_skill_episodes": sum(bool(row["loaded_skills"]) for row in episodes),
                       "executed_actions": sum(row["executed_actions"] for row in episodes)}})
    persist(output, result)
    return result


def run(config: dict, output: Path) -> dict:
    fixed_budget(config)
    trace, partial = output.with_suffix(".trace.jsonl"), output.with_suffix(".partial.json")
    if any(path.exists() for path in (output, trace, partial)):
        raise FileExistsError("immutable validation probe output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    trace.touch()
    persist(partial, {"status": "starting", "scope": "fixed_validation_format_probe", "episodes": [],
                      "diagnostic_only": True, "promotion_eligible": False, "capability_receipt": False})
    start = time.monotonic()
    try:
        with hard_wall(600):
            return _execute_probe(config, output)
    except Exception as exc:
        retained = json.loads(partial.read_text())
        retained.update({"status": "timed_out" if isinstance(exc, TimeoutError) else "failed",
                         "failure": {"type": type(exc).__name__, "message": str(exc)},
                         "wall_seconds": time.monotonic() - start,
                         "capability_receipt": False, "diagnostic_only": True, "promotion_eligible": False})
        # These files belong to this active fresh run; failure cannot leave a
        # completed marker behind even if the deadline fired during persistence.
        persist(partial, retained)
        persist(output, retained)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.audit:
        print(json.dumps(audit(config, framework=True), ensure_ascii=False, indent=2))
    elif args.output is None:
        parser.error("--output is required for the authorized GPU probe")
    else:
        result = run(config, args.output)
        print(json.dumps({"status": result["status"], "checks": result["execution_checks"]}))
