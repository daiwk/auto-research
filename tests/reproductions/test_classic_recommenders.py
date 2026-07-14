import numpy as np
import pytest

from auto_research.reproductions.din.model import DINConfig, build_model as build_din
from auto_research.reproductions.hstu.model import HSTUConfig, build_model as build_hstu
from auto_research.reproductions.sasrec.model import SASRecConfig, build_model as build_sasrec
from auto_research.reproductions.tiger.model import (
    TIGERConfig,
    append_collision_tokens,
    build_model as build_tiger,
)


def test_din_scores_are_candidate_conditioned():
    torch = pytest.importorskip("torch")
    model = build_din("din", 6, np.eye(6, dtype=np.float32), DINConfig(dimensions=8))
    histories = torch.tensor([[0, 1, 2]])
    scores = model(histories, torch.tensor([[3, 4]]))
    assert scores.shape == (1, 2)


def test_sasrec_and_hstu_emit_all_position_logits():
    torch = pytest.importorskip("torch")
    items = torch.tensor([[0, 1, 2, 3]])
    sasrec = build_sasrec(7, SASRecConfig(dimensions=8, heads=2, sequence_length=4))
    hstu = build_hstu(7, HSTUConfig(dimensions=8, heads=2, sequence_length=4))
    assert sasrec(items).shape == hstu(items).shape == (1, 4, 7)


def test_tiger_collision_token_makes_semantic_ids_unique():
    codes = np.asarray([[1, 2, 3], [1, 2, 3], [1, 2, 4]])
    semantic_ids, cardinality = append_collision_tokens(codes)
    assert cardinality == 2
    assert len({tuple(row) for row in semantic_ids}) == 3


def test_tiger_autoregressively_predicts_each_semantic_token():
    torch = pytest.importorskip("torch")
    config = TIGERConfig(
        dimensions=8, heads=2, layers=1, sequence_length=2,
        codebooks=3, codebook_size=4,
    )
    ids = np.asarray([[0, 0, 0, 0], [1, 1, 1, 0], [2, 2, 2, 0]])
    model = build_tiger(ids, config)
    logits, targets = model(torch.tensor([[0, 1]]), torch.tensor([2]))
    assert logits.shape[:2] == targets.shape == (1, 4)
