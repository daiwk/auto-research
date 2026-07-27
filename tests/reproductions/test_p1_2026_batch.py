from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.evolution.planner import allowed_architectures
from auto_research.reproductions.registry import get_adapter


P1_KEYS = (
    "onemall", "dos", "mdl", "hisac", "pinclip", "pin-scale",
    "causal-retrieval", "podcast-mtl",
)
LLM_KEYS = ("engram", "looped-latent-attention", "gaugequant")


def test_p1_selection_gate_and_metadata():
    for key in P1_KEYS:
        adapter = get_adapter(key)
        assert adapter.paper.has_online_ab
        assert adapter.paper.organization
        assert adapter.paper.published
        assert adapter.paper.url
        assert adapter.fidelity.value == "core_mechanism"


def test_llm_evolve_papers_are_registered_with_exact_dates():
    expected = {
        "engram": "2026-01-12",
        "looped-latent-attention": "2026-07-16",
        "gaugequant": "2026-07-22",
    }
    for key, published in expected.items():
        adapter = get_adapter(key)
        assert adapter.paper.published == published
        assert adapter.paper.track == "llm"
    assert get_adapter("pin-scale").paper.published == "2026-07-19"


def test_new_llm_mutations_execute_and_preserve_shape():
    import torch

    config = MicroLMConfig(
        vocab_size=64, dimensions=32, layers=2, heads=4, kv_heads=2,
        sequence_length=12,
    )
    tokens = torch.randint(0, config.vocab_size, (2, config.sequence_length))
    for architecture in ("engram", "looped_latent_attention", "gaugequant"):
        model = build_micro_lm(architecture, config)
        output = model(tokens)
        assert output.shape == (2, config.sequence_length, config.vocab_size)
        (output.mean() + model.auxiliary_loss()).backward()
        assert model.architecture_stats()


def test_direction_prioritizes_new_llm_mutations():
    for term, architecture in (
        ("Engram 条件记忆", "engram"),
        ("Looped Latent Attention KV 压缩", "looped_latent_attention"),
        ("GaugeQuant W4A4 量化", "gaugequant"),
    ):
        assert allowed_architectures("micro-llm", term, [])[0] == architecture
