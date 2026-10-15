from __future__ import annotations

import math

import pytest

torch = pytest.importorskip("torch")

from auto_research.reproductions.oob_regularization.algorithm import (  # noqa: E402
    GaussianAnchors, SphericalAnchors, alignment_loss, gaussian_quantile_targets,
    in_batch_gaussian_loss, simclr_loss, spherical_objective, unit_projections,
)
from auto_research.reproductions.oob_regularization.experiment import (  # noqa: E402
    load_public_images, run_comparison,
)


def test_quantiles_follow_population_rank_not_minibatch_moments():
    projected = torch.tensor([[3., 1.], [1., 4.], [2., 3.], [4., 2.]], requires_grad=True)
    actual = gaussian_quantile_targets(projected)
    grid = torch.tensor([math.sqrt(2) * torch.erfinv(torch.tensor(2 * (k + .5) / 4 - 1)).item()
                         for k in range(4)])
    torch.testing.assert_close(actual[:, 0], grid[torch.tensor([2, 0, 1, 3])])
    torch.testing.assert_close(actual[:, 1], grid[torch.tensor([0, 3, 2, 1])])
    assert not actual.requires_grad
    assert not torch.equal(actual[:2], gaussian_quantile_targets(projected[:2]))


def test_gaussian_cache_is_detached_cpu_indexed_and_refresh_frozen():
    z = torch.tensor([[3., 1.], [1., 4.], [2., 3.], [4., 2.]], requires_grad=True)
    directions = torch.eye(2)
    cache = GaussianAnchors.build(z, directions, step=7)
    expected = cache.targets.clone()
    indices = torch.tensor([2, 0])
    live = z.detach()[indices].clone().requires_grad_()
    loss = cache.loss(live, indices)
    loss.backward()
    torch.testing.assert_close(live.grad, 2 * (live.detach() - expected[indices]) / live.numel())
    assert cache.targets.device.type == "cpu" and not cache.targets.requires_grad
    assert cache.refresh_step == 7
    with torch.no_grad():
        z.add_(100)
        directions.zero_()
    torch.testing.assert_close(cache.targets, expected)
    torch.testing.assert_close(cache.directions, torch.eye(2))
    with pytest.raises(ValueError, match="outside"):
        cache.loss(live, torch.tensor([0, 4]))


def test_fresh_gaussian_cache_matches_full_population_gradient():
    generator = torch.Generator().manual_seed(12)
    first = torch.randn(9, 4, generator=generator).requires_grad_()
    second = first.detach().clone().requires_grad_()
    directions = unit_projections(4, 5, seed=8)
    cache = GaussianAnchors.build(first, directions)
    cache.loss(first, torch.arange(9)).backward()
    in_batch_gaussian_loss(second, directions).backward()
    torch.testing.assert_close(first.grad, second.grad)


def test_one_sample_online_batch_has_nontrivial_global_targets():
    z = torch.tensor([[-2., 3.], [0., 0.], [2., -3.]])
    cache = GaussianAnchors.build(z, torch.eye(2))
    probe = torch.zeros(1, 2, requires_grad=True)
    cache.loss(probe, torch.tensor([0])).backward()
    assert torch.count_nonzero(probe.grad) == 2
    assert gaussian_quantile_targets(probe).tolist() == [[0., 0.]]


def test_spherical_exact_objective_has_no_self_pairs():
    anchors = torch.tensor([[1., 0.], [0., 1.]])
    loss = spherical_objective(anchors, anchors)
    torch.testing.assert_close(loss, torch.tensor(-4.))
    with pytest.raises(ValueError):
        spherical_objective(anchors[:1], anchors[:1])


def test_spherical_cache_is_actual_optimized_unit_norm_and_supports_resume_refresh():
    z = torch.tensor([[1., .1], [1., -.1], [.9, .1], [.9, -.1]])
    cache = SphericalAnchors.build(z, seed=19, steps=5, subset_size=4)
    assert not cache.targets.requires_grad and cache.optimization_steps == 5
    torch.testing.assert_close(cache.targets.norm(dim=-1), torch.ones(4))
    assert not torch.allclose(cache.targets, torch.nn.functional.normalize(z, dim=1))
    next_cache = SphericalAnchors.build(z, seed=20, step=8, previous=cache, steps=2, subset_size=4)
    assert next_cache.refresh_step == 8
    probe = z[:2].clone().requires_grad_()
    next_cache.loss(probe, torch.tensor([0, 1])).backward()
    assert torch.isfinite(probe.grad).all() and torch.count_nonzero(probe.grad) > 0


def test_view_alignment_and_simclr_use_real_differentiable_pairs():
    first = torch.tensor([[1., .2], [.1, 1.]], requires_grad=True)
    second = first.detach().flip(0).clone().requires_grad_()
    value = simclr_loss(first, second) + alignment_loss(first, second)
    value.backward()
    assert float(value.detach()) > 0 and torch.count_nonzero(first.grad) > 0
    with pytest.raises(ValueError):
        simclr_loss(first[:1], second[:1])


def test_untrusted_pickle_rejected_before_deserialization(tmp_path, monkeypatch):
    (tmp_path / "data_batch_1").write_bytes(b"not official CIFAR")
    monkeypatch.setattr("pickle.loads", lambda *args, **kwargs: pytest.fail("unverified pickle was read"))
    with pytest.raises(ValueError, match="checksum"):
        load_public_images(tmp_path, training=8, validation=4)
    assert not (tmp_path / "test_batch").exists()


def test_small_real_training_protocol_and_pairing_with_fixture_images(tmp_path, monkeypatch):
    # A declared unit fixture exercises the runtime, never becomes paper evidence.
    torch.set_num_threads(1)
    images = torch.rand(16, 3, 32, 32)
    labels = torch.arange(16) % 10
    monkeypatch.setattr("auto_research.reproductions.oob_regularization.experiment.load_public_images",
                        lambda *a, **k: (images[:12], labels[:12], images[12:], labels[12:],
                                         {"official_test_read": False, "fixture_only": True}))
    result = run_comparison(tmp_path, seed=3, steps=2, batch_size=4, refresh_interval=1)
    assert result["diagnostic_only"] and not result["promotion_eligible"]
    assert len(result["metrics"]) == 4
    for arm, row in result["metrics"].items():
        assert row["optimizer_steps"] == 2 and row["parameter_update_observed"]
        assert row["refreshes"] == (2 if arm.endswith("oob") else 0)
        assert row["cached_targets_require_grad"] is False


def test_bounds_reject_before_loading_data(tmp_path):
    for kwargs in ({"steps": 121}, {"maximum_seconds": 3600}, {"batch_size": 1}, {"device": "mps"}):
        with pytest.raises(ValueError):
            run_comparison(tmp_path, **kwargs)
