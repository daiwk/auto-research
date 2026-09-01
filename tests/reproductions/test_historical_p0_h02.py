import json
from pathlib import Path

import numpy as np

from auto_research.evolution.models import PaperInspiration
from auto_research.evolution.papers import INSTALLED_MUTATIONS
from auto_research.evolution.planner import allowed_architectures
from auto_research.reproductions.director.model import hard_global_match, transport_plan
from auto_research.reproductions.drem.model import build_drem, robustness_diagnostics, score_drem
from auto_research.reproductions.incrementality.model import (
    build_incrementality_problem,
    evaluate_policy,
)
from auto_research.reproductions.psg.model import decode_pairs
from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.reward_guided_decoding.model import (
    business_reward,
    reward_guided_distribution,
)
from auto_research.reproductions.snaplgr.model import build_snaplgr, snaplgr_diagnostics
from auto_research.reproductions.tm20k.model import score_tm20k, tm20k_diagnostics
from auto_research.reproductions.transx.model import score_transx, transx_diagnostics


class _Sequences:
    rng = np.random.default_rng(7)
    features = rng.normal(size=(24, 8))
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-12)
    train = tuple(tuple((user * 3 + step) % 24 for step in range(16)) for user in range(8))
    validation = tuple((user * 3 + 16) % 24 for user in range(8))
    test = tuple((user * 3 + 17) % 24 for user in range(8))


class _Data:
    sequences = _Sequences()
    item_count = 24
    popularity = np.linspace(0.0, 1.0, 24)
    cosine = _Sequences.features @ _Sequences.features.T
    transition = np.full((24, 24), 1e-3, dtype=np.float64)
    for sequence in _Sequences.train:
        for left, right in zip(sequence, sequence[1:]):
            transition[left, right] += 1
    transition /= transition.sum(axis=1, keepdims=True)
    domains = np.arange(24) % 4


KEYS = (
    "drem",
    "incrementality",
    "tm20k",
    "transx",
    "snaplgr",
    "psg",
    "director",
    "reward-guided-decoding",
)
IDS = (
    "2608.12778",
    "2608.10182",
    "2608.07055",
    "2607.28940",
    "2607.28895",
    "2607.26427",
    "2607.26418",
    "2607.25344",
)


def test_h02_adapters_have_evidence_metadata_and_executable_operators():
    papers = []
    for key, arxiv_id in zip(KEYS, IDS):
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == arxiv_id
        assert adapter.paper.organization
        assert adapter.paper.published.startswith("2026-")
        assert adapter.paper.has_online_ab
        assert adapter.default_seeds == (42, 43, 44)
        assert adapter.requires_gpu_validation is False
        operator = adapter.evolve_operators[0]
        assert INSTALLED_MUTATIONS[arxiv_id][0] == operator
        papers.append(
            PaperInspiration(
                arxiv_id,
                adapter.paper.title,
                adapter.paper.url,
                adapter.paper.published,
                operator,
                "core mechanism",
                "installed",
                executable=True,
            )
        )
    allowed = allowed_architectures("genrec", "H02", papers)
    assert {INSTALLED_MUTATIONS[paper_id][0] for paper_id in IDS}.issubset(allowed)


def test_h02_mechanisms_execute_distinct_computation_paths():
    history = _Sequences.train[0]

    drem = build_drem(_Data, 42)
    robust = score_drem(_Data, drem, history)
    diagnostics = robustness_diagnostics(_Data, drem, history)
    assert robust.shape == (24,)
    assert diagnostics["noise_perturbations"] == 24

    problem = build_incrementality_problem(_Data, 42)
    predictive = evaluate_policy(problem, "predictive_score")
    causal = evaluate_policy(problem, "incremental_score")
    assert predictive["budget_fraction"] == causal["budget_fraction"]
    assert np.isfinite(causal["policy_value"])

    merged = tm20k_diagnostics(_Data, history)
    assert merged["merged_tokens"] < merged["input_tokens"]
    assert merged["distilled_teacher_mse"] < merged["student_teacher_mse"]
    assert score_tm20k(_Data, history).shape == (24,)

    crossed = transx_diagnostics(_Data, history)
    assert crossed["attention_pair_reduction"] > 0
    assert score_transx(_Data, history).shape == (24,)

    snap = build_snaplgr(_Data, 42, width=4)
    assert snaplgr_diagnostics(snap)["grounded_tokens"] > 0

    pairs, slate = decode_pairs(_Data, history, slate_length=6)
    assert len(pairs) == 3
    assert len(slate) == len(set(slate)) == 6

    logits, plan = transport_plan(_Data, history)
    matched = hard_global_match(logits)
    assert len(matched) == len(set(matched)) == 6
    assert np.allclose(plan.sum(axis=1), 1.0)

    prior_logits = np.linspace(-1, 1, 24)
    reward = business_reward(_Data, history)
    guided = reward_guided_distribution(prior_logits, reward)
    prior = np.exp(prior_logits - prior_logits.max())
    prior /= prior.sum()
    assert guided @ reward > prior @ reward


def test_h02_genrec_operators_are_accepted_by_the_evaluator():
    from auto_research.evolution.genrec import _context, _initial_catalog, _reward
    from auto_research.evolution.models import Genome
    from auto_research.reproductions.genrec_netflix.data import GenRecData

    data = GenRecData(
        train=_Sequences.train,
        validation=_Sequences.validation,
        test=_Sequences.test,
        item_texts=tuple(f"item {index}" for index in range(24)),
        item_genres=tuple((("even",) if index % 2 == 0 else ("odd",)) for index in range(24)),
        popularity=np.arange(24, dtype=np.float64) + 1,
    )
    rng = np.random.default_rng(42)
    for head in ("snaplgr-sid", "pair-space", "transport-index"):
        catalog = _initial_catalog(data, Genome(dimensions=8, genrec_head=head), rng)
        assert catalog.shape == (24, 8)
    catalog = rng.normal(size=(24, 8))
    for context in ("tm20k-merge", "transx-cross-stream"):
        user, items, weights = _context(_Sequences.train[0], catalog, context, 8)
        assert user.shape == (8,)
        assert len(items) == len(weights)
        assert np.isclose(weights.sum(), 1.0)
    for reward in ("robust-preference", "incrementality", "reward-guided"):
        assert _reward(data, _Sequences.train[0], 17, reward) > 0


def test_h02_docs_have_original_figures_and_formal_three_seed_artifacts():
    root = Path(__file__).resolve().parents[2]
    for key, arxiv_id in zip(KEYS, IDS):
        doc = root / "docs" / "reproductions" / f"{arxiv_id}-{key}"
        readme = (doc / "README.md").read_text()
        assert "## 论文信息" in readme
        assert "原文开源代码 | 否：论文未提供官方/作者代码" in readme
        assert f"Adapter | `{key}`" in readme
        assert (doc / "assets" / "paper-figure-01.png").stat().st_size > 10_000
        payload = json.loads((doc / "metrics" / "public-seeds42-44.json").read_text())
        assert payload["evaluation_protocol"]["formal_comparison"] is True
        assert payload["evaluation_protocol"]["seeds"] == [42, 43, 44]
        assert len(payload["seed_results"]) == 3


def test_h02_is_marked_done_only_after_all_artifacts_exist():
    root = Path(__file__).resolve().parents[2]
    roadmap = (root / "docs/paper-audits/2026-historical-p0-implementation-roadmap.md").read_text()
    line = next(row for row in roadmap.splitlines() if "H02 ·" in row)
    assert "| DONE | 8 |" in line
    assert all(f"`{arxiv_id}`" in line for arxiv_id in IDS)
