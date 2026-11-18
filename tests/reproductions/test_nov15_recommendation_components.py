import itertools
import math

import numpy as np
import pytest
import torch

from auto_research.reproductions import kuairec_v2_protocol as kuai
from auto_research.reproductions import resid_components as resid
from auto_research.reproductions import trigen_components as trigen


def test_resid_full_beam_matches_independent_enumeration():
    sids = list(itertools.product(range(2), repeat=3))
    sim = np.linspace(-1, 1, 8)
    logits = lambda prefix: np.array([0.3 * len(prefix), -0.4])
    prior = lambda prefix: np.array([0.75, 0.25])
    actual = resid.guided_beam(sids, sim, logits, prior, vocabulary_size=2, beam_size=8,
                               popularity_weight=0.7, semantic_weight=0.8, temperature=0.5)
    root_potential = math.log(np.exp(sim / 0.5).mean())
    expected = []
    for index, sid in enumerate(sids):
        score = 0
        for level, token in enumerate(sid):
            calibrated = logits(sid[:level]) - 0.7 * np.log(prior(sid[:level]))
            probability = np.exp(calibrated) / np.exp(calibrated).sum()
            score += math.log(probability[token])
        score += 0.8 * (sim[index] / 0.5 - root_potential)
        expected.append((sid, score))
    expected.sort(key=lambda value: (-value[1], value[0]))
    assert [x[0] for x in actual] == [x[0] for x in expected]
    np.testing.assert_allclose([x[1] for x in actual], [x[1] for x in expected])


def test_resid_constraints_duplicates_and_no_target():
    catalog = [(0, 0), (0, 0), (1, 1)]
    beams = resid.guided_beam(catalog, [0, 0, 0], lambda _: [0, 0], lambda _: [0.5, 0.5],
                              vocabulary_size=2, beam_size=4, popularity_weight=0, semantic_weight=0, temperature=1)
    assert {x[0] for x in beams} == {(0, 0), (1, 1)}
    assert resid.partial_match(catalog, [((0, 0), -9), ((1, 1), -1)], 0) == [2, 0, 1]
    with pytest.raises(ValueError, match="positive"):
        resid.guided_beam(catalog, [0, 0, 0], lambda _: [0, 0], lambda _: [0, 1],
                          vocabulary_size=2, beam_size=1, popularity_weight=1, semantic_weight=0, temperature=1)


def test_independent_quantization_cannot_propagate_subspace_error():
    books = np.array([[[0.0], [1.0]], [[0.0], [1.0]]])
    original = np.array([[[0.1], [0.1]]])
    changed = np.array([[[0.9], [0.1]]])
    assert resid.parallel_quantize(original, books).tolist() == [[0, 0]]
    assert resid.parallel_quantize(changed, books).tolist() == [[1, 0]]


@pytest.mark.parametrize("field", ["popularity_weight", "semantic_weight", "temperature"])
@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_resid_rejects_nonfinite_controls(field, bad):
    controls = {"popularity_weight": 0, "semantic_weight": 0, "temperature": 1}
    controls[field] = bad
    with pytest.raises(ValueError):
        resid.guided_beam([(0, 0)], [0], lambda _: [0, 0], lambda _: [0.5, 0.5],
                          vocabulary_size=2, beam_size=1, **controls)


def test_trigen_rejects_nonfinite_padding_instead_of_zero_times_nan():
    model = trigen.DualPathConditioner(4, 3)
    h, trigger = torch.ones(1, 4, 4), torch.ones(1, 4)
    h[:, 0] = float("nan")
    with pytest.raises(ValueError):
        model(h, trigger, torch.tensor([[False, True, True, True]]))


@pytest.mark.parametrize("n", [0, 1, 4])
def test_trigen_tail_retains_exact_context_budget(n):
    h, t = torch.arange(8.0).reshape(1, 4, 2), torch.tensor([[90.0, 91.0]])
    actual = trigen.tail_inject(h, t, n)
    torch.testing.assert_close(actual[:, :4-n], h[:, n:])
    assert actual.shape == h.shape
    if n:
        torch.testing.assert_close(actual[:, -n:], t[:, None].expand(-1, n, -1))


def test_trigen_two_paths_use_pristine_history_and_padding_mask():
    torch.manual_seed(3)
    m = trigen.DualPathConditioner(4, 3)
    h, t = torch.randn(2, 4, 4), torch.randn(2, 4)
    mask = torch.tensor([[False, True, True, True], [False, True, True, True]])
    first = m(h, t, mask)
    corrupt_padding = h.clone()
    corrupt_padding[:, 0] = 10000
    second = m(corrupt_padding, t, mask)
    for a, b in zip(first, second, strict=True):
        torch.testing.assert_close(a, b)
    other = m(h, -t, mask)
    torch.testing.assert_close(first[3], other[3])
    assert not torch.allclose(first[2], other[2])
    with pytest.raises(ValueError):
        m(h, t, torch.zeros_like(mask))


def test_trigen_position_specific_condition_changes_only_its_level():
    torch.manual_seed(4)
    model = trigen.DualPathConditioner(4, 3)
    h, t = torch.randn(2, 4, 4), torch.randn(2, 4)
    before = model(h, t)[0].detach().clone()
    with torch.no_grad():
        model.pffns[1][-1].bias.add_(10)
    after = model(h, t)[0]
    torch.testing.assert_close(after[:, 0], before[:, 0])
    torch.testing.assert_close(after[:, 2], before[:, 2])
    torch.testing.assert_close(after[:, 1], before[:, 1] + 10)


def test_kuairec_weighting_split_and_single_retrieval_contract():
    assert kuai.full_month_score({1: 0.8, 2: 0.2}, {1: 1, 2: 3}) == pytest.approx(0.35)
    with pytest.raises(ValueError):
        kuai.full_month_score({1: 0.8}, {1: 0})
    with pytest.raises(ValueError):
        kuai.single_retrieval_evaluate_all({"q": {"click": ["x"]}}, {"q": ("x", ["click"])}, 1)
    with pytest.raises(ValueError, match="timestamp tie"):
        kuai.daily_leave_one_out([kuai.Interaction("a", 1, 2, "x"), kuai.Interaction("a", 1, 2, "y")])


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("module", [resid, trigen, kuai])
def test_all_bounded_diagnostics(seed, module):
    assert all(module.diagnostic(seed)["checks"].values())
