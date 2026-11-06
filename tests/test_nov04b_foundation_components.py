"""Independent semantic support, external-state and reward-density contracts."""
import math

import pytest
import torch

from auto_research.foundation_models import semantic_block_sparse_attention as csb
from auto_research.foundation_models.anchor_kv import KVState, SharedKVReadout
from auto_research.foundation_models import anchor_kv
from auto_research.post_training import dars


@pytest.mark.parametrize('module', [csb, anchor_kv, dars])
@pytest.mark.parametrize('seed', [42, 43, 44])
def test_real_component_diagnostics(module, seed):
    output = module.diagnostic(seed, 'cpu')
    assert output['diagnostic_only'] and output['evaluation_tier'] == 'l1_mechanism'
    assert output['seed'] == seed and module.REQUIRES_GPU_VALIDATION
    assert all(type(x) is bool and x for x in output['checks'].values()), output
    assert all(math.isfinite(x) for x in output['metrics'].values())


def _index():
    return csb.SemanticIndex(torch.tensor([[[1., 0.], [0., 1.]]], dtype=torch.float64),
                             torch.tensor([[0, 1, 0, 1, 0, 1]]))


def test_semantic_blocks_are_noncontiguous_whole_and_may_overshoot():
    query = torch.tensor([[[1., 0.], [1., 0.]]], dtype=torch.float64)
    mask = csb.select_positions(query, _index(), torch.tensor([5]), torch.tensor([5]), history_budget=1)
    assert mask.tolist() == [[[True, False, True, False, True, True]]]
    assert int(mask.sum()) == 4  # 3 selected history tokens + dense current token


def test_gqa_scores_normalize_per_head_before_sum_and_size_penalty():
    query = torch.tensor([[[1., 0.], [0., 1.]]], dtype=torch.float64)
    index = csb.SemanticIndex(_index().centroids, torch.tensor([[0, 0, 0, 0, 1, 1]]))
    mask = csb.select_positions(query, index, torch.tensor([5]), torch.tensor([5]), history_budget=1)
    assert mask.tolist() == [[[False, False, False, False, True, True]]]


def test_sparse_attention_dense_limit_gradient_and_future_support():
    torch.manual_seed(8)
    query = torch.randn(2, 2, 2, dtype=torch.float64, requires_grad=True)
    key = torch.randn(6, 1, 2, dtype=torch.float64, requires_grad=True)
    value = torch.randn(6, 1, 3, dtype=torch.float64, requires_grad=True)
    positions, starts = torch.tensor([2, 5]), torch.tensor([2, 5])
    actual, mask = csb.sparse_attention(query, key, value, _index(), positions, starts, history_budget=6)
    expected = []
    for row, position in enumerate(positions):
        heads = []
        for head in range(2):
            weights = (key[:position + 1, 0] @ query[row, head] / math.sqrt(2)).softmax(0)
            heads.append(weights @ value[:position + 1, 0])
        expected.append(torch.stack(heads))
    assert torch.allclose(actual, torch.stack(expected), atol=1e-12)
    assert not bool(mask[0, :, 3:].any())
    actual.square().sum().backward()
    assert all(float(t.grad.abs().sum()) > 0 for t in (query, key, value))


def test_generated_unindexed_tokens_must_remain_in_dense_region():
    query = torch.tensor([[[1., 0.]]], dtype=torch.float64)
    mask = csb.select_positions(query, _index(), torch.tensor([8]), torch.tensor([6]),
                               history_budget=0, total_length=9)
    assert mask.tolist() == [[[False] * 6 + [True] * 3]]
    with pytest.raises(ValueError):
        csb.select_positions(query, _index(), torch.tensor([8]), torch.tensor([7]),
                             history_budget=1, total_length=9)


def test_spherical_kmeans_unit_centroids_default_count_reproducibility():
    torch.manual_seed(1)
    keys = torch.randn(12, 2, 3, dtype=torch.float64)
    a = csb.build_index(keys, clusters=3, seed=9)
    b = csb.build_index(keys, clusters=3, seed=9)
    assert torch.equal(a.centroids, b.centroids) and torch.equal(a.assignments, b.assignments)
    assert torch.allclose(a.centroids.norm(dim=-1), torch.ones(2, 3, dtype=keys.dtype))
    assert csb.build_index(keys).centroids.shape[1] == 12
    with pytest.raises(ValueError):
        csb.build_index(torch.zeros_like(keys))


def test_anchor_external_writer_identity_readers_and_immutable_old_state():
    model = SharedKVReadout(1, 2, 2, 3).double()
    old = KVState(torch.zeros(1, 2, 2, dtype=torch.float64), 0)
    matrix = torch.eye(2, dtype=torch.float64)[None]
    state = model.accept_write(old, matrix, layer=0, revision=1)
    matrix.zero_()
    assert torch.equal(state.matrix, torch.eye(2, dtype=torch.float64)[None])
    assert old.matrix.count_nonzero() == 0
    query, local, hidden = torch.ones(1, 1, 2, dtype=torch.float64), torch.zeros(1, 1, 2, dtype=torch.float64), torch.zeros(1, 3, dtype=torch.float64)
    assert torch.equal(model(query, local, hidden, state, layer=0), model(query, local, hidden, state, layer=2))
    with pytest.raises(ValueError):
        model.accept_write(state, state.matrix, layer=1, revision=2)
    with pytest.raises(ValueError):
        model.accept_write(state, state.matrix, layer=0, revision=1)


def test_anchor_nonidentity_reader_learns_basis_and_gate_can_select_local():
    model = SharedKVReadout(1, 2, 2, 2).double()
    state = KVState(torch.eye(2, dtype=torch.float64)[None], 0)
    query = torch.tensor([[[1., 2.]]], dtype=torch.float64)
    local, hidden = torch.ones_like(query), torch.zeros(1, 2, dtype=torch.float64)
    with torch.no_grad():
        model.read_maps['1'].copy_(torch.tensor([[[0., -1.], [1., 0.]]], dtype=torch.float64))
        model.gates['1'].bias.fill_(0.)
    assert torch.equal(model(query, local, hidden, state, layer=1), local + .5 * torch.tensor([[[2., -1.]]]))
    with torch.no_grad():
        model.gates['1'].bias.fill_(-1000.)
    assert torch.equal(model(query, local, hidden, state, layer=1), local)
    assert '0' not in model.read_maps  # writer basis cannot drift


def test_dars_duplicate_density_self_and_isolated_point():
    output = dars.density_scaled_advantages(torch.tensor([[0.], [0.], [100.]]), torch.ones(3), bandwidth=.001)
    assert torch.equal(output['density'], torch.tensor([2., 2., 1.]))
    assert torch.equal(output['scaled_rewards'], torch.tensor([.5, .5, 1.]))
    assert output['advantages'][2] > output['advantages'][0]


def test_dars_group_isolation_permutation_and_bandwidth_limits():
    values = torch.tensor([[[0.], [1.], [3.]], [[0.], [0.], [0.]]], dtype=torch.float64)
    rewards = torch.tensor([[0., 1., 3.], [1., 3., 0.]], dtype=torch.float64)
    result = dars.density_scaled_advantages(values, rewards, bandwidth=.4)
    for group in range(2):
        single = dars.density_scaled_advantages(values[group], rewards[group], bandwidth=.4)
        assert torch.equal(single['advantages'], result['advantages'][group])
    permutation = torch.tensor([2, 0, 1])
    permuted = dars.density_scaled_advantages(values[:, permutation], rewards[:, permutation], bandwidth=.4)
    assert torch.allclose(permuted['advantages'], result['advantages'][:, permutation], atol=1e-14)
    small = dars.density_scaled_advantages(values[0], rewards[0], bandwidth=1e-12)
    large = dars.density_scaled_advantages(values[0], rewards[0], bandwidth=1e100)
    assert torch.equal(small['density'], torch.ones(3, dtype=torch.float64))
    assert torch.equal(large['density'], torch.full((3,), 3., dtype=torch.float64))
    assert torch.allclose(small['advantages'], large['advantages'], atol=1e-14)


def test_dars_explicit_std_convention_zero_variance_stopgrad_and_validation():
    values = torch.zeros(3, 2, dtype=torch.float64, requires_grad=True)
    rewards = torch.tensor([1., 2., 4.], dtype=torch.float64, requires_grad=True)
    population = dars.density_scaled_advantages(values, rewards)
    sample = dars.density_scaled_advantages(values, rewards, correction=1)
    assert torch.allclose(sample['advantages'], population['advantages'] * math.sqrt(2 / 3))
    assert all(not x.requires_grad for x in sample.values())
    constant = dars.density_scaled_advantages(values, torch.ones_like(rewards))
    assert torch.equal(constant['advantages'], torch.zeros_like(rewards))
    with pytest.raises(ValueError):
        dars.density_scaled_advantages(values, torch.ones_like(rewards), zero_variance='raise')
    for bandwidth in (0, -1, float('nan'), float('inf')):
        with pytest.raises(ValueError):
            dars.density_scaled_advantages(values, rewards, bandwidth=bandwidth)
    with pytest.raises(ValueError, match='nonnegative'):
        dars.density_scaled_advantages(values, torch.tensor([1., -1., 2.], dtype=values.dtype))
