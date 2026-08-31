"""Safe, dataset-backed evaluations for late-August Agent mechanisms.

The runner consumes official benchmark exports without executing attacks,
untrusted paper code, or repository mutations.  Each method has an explicit
schema and compares its selection rule with equal-budget random baselines.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import random
import statistics


METHODS = ("redevoagent", "ace-data", "deeprepro")


@dataclass(frozen=True)
class PublicAgentArtifactConfig:
    method: str
    artifact: Path
    dataset_id: str
    dataset_revision: str
    output_dir: Path = Path("runs/public-agent-artifacts")
    seeds: tuple[int, ...] = (42, 43, 44)
    budget: int = 32

    def validate(self) -> None:
        if self.method not in METHODS:
            raise ValueError(f"method must be one of {METHODS}")
        if len(self.seeds) != 3 or len(set(self.seeds)) != 3:
            raise ValueError("public Agent evaluation requires three distinct seeds")
        if self.budget < 1:
            raise ValueError("budget must be positive")
        if not self.dataset_id or not self.dataset_revision:
            raise ValueError("public dataset id and immutable revision are required")


def run_public_agent_artifact(config: PublicAgentArtifactConfig) -> tuple[dict, Path]:
    config.validate()
    rows = _load_rows(config.artifact)
    evaluator = {
        "redevoagent": _redevoagent,
        "ace-data": _ace_data,
        "deeprepro": _deeprepro,
    }[config.method]
    seed_results = [evaluator(rows, config.budget, seed) for seed in config.seeds]
    payload = {
        "schema_version": 1,
        "method": config.method,
        "config": {
            **asdict(config),
            "artifact": str(config.artifact),
            "output_dir": str(config.output_dir),
        },
        "seed_results": seed_results,
        "metrics": {
            "baseline": _aggregate([row["baseline_score"] for row in seed_results]),
            "method": _aggregate([row["method_score"] for row in seed_results]),
        },
        "provenance": {
            "dataset_id": config.dataset_id,
            "dataset_revision": config.dataset_revision,
            "rows": len(rows),
        },
        "protocol": {
            "three_seeds": True,
            "equal_budget_baseline": True,
            "raw_content_committed": False,
            "safe_offline_replay": True,
            "claim_boundary": _claim_boundary(config.method),
        },
    }
    target = config.output_dir / config.method
    target.mkdir(parents=True, exist_ok=True)
    path = target / "metrics.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload, path


def _load_rows(path: Path) -> list[dict]:
    if path.suffix == ".jsonl":
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload.get("rows", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or not rows:
        raise ValueError("public artifact must contain a non-empty row list")
    return rows


def _redevoagent(rows, budget, seed):
    required = {"split", "tool_trace", "success"}
    _require(rows, required)
    train = [row for row in rows if row["split"] == "train"]
    validation = [row for row in rows if row["split"] == "validation"]
    test = [row for row in rows if row["split"] == "test"]
    if not train or not validation or not test:
        raise ValueError("RedEvoAgent export requires train/validation/test splits")
    profiles = {}
    for row in train:
        for tool in set(map(str, row["tool_trace"])):
            score, count = profiles.get(tool, (0, 0))
            profiles[tool] = (score + int(bool(row["success"])), count + 1)
    ranked = sorted(profiles, key=lambda tool: profiles[tool][0] / profiles[tool][1], reverse=True)
    best_skill = ()
    best_validation = -1.0
    accepts = rejects = 0
    for size in range(1, min(len(ranked), budget) + 1):
        candidate = tuple(ranked[:size])
        score = _tool_coverage(validation, candidate)
        if score > best_validation:
            best_skill, best_validation, accepts = candidate, score, accepts + 1
        else:
            rejects += 1
    rng = random.Random(seed)
    random_skill = tuple(rng.sample(ranked, k=len(best_skill)))
    return {
        "seed": seed,
        "baseline_score": _tool_coverage(test, random_skill),
        "method_score": _tool_coverage(test, best_skill),
        "validation_ratchet_accepts": accepts,
        "validation_ratchet_rejects": rejects,
        "skill_size": len(best_skill),
    }


def _tool_coverage(rows, skill):
    skill = set(skill)
    return statistics.fmean(
        int(bool(row["success"])) * len(skill & set(map(str, row["tool_trace"])))
        / max(1, len(set(map(str, row["tool_trace"]))))
        for row in rows
    )


def _ace_data(rows, budget, seed):
    required = {"verified", "learner_loss", "environment", "task", "trajectory"}
    _require(rows, required)
    accurate = [row for row in rows if bool(row["verified"])]
    if not accurate:
        raise ValueError("ACE Lens export has no verifier-supported rows")
    losses = sorted(float(row["learner_loss"]) for row in accurate)
    low, high = _quantile(losses, 0.2), _quantile(losses, 0.8)
    candidates = [row for row in accurate if low <= float(row["learner_loss"]) <= high]
    selected = []
    signatures = set()
    for row in sorted(candidates, key=lambda item: float(item["learner_loss"]), reverse=True):
        signature = (str(row["environment"]), str(row["task"]), json.dumps(row["trajectory"], sort_keys=True))
        if signature not in signatures:
            signatures.add(signature)
            selected.append(row)
        if len(selected) >= budget:
            break
    rng = random.Random(seed)
    baseline = rng.sample(accurate, k=min(len(selected), len(accurate)))
    return {
        "seed": seed,
        "baseline_score": _ace_score(baseline),
        "method_score": _ace_score(selected),
        "accuracy_gate_passes": len(accurate),
        "complexity_band": [low, high],
        "diversity_accepts": len(selected),
    }


def _ace_score(rows):
    if not rows:
        return 0.0
    supported = statistics.fmean(int(bool(row["verified"])) for row in rows)
    diversity = len({(str(row["environment"]), str(row["task"])) for row in rows}) / len(rows)
    return supported * diversity


def _deeprepro(rows, budget, seed):
    required = {"paper_id", "state_id", "plan_steps", "executed_steps", "tests_passed"}
    _require(rows, required)
    by_paper = {}
    for row in rows:
        by_paper.setdefault(str(row["paper_id"]), []).append(row)
    method_scores = []
    static_scores = []
    revisions = 0
    rng = random.Random(seed)
    for states in by_paper.values():
        states.sort(key=lambda row: str(row["state_id"]))
        static_plan = set(map(str, states[0]["plan_steps"]))
        sampled = rng.sample(list(static_plan), k=min(len(static_plan), budget))
        static_scores.append(_execution_coverage(states[-1], sampled))
        previous = None
        for state in states:
            plan = tuple(map(str, state["plan_steps"]))[:budget]
            revisions += int(previous is not None and plan != previous)
            previous = plan
        method_scores.append(_execution_coverage(states[-1], previous or ()))
    return {
        "seed": seed,
        "baseline_score": statistics.fmean(static_scores),
        "method_score": statistics.fmean(method_scores),
        "repository_snapshots": len(rows),
        "subplan_revisions": revisions,
    }


def _execution_coverage(row, plan):
    executed = set(map(str, row["executed_steps"]))
    coverage = len(executed & set(plan)) / max(1, len(executed))
    return coverage * int(bool(row["tests_passed"]))


def _require(rows, fields):
    for index, row in enumerate(rows):
        missing = fields - set(row)
        if missing:
            raise ValueError(f"row {index} lacks required fields: {sorted(missing)}")


def _quantile(values, q):
    position = (len(values) - 1) * q
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return values[lower]
    return values[lower] * (upper - position) + values[upper] * (position - lower)


def _aggregate(values):
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    radius = 1.96 * std / math.sqrt(len(values))
    return {"mean": mean, "std": std, "ci95_low": mean - radius, "ci95_high": mean + radius}


def _claim_boundary(method):
    return {
        "redevoagent": "offline replay of benchmark traces; no live jailbreak or target-agent attack is executed",
        "ace-data": "data curation evaluation, not a claim that the survey introduced a trained model",
        "deeprepro": "PaperBench/Code-Dev artifact replay; no claim of reproducing the paper's full API-budget run",
    }[method]
