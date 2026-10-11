from copy import deepcopy

import pytest
torch = pytest.importorskip("torch")

from auto_research.foundation.adamw4bit import (
    AdamW4Bit, decode_blockwise, dynamic4, pack4, quantize_blockwise,
    rounding_probabilities, unpack4,
)


def test_pack_is_real_half_byte_storage_and_reversible():
    codes = torch.arange(16, dtype=torch.uint8)
    packed = pack4(codes)
    assert packed.dtype == torch.uint8 and packed.numel() == 8
    assert torch.equal(unpack4(packed), codes.long())
    assert dynamic4("cpu").numel() == 16


def test_zero_cell_rounding_preserves_expected_preconditioner_not_state():
    v, low, high = torch.tensor([1e-4]), torch.tensor([0.]), torch.tensor([.01])
    p = rounding_probabilities(v, low, high, bias_correction=.5, eps=1e-6)
    h = lambda x: (torch.sqrt(x / .5) + 1e-6).reciprocal()
    assert torch.allclose(p * h(low) + (1 - p) * h(high), h(v), rtol=1e-6)
    assert float(p) < 1e-3


@pytest.mark.parametrize("recipe", ["zip-sr", "ze-eden"])
def test_persistent_moments_are_packed_and_resume_matches(recipe):
    torch.manual_seed(4)
    p = torch.nn.Parameter(torch.linspace(-1, 1, 4096))
    optimizer = AdamW4Bit([p], recipe=recipe)
    p.grad = torch.linspace(-.1, .2, 4096)
    optimizer.step()
    state = optimizer.state[p]
    assert state["m_codes"].dtype == state["v_codes"].dtype == torch.uint8
    assert state["m_codes"].numel() == state["v_codes"].numel() == 2048
    assert "m" not in state and "v" not in state
    saved = deepcopy(optimizer.state_dict())
    q = torch.nn.Parameter(p.detach().clone())
    resumed = AdamW4Bit([q], recipe=recipe)
    resumed.load_state_dict(saved)
    rng = torch.get_rng_state()
    optimizer.step()
    q.grad = p.grad.clone()
    torch.set_rng_state(rng)
    resumed.step()
    assert torch.equal(p, q)
    assert torch.equal(optimizer.state[p]["v_codes"], resumed.state[q]["v_codes"])


def test_first_update_precedes_quantization_and_fp32_fallback_matches_adamw():
    for size in (16, 4096):
        p = torch.nn.Parameter(torch.linspace(-1, 1, size))
        q = torch.nn.Parameter(p.detach().clone())
        actual = AdamW4Bit([p])
        reference = torch.optim.AdamW([q], lr=1e-3, betas=(.9, .95), weight_decay=.1)
        p.grad = torch.linspace(-.5, .5, size)
        q.grad = p.grad.clone()
        actual.step()
        reference.step()
        assert torch.allclose(p, q, atol=1e-7, rtol=1e-6)


def test_zero_eden_block_decodes_to_exactly_zero():
    codes, scales = quantize_blockwise(torch.zeros(4096), block_size=128, scheme="ze-eden")
    value = decode_blockwise(codes, scales, block_size=128, signed=False, shape=(4096,))
    assert torch.equal(value, torch.zeros_like(value))


def test_lm_head_switch_only_last_ten_percent():
    p = torch.nn.Parameter(torch.ones(4096))
    optimizer = AdamW4Bit([p])
    optimizer.schedule_lm_head([p], completed_steps=89, total_steps=100)
    assert not optimizer._head_sr
    optimizer.schedule_lm_head([p], completed_steps=90, total_steps=100)
    assert optimizer._head_sr and optimizer._head_ids == {id(p)}


def test_bfloat16_resume_does_not_round_fp32_scales():
    p = torch.nn.Parameter(torch.ones(4096, dtype=torch.bfloat16))
    optimizer = AdamW4Bit([p])
    p.grad = torch.linspace(-.7, .6, 4096).to(torch.bfloat16)
    optimizer.step()
    saved = deepcopy(optimizer.state_dict())
    resumed = AdamW4Bit([p])
    resumed.load_state_dict(saved)
    for key in ("m_scale", "v_scale"):
        assert resumed.state[p][key].dtype == torch.float32
        assert torch.equal(resumed.state[p][key], optimizer.state[p][key])
