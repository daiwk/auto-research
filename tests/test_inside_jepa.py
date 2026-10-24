"""Independent equations/masking/gradient contracts; not a video benchmark."""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path

import pytest
import torch
from torch import nn
from torch.nn import functional as F

from auto_research.foundation_models.inside_jepa import (
    ARMS, InsideJEPA, RelationalStateEncoder, box_fourier_features, diagnostic,
)


class TestInverse(nn.Module):
    __test__ = False

    def __init__(self, width, outputs=4):
        super().__init__()
        self.layer = nn.Linear(2 * width, outputs)

    def forward(self, current, future):
        return self.layer(torch.cat((current, future), -1))


def fixture(arm="INV-S", *, continuous=False, conditioned=True, channels=8):
    torch.manual_seed(19)
    encoder = RelationalStateEncoder(nn.Linear(36, 128), nn.GELU(), channels=channels)
    width = 4 * 4 * channels if arm in ("INV-S", "INV-SHUF") else (128 if arm == "INV-R" else encoder.state_dimension)
    model = InsideJEPA(encoder, arm=arm, action_size=4,
                       inverse_head=None if arm == "PRED" else TestInverse(width),
                       continuous_actions=continuous, action_conditioned=conditioned)
    feature = torch.randn(4, 4, 512, requires_grad=True)
    xy = torch.rand(4, 4, 2) * .5
    boxes = torch.cat((xy, xy + .3), -1)
    valid = torch.tensor([[1, 1, 1, 0]] * 4, dtype=torch.bool)
    kinds = torch.tensor([[0, 1, 0, 0]] * 4)
    start = dict(features=feature, boxes=boxes, valid=valid, entity_types=kinds)
    future = {**start, "features": torch.randn(4, 4, 512, requires_grad=True), "boxes": boxes + .1}
    actions = torch.randn(4, 4) if continuous else torch.arange(4)
    return model, start, future, actions


def test_fourier_coordinates_use_pi_and_raw_coordinates_not_2pi():
    boxes = torch.tensor([[[0., .125, .5, 1.]]], dtype=torch.float64)
    actual = box_fourier_features(boxes)
    expected = list(boxes.flatten())
    for operation in (math.sin, math.cos):
        expected += [operation(2 ** k * math.pi * coordinate)
                     for coordinate in (0., .125, .5, 1.) for k in range(4)]
    torch.testing.assert_close(actual.flatten(), torch.tensor(expected, dtype=torch.float64))
    assert actual.shape == (1, 1, 36)


@pytest.mark.parametrize("channels,dimension", [(8, 256), (16, 384)])
def test_exact_state_shape_pair_formula_ordering_and_padding(channels, dimension):
    model, start, _, _ = fixture(channels=channels)
    encoder = model.encoder
    state = encoder(**start)
    assert state.z.shape == (4, dimension)
    e = encoder.entity_norm(encoder.appearance(start["features"].detach())
                            + encoder.box_mlp(box_fourier_features(start["boxes"]))
                            + encoder.entity_type(start["entity_types"]))
    expected = encoder.relation(torch.cat((e[:, 0], e[:, 1], e[:, 0] - e[:, 1],
                                           e[:, 0] * e[:, 1]), -1)).sigmoid()
    torch.testing.assert_close(state.s[:, 0, 1], expected)
    assert not torch.allclose(state.s[:, 0, 1], state.s[:, 1, 0])
    assert (state.r[:, 3] == 0).all()
    assert (state.s[:, 3] == 0).all() and (state.s[:, :, 3] == 0).all()
    index = torch.arange(4)
    assert (state.s[:, index, index] == 0).all()
    # Padded appearance/box/type values cannot affect valid pair entries.
    other = {k: v.detach().clone() for k, v in start.items()}
    other["features"][:, 3] += 100
    other["boxes"][:, 3] = torch.tensor([0., 0., 1., 1.])
    other["entity_types"][:, 3] = 1
    torch.testing.assert_close(encoder(**other).z, state.z)


@pytest.mark.parametrize("arm", ARMS)
def test_five_arms_losses_match_independent_formulas_and_route_future_online(arm):
    model, start, future, actions = fixture(arm)
    permutation = torch.tensor([1, 2, 3, 0]) if arm == "INV-SHUF" else None
    result = model.losses(start, future, actions, inverse_permutation=permutation)
    current = model.encoder(**start)
    with torch.no_grad():
        target = model.target_encoder(**future).z
    expected_forward = ((model.predict(current, actions) - target) ** 2).sum(1).mean()
    torch.testing.assert_close(result["forward"], expected_forward)
    if arm == "PRED":
        assert result["inverse"] == 0
    else:
        later = model.encoder(**future)
        expected_logits = model.inverse_head(model.inverse_inputs(current), model.inverse_inputs(later))
        targets = actions if permutation is None else actions[permutation]
        torch.testing.assert_close(result["inverse"], F.cross_entropy(expected_logits, targets))
        grads = torch.autograd.grad(result["inverse"], tuple(model.encoder.relation.parameters()),
                                    allow_unused=True, retain_graph=True)
        assert any(g is not None and g.abs().sum() > 0 for g in grads) == (arm != "INV-R")
    torch.testing.assert_close(result["loss"], result["forward"] + result["inverse"])
    result["loss"].backward()
    assert start["features"].grad is None and future["features"].grad is None
    assert all(p.grad is None and not p.requires_grad for p in model.target_encoder.parameters())


def test_inverse_reaches_both_online_frames_not_detached_or_target_future():
    model, start, future, actions = fixture()
    current = model.encoder(**start)
    later = model.encoder(**future)
    loss = F.cross_entropy(model.inverse_head(current.s.flatten(1), later.s.flatten(1)), actions)
    g_current, g_future = torch.autograd.grad(loss, (current.s, later.s))
    assert g_current.norm() > 0 and g_future.norm() > 0
    # Separate frame inputs allow verifying online future box-encoder gradients.
    future["boxes"] = future["boxes"].clone().requires_grad_()
    start["boxes"] = start["boxes"].clone().requires_grad_()
    result = model.losses(start, future, actions)
    gc, gf = torch.autograd.grad(result["inverse"], (start["boxes"], future["boxes"]))
    assert gc.norm() > 0 and gf.norm() > 0


def test_shuffled_targets_never_replace_true_forward_action():
    original, start, future, actions = fixture("INV-S")
    shuffled = deepcopy(original)
    shuffled.arm = "INV-SHUF"
    permutation = torch.tensor([2, 3, 0, 1])
    real = original.losses(start, future, actions)
    fake = shuffled.losses(start, future, actions, inverse_permutation=permutation)
    torch.testing.assert_close(fake["forward"], real["forward"])
    assert not torch.allclose(fake["inverse"], real["inverse"])
    altered = original.losses(start, future, actions[permutation])
    assert not torch.allclose(fake["forward"], altered["forward"])


@pytest.mark.parametrize("conditioned", [True, False])
def test_continuous_control_uses_squared_l2_and_optional_action_conditioning(conditioned):
    model, start, future, actions = fixture(continuous=True, conditioned=conditioned)
    result = model.losses(start, future, actions)
    current, later = model.encoder(**start), model.encoder(**future)
    output = model.inverse_head(current.s.flatten(1), later.s.flatten(1))
    torch.testing.assert_close(result["inverse"], (output - actions).square().sum(1).mean())
    if not conditioned:
        torch.testing.assert_close(model.predict(current, actions), model.predict(current, actions + 1))


def test_target_updates_only_explicitly_by_ema_after_online_step():
    model, start, future, actions = fixture()
    model.train()
    assert not model.target_encoder.training
    before = [p.clone() for p in model.target_encoder.parameters()]
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=2e-4)
    optimizer.zero_grad()
    model.losses(start, future, actions)["loss"].backward()
    optimizer.step()
    for old, current in zip(before, model.target_encoder.parameters(), strict=True):
        torch.testing.assert_close(current, old)
    model.update_target()
    for old, current, online in zip(before, model.target_encoder.parameters(), model.encoder.parameters(), strict=True):
        torch.testing.assert_close(current, .996 * old + .004 * online)


@pytest.mark.parametrize("overflow", ["forward", "inverse", "total"])
def test_finite_inputs_cannot_silently_return_nonfinite_losses(overflow):
    model, start, future, actions = fixture(continuous=True, conditioned=False)
    if overflow == "inverse":
        # The finite control passes input validation but its squared error overflows.
        actions.fill_(1e30)
    else:
        with torch.no_grad():
            model.predictor[-1].weight.zero_()
            model.predictor[-1].bias.zero_()
            model.predictor[-1].bias[0] = 1e30 if overflow == "forward" else math.sqrt(1.8e38)
            if overflow == "total":
                # Each term is finite (~1.8e38), but their FP32 sum is not.
                actions.zero_()
                model.inverse_head.layer.weight.zero_()
                model.inverse_head.layer.bias.zero_()
                model.inverse_head.layer.bias[0] = math.sqrt(1.8e38)
    with pytest.raises(ValueError, match="nonfinite forward, inverse or total loss"):
        model.losses(start, future, actions)


@pytest.mark.parametrize("mutation", ["nan", "bounds", "box_order", "types", "mask", "slots", "cost"])
def test_invalid_inputs_do_not_silently_fallback(mutation):
    model, start, future, actions = fixture()
    if mutation == "nan":
        start["features"] = start["features"].detach().clone()
        start["features"][0, 0, 0] = float("nan")
    elif mutation == "bounds":
        start["boxes"][0, 0, 0] = -1
    elif mutation == "box_order":
        start["boxes"][0, 0] = torch.tensor([.8, .8, .1, .1])
    elif mutation == "types":
        start["entity_types"][0, 0] = 2
    elif mutation == "mask":
        start["valid"][0] = False
    elif mutation == "slots":
        start["features"] = start["features"][:, :3]
    else:
        start = {k: v[:1].expand(65, *v.shape[1:]) for k, v in start.items()}
    with pytest.raises(ValueError):
        model.encoder(**start)


@pytest.mark.parametrize("permutation", [None, torch.arange(4), torch.tensor([0, 0, 2, 3]), torch.tensor([3, 2, 1])])
def test_shuffle_requires_real_explicit_batch_permutation(permutation):
    model, start, future, actions = fixture("INV-SHUF")
    with pytest.raises(ValueError, match="permutation"):
        model.losses(start, future, actions, inverse_permutation=permutation)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic(seed):
    result = diagnostic(seed)
    assert result["seed"] == seed
    assert all(result["checks"].values())
    assert result["metrics"]["fixture_loss_after"] < result["metrics"]["fixture_loss_before"]


def test_catalog_docs_and_original_figure_keep_l1_and_cost_boundaries():
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "src/auto_research/paper_specs/catalog/foundation-models/inside-jepa.json").read_text())
    assert catalog["published_at"] == "2026-10-22T12:43:03Z"
    assert catalog["first_author_affiliation"] == "Australian Institute for Machine Learning, Adelaide University"
    assert catalog["code"] is None and catalog["upstream_revision"] is None
    assert catalog["diagnostic_only"] and not catalog["promotion_eligible"] and not catalog["evolve_integrated"]
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost"
    assert catalog["review_done"] and not catalog["automatic_retry"] and not catalog["automatic_implementation_queue"]
    folder = root / "docs/foundation-models/2610.31194-inside-jepa"
    text = (folder / "README.md").read_text()
    for phrase in ("论文信息", "原作者代码", "本地复现代码目录", "成本过高，不复现", "512", "INV-SHUF", "0.996", "验证集", "L1"):
        assert phrase in text
    provenance = json.loads((folder / "assets/provenance.json").read_text())
    assert provenance["figure"] == "Figure 2" and provenance["visually_verified"]
    assert hashlib.sha256((folder / "assets/paper-figure-01.png").read_bytes()).hexdigest() == provenance["image_sha256"]
