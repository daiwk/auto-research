import pytest

from auto_research.reproductions.registry import get_adapter


def test_lwgr_adapter_has_online_revenue_and_ctr():
    adapter = get_adapter("lwgr")
    assert adapter.paper.has_online_ab
    assert {row.lift_percent for row in adapter.paper.online_ab} == {1.35, 1.17}


def test_parallel_codebook_has_straight_through_gradients_when_torch_available():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.lwgr.model import LWGRConfig, build_gr, build_lwgr

    class TinyLLM(torch.nn.Module):
        def forward(self, inputs_embeds, **_):
            return type("Output", (), {"hidden_states": (inputs_embeds,)})()

    config = LWGRConfig()
    gr = build_gr(20, (8, 8, 8), config)
    model = build_lwgr(gr, TinyLLM(), torch.randn(20, 12), config)
    histories = torch.randint(0, 20, (2, 12))
    codes = torch.randint(0, 8, (2, 3))
    logits, probability = model(histories, codes)
    sum(value.sum() for value in logits).backward()
    assert probability.shape == (2, 3, 8)
    assert model.instructions.codebooks.grad is not None
