"""The five affordable components do not imply full paper reproduction."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.paper_specs.catalog import catalog_records
from auto_research.reproductions.registry import get_adapter

ROOT = Path(__file__).resolve().parents[1]


def generator():
    spec = importlib.util.spec_from_file_location("oct15_catalogs", ROOT / "scripts/generate_research_catalogs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("key,gpu", (("casi", False), ("pn-mix", True), ("smrc-pmrc", True)))
def test_executable_components_keep_real_gpu_gate_and_no_evolve_promotion(key, gpu):
    adapter = get_adapter(key)
    assert adapter.evaluation_tier.value == "l1_mechanism"
    assert adapter.requires_gpu_validation is gpu
    assert not adapter.evolve_operators
    record = next(row for row in catalog_records() if row["key"] == key)
    assert record["implementation_status"] == "component_only"
    assert record["full_experiment_status"] == "not_reproduced_high_cost"
    text = (ROOT / "docs" / record["detail_path"]).read_text()
    assert "不复现（审查 DONE）" in text
    if gpu:
        assert (ROOT / adapter.gpu_validation_artifact).is_file()
    else:
        assert adapter.device_capabilities == ("cpu",)


@pytest.mark.parametrize("key,domain", (("autoformbench", "agent-research"),
                                        ("jepa-prediction-planning", "foundation-models")))
def test_interfaces_are_visible_but_not_fake_model_adapters(key, domain):
    record = next(row for row in catalog_records() if row["key"] == key)
    assert record["domain"] == domain
    assert record["adapter"] is None
    assert record["implementation_status"] == "evaluation_protocol_interface"
    assert record["requires_gpu_validation"] is False
    for dimension in ("organization", "topic", "year"):
        page = ROOT / "docs" / domain / "catalog" / f"by-{dimension}.md"
        assert record["detail_path"].split("/", 1)[1] in page.read_text()
    assert "CPU 评测接口，不执行模型" in (ROOT / "docs" / domain / "catalog.md").read_text()


def test_unconfirmed_autoformbench_publication_date_stays_unconfirmed():
    module = generator()
    row = next(row for row in module.read_rows("agent-research") if row["key"] == "autoformbench")
    assert row["date"] == row["year"] == "未标注"
    assert module.TOPIC_HIERARCHY["agent-research"][row["topic"]][0] == "工具调用与环境执行"
    page = module.render("agent-research", "year", "Agent 研究：按年份")
    assert page.index("## 2026") < page.index("## 未标注")
    rows = [{"title": "unknown", "date": "未标注"}, {"title": "known", "date": "2026-10-14"}]
    assert module._date_descending(rows)[0]["title"] == "known"


def test_controlled_jepa_input_is_not_reported_as_a_real_environment_or_planner():
    path = ROOT / "docs/foundation-models/2610.19375-jepa-prediction-planning/metrics/controlled-cpu.json"
    result = json.loads(path.read_text())
    assert result["dataset"]["synthetic"] is True
    assert result["diagnostic_only"] and not result["promotion_eligible"]
    assert "planning_comparison" not in result
    assert "planning_noise_floor" not in result
    assert result["fidelity"]["prediction_is_not_planning"] is True
    assert result["fidelity"]["episodes"] == 3


def test_autoformbench_published_receipt_counts_parsing_not_model_success():
    result = json.loads((ROOT / "docs/agent-research/autoformbench/validation/interface-cpu.json").read_text())
    assert result["kind"] == "fixed_release_interface_validation_not_experiment"
    assert result["checks"]["official_rows_parsed"] == 341 * 9
    assert result["checks"]["budget_overrun_rows_retained"] == 1
    assert result["local_capability_score"] is None
    assert not result["lean_verification_performed"] and not result["local_model_inference_performed"]
    assert result["source_condition_of_imported_results"] != result["exported_workspace_condition"]
    assert "metrics" not in result
    assert not {"solve_rate", "answer_accuracy", "plan_success"} & result["checks"].keys()
