from pathlib import Path

import numpy as np

from auto_research.agent_research.models import AgentResearchConfig, AgentTask
from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.runner import AgentResearchRunner
from auto_research.evolution.compatibility import operator_registry
from auto_research.evolution.papers import (
    AGENT_MUTATIONS,
    INSTALLED_MUTATIONS,
    LLM_MUTATIONS,
    POST_TRAINING_MUTATIONS,
)
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


def test_latest_post_training_objectives_execute_distinct_credit_paths(tmp_path: Path):
    expectations = {
        "v-rubrics": "visual_faithfulness_credit",
        "clue-opsd": "clue_teacher_process_reward",
        "grin": "golden_answer_injection_fraction",
        "grip": "interpolation_alpha_mean",
    }
    for algorithm, marker in expectations.items():
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=algorithm, steps=4, maximum_examples=32,
            output_dir=tmp_path / algorithm, allow_network=False,
        )).run()
        assert marker in result.training["last_diagnostics"]


def test_latest_agents_expose_paper_specific_control_flow(tmp_path: Path):
    task = AgentTask(
        "t0", "planning", "deploy safely", ("repo",), "ok",
        ("inspect", "patch", "verify"), ("inspect", "patch", "verify"),
    )
    expectations = {
        "jit-agent": ("memory+planning+protocol+tools", "harness_generations"),
        "traceml": ("trace-schema", "versioned_edits"),
        "adavdr": ("reliability-reflection", "tool_necessity_filters"),
        "topas": ("critical-path", "critical_path_updates"),
        "caskg": ("counterfactual-probe", "counterfactual_probes"),
        "progrouter": ("budget-gate", "meta_gate_decisions"),
    }
    for method, (source_marker, counter) in expectations.items():
        agent = build_agent(method, 8, np.random.default_rng(42))
        assert source_marker in agent.solve(task, 0)[2]
        assert getattr(agent, counter) > 0
        result, _ = AgentResearchRunner(AgentResearchConfig(
            method=method, episodes=12, output_dir=tmp_path / method,
        )).run()
        assert counter in result.diagnostics


def test_latest_batch_is_registered_for_reproduction_and_evolution():
    adapters = {
        "dceo": "2608.25635",
        "transretrieval": "2608.25528",
        "vbvr-pro": "2608.26105",
        "mllmclip": "2608.25575",
    }
    for key, paper_id in adapters.items():
        assert get_adapter(key).paper.arxiv_id == paper_id
    assert INSTALLED_MUTATIONS["2608.25635"][0] == "rankmixer_dceo"
    assert INSTALLED_MUTATIONS["2608.25528"][0] == "rankmixer_transretrieval"
    assert LLM_MUTATIONS["2608.26105"][0] == "multimodal:vbvr-verifier"
    assert LLM_MUTATIONS["2608.25575"][0] == "multimodal:mllmclip-cka"
    for paper_id in ("2608.25580", "2608.25356", "2608.25243", "2608.25583"):
        assert paper_id in POST_TRAINING_MUTATIONS
    for paper_id in (
        "2608.25593", "2608.26086", "2608.25559",
        "2608.25523", "2608.25500", "2608.25992",
    ):
        assert paper_id in AGENT_MUTATIONS
    registry = operator_registry()
    for operator in (
        "rankmixer_dceo", "rankmixer_transretrieval",
        "multimodal:vbvr-verifier", "multimodal:mllmclip-cka",
        "v-rubrics", "clue-opsd", "grin", "grip",
        "planner:jit-agent", "planner:traceml", "tool:adavdr",
        "policy:topas", "memory:caskg", "policy:progrouter",
    ):
        assert operator in registry
