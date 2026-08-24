from pathlib import Path

import numpy as np

from auto_research.agent_research.latest_20260824 import action_information
from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentResearchConfig
from auto_research.post_training.models import PostTrainingConfig
from auto_research.reproductions.registry import get_adapter


def test_recent_adapters_have_verified_metadata_and_mechanisms(tmp_path: Path):
    onemodel = get_adapter("onemodel")
    assert onemodel.paper.has_online_ab
    assert onemodel.paper.organization == "Xiaohongshu"

    rare = get_adapter("rare")
    result = rare.run(tmp_path, 42)
    assert result["variants"]["RARE null-space + correction"]["route_agreement"] == 1.0
    assert result["variants"]["raw representation steering"]["route_flip_rate"] > 0


def test_gcpo_and_auso_are_public_runner_choices():
    assert PostTrainingConfig(algorithm="gcpo").algorithm == "gcpo"
    assert AgentResearchConfig(method="auso").method == "auso"
    agent = build_agent("auso", 8, np.random.default_rng(42))
    assert agent.__class__.__name__ == "AUSOAgent"
    assert action_information((0.8, 0.15, 0.05), (0.4, 0.35, 0.25)) > 0
