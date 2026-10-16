"""Accepted twelve components: executed evidence, source binding and honest scope."""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

import pytest

from auto_research.gpu_validation import load_gpu_receipt
from auto_research.paper_specs.catalog import catalog_records

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = {
    "drop-kv", "mirror-moe", "bit-sparse", "lct", "roleq",
    "shared-residual-distillation", "progress-reward", "elite-replay", "clean-rm",
    "shortcut-sensitivity", "disagreement-routing", "tracer",
}
GPU = COMPONENTS - {"shortcut-sensitivity", "disagreement-routing", "tracer"}


def records():
    return {row["key"]: row for row in catalog_records() if row["key"] in COMPONENTS | {"hardware-diversity"}}


def test_all_twelve_and_system_reference_are_present_without_capability_promotion():
    rows = records()
    assert set(rows) == COMPONENTS | {"hardware-diversity"}
    for key, row in rows.items():
        assert row["adapter"] is None, key
        assert row["full_experiment_status"] == "not_reproduced_high_cost", key
        assert row["promotion_eligible"] is False and row["evolve_integrated"] is False, key
        assert row["first_author_affiliation"] and row["published"], key
        if not row.get("code"):
            assert "未" in row.get("code_status", ""), key
        page = ROOT / "docs" / row["detail_path"]
        text = page.read_text()
        for token in ("## 论文信息", "## 原始论文总结", "### 核心公式", "## 本地复现",
                      "不复现", "DONE", "assets/paper-figure-01.png"):
            assert token in text, (key, token)
        if key in COMPONENTS:
            assert row["implementation_status"] == "component_only", key
            module, name = row["local_operator"].rsplit(".", 1)
            assert callable(getattr(importlib.import_module(module), name)), key
            assert row["local_command"] and row["diagnostic_only"] is True, key
        else:
            assert row["implementation_status"] == "deferred_high_cost"
            assert not row.get("local_operator")
            assert "不是线上 A/B" in row["deferral_reason"]


@pytest.mark.parametrize("key", sorted(GPU))
def test_cuda_components_bind_current_executed_sources_and_real_device(key):
    row = records()[key]
    assert row["requires_gpu_validation"] is True
    artifact = row["gpu_validation_artifact"]
    receipt = load_gpu_receipt(ROOT / artifact)
    assert receipt["adapter_key"] == key
    assert receipt["seeds"] == [42, 43, 44]
    assert any(name in receipt["accelerator"]["model"].upper() for name in ("A100", "A30"))
    assert receipt["provenance"]["artifact_path"] == artifact
    assert receipt["diagnostic_only"] is True and receipt["promotion_eligible"] is False
    assert receipt["full_experiment_status"] == "not_reproduced_high_cost"
    hashes = receipt["executed_source_sha256"]
    assert any(name.startswith("src/") for name in hashes)
    assert any(name.startswith("scripts/") for name in hashes)
    for name, digest in hashes.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, (key, name)
    metric = json.loads((ROOT / receipt["provenance"]["metric_artifact_path"]).read_text())
    assert metric["metrics"] == receipt["metrics"]
    assert metric["diagnostic_only"] is True
    assert metric["evaluation_protocol"]["formal_comparison"] is False
    assert metric["evaluation_protocol"]["seeds"] == [42, 43, 44]


def test_cpu_audits_have_per_paper_metrics_but_no_fake_cuda_receipts():
    rows = records()
    for key in COMPONENTS - GPU:
        row = rows[key]
        assert row["requires_gpu_validation"] is False
        assert not row.get("gpu_validation_artifact")
        metrics = list((ROOT / "docs" / row["detail_path"]).parent.glob("metrics/*.json"))
        assert metrics, key
        for path in metrics:
            artifact = json.loads(path.read_text())
            assert artifact["diagnostic_only"] is True
            assert artifact["promotion_eligible"] is False
            assert artifact["evaluation_protocol"]["formal_comparison"] is False
            assert artifact["evaluation_protocol"]["seeds"] == [42, 43, 44]


def test_all_thirteen_are_linked_once_in_each_domain_browse_dimension():
    for key, row in records().items():
        expected = (ROOT / "docs" / row["detail_path"]).resolve()
        for dimension in ("organization", "topic", "year"):
            path = ROOT / "docs" / row["domain"] / "catalog" / f"by-{dimension}.md"
            links = re.findall(r"\]\(([^)]+)\)", path.read_text())
            assert sum((path.parent / link).resolve() == expected for link in links) == 1, (key, dimension)
    index = (ROOT / "docs/foundation-models/catalog.md").read_text()
    system_row = next(line for line in index.splitlines() if "2610.22230-hardware-diversity" in line)
    assert "审查 DONE" in system_row and "待验收" not in system_row


def test_upstream_code_urls_do_not_embed_license_text():
    for key, row in records().items():
        code = row.get("code") or ""
        if code.startswith("http"):
            assert not any(character.isspace() for character in code), key
            assert urlsplit(code).scheme == "https" and urlsplit(code).netloc, key
    post = (ROOT / "docs/post-training/catalog.md").read_text()
    clean_row = next(line for line in post.splitlines() if "2610.21138-clean-rm" in line)
    assert "本轮访问失败" in clean_row and "[已开源]" not in clean_row
