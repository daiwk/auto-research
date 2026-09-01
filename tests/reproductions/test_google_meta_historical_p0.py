import json
from pathlib import Path
import re

import numpy as np

from auto_research.evolution.papers import INSTALLED_MUTATIONS
from auto_research.evolution.planner import allowed_architectures
from auto_research.reproductions.hill_index.model import build_hill, hill_candidates
from auto_research.reproductions.memory_layer.model import build_memory_layer, memory_diagnostics
from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.scalr.model import build_translation, synthesize_events
from auto_research.reproductions.semantic_native_longseq.model import (
    build_semantic_native,
    score_semantic_long,
)


class _Sequences:
    features = np.eye(24, 8, dtype=np.float64)
    train = tuple(tuple((user * 3 + step) % 24 for step in range(16)) for user in range(8))
    validation = tuple((user * 3 + 16) % 24 for user in range(8))
    test = tuple((user * 3 + 17) % 24 for user in range(8))


class _Data:
    sequences = _Sequences()
    item_count = 24
    popularity = np.linspace(0.0, 1.0, 24)
    cosine = _Sequences.features @ _Sequences.features.T
    transition = np.full((24, 24), 1 / 24, dtype=np.float64)
    domains = np.arange(24) % 4
    item_features = _Sequences.features
    train = _Sequences.train


KEYS = ("memory-layer", "scalr", "hill-index", "semantic-native-longseq")
IDS = ("2607.25110", "2606.00282", "2604.12965", "2606.07546")


def test_google_meta_adapters_have_full_evidence_and_evolve_operators():
    for key, arxiv_id in zip(KEYS, IDS):
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == arxiv_id
        assert adapter.paper.organization
        assert adapter.paper.published.startswith("2026-")
        assert adapter.paper.has_online_ab
        assert adapter.evolve_operators
        assert arxiv_id in INSTALLED_MUTATIONS
        assert adapter.requires_gpu_validation is False


def test_four_paper_mechanisms_execute_their_distinct_paths():
    memory = build_memory_layer(_Data)
    diagnostics = memory_diagnostics(memory)
    assert diagnostics["memory_coverage"] >= diagnostics["snapshot_coverage"]
    assert diagnostics["prediction_coverage_with_always_on"] == 1.0

    translation = build_translation(_Data)
    synthetic = synthesize_events(_Data, translation, seed=42)
    assert synthetic["sampled_catalog_coverage"] > synthetic["deterministic_catalog_coverage"]

    hill = build_hill(_Data, seed=42, coarse_width=4, fine_width=3)
    candidates = hill_candidates(_Data, hill, _Sequences.train[0], coarse_beam=2, fine_beam=1)
    assert 0 < len(candidates) < _Data.item_count

    semantic = build_semantic_native(_Data, seed=42, width=4)
    scores, trace = score_semantic_long(_Data, semantic, _Sequences.train[0], folding=4)
    assert scores.shape == (_Data.item_count,)
    assert trace["folded_tokens"] < trace["input_events"]
    assert trace["attention_pair_reduction"] > 0


def test_rankmixer_evolve_variants_are_selectable_and_executable():
    import torch

    from auto_research.reproductions.rankmixer.model import RankMixerConfig, build_model

    expected = {
        "Memory Layer writeback": "rankmixer_memory_layer",
        "HILL hierarchical index": "rankmixer_hill_index",
        "semantic-native temporal folding": "rankmixer_semantic_native_longseq",
    }
    config = RankMixerConfig(dimensions=16, tokens=4, layers=1, sequence_length=12)
    history = torch.arange(12)[None]
    for direction, architecture in expected.items():
        assert allowed_architectures("rankmixer", direction, [])[0] == architecture
        model = build_model(architecture, _Data, config)
        logits = model(history)
        assert logits.shape == (1, _Data.item_count)
        logits.mean().backward()


def test_historical_p0_roadmap_contains_every_promoted_id_once():
    root = Path(__file__).resolve().parents[2]
    decisions = json.loads(
        (root / "docs/paper-audits/2026-historical-fulltext-decisions.json").read_text()
    )["decisions"]
    expected = {row["arxiv_id"] for row in decisions if row["decision"] == "promoted-p0"}
    roadmap = (root / "docs/paper-audits/2026-historical-p0-implementation-roadmap.md").read_text()
    observed = re.findall(r"`(26\d{2}\.\d{5})`", roadmap)
    assert len(expected) == len(observed) == 55
    assert expected == set(observed)


def test_metric_artifacts_are_formal_three_seed_results():
    root = Path(__file__).resolve().parents[2]
    for key, arxiv_id in zip(KEYS, IDS):
        artifact = (
            root / "docs/reproductions" / f"{arxiv_id}-{key}" / "metrics/public-seeds42-44.json"
        )
        payload = json.loads(artifact.read_text())
        assert payload["evaluation_protocol"]["formal_comparison"] is True
        assert payload["evaluation_protocol"]["seeds"] == [42, 43, 44]
        assert len(payload["seed_results"]) == 3
