"""Negative controls for new source parsing and seven bounded operators."""

import importlib
import numpy as np
import pytest
import torch


@pytest.mark.parametrize(
    "name",
    [
        "foundation_models.dealrank",
        "foundation_models.unigraph",
        "foundation_models.simq",
        "foundation_models.efficient_evals_tensor",
        "reproductions.yuanbao_rubric_components",
        "reproductions.cotti_components",
        "reproductions.intentflow_components",
    ],
)
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_actual_root_diagnostics(name, seed):
    result = importlib.import_module("auto_research." + name).diagnostic(seed)
    assert result["diagnostic_only"] is True and result["evaluation_tier"] == "l1_mechanism"
    assert all(value is True for value in result["checks"].values())


@pytest.mark.parametrize(
    "name",
    [
        "foundation_models.dealrank",
        "foundation_models.unigraph",
        "foundation_models.simq",
        "foundation_models.efficient_evals_tensor",
        "reproductions.yuanbao_rubric_components",
        "reproductions.cotti_components",
        "reproductions.intentflow_components",
    ],
)
def test_diagnostic_seed_rejects_boolean(name):
    with pytest.raises(ValueError):
        importlib.import_module("auto_research." + name).diagnostic(True)


def test_absolute_google_directory_links():
    from prepare_nov18_priority_sources import paper_links

    assert paper_links(
        ["/pubs/", "/pubs/a/", "https://research.google/pubs/b/", "https://evil.example/pubs/c/"]
    ) == {"/pubs/a/", "/pubs/b/"}


def test_priority_link_parser_imports_without_site_packages():
    """Source capture's optional HTML parser must not leak into the pure normalizer."""
    from pathlib import Path
    import subprocess
    import sys

    path = Path(__file__).resolve().parents[1] / "scripts/prepare_nov18_priority_sources.py"
    code = (
        "import importlib.util; "
        f"s=importlib.util.spec_from_file_location('priority',{str(path)!r}); "
        "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
        "assert m.paper_links(['https://research.google/pubs/example/'])=={'/pubs/example/'}"
    )
    subprocess.run([sys.executable, "-S", "-c", code], check=True, capture_output=True)


def test_dealrank_hierarchy_and_bad_ranker():
    from auto_research.foundation_models.dealrank import schedule

    for n, rounds, calls in [(20, 1, 1), (100, 2, 6), (500, 3, 30), (1000, 3, 56)]:
        ids = [str(i) for i in range(n)]
        result = schedule(ids, lambda group: sorted(group, key=int))
        assert result["ranking"][:2] == ids[:2]
        assert len(result["rounds"]) == rounds and result["calls"] == calls
    with pytest.raises(ValueError):
        schedule(["a", "b"], lambda _: ["a", "a"])
    with pytest.raises(ValueError):
        schedule([str(i) for i in range(101)], lambda x: x)


def test_dealrank_hierarchical_final_uses_retriever_order():
    from auto_research.foundation_models.dealrank import schedule

    calls = []

    def ranker(group):
        calls.append(group)
        return sorted(group, key=int, reverse=True)

    schedule([str(i) for i in range(1000)], ranker, workers=1)
    assert list(calls[-1]) == sorted(calls[-1], key=int)


def test_unigraph_unsafe_scale_not_called_safe():
    from auto_research.foundation_models.unigraph import alpha_cover, search

    dense = np.eye(4)
    sparse = np.eye(4)
    graph = alpha_cover(dense, sparse, neighbors=2, degree=3)
    out = search(dense, sparse, graph, dense[0], sparse[0], alpha=0.5, k=1, beam=2, gamma=0.3)
    assert not out["safe_pruning"] and out["guide"] == "sparse"
    with pytest.raises(ValueError):
        search(dense, sparse, graph, dense[0], sparse[0], alpha=2)


def test_simq_tie_expands_minimum_and_no_duplicate_token_count():
    from auto_research.foundation_models.simq import Index

    index = Index([[[1.0, 0.0]], [[1.0, 0.0]], [[0.0, 1.0]]], ratio=1, cluster_limit=1, degree=2)
    out = index.query([[1.0, 0.0]], centroid_count=2, beam=3, plus=True, minimum_candidates=1, k=1)
    assert out["candidates"] == [0, 1] and out["counts"] == {0: 1, 1: 1}


def test_yuanbao_distills_best_not_failed_rollout():
    from auto_research.reproductions.yuanbao_rubric_components import (
        dual_branch_loss,
        focal_pairwise,
    )

    lp = torch.tensor([[[-1.0, -2.0], [-3.0, -4.0]]], requires_grad=True)
    mask = torch.ones_like(lp, dtype=torch.bool)
    result = dual_branch_loss(lp, lp.detach(), mask, torch.tensor([[0.0, 2.0]]))
    assert torch.isclose(result["distill"], torch.tensor(7.0))
    (grad,) = torch.autograd.grad(result["distill"], lp)
    assert torch.equal(grad[0, 0], torch.zeros(2)) and (grad[0, 1] < 0).all()
    scores = torch.tensor([[2.0, 1.0]], requires_grad=True)
    assert focal_pairwise(scores, torch.tensor([[1.0, 1.0]])) == 0
    with pytest.raises(ValueError):
        dual_branch_loss(lp, lp.detach(), torch.zeros_like(mask), torch.tensor([[0.0, 2.0]]))
    with pytest.raises(ValueError):
        dual_branch_loss(lp, lp.detach(), mask, torch.tensor([[0.0, 2.0]]), kl_weight=0.1)


def test_cotti_population_variance_and_unclipped_weights():
    from auto_research.reproductions.cotti_components import historical_weights, event_adjustment

    item = torch.tensor([[0.0], [1.0], [4.0]], requires_grad=True)
    w = historical_weights(item, torch.zeros_like(item), 0.5)
    expected = torch.exp(
        -0.5
        * (item.detach().square().squeeze() - item.detach().square().mean())
        / (item.detach().square().std(correction=0) + 1e-8)
    )
    assert torch.allclose(w, expected) and not w.requires_grad
    assert not torch.isclose(w.mean(), torch.tensor(1.0))
    base = torch.zeros(1)
    samples = torch.tensor([[-1.0], [1.0]])
    output = event_adjustment(base, samples, time=0, peak=0, event_width=1, amplitude=0.5, beta=1)
    assert torch.allclose(output, torch.tensor([0.5 * torch.tanh(torch.tensor(1.0))]).sigmoid())
    with pytest.raises(ValueError):
        event_adjustment(base, samples, time=0, peak=0, event_width=0, amplitude=0.5, beta=1)


def test_intentflow_masked_distribution_and_teacher_detach():
    from auto_research.reproductions.intentflow_components import distribution_distillation

    scores = torch.randn(3, 3, requires_grad=True)
    teacher = torch.randn(3, 3, requires_grad=True)
    valid = ~torch.eye(3, dtype=torch.bool)
    loss = distribution_distillation(scores, teacher, valid)
    loss.backward()
    assert (
        torch.isfinite(loss)
        and teacher.grad is None
        and torch.equal(scores.grad.diag(), torch.zeros(3))
    )
    assert torch.allclose(
        distribution_distillation(scores, scores.detach(), valid), torch.tensor(0.0), atol=1e-7
    )


def test_efficient_evals_ordered_ratings_pairwise_ties_and_covariance():
    from auto_research.foundation_models.efficient_evals_tensor import (
        ordinal_probabilities,
        conditional_wald,
        frozen_human_nll,
    )

    with pytest.raises(ValueError):
        ordinal_probabilities(torch.tensor(0.0), torch.tensor([1.0, 0.0]))
    models = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    prompts = torch.tensor([[1.0, 1.0]])
    human = torch.tensor([1.0, 1.0], requires_grad=True)
    loss = frozen_human_nll(
        models,
        prompts,
        human,
        torch.tensor([-0.5, 0.5]),
        torch.tensor([0]),
        torch.tensor([0]),
        torch.tensor([1]),
        opponents=torch.tensor([1]),
    )
    assert torch.isfinite(loss)
    with pytest.raises(ValueError):
        conditional_wald(torch.ones(2), human, torch.tensor([[1.0, 2.0], [2.0, 1.0]]), 4)
