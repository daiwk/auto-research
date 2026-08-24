from pathlib import Path

import numpy as np

from auto_research.reproductions.historical_b04_b06 import HistoricalMechanism, SPECS
from auto_research.reproductions.historical_b04_b06_metadata import ENTRIES
from auto_research.reproductions.industrial_2026 import IndustrialData
from auto_research.reproductions.industrial_batch import CompactSequences
from auto_research.reproductions.registry import get_adapter


def fixture_data() -> IndustrialData:
    features = np.asarray([
        [1, 0, 0], [.9, .1, 0], [0, 1, 0], [.1, .9, 0],
        [0, 0, 1], [.1, 0, .9], [.5, .5, 0], [0, .5, .5],
    ], dtype=float)
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-9)
    sequences = CompactSequences(
        train=((0, 1, 2, 3, 4), (2, 3, 6, 1, 7), (4, 5, 7, 2, 6)),
        validation=(5, 0, 3), test=(6, 4, 1), features=features,
        popularity=np.asarray([8, 7, 6, 5, 4, 3, 2, 1], dtype=float),
    )
    transition = np.full((8, 8), .01)
    for sequence in sequences.train:
        for left, right in zip(sequence, sequence[1:]):
            transition[left, right] += 1
    transition /= transition.sum(1, keepdims=True)
    popularity = np.log1p(sequences.popularity)
    popularity /= popularity.max()
    return IndustrialData(
        sequences, transition, features @ features.T, popularity,
        np.argmax(features, axis=1),
    )


def test_all_nineteen_papers_register_with_complete_verified_metadata():
    assert len(ENTRIES) == 19
    for key, entry in ENTRIES.items():
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == entry.arxiv_id
        assert adapter.paper.organization == entry.organization
        assert adapter.paper.published == entry.published
        assert adapter.paper.has_online_ab
        assert adapter.paper.code_url is None
        evidence = adapter.paper.online_ab[0]
        assert evidence.source_url.endswith(f"{entry.arxiv_id}v1")
        assert evidence.source_location == entry.source_location
        package = key.replace("-", "_")
        assert Path(f"src/auto_research/reproductions/{package}/model.py").exists()


def test_each_paper_executes_its_fitted_mechanism():
    data = fixture_data()
    signatures = {}
    for key, spec in SPECS.items():
        model = HistoricalMechanism(spec.mode, seed=42).fit(data)
        scores = model.score(data, data.sequences.train[0])
        assert scores.shape == (data.item_count,)
        assert np.isfinite(scores).all()
        assert model.diagnostics()["fitted"] is True
        signatures[key] = tuple(np.round(scores, 8))
    assert len(set(signatures.values())) == len(SPECS)
