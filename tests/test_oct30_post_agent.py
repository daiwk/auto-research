from dataclasses import replace

import numpy as np
import pytest
from scipy.optimize import LinearConstraint, minimize
import torch

from auto_research.post_training import concur, mpopd
from auto_research.agent_research import emma, evalalloc


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("tied", [False, True])
def test_concur_projection_matches_independent_convex_problem(seed, tied):
    p = np.array([0., .3, .3, .7, 1., 1.])
    z = np.random.default_rng(seed).normal(size=len(p))
    matrix, lower, upper = [], [], []
    for i in range(len(p)):
        for j in range(len(p)):
            if p[i] > p[j] or (tied and i < j and p[i] == p[j] == 1):
                row = np.zeros(len(p))
                row[i], row[j] = 1, -1
                matrix.append(row)
                lower.append(0)
                upper.append(0 if p[i] == p[j] else np.inf)
    matrix, upper = np.asarray(matrix), np.asarray(upper)
    equal = upper == 0
    constraints = [LinearConstraint(matrix[~equal], 0, np.inf)]
    if equal.any():
        constraints.append(LinearConstraint(matrix[equal], 0, 0))
    solution = minimize(lambda x: (.5 * np.sum((x - z) ** 2), x - z), np.zeros(len(p)),
        jac=True, method="SLSQP", constraints=constraints, options={"ftol": 1e-12})
    assert solution.success
    actual = concur.projected_scores(p, z, tie_ceiling=tied)
    np.testing.assert_allclose(actual, solution.x, atol=1e-7)
    assert actual.sum() == pytest.approx(z.sum())
    assert z @ z == pytest.approx(actual @ actual + (z - actual) @ (z - actual))


def test_concur_below_ceiling_equal_primary_is_not_forced_equal():
    np.testing.assert_array_equal(concur.projected_scores([.3, .3, .7], [-1, 0, 1], tie_ceiling=True), [-1, 0, 1])
    p, z = np.array([1., .3, .3, 1., 0.]), np.array([2., -.3, .2, -1., .9])
    perm = [2, 0, 4, 1, 3]
    np.testing.assert_allclose(concur.projected_scores(p[perm], z[perm], tie_ceiling=True), concur.projected_scores(p, z, tie_ceiling=True)[perm])


def test_concur_batch_trust_includes_current_batch_before_any_projection():
    groups = [dict(task="x", raw_rewards=np.array([[1., .2], [1., .8]]), primary=0, gated_auxiliaries=(1,), weights=[1, 1]),
              dict(task="x", raw_rewards=np.array([[.5, .2], [.8, .8]]), primary=0, gated_auxiliaries=(1,), weights=[1, 1])]
    values, trust = concur.concur_batch(groups, variant="A", trust={("x", 1): concur.EarnedTrust((.4,) * 60)}, batch_std_correction=0)
    assert len(trust["x", 1].readings) == 61 and trust["x", 1].untied
    assert values[0][0] != values[0][1]  # First group also sees later group's current reading.
    tied, _ = concur.concur_batch(groups, variant="T", trust={}, batch_std_correction=0)
    assert tied[0][0] == tied[0][1]
    assert concur.agreement([1, 1, 0], [.2, .8, 0]) is None
    assert not concur.EarnedTrust((.2,) * 60).untied
    assert not concur.EarnedTrust((-.2,) * 61).untied


@pytest.mark.parametrize("bad", [[0, np.nan], [0, 1.1], [-.1, .5]])
def test_concur_refuses_bad_primary(bad):
    with pytest.raises(ValueError):
        concur.projected_scores(bad, [1, 2], tie_ceiling=True)


def test_concur_finite_overflow_is_not_a_pass_and_trust_history_is_immutable():
    with pytest.raises(ValueError):
        concur.projected_scores([0, .5], [1e308, 9e307], tie_ceiling=False)
    with pytest.raises(ValueError):
        concur.projected_scores([1, 1], [1e308, 9e307], tie_ceiling=True)
    original = [.4]
    history = concur.EarnedTrust(original)
    original.append(-1)
    assert history.readings == (.4,)


def tiny_weights():
    old = torch.tensor([[[.8, .2], [.8, .2], [.8, .2]]], dtype=torch.float64).log()
    proposal = torch.tensor([[[.2, .8], [.2, .8], [.2, .8]]], dtype=torch.float64).log()
    mask = torch.ones((1, 3), dtype=torch.bool)
    return old, proposal, mask, mpopd.freeze_rollout_weights(old, proposal, torch.tensor([[0, 1, 0]]), mask)


def test_mpopd_one_step_importance_is_lagged_not_current_or_cumulative():
    _, _, _, snapshot = tiny_weights()
    torch.testing.assert_close(snapshot.prefix_weights, torch.tensor([[1., 4., .25]], dtype=torch.float64))
    student = torch.tensor([[[.6, .4]] * 3], dtype=torch.float64).log().requires_grad_()
    teacher = torch.tensor([[[.3, .7]] * 3], dtype=torch.float64).log().requires_grad_()
    single = (.6 * np.log(.6 / .3) + .4 * np.log(.4 / .7))
    loss = mpopd.student_loss(student, teacher, snapshot, top_k=2)
    assert float(loss.detach()) == pytest.approx(single * (1 + 4 + .25))
    loss.backward()
    assert student.grad.norm() > 0 and teacher.grad is None


def test_mpopd_both_reverse_kl_gradients_and_geometric_endpoints():
    rng = torch.Generator().manual_seed(12)
    s, t, q = [torch.randn((1, 2, 5), generator=rng, dtype=torch.float64) for _ in range(3)]
    mask = torch.ones((1, 2), dtype=torch.bool)
    weights = mpopd.freeze_rollout_weights(s, q, torch.tensor([[1, 2]]), mask)
    assert torch.autograd.gradcheck(lambda a: mpopd.student_loss(a, t, weights, top_k=4), (s.requires_grad_(),))
    assert torch.autograd.gradcheck(lambda a: mpopd.proposal_loss(a, s, t, mask, eta=.4, top_k=4), (q.requires_grad_(),))
    for eta, source in [(0, s), (1, t)]:
        target, ids = mpopd.tilted_log_target(s, t, mask, eta=eta, top_k=4)
        expected = source.detach().gather(-1, ids).log_softmax(-1)
        torch.testing.assert_close(target, expected)
    target, ids = mpopd.tilted_log_target(s, t, mask, eta=.4, top_k=4)
    logq = q.gather(-1, ids).log_softmax(-1)
    expected = (logq.exp() * (logq - target)).sum()
    torch.testing.assert_close(mpopd.proposal_loss(q, s, t, mask, eta=.4, top_k=4), expected)


def test_mpopd_padding_is_ignored_but_nonprefix_masks_and_active_nan_refused():
    s = torch.randn(1, 3, 4, dtype=torch.float64)
    mask = torch.tensor([[True, True, False]])
    s[:, -1] = torch.nan
    teacher = s.clone()
    snapshot = mpopd.freeze_rollout_weights(s, teacher, torch.tensor([[0, 1, -99]]), mask)
    current = s.clone().requires_grad_()
    mpopd.student_loss(current, teacher, snapshot, top_k=3).backward()
    assert torch.equal(current.grad[:, -1], torch.zeros_like(current.grad[:, -1]))
    with pytest.raises(ValueError):
        mpopd.freeze_rollout_weights(s, teacher, torch.tensor([[0, 1, 0]]), torch.tensor([[True, False, True]]))
    with pytest.raises(ValueError):
        mpopd.tilted_log_target(s, teacher, torch.ones_like(mask), eta=.5, top_k=3)


@pytest.mark.parametrize("fault", ["eta", "clip", "first_weight", "gradient", "support"])
def test_mpopd_invalid_contract_is_fail_closed(fault):
    old, proposal, mask, snapshot = tiny_weights()
    with pytest.raises(ValueError):
        if fault == "eta": mpopd.tilted_log_target(old, proposal, mask, eta=float("nan"), top_k=2)
        elif fault == "clip": mpopd.freeze_rollout_weights(old, proposal, torch.tensor([[0, 1, 0]]), mask, clip=True)
        elif fault == "first_weight": mpopd.RolloutWeights(torch.full((1, 3), 2.), mask, 5.)
        elif fault == "gradient": mpopd.RolloutWeights(torch.ones((1, 3), requires_grad=True), mask, 5.)
        else: mpopd.student_loss(old, proposal, snapshot, top_k=3)


def memory_and_context():
    memory = emma.EpisodicMemory({"generalist": "a\nb\nc\nd\ne"})
    safety = emma.ExternalSafety(True, True, True, True, True, True)
    context = emma.EditContext("public task only", frozenset({"generalist"}), (), False, True, True, safety)
    return memory, context


def test_emma_prompt_retention_participation_and_dynamic_inheritance():
    memory, context = memory_and_context()
    prompt = emma.Edit("agent_behavior", "refine_prompt", "generalist", "a\nb\nc\nnew")
    updated = emma.apply_guarded_edit(memory, prompt, context).memory
    assert updated.agents["generalist"] == "a\nb\nc\nnew" and memory.agents["generalist"] == "a\nb\nc\nd\ne"
    for bad in [replace(prompt, content="a\nb\nnew"), replace(prompt, target="not-participating")]:
        with pytest.raises(ValueError):
            emma.apply_guarded_edit(memory, bad, context)
    specialized = emma.apply_guarded_edit(memory, emma.Edit("missing_capability", "create_agent", "expert", "An explicit reusable working method. " * 6, "narrow role"), context).memory
    assert specialized.prompt_for("expert").startswith(memory.agents["generalist"])


@pytest.mark.parametrize("change", ["inference", "no-rerun", "scope", "rotation", "answer", "overflow", "duplicate", "path"])
def test_emma_guarded_update_negative_controls(change):
    memory, context = memory_and_context()
    edit = emma.Edit("procedure", "create_skill", "units", "Reusable dimensional checks.", "unit checks")
    if change == "inference": context = replace(context, training=False)
    if change == "no-rerun": context = replace(context, rerun_available=False)
    if change == "scope": edit = replace(edit, scope="agent_behavior")
    if change == "rotation": context = replace(context, failed_levels=("skill", "skill"))
    if change == "answer": context = replace(context, safety=replace(context.safety, reference_answer_absent=False))
    if change == "overflow": context = replace(context, repeated_step_overflow=True)
    if change == "duplicate": context = replace(context, safety=replace(context.safety, semantic_duplicate_absent=False))
    if change == "path": context = replace(context, safety=replace(context.safety, dataset_or_run_paths_absent=False))
    with pytest.raises(ValueError): emma.apply_guarded_edit(memory, edit, context)
    assert not memory.skills


def test_emma_verbatim_task_leak_unused_edit_and_overflow_prefix():
    memory, context = memory_and_context()
    task = " ".join(f"word{i}" for i in range(16))
    with pytest.raises(ValueError):
        emma.apply_guarded_edit(memory, emma.Edit("procedure", "create_skill", "s", task, "description"), replace(context, public_task=task))
    result = emma.apply_guarded_edit(memory, emma.Edit("procedure", "create_skill", "s", "A reusable method.", "description"), context)
    with pytest.raises(ValueError): emma.assert_exercised(result, agents={"generalist"}, skills=set())
    plan = (emma.Step("generalist", "done"), emma.Step("generalist", "unfinished"), emma.Step("generalist", "future"))
    updated = emma.splice_overflow(plan, 1, (emma.Step("generalist", "part1"), emma.Step("generalist", "part2")), memory)
    assert updated[:1] == plan[:1] and updated[-1:] == plan[-1:]
    with pytest.raises(ValueError): emma.splice_overflow(plan, 1, (emma.Step("imaginary", "part"),), memory)


def test_evalalloc_beta_moment_and_fractional_failure_acquisition():
    # Uniform Beta(1,1): E[p(1-p)]=1/6, Var=1/180.
    assert evalalloc.informativeness([0], [0])[0] == pytest.approx(4 * (1 / 6 - 2 / np.sqrt(180)))
    values = evalalloc.informativeness([0, 5, 10], [10, 10, 10])
    assert values[1] > values[0] and values[1] > values[2]
    with pytest.raises(ValueError): evalalloc.informativeness([.5], [2])


def test_evalalloc_map_only_candidate_changes_and_known_observations_override_predictions():
    model = evalalloc.FrozenItemModel(np.zeros(4), np.array([[0], [1], [2], [3.]]), np.zeros(2), np.eye(2), frozenset({"pilot"}))
    original = model.item_loadings.copy()
    predictions, params = evalalloc.infer_candidate(model, "new", {0: 1., 2: .5})
    np.testing.assert_array_equal(model.item_loadings, original)
    assert params.shape == (2,) and np.isfinite(params).all()
    expected = (1 + .5 + predictions[1] + predictions[3]) / 4
    assert evalalloc.completed_fitness(predictions, {0: 1., 2: .5}) == pytest.approx(expected)
    with pytest.raises(ValueError): evalalloc.infer_candidate(model, "pilot", {0: 1.})
    with pytest.raises(ValueError): model.item_loadings[0, 0] = 12


def test_evalalloc_paired_union_budget_and_crossfit_negative_control():
    scores = evalalloc.informativeness([0, 3, 5, 7, 10], [10] * 5)
    core = evalalloc.shared_core(scores, size=2)
    selected = evalalloc.acquire(scores, core, total=4, seed=42)
    assert selected[:2] == core and len(set(selected)) == 4
    cache = {"a": {0: .2, 4: 1.}, "b": {0: .8}}
    cells = evalalloc.plan_paired_round(cache, (0, 1, 2), n_items=5, remaining_budget=4)
    assert len(cells) == 4 and all(i not in cache[c] for c, i in cells)
    with pytest.raises(ValueError): evalalloc.plan_paired_round(cache, (0, 1, 2), n_items=5, remaining_budget=3)
    updated = evalalloc.accept_round_results(cache, cells, {cell: .5 for cell in cells})
    assert updated["a"][4] == 1 and 1 not in cache["a"]
    with pytest.raises(ValueError): evalalloc.accept_round_results(cache, cells, {**{cell: .5 for cell in cells}, ("a", 99): 1})
    pred = {c: np.linspace(.1, .9, 5) for c in cache}
    with pytest.raises(ValueError): evalalloc.regression_adjusted_scores(updated, pred, {"a": frozenset({"a"}), "b": frozenset({"a"})}, first_round=False)
    adjusted, slope = evalalloc.regression_adjusted_scores(updated, pred, {"a": frozenset({"b"}), "b": frozenset({"a"})}, first_round=False)
    assert set(adjusted) == {"a", "b"} and 0 <= slope <= 1.5


def test_evalalloc_large_counts_and_hidden_sigmoid_overflow_fail_closed():
    for count in (1e308, 2**53 + 1):
        with pytest.raises(ValueError):
            evalalloc.informativeness([count], [count])
    model = evalalloc.FrozenItemModel(np.array([1e308, 1e308]), np.array([[1e308], [1e308]]),
        np.array([1e308, 1e308]), np.eye(2), frozenset({"pilot"}))
    with pytest.raises(ValueError):
        evalalloc.infer_candidate(model, "new", {0: 1.})


def test_external_provenance_and_context_collections_are_copied():
    fitted = {"pilot"}
    model = evalalloc.FrozenItemModel(np.zeros(2), np.ones((2, 1)), np.zeros(2), np.eye(2), fitted)
    fitted.add("new")
    assert model.fit_candidates == frozenset({"pilot"})
    memory, context = memory_and_context()
    levels, participants = ["skill"], {"generalist"}
    captured = replace(context, failed_levels=levels, participating_agents=participants)
    levels.append("skill")
    participants.clear()
    assert captured.failed_levels == ("skill",) and captured.participating_agents == frozenset({"generalist"})
    assert memory.prompt_for("generalist")


@pytest.mark.parametrize("module", [concur, mpopd, emma, evalalloc])
def test_oct30_diagnostics_have_actual_native_true_checks(module):
    for seed in (42, 43, 44):
        result = module.diagnostic(seed)
        assert result["seed"] == seed and result["diagnostic_only"]
        assert all(type(value) is bool and value for value in result["checks"].values())
        assert all(np.isfinite(value) for value in result["metrics"].values())
