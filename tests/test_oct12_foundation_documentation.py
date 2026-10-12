"""Five-paper metadata and honest-evidence contracts (no GPU receipt fixture)."""
import json
import re
import struct
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "msar": ("2610.13630", "2026-10-09", "foundation-models"),
    "orthros": ("2610.13735", "2026-10-09", "foundation-models"),
    "dualquant": ("2610.13767", "2026-10-09", "foundation-models"),
    "woven": ("2610.12417", "2026-10-08", "multimodal-models"),
    "umrm": ("2610.12707", "2026-10-08", "multimodal-models"),
}


@pytest.mark.parametrize("key", PAPERS)
def test_oct12_five_paper_metadata_figures_and_diagnostic_contract(key):
    identifier, date, domain = PAPERS[key]
    package = ROOT / "src/auto_research/reproductions" / key
    spec = json.loads((package / "paper.yaml").read_text())
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog" / domain / f"{key}.json").read_text())
    directory = ROOT / "docs/reproductions" / f"{identifier}-{key}"
    text = (directory / "README.md").read_text()
    assert spec["arxiv_id"] == identifier and spec["published"] == date
    assert spec["fidelity"] == "core_mechanism" and spec["evaluation_tier"] == "l1_mechanism"
    assert spec["execution"]["requires_gpu_validation"] is True
    assert catalog["gpu_validation_artifact"] == spec["execution"]["gpu_validation_artifact"]
    assert spec["evolve_operators"] == []
    for required in ("## 论文信息", f"[arXiv {identifier}](https://arxiv.org/abs/{identifier})",
                     "| 公司/机构 |", f"| 首次公开日期 | {date}（arXiv v1） |",
                     "| 原文开源代码 |", f"| Adapter | `{key}` |",
                     f"src/auto_research/reproductions/{key}/", "## 原始论文总结",
                     "### 核心公式", "### 论文离线与线上效果", "## 本地复现",
                     "```mermaid", "版权归原作者所有", "metrics/protocol.json"):
        assert required in text
    assert re.search(r"^\| 原文开源代码 \| (?:是：\[[^]]+\]\(https?://[^)]+\)|否：[^|]+) \|$", text, re.M)
    image = (directory / "assets/paper-figure-01.png").read_bytes()
    assert image.startswith(b"\x89PNG\r\n\x1a\n") and len(image) > 5000
    width, height = struct.unpack(">II", image[16:24])
    assert width >= 400 and height >= 140
    protocol = json.loads((directory / "metrics/protocol.json").read_text())
    assert protocol["diagnostic_only"] is True
    assert "paper_results" not in protocol and "paper_reported" not in protocol
    assert "线上 A/B：未报告" in text


def test_oct12_sources_are_hash_verified_and_test_selection_is_separate():
    reward = (ROOT / "src/auto_research/multimodal/oct12_reward_transition.py").read_text()
    assert 'for name in ("train", "validation"):' in reward
    assert reward.index('selected = select_probe_layer(validation)') < reward.index(
        'features["test"] = extract_split("test", [selected])')
    for key in ("msar", "orthros", "dualquant", "woven", "umrm"):
        assert (ROOT / f"src/auto_research/reproductions/{key}/adapter.py").is_file()
