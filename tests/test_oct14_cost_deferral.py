"""Deferred research remains visible without becoming runnable or accepted."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.paper_specs.catalog import catalog_records
from auto_research.paper_specs.runtime import spec_index
from auto_research.reproductions.registry import get_adapter, list_adapters

ROOT = Path(__file__).resolve().parents[1]


def test_mbs_deferral_is_not_an_executable_adapter_or_evolve_operator():
    assert "magicbeanstalk" not in spec_index()
    assert "magicbeanstalk" not in {adapter.key for adapter in list_adapters()}
    with pytest.raises(ValueError, match="unknown paper adapter"):
        get_adapter("magicbeanstalk")
    from auto_research.reproductions.magicbeanstalk import adapter
    with pytest.raises(RuntimeError, match="成本过高，暂不复现"):
        adapter.run(ROOT / "nonexistent-input", 42)
    assert not hasattr(adapter, "ADAPTER")


def test_mbs_catalog_retains_research_and_explicit_pending_evidence():
    row = next(row for row in catalog_records() if row["key"] == "magicbeanstalk")
    assert row["implementation_status"] == "deferred_high_cost"
    assert "成本过高，暂不复现" in row["deferral_reason"]
    assert row.get("adapter") is None
    assert row["local_code"] == "src/auto_research/reproductions/magicbeanstalk"
    assert row["gpu_validation_passed"] is False
    assert (ROOT / "docs" / row["detail_path"]).is_file()
    archive = ROOT / row["deferred_execution_spec"]
    saved = json.loads(archive.read_text())
    assert saved["execution"]["requires_gpu_validation"] is True
    assert not (ROOT / saved["execution"]["gpu_validation_artifact"]).exists()
    assert saved["evolve_operators"] == []
    assert not archive.with_name("paper.yaml").exists()


def test_shared_public_runner_does_not_offer_deferred_mbs():
    spec = importlib.util.spec_from_file_location("cost_gate_runner", ROOT / "scripts/run_oct13_post_training.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert "magicbeanstalk" not in module.METHODS
    assert len(module.METHODS) == 8


def test_generated_browse_and_method_index_expose_deferral():
    spec = importlib.util.spec_from_file_location("cost_gate_catalog", ROOT / "scripts/generate_research_catalogs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for text in (module.render_method_index("post-training", "LLM 后训练"),
                 module.render("post-training", "organization", "按机构"),
                 module.render("post-training", "year", "按年份"),
                 module.render_topic_hierarchy("post-training", "按主题")):
        line = next(line for line in text.splitlines() if "MagicBeanStalk" in line)
        assert "成本过高，暂不复现" in line
        assert "待验收" in line


def test_gpu_gate_is_not_disabled_for_missing_active_receipts():
    spec = importlib.util.spec_from_file_location("cost_gate_gpu", ROOT / "scripts/validate_gpu_evidence.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    from dataclasses import replace
    active = get_adapter("state-opd")
    invalid = replace(active, gpu_validation_artifact="docs/gpu-validations/missing-active-receipt.json")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(module, "list_adapters", lambda: (invalid,))
        assert any("state-opd: GPU validation artifact does not exist" in error for error in module.audit())
