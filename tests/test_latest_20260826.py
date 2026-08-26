from pathlib import Path

import numpy as np

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentResearchConfig, AgentTask
from auto_research.evolution.papers import (
    AGENT_MUTATIONS,
    INSTALLED_MUTATIONS,
    LLM_MUTATIONS,
    POST_TRAINING_MUTATIONS,
)
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


def test_opd_search_plus_and_opdvr_execute_distinct_objectives(tmp_path: Path):
    diagnostics = {}
    for algorithm, marker in (
        ("opd-search-plus", "search_evidence_mean"),
        ("opdvr", "relu_gated_reward_mean"),
    ):
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=algorithm,
            steps=4,
            maximum_examples=32,
            output_dir=tmp_path / algorithm,
            allow_network=False,
        )).run()
        diagnostics[algorithm] = result.training["last_diagnostics"]
        assert marker in diagnostics[algorithm]
    assert diagnostics["opd-search-plus"]["teacher_finetuning_calls"] == 0.0
    assert diagnostics["opdvr"]["extra_loss_hyperparameters"] == 0.0


def test_latest_agents_expose_paper_specific_state_transitions():
    task = AgentTask(
        "t0", "planning", "deploy safely", (), "ok",
        ("inspect", "patch", "verify"), ("inspect", "patch", "verify"),
    )
    expectations = {
        "spo-plus-plus": ("event-time-value", "per_token_clips"),
        "skillforge": ("explicit-call", "skills_created"),
        "ahead": ("corrective-hint", "privileged_guidance_updates"),
        "smith": ("schema+code+outcome", "local_verifier_calls"),
    }
    for method, (source_marker, counter) in expectations.items():
        agent = build_agent(method, 8, np.random.default_rng(42))
        source = agent.solve(task, 0)[2]
        assert source_marker in source
        assert getattr(agent, counter) > 0
        assert AgentResearchConfig(method=method).method == method


def test_latest_papers_are_registered_for_reproduction_and_evolution():
    assert get_adapter("tagr").paper.arxiv_id == "2608.24034"
    assert get_adapter("wemm-embedding").paper.arxiv_id == "2608.24053"
    assert INSTALLED_MUTATIONS["2608.24034"][0] == "rankmixer_tagr"
    assert LLM_MUTATIONS["2608.24053"][0] == "multimodal:wemm-embedding"
    for paper_id in ("2608.24310", "2608.24696"):
        assert paper_id in POST_TRAINING_MUTATIONS
    for paper_id in ("2608.24870", "2608.24747", "2608.24114", "2608.24571"):
        assert paper_id in AGENT_MUTATIONS
