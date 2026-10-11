from copy import deepcopy

import pytest
import torch

from auto_research.foundation.data_space_iteration import (
    DMDTrainer, DataSpaceGenerator, FakeFlowNetwork, SmallFlowNetwork,
    distribution_matching_loss, flow_matching_loss, rollout_data_space,
    rollout_flow_renoise, FlowRenoiseGenerator,
)


def models():
    torch.manual_seed(42)
    teacher = SmallFlowNetwork(width=4, depth=1)
    return teacher, DataSpaceGenerator(teacher), FakeFlowNetwork(teacher)


def test_shared_noise_zero_start_and_only_final_step_has_grad():
    noise = torch.randn(2, 3, 4, 4)
    calls = []
    weight = torch.nn.Parameter(torch.tensor(2.))

    def generator(current, z, r):
        calls.append((current.clone(), z.data_ptr(), r, torch.is_grad_enabled()))
        return current + z * weight

    output = rollout_data_space(generator, noise, 2, track_grad=True)
    assert torch.equal(calls[0][0], torch.zeros_like(noise))
    assert [x[1] for x in calls] == [noise.data_ptr()] * 3
    assert [x[2:] for x in calls] == [(0, False), (1, False), (2, True)]
    output.sum().backward()
    assert torch.allclose(weight.grad, noise.sum())  # detached prefix, not BPTT


def test_generator_copies_teacher_and_fix_time_one():
    teacher, generator, fake = models()
    for name, value in teacher.state_dict().items():
        assert torch.equal(value, generator.backbone.state_dict()[name])
        assert torch.equal(value, fake.backbone.state_dict()[name])
    noise = torch.randn(2, 3, 4, 4)
    generator.estimate.weight.data.zero_()
    generator.step.weight.data.zero_()
    expected = noise - teacher(noise, torch.ones(2))
    assert torch.allclose(generator(torch.randn_like(noise), noise, 0), expected)


def test_dmd_exact_direction_and_no_teacher_fake_gradients():
    teacher, generator, fake = models()
    data, noise, epsilon = [torch.randn(2, 3, 4, 4) for _ in range(3)]
    time = torch.tensor([.2, .8])
    predicted = generator(torch.zeros_like(noise), noise, 0)
    noisy = (1 - time[:, None, None, None]) * predicted + time[:, None, None, None] * epsilon
    direction = (teacher(noisy, time) - fake(noisy, time, 0)).detach()
    loss = distribution_matching_loss(generator, teacher, fake, data, 0,
        generator_update=True, noise=noise, epsilon=epsilon, time=time)
    assert torch.allclose(loss, (predicted * direction).mean())
    loss.backward()
    assert any(p.grad is not None for p in generator.parameters())
    assert all(p.grad is None for p in teacher.parameters())
    assert all(p.grad is None for p in fake.parameters())


def test_fake_tracks_generated_distribution_not_real_data():
    teacher, generator, fake = models()
    shape, noise, epsilon = [torch.randn(2, 3, 4, 4) for _ in range(3)]
    time = torch.tensor([.3, .7])
    loss = distribution_matching_loss(generator, teacher, fake, shape, 1,
        generator_update=False, noise=noise, epsilon=epsilon, time=time)
    changed = distribution_matching_loss(generator, teacher, fake, shape + 100, 1,
        generator_update=False, noise=noise, epsilon=epsilon, time=time)
    assert torch.equal(loss, changed)
    loss.backward()
    assert all(p.grad is None for p in generator.parameters())
    assert any(p.grad is not None for p in fake.parameters())


def test_four_fake_updates_one_generator_ema_and_cycling():
    teacher, generator, fake = models()
    initial = deepcopy(generator.state_dict())
    trainer = DMDTrainer(generator, teacher, fake,
        torch.optim.Adam(generator.parameters(), lr=1e-3, betas=(0., .95)),
        torch.optim.Adam(fake.parameters(), lr=1e-3, betas=(0., .95)), ema_decay=.5)
    rows = [trainer.step(torch.randn(2, 3, 4, 4)) for _ in range(5)]
    assert [r['refinement'] for r in rows] == [0, 1, 2, 3, 0]
    assert all(len(r['fake_losses']) == 4 for r in rows)
    assert all(r['generator_gradient_norm'] > 0 for r in rows)
    assert any(not torch.equal(v, generator.state_dict()[k]) for k, v in initial.items())
    assert all(p.grad is None and not p.requires_grad for p in teacher.parameters())
    assert all(p.grad is None for p in fake.parameters())
    assert any(not torch.equal(v, trainer.ema.state_dict()[k]) for k, v in initial.items())


def test_teacher_flow_target_and_negative_rollout_errors():
    images, noise = torch.ones(2, 3, 4, 4), torch.zeros(2, 3, 4, 4)
    loss = flow_matching_loss(lambda x, t: -torch.ones_like(x), images,
                              noise=noise, time=torch.tensor([.2, .9]))
    assert loss == 0
    with pytest.raises(ValueError):
        rollout_data_space(None, images, -1)
    with pytest.raises(ValueError):
        rollout_flow_renoise(None, images, 4)


def test_flow_renoise_is_separate_baseline_and_dmd_time_guard():
    teacher, _, _ = models()
    gen = FlowRenoiseGenerator(teacher)
    value = rollout_flow_renoise(gen, torch.randn(2, 3, 4, 4), 1, track_grad=True)
    value.mean().backward()
    assert any(p.grad is not None for p in gen.parameters())
    teacher, generator, fake = models()
    with pytest.raises(ValueError, match='strictly'):
        distribution_matching_loss(generator, teacher, fake, value, 0,
            generator_update=True, time=torch.tensor([0., 1.]))
