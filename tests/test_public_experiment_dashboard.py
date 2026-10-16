from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_seedless_deterministic_audits_are_labeled_without_inventing_seeds():
    from scripts.generate_public_experiment_dashboard import _seed

    payload = {"deterministic": True, "evaluation_protocol": {"seeds": []}}
    assert _seed("", payload, "audit.json") == "不适用（确定性审计）"
    assert _seed("", {"evaluation_protocol": {"seeds": []}}, "audit.json") == ""
    assert _seed("", {"deterministic": True}, "audit.json") == ""
    assert _seed("", {"evaluation_protocol": {"seeds": [42, 43, 44]}}, "audit.json") == "42, 43, 44"


def test_dashboard_dataset_label_does_not_dump_revision_manifest():
    from scripts.generate_public_experiment_dashboard import _dataset_name

    source = {"dataset": {"id": "WikiText-2", "revision": {"train": "a" * 64}}}
    assert _dataset_name(str(source['dataset']), source) == 'WikiText-2'
    assert _dataset_name('', {'dataset': {'name': 'CIFAR-10'}}) == 'CIFAR-10'
    assert _dataset_name('', {'dataset': {'public_id': 'xiaowu0162/longmemeval-cleaned',
                                         'revision': 'fixed-revision'}}) == 'xiaowu0162/longmemeval-cleaned'
    assert _dataset_name('raw manifest', {'dataset': {'source_id': 'openai/grade-school-math',
                                                     'source_revision': 'fixed'}}) == 'openai/grade-school-math'
    assert _dataset_name('legacy-dataset', {}) == 'legacy-dataset'
    assert _dataset_name('', {'benchmark': 'public-benchmark'}) == 'public-benchmark'


def test_explicit_diagnostic_flags_override_formal_labels():
    from scripts.generate_public_experiment_dashboard import _agent_evidence

    evidence = _agent_evidence({"training": {"diagnostic_only": True},
                               "evaluation_protocol": {"tier": "l2_capability", "formal_comparison": True}}, {})
    assert evidence["diagnostic_only"] and evidence["formal_comparison"] is False
    assert evidence["tier"].startswith("l1_")
    assert not _agent_evidence({"dataset": {"id": "public-dataset"}}, {})["diagnostic_only"]


def test_dataset_label_reads_declared_live_agent_protocol_without_inventing_metadata():
    from scripts.generate_public_experiment_dashboard import _dataset_name

    source = {"evaluation_protocol": {"protocol": {"dataset": {
        "public_id": "openai/grade-school-math", "revision": "fixed",
        "source_split": "train", "official_test_opened": False}}}}
    assert _dataset_name("", source) == "openai/grade-school-math"
    assert _dataset_name("legacy", {"evaluation_protocol": {"protocol": "invalid"}}) == "legacy"
    assert _dataset_name("", {"evaluation_protocol": {"protocol": {"dataset": {"revision": "fixed"}}}}) == ""


def test_public_dashboard_contains_only_committed_documentation_metrics():
    payload = json.loads(
        (ROOT / "docs/assets/data/experiment-dashboard.json").read_text(encoding="utf-8")
    )
    experiments = payload["experiments"]

    assert payload["schema_version"] == 2
    assert payload["artifact_count"] == len(experiments)
    assert payload["indexed_artifact_count"] == (
        payload["artifact_count"] + payload["unmeasured_artifact_count"]
    )
    assert len(experiments) >= 300
    assert all(item["path"].startswith("docs/") for item in experiments)
    assert all(item["method"] != "metrics" for item in experiments)
    assert all(item["metrics"] for item in experiments)
    assert any(item["domain"] == "foundation-model" for item in experiments)
    assert any(item["domain"] == "system-one" for item in experiments)
    assert any(item["title"] for item in experiments)


def test_boolean_only_implementation_contracts_remain_auditable_not_result_cards():
    from scripts.generate_public_experiment_dashboard import build_payload

    payload = build_payload()
    displayed = {item["path"] for item in payload["experiments"]}
    contracts = list((ROOT / "docs").glob("**/metrics/implementation-contract.json"))
    unmeasured = [path for path in contracts
                  if all(isinstance(value, bool)
                         for value in json.loads(path.read_text())["metrics"].values())]
    assert unmeasured
    assert all(path.relative_to(ROOT).as_posix() not in displayed for path in unmeasured)
    assert payload["unmeasured_artifact_count"] >= len(unmeasured)


def test_resumed_gpu_cards_show_measured_scores_with_explicit_diagnostic_protocols():
    payload = json.loads((ROOT / "docs/assets/data/experiment-dashboard.json").read_text())
    filenames = {
        "oal": "a100-three-seeds-4496283a.json",
        "near": "a30-diagnostics-34148c2e.json",
        "beyond-final-embedding": "a30-diagnostics-34148c2e.json",
    }
    for method, filename in filenames.items():
        items = [item for item in payload["experiments"]
                 if item["method"] == method and item["path"].endswith("/" + filename)]
        assert len(items) == 1
        item = items[0]
        assert item["dataset"] and all(str(seed) in item["seed"] for seed in (42, 43, 44))
        assert item["metrics"] and "schema_version" not in item["metrics"]
        assert item["evidence"]["diagnostic_only"]
        assert not item["evidence"]["formal_comparison"]
        assert any("test" in key and ("ppl" in key or "ndcg" in key)
                   for key in item["metrics"])


def test_sguid_dashboard_keeps_negative_validation_and_mechanism_tier():
    payload = json.loads((ROOT / "docs/assets/data/experiment-dashboard.json").read_text())
    items = [item for item in payload["experiments"] if item["method"] == "sguid"]
    assert len(items) == 1
    item = items[0]
    assert item["domain"] == "post-training"
    assert item["dataset"] == "openai/grade-school-math"
    assert item["seed"] == "42"
    assert item["metrics"]["completed_rounds"] == 2
    assert item["metrics"]["baseline_validation_exact_match"] == .75
    assert item["metrics"]["final_validation_exact_match"] == .25
    assert item["metrics"]["validation_exact_match_delta"] == -.5
    assert item["evidence"]["diagnostic_only"] is True
    assert item["evidence"]["formal_comparison"] is False
    assert item["evidence"]["tier"] == "l1_mechanism"
    script = (ROOT / "docs/assets/javascripts/experiment-dashboard.js").read_text()
    # Suppress saturated Agent fixture scores, not measured non-Agent smoke
    # comparisons such as SGUID's negative validation delta.
    assert 'const agentDiagnostic = diagnostic && item.domain === "agent";' in script
    assert "const primary = agentDiagnostic" in script


def test_agent_mechanism_results_are_not_presented_as_capability_scores():
    payload = json.loads(
        (ROOT / "docs/assets/data/experiment-dashboard.json").read_text(encoding="utf-8")
    )
    agents = [item for item in payload["experiments"] if item["domain"] == "agent"]
    diagnostics = [
        item for item in agents if item.get("evidence", {}).get("diagnostic_only")
    ]

    assert diagnostics
    assert all(item["dataset"] and item["seed"] for item in diagnostics)
    assert all(item["evidence"]["tier"].startswith("l1_") for item in diagnostics)
    assert all(item["evidence"]["formal_comparison"] is False for item in diagnostics)
    assert all(
        item["evidence"]["capability_metrics_saturated"]
        for item in diagnostics
        if all(
            item["metrics"].get(metric) == 1.0
            for metric in ("answer_accuracy", "plan_success", "joint_success")
        )
    )

    capabilities = [
        item for item in agents
        if item.get("evidence", {}).get("tier") == "l2_capability"
    ]
    assert len(capabilities) >= 7
    assert all(not item["evidence"]["diagnostic_only"] for item in capabilities)
    # Historical capability measurements remain available, but an old boolean
    # is not a substitute for the now-required versioned comparison contract.
    assert all(item["evidence"]["formal_comparison"] is False for item in capabilities)
    assert all("comparison_contract_missing" in item["evidence"]["eligibility_reasons"] for item in capabilities)
    assert all(item["dataset"] == "toolroute-l2.1-v1" for item in capabilities)
    assert any(item["method"] == "agent-evolve" for item in capabilities)


def test_agentx_replay_dashboard_shows_measured_summary_not_schema_version():
    payload = json.loads(
        (ROOT / "docs/assets/data/experiment-dashboard.json").read_text(encoding="utf-8")
    )
    items = [item for item in payload["experiments"]
             if item["method"] == "agentx-model-replay"]
    assert len(items) == 1
    item = items[0]
    assert item["evidence"]["tier"] == "l1_mechanism_diagnostic"
    assert item["evidence"]["formal_comparison"] is False
    assert "fixed_best_validation_auc_mean" in item["metrics"]
    assert "diagnose_pcoc_absolute_error_after_mean" in item["metrics"]
    assert "schema_version" not in item["metrics"]


def test_public_dashboard_page_uses_card_layout_and_progressive_disclosure():
    page = (ROOT / "docs/public-experiment-dashboard.md").read_text(encoding="utf-8")
    script = (ROOT / "docs/assets/javascripts/experiment-dashboard.js").read_text(
        encoding="utf-8"
    )
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert 'class="ar-dashboard"' in page
    assert "查看全部" in script
    assert "slice(0, 6)" in script
    assert "L1 机制诊断" in script
    assert "非正式能力比较" in script
    assert "三个 success=1 只表示机制合约通过" in script
    assert "L2.1 隔离能力评测" in script
    assert "三 seed 正式比较" in script
    assert "公开实验看板: public-experiment-dashboard.md" in navigation
    assert "2026 历史论文扫描:" not in navigation
    assert "历史扫描清单与实现批次:" not in navigation
    assert "统一后续路线图与 TODO:" not in navigation
