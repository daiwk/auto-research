"""Primary-equation references, negative controls and input boundaries."""
import pytest
import torch

from auto_research.foundation_models import fold_bias, merlin, swim


@pytest.mark.parametrize("module", [merlin, fold_bias, swim])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_seeded_measured_contracts(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed
    assert len(result["checks"]) == 8 and all(result["checks"].values())
    assert all(torch.isfinite(torch.tensor(v)) for v in result["metrics"].values())


def test_merlin_second_moment_is_not_covariance_and_mix_is_not_single_softmax():
    keys = torch.tensor([[[1.], [1.]], [[-1.], [3.]]], dtype=torch.float64)
    means, seconds = merlin.segment_moments(keys)
    assert torch.equal(means, torch.ones(2, 1, dtype=torch.float64))
    assert torch.equal(seconds[:, 0, 0], torch.tensor([1., 5.], dtype=torch.float64))
    query = torch.ones(1, 1, dtype=torch.float64)
    visible = torch.ones(1, 2, dtype=torch.bool)
    one = torch.ones((), dtype=torch.float64)
    result = merlin.routing_weights(query, means, seconds, visible,
                                    torch.zeros(1, dtype=torch.float64), one, one)
    assert torch.equal(result["variance_scores"], torch.tensor([[0., 4.]], dtype=torch.float64))
    assert result["weights"][0, 1] > .9
    mixed = merlin.routing_weights(query, torch.tensor([[0.], [2.]], dtype=torch.float64),
        torch.tensor([[[4.]], [[4.]]], dtype=torch.float64), visible,
        torch.tensor([.5], dtype=torch.float64), one, one)
    expected = .5 * torch.tensor([[0., 2.]], dtype=torch.float64).softmax(-1) + .5 * torch.tensor([[4., 0.]], dtype=torch.float64).softmax(-1)
    assert torch.equal(mixed["weights"], expected)
    assert not torch.allclose(expected, torch.tensor([[2., 1.]], dtype=torch.float64).softmax(-1))


def test_merlin_completed_boundary_and_masked_readout_gradients():
    starts = torch.tensor([0, 4, 8])
    visible = merlin.completed_segment_visibility(starts, 4, torch.tensor([2, 3, 7, 11]))
    assert torch.equal(visible, torch.tensor([[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]], dtype=torch.bool))
    readouts = torch.randn(1, 3, 2, dtype=torch.float64, requires_grad=True)
    merlin.aggregate_readouts(readouts, torch.tensor([[1., 0., 0.]], dtype=torch.float64)).sum().backward()
    assert torch.equal(readouts.grad[0, 1:], torch.zeros(2, 2, dtype=torch.float64))
    with pytest.raises(ValueError, match="disjoint"):
        merlin.completed_segment_visibility(torch.tensor([0, 3]), 4, torch.tensor([8]))
    with pytest.raises(ValueError, match="nonnegative"):
        merlin.completed_segment_visibility(starts, True, torch.tensor([8]))


def test_merlin_rejects_negative_variance_or_no_visible_history():
    query, mean = torch.ones(1, 2, dtype=torch.float64), torch.ones(2, 2, dtype=torch.float64)
    second = torch.zeros(2, 2, 2, dtype=torch.float64)
    gate = torch.ones(1, dtype=torch.float64)
    scale = torch.ones((), dtype=torch.float64)
    with pytest.raises(ValueError, match="negative"):
        merlin.routing_weights(query, mean, second, torch.ones(1, 2, dtype=torch.bool), gate, scale, scale)
    with pytest.raises(ValueError, match="visible"):
        merlin.routing_weights(query, mean, second, torch.zeros(1, 2, dtype=torch.bool), gate, scale, scale)


def test_merlin_derived_storage_and_overflow_fail_before_invalid_routing():
    with pytest.raises(ValueError, match="derived"):
        merlin.segment_moments(torch.ones(1, 1, 1025))
    with pytest.raises(ValueError, match="finite"):
        merlin.segment_moments(torch.full((1, 2, 1), 1e30))
    with pytest.raises(ValueError, match="finite"):
        merlin.routing_weights(torch.tensor([[1e20]]), torch.tensor([[1.], [2.]]),
            torch.tensor([[[1.]], [[4.]]]), torch.ones(1, 2, dtype=torch.bool),
            torch.tensor([.5]), torch.tensor(1.), torch.tensor(1.))
    with pytest.raises(ValueError, match="finite"):
        merlin.routing_weights(torch.tensor([[1.]]), torch.tensor([[1e20]]),
            torch.tensor([[[1.]]]), torch.ones(1, 1, dtype=torch.bool),
            torch.tensor([.5]), torch.tensor(1.), torch.tensor(1.))


def test_fold_direction_uses_population_covariance_and_mean_constraint():
    q = torch.tensor([[2., 1.], [4., 2.], [3., 0.], [1., 3.]], dtype=torch.float64)
    fitted = fold_bias.fit_direction(q)
    mean = q.mean(0)
    covariance = sum(torch.outer(row - mean, row - mean) for row in q) / len(q)
    assert torch.equal(fitted["covariance"], covariance)
    a = torch.linalg.solve(covariance + .01 * covariance.trace() / 2 * torch.eye(2, dtype=q.dtype), mean)
    expected = a / (mean @ a)
    assert torch.allclose(fitted["direction"], expected, atol=1e-12, rtol=0)
    assert (q @ expected).mean().item() == pytest.approx(1., abs=1e-12)
    with pytest.raises(ValueError, match="covariance"):
        fold_bias.fit_direction(torch.ones(3, 2, dtype=q.dtype))
    with pytest.raises(ValueError, match="mean"):
        fold_bias.fit_direction(torch.cat((torch.eye(2, dtype=q.dtype), -torch.eye(2, dtype=q.dtype))))


def test_fold_really_rounds_before_refit_and_retains_dimension():
    gen = torch.Generator().manual_seed(7)
    q = torch.randn(25, 4, dtype=torch.float64, generator=gen) + 1
    k = torch.randn(3, 4, dtype=torch.float64, generator=gen)
    bias = torch.tensor([-.7, .2, 1.1], dtype=torch.float64)
    target = torch.randn(25, 2, dtype=torch.float64, generator=gen)
    fit = fold_bias.refit_rounded_cache(q, q, k, bias, target)
    assert fit["keys"].dtype == torch.bfloat16 and fit["keys"].shape == k.shape
    expected_attention = (q @ fit["keys"].to(q.dtype).T / 2).softmax(-1)
    assert torch.equal(expected_attention, fit["reference_attention"])
    expected_values = torch.linalg.pinv(expected_attention) @ target
    assert torch.equal(fit["values"], expected_values)
    wrong_attention = (q @ fit["unrounded_keys"].T / 2).softmax(-1)
    assert not torch.allclose(wrong_attention, expected_attention, atol=1e-6, rtol=0)


def test_fold_logit_identity_and_same_bias_softmax_invariance():
    q = torch.tensor([[1., 0.], [0., 1.]], dtype=torch.float64)
    k = torch.tensor([[1., 2.], [3., 1.]], dtype=torch.float64)
    u = torch.tensor([.5, -.3], dtype=torch.float64)
    beta = torch.ones(2, dtype=torch.float64)
    folded = fold_bias.fold_keys(k, beta, u)
    assert torch.allclose((q @ folded.T / 2**.5).softmax(-1), (q @ k.T / 2**.5 + beta).softmax(-1), atol=1e-12)
    bound = fold_bias.output_error_bound(q, u, beta, torch.eye(2, dtype=q.dtype))
    assert torch.equal(bound, torch.zeros(2, dtype=q.dtype))


def test_fold_derived_storage_and_overflow_are_bounded():
    with pytest.raises(ValueError, match="derived"):
        fold_bias.fit_direction(torch.ones(2, 1025))
    with pytest.raises(ValueError, match="aligned"):
        fold_bias.refit_rounded_cache(torch.ones(2, 1), torch.ones(1025, 1),
            torch.ones(1025, 1), torch.ones(1025), torch.ones(1025, 1))
    with pytest.raises(ValueError, match="finite"):
        fold_bias.fold_keys(torch.ones(2, 1), torch.full((2,), 1e30), torch.full((1,), 1e30))


def test_swim_cyclic_negatives_keep_current_and_actions_fixed():
    model = swim.GatedInverseDynamics(2, 1, 4).double()
    current = torch.tensor([[0., 1.], [2., 4.], [3., 5.], [6., 1.]], dtype=torch.float64)
    later = current + 1
    actions = torch.arange(4, dtype=torch.float64)[:, None]
    hinge = model.stage1_loss(current, later, actions)
    assert torch.equal(hinge["negative_indices"], torch.tensor([[1], [2], [3], [0]]))
    assert torch.equal(hinge["negative_logp"][:, 0], model.action_log_probability(current, later.roll(-1, 0), actions))
    info = model.stage1_loss(current, later, actions, discrimination="infonce", negatives=2)
    assert torch.equal(info["negative_indices"], torch.tensor([[1, 2], [2, 3], [3, 0], [0, 1]]))
    with pytest.raises(ValueError, match="cyclic"):
        model.stage1_loss(current, later, actions, discrimination="infonce", negatives=4)


def test_swim_does_not_gate_current_state_or_restandardize_weighted_coordinates():
    model = swim.GatedInverseDynamics(2, 1, 4).double()
    with torch.no_grad():
        model.alpha.fill_(-100)
    current = torch.tensor([[1., 3.], [2., 4.]], dtype=torch.float64)
    features = model(current, current + 10)["features"]
    assert torch.equal(features[:, :2], current)
    states = torch.tensor([[0., 0.], [2., 4.]], dtype=torch.float64)
    gates = torch.tensor([.25, 1.], dtype=torch.float64, requires_grad=True)
    target = swim.weighted_state_distances(states, torch.tensor([[0, 1]]), gates)
    assert target.item() == 17 and not target.requires_grad
    assert target.item() != 16.25  # g*q would incorrectly square the weights.


def test_swim_pearson_degenerate_target_fails_closed():
    latents = torch.tensor([[1., 2.], [2., 4.], [5., 1.]], dtype=torch.float64)
    pairs = torch.tensor([[0, 1], [1, 2]])
    with pytest.raises(ValueError, match="undefined"):
        swim.latent_state_correlation(latents, pairs, torch.ones(2, dtype=torch.float64))


def test_swim_derived_distances_and_nll_fail_on_overflow():
    with pytest.raises(ValueError, match="finite"):
        swim.weighted_state_distances(torch.tensor([[0.], [1e20]]), torch.tensor([[0, 1]]), torch.ones(1))
    model = swim.GatedInverseDynamics(1, 1, 4)
    with pytest.raises(ValueError, match="finite"):
        model.action_log_probability(torch.ones(2, 1), torch.ones(2, 1), torch.full((2, 1), 1e30))


@pytest.mark.parametrize("module", [merlin, fold_bias, swim])
def test_no_silent_gpu_fallback(module, monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    with pytest.raises(ValueError, match="actual available cuda"):
        module.diagnostic(42, "cuda")
