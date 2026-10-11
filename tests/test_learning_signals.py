import pytest
import torch

from auto_research.post_training.learning_signals import (
    cross_fitted_occupancy, learning_signal_proxy, linear_cka, mean_pool_prompt,
    occupancy_surrogate, parameter_displacement, prompt_layer_features, topk_residual,
)


def test_negative_truncated_loss_does_not_become_fake_positive_kl():
    s = torch.tensor([[[0., 0., 0.]]], requires_grad=True)
    t = torch.tensor([[[4., -4., -4.]]])
    loss = topk_residual(s, t, torch.ones(1, 1, dtype=torch.bool), topk=1)
    assert float(loss.detach()) < 0
    assert learning_signal_proxy(loss, 2.) is None
    assert learning_signal_proxy(2., 3.) == 2.25


def test_cross_fitted_estimator_uses_opposite_folds_and_keeps_invalid_denominator():
    scores = torch.tensor([[1., 2., 3., 4.]], requires_grad=True)
    losses = torch.tensor([[2., 4., 8., 10.]], requires_grad=True)
    h0, h1 = occupancy_surrogate(losses, scores)
    h0.backward(retain_graph=True)
    torch.testing.assert_close(scores.grad, torch.tensor([[-3.5, -2.5, 0., 0.]]))
    assert losses.grad is None
    assert cross_fitted_occupancy([torch.tensor([1.])], [torch.tensor([-1.])],
                                  [torch.tensor([2.])], [torch.tensor([3.])])["alpha"] is None
    result = cross_fitted_occupancy([torch.tensor([2.])], [torch.tensor([4.])],
                                    [torch.tensor([6.])], [torch.tensor([8.])])
    assert result["alpha"] == 2.5


def test_cka_centers_prompts_and_is_rotation_scale_invariant_not_identity_claim():
    torch.manual_seed(15)
    x = torch.randn(12, 4)
    q = torch.linalg.qr(torch.randn(4, 4))[0]
    assert linear_cka(x, 3 * x @ q + 10) == pytest.approx(1., abs=1e-6)
    assert linear_cka(torch.ones(12, 4), x) is None
    h = torch.tensor([[[1., 2.], [3., 4.], [999., 999.]]])
    torch.testing.assert_close(mean_pool_prompt(h, torch.tensor([[1, 1, 0]])), torch.tensor([[2., 3.]]))


def test_global_displacement_counts_tied_weights_once_not_mean_of_ratios():
    a, b = torch.ones(3), torch.ones(3) * 2
    result = parameter_displacement({"embed": a, "head": a}, {"embed": b, "head": b})
    assert result["unique_parameter_entries"] == 3
    assert result["relative_displacement"] == 1.
    with pytest.raises(ValueError, match="parameter space"):
        parameter_displacement({"a": a}, {"b": b})


def test_real_qwen_feature_hooks_match_all_hidden_states_and_ignore_broken_recorder():
    from types import SimpleNamespace
    pytest.importorskip("transformers")
    from transformers import Qwen3Config, Qwen3ForCausalLM

    torch.manual_seed(17)
    config = Qwen3Config(hidden_size=32, intermediate_size=64, num_hidden_layers=3,
                        num_attention_heads=4, num_key_value_heads=2, head_dim=8,
                        vocab_size=128)
    config._attn_implementation = "eager"
    model = Qwen3ForCausalLM(config).eval()
    prompts = [torch.tensor([[1, 2, 3]]), torch.tensor([[4, 5]])]
    expected = []
    for ids in prompts:
        with torch.no_grad():
            hidden = model(ids, use_cache=False, output_hidden_states=True).hidden_states
        expected.append(torch.stack([h.float().mean(1)[0] for h in hidden]))
    reference = torch.stack(expected).transpose(0, 1)
    assert reference.shape == (4, 2, 32)
    # Reproduce the remote recorder returning one final tensor instead of a
    # tuple: hooks must still observe all N+1 actual hidden-state positions.
    forward = model.forward
    def broken_recorder(*args, **kwargs):
        output = forward(*args, **kwargs)
        return SimpleNamespace(hidden_states=output.logits)
    model.forward = broken_recorder
    modules = (model.model.embed_tokens, *model.model.layers, model.model.norm)
    existing_hooks = [dict(module._forward_hooks) for module in modules]
    torch.testing.assert_close(prompt_layer_features(model, prompts), reference)
    # Transformers installs its own persistent recorders. Preserve them, but
    # remove every hook added by this feature extractor.
    assert [dict(module._forward_hooks) for module in modules] == existing_hooks


def test_feature_hooks_reject_padded_batch_and_remove_handles_after_failure():
    from types import SimpleNamespace

    decoder = SimpleNamespace(embed_tokens=torch.nn.Embedding(8, 4),
                              layers=torch.nn.ModuleList([torch.nn.Identity()]), norm=torch.nn.Identity())
    model = SimpleNamespace(model=decoder)
    with pytest.raises(ValueError, match="one nonempty unpadded prompt"):
        prompt_layer_features(model, [torch.ones(2, 3, dtype=torch.long)])
    assert not decoder.embed_tokens._forward_hooks
    assert not decoder.norm._forward_hooks
