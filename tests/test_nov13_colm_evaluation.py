"""Defining formulas and negative controls, not paper-scale capability tests."""
import importlib
import itertools
import math

import numpy as np
import pytest
import torch

from auto_research.foundation_models import cultural_cue as cue
from auto_research.foundation_models import decoding_constrained_beam as cbs
from auto_research.foundation_models import qe_length_normalization as qe
from auto_research.foundation_models import storyscope
from auto_research.post_training import behavioral_canaries as canary
from auto_research.post_training import rlmf


MODULES = [("foundation_models", name) for name in ("qe_length_normalization", "cultural_cue", "decoding_constrained_beam", "storyscope")]
MODULES += [("post_training", name) for name in ("behavioral_canaries", "rlmf")]


@pytest.mark.parametrize("domain,name", MODULES)
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics_are_finite_and_bounded(domain, name, seed):
    result = importlib.import_module(f"auto_research.{domain}.{name}").diagnostic(seed)
    assert result["diagnostic_only"] is True and result["evaluation_tier"] == "l1_mechanism"
    assert result["seed"] == seed and result["device"] == "cpu"
    assert result["checks"] and all(type(x) is bool and x for x in result["checks"].values())
    assert all(isinstance(x, (int, float)) and math.isfinite(x) for x in result["metrics"].values())
    assert result["metrics"]["pretrained_model_calls"] == 0


def test_qe_training_target_and_inference_scale_not_posthoc_fix():
    assert qe.density_targets([-5, -5], [10, 20], length_unit="fixed tokenizer") == (-.5, -.25)
    assert qe.restore_ratings([-.5, -.25], [10, 20], length_unit="fixed tokenizer") == (-5., -5.)
    with pytest.raises(ValueError):
        qe.density_targets([1], [0], length_unit="token")
    with pytest.raises(ValueError):
        qe.restore_ratings([1], [2], length_unit="")
    with pytest.raises(ValueError):
        qe.controlled_passages(["a"] * 5, [1, 4, 3, 5, 6])


def test_cue_cumulative_mass_is_not_fixed_fraction_of_features():
    mi = torch.tensor([.97, .01, .01, .01], dtype=torch.float64)
    assert cue.select_cumulative_mi(mi, .5).tolist() == [0]
    assert cue.select_cumulative_mi(torch.tensor([1., 1., 1.]), 2/3).tolist() == [0, 1]
    with pytest.raises(ValueError):
        cue.select_cumulative_mi(torch.zeros(2))


def test_cue_country_weighting_decoder_and_gradient():
    samples = torch.tensor([[4.], [2.], [2.], [0.]], requires_grad=True)
    _, prototypes = cue.country_prototypes(samples, ["A", "B", "B", "C"])
    decoder = torch.tensor([[2., 3.]])
    direction = cue.steering_direction(prototypes, 0, decoder)
    # Other country mean = (2+0)/2 = 1, not mean([2,2,0]).
    torch.testing.assert_close(direction, torch.tensor([6., 9.]))
    output = cue.apply_steering(torch.zeros(2, 2), direction, .5)
    output.sum().backward()
    assert samples.grad is not None and torch.isfinite(samples.grad).all()
    with pytest.raises(ValueError):
        cue.max_pool_features(torch.ones(2, 3, 1), torch.zeros(2, 3, dtype=torch.bool))


def _lev(a, b):
    row = list(range(len(b)+1))
    for i, x in enumerate(a, 1):
        new = [i]
        for j, y in enumerate(b, 1):
            new.append(min(row[j]+1, new[-1]+1, row[j-1]+int(x != y)))
        row = new
    return row[-1]


@pytest.mark.parametrize("distance", ["levenshtein", "hamming"])
@pytest.mark.parametrize("epsilon", [0, 1, 2])
def test_cbs_bounds_against_exhaustive_distribution(distance, epsilon):
    def logits(history):
        p = .8 if not history or history[-1] == 0 else .3
        return [math.log(p), math.log(1-p), -100.]
    target = (0, 1, 0)
    exact = 0.
    for tokens in itertools.product((0, 1), repeat=3):
        dist = _lev(tokens, target) if distance == "levenshtein" else sum(a != b for a, b in zip(tokens, target))
        if dist <= epsilon:
            mass = 1.
            for t, token in enumerate(tokens):
                lp = logits(tokens[:t]); mass *= math.exp(lp[token])
            exact += mass
    for beam in (1, 2, 8):
        result = cbs.search(logits, (), target, beam_width=beam, top_k=2, epsilon=epsilon, distance=distance)
        assert result.lower_bound <= exact+1e-12
        assert exact <= result.upper_bound+1e-12
        for continuation in result.continuations:
            lp = sum(logits(continuation.tokens[:t])[token] for t, token in enumerate(continuation.tokens))
            assert continuation.log_probability == pytest.approx(lp)
        if beam == 8:
            assert result.lower_bound == pytest.approx(exact)


def test_cbs_top_k_renormalization_and_last_expansion():
    result = cbs.search(lambda h: [math.log(.5), math.log(.3), math.log(.2)], (), [0], beam_width=1, top_k=2, epsilon=1)
    assert len(result.continuations) == 2
    assert result.lower_bound == pytest.approx(1.)
    assert math.exp(result.continuations[0].log_probability) == pytest.approx(.5/.8)


def test_cbs_eos_is_removed_only_before_final_step_and_callback_has_no_target():
    histories = []
    def logits(history):
        histories.append(history)
        return [0., 0.]
    result = cbs.search(logits, [7], [0, 1], beam_width=2, top_k=2, epsilon=1, eos_token_id=1)
    assert all(h in [(7,), (7, 0)] for h in histories)
    assert any(c.tokens[-1] == 1 for c in result.continuations)
    with pytest.raises(ValueError):
        cbs.search(logits, (), (), beam_width=2, top_k=2)


def test_storyscope_bootstrap_keeps_all_sources_from_same_prompt_together():
    draws = storyscope.prompt_bootstrap(["a"]*6 + ["b"]*6, seed=42)
    for draw in draws:
        assert len(set(draw.count(i) for i in range(6))) == 1
        assert len(set(draw.count(i) for i in range(6, 12))) == 1


def test_storyscope_core_conjunction_and_strict_quartile():
    n = 12
    shap = np.arange(n, dtype=float)
    stability = np.full(n, .8); top = np.full(n, .8)
    null = np.zeros(n); p = np.full(n, .05)
    ai = np.full((n, 5), .5); human = np.zeros(n)
    p[-1] = .11  # Above the permutation p gate must fail despite high SHAP.
    top[-2] = .59
    result = storyscope.select_core_features(shap, stability, top, null, p, human, ai)
    assert result["core"][9] and not result["core"][10] and not result["core"][11]
    with pytest.raises(ValueError):
        storyscope.select_core_features(shap, stability, top, null, p, human, ai[:, :4])


def test_canary_sequence_logprob_is_sum_not_token_average_and_gradients():
    logits = torch.zeros(2, 3, 2, dtype=torch.float64, requires_grad=True)
    ids = torch.zeros(2, 3, dtype=torch.long)
    mask = torch.tensor([[True, False, False], [True, True, True]])
    lp = canary.sequence_log_probability(logits, ids, mask)
    torch.testing.assert_close(lp, torch.tensor([-math.log(2), -3*math.log(2)], dtype=torch.float64))
    lp.sum().backward()
    assert logits.grad is not None and not logits.grad[0, 1:].any()


def test_canary_document_not_row_disjoint_and_policy_level_auc():
    with pytest.raises(ValueError, match="documents"):
        canary.assert_document_disjoint(["doc1"], ["doc2"], ["doc1"])
    assert canary.policy_auroc([0., 0.], [0., 0.]) == .5
    assert canary.policy_auroc([0., 1.], [2., 3.]) == 1.


def test_rlmf_only_above_mean_faithfulness_is_boosted():
    f = torch.tensor([[0., 1., 2.]], dtype=torch.float64, requires_grad=True)
    o = torch.tensor([[1., 0., -1.]], dtype=torch.float64)
    z = torch.ones_like(f)
    out = rlmf.advantages(f, o, z)
    torch.testing.assert_close(out, torch.tensor([[0., 0., 1.]], dtype=torch.float64))
    # A standard group-mean subtraction would destroy the specified output.
    assert out.mean().item() == pytest.approx(1/3)
    out.sum().backward()
    assert torch.isfinite(f.grad).all()


def test_rlmf_strict_tau_mask_and_training_only_selection():
    c = torch.tensor([[0., .25, 1.]], dtype=torch.float64)
    g = torch.tensor([[.125, .25, 0.]], dtype=torch.float64)
    mask = torch.tensor([[True, True, False]])
    assert rlmf.faithful_calibration(c, g, mask, tau=.125).item() == .5
    assert rlmf.select_training_tails(["a", "b", "c", "d"], [1, 2, 3, 4], 2, split="train") == ("a", "d")
    for split, count in [("test", 2), ("validation", 2), ("train", 3)]:
        with pytest.raises(ValueError):
            rlmf.select_training_tails(["a", "b", "c", "d"], [1, 2, 3, 4], count, split=split)


@pytest.mark.parametrize("module", [cue, canary, rlmf])
def test_tensor_components_advertise_real_gpu_gate(module):
    assert module.REQUIRES_GPU_VALIDATION is True
