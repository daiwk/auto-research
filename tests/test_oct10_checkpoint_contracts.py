import json

import pytest
import torch

from auto_research.post_training.oct10_checkpoint import (
    LowRankLinear, install_lora, load_public_rows, numeric_answer,
)


def test_lora_zero_initial_output_and_frozen_base():
    torch.manual_seed(42)
    base = torch.nn.Linear(4, 6)
    x = torch.randn(3, 4)
    original = base(x).detach()
    layer = LowRankLinear(base, rank=2)
    assert torch.equal(layer(x), original)
    layer(x).square().mean().backward()
    assert base.weight.grad is None and layer.b.grad.abs().sum() > 0
    assert layer.a.dtype == torch.float32


def test_lora_installs_only_declared_attention_projections():
    class Attention(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.q_proj = torch.nn.Linear(4, 4)
            self.v_proj = torch.nn.Linear(4, 4)
            self.k_proj = torch.nn.Linear(4, 4)

    model = torch.nn.Sequential(Attention())
    assert install_lora(model, rank=2) == 2
    assert not model[0].k_proj.weight.requires_grad
    assert model[0].q_proj.a.requires_grad


def test_dataset_contract_and_external_verifier(tmp_path):
    path = tmp_path / "public.jsonl"
    path.write_text(json.dumps({"question": "How many?", "answer": "#### 1,200"}) + "\n")
    assert len(load_public_rows(path)) == 1
    assert numeric_answer("Steps 12 then \\boxed{1,200}") == "1200"
    assert numeric_answer("no numeric answer") is None
    path.write_text('{}\n')
    with pytest.raises(ValueError):
        load_public_rows(path)
