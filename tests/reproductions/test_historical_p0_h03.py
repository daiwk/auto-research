import json
from pathlib import Path

import numpy as np

from auto_research.evolution.genrec import _context, _initial_catalog
from auto_research.evolution.models import Genome, PaperInspiration
from auto_research.evolution.papers import INSTALLED_MUTATIONS
from auto_research.evolution.planner import allowed_architectures
from auto_research.reproductions.genrec_netflix.data import GenRecData
from auto_research.reproductions.historical_p0_h03 import SCORERS, diagnostics
from auto_research.reproductions.registry import get_adapter


KEYS = ("specformer", "egr", "zorro", "elise", "poem", "uniformer", "rag-generation", "onerank", "piano")
INTERNAL = ("specformer", "egr", "zorro", "elise", "poem", "uniformer", "rag_generation", "onerank", "piano")
IDS = ("2607.24025", "2607.23038", "2607.10910", "2607.10239", "2606.29946", "2606.27058", "2606.25496", "2606.16838", "2606.16641")


class _Sequences:
    rng = np.random.default_rng(9)
    features = rng.normal(size=(32, 12))
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-12)
    train = tuple(tuple((user * 3 + step) % 32 for step in range(18)) for user in range(10))
    validation = tuple((user * 3 + 18) % 32 for user in range(10))
    test = tuple((user * 3 + 19) % 32 for user in range(10))


class _Data:
    sequences = _Sequences()
    item_count = 32
    popularity = np.linspace(0.0, 1.0, 32)
    cosine = _Sequences.features @ _Sequences.features.T
    transition = np.full((32, 32), 1e-3)
    for sequence in _Sequences.train:
        for left, right in zip(sequence, sequence[1:]):
            transition[left, right] += 1
    transition /= transition.sum(1, keepdims=True)
    domains = np.arange(32) % 5


def test_h03_adapters_have_complete_evidence_and_executable_operators():
    papers = []
    for key, paper_id in zip(KEYS, IDS):
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == paper_id
        assert adapter.paper.organization and adapter.paper.published.startswith("2026-")
        assert adapter.paper.has_online_ab
        assert adapter.default_seeds == (42, 43, 44)
        assert adapter.requires_gpu_validation is False
        operator = adapter.evolve_operators[0]
        assert INSTALLED_MUTATIONS[paper_id][0] == operator
        papers.append(PaperInspiration(paper_id, adapter.paper.title, adapter.paper.url, adapter.paper.published, operator, "core", "installed", executable=True))
    allowed = allowed_architectures("genrec", "H03", papers)
    assert {INSTALLED_MUTATIONS[paper_id][0] for paper_id in IDS}.issubset(allowed)


def test_h03_methods_execute_nine_distinct_mechanisms():
    history = _Sequences.train[0]
    outputs = []
    for key in INTERNAL:
        scores = SCORERS[key](_Data, history)
        assert scores.shape == (32,) and np.isfinite(scores).all() and np.std(scores) > 0
        outputs.append(scores)
        info = diagnostics(key, _Data, history)
        assert info["finite_scores"] == 32
    assert all(not np.allclose(left, right) for i, left in enumerate(outputs) for right in outputs[i + 1 :])
    assert diagnostics("zorro", _Data, history)["trainable_parameters"] == 0
    assert diagnostics("rag_generation", _Data, history)["sid_levels"] == 3
    assert diagnostics("onerank", _Data, history)["gradient_detach_boundaries"] == 2


def test_h03_genrec_operators_execute():
    data = GenRecData(
        train=_Sequences.train, validation=_Sequences.validation, test=_Sequences.test,
        item_texts=tuple(f"item {index}" for index in range(32)),
        item_genres=tuple((("even",) if index % 2 == 0 else ("odd",)) for index in range(32)),
        popularity=np.arange(32, dtype=np.float64) + 1,
    )
    rng = np.random.default_rng(42)
    for head in ("embedding-native", "disentangled-sid", "unified-ranker", "listwise-node"):
        catalog = _initial_catalog(data, Genome(dimensions=12, genrec_head=head), rng)
        assert catalog.shape == (32, 12) and np.isfinite(catalog).all()
    catalog = rng.normal(size=(32, 12))
    for context in ("spectral-soften", "zero-weight", "quantile-fusion", "partial-order", "unified-token"):
        user, items, weights = _context(_Sequences.train[0], catalog, context, 12)
        assert user.shape == (12,) and len(items) == len(weights) and np.isclose(weights.sum(), 1.0)


def test_h03_docs_have_metadata_original_figures_and_three_seed_metrics():
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
        assert payload["evaluation_protocol"]["formal_comparison"] is True
        assert payload["evaluation_protocol"]["seeds"] == [42, 43, 44]
        assert len(payload["seed_results"]) == 3


def test_h03_roadmap_done_only_after_artifacts_exist():
    root = Path(__file__).resolve().parents[2]
    roadmap = (root / "docs/paper-audits/2026-historical-p0-implementation-roadmap.md").read_text()
    line = next(row for row in roadmap.splitlines() if "H03 ·" in row)
    assert "| DONE | 9 |" in line
    assert all(f"`{paper_id}`" in line for paper_id in IDS)
