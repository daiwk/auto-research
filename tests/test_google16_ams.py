import math
from types import SimpleNamespace

import pytest
import torch

from auto_research.foundation_models.google16_ams import (
    ConceptFingerprint, activation_direction, candidate_layers, compare_fingerprints,
    extract_last_token_activations, select_concept_layer, tier_one,
)


def test_direction_and_population_pooled_separation_match_upstream_equation():
    positive = torch.tensor([[3., 0.], [5., 0.]])
    negative = torch.tensor([[0., 0.], [2., 0.]])
    direction, separation = activation_direction(positive, negative)
    torch.testing.assert_close(direction, torch.tensor([1., 0.], dtype=torch.float64))
    assert separation.item() == pytest.approx(3.)


def test_layer_selection_preserves_actual_block_identity_and_reference_bands():
    pos = torch.tensor([[[1., 0.], [3., 0.]], [[3., 0.], [5., 0.]]])
    neg = torch.tensor([[[0., 0.], [0., 0.]], [[2., 0.], [2., 0.]]])
    result = select_concept_layer(pos, neg, (3, 4))
    assert result.layer == 4 and result.separation == pytest.approx(3.)
    assert tier_one({"x": result}) == "WARNING"
    for value, expected in ((1.99, "CRITICAL"), (2., "WARNING"), (3.5, "WARNING"), (3.5001, "PASS")):
        assert tier_one({"x": ConceptFingerprint(4, result.direction, value, 2)}) == expected


def test_no_cluster_difference_and_constant_variance_are_finite_not_infinite_safety():
    direction, separation = activation_direction(torch.ones(2, 3), torch.ones(2, 3))
    assert direction.norm() == 0 and separation == 0
    _, constant = activation_direction(torch.ones(2, 3), torch.zeros(2, 3))
    assert math.isfinite(float(constant))


def test_tier_two_rejects_rotations_drift_and_different_layer_comparisons():
    baseline = ConceptFingerprint(4, torch.tensor([1., 0.]), 4., 16)
    assert compare_fingerprints(baseline, baseline)["verified"]
    assert not compare_fingerprints(ConceptFingerprint(4, torch.tensor([0., 1.]), 4., 16), baseline)["verified"]
    assert not compare_fingerprints(ConceptFingerprint(4, torch.tensor([1., 0.]), 5., 16), baseline)["verified"]
    with pytest.raises(ValueError):
        compare_fingerprints(ConceptFingerprint(5, baseline.direction, 4., 16), baseline)


def test_checkpoint_extraction_is_last_real_token_no_generation_and_no_truncation():
    class Tokenizer:
        def __call__(self, prompt, **kwargs):
            return {"input_ids": torch.tensor([[1, 2, 3]]), "attention_mask": torch.ones(1, 3)}

    class Model:
        config = SimpleNamespace(num_hidden_layers=5)

        def __call__(self, **kwargs):
            assert kwargs["output_hidden_states"] and not kwargs["use_cache"]
            hidden = tuple(torch.arange(6.).reshape(1, 3, 2) + layer for layer in range(6))
            return SimpleNamespace(hidden_states=hidden)

    activations, layers = extract_last_token_activations(Model(), Tokenizer(), ["public prompt"], device="cpu")
    assert layers == candidate_layers(5) == (2, 3)
    assert activations.tolist() == [[[7., 8.], [8., 9.]]]
    with pytest.raises(ValueError, match="token budget"):
        extract_last_token_activations(Model(), Tokenizer(), ["public prompt"], device="cpu", max_tokens=2)


def test_hidden_state_mapping_matches_real_transformer_block_hooks_without_download():
    transformers = pytest.importorskip("transformers")
    model = transformers.GPT2LMHeadModel(transformers.GPT2Config(
        vocab_size=12, n_positions=8, n_embd=8, n_layer=5, n_head=2,
        resid_pdrop=0, embd_pdrop=0, attn_pdrop=0,
    )).eval()

    class Tokenizer:
        def __call__(self, prompt, **kwargs):
            return {"input_ids": torch.tensor([[1, 2, 3]])}

    cached = {}
    handles = []
    for block_id in candidate_layers(5):
        def hook(_module, _inputs, output, block_id=block_id):
            hidden = output[0] if isinstance(output, tuple) else output
            cached[block_id] = hidden[0, -1].detach()
        handles.append(model.transformer.h[block_id].register_forward_hook(hook))
    try:
        actual, layers = extract_last_token_activations(model, Tokenizer(), ["prompt"], device="cpu")
    finally:
        for handle in handles:
            handle.remove()
    assert layers == (2, 3)
    torch.testing.assert_close(actual[0], torch.stack([cached[layer] for layer in layers]))
    assert candidate_layers(24) == tuple(range(9, 19))


def test_bad_shapes_nonfinite_and_empty_concepts_rejected():
    with pytest.raises(ValueError):
        activation_direction(torch.ones(1, 2), torch.ones(1, 2))
    with pytest.raises(ValueError):
        activation_direction(torch.full((2, 2), float("nan")), torch.ones(2, 2))
    with pytest.raises(ValueError):
        tier_one({})
