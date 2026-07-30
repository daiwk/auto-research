from pathlib import Path

import numpy as np

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training.algorithms import initialize, update
from auto_research.post_training.data import load_post_training_data
from auto_research.reproductions.registry import get_adapter
from auto_research.evolution.planner import allowed_architectures


def test_latest_industrial_adapters_have_quantified_online_evidence():
    oxygen = get_adapter("oxygenrec-v2")
    asarl = get_adapter("asarl")
    assert oxygen.paper.organization == "JD.COM"
    assert oxygen.paper.online_ab[0].metric == "UCTCVR"
    assert asarl.paper.organization == "Tencent PCG"
    assert "20% treatment" in asarl.paper.online_ab[0].traffic


def test_reco_executes_both_distribution_corrections():
    suite = load_post_training_data(
        "arithmetic-smoke", Path("data"), False, 32, 42
    )
    state = initialize(len(suite.feature_names), suite.train)
    _, diagnostics = update(
        "reco-grpo",
        state,
        suite.train[0],
        0.05,
        np.random.default_rng(42),
        4,
        0,
    )
    assert diagnostics["response_weight_max"] >= diagnostics["response_weight_mean"]
    assert diagnostics["variance_ratio_mean"] > 0
    assert state.reco_updates == 1


def test_cam_df_and_skillrise_expose_paper_specific_diagnostics(tmp_path):
    cam, _ = AgentResearchRunner(
        AgentResearchConfig(
            method="cam-df",
            benchmark="scalemcp-mini",
            episodes=12,
            output_dir=tmp_path,
        )
    ).run()
    assert cam.diagnostics["cost_aware_stops"] == 12
    assert 0 < cam.diagnostics["tool_exposure_reduction"] < 1

    skills, _ = AgentResearchRunner(
        AgentResearchConfig(
            method="skillrise",
            benchmark="planbench-mini",
            episodes=12,
            output_dir=tmp_path,
        )
    ).run()
    assert skills.diagnostics["skill_document_updates"] == 12
    assert skills.diagnostics["cross_task_skill_reuses"] > 0
    assert skills.diagnostics["downstream_credit_updates"] > 0


def test_latest_methods_are_selectable_by_evolve_direction():
    assert allowed_architectures(
        "post-training", "重点比较 ReCo 与 GRPO", []
    )[0] == "reco-grpo"
