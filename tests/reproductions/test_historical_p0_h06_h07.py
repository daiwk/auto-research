import json
from pathlib import Path

import numpy as np

from auto_research.evolution.genrec import _context, _initial_catalog, _reward
from auto_research.evolution.models import Genome
from auto_research.evolution.papers import INSTALLED_MUTATIONS
from auto_research.reproductions.genrec_netflix.data import GenRecData
from auto_research.reproductions.historical_p0_h06_h07 import SCORERS, diagnostics
from auto_research.reproductions.registry import get_adapter


KEYS = (
    "unimvt", "rq-gmm", "capts", "mlcc", "ug-sep", "smes", "pit", "zenith",
    "easq", "s2gr", "sparsectr", "hcub", "airbnb-ebr", "promise", "harmonrank",
)
INTERNAL = (
    "unimvt", "rq_gmm", "capts", "mlcc", "ug_sep", "smes", "pit", "zenith",
    "easq", "s2gr", "sparsectr", "hcub", "airbnb_ebr", "promise", "harmonrank",
)
IDS = (
    "2602.12972", "2602.12593", "2602.12564", "2602.12041", "2602.10455",
    "2602.09386", "2602.08530", "2601.21285", "2601.20215", "2601.18664",
    "2601.17836", "2601.14333", "2601.06873", "2601.04674", "2601.02955",
)


class _Sequences:
    rng = np.random.default_rng(31)
    features = rng.normal(size=(40, 12))
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-12)
    train = tuple(tuple((user * 7 + step * 3) % 40 for step in range(24)) for user in range(10))
    validation = tuple((user * 7 + 33) % 40 for user in range(10))
    test = tuple((user * 7 + 36) % 40 for user in range(10))


class _Data:
    sequences = _Sequences()
    item_count = 40
    popularity = np.linspace(0.02, 1.0, 40)
    cosine = _Sequences.features @ _Sequences.features.T
    transition = np.full((40, 40), 1e-3)
    for sequence in _Sequences.train:
        for left, right in zip(sequence, sequence[1:]):
            transition[left, right] += 1
    transition /= transition.sum(1, keepdims=True)
    domains = np.arange(40) % 8


def _genrec_data():
    return GenRecData(
        train=_Sequences.train,
        validation=_Sequences.validation,
        test=_Sequences.test,
        item_texts=tuple(f"item {index}" for index in range(40)),
        item_genres=tuple((("even", "popular") if index % 2 == 0 else ("odd",)) for index in range(40)),
        popularity=np.arange(40, dtype=np.float64) + 1,
    )


def test_h06_h07_adapters_have_complete_evidence_and_cpu_contracts():
    for key, paper_id in zip(KEYS, IDS):
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == paper_id
        assert adapter.paper.organization and adapter.paper.published.startswith("2026-")
        assert adapter.paper.has_online_ab
        assert adapter.default_seeds == (42, 43, 44)
        assert adapter.device_capabilities == ("cpu",)
        assert adapter.requires_gpu_validation is False
        assert INSTALLED_MUTATIONS[paper_id][0] == adapter.evolve_operators[0]


def test_h06_h07_methods_execute_fifteen_distinct_mechanisms():
    history = _Sequences.train[0]
    outputs = []
    for key in INTERNAL:
        scores = SCORERS[key](_Data, history)
        assert scores.shape == (40,)
        assert np.isfinite(scores).all() and np.std(scores) > 0
        outputs.append(scores)
        assert diagnostics(key, _Data, history)["finite_scores"] == 40
    assert all(
        not np.allclose(left, right)
        for index, left in enumerate(outputs)
        for right in outputs[index + 1 :]
    )
    assert diagnostics("sparsectr", _Data, history)["sparse_attention_branches"] == 3
    assert diagnostics("promise", _Data, history)["process_reward_steps"] == 4


def test_h06_h07_genrec_operators_execute():
    data = _genrec_data()
    rng = np.random.default_rng(42)
    for head in (
        "residual-gmm", "multi-level-cross", "ug-separation",
        "personalized-tokenizer", "stepwise-semantic-reasoning",
    ):
        catalog = _initial_catalog(data, Genome(dimensions=12, genrec_head=head), rng)
        assert catalog.shape == (40, 12) and np.isfinite(catalog).all()
    catalog = rng.normal(size=(40, 12))
    for context in (
        "channel-trigger-routing", "questionnaire-alignment",
        "evolutionary-sparse-attention", "hierarchical-uplift", "journey-retrieval",
    ):
        user, items, weights = _context(_Sequences.train[0], catalog, context, 12)
        assert user.shape == (12,) and len(items) == len(weights)
        assert np.isclose(weights.sum(), 1.0)
    for reward in ("causal-uplift", "expert-balance", "process-reward", "rank-consistency"):
        assert np.isfinite(_reward(data, _Sequences.train[0], 7, reward))


def test_h06_h07_docs_have_metadata_figures_and_three_seed_metrics():
    root = Path(__file__).resolve().parents[2]
    for key, paper_id in zip(KEYS, IDS):
        doc = root / "docs/reproductions" / f"{paper_id}-{key}"
        readme = (doc / "README.md").read_text()
        assert "## 论文信息" in readme
        assert "原文开源代码 |" in readme
        assert f"Adapter | `{key}`" in readme
        assert "首次公开日期 | 2026-" in readme
        assert (doc / "assets/paper-figure-01.png").stat().st_size > 10_000
        payload = json.loads((doc / "metrics/public-seeds42-44.json").read_text())
        assert payload["manifest_ref"] == f"reproduction:{key}"
        assert payload["manifest"]["evolve_operators"]
        assert payload["evaluation_protocol"]["formal_comparison"] is True
        assert payload["evaluation_protocol"]["seeds"] == [42, 43, 44]
        assert len(payload["seed_results"]) == 3


def test_h06_h07_roadmap_done_only_after_artifacts_exist():
    root = Path(__file__).resolve().parents[2]
    roadmap = (root / "docs/paper-audits/2026-historical-p0-implementation-roadmap.md").read_text()
    h06 = next(row for row in roadmap.splitlines() if "H06 ·" in row)
    h07 = next(row for row in roadmap.splitlines() if "H07 ·" in row)
    assert "| DONE | 8 |" in h06
    assert "| DONE | 7 |" in h07
    assert all(f"`{paper_id}`" in h06 or f"`{paper_id}`" in h07 for paper_id in IDS)
