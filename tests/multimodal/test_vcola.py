import pytest
import torch
from concurrent.futures import ThreadPoolExecutor
import inspect
from threading import Barrier
from types import FunctionType, MethodType

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
    expected_api = ('instance_kernel' if callable(getattr(
        backend.text.layers[0].linear_attn, 'chunk_gated_delta_rule', None)) else 'private_forward_globals')
    assert details['delta_capture_api'] == expected_api
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
    first = backend.text.layers[0].linear_attn
    original_forward = first.forward
    original_kernel = getattr(first, 'chunk_gated_delta_rule', None)
    original_instance_fields = dict(vars(first))
    raw = inspect.unwrap(original_forward.__func__)
    global_kernel = raw.__globals__.get('torch_chunk_gated_delta_rule')
    prefix = VisualPrefix(torch.ones(1, 5, 32), torch.arange(5)[None, None].expand(3, 1, -1),
                          torch.tensor([True, False, True, False, False]), 5)
    with pytest.raises(ValueError, match='contiguous'):
        backend.forward(prefix, remain_rate=.5)
    assert first.forward == original_forward
    assert getattr(first, 'chunk_gated_delta_rule', None) is original_kernel
    assert vars(first).keys() == original_instance_fields.keys()
    assert raw.__globals__.get('torch_chunk_gated_delta_rule') is global_kernel


def test_capture_observes_only_target_instance_and_preserves_global_kernel():
    from auto_research.multimodal.vcola_checkpoint import observe_delta_prefill
    model = tiny_model()
    first = model.model.language_model.layers[0].linear_attn
    other = model.model.language_model.layers[1].linear_attn
    hidden = torch.randn(1, 7, 32)
    original_first, original_other = first.forward, other.forward
    raw = inspect.unwrap(original_first.__func__)
    global_kernel = raw.__globals__.get('torch_chunk_gated_delta_rule')
    observed = []
    with torch.no_grad():
        expected_first, expected_other = first(hidden), other(hidden)
        with observe_delta_prefill(first, lambda q, k, v, kwargs, result: observed.append(result[0])):
            assert raw.__globals__.get('torch_chunk_gated_delta_rule') is global_kernel
            assert torch.equal(other(hidden), expected_other)
            assert not observed
            assert torch.equal(first(hidden), expected_first)
            assert len(observed) == 1
        assert torch.equal(first(hidden), expected_first)
    assert first.forward == original_first and other.forward == original_other
    assert raw.__globals__.get('torch_chunk_gated_delta_rule') is global_kernel


def test_capture_callback_failure_restores_exact_instance_and_module_state():
    from auto_research.multimodal.vcola_checkpoint import observe_delta_prefill
    first = tiny_model().model.language_model.layers[0].linear_attn
    before = dict(vars(first))
    original_forward = first.forward
    raw = inspect.unwrap(original_forward.__func__)
    global_kernel = raw.__globals__.get('torch_chunk_gated_delta_rule')

    def failing_observer(*args):
        raise RuntimeError('deliberate actual-kernel observation failure')

    with torch.no_grad(), pytest.raises(RuntimeError, match='deliberate'):
        with observe_delta_prefill(first, failing_observer):
            first(torch.randn(1, 7, 32))
    assert vars(first).keys() == before.keys()
    assert all(vars(first)[name] is value for name, value in before.items())
    assert first.forward == original_forward
    assert raw.__globals__.get('torch_chunk_gated_delta_rule') is global_kernel


def test_capture_unrelated_thread_on_same_instance_is_not_observed():
    from auto_research.multimodal.vcola_checkpoint import observe_delta_prefill
    first = tiny_model().model.language_model.layers[0].linear_attn
    hidden = torch.randn(1, 7, 32)
    observed = []

    def inference():
        with torch.no_grad():
            return first(hidden)

    expected = inference()
    with observe_delta_prefill(first, lambda *args: observed.append(True)):
        with ThreadPoolExecutor(max_workers=1) as pool:
            assert torch.equal(pool.submit(inference).result(timeout=30), expected)
        assert not observed
        assert torch.equal(inference(), expected)
        assert observed == [True]


def test_private_forward_keeps_actual_accelerate_decorator_hooks():
    from auto_research.multimodal.vcola_checkpoint import observe_delta_prefill
    first = tiny_model().model.language_model.layers[0].linear_attn
    called = []

    class Hook:
        def pre_forward(self, module):
            called.append(('pre', module))

        def post_forward(self, module, output):
            called.append(('post', module))

    first.conv1d._hf_hook = Hook()
    # Both official releases already decorate forward (5.14 has no __wrapped__
    # metadata). Compare actual hook execution, not wrapper naming conventions.
    original_forward = first.forward
    hidden = torch.randn(1, 7, 32)
    observed = []
    with torch.no_grad():
        expected = first(hidden)
        assert called == [('pre', first.conv1d), ('post', first.conv1d)]
        called.clear()
        with observe_delta_prefill(first, lambda *args: observed.append(True)):
            assert torch.equal(first(hidden), expected)
    assert called == [('pre', first.conv1d), ('post', first.conv1d)]
    assert observed == [True]
    assert first.forward == original_forward


def test_two_instances_capture_concurrently_without_cross_observation():
    from auto_research.multimodal.vcola_checkpoint import observe_delta_prefill
    model = tiny_model()
    instances = [model.model.language_model.layers[i].linear_attn for i in (0, 1)]
    originals = [instance.forward for instance in instances]
    before = [dict(vars(instance)) for instance in instances]
    hidden = [torch.randn(1, 7 + i, 32) for i in range(2)]
    with torch.no_grad():
        expected = [instance(value) for instance, value in zip(instances, hidden)]
    barrier = Barrier(2)
    observed = [[], []]

    def inference(index):
        with torch.no_grad(), observe_delta_prefill(instances[index],
                lambda q, k, v, kwargs, result: observed[index].append(q.shape[1])):
            barrier.wait(timeout=30)
            output = instances[index](hidden[index])
            barrier.wait(timeout=30)
            return output

    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = [pool.submit(inference, index) for index in range(2)]
        actual = [task.result(timeout=30) for task in pending]
    assert observed == [[7], [8]]
    for index, instance in enumerate(instances):
        assert torch.equal(actual[index], expected[index])
        assert instance.forward == originals[index]
        assert vars(instance).keys() == before[index].keys()
        assert all(vars(instance)[key] is value for key, value in before[index].items())


def _module_kernel_prefill(q, k, v, **kwargs):
    return torch_chunk_gated_delta_rule(q, k, v, **kwargs)  # noqa: F821


def test_unknown_decorator_fails_closed_before_mutating_instance():
    from auto_research.multimodal.vcola_checkpoint import observe_delta_prefill
    module = pytest.importorskip('transformers.models.qwen3_5.modeling_qwen3_5')
    # A synthetic unsupported wrapper tests safety only, not model capability.
    # Private globals keep even this test from changing an official module.
    raw = FunctionType(_module_kernel_prefill.__code__,
        {'torch_chunk_gated_delta_rule': module.torch_chunk_gated_delta_rule})
    reference = {'forward': raw}

    def unsupported(self, *args, **kwargs):
        return reference['forward'](*args, **kwargs)

    unsupported.__wrapped__ = raw
    instance = torch.nn.Module()
    instance.forward = MethodType(unsupported, instance)
    before = dict(vars(instance))
    original_kernel = raw.__globals__['torch_chunk_gated_delta_rule']
    with pytest.raises(RuntimeError, match='unsupported Qwen decorator closure'):
        with observe_delta_prefill(instance, lambda *args: pytest.fail('must not observe')):
            pytest.fail('unsafe wrapper must fail before entering capture')
    assert vars(instance).keys() == before.keys()
    assert all(vars(instance)[key] is value for key, value in before.items())
    assert raw.__globals__['torch_chunk_gated_delta_rule'] is original_kernel
