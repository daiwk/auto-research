from types import SimpleNamespace

import pytest

torch = pytest.importorskip("torch")
qwen = pytest.importorskip("transformers.models.qwen3.modeling_qwen3")

from auto_research.reproductions.kv_task_evaluation import attention_workspace


@pytest.mark.parametrize("method", ["full", "recent", "beaconkv", "kvmem"])
def test_workspace_drives_actual_gqa_decode_and_restores_backend(method):
    torch.manual_seed(42)
    module = SimpleNamespace(layer_idx=0, num_key_value_groups=2, training=False)
    query = torch.randn(1, 4, 64, 8)
    key, value = torch.randn(1, 2, 64, 8), torch.randn(1, 2, 64, 8)
    original = qwen.eager_attention_forward
    with attention_workspace(method, 32):
        qwen.eager_attention_forward(module, query, key, value, None, scaling=8 ** -0.5)
        output, weights = qwen.eager_attention_forward(
            module, query[:, :, -1:], key, value, None, scaling=8 ** -0.5,
        )
        assert output.shape == (1, 1, 4, 8)
        assert weights.shape[-1] == (64 if method == "full" else 32)
        assert torch.isfinite(output).all()
    assert qwen.eager_attention_forward is original
