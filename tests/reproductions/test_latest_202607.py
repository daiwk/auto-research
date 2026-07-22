import numpy as np

from auto_research.reproductions.ppl_factory.model import budget_aware_mode, select_blocks
from auto_research.reproductions.registry import get_adapter


def test_latest_industrial_papers_pass_quantified_online_gate():
    assert get_adapter("recap").paper.has_online_ab
    assert get_adapter("uame").paper.has_online_ab
    assert get_adapter("recap").paper.published == "2026-07-17"
    assert get_adapter("uame").paper.published == "2026-07-19"
    # The user explicitly accepts SlimPer's statistically significant full-traffic
    # launch even though Meta did not publish exact engagement lift percentages.
    assert get_adapter("slimper").paper.selection_exception


def test_ppl_factory_changes_selection_with_budget():
    scores = np.arange(100, dtype=np.float64)
    assert budget_aware_mode(0.01) == "mid_random"
    assert budget_aware_mode(0.10) == "middle"
    assert budget_aware_mode(0.50) == "easy"
    selected = select_blocks(scores, 0.10, seed=42)
    assert len(selected) == 10
    assert 40 <= int(np.median(selected)) <= 59


def test_qkv_conv_is_a_residual_depthwise_kernel_three_block():
    import torch
    from auto_research.reproductions.conv_llm.model import build_variant

    model, _ = build_variant("QKV-Conv", 128)
    conv = model.blocks[0].attention.qkv_conv
    assert conv.kernel_size == (3,)
    assert conv.groups == conv.in_channels == conv.out_channels
    logits = model(torch.randint(0, 128, (2, 12)))
    assert logits.shape == (2, 12, 128)


def test_slimper_decouples_stacked_state_from_history_length():
    from auto_research.reproductions.slimper.model import SlimPerConfig, complexity

    short = complexity(SlimPerConfig(item_count=100, maximum_length=32))
    long = complexity(SlimPerConfig(item_count=100, maximum_length=128))
    assert short["slimper_intermediate_elements"] == long["slimper_intermediate_elements"]
    assert long["slimper_attention_score_elements"] == 4 * short["slimper_attention_score_elements"]
    assert long["baseline_attention_score_elements"] > 10 * short["baseline_attention_score_elements"]
