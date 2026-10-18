"""CPU-only SKILL.state contract diagnostic, not a language-model benchmark."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import statistics
import subprocess
import time

from auto_research.agent_research.skill_state import SkillStateRuntime, merge_patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = ("scripts/run_oct19_skill_state.py", "src/auto_research/agent_research/skill_state.py")


def diagnostic(seed):
    rng = random.Random(seed)
    def schema(state):
        return set(state) == {"count", "marker"} and type(state["count"]) is int and isinstance(state["marker"], str) and len(state["marker"]) == 8
    runtime = SkillStateRuntime("Apply only the latest public delta; emit an inert action.",
        {"count": 0, "marker": "00000000"}, validator=schema, max_state_chars=64, max_observation_chars=64)
    transient = f"TRANSIENT-{rng.randrange(10**9)}"
    history, lengths, errors, fixture = [], [], [], []
    calls, retries, replayed, drift = [], 0, 0, 0
    expected = 0
    for turn in range(200):
        observation = {"delta": rng.choice((-1, 1)), "marker": f"{rng.randrange(10**8):08d}"}
        expected += observation["delta"]
        views = []
        def actor(context):
            nonlocal replayed
            views.append(context)
            replayed += transient in str(context)
            public = json.loads(context.observation_json)
            state = json.loads(context.state_json)
            patch = {"forbidden_history": "not schema state"} if turn == 0 and len(views) == 1 else {
                "count": state["count"] + public["delta"], "marker": public["marker"]}
            return transient + "\n```json\n" + json.dumps({"state_patch": patch, "action": "inert-update"}) + "\n```"
        outcome = runtime.step(observation, actor=actor, executor=lambda action: calls.append(action) or {"status": "observed"})
        retries += outcome.attempts - 1
        drift += any(view != views[0] for view in views)
        errors.append(abs(runtime.snapshot()["count"] - expected))
        lengths.append(outcome.prompt_characters)
        fixture.append(observation)
        history.append(json.dumps(observation) + transient + "inert-update")
    source = {"keep": 1, "nested": {"a": 2, "b": 3}}
    merged = merge_patch(source, {"nested": {"a": None}})
    merge_error = int(merged != {"keep": 1, "nested": {"b": 3}})
    assert max(errors) == 0 and retries == 1 and not replayed and not drift and merge_error == 0
    assert len(calls) == runtime.version == 200 and max(lengths) - min(lengths) < 8
    negative_growth = sum(len(item) for item in history) - max(lengths)
    assert negative_growth > 1000
    return {"seed": seed, "fixture_sha256": hashlib.sha256(json.dumps(fixture, sort_keys=True).encode()).hexdigest(),
        "metrics": {"public_turns": 200, "executed_inert_actions": len(calls), "invalid_patch_retries": retries,
            "state_update_reference_max_error": max(errors), "recursive_deletion_reference_error": merge_error,
            "discarded_reasoning_replayed": replayed, "retry_public_context_drift": drift,
            "max_prompt_characters": max(lengths), "prompt_character_range": max(lengths)-min(lengths),
            "append_only_fixture_negative_control_character_growth": negative_growth}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not 1 <= len(seeds) <= 5 or len(set(seeds)) != len(seeds) or any(not 0 <= value < 2**32 for value in seeds):
        parser.error("one to five distinct uint32 seeds required")
    if args.output.exists():
        parser.error("immutable output already exists")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("full code commit required")
    start = time.monotonic()
    rows = [diagnostic(seed) for seed in seeds]
    metrics = {key: {"mean": statistics.mean(row["metrics"][key] for row in rows),
        "std": statistics.stdev(row["metrics"][key] for row in rows) if len(rows) > 1 else 0., "n": len(rows)}
        for key in rows[0]["metrics"]}
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS], cwd=ROOT, text=True).strip())
    payload = {"schema_version": 2, "code_commit": commit, "device": "cpu", "accelerator": "CPU",
        "executed_source_uncommitted": dirty, "evolve_integrated": False,
        "seeds": seeds, "diagnostic_only": True, "promotion_eligible": False,
        "executed_source_sha256": {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in SOURCE_PATHS},
        "components": {"skill-state": {"dataset": {"id": "synthetic-skill-state-public-counter",
            "revision": "oct19-skill-state-contract-v1", "capability_benchmark": False},
            "per_seed": rows, "metrics": metrics, "diagnostic_only": True, "promotion_eligible": False,
            "evolve_integrated": False, "full_experiment_status": "not_reproduced_high_cost"}},
        "elapsed_seconds": time.monotonic()-start}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"components": ["skill-state"], "output": str(args.output), "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
