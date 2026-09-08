from pathlib import Path

import numpy as np
import torch

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentTask
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner
from auto_research.reproductions.beaconkv.model import beacon_retained_indices, farthest_point_beacons
from auto_research.reproductions.kvmem.model import select_workspace_blocks
from auto_research.reproductions.registry import get_adapter


def test_new_recommendation_adapters_execute_public_protocol():
    for key in ("allecompanion", "autolr"):
        result = get_adapter(key).run(Path("data"), 42)
        assert result["method"]["ndcg_at_10"] >= 0
        assert result["stages"]["finite_scores"] == result["dataset"]["items"]


def test_beaconkv_preserves_budget_and_diverse_beacons():
    torch.manual_seed(42)
    keys, queries = torch.randn(128, 16), torch.randn(48, 16)
    beacon_ids = farthest_point_beacons(queries, 6)
    retained = beacon_retained_indices(keys, queries, 40, beacon_count=6, recent_tokens=12)
    assert len(torch.unique(beacon_ids)) == 6
    assert len(retained) == 40
    assert set(range(116, 128)).issubset(set(retained.tolist()))


def test_kvmem_materializes_only_query_selected_blocks():
    torch.manual_seed(42)
    keys = torch.randn(160, 16)
    selected, blocks, scores = select_workspace_blocks(keys, keys[35], block_size=16, selected_blocks=3)
    assert len(selected) == 48
    assert len(blocks) == 3
    assert len(scores) == 10


def test_new_agents_abstain_without_public_evidence():
    task = AgentTask("t", "tools", "inspect then verify", ("ctx",), "ok", ("inspect", "verify"), ("inspect", "verify"))
    for key in ("atomrec", "coskill", "silr", "multi-harness-rl"):
        agent = build_agent(key, 8, np.random.default_rng(42))
        answer, plan, trace = agent.solve(task, 0)
        assert answer == "" and plan == ()
        assert trace


def test_sparse_opd_uses_only_one_or_two_supervision_positions(tmp_path):
    result, _ = PostTrainingRunner(PostTrainingConfig(
        algorithm="sparse-opd", steps=4, maximum_examples=32,
        output_dir=tmp_path / "sparse-opd", allow_network=False,
    )).run()
    diagnostics = result.training["last_diagnostics"]
    assert diagnostics["supervised_positions"] <= 2
    assert 0 < diagnostics["supervision_fraction"] <= 0.5
