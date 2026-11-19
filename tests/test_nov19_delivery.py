"""Finite intake closure, reviewed bilingual learning and actual device evidence."""

import hashlib
import json
from pathlib import Path

from close_nov19_latest_intake import learning_counts
from run_nov19_latest_components import config, source_hashes, validate_raw

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov19-latest"


def load(path):
    return json.loads(path.read_text())


def test_fixed_scope_not_metadata_backlog_or_watermark_advance():
    scope = load(AUDIT / "task-scope.json")
    assert scope["selected_scope_complete"] and scope["delivery_status"] == "fixed_scope_complete"
    assert not scope["watermark_advanced"] and not scope["all_sources_exhaustive"]
    assert len(scope["accepted_papers"]) == 20
    assert len(scope["component_papers"]) == 17 and len(scope["review_only_papers"]) == 3
    assert len(scope["new_papers"]) == 18
    assert scope["historical_directory_backfill"] == ["agent-research:searchinject"]
    assert scope["announcement_overlap_backfill"] == ["multimodal-models:autoregressive-view-model"]
    assert scope["counts"]["full_capability_reproductions"] == 0
    metadata = load(AUDIT / "metadata-index.json")
    assert (
        metadata["metadata_only"] and not metadata["metadata_inventory_is_implementation_backlog"]
    )


def test_frozen_cpu_and_actual_nvidia_runs_remain_source_bound():
    frozen = load(AUDIT / "frozen-sources.json")
    assert source_hashes() == frozen["source_sha256"]
    for device in ("cpu", "cuda"):
        raw = load(AUDIT / f"raw-{device}.json")
        validate_raw(raw, frozen)
        assert raw["code_commit"] == frozen["commit"]
        assert raw["full_experiments_executed"] is False
        assert raw["pretrained_model_calls"] == raw["api_calls"] == 0
    assert len(load(AUDIT / "raw-cpu.json")["components"]) == 17
    assert len(load(AUDIT / "raw-cuda.json")["components"]) == 7


def test_twenty_papers_have_complete_metadata_reviewed_english_and_figures():
    scope = load(AUDIT / "task-scope.json")
    for p in scope["papers"]:
        page = ROOT / "docs" / p["detail_path"]
        cn = page.read_text()
        assert all(
            label in cn for label in ("论文信息", "首次公开日期", "本地", "核心公式", "不复现")
        )
        assert any(
            f"| {label} |" in cn
            for label in (
                "原作者代码",
                "原作者开源代码",
                "原文开源代码",
                "原作者代码 / 权重",
                "原文是否开源",
            )
        )
        assert p["published"] in cn
        assert (
            "<!-- source-sha256: " + hashlib.sha256(page.read_bytes()).hexdigest() + " -->"
            in page.with_name("README-en.md").read_text()
        )
        assert (page.parent / "assets/paper-figure-01.png").stat().st_size > 1000
        assert "<!-- paper-figure:start -->" in cn and "版权归原作者所有" in cn
        if not p["component_implemented"]:
            assert p["status"] == "deferred" and p["resolution"] == "not_reproduced_high_cost"
            assert not p.get("local_operator") and not (page.parent / "metrics").exists()
        elif p["requires_gpu_validation"]:
            receipt = load(ROOT / p["gpu_validation_artifact"])
            assert receipt["adapter_key"] == p["key"] and receipt["result"] == "passed"
            assert receipt["seeds"] == [42, 43, 44]
            assert receipt["validated_at"] == "2026-11-19"


def test_all_four_learning_levels_and_same_topic_updates_are_reviewed():
    expected = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    assert learning_counts(expected) == {
        "authored_bilingual_questions": 80,
        "same_topic_deep_dive_updates": 20,
    }
    assert sum(p["cuda"] for p in config()["components"].values()) == 7


def test_priority_affiliation_and_date_boundaries_are_explicit():
    reviews = load(AUDIT / "priority-primary-selection.json")
    assert set(reviews["priority_admissions"]) == {
        "recommendation:mle-agents",
        "multimodal-models:autoregressive-view-model",
        "agent-research:searchinject",
    }
    assert "Brown/AMI" in reviews["affiliation_corrections"]["foundation-models:counterfactual-wm"]
    assert len(reviews["primary_source_exclusions"]) == 2
