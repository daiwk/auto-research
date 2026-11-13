"""Source-bound negative controls for the eight COLM historical components."""
from importlib import import_module
from itertools import permutations
from math import isfinite

import numpy as np
import pytest
import torch
from torch import nn

from auto_research.agent_research import planning_optimality as planning
from auto_research.foundation_models import continuousbench as cb
from auto_research.foundation_models import ecg_rag as ecg
from auto_research.foundation_models import latent_generalization as latent
from auto_research.foundation_models import lidas
from auto_research.foundation_models import llm_stochasticity as stochastic
from auto_research.foundation_models import rosetta_unification as rosetta
from auto_research.foundation_models import thinking_to_recall as recall

MODULES = ["foundation_models." + x for x in ["rosetta_unification", "lidas", "thinking_to_recall", "latent_generalization", "llm_stochasticity", "ecg_rag", "continuousbench"]] + ["agent_research.planning_optimality"]


@pytest.mark.parametrize("module", MODULES)
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_contract(module, seed):
    implementation = import_module("auto_research." + module)
    assert implementation.REQUIRES_GPU_VALIDATION is (module in {"foundation_models.lidas", "foundation_models.ecg_rag"})
    result = implementation.diagnostic(seed, "cpu")
    assert result["seed"] == seed and result["device"] == "cpu"
    assert result["diagnostic_only"] and result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(type(v) is bool and v for v in result["checks"].values())
    assert result["metrics"] and all(isinstance(v, (int, float)) and isfinite(v) for v in result["metrics"].values())


@pytest.mark.parametrize("module", [m for m in MODULES if m not in ["foundation_models.lidas", "foundation_models.ecg_rag"]])
def test_cpu_evaluators_reject_cuda(module):
    with pytest.raises(ValueError):
        import_module("auto_research." + module).diagnostic(42, "cuda")


@pytest.mark.parametrize("module", [lidas, ecg])
@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.skipif(not torch.cuda.is_available(), reason="requires a real NVIDIA CUDA device")
def test_real_cuda_diagnostic(module, seed):
    result = module.diagnostic(seed, "cuda")
    assert all(result["checks"].values()) and result["device"] == "cuda"


def test_lidas_index_order_and_odd_blocks():
    assert lidas.growth_indices(8) == ((2, 3, 4, 5), 6)
    assert lidas.growth_indices(12) == ((4, 5, 6, 7), 8)
    for n in [0, -4, 5, True]:
        with pytest.raises(ValueError):
            lidas.growth_indices(n)


def test_lidas_preserves_scheduler_groups_and_deep_copies_all_adam_state():
    layers = nn.ModuleList([nn.Linear(2, 2) for _ in range(8)])
    extra = nn.Parameter(torch.ones(2))
    optimizer = torch.optim.AdamW([{"params": list(layers.parameters()), "lr": .02}, {"params": [extra], "lr": .07}], amsgrad=True)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 3)
    sum(p.square().sum() for p in layers.parameters()).backward(); optimizer.step(); scheduler.step()
    before = scheduler.last_epoch
    grown = lidas.grow_layers(layers, optimizer)
    old, new = layers[2].weight, grown[6].weight
    assert len(optimizer.param_groups) == 2 and scheduler.last_epoch == before
    assert optimizer.param_groups[1]["params"][0] is extra
    for field in ["step", "exp_avg", "exp_avg_sq", "max_exp_avg_sq"]:
        a, b = optimizer.state[old][field], optimizer.state[new][field]
        assert torch.equal(a, b) and a.data_ptr() != b.data_ptr()
    optimizer.state[new]["exp_avg"].add_(1)
    assert not torch.equal(optimizer.state[new]["exp_avg"], optimizer.state[old]["exp_avg"])


def test_lidas_rejects_tied_layers_without_mutation():
    layer = nn.Linear(2, 2); layers = nn.ModuleList([layer] * 4)
    optimizer = torch.optim.AdamW(layers.parameters())
    before = len(optimizer.param_groups[0]["params"])
    with pytest.raises(ValueError):
        lidas.grow_layers(layers, optimizer)
    assert len(optimizer.param_groups[0]["params"]) == before


def test_prop1_budget_and_order():
    assert lidas.prop1_schedule(10, 4) == (1, 2, 3, 4)
    assert sum(lidas.prop1_schedule(170000, 8)) == 170000
    with pytest.raises(ValueError):
        lidas.prop1_schedule(2, 4)


def test_ecg_mean_maxsim_not_sum_or_unit_normalized():
    q = torch.tensor([[[2., 0.], [0., 3.]]])
    d = torch.tensor([[[[1., 0.], [0., 1.]]]])
    assert ecg.mean_maxsim(q, d).item() == 2.5


def test_ecg_losses_have_correct_orientation_sum_mask_and_gradients():
    student = torch.tensor([[[2., 0.], [0., 2.]]], requires_grad=True)
    teacher = torch.tensor([[[0., 2.], [2., 0.]]], requires_grad=True)
    scores = torch.tensor([[3., 1., -2.]], requires_grad=True)
    ts = torch.tensor([[5., 1., -1.]], requires_grad=True)
    tau = torch.tensor(2., requires_grad=True); alpha = torch.tensor(.5, requires_grad=True)
    result = ecg.joint_loss(student, teacher, scores, ts, torch.tensor([0]), torch.tensor([[False, True, False]]), tau, alpha, torch.tensor([[True, False]]))
    p = teacher.detach()[0, 0].softmax(-1)
    expected_kl = (p * (p.log() - student[0, 0].log_softmax(-1))).sum()
    assert torch.allclose(result["generation"], expected_kl)
    assert result["margin"].item() == 0.  # 3-1 = .5*(5-1)
    assert torch.allclose(result["contrastive"], -torch.log_softmax(scores / 2, -1)[0, 0])
    result["total"].backward()
    assert teacher.grad is None and ts.grad is None and tau.grad is not None
    assert torch.equal(student.grad[0, 1], torch.zeros(2))


def test_ecg_sqrt_scaling_roundtrip_and_final_signed_projection():
    model = ecg.SharedRepresentation(4)
    x = torch.randn(2, 3, 4)
    raw = model.retrieval(x)
    assert torch.allclose(model.encode(x), raw / 2)
    assert torch.allclose(model.compress(model.encode(x)), model.compression(raw))
    projection = ecg.GatedProjection(2)
    for layer in projection.projections:
        nn.init.zeros_(layer.weight); nn.init.zeros_(layer.bias)
    projection.projections[-1].bias.data.fill_(-3)
    assert (projection(torch.zeros(1, 2)) < 0).all()


def test_rosetta_ratio_is_mean_of_ratios_not_ratio_of_means():
    x = np.array([[1., 0.]])
    y1, y2 = np.array([[.8, .6]]), np.array([[.6, .8]])
    b1, b2 = np.array([[.6, .8]]), np.array([[.8, .6]])
    assert np.isclose(rosetta.unification_score([(x, y1, b1), (x, y2, b2)]), (.8/.6 + .6/.8)/2)
    with pytest.raises(ValueError):
        rosetta.average_cosine(x, np.zeros((1, 2)))
    with pytest.raises(ValueError):
        rosetta.unification_score([(x, y1, np.array([[0., 1.]]))])


def test_recall_common_mask_and_macro_not_micro():
    a = np.array([[True, False, False], [True, True, False], [False, True, True]])
    f = np.array([[True, False, False], [True, True, True], [False, False, False]])
    c = np.ones_like(f)
    r = recall.conditional_expected_accuracy(a, f, c, samples_per_question=3)
    assert r["dropped_questions"] == 1 and r["retained_questions"] == 2
    assert r["factual_expected_accuracy"] == (1 + 2/3) / 2
    assert r["all_expected_accuracy"] == .5
    with pytest.raises(ValueError):
        recall.conditional_expected_accuracy(a, f, c)
    with pytest.raises(ValueError):
        recall.conditional_expected_accuracy(a, np.zeros_like(f), c, samples_per_question=3)


def test_latent_exact_set_requires_no_omission_or_false_inclusion():
    all_answers = {"a", "b"}; hold = {"b"}
    score = latent.score_completion({"a", "b", "wrong"}, all_answers, hold, "b")
    assert score["heldout_recall"] == 1 and score["exact_set_match"] == 0
    assert latent.exact_set_pass_at_n([{ "a"}, all_answers], all_answers, 1) == .5
    with pytest.raises(ValueError):
        latent.score_completion({"a"}, all_answers, {"outside"}, "outside")


def test_planning_formula_independent_bfs_many_restricted_layouts():
    # Different cover counts and base obstructions; no formula is used by BFS.
    for order in permutations(["A", "B", "x", "y"]):
        initial = planning.State(((order[0], order[1]), (order[2], order[3])))
        goal = (order[0], order[2])
        assert planning.restricted_optimal_cost(initial, goal) == planning.bfs_optimal_cost(initial, goal)
    with pytest.raises(ValueError):
        planning.restricted_optimal_cost(planning.State((("a", "b"),)), ("a", "b"))
    with pytest.raises(ValueError):
        planning.transition(planning.State((("a", "b"),)), ("pickup", "a"))


def test_temporal_cycle_is_not_random_despite_perfect_marginal():
    cycle = stochastic.evaluate_discrete_uniform([0, 1]*512, [0, 1])
    assert cycle["marginal_p_value"] == 1 and cycle["lag1_repeat_rate"] == 0
    with pytest.raises(ValueError):
        stochastic.evaluate_discrete_uniform([0]*1023 + [2], [0, 1])
    with pytest.raises(ValueError):
        stochastic.evaluate_continuous([1.1]*1024, distribution="uniform")


def test_continuousbench_parser_exact_vs_contains_and_code_revision():
    score = cb.score_geminon("What are the types of X?", " Flying and Normal. Q: continuation", "Normal and Flying")
    assert score["contains_match"] and not score["exact_match"]
    assert cb.score_geminon("height", "14 m", "14")["exact_match"] is False
    assert cb.score_geminon("name", "\n\nSponge.\nQ: next", "Sponge")["exact_match"] is True
    assert len(cb.UPSTREAM_REVISION) == 40


def test_continuousbench_rejects_test_selection_and_mismatched_release():
    with pytest.raises(ValueError):
        cb.select_validation_checkpoint([{"checkpoint": "a", "split": "test", "contains_accuracy": 1.}])
    a = {"id": "q", "question": "q", "ground_truth": "A", "raw_prediction": "A", "split": "test", "release_revision": "r"}
    with pytest.raises(ValueError):
        cb.capability_gain([a], [{**a, "release_revision": "different"}], release_revision="r")
    with pytest.raises(ValueError):
        cb.capability_gain([a], [{**a, "ground_truth": "B"}], release_revision="r")
