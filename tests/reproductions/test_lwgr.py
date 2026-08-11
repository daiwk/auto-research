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


def test_decoder_accepts_non_contiguous_attention_context():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.lwgr.model import LWGRConfig, build_gr

    config = LWGRConfig()
    model = build_gr(20, (8, 8, 8), config)
    context = torch.randn(4, config.dimensions * 2)[:, ::2]
    assert not context.is_contiguous()
    codes = torch.zeros((4, 3), dtype=torch.long)
    logits = model.decode(context, codes)
    assert [tuple(row.shape) for row in logits] == [(4, 8), (4, 8), (4, 8)]


def test_world_knowledge_bridges_bfloat_checkpoint_to_float_recommender():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.lwgr.model import LWGRConfig, build_gr, build_lwgr

    class TinyBF16LLM(torch.nn.Module):
        def forward(self, inputs_embeds, **_):
            assert inputs_embeds.dtype == torch.bfloat16
            return type("Output", (), {"hidden_states": (inputs_embeds,)})()

    config = LWGRConfig()
    gr = build_gr(20, (8, 8, 8), config)
    model = build_lwgr(
        gr,
        TinyBF16LLM(),
        torch.randn(20, 12, dtype=torch.bfloat16),
        config,
    )
    histories = torch.randint(0, 20, (2, 12))
    codes = torch.randint(0, 8, (2, 3))
    logits, _ = model(histories, codes)
    assert all(row.dtype == torch.float32 for row in logits)
