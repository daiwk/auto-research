from __future__ import annotations

from auto_research.evolution.compatibility import (
    operator_registry, validate_operator_set, write_compatibility_graph,
)
from auto_research.evolution.planner import allowed_architectures


def test_registry_covers_all_research_domains():
    registry = operator_registry()
    assert len(registry) >= 150
    assert {spec.domain for spec in registry.values()} >= {
        "recommendation", "foundation-model", "multimodal", "post-training", "agent",
    }


def test_compatibility_rejects_model_slot_and_budget_conflicts():
    assert not validate_operator_set("agent", ["memory:u-mem", "planner:react"])
    assert validate_operator_set("micro-llm", ["memory:u-mem"])
    assert validate_operator_set("post-training", ["dpo", "grpo"])
    assert validate_operator_set("agent", ["memory:u-mem"], max_memory=0)


def test_planner_filters_incompatible_known_operators_and_exports_graph(tmp_path):
    architectures = allowed_architectures("micro-vlm", "", [])
    assert "micro_vlm_qformer" in architectures
    assert "dpo" not in architectures
    payload = write_compatibility_graph(tmp_path / "operators.json").read_text()
    assert '"schema_version": 1' in payload
    assert '"compatible_models"' in payload
