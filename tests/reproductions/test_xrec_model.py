import json
from pathlib import Path

import torch

from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.xrec.experiment import training_examples
from auto_research.reproductions.xrec.model import (
    XRec,
    geodesic_interpolate,
    riemannian_euler,
    tangent_projection,
)


def test_geodesic_path_velocity_matches_finite_difference() -> None:
    noise = torch.tensor([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    target = torch.tensor([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    time = torch.tensor([0.2, 0.7])
    point, velocity = geodesic_interpolate(noise, target, time)
    ahead, _ = geodesic_interpolate(noise, target, time + 1e-4)
    behind, _ = geodesic_interpolate(noise, target, time - 1e-4)
    torch.testing.assert_close(velocity, (ahead - behind) / 2e-4, atol=3e-4, rtol=3e-4)
    torch.testing.assert_close((point * velocity).sum(-1), torch.zeros(2), atol=1e-5, rtol=0)


def test_riemannian_euler_stays_on_sphere_and_zero_velocity_is_stable() -> None:
    point = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    raw = torch.tensor([[0.2, 1.0], [0.0, 0.0]])
    updated = riemannian_euler(point, tangent_projection(point, raw), 0.25)
    torch.testing.assert_close(updated.norm(dim=-1), torch.ones(2))
    torch.testing.assert_close(updated[1], point[1])


def test_training_has_flow_and_anchor_gradients_and_inference_reuses_history() -> None:
    torch.manual_seed(3)
    model = XRec(torch.randn(16, 8), anchors=4, width=16, heads=2)
    history = torch.tensor([[1, 2, 3], [4, 5, 0]])
    valid = torch.tensor([[True, True, True], [True, True, False]])
    loss, components = model.loss(history, valid, torch.tensor([6, 7]), torch.tensor([1, 2]))
    assert set(components) == {"anchor_ce", "rfm_squared_norm"}
    loss.backward()
    assert model.velocity_head.weight.grad.abs().sum() > 0
    assert model.anchor_head.weight.grad.abs().sum() > 0
    prefill_calls = []
    hook = model.prefill.register_forward_hook(lambda *_: prefill_calls.append(1))
    triggers = model.triggers(history, valid, samples=3, steps=2)
    hook.remove()
    assert len(prefill_calls) == 1
    assert triggers.shape == (2, 3, 8)
    torch.testing.assert_close(triggers.norm(dim=-1), torch.ones(2, 3), atol=1e-5, rtol=0)


def test_xrec_training_prefixes_and_audited_metrics() -> None:
    examples = training_examples(((1, 2, 3, 4),), max_history=2)
    assert examples == (((1,), 2), ((1, 2), 3), ((2, 3), 4))
    adapter = get_adapter("xrec")
    assert adapter.paper.has_online_ab
    assert adapter.device_capabilities == ("cpu",)
    path = Path(__file__).resolve().parents[2] / "docs/reproductions/2609.29180-xrec/metrics/public-seeds42-44.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["evaluation_protocol"]["tier"] == "l2_public_dataset"
    for phase in ("validation", "test"):
        for model in ("xrec", "u2i"):
            for metric in ("hit_at_10", "ndcg_at_10"):
                key = f"{phase}_{metric}_{model}_mean"
                values = [row[phase][model][metric] for row in payload["seeds"]]
                assert abs(payload["metrics"][key] - sum(values) / len(values)) < 1e-9
