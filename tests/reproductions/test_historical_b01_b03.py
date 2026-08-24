from pathlib import Path

import numpy as np

from auto_research.reproductions.historical_b01_b03 import HistoricalMechanism, SPECS
from auto_research.reproductions.historical_b01_b03_metadata import ENTRIES
from auto_research.reproductions.industrial_2026 import IndustrialData
from auto_research.reproductions.industrial_batch import CompactSequences
from auto_research.reproductions.registry import get_adapter


def fixture_data() -> IndustrialData:
    features = np.asarray([
        [1, 0, 0], [0.9, .1, 0], [0, 1, 0], [.1, .9, 0],
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


def test_all_eighteen_papers_register_with_verified_online_evidence():
    assert len(ENTRIES) == 18
    for key, entry in ENTRIES.items():
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == entry.arxiv_id
        assert adapter.paper.organization == entry.organization
        assert adapter.paper.published == entry.published
        assert adapter.paper.has_online_ab
        assert Path(f"src/auto_research/reproductions/{key.replace('-', '_')}/model.py").exists()


def test_each_paper_executes_a_distinct_fitted_mechanism():
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


def test_official_code_links_are_not_inferred_for_closed_sources():
    assert get_adapter("recharness").paper.code_url == "https://github.com/6lyc/RecHarness"
    assert get_adapter("guess-where-you-go").paper.code_url == "https://github.com/alibaba/SimCIT"
    assert get_adapter("dadf").paper.code_url == "https://github.com/liuzhao09/DADF"
    assert get_adapter("genpage").paper.code_url is None

