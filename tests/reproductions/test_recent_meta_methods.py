import numpy as np
import torch

from auto_research.reproductions.cmsl.model import build_cmsl_model
from auto_research.reproductions.g2rec.model import coengagement_edges
from auto_research.reproductions.llatte.model import build_llatte_model
from auto_research.reproductions.memento.model import maximal_marginal_relevance
from auto_research.reproductions.self_evolving_rec.model import LLMResearchAgent, candidate_space


class _Model:
    context = np.asarray([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]])
    item = context.copy()


def test_cmsl_learns_contextual_lenses_and_hstu():
    model = build_cmsl_model(5, dimensions=8, lenses=2)
    history = torch.tensor([[5, 0, 1, 2]])
    mask = history.ne(5)
    loss = model(history, mask, torch.tensor([3])).sum()
    loss.backward()
    assert model.lens_queries.grad is not None
    assert model.hstu.qkv.weight.grad is not None


def test_g2rec_builds_sparse_windowed_coengagement_graph():
    edges, weights, degree = coengagement_edges(((0, 1, 2), (2, 1)), 3, window=1)
    assert {tuple(edge) for edge in edges} == {(0, 1), (1, 2)}
    assert np.all(weights > 0)
    assert degree[1] > degree[0]


def test_memento_mmr_avoids_redundant_memories():
    documents = np.asarray([[1.0, 0.0], [0.99, 0.01], [0.0, 1.0]])
    selected = maximal_marginal_relevance(documents, np.asarray([1.0, 0.0]), 0.4, 2)
    assert selected == [0, 2]


def test_llatte_combines_online_and_cached_upstream_stages():
    model = build_llatte_model(np.random.default_rng(2).normal(size=(5, 6)), dimensions=8)
    history = torch.tensor([[5, 0, 1, 2]])
    mask = history.ne(5)
    score = model(history, mask, torch.tensor([3]))
    score.sum().backward()
    assert score.shape == (1,)
    assert model.latent_queries.grad is not None
    assert model.dhen_gate[-1].weight.grad is not None


def test_self_evolving_search_contains_paper_discoveries():
    candidates = candidate_space()
    assert {candidate.optimizer for candidate in candidates} == {"adagrad", "rmsprop"}
    assert any(candidate.gated and candidate.multi_objective_reward for candidate in candidates)
    prompt = LLMResearchAgent.prompt([
        {"candidate": "baseline", "validation_ndcg_at_10": 0.01}
    ])
    assert "baseline" in prompt and "0.010000" in prompt
