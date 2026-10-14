import pytest
import torch
from torch.nn import functional as F

from auto_research.foundation_models.oal import GroupedQuadratic, contribution, group_dimensions


@pytest.fixture(autouse=True)
def fixed_contract_random_state():
    state = torch.random.get_rng_state()
    torch.manual_seed(42)
    yield
    torch.random.set_rng_state(state)


def test_causal_contribution_and_prompt_weighting():
    q = torch.tensor([[[[1., 2.], [3., 4.]]]])
    k = torch.tensor([[[[5., 6.], [7., 8.]]]])
    expected = torch.tensor([[[1 * 5 + 3 * 5 + 3 * 7, 2 * 6 + 4 * 6 + 4 * 8]]]) / (3 * 2**.5)
    torch.testing.assert_close(contribution(q, k), expected)


def test_bootstrap_groups_and_no_cap():
    scores = torch.tensor([[[1., 1.1, 2., 4., 8., 16., 32., 64.]]]).expand(5, -1, -1)
    groups = group_dimensions(scores, tail=1., bootstrap=12, minimum=2)
    assert int(groups.max()) >= 4
    assert len(groups.unique()) == int(groups.max()) + 1
    tied = group_dimensions(torch.ones(3, 1, 8), bootstrap=12)
    assert len(tied.unique()) == 2  # fallback, not a fake natural cut


def test_positive_kernel_recurrent_equivalence_and_gradient():
    torch.manual_seed(11)
    kernel = GroupedQuadratic(torch.tensor([[0, 0, 1, 2], [0, 1, 1, 2]]))
    q, k, v = (torch.randn(2, 2, 5, 4) for _ in range(3))
    assert float(kernel.kernel(q, k).detach().min()) > 0
    dense = kernel(q, k, v)
    torch.testing.assert_close(dense, kernel.recurrent(q, k, v), atol=3e-6, rtol=3e-6)
    dense.square().mean().backward()
    assert float(kernel.factors.grad.norm()) > 0


def test_calibration_matches_outputs_not_only_weights():
    torch.manual_seed(2)
    q, k, v = (torch.randn(1, 1, 8, 4) for _ in range(3))
    target = F.scaled_dot_product_attention(q, k, v, is_causal=True)
    kernel = GroupedQuadratic(torch.tensor([[0, 0, 0, 1]]))
    optimizer = torch.optim.Adam(kernel.parameters(), lr=.02)
    first = float((kernel(q, k, v) - target).detach().square().mean())
    for _ in range(15):
        optimizer.zero_grad()
        loss = (kernel(q, k, v) - target).square().mean()
        loss.backward()
        optimizer.step()
    assert float((kernel(q, k, v) - target).detach().square().mean()) < first


def test_actual_qwen_conversion_and_lora_update():
    from transformers import Qwen2Config, Qwen2ForCausalLM
    from auto_research.foundation_models.oal import QwenOALAttention, install_lora

    config = Qwen2Config(vocab_size=32, hidden_size=16, intermediate_size=32,
                         num_hidden_layers=2, num_attention_heads=2,
                         num_key_value_heads=1, use_cache=False)
    model = Qwen2ForCausalLM(config)
    install_lora(model, rank=2)
    kernel = GroupedQuadratic(torch.tensor([[0] * 7 + [1], [0] * 7 + [1]]))
    model.model.layers[0].self_attn = QwenOALAttention(model.model.layers[0].self_attn, kernel)
    ids = torch.randint(0, 32, (1, 8))
    output = model(input_ids=ids, labels=ids, use_cache=False)
    output.loss.backward()
    assert kernel.factors.grad is not None
    assert any(p.grad is not None and float(p.grad.abs().sum()) > 0
               for name, p in model.named_parameters() if name.endswith(".b"))
