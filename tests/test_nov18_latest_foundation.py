"""Mechanism/negative-control tests, never claims of end-to-end paper quality."""

import importlib
import hashlib
import json
import math
from pathlib import Path
import re

import pytest
import torch

from auto_research.foundation_models import cascadejepa, echomoe, fm_mamba, gaugerope, infuseloop
from auto_research.foundation_models import lara_plus_plus, risa, spool, vishead_spec, wm_quant

MODULES = [
    "vishead_spec",
    "spool",
    "infuseloop",
    "echomoe",
    "wm_quant",
    "fm_mamba",
    "lara_plus_plus",
    "gaugerope",
    "risa",
    "cascadejepa",
]


@pytest.fixture(autouse=True)
def small_tensor_threads():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


@pytest.mark.parametrize("module", MODULES)
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_contract_and_nontrivial_controls(module, seed):
    implementation = importlib.import_module("auto_research.foundation_models." + module)
    result = implementation.diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(
        type(value) is bool and value for value in result["checks"].values()
    )
    assert all(
        type(value) in (float, int) and math.isfinite(value) for value in result["metrics"].values()
    )
    assert implementation.REQUIRES_GPU_VALIDATION is True
    assert implementation.GPU_VALIDATION_ARTIFACT.endswith("-a100-20261118-latest.json")


def test_vishead_soft_acceptance_is_not_argmax_agreement():
    logits = torch.tensor([[[2.0, 1.0]]], requires_grad=True)
    target = torch.tensor([[[0.6, 0.4]]], requires_grad=True)
    confidence = torch.tensor([[0.5]], requires_grad=True)
    loss = vishead_spec.drafter_loss(
        logits, target, torch.tensor([[0]]), confidence, torch.tensor([0])
    )
    loss.backward()
    acceptance = 1 - 0.5 * (logits.detach().softmax(-1) - target.detach()).abs().sum(-1)
    assert 0 < acceptance.item() < 1
    assert confidence.grad.item() == pytest.approx(2 - 4 * acceptance.item())
    assert target.grad is None


def test_vishead_preserves_given_context_and_bidirectional_block_mask():
    q = torch.zeros(1, 2, 2, 2)
    k = torch.zeros(1, 1, 4, 2)
    v = torch.arange(4.0).view(1, 1, 4, 1).expand(-1, -1, -1, 2)
    visible = torch.tensor([[False, True, True, True], [False, False, True, True]])
    result = vishead_spec.routed_attention(
        q, k, v, torch.tensor([True, False, False, False]), torch.tensor([False]), visible
    )
    assert torch.equal(result[0, :, 0], torch.full((2, 2), 2.0))
    assert torch.equal(result[0, :, 1], torch.full((2, 2), 2.5))


def test_spool_cached_gdn_transitions_match_literal_update():
    torch.manual_seed(3)
    k = torch.nn.functional.normalize(torch.randn(4, 3, dtype=torch.float64), dim=-1)
    v = torch.randn(4, 2, dtype=k.dtype)
    a = torch.rand(4, dtype=k.dtype)
    b = torch.rand(4, dtype=k.dtype)
    state = torch.randn(2, 3, dtype=k.dtype)
    expected = state.clone()
    for key, value, alpha, beta in zip(k, v, a, b):
        expected = alpha * expected + beta * (value - alpha * (expected @ key))[:, None] @ key[None]
    assert torch.allclose(spool.apply(spool.gdn_summary(k, v, a, b), state), expected, atol=1e-12)
    tree = spool.WindowTree(3, spool.gdn_summary(k, v, a, b))
    assert torch.equal(tree.state(state), state)
    with pytest.raises(ValueError):
        tree.expire()


def test_infuseloop_reads_only_previous_cycle_and_shallower_sources():
    layer = infuseloop.CrossTrajectoryInjection(4, 3)
    bank = torch.randn(4, 8, 3, requires_grad=True)
    output = layer(bank, torch.zeros(8, dtype=torch.long))
    output[3, 1].sum().backward()
    support = bank.grad.abs().sum(-1).nonzero().tolist()
    assert sorted(support) == [[0, 3], [1, 2], [2, 1]]
    # No current loop, later cycle, or source in a different document may enter.
    assert torch.count_nonzero(bank.grad[3]) == 0


def test_wm_quant_ranges_receive_horizon_gradients_but_backbone_does_not():
    model = wm_quant.RolloutCalibrator(3, 3)
    model.objective(torch.randn(4, 3), torch.randn(4, 3, 1)).backward()
    assert model.low.grad is not None and torch.isfinite(model.low.grad).all()
    assert model.log_width.grad is not None and model.log_width.grad.abs().sum() > 0
    assert all(p.grad is None for p in model.predictor.parameters())


@pytest.mark.parametrize("bits", [3, 4, 8])
def test_wm_quant_integer_zero_point_matches_literal_equations(bits):
    low = torch.tensor(-0.3, dtype=torch.float64, requires_grad=True)
    log_width = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    x = torch.tensor(
        [-10.0, -0.3, -0.12, 0.0, 0.12, 0.393, 10.0], dtype=torch.float64, requires_grad=True
    )
    actual = wm_quant.fake_quantize(x, low, log_width, bits)
    scale = (torch.nn.functional.softplus(log_width.detach()) + 1e-6) / (2**bits - 1)
    zero_point = torch.round(-low.detach() / scale)
    integer = torch.clamp(torch.round(x.detach() / scale) + zero_point, 0, 2**bits - 1)
    literal = scale * (integer - zero_point)
    assert torch.equal(actual, literal)
    assert actual[3].item() == 0
    assert actual[0] == -scale * zero_point
    assert actual[-1] == scale * ((2**bits - 1) - zero_point)
    wrong = (
        low.detach()
        + torch.clamp(torch.round((x.detach() - low.detach()) / scale), 0, 2**bits - 1) * scale
    )
    assert not torch.equal(actual, wrong)
    assert wrong[3].item() != 0
    actual.square().sum().backward()
    assert torch.isfinite(x.grad).all()
    assert low.grad is not None and torch.isfinite(low.grad)
    assert log_width.grad is not None and torch.isfinite(log_width.grad)


def test_fm_mamba_rejects_unstable_branches_and_includes_diagonal():
    for invalid in [0.0, 1.0, -2.0]:
        with pytest.raises(ValueError):
            fm_mamba.coefficients(
                torch.tensor([-1.0]),
                torch.tensor([-1.0]),
                torch.tensor([invalid]),
                torch.ones(2, 2),
                torch.ones(2, 2),
            )
    injected = torch.zeros(2, 2, 1)
    injected[0, 0] = 1
    zero = torch.zeros_like(injected)
    diagonal = torch.ones_like(injected)
    result = fm_mamba.scan(injected, zero, zero, diagonal)
    assert result[1, 1].item() == 1


def test_gaugerope_absorption_matches_explicit_approximate_rkv_not_dense():
    torch.manual_seed(7)
    keys, values = (
        torch.randn(20, 2, 4, dtype=torch.float64),
        torch.randn(20, 2, 4, dtype=torch.float64),
    )
    cache = gaugerope.LatentCache.calibrate(keys, values, 1, 5)
    z, code = cache.encode(keys, values)
    query = torch.randn(4, 4, dtype=keys.dtype)
    omega = torch.tensor([0.6, 0.1], dtype=keys.dtype)
    positions = torch.arange(20)
    actual = cache.attention(query, z, code, omega, positions, 20)
    carrier = torch.einsum("nfr,fhr->nhf", z, cache.basis)
    carrier *= torch.exp(1j * (positions - 20)[:, None, None] * omega)
    # RKV deliberately has NO rotary action. Rotating it would change Eq20.
    approximate_k = gaugerope.real_pairs(carrier) + (code @ cache.key_decoder.T).reshape_as(keys)
    approximate_v = (code @ cache.value_decoder.T).reshape_as(values)
    scores = torch.einsum("gd,ngd->gn", query, approximate_k.repeat_interleave(2, 1)) / 2
    expected = torch.einsum("gn,ngd->gd", scores.softmax(-1), approximate_v.repeat_interleave(2, 1))
    assert torch.allclose(actual, expected, atol=1e-10)


def test_risa_plan_uses_max_after_dot_and_joint_softmax():
    keys = torch.tensor([[[10.0, -1.0], [-1.0, 10.0]], [[2.0, 2.0], [3.0, 3.0]]])
    query = torch.tensor([[1.0, -1.0]])
    assert torch.equal(risa.page_scores(query, keys), torch.zeros(2))
    values = torch.tensor([[[0.0, 0.0], [1.0, 1.0]], [[3.0, 3.0], [9.0, 9.0]]])
    plan = torch.tensor([0, 1, 2, 3])
    result = risa.planned_attention(query, keys, values, plan)
    literal = (query @ keys.flatten(0, 1).T / math.sqrt(2)).softmax(-1) @ values.flatten(0, 1)
    assert torch.allclose(result, literal)


def test_lara_author_clustering_and_value_gradient():
    q, k = torch.ones(6, 3), torch.ones(6, 3)
    first, second = lara_plus_plus.cluster_means(q, k, 4)
    assert torch.isfinite(first).all() and torch.isfinite(second).all()
    assert torch.count_nonzero(first[1:]) == 0  # Pinned author's empty-cluster rule.
    values = torch.randn(6, 2, requires_grad=True)
    lara_plus_plus.attention(q, k, values, 3).sum().backward()
    assert values.grad is not None and values.grad.abs().sum() > 0


def test_cascadejepa_ema_and_two_direction_boundaries():
    model = cascadejepa.CascadeJEPA()
    old = [p.clone() for p in model.target.parameters()]
    with torch.no_grad():
        for p in model.context.parameters():
            p.add_(1)
    model.update_target(0.75)
    for before, target in zip(old, model.target.parameters()):
        assert torch.allclose(target, before + 0.25)
        assert target.requires_grad is False


def test_owned_paper_docs_and_reviewed_learning_sources():
    root = Path(__file__).resolve().parents[1]
    review = json.loads(
        (root / "docs/research-audits/nov18-latest/foundation-review.json").read_text()
    )
    questions = json.loads(
        (root / "docs/learning/questions/nov18-latest-foundation.json").read_text()
    )["papers"]
    english = json.loads(
        (root / "docs/en/learning/translations/qa-nov18-latest-foundation.json").read_text()
    )["units"]
    proposals = json.loads(
        (root / "docs/research-audits/nov18-latest/deep-dive-proposals-foundation.json").read_text()
    )["proposals"]
    assert len(review["accepted"]) == len(proposals) == 13
    for row in review["accepted"]:
        path = root / "docs" / row["local_detail_path"]
        cn, en = path.read_text(), path.with_name("README-en.md").read_text()
        fingerprint = hashlib.sha256(path.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {fingerprint} -->" in en
        assert "[简体中文](README.md)" in en
        assert "图片来自[原论文]" in cn and "版权归原作者所有" in cn
        assert not re.search(r"(?m)^\$\$.+", cn)  # Display delimiters occupy their own lines.
        provenance = json.loads((path.parent / "assets/provenance.json").read_text())
        asset = path.parent / "assets/paper-figure-01.png"
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == provenance["asset_sha256"]
        rows = questions[row["identity"]]["questions"]
        assert {q["level"] for q in rows} == {"basics", "mechanism", "comparison", "implementation"}
        for question in rows:
            assert all("### " + section in cn for section in question["source_sections"])
            unit = english[f"qa/{row['identity']}/{question['id']}"]
            expected = hashlib.sha256(
                json.dumps(
                    question, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ).encode()
            ).hexdigest()
            assert unit["source_sha256"] == expected and unit["reviewed"] is True
            assert all(
                value and not re.search(r"[\u3400-\u9fff]", value)
                for value in unit["fields"].values()
            )
        proposal = next(p for p in proposals if p["paper"] == row["identity"])
        assert proposal["source_revisions"][row["identity"]] == fingerprint
