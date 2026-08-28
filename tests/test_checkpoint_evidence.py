from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_research.agent_research.code_benchmark import build_code_benchmark
from auto_research.agent_research.lightning_policy import LightningPolicyConfig
from auto_research.evolution.checkpoint_evidence import (
    load_checkpoint_evidence, promoted_operators,
)


def _write(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_agent_checkpoint_policy_uses_disjoint_splits_and_three_seeds(tmp_path):
    train = build_code_benchmark(10, "train")
    validation = build_code_benchmark(4, "validation")
    test = build_code_benchmark(4, "test")
    assert {row.family for row in train}.isdisjoint(row.family for row in validation)
    assert {row.family for row in train}.isdisjoint(row.family for row in test)
    assert {row.family for row in validation}.isdisjoint(row.family for row in test)
    assert LightningPolicyConfig(tmp_path).seeds == (42, 43, 44)
    with pytest.raises(ValueError, match="three distinct"):
        LightningPolicyConfig(tmp_path, seeds=(42, 42, 43)).validate()


def test_three_seed_checkpoint_artifact_becomes_evolve_proposal_prior(tmp_path):
    artifact = _write(tmp_path / "agent.json", {
        "task": "ag-001-agent-lightning-checkpoint-policy",
        "seed_results": [{"seed": seed} for seed in (42, 43, 44)],
    })
    records = load_checkpoint_evidence((artifact,))
    assert promoted_operators(records, "agent") == ("policy:agent-lightning",)
    assert promoted_operators(records, "post-training") == ()


def test_checkpoint_evidence_rejects_single_seed_diagnostic(tmp_path):
    artifact = _write(tmp_path / "mllm.json", {
        "method": "mllmclip-real-checkpoint-cka",
        "metrics": {"seed_results": [{"seed": 42}]},
    })
    with pytest.raises(ValueError, match="three independent seeds"):
        load_checkpoint_evidence((artifact,))
