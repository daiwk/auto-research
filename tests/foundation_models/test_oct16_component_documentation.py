import hashlib
import json
from pathlib import Path
import runpy
import struct
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
PAPERS = {
    "novelty-patching": ("2610.22100", "2026-10-15T15:47:08Z", "component-cpu.json"),
    "rope-relay": ("2610.21126", "2026-10-15T02:30:27Z", "component-cpu-seeds42-44.json"),
    "cots": ("2610.20642", "2026-10-08T02:47:16Z", "component-cpu-seeds42-44.json"),
}


@pytest.mark.parametrize("key", PAPERS)
def test_paper_metadata_measured_schema_and_original_figure_are_complete(key):
    identifier, published, metric_name = PAPERS[key]
    directory = ROOT / "docs/foundation-models" / f"{identifier}-{key}"
    readme = (directory / "README.md").read_text()
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog/foundation-models" / f"{key}.json").read_text())
    metric = json.loads((directory / "metrics" / metric_name).read_text())
    assert catalog["published_at"] == published and catalog["published"] == published[:10]
    assert catalog["adapter"] is None and catalog["evolve_integrated"] is False
    assert catalog["implementation_status"] == "component_only"
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost"
    for phrase in ("## 论文信息", "| 公司/机构 |", "| 原文开源代码 |", "| 首次公开日期 |",
                   published, f"[arXiv {identifier}](https://arxiv.org/abs/{identifier})", f"`{key}`",
                   "## 原始论文总结", "### 核心公式", "### 论文离线与线上效果", "## 本地复现",
                   "```mermaid", "线上 A/B：未报告", "版权归原作者所有", f"metrics/{metric_name}",
                   "成本过高，不复现（审查 DONE）"):
        assert phrase in readme
    image = (directory / "assets/paper-figure-01.png").read_bytes()
    assert image.startswith(b"\x89PNG\r\n\x1a\n") and len(image) > 5000
    width, height = struct.unpack(">II", image[16:24])
    assert width >= 400 and height >= 140
    assert metric["schema_version"] == 2 and metric["measured_locally"] is True and metric["metrics"]
    assert metric["diagnostic_only"] is True and metric["promotion_eligible"] is False
    assert metric["evaluation_protocol"]["formal_comparison"] is False
    assert metric["manifest_ref"] == f"foundation-models:{key}"
    assert metric["adapter"] is None and metric["full_experiment"]["review_done"] is True
    module = ROOT / "src/auto_research/foundation_models" / (key.replace("-", "_") + ".py")
    assert metric["provenance"]["implementation_sha256"] == hashlib.sha256(module.read_bytes()).hexdigest()
    if key == "novelty-patching":
        assert metric["deterministic"] and not metric["seeds"]
        assert not metric["dataset"]["validation_used_for_threshold"] and not metric["dataset"]["test_read"]


def test_runner_actual_call_outputs_measured_diagnostic_and_rejects_overwrite(tmp_path, monkeypatch):
    pytest.importorskip("torch")
    module = runpy.run_path(str(ROOT / "scripts/run_oct16_foundation_components.py"))
    output = tmp_path / "result.json"
    arguments = ["runner", "--papers", "cots", "--seeds", "42", "--device", "cpu", "--output", str(output)]
    monkeypatch.setattr(sys, "argv", arguments)
    assert module["main"]() == 0
    measured = json.loads(output.read_text())
    assert measured["diagnostic_only"] and not measured["promotion_eligible"]
    assert measured["metrics"]["phase_lock_and_protection_correct"] is True
    original = output.read_bytes()
    with pytest.raises(SystemExit):
        module["main"]()
    assert output.read_bytes() == original


def test_runner_requires_public_corpus_hash_and_cannot_read_oversized_inputs(tmp_path, monkeypatch):
    pytest.importorskip("torch")
    module = runpy.run_path(str(ROOT / "scripts/run_oct16_foundation_components.py"))
    corpus = tmp_path / "train.txt"
    corpus.write_bytes(b"public training bytes")
    output = tmp_path / "result.json"
    monkeypatch.setattr(sys, "argv", ["runner", "--papers", "novelty-patching", "--corpus-path", str(corpus),
                         "--corpus-sha256", "bad", "--corpus-id", "public", "--corpus-revision", "pinned",
                         "--output", str(output)])
    with pytest.raises(ValueError, match="SHA-256"):
        module["main"]()
    assert not output.exists()
    with corpus.open("wb") as handle:
        handle.truncate(16_000_001)
    with pytest.raises(ValueError, match="16 MB"):
        module["main"]()


def test_runner_controlled_source_export_commit_is_validated_and_avoids_git(tmp_path, monkeypatch):
    pytest.importorskip("torch")
    module = runpy.run_path(str(ROOT / "scripts/run_oct16_foundation_components.py"))
    output = tmp_path / "result.json"
    args = ["runner", "--papers", "cots", "--seeds", "42", "--output", str(output), "--code-commit"]
    monkeypatch.setattr(sys, "argv", args + ["not-a-commit"])
    with pytest.raises(SystemExit):
        module["main"]()
    assert not output.exists()
    def forbidden_git(*_args, **_kwargs):
        raise AssertionError("a controlled source export must not require a Git checkout")
    monkeypatch.setattr(module["subprocess"], "check_output", forbidden_git)
    monkeypatch.setattr(sys, "argv", args + ["A" * 40])
    assert module["main"]() == 0
    assert json.loads(output.read_text())["provenance"]["code_commit"] == "a" * 40
