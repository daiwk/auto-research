"""Source-specific CoLiR and VisAlloc formula, mask and negative controls."""

import pytest

torch = pytest.importorskip("torch")

from auto_research.post_training import colir_replay as colir  # noqa: E402
from auto_research.post_training import visalloc as va  # noqa: E402


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("module", [colir, va])
def test_seeded_cpu_diagnostic(seed, module):
    result = module.diagnostic(seed)
    assert result["diagnostic_only"]
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(result["checks"].values())


def test_colir_distinct_response_sets_and_equal_half_weights():
    a = torch.tensor([[-1., -2.]])
    b = torch.tensor([[-3., -20.]])
    c = torch.tensor([[-10., -8., -4.]])
    d = torch.tensor([[-7., -3., -30.]])
    score, eligible = colir.contrastive_scores(a, b, c, d,
                                              torch.tensor([[False, True]]),
                                              torch.tensor([[True, True, False]]))
    assert eligible.tolist() == [True]
    # Correct final responses: mean gain (3+5)/2; incorrect initial: suppression 2.
    assert score.item() == 3


def test_colir_does_not_pick_all_correct_or_all_wrong_final_groups():
    p = torch.zeros(3, 2)
    score, eligible = colir.contrastive_scores(p, p, p, p,
        torch.tensor([[False, False], [False, False], [True, True]]),
        torch.tensor([[True, True], [False, False], [True, False]]))
    assert not eligible.any()
    assert colir.select_task_memory(["a", "b", "c"], score, eligible) == ()


def test_colir_topk_is_per_task_and_deterministic_on_ties():
    assert colir.select_task_memory(["z", "a", "b"], torch.tensor([2., 2., 100.]),
                                    torch.tensor([True, True, False]), budget=1) == ("z",)
    assert colir.sample_replay(["a", "b"], 2, 42) == colir.sample_replay(["a", "b"], 2, 42)


def test_colir_task_sampling_does_not_flatten_unequal_buffers():
    memory = {"small": ["a"], "large": [str(i) for i in range(80)], "empty": []}
    sampled = colir.sample_historical_tasks(memory, 1000, 42)
    assert all(prompt in memory[task] for task, prompt in sampled)
    small = sum(task == "small" for task, _ in sampled)
    assert 400 < small < 600  # Flat prompt sampling would allocate about 1/81.
    assert sampled == colir.sample_historical_tasks(memory, 1000, 42)


@pytest.mark.parametrize("budget", [-1, True, 1.5])
def test_colir_invalid_budget_rejected(budget):
    with pytest.raises(ValueError):
        colir.select_task_memory(["a"], torch.tensor([1.]), torch.tensor([True]), budget=budget)


def test_sample_filter_requires_correct_positive_and_incorrect_negative():
    assert va.sample_filter(torch.tensor([True, True, False, True]),
                            torch.tensor([True, False, True, True]),
                            torch.tensor([False, False, False, True])).tolist() == [True, False, False, False]


def test_coarsened_support_comes_from_student_not_teacher():
    s = torch.tensor([[[5., 1., 0., -1.]]], dtype=torch.float64, requires_grad=True)
    t = torch.tensor([[[-2., -1., 1., 5.]]], dtype=torch.float64, requires_grad=True)
    n = torch.zeros_like(t, requires_grad=True)
    actual, _, p, q, _ = va.coarsened_jsd(s, t, n, k=1)
    a, b = p[..., 0].exp(), q[..., 0].exp()
    pp = torch.stack([a, 1-a], -1)
    qq = torch.stack([b, 1-b], -1)
    mm = (pp+qq)/2
    expected = .5*((pp*(pp.log()-mm.log())).sum(-1)+(qq*(qq.log()-mm.log())).sum(-1))
    assert torch.allclose(actual, expected)
    actual.sum().backward()
    assert s.grad.abs().sum() > 0 and t.grad is None and n.grad is None


def test_topk_tail_is_not_renormalized_singleton():
    s = torch.tensor([[[2., 0., 0.]]], dtype=torch.float64)
    t = torch.zeros_like(s)
    j, _, _, _, _ = va.coarsened_jsd(s, t, t, k=1)
    assert j.item() > 0  # Renormalized singleton distributions would give zero.


@pytest.mark.parametrize("k", [0, True, 3, 4])
def test_invalid_coarsening_support_rejected(k):
    x = torch.zeros(1, 2, 3)
    with pytest.raises(ValueError):
        va.coarsened_jsd(x, x, x, k=k)


def _allocation_inputs():
    ids = torch.tensor([[0, 1, 2, 3, 4, 5]])
    x = torch.zeros(1, 6, dtype=torch.float64)
    pos = torch.tensor([[.1, .2, .3, .4, .5, 10.]], dtype=x.dtype)
    j = torch.tensor([[.1, .2, .3, .4, .5, .9]], dtype=x.dtype)
    h = torch.tensor([[.01, .02, .03, .04, .05, .9]], dtype=x.dtype)
    mask = torch.ones(1, 6, dtype=torch.bool)
    rates = torch.full((6,), .3, dtype=x.dtype)
    counts = torch.arange(6, dtype=x.dtype)
    return ids, x, pos, x, j, h, mask, rates, counts


def test_allocation_valid_only_quantiles_ignore_padding_extremes():
    inputs = list(_allocation_inputs())
    inputs[6][0, -1] = False
    a, ia = va.allocation(*inputs)
    for at in [1, 2, 3, 4, 5]:
        inputs[at] = inputs[at].clone()
        inputs[at][0, -1] = 1e100
    b, ib = va.allocation(*inputs)
    assert torch.allclose(a, b)
    assert ia["tau"] == ib["tau"]
    assert ia["theta_j"] == ib["theta_j"]


def test_template_rate_and_positive_loss_gates_cannot_be_bypassed_by_disagreement():
    args = list(_allocation_inputs())
    _, open_info = va.allocation(*args)
    assert open_info["eligible"][0, -1]
    args[7][-1] = .1
    _, low_rate = va.allocation(*args)
    assert not low_rate["eligible"][0, -1]
    args[7][-1] = .3
    _, template = va.allocation(*args, template_pairs=frozenset({(4, 5)}))
    assert not template["eligible"][0, -1]
    args[4] = torch.zeros_like(args[4])
    _, zero_jsd = va.allocation(*args)
    assert not zero_jsd["eligible"].any()
    assert zero_jsd["bonus"].sum() == 0


def test_missing_negative_is_neutral_and_zero_budget_remains_zero():
    args = list(_allocation_inputs())
    args[6][:] = False
    w, info = va.allocation(*args)
    assert (w == 1).all() and info["bonus"].sum() == 0


def test_tiny_frequency_budget_preserved_without_epsilon_floor():
    x = torch.tensor([[1e-30, 1e-30]], dtype=torch.float64)
    y = va.redistribute_bonus(x, torch.tensor([0., 1000.], dtype=x.dtype),
                              torch.tensor([[0, 1]]), torch.ones_like(x, dtype=torch.bool))
    assert y.sum().item()/x.sum().item() == pytest.approx(1)
    assert y[0, 0] > y[0, 1]
    assert not va.redistribute_bonus(x*0, torch.zeros(2), torch.tensor([[0, 1]]),
                                     torch.ones_like(x, dtype=torch.bool)).any()


def test_frozen_prior_unseen_rate_and_per_response_template_count():
    ids = torch.tensor([[0, 1, 0, 1], [2, 3, 2, 3], [2, 3, 2, 3], [2, 3, 2, 3], [2, 3, 2, 3]])
    x = torch.zeros_like(ids, dtype=torch.float64)
    rates, counts, templates = va.frozen_priors(ids, x, x, x, torch.ones_like(ids, dtype=torch.bool), vocab_size=5)
    assert rates[4].item() == .1 and counts[4].item() == 0
    assert (0, 1) not in templates  # repeated twice in one of five responses != 40%.
    assert (2, 3) in templates


def test_visalloc_loss_freezes_coefficients_and_keeps_baseline_without_negative_view():
    torch.manual_seed(7)
    s = torch.randn(2, 3, 5, dtype=torch.float64, requires_grad=True)
    p = torch.randn_like(s, requires_grad=True)
    n = torch.randn_like(s, requires_grad=True)
    ids = torch.tensor([[0, 1, 2], [1, 2, 3]])
    mask = torch.tensor([[True, True, False], [True, True, False]])
    old = torch.full((2, 3), -2., dtype=s.dtype, requires_grad=True)
    old.data[~mask] = -1e100
    rates = torch.full((5,), .3, dtype=s.dtype, requires_grad=True)
    counts = torch.ones(5, dtype=s.dtype, requires_grad=True)
    correction = torch.ones(2, 3, dtype=s.dtype, requires_grad=True)
    value, w, _ = va.loss(s, p, n, ids, old, mask, torch.tensor([False, False]),
                          rates, counts, k=2, rollout_correction=correction)
    value.backward()
    assert torch.isfinite(value) and (w == 1).all()
    assert (s.grad[~mask] == 0).all() and s.grad[mask].abs().sum() > 0
    assert all(x.grad is None for x in [p, n, old, rates, counts, correction])
