"""Independent equation controls, not full-model performance evidence."""

import importlib
import hashlib
import json
import math
from pathlib import Path
import pytest
import torch

from auto_research.foundation_models import counterfactual_wm as cwm
from auto_research.foundation_models import kernel_ridge_attention as kra
from auto_research.foundation_models import loopcache_interface as loopcache
from auto_research.foundation_models import narrow_spec


def test_bilingual_documents_original_assets_and_reviewed_questions():
    root = Path(__file__).resolve().parents[1]
    audit = json.loads(
        (root / "docs/research-audits/nov19-latest/foundation-review.json").read_text()
    )
    bank = json.loads((root / "docs/learning/questions/nov19-latest-foundation.json").read_text())[
        "papers"
    ]
    overlays = json.loads(
        (root / "docs/en/learning/translations/qa-nov19-latest-foundation.json").read_text()
    )["units"]
    assert len(audit["accepted"]) == 5
    for paper in audit["accepted"]:
        directory = root / "docs" / paper["local_detail_path"]
        cn = directory.read_bytes()
        en = (directory.parent / "README-en.md").read_text()
        assert "<!-- source-sha256: " + hashlib.sha256(cn).hexdigest() + " -->" in en
        assert "[简体中文](README.md)" in en
        text = cn.decode()
        for heading in [
            "论文信息",
            "背景与主要改动",
            "核心公式",
            "论文离线与线上效果",
            "同主题比较与边界",
            "高成本完整实验",
        ]:
            assert heading in text
        assert "~~~mermaid" in text and "成本过高，不复现（审查 DONE）" in text
        provenance = json.loads((directory.parent / "assets/provenance.json").read_text())
        asset = directory.parent / "assets/paper-figure-01.png"
        assert provenance["asset_sha256"] == hashlib.sha256(asset.read_bytes()).hexdigest()
        assert provenance["reviewed_version"] == "v1"
        questions = bank[paper["identity"]]["questions"]
        assert {q["level"] for q in questions} == {
            "basics",
            "mechanism",
            "comparison",
            "implementation",
        }
        for q in questions:
            raw = json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            unit = overlays[f"qa/{paper['identity']}/{q['id']}"]
            assert unit["reviewed"] is True
            assert unit["source_sha256"] == hashlib.sha256(raw.encode()).hexdigest()
            assert all(q[h] for h in ("question", "answer", "example"))
            assert all(section in text for section in q["source_sections"])


def test_priority_affiliations_do_not_follow_familiar_author_names():
    root = Path(__file__).resolve().parents[1]
    base = root / "src/auto_research/paper_specs/catalog"
    cwm_spec = json.loads((base / "foundation-models/counterfactual-wm.json").read_text())
    avm_spec = json.loads((base / "multimodal-models/autoregressive-view-model.json").read_text())
    assert cwm_spec["first_author_affiliation"] == "Brown University / AMI Labs"
    assert cwm_spec["verified_priority_organizations"] == []
    assert avm_spec["verified_priority_organizations"] == ["Meta"]
    assert avm_spec["implementation_status"] == "deferred_high_cost"
    assert avm_spec["requires_gpu_validation"] is False
    assert avm_spec["local_operator"] is None
    assert avm_spec["automatic_implementation_queue"] is False


@pytest.fixture(autouse=True)
def single_thread():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


@pytest.mark.parametrize(
    "module,tier",
    [
        ("kernel_ridge_attention", "l1_mechanism"),
        ("narrow_spec", "l1_mechanism"),
        ("counterfactual_wm", "l1_mechanism"),
        ("loopcache_interface", "l0_interface"),
    ],
)
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_checks(module, tier, seed):
    result = importlib.import_module("auto_research.foundation_models." + module).diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == tier
    assert result["checks"] and all(type(v) is bool and v for v in result["checks"].values())
    assert result["metrics"] and all(
        type(v) in (int, float) and math.isfinite(v) for v in result["metrics"].values()
    )


@pytest.mark.parametrize("module", [kra, narrow_spec, cwm, loopcache])
@pytest.mark.parametrize("seed", [True, -1, 0.5])
def test_invalid_seed(module, seed):
    with pytest.raises(ValueError):
        module.diagnostic(seed)


def test_kra_literal_covariance_recovery_and_inclusive_write():
    key = torch.tensor([[1.0, 0.0]], dtype=torch.float64)
    value = torch.tensor([[4.0]], dtype=torch.float64)
    theta = torch.tensor([[2.0], [0.0]], dtype=torch.float64)
    covariance = torch.diag(torch.tensor([0.1, 0.2], dtype=torch.float64))
    out, (new_theta, new_p) = kra.recurrent(
        key, key, value, torch.tensor([math.log(2)], dtype=torch.float64), state=(theta, covariance)
    )
    # delta=.5, predicted P=.25P+.75I, not .25P.
    p = 0.25 * covariance + 0.75 * torch.eye(2, dtype=torch.float64)
    z = p[:, 0]
    expected_theta = 0.5 * theta + z[:, None] / (1 + p[0, 0]) * 3
    assert torch.allclose(new_theta, expected_theta)
    assert torch.allclose(new_p, p - torch.outer(z, z) / (1 + p[0, 0]))
    assert out.item() == pytest.approx(expected_theta[0, 0].item())
    assert out.item() != pytest.approx(1.0)  # read-before-write would be1


def test_kra_covariance_geometry_is_not_scalar_gate():
    key = torch.tensor([[1.0, 1.0]], dtype=torch.float64) / math.sqrt(2)
    p = torch.tensor([[0.4, 0.1], [0.1, 0.2]], dtype=torch.float64)
    _, (theta, _) = kra.recurrent(
        key,
        key,
        torch.ones(1, 1, dtype=torch.float64),
        torch.zeros(1, dtype=torch.float64),
        state=(torch.zeros(2, 1, dtype=torch.float64), p),
    )
    assert not torch.allclose(theta[:, 0] / theta[0, 0], key[0] / key[0, 0])


@pytest.mark.parametrize("ridge", [0.0, -1.0, float("nan"), True])
def test_kra_rejects_bad_ridge(ridge):
    with pytest.raises(ValueError):
        kra.recurrent(torch.ones(2, 2), torch.ones(2, 2), torch.ones(2, 1), torch.ones(2), ridge)


def test_kra_rejects_non_spd_state_and_negative_time():
    args = (torch.ones(2, 2), torch.ones(2, 2), torch.ones(2, 1))
    with pytest.raises(ValueError):
        kra.recurrent(*args, torch.tensor([-1.0, 1.0]))
    with pytest.raises(ValueError):
        kra.recurrent(*args, torch.ones(2), state=(torch.zeros(2, 1), -torch.eye(2)))


def test_narrow_folds_literal_linear_composition_but_not_nonlinearity():
    head = torch.tensor([[1.0, 2.0], [3.0, -1.0]], dtype=torch.float64)
    adapter = torch.tensor([[1.0], [-2.0]], dtype=torch.float64)
    x = torch.tensor([[-1.0]], dtype=torch.float64)
    assert torch.equal(x @ narrow_spec.fold_output_head(head, adapter).T, (x @ adapter.T) @ head.T)
    assert not torch.equal(
        x @ narrow_spec.fold_output_head(head, adapter).T, (x @ adapter.T).relu() @ head.T
    )
    with pytest.raises(ValueError):
        narrow_spec.fold_output_head(head, torch.ones(3, 1, dtype=head.dtype))
    with pytest.raises(ValueError):
        narrow_spec.fold_input_embedding(head, torch.ones(1, 3, dtype=head.dtype))


def test_counterfactual_identity_error_is_action_disturbance_interaction():
    # disturbance is balanced, so factual conditional means really are actions.
    e = torch.tensor([[-0.5], [0.5]], dtype=torch.float64)
    factual, alternative = torch.ones_like(e), 3 * torch.ones_like(e)
    observed, truth = factual * (1 + e), alternative * (1 + e)
    predicted = cwm.residual_reuse(observed, factual, alternative)
    delta = truth - observed
    assert torch.allclose(predicted - truth, delta.mean(0) - delta)
    assert (predicted - truth).square().mean().item() == pytest.approx(1.0)


def test_counterfactual_rejects_broadcast_and_nonfinite():
    with pytest.raises(ValueError):
        cwm.residual_reuse(torch.ones(2, 1), torch.ones(1), torch.ones(2, 1))
    with pytest.raises(ValueError):
        cwm.residual_reuse(torch.tensor([float("nan")]), torch.ones(1), torch.ones(1))


def test_loopcache_policy_has_no_commit_or_future_oracle():
    assert loopcache.update_draft(0, [0.0, 1.0, 0.5], threshold=0.125) == (1, True)
    assert loopcache.update_draft(1, [0.0, 1.0, 0.5], threshold=0.125) == (1, False)
    assert loopcache.next_verification_cycle(5, 4) == 5
    assert (
        loopcache.speculative_cache_loop(1, 3, 2, shallow_layers={1}, gap_threshold=2, loops=4) == 2
    )
    assert loopcache.diagnostic(42)["metrics"]["tokens_committed"] == 0
    with pytest.raises(ValueError):
        loopcache.update_draft(0, [0.0, 1.0], threshold=-1.0)
    with pytest.raises(ValueError):
        loopcache.scheduled_loop(True, 4)
    with pytest.raises(ValueError):
        loopcache.speculative_cache_loop(1, 5, 2, shallow_layers={1}, gap_threshold=1, loops=4)
