import json

import pytest
import torch

from auto_research.post_training.oct10_checkpoint import (
    LowRankLinear, install_lora, load_public_rows, numeric_answer, verified_reward,
    PAPER_OBJECTIVES, OBJECTIVES,
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
    assert verified_reward("no numeric answer", "#### 1200") == 0
    assert verified_reward("\\boxed{1,200}", "#### 1200") == 1
    with pytest.raises(ValueError):
        verified_reward("no numeric answer", "no numeric answer")
    path.write_text('{}\n')
    with pytest.raises(ValueError):
        load_public_rows(path)


def test_paper_catalog_has_executable_objective_and_complete_metadata():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    for key, objectives in PAPER_OBJECTIVES.items():
        assert set(objectives) <= set(OBJECTIVES)
        spec = json.loads((root / "src/auto_research/paper_specs/catalog/post-training" /
                           f"{key}.json").read_text())
        assert spec["adapter"] == key and spec["requires_gpu_validation"] is True
        assert spec["first_author_affiliation"] and spec["published"] == "2026-10-08"
        text = (root / "docs" / spec["detail_path"]).read_text()
        for label in ("论文链接", "公司 / 机构", "首次公开日期", "原作者代码",
                      "本地 adapter", "本地复现代码", "核心公式", "复现边界"):
            assert label in text
