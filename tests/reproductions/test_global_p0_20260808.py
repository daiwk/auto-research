from pathlib import Path

import pytest

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.evolution.planner import allowed_architectures
from auto_research.reproductions.registry import get_adapter


RECOMMENDATION = (
    "glorank", "dual-rerank", "oneranker", "radar", "dualgr", "mpformer",
    "hap", "onepiece", "intsr", "cdm", "cwm",
)
FOUNDATION = (
    "rope", "alibi", "gqa", "hymba", "moba", "blt", "doremi",
    "data-mixing-laws",
)


def test_global_p0_reproductions_are_registered_and_documented():
    for key in RECOMMENDATION + FOUNDATION:
        adapter = get_adapter(key)
        assert adapter.paper.organization
        assert adapter.paper.published
        page = Path("docs/reproductions") / f"{adapter.paper.arxiv_id}-{key}" / "README.md"
        assert page.is_file()
        if key in RECOMMENDATION:
            assert adapter.paper.online_ab


@pytest.mark.parametrize(
    ("architecture", "stat"),
    [
        ("rope", "position_encoding"),
        ("alibi", "train_short_test_long"),
        ("gqa", "kv_heads"),
        ("hymba", "parallel_attention_ssm"),
        ("moba", "selected_block_fraction"),
        ("blt", "observed_patch_boundary_rate"),
    ],
)
def test_global_p0_llm_architectures_execute_their_real_path(architecture, stat):
    torch = pytest.importorskip("torch")
    model = build_micro_lm(
        architecture,
        MicroLMConfig(vocab_size=64, dimensions=32, layers=2, heads=4),
    )
    tokens = torch.randint(0, 64, (2, 16))
    loss = model(tokens).square().mean() + model.auxiliary_loss()
    loss.backward()
    assert stat in model.architecture_stats()


@pytest.mark.parametrize(
    ("term", "architecture"),
    [
        ("RoPE 长上下文", "rope"), ("ALiBi 外推", "alibi"),
        ("GQA KV cache", "gqa"), ("Hymba 混合 SSM", "hymba"),
        ("MoBA block routing", "moba"), ("BLT byte patch", "blt"),
    ],
)
def test_global_p0_architectures_are_selectable_by_direction(term, architecture):
    assert allowed_architectures("micro-llm", term, [])[0] == architecture
