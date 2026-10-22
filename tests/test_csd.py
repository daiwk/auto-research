import pytest
import torch

from auto_research.post_training.csd import (
    Chunk,
    align_offsets,
    common_support_loss,
    diagnostic,
    divergence,
    event_distribution,
    paired_completions,
)


def decoder(vocabulary):
    return lambda ids: "".join(vocabulary[i] for i in ids)


def test_offset_alignment_is_minimal_and_checks_decoded_whole_chunks():
    ds, dt = decoder(("a", "bc", "x")), decoder(("ab", "c", "x"))
    actual = align_offsets((0, 1, 2), (0, 1, 2), ((0, 1), (1, 3), (3, 4)), ((0, 2), (2, 3), (3, 4)), ds, dt)
    assert actual == (Chunk(0, 2, 0, 2, 0, 3), Chunk(2, 3, 2, 3, 3, 4))
    bad_decode = decoder(("WRONG", "c", "x"))
    assert len(align_offsets((0, 1, 2), (0, 1, 2), ((0, 1), (1, 3), (3, 4)), ((0, 2), (2, 3), (3, 4)), ds, bad_decode)) == 1
    with pytest.raises(ValueError, match="positive"):
        align_offsets((0,), (0,), ((0, 0),), ((0, 1),), ds, dt)


def test_offset_whitespace_gap_accepts_verified_whole_chunk():
    ds, dt = decoder(("ab cd",)), decoder(("ab", "cd"))
    args = ((0,), (0, 1), ((0, 5),), ((0, 2), (3, 5)), ds, dt)
    assert align_offsets(*args, source_text="ab cd") == (Chunk(0, 1, 0, 2, 0, 5),)
    # Without original text, the gap cannot safely be identified as whitespace.
    assert align_offsets(*args) == ()


def test_offset_content_gap_and_mismatched_source_are_rejected():
    ds, dt = decoder(("ab cd",)), decoder(("ab", "cd"))
    args = ((0,), (0, 1), ((0, 5),), ((0, 2), (3, 5)), ds, dt)
    # The two decoded strings pass whitespace-stripped equivalence but cannot
    # justify silently dropping the source's non-whitespace X.
    assert align_offsets(*args, source_text="abXcd") == ()
    # Shared contiguous offsets alone cannot excuse fabricated decoded content.
    assert align_offsets((0,), (0,), ((0, 5),), ((0, 5),), ds,
                         decoder(("abcd",)), source_text="abXcd") == ()
    with pytest.raises(ValueError, match="exceed"):
        align_offsets(*args, source_text="ab")


def test_decoded_text_not_equal_ids_and_all_non_one_to_one_shapes():
    ds = decoder(("120", "129", "a", "bc", "ab", "c"))
    dt = decoder(("1", "2", "0", "9", "ab", "c", "a", "bc", "120"))
    assert (0, 8) in paired_completions((0,), (8,), 6, 9, ds, dt)
    assert paired_completions((0,), (0, 1, 2), 6, 9, ds, dt) == ((0, 2), (1, 3))
    assert paired_completions((2, 3), (4, 5), 6, 9, ds, dt) == ((3, 5),)
    # Same visible text with duplicate token spellings is not counted twice.
    duplicate = decoder(("120", "120"))
    assert paired_completions((0,), (8,), 2, 9, duplicate, dt) == ()


def test_chain_rule_prefix_gradients_and_rest_not_length_normalized():
    logits = torch.tensor([[.2, .1, -.3], [.8, -.1, .3]], dtype=torch.float64, requires_grad=True)
    got = event_distribution(logits, (1, 0), (0, 2))
    p = logits.softmax(-1)
    q = torch.stack((p[0, 1] * p[1, 0], p[0, 1] * p[1, 2]))
    expected = torch.cat((q, (1 - q.sum()).reshape(1)))
    torch.testing.assert_close(got, expected)
    assert not torch.allclose(got[:-1], q.sqrt())
    grad = torch.autograd.grad(got[0], logits)[0]
    assert grad[0].abs().sum() > 0
    assert grad[1].abs().sum() > 0
    with pytest.raises(ValueError, match="distinct"):
        event_distribution(logits, (1, 0), (0, 0))


def test_top_k_changes_support_without_renormalizing_probabilities():
    logits = torch.tensor([[1., .5, -.2]], dtype=torch.float64)
    got = event_distribution(logits, (0,), (0,))
    torch.testing.assert_close(got[0], logits.softmax(-1)[0, 0])
    assert 0 < got[-1] < 1
    assert got[0] < 1


@pytest.mark.parametrize("kind", ["jsd", "forward_kl", "reverse_kl"])
def test_unequal_vocab_loss_matches_independent_distribution_reference(kind):
    ds, dt = decoder(("a", "b", "c")), decoder(("b", "a", "d", "e"))
    sl = torch.tensor([[.2, .9, -.3]], dtype=torch.float64, requires_grad=True)
    tl = torch.tensor([[.3, -.2, .4, .1]], dtype=torch.float64, requires_grad=True)
    _, audit = common_support_loss(sl, tl, (0,), (1,), (Chunk(0, 1, 0, 1, 0, 1),), ds, dt, kind=kind)
    p, q = sl.softmax(-1)[0], tl.detach().softmax(-1)[0]
    ps = torch.stack((p[0], p[1], p[2]))
    pt = torch.stack((q[1], q[0], q[2] + q[3]))
    torch.testing.assert_close(audit["kd"], divergence(pt, ps, kind))
    assert audit["events"][0]["pairs"] == ((0, 1), (1, 0))
    audit["kd"].backward()
    assert tl.grad is None
    assert sl.grad is not None and bool(torch.isfinite(sl.grad).all())


def test_weighted_numerator_unweighted_chunk_count_and_detached_scaling():
    ds, dt = decoder(("ab", "x", "ac")), decoder(("a", "b", "x", "c"))
    sl = torch.tensor([[.2, .1, -.3], [.8, -.1, .3]], dtype=torch.float64, requires_grad=True)
    tl = torch.tensor([[.3, -.2, .4, .1], [.8, -.2, .1, .5], [-.1, .2, .3, .7]], dtype=torch.float64)
    chunks = (Chunk(0, 1, 0, 2, 0, 2), Chunk(1, 2, 2, 3, 2, 3))
    total, audit = common_support_loss(sl, tl, (0, 1), (0, 1, 2), chunks, ds, dt, beta=5)
    events = audit["events"]
    expected = (5 * divergence(events[0]["teacher"], events[0]["student"]) + divergence(events[1]["teacher"], events[1]["student"])) / 2
    torch.testing.assert_close(audit["kd"], expected)
    assert not audit["scale"].requires_grad
    actual_grad = torch.autograd.grad(total, sl, retain_graph=True)[0]
    expected_grad = torch.autograd.grad(audit["ce"] + audit["scale"].item() * expected, sl)[0]
    torch.testing.assert_close(actual_grad, expected_grad)


def test_empty_support_is_ce_only_not_a_fabricated_token_match():
    ds, dt = decoder(("a", "b")), decoder((" a ", "c", "d"))
    sl = torch.tensor([[.2, -.2]], requires_grad=True)
    tl = torch.tensor([[.3, -.2, .4]])
    # Alignment accepts whitespace equivalence, but event matching must be exact.
    loss, audit = common_support_loss(sl, tl, (0,), (0,), (Chunk(0, 1, 0, 1, 0, 1),), ds, dt)
    assert audit["accepted_chunks"] == 0
    assert audit["kd"].item() == 0
    torch.testing.assert_close(loss, torch.nn.functional.cross_entropy(sl, torch.tensor([0])))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_trains_tiny_models_without_pretrained_or_benchmark_calls(seed):
    result = diagnostic(seed)
    assert result["metrics"]["optimizer_updates"] == 3
    assert result["metrics"]["student_vocabulary"] != result["metrics"]["teacher_vocabulary"]
    assert all(result["checks"].values())
    assert all(torch.isfinite(torch.tensor(value)) for value in result["metrics"].values())
