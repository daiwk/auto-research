from __future__ import annotations

import itertools

import pytest
import torch

from auto_research.reproductions.cross_task_relationships.model import (
    CrossTaskModel, auxiliary_loss, joint_distribution, validate_pair,
)
from auto_research.reproductions.static_constraint_decoding.algorithm import StaticTrie, beam_step
from auto_research.reproductions.transx.technical_report import PoolState, RowWiseAdagrad, multi_cutoff_memory


@pytest.mark.parametrize("dense_depth", [0, 1, 2])
def test_static_matches_prefix_oracle_and_reorders_beams(dense_depth):
    rows = [(0, 1, 2), (0, 1, 3), (0, 3, 1), (2, 0, 3)]
    trie = StaticTrie.build(rows, 4, dense_depth=dense_depth)
    nodes = torch.ones((1, 1), dtype=torch.long)
    scores = torch.zeros(1, 1, dtype=torch.float64)
    prefixes = torch.empty(1, 1, 0, dtype=torch.long)
    all_log_probs = []
    for step in range(3):
        logits = torch.arange(4, dtype=torch.float64).expand(1, nodes.shape[1], 4)
        for beam in range(nodes.shape[1]):
            prefix = tuple(prefixes[0, beam].tolist())
            values, tokens, targets = trie.candidates(logits.log_softmax(-1), nodes, step)
            expected = {row[step] for row in rows if row[:step] == prefix} if torch.isfinite(scores[0, beam]) else set()
            actual = set(tokens[0, beam][torch.isfinite(values[0, beam])].tolist())
            assert actual == expected
            assert (targets[0, beam][torch.isfinite(values[0, beam])] > 0).all()
        result = beam_step(trie, logits, nodes, scores, prefixes, step=step, beam_width=4)
        nodes, scores, prefixes = result["nodes"], result["scores"], result["prefixes"]
        all_log_probs.append(logits.log_softmax(-1)[0, 0])
    actual = {tuple(row.tolist()): float(score) for row, score in zip(prefixes[0], scores[0], strict=True)
              if torch.isfinite(score)}
    assert set(actual) == set(rows)
    for row in rows:
        assert actual[row] == pytest.approx(sum(float(all_log_probs[i][token]) for i, token in enumerate(row)))
    assert result["finished"].all()


def test_static_invalid_input_and_explicit_eos():
    with pytest.raises(ValueError, match="explicit EOS"):
        StaticTrie.build([(1,), (1, 2)], 4)
    trie = StaticTrie.build([(1,), (1, 2)], 4, eos_token=3)
    assert trie.depth == 3
    with pytest.raises(ValueError):
        StaticTrie.build([(4,)], 4)
    with pytest.raises(ValueError):
        StaticTrie.build([], 4)


def test_static_mask_is_not_renormalized_and_dead_beams_do_not_revive():
    trie = StaticTrie.build([(0, 1)], 3)
    result = beam_step(trie, torch.tensor([[[0., 10., 20.]]]), torch.ones(1, 1, dtype=torch.long),
                       torch.zeros(1, 1), torch.empty(1, 1, 0, dtype=torch.long), step=0, beam_width=3)
    assert result["alive"].sum() == 1
    assert result["scores"][0, 0] < -19
    assert torch.all(result["nodes"][~result["alive"]] == 0)


def test_cross_task_loss_changes_shared_gradient_without_gold_in_forward():
    torch.manual_seed(42)
    model = CrossTaskModel(4, 5, 8)
    users, items, context = torch.arange(4), torch.arange(4), torch.randn(4, 3)
    labels = torch.tensor(list(itertools.product((0., 1.), repeat=2)))
    assert validate_pair(labels) == {"00": 1, "01": 1, "10": 1, "11": 1}
    marginal, cross = model(users, items, context)
    base, _ = auxiliary_loss(marginal, cross, labels, weight=0)
    baseline = torch.autograd.grad(base, model.body[0].weight, retain_graph=True)[0]
    loss, _ = auxiliary_loss(marginal, cross, labels, weight=0.3)
    upgraded = torch.autograd.grad(loss, model.body[0].weight)[0]
    assert torch.linalg.vector_norm(upgraded - baseline) > 0
    with pytest.raises(ValueError, match="nested"):
        validate_pair(torch.tensor([[0., 0.], [1., 1.]]))


def test_joint_table_preserves_covariance_and_reports_infeasibility():
    table, valid = joint_distribution(torch.tensor([[.2, .1]]), torch.tensor([.05]))
    torch.testing.assert_close(table[0], torch.tensor([[.75, .05], [.15, .05]]))
    assert valid.item()
    _, bad = joint_distribution(torch.tensor([[.2, .1]]), torch.tensor([.9]))
    assert not bad.item()


def test_transx_shared_memory_matches_direct_values_and_full_gradients():
    torch.manual_seed(9)
    x = torch.randn(27, 5, dtype=torch.float64, requires_grad=True)
    scores = (torch.randn(27, dtype=torch.float64) * 200).requires_grad_()
    cutoffs = [0, 2, 9, 16, 24, 27]
    shared, counts = multi_cutoff_memory(x, scores, cutoffs, local_width=4, global_blocks=3)
    direct, _ = multi_cutoff_memory(x, scores, cutoffs, local_width=4, global_blocks=3, shared=False)
    weights = [torch.randn_like(value) for value in shared]
    left = sum((a * w).sum() for a, w in zip(shared, weights, strict=True))
    right = sum((a * w).sum() for a, w in zip(direct, weights, strict=True))
    g1 = torch.autograd.grad(left, (x, scores), retain_graph=True)
    g2 = torch.autograd.grad(right, (x, scores))
    for a, b in zip(shared, direct, strict=True):
        torch.testing.assert_close(a, b, atol=1e-11, rtol=1e-11)
    for a, b in zip(g1, g2, strict=True):
        torch.testing.assert_close(a, b, atol=1e-10, rtol=1e-10)
    assert counts["atomic_tokens_pooled"] < counts["direct_tokens_pooled"]


def test_transx_causality_associativity_and_sparse_duplicate_aggregation():
    x = torch.arange(20., dtype=torch.float64).reshape(10, 2)
    scores = torch.arange(10., dtype=torch.float64)
    a, b, c = [PoolState.from_tokens(x[s:e], scores[s:e]) for s, e in ((0, 2), (2, 5), (5, 10))]
    torch.testing.assert_close(a.merge(b).merge(c).readout(), a.merge(b.merge(c)).readout())
    before, _ = multi_cutoff_memory(x, scores, [4])
    changed = x.clone()
    changed[4:] = 1e8
    after, _ = multi_cutoff_memory(changed, scores, [4])
    torch.testing.assert_close(before[0], after[0])
    parameter = torch.nn.Parameter(torch.zeros(4, 2, dtype=torch.float64))
    parameter.grad = torch.sparse_coo_tensor(torch.tensor([[1, 1, 3]]),
                                           torch.tensor([[1., 2.], [3., 4.], [2., 2.]], dtype=torch.float64), (4, 2))
    opt = RowWiseAdagrad([parameter], lr=.1)
    opt.step()
    assert opt.state[parameter]["sum"][1] == 26  # mean(([1,2]+[3,4])**2), not sum of squares
    torch.testing.assert_close(parameter[1], torch.tensor([-.4, -.6], dtype=torch.float64) / (26 ** .5 + 1e-8))
    assert not parameter[0].any() and not parameter[2].any()


def test_transx_half_precision_cancelled_row_keeps_finite_state():
    parameter = torch.nn.Parameter(torch.zeros(4, 2, dtype=torch.float16))
    parameter.grad = torch.sparse_coo_tensor(
        torch.tensor([[1, 1, 2]]), torch.tensor([[1., 2.], [-1., -2.], [1., 1.]], dtype=torch.float16), (4, 2),
    )
    optimizer = RowWiseAdagrad([parameter])
    optimizer.step()
    assert torch.isfinite(parameter).all()
    assert not parameter[1].any()
    assert optimizer.state[parameter]["sum"].dtype == torch.float32
