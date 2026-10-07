from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .agent_research import AgentResearchConfig, AgentResearchRunner
from .post_training import PostTrainingConfig, PostTrainingRunner
from .reproductions import get_adapter
from .reproductions.execution import run_with_budget
from .reproductions.schema import aggregate_seed_metrics, dataset_fingerprint
from .reproductions.schema import enrich_result
from .experiment_contract import ExperimentSpec, canonical, source_revision
from .evidence_policy import assess_evidence
from .runtime import exclusive_file_lock


@dataclass(frozen=True)
class EvidencePromotionConfig:
    dataset_dir: Path = Path("data")
    output_dir: Path = Path("runs/evidence-promotion")
    seeds: tuple[int, ...] = (42, 43, 44)
    adapters: tuple[str, ...] = ("rankmixer", "switch-transformer")
    post_training: tuple[str, ...] = ("grpo",)
    agent_methods: tuple[str, ...] = ("agent-lightning",)
    budget: str = "standard"
    budget_seconds: int | None = None
    post_steps: int = 80
    agent_episodes: int = 120
    retry_failed: bool = False

    def validate(self) -> None:
        if len(self.seeds) < 3:
            raise ValueError("formal evidence promotion requires at least three seeds")
        if len(set(self.seeds)) != len(self.seeds):
            raise ValueError("seeds must be unique")
        if not (self.adapters or self.post_training or self.agent_methods):
            raise ValueError("at least one promotion target is required")
        if min(self.post_steps, self.agent_episodes) < 1:
            raise ValueError("post steps and agent episodes must be positive")


class EvidencePromotionRunner:
    """Resume-safe three-seed promotion across repository research domains."""

    def __init__(self, config: EvidencePromotionConfig):
        config.validate()
        self.config = config

    def run(self) -> tuple[dict[str, Any], Path]:
        with exclusive_file_lock(self.config.output_dir / "state.json"):
            return self._run()

    def _run(self) -> tuple[dict[str, Any], Path]:
        config = self.config
        run_dir = config.output_dir
        run_dir.mkdir(parents=True, exist_ok=True)
        state_path = run_dir / "state.json"
        state = _read_state(state_path)
        spec = ExperimentSpec(
            {key: value for key, value in canonical(config).items()
             if key not in {"output_dir", "retry_failed"}},
            {"dataset": dataset_fingerprint(config.dataset_dir)}, source_revision(),
        )
        if state["runs"]:
            spec.require_match(state.get("experiment_spec", {}))
        state["experiment_spec"] = spec.to_dict()
        targets = [
            *(("reproduction", key) for key in config.adapters),
            *(("post-training", key) for key in config.post_training),
            *(("agent", key) for key in config.agent_methods),
        ]
        for family, name in targets:
            for seed in config.seeds:
                key = f"{family}:{name}:{seed}"
                previous = state["runs"].get(key)
                if previous and (
                    previous.get("status") == "completed" or not config.retry_failed
                ):
                    continue
                started = datetime.now(timezone.utc).isoformat()
                try:
                    result = self._execute(family, name, seed)
                    record = {
                        "status": "completed", "started_at": started,
                        "completed_at": datetime.now(timezone.utc).isoformat(),
                        "result": result,
                    }
                except Exception as exc:  # failures are evidence, not batch aborts
                    record = {
                        "status": "failed", "started_at": started,
                        "completed_at": datetime.now(timezone.utc).isoformat(),
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                if previous:
                    attempts = list(previous.get("previous_attempts", ()))
                    attempts.append({
                        key: value for key, value in previous.items()
                        if key != "previous_attempts"
                    })
                    record["previous_attempts"] = attempts
                state["runs"][key] = record
                _write_json_atomic(state_path, state)
        payload = _summarize(config, state, targets)
        _write_json_atomic(run_dir / "metrics.json", payload)
        (run_dir / "report.md").write_text(_render_report(payload), encoding="utf-8")
        return payload, run_dir

    def _execute(self, family: str, name: str, seed: int) -> dict[str, Any]:
        config = self.config
        if family == "reproduction":
            adapter = get_adapter(name)
            result = run_with_budget(
                adapter, config.dataset_dir, seed, config.budget,
                timeout_override=config.budget_seconds,
            )
            return {"seed": seed, **enrich_result(
                adapter, result, seeds=(seed,), dataset_dir=config.dataset_dir, budget=config.budget,
            )}
        if family == "post-training":
            result, _ = PostTrainingRunner(PostTrainingConfig(
                algorithm=name, dataset="arithmetic-smoke",
                dataset_dir=config.dataset_dir,
                output_dir=config.output_dir / "raw" / "post-training",
                steps=config.post_steps, seed=seed, allow_network=False,
            )).run()
            return {
                "seed": seed, "baseline": result.baseline,
                "final": result.final,
                "relative_accuracy": result.relative_accuracy,
                "training": result.training,
            }
        code_methods = {"agent-lightning", "swe-agent", "openhands", "critic", "metagpt"}
        benchmark = "swebench-local" if name in code_methods else "evomem-mini"
        result, _ = AgentResearchRunner(AgentResearchConfig(
            method=name, benchmark=benchmark,
            episodes=config.agent_episodes, seed=seed,
            output_dir=config.output_dir / "raw" / "agent",
        )).run()
        return {
            "seed": seed, "metrics": result.metrics,
            "axis_metrics": result.axis_metrics,
            "diagnostics": result.diagnostics,
        }


def _read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "runs": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError(f"unsupported evidence-promotion state: {path}")
    return payload


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _summarize(config, state, targets):
    summaries = {}
    for family, name in targets:
        records = [
            state["runs"].get(f"{family}:{name}:{seed}", {})
            for seed in config.seeds
        ]
        successes = [record["result"] for record in records if record.get("status") == "completed"]
        failures = [
            {"seed": seed, "error": record.get("error", "missing")}
            for seed, record in zip(config.seeds, records)
            if record.get("status") != "completed"
        ]
        first = successes[0] if successes else {}
        seed_payload = {
            "seed_results": successes,
            "evaluation_protocol": first.get("evaluation_protocol", {}),
            "comparison_contract": first.get("comparison_contract", {}),
        }
        assessment = assess_evidence(seed_payload, seeds=[row["seed"] for row in successes])
        if failures:
            assessment["formal_comparison"] = False
            assessment["eligibility_reasons"].append("requested_seed_failed")
            assessment["claim_policy"] = "incomplete comparison; requested seed failed"
        summaries[f"{family}:{name}"] = {
            "family": family,
            "name": name,
            "requested_seeds": list(config.seeds),
            "successful_seeds": [row["seed"] for row in successes],
            "failed_seeds": failures,
            "previous_failed_attempts": [
                {
                    "seed": seed,
                    "attempts": [
                        attempt for attempt in record.get("previous_attempts", ())
                        if attempt.get("status") == "failed"
                    ],
                }
                for seed, record in zip(config.seeds, records)
                if any(
                    attempt.get("status") == "failed"
                    for attempt in record.get("previous_attempts", ())
                )
            ],
            "seed_results": successes,
            "aggregate_metrics": aggregate_seed_metrics(successes) if successes else {},
            **assessment,
        }
    return {
        "schema_version": 2,
        "manifest_ref": "docs/research-roadmap.md#auto-research--evolve",
        "config": {**asdict(config), "dataset_dir": str(config.dataset_dir), "output_dir": str(config.output_dir)},
        "experiment_spec": state.get("experiment_spec", {}),
        "provenance": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "dataset_fingerprint": dataset_fingerprint(config.dataset_dir),
        },
        "evaluation_protocol": {
            "tier": "mixed_per_target; see targets for actual evidence tier",
            "seeds": list(config.seeds),
            "failure_policy": "retain every failed seed and continue resumably",
            "confidence_interval": "normal 95%; shown only when >=3 seeds complete",
        },
        "targets": summaries,
    }


def _render_report(payload):
    lines = [
        "# 重点方法三 seed 晋级报告", "",
        "本报告统一保留每个 seed 的成功、失败、均值、标准差与 95% 置信区间。",
        "少于三个成功 seed 的目标不得用于稳定提升声明；诊断结果无论 seed 数量多少均不得晋级。",
        "正式比较还要求可核验的数据/切分版本、基线、代码版本与 test 隔离协议。", "",
        "| 目标 | 成功 seeds | 当前失败 seeds | 历史失败尝试 | 正式比较 |",
        "|---|---|---|---:|---|",
    ]
    for key, result in payload["targets"].items():
        failures = ", ".join(str(row["seed"]) for row in result["failed_seeds"]) or "—"
        lines.append(
            f"| `{key}` | {', '.join(map(str, result['successful_seeds'])) or '—'} | "
            f"{failures} | "
            f"{sum(len(row['attempts']) for row in result['previous_failed_attempts'])} | "
            f"{'是' if result['formal_comparison'] else '否'} |"
        )
        if result["eligibility_reasons"]:
            lines.append(f"\n`{key}` 未满足条件：" + ", ".join(result["eligibility_reasons"]) + "\n")
    lines += [
        "", "## 复现", "",
        "```bash",
        "auto-research promote-evidence --dataset-dir data --seeds 42,43,44",
        "```", "",
        "中断后重复同一命令会读取 `state.json`，只补跑缺失的 target/seed；"
        "checkpoint 与 raw runs 不提交 Git。", "",
    ]
    return "\n".join(lines)
