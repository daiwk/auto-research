import json
from pathlib import Path

import numpy as np

from auto_research.evolution.genrec import _context, _initial_catalog, _reward
from auto_research.evolution.models import Genome, PaperInspiration
from auto_research.evolution.papers import INSTALLED_MUTATIONS
from auto_research.evolution.planner import allowed_architectures
from auto_research.reproductions.genrec_netflix.data import GenRecData
from auto_research.reproductions.historical_p0_h05 import SCORERS, diagnostics
from auto_research.reproductions.registry import get_adapter


KEYS = ("marc", "rankup", "sid-coord", "rclrec", "tagllm", "genfacet", "cgr", "hpgr", "climber-pilot", "rolegen")
INTERNAL = ("marc", "rankup", "sid_coord", "rclrec", "tagllm", "genfacet", "cgr", "hpgr", "climber_pilot", "rolegen")
IDS = ("2604.18146", "2604.17878", "2604.10471", "2603.28124", "2603.21481", "2603.19665", "2603.04227", "2603.00980", "2602.13581", "2602.13134")


class _Sequences:
    rng = np.random.default_rng(29)
    features = rng.normal(size=(36, 12))
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-12)
    train = tuple(tuple((user * 7 + step * 3) % 36 for step in range(20)) for user in range(10))
    validation = tuple((user * 7 + 25) % 36 for user in range(10))
    test = tuple((user * 7 + 28) % 36 for user in range(10))


class _Data:
    sequences = _Sequences()
    item_count = 36
    popularity = np.linspace(0.02, 1.0, 36)
    cosine = _Sequences.features @ _Sequences.features.T
    transition = np.full((36, 36), 1e-3)
    for sequence in _Sequences.train:
        for left, right in zip(sequence, sequence[1:]):
            transition[left, right] += 1
    transition /= transition.sum(1, keepdims=True)
    domains = np.arange(36) % 6


def _genrec_data():
    return GenRecData(
        train=_Sequences.train,
        validation=_Sequences.validation,
        test=_Sequences.test,
        item_texts=tuple(f"item {index}" for index in range(36)),
        item_genres=tuple((("even", "popular") if index % 2 == 0 else ("odd",)) for index in range(36)),
        popularity=np.arange(36, dtype=np.float64) + 1,
    )


def test_h05_adapters_have_complete_evidence_and_executable_operators():
    papers = []
    for key, paper_id in zip(KEYS, IDS):
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == paper_id
        assert adapter.paper.organization and adapter.paper.published.startswith("2026-")
        assert adapter.paper.has_online_ab
        assert adapter.default_seeds == (42, 43, 44)
        assert adapter.device_capabilities == ("cpu",)
        assert adapter.requires_gpu_validation is False
        operator = adapter.evolve_operators[0]
        assert INSTALLED_MUTATIONS[paper_id][0] == operator
        papers.append(PaperInspiration(paper_id, adapter.paper.title, adapter.paper.url, adapter.paper.published, operator, "core", "installed", executable=True))
    allowed = allowed_architectures("genrec", "H05", papers)
    assert {INSTALLED_MUTATIONS[paper_id][0] for paper_id in IDS}.issubset(allowed)


def test_h05_methods_execute_ten_distinct_mechanisms():
    history = _Sequences.train[0]
    outputs = []
    for key in INTERNAL:
        scores = SCORERS[key](_Data, history)
        assert scores.shape == (36,) and np.isfinite(scores).all() and np.std(scores) > 0
        outputs.append(scores)
        assert diagnostics(key, _Data, history)["finite_scores"] == 36
    assert all(not np.allclose(left, right) for index, left in enumerate(outputs) for right in outputs[index + 1 :])
    assert diagnostics("rankup", _Data, history)["permuted_embedding_views"] == 3
    assert diagnostics("sid_coord", _Data, history)["semantic_id_levels"] == 3
    assert diagnostics("cgr", _Data, history)["bounded_decoder_steps"] == 20


def test_h05_genrec_operators_execute():
    data = _genrec_data()
    rng = np.random.default_rng(42)
    for head in ("modular-compression", "high-rank-representation", "sid-coordination", "fine-grained-tags"):
        catalog = _initial_catalog(data, Genome(dimensions=12, genrec_head=head), rng)
        assert catalog.shape == (36, 12) and np.isfinite(catalog).all()
    catalog = rng.normal(size=(36, 12))
    for context in ("reverse-curriculum", "hierarchical-preference", "instruction-foresight"):
        user, items, weights = _context(_Sequences.train[0], catalog, context, 12)
        assert user.shape == (12,) and len(items) == len(weights) and np.isclose(weights.sum(), 1.0)
    for reward in ("facet-preference", "constraint-aware", "counterfactual-role"):
        value = _reward(data, _Sequences.train[0], 7, reward)
        assert np.isfinite(value) and value > 0


def test_h05_docs_have_metadata_original_figures_and_three_seed_metrics():
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
        assert payload["manifest"]["local_code_dir"].endswith(f"/reproductions/{key.replace('-', '_')}")
        assert payload["manifest"]["evolve_operators"]
        assert payload["evaluation_protocol"]["formal_comparison"] is True
        assert payload["evaluation_protocol"]["seeds"] == [42, 43, 44]
        assert len(payload["seed_results"]) == 3


def test_h05_roadmap_done_only_after_artifacts_exist():
    root = Path(__file__).resolve().parents[2]
    roadmap = (root / "docs/paper-audits/2026-historical-p0-implementation-roadmap.md").read_text()
    line = next(row for row in roadmap.splitlines() if "H05 ·" in row)
    assert "| DONE | 10 |" in line
    assert all(f"`{paper_id}`" in line for paper_id in IDS)
