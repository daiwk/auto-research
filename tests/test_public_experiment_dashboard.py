from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_dashboard_contains_only_committed_documentation_metrics():
    payload = json.loads(
        (ROOT / "docs/assets/data/experiment-dashboard.json").read_text(encoding="utf-8")
    )
    experiments = payload["experiments"]

    assert payload["schema_version"] == 1
    assert payload["artifact_count"] == len(experiments)
    assert len(experiments) >= 300
    assert all(item["path"].startswith("docs/") for item in experiments)
    assert all(item["method"] != "metrics" for item in experiments)
    assert all(item["metrics"] for item in experiments)
    assert any(item["domain"] == "foundation-model" for item in experiments)
    assert any(item["title"] for item in experiments)


def test_public_dashboard_page_uses_card_layout_and_progressive_disclosure():
    page = (ROOT / "docs/public-experiment-dashboard.md").read_text(encoding="utf-8")
    script = (ROOT / "docs/assets/javascripts/experiment-dashboard.js").read_text(
        encoding="utf-8"
    )
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert 'class="ar-dashboard"' in page
    assert "查看全部" in script
    assert "slice(0, 6)" in script
    assert "公开实验看板: public-experiment-dashboard.md" in navigation
    assert "2026 历史论文扫描:" not in navigation
    assert "历史扫描清单与实现批次:" not in navigation
    assert "统一后续路线图与 TODO:" not in navigation
