import pytest
import torch

from auto_research.multimodal.vcola import (
    delta_state_scores, early_exit_visual, importance_chunks, merge_visual_tokens,
)


def example():
    torch.manual_seed(42)
    q, k = torch.randn(1, 7, 2, 3), torch.randn(1, 7, 2, 3)
    v = torch.randn(1, 7, 2, 4)
    return q, k, v, -torch.rand(1, 7, 2), torch.rand(1, 7, 2)


def test_delta_state_replay_matches_official_reference():
    module = pytest.importorskip('transformers.models.qwen3_5.modeling_qwen3_5')
    q, k, v, g, beta = example()
    scores = delta_state_scores(q, k, v, g, beta)
    output, state = module.torch_recurrent_gated_delta_rule(q, k, v, g, beta,
        initial_state=None, output_final_state=True, use_qk_l2norm_in_kernel=True)
    assert torch.allclose(scores.recurrent_output, output, atol=1e-6)
    assert torch.allclose(scores.final_state, state, atol=1e-6)


def test_importance_reads_final_state_and_uniqueness_is_probe_change():
    q = torch.tensor([[[[1., 0.]], [[0., 1.]]]])
    key = q.clone()
    value = torch.tensor([[[[1., 2.]], [[3., 4.]]]])
    g, beta = torch.zeros(1, 2, 1), torch.ones(1, 2, 1)
    scores = delta_state_scores(q, key, value, g, beta, window=(0, 1), mix=.1)
    assert torch.allclose(scores.importance, torch.ones(1, 2))
    assert torch.allclose(scores.uniqueness, torch.full((1, 2), .5))
    changed = delta_state_scores(q, key, value, g, torch.zeros_like(beta))
    assert not torch.equal(changed.combined, scores.combined)
    assert bool(((scores.combined >= 0) & (scores.combined <= 1)).all())


def test_mass_partition_keeps_every_member_and_nonempty_chunks():
    for scores in (torch.zeros(9), torch.ones(9), torch.tensor([100., 0., 0., 0., 0., 0., 0., 0., 0.])):
        chunks = importance_chunks(scores, 6)
        assert len(chunks) == 6
        assert [i for a, b in chunks for i in range(a, b)] == list(range(9))
        assert all(b > a for a, b in chunks)
    score = torch.tensor([.01, .01, .01, 1., 1., 1., 1., 1.])
    chunks = importance_chunks(score, 3)
    assert chunks[0][1] - chunks[0][0] > chunks[-1][1] - chunks[-1][0]


def test_visual_only_weighted_merge_keeps_original_text_and_mrope():
    hidden = torch.arange(24.).reshape(1, 8, 3)
    positions = torch.arange(8)[None, None].expand(3, 1, -1)
    mask = torch.tensor([False, True, True, True, True, False, False, False])
    scores = torch.ones(8)
    out, pos, visual, receipt = merge_visual_tokens(hidden, positions, mask, scores, remain_rate=.5)
    assert out.shape[1] == 6 and int(visual.sum()) == 2
    assert torch.equal(out[:, ~visual], hidden[:, ~mask])
    assert torch.equal(pos[:, :, ~visual], positions[:, :, ~mask])
    assert torch.allclose(out[:, 1], hidden[:, 1:3].mean(1))
    assert sum(receipt['chunk_sizes']) == 4
    exited, exit_pos, exit_mask = early_exit_visual(out, pos, visual)
    assert torch.equal(exited, hidden[:, ~mask])
    assert torch.equal(exit_pos, positions[:, :, ~mask])
    assert not bool(exit_mask.any())


def test_reference_boundaries_are_explicit_errors():
    q, k, v, g, beta = example()
    bad_value = v.clone()
    bad_value[0, 0, 0, 0] = float('nan')
    with pytest.raises(ValueError, match='finite'):
        delta_state_scores(q, k, bad_value, g, beta)
    with pytest.raises(ValueError):
        delta_state_scores(q, k, v, -g, beta)
    with pytest.raises(ValueError):
        importance_chunks(torch.tensor([1., float('nan')]), 1)
    with pytest.raises(ValueError):
        importance_chunks(torch.ones(3), 4)
    with pytest.raises(ValueError, match='contiguous'):
        merge_visual_tokens(torch.ones(1, 3, 2), torch.zeros(3, 1, 3),
            torch.tensor([True, False, True]), torch.ones(3))


def tiny_model():
    module = pytest.importorskip('transformers.models.qwen3_5.modeling_qwen3_5')
    from transformers import Qwen3_5Config
    config = Qwen3_5Config(text_config=dict(vocab_size=64, hidden_size=32, intermediate_size=48,
        num_hidden_layers=4, num_attention_heads=2, num_key_value_heads=1, head_dim=16,
        linear_num_key_heads=1, linear_num_value_heads=2, linear_key_head_dim=8,
        linear_value_head_dim=8, eos_token_id=63,
        rope_parameters={'rope_type': 'default', 'rope_theta': 10000.,
                         'partial_rotary_factor': 1., 'mrope_section': [2, 3, 3],
                         'mrope_interleaved': True}),
        vision_config=dict(depth=1, hidden_size=16, intermediate_size=24, num_heads=2,
                           out_hidden_size=32, num_position_embeddings=16),
        image_token_id=60, video_token_id=61, vision_start_token_id=58, vision_end_token_id=59)
    torch.manual_seed(42)
    return module.Qwen3_5ForConditionalGeneration(config).eval()


def test_real_hybrid_layers_baseline_parity_compression_and_early_exit():
    from auto_research.multimodal.vcola_checkpoint import Qwen35VCoLA, VisualPrefix
    model = tiny_model()
    hidden = torch.randn(1, 12, 32)
    positions = torch.arange(12)[None, None].expand(3, 1, -1)
    visual = torch.tensor([False] * 2 + [True] * 6 + [False] * 4)
    prefix = VisualPrefix(hidden, positions, visual, 12)
    backend = Qwen35VCoLA(model)
    with torch.no_grad():
        original = model.model.language_model(inputs_embeds=hidden, position_ids=positions,
            attention_mask=torch.ones(1, 12, dtype=torch.long), use_cache=False).last_hidden_state
        expected = model.lm_head(original[:, -1]).float()
    logits, details = backend.forward(prefix, collect_scores=True)
    assert torch.allclose(logits, expected, atol=1e-5)
    assert details['recurrence_relative_error'] < 1e-5
    compressed, info = backend.forward(prefix, remain_rate=.5, exit_layer=3)
    assert torch.isfinite(compressed).all()
    assert [x['visual_tokens'] for x in info['layers']] == [6, 3, 3, 0]
    assert [x['sequence_tokens'] for x in info['layers']] == [12, 9, 9, 6]
    assert not torch.allclose(compressed, expected)
    assert info['merge']['original_visual_tokens'] == 6
    assert info['original_text_positions_preserved']


def test_actual_vision_encoder_prepare_and_original_multimodal_forward_parity():
    from auto_research.multimodal.vcola_checkpoint import Qwen35VCoLA
    model = tiny_model()
    # Processor geometry for one 224x224 image: 14x14 patches and 2x2 merge.
    # Random pixels are exclusively a numerical mechanism fixture, no task score.
    ids = torch.tensor([[7, 58, *([60] * 49), 59, 8, 9]])
    batch = {'input_ids': ids, 'attention_mask': torch.ones_like(ids),
        'mm_token_type_ids': (ids == 60).long(),
        'pixel_values': torch.randn(196, 1536), 'image_grid_thw': torch.tensor([[1, 14, 14]])}
    backend = Qwen35VCoLA(model)
    with torch.no_grad():
        expected = model(**batch, use_cache=False, logits_to_keep=1).logits[:, -1].float()
        prefix = backend.prepare(batch)
        logits, _ = backend.forward(prefix, collect_scores=True)
    assert int(prefix.visual_mask.sum()) == 49
    assert prefix.positions.shape == (3, 1, ids.shape[1])
    assert torch.allclose(logits, expected, atol=1e-5)
    _, details = backend.forward(prefix, remain_rate=.5, exit_layer=3)
    assert [x['visual_tokens'] for x in details['layers']] == [49, 24, 24, 0]


def test_hook_restored_after_failure():
    from auto_research.multimodal.vcola_checkpoint import Qwen35VCoLA, VisualPrefix
    model = tiny_model()
    backend = Qwen35VCoLA(model)
    kernel = backend.text.layers[0].linear_attn.chunk_gated_delta_rule
    prefix = VisualPrefix(torch.ones(1, 5, 32), torch.arange(5)[None, None].expand(3, 1, -1),
                          torch.tensor([True, False, True, False, False]), 5)
    with pytest.raises(ValueError, match='contiguous'):
        backend.forward(prefix, remain_rate=.5)
    assert backend.text.layers[0].linear_attn.chunk_gated_delta_rule == kernel
