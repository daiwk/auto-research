from __future__ import annotations

import random

import numpy as np

from auto_research.evidence_promotion import (
    EvidencePromotionConfig, EvidencePromotionRunner,
)
from auto_research.evolution.composable import AgentEvolutionEvaluator
from auto_research.evolution.genrec import GenRecEvolutionEvaluator
from auto_research.evolution.models import Genome
from auto_research.evolution.planner import allowed_architectures, propose
from auto_research.reproductions.genrec_netflix.data import GenRecData


def _genrec_data(users=30, items=28):
    train = tuple(
        tuple((user * 3 + offset) % items for offset in range(10))
        for user in range(users)
    )
    return GenRecData(
        train=train,
        validation=tuple((user * 3 + 10) % items for user in range(users)),
        test=tuple((user * 3 + 11) % items for user in range(users)),
        item_texts=tuple(f"movie {item}" for item in range(items)),
        item_genres=tuple((("action" if item % 2 else "drama"),) for item in range(items)),
        popularity=np.asarray([items - item for item in range(items)], dtype=np.float32),
    )


def test_genrec_evolve_uses_real_full_catalog_and_composable_axes(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "auto_research.evolution.genrec.load_genrec_data",
        lambda *args, **kwargs: _genrec_data(),
    )
    evaluator = GenRecEvolutionEvaluator(tmp_path, 3, (42, 43, 44), False, None, None)
    operators = allowed_architectures("genrec", "组合 GenRec", [])
    assert {value.split(":", 1)[0] for value in operators} == {
        "context", "head", "reward", "distillation",
    }
    parent = Genome(architecture="genrec-catalog", dimensions=16, sequence_length=4)
    first, _ = propose(parent, 1, 0, operators, random.Random(42), "genrec")
    combined, _ = propose(first, 2, 0, operators, random.Random(42), "genrec")
    trial = evaluator.evaluate("g1-t1", 1, "g0-t0", combined, (), "test")
    assert trial.training["full_catalog"] is True
    assert trial.training["catalog_items"] == 28
    assert trial.training["seeds"] == [42, 43, 44]
    assert trial.validation["primary_std"] >= 0
    assert 0 <= trial.validation["ndcg_at_10"] <= 1


def test_agent_evolve_has_independent_policy_and_failure_recovery_axes():
    operators = [
        "planner:fast", "policy:agent-lightning", "recovery:reflexion",
        "memory:skillrise", "tool:direct", "critic:agent-lightning",
    ]
    parent = Genome(
        architecture="composable-agent", agent_planner="fast",
        agent_policy="agent-lightning", agent_failure_recovery="reflexion",
    )
    child, rationale = propose(parent, 2, 1, operators, random.Random(7), "agent")
    assert child.agent_policy in {"heuristic", "replay-policy", "pairwise-policy", "agent-lightning"}
    assert child.agent_failure_recovery in {"none", "retry", "rollback", "reflexion"}
    assert "policy / recovery" in rationale
    evaluator = AgentEvolutionEvaluator("planbench-mini", (42, 43, 44), episodes=24)
    trial = evaluator.evaluate("g2-t1", 2, "g1-t1", parent, (), rationale)
    assert trial.training["components"]["policy"] == "agent-lightning"
    assert trial.validation["recovery_attempts"] > 0
    assert trial.validation["recovery_rate"] == 1.0
    assert trial.validation["policy_updates"] > 0


def test_evidence_promotion_is_three_seed_resume_safe_and_retains_failures(monkeypatch, tmp_path):
    config = EvidencePromotionConfig(
        dataset_dir=tmp_path / "data", output_dir=tmp_path / "promotion",
        adapters=("toy",), post_training=(), agent_methods=(),
    )
    calls = []

    def execute(self, family, name, seed):
        calls.append(seed)
        if seed == 43:
            raise RuntimeError("intentional seed failure")
        return {"seed": seed, "metrics": {"primary": seed / 100.0}}

    monkeypatch.setattr(EvidencePromotionRunner, "_execute", execute)
    payload, run_dir = EvidencePromotionRunner(config).run()
    target = payload["targets"]["reproduction:toy"]
    assert target["formal_comparison"] is False
    assert target["failed_seeds"] == [
        {"seed": 43, "error": "RuntimeError: intentional seed failure"}
    ]
    assert (run_dir / "state.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert "不得用于稳定提升声明" in (run_dir / "report.md").read_text(encoding="utf-8")
    EvidencePromotionRunner(config).run()
    assert calls == [42, 43, 44]  # completed and failed terminal states both resume


def test_evidence_promotion_marks_three_successful_seeds_formal(monkeypatch, tmp_path):
    config = EvidencePromotionConfig(
        dataset_dir=tmp_path / "data", output_dir=tmp_path / "promotion",
        adapters=("toy",), post_training=(), agent_methods=(),
    )
    monkeypatch.setattr(
        EvidencePromotionRunner, "_execute",
        lambda self, family, name, seed: {
            "seed": seed, "metrics": {"primary": float(seed)}
        },
    )
    payload, _ = EvidencePromotionRunner(config).run()
    target = payload["targets"]["reproduction:toy"]
    assert target["formal_comparison"] is True
    assert target["aggregate_metrics"]["metrics.primary"]["n"] == 3
    assert target["aggregate_metrics"]["metrics.primary"]["ci95"] is not None
