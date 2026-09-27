import json
from pathlib import Path

import torch

from auto_research.reproductions.onetrans_v2.model import OneTransV2
from auto_research.reproductions.registry import get_adapter


def test_stage_isolation_and_all_losses_train() -> None:
    torch.manual_seed(4)
    codes = torch.randint(0, 4, (20, 3))
    model = OneTransV2(20, 5, codes, width=16, history_limit=8)
    history = torch.tensor([[1, 2, 3], [4, 5, 0]])
    valid = torch.tensor([[True, True, True], [True, True, False]])
    item = torch.tensor([6, 7])
    genre = torch.randn(2, 5)
    decision = torch.tensor([[1, 0], [0, 1]])
    labels = torch.tensor([[1., 1.], [1., 0.]])
    outputs = model(history, valid, item, genre, decision, codes[item])
    loss, components = model.loss(outputs, decision_targets=decision, sid_targets=codes[item], labels=labels, retrieval_mask=labels[:, 0].bool())
    loss.backward()
    assert set(components) == {"decision_ce", "sid_ce", "pre_bce", "fine_bce", "fine_to_pre_kd"}
    assert model.backbone.self_attn.in_proj_weight.grad.abs().sum() > 0
    assert model.pre_head.weight.grad.abs().sum() > 0
    assert model.fine_head.weight.grad.abs().sum() > 0
    assert model.sid_heads[0].weight.grad.abs().sum() > 0
    assert model.decisions[0].weight.grad.abs().sum() > 0
    # Changing a future behavior cannot change the earlier causal state.
    before = model.encode(history, valid)[0, 0].detach()
    changed = history.clone()
    changed[0, 2] = 9
    torch.testing.assert_close(before, model.encode(changed, valid)[0, 0])
    # The pre-rank head cannot see extra fine-rank-only genre features.
    other = model(history, valid, item, genre + 10, decision, codes[item])
    torch.testing.assert_close(outputs["pre"], other["pre"])
    default = model(history, valid, item, genre)
    steered = model(history, valid, item, genre, decision_offsets=torch.tensor([[-100., 100.], [-100., 100.]]))
    assert steered["selected_decisions"].eq(1).all()
    torch.testing.assert_close(default["pre"], steered["pre"])
    torch.testing.assert_close(default["fine"], steered["fine"])


def test_adapter_does_not_advertise_unsupported_business_or_cuda_claims() -> None:
    adapter = get_adapter("onetrans-v2")
    assert adapter.device_capabilities == ("cpu",)
    assert adapter.fidelity.value == "concept_demo"
    assert adapter.paper.has_online_ab


def test_public_three_seed_receipt_is_diagnostic_and_consistent() -> None:
    root = Path(__file__).resolve().parents[2]
    path = root / "docs/reproductions/2609.28589-onetrans-v2/metrics/public-seeds42-44.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["evaluation_protocol"]["tier"] == "l1_mechanism"
    assert payload["evaluation_protocol"]["formal_comparison"] is False
    assert [entry["seed"] for entry in payload["seeds"]] == [42, 43, 44]
    for phase in ("validation", "test"):
        for key in ("pre_rating_ge_3_auc", "fine_rating_ge_3_auc", "sid_exact_accuracy"):
            observed = sum(row[phase][key] for row in payload["seeds"]) / 3
            assert abs(observed - payload["metrics"][f"{phase}_{key}_mean"]) < 1e-10
