from dataclasses import replace
import inspect

import numpy as np
import pytest
import torch

from auto_research.system_one.jev_dlc import JevDLC, diagnostic, pa_i, softmax
from auto_research.recommendation_components.pair import PositionalHistory, exposure_negatives, preference_loss
from auto_research.recommendation_components.pair import diagnostic as pair_diagnostic


def learner_and_slate():
    learner = JevDLC(['a', 'b', 'c'], np.eye(2), model_revision='m1', projection_revision='p1')
    slate = dict(candidate_ids=['a', 'b', 'c'], semantic_ids=['a', 'b', 'c'],
                 logits=[.4, -.2, 50.], hidden=[[1., 0.], [0., 1.], [1., 1.]],
                 safe=[True, True, False], model_revision='m1', projection_revision='p1')
    return learner, slate


@pytest.mark.parametrize('seed', [42, 43, 44])
def test_short_real_component_diagnostics(seed):
    for run in (diagnostic, pair_diagnostic):
        result = run(seed)
        assert all(result['checks'].values())
        assert all(np.isfinite(v) for v in result['metrics'].values())


@pytest.mark.parametrize('direction,base', [([0., 0.], -2.), ([1., 0.], 2.), ([1., 2.], -.2), ([.01, 0.], -2.)])
def test_pa_i_minimizes_independent_primal_search(direction, base):
    state, delta = np.array([.2, -.1]), np.array(direction)
    result = pa_i(state, delta, base)
    objective = lambda value: .5*np.sum((value-state)**2)+max(0., 1.-base-value@delta)
    # Closed-form solution beats a dense grid of independent alternative states.
    alternatives = np.stack(np.meshgrid(np.linspace(-1.2, 1.4, 71), np.linspace(-1.2, 1.4, 71)), -1).reshape(-1, 2)
    assert objective(result) <= min(objective(v) for v in alternatives)+1e-12


def test_geometric_mixture_and_pre_feedback_losses_match_paper():
    learner, slate = learner_and_slate()
    learner.counts[:] = [4, 1, 0]
    learner.states[:] = [[-.5, .2], [.4, -.3]]
    learner.log_weights[:] = [.1, -.4]
    before_counts, before_states = learner.counts.copy(), learner.states.copy()
    prior = 2*np.log((np.array([4., 1.])+.5)/6.)
    features = np.array([[[2., 0.], [0., 2.]], [[1., 0.], [0., 1.]]])
    base = np.array([[.4, -.2]+prior, [.4, -.2]])
    scores = base+np.array([[before_states[j]@v for v in features[j]] for j in range(2)])
    channels = np.stack([softmax(s) for s in scores])
    w = softmax(learner.log_weights)
    geo = channels[0]**w[0]*channels[1]**w[1]
    geo /= geo.sum()
    first = learner.predict(0, **slate)
    np.testing.assert_allclose(first.probabilities, [*geo, 0.], rtol=1e-14)
    np.testing.assert_array_equal(learner.counts, before_counts)
    preferred = 1 if first.choice == 'a' else 0
    rejected = 1-preferred
    expected_states = np.stack([pa_i(before_states[j], features[j, preferred]-features[j, rejected],
                                   base[j, preferred]-base[j, rejected]) for j in range(2)])
    expected_weights = .9*softmax(learner.log_weights-.25*(channels.argmax(-1) != preferred))+.05
    learner.feedback(first, accepted=False, replacement=['a', 'b'][preferred])
    np.testing.assert_allclose(learner.states, expected_states)
    np.testing.assert_allclose(np.exp(learner.log_weights), expected_weights)
    assert learner.counts.sum() == before_counts.sum()+1


def test_feedback_is_bound_to_committed_safe_prediction_and_revision():
    learner, slate = learner_and_slate()
    first = learner.predict(0, **slate)
    for invalid in ('c', first.choice, 'unknown'):
        with pytest.raises(ValueError):
            learner.feedback(first, accepted=False, replacement=invalid)
    with pytest.raises(ValueError, match='uncommitted'):
        learner.feedback(replace(first), accepted=True)
    with pytest.raises(ValueError, match='chronological'):
        learner.predict(1, **slate)
    learner.feedback(first, accepted=True)
    with pytest.raises(ValueError):
        learner.feedback(first, accepted=True)
    with pytest.raises(ValueError, match='chronological'):
        learner.predict(0, **slate)
    with pytest.raises(ValueError, match='revision'):
        learner.predict(1, **{**slate, 'model_revision': 'm2'})
    learner.reset()
    assert not learner.counts.any() and not learner.states.any()
    assert 'target' not in inspect.signature(learner.predict).parameters


def test_projected_direction_is_scale_invariant_and_overflow_rejected():
    first, slate = learner_and_slate()
    second, _ = learner_and_slate()
    original = first.predict(0, **slate)
    huge = second.predict(0, **{**slate, 'hidden': (np.asarray(slate['hidden'])*1e308).tolist()})
    np.testing.assert_allclose(original.probabilities, huge.probabilities)
    first.feedback(original, accepted=False, replacement='b')
    second.feedback(huge, accepted=False, replacement='b')
    np.testing.assert_allclose(first.states, second.states)
    overflowing = JevDLC(['a', 'b', 'c'], np.eye(2)*1e308, model_revision='m1', projection_revision='p1')
    with pytest.raises(ValueError, match='nonfinite projected'):
        overflowing.predict(0, **{**slate, 'hidden': [[2., 2.]]*3})


@pytest.mark.parametrize('bad', [dict(safe=[False]*3), dict(safe=[1, 1, 0]), dict(semantic_ids=['a', 'new', 'c']),
    dict(logits=[float('nan'), 1., 2.]), dict(hidden=[[0., 0.]]*3), dict(candidate_ids=['a']*3)])
def test_invalid_runtime_slates_rejected(bad):
    learner, slate = learner_and_slate()
    with pytest.raises(ValueError):
        learner.predict(0, **{**slate, **bad})


def test_pair_position_order_and_query_agnostic_attention():
    model = PositionalHistory(2, 2).double()
    with torch.no_grad():
        model.attention.copy_(torch.tensor([1., 0.]))
        model.position.copy_(torch.tensor([[2., 0.], [-2., 0.]]))
    history = torch.tensor([[[1., 0.], [0., 1.]]], dtype=torch.float64, requires_grad=True)
    profile = torch.tensor([[.3, .7]], dtype=torch.float64)
    mask = torch.ones(1, 2, dtype=torch.bool)
    query, weights = model(profile, history, mask)
    expected = torch.softmax(torch.tensor([[3., -2.]], dtype=torch.float64), -1)
    torch.testing.assert_close(weights, expected)
    _, other_weights = model(-profile, history, mask)
    torch.testing.assert_close(other_weights, weights)
    reversed_query, _ = model(profile, history.flip(1), mask)
    assert not torch.allclose(query, reversed_query)


def test_pair_sum_prefix_objective_value_and_gradient_independent_reference():
    torch.manual_seed(1)
    q = torch.randn(2, 6, dtype=torch.float64, requires_grad=True)
    c = torch.randn(2, 4, 6, dtype=torch.float64, requires_grad=True)
    loss = preference_loss(q, c, temperature=.3, dimensions=[3, 6])
    reference = sum(sum(-torch.log(torch.softmax(torch.stack([
        (q[b, :d]@c[b, i, :d])/(q[b, :d].norm()*c[b, i, :d].norm()*.3)
        for i in range(4)]), 0)[0]) for b in range(2))/2 for d in (3, 6))
    torch.testing.assert_close(loss, reference)
    for actual, expected in zip(torch.autograd.grad(loss, (q, c), retain_graph=True), torch.autograd.grad(reference, (q, c))):
        torch.testing.assert_close(actual, expected)
    assert not torch.isclose(loss, reference/2)


def test_exposure_negatives_exclude_positive_and_fill_only_outside_impressions():
    assert set(exposure_negatives('p', ['p', 'a', 'a', 'b', 'c'], ['p', 'z'])) == {'a', 'b', 'c'}
    assert set(exposure_negatives('p', ['p', 'a'], ['p', 'a', 'b', 'c'])) == {'a', 'b', 'c'}
    with pytest.raises(ValueError, match='insufficient'):
        exposure_negatives('p', ['p', 'a'], ['a', 'p'])
