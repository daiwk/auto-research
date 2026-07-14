import numpy as np
import pytest

from auto_research.reproductions.pinfm.model import PinFMConfig, build_model as build_pinfm
from auto_research.reproductions.transact_v2.model import (
    TransActV2Config,
    build_model as build_transact_v2,
)
from auto_research.reproductions.rec_utils import batched_ranking_metrics, ranking_metrics


def test_transact_v2_selects_fixed_candidate_conditioned_sequence():
    torch = pytest.importorskip("torch")
    config = TransActV2Config(
        dimensions=8, heads=2, layers=1, lifelong_length=8,
        realtime_length=4, recent_length=2, nearest_lifelong=2,
        nearest_realtime=2,
    )
    features = np.eye(10, dtype=np.float32)
    model = build_transact_v2("transact_v2", 10, features, config)
    history = torch.tensor([[0, 1, 2, 3, 4, 5, 6, 7]])
    selected = model.select(history, torch.tensor([7]))
    assert selected.shape == (1, config.selected_length)
    assert selected[0, -2:].tolist() == [6, 7]


def test_transact_v2_scores_each_candidate():
    torch = pytest.importorskip("torch")
    config = TransActV2Config(
        dimensions=8, heads=2, layers=1, lifelong_length=8,
        realtime_length=4, recent_length=2, nearest_lifelong=2,
        nearest_realtime=2,
    )
    model = build_transact_v2("transact_v2", 10, np.eye(10, dtype=np.float32), config)
    histories = torch.tensor([[0, 1, 2, 3, 4, 5, 6, 7]]).expand(3, -1)
    assert model(histories, torch.tensor([7, 8, 9])).shape == (3,)


def test_pinfm_dcat_reuses_context_for_candidate_batch():
    torch = pytest.importorskip("torch")
    config = PinFMConfig(dimensions=8, heads=2, layers=1, sequence_length=4)
    model = build_pinfm(7, np.eye(7, dtype=np.float32), config)
    histories = torch.tensor([[0, 1, 2, 3]])
    candidates = torch.tensor([[4, 5, 6]])
    assert model.score(histories, candidates).shape == (1, 3)


def test_pinfm_exposes_all_three_pretraining_losses():
    torch = pytest.importorskip("torch")
    config = PinFMConfig(
        dimensions=8, heads=2, layers=1, sequence_length=6, future_window=2
    )
    model = build_pinfm(8, np.eye(8, dtype=np.float32), config)
    items = torch.tensor([[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]])
    valid = torch.ones_like(items, dtype=torch.bool)
    losses = model.sequence_losses(items, valid)
    assert len(losses) == 3
    assert all(loss.ndim == 0 for loss in losses)


def test_batched_metrics_match_single_history_metrics():
    from auto_research.reproductions.rec_utils import MovieLensSequences

    data = MovieLensSequences(
        train=((0, 1), (1, 2)), validation=(2, 3), test=(3, 0), item_count=4,
        item_features=np.eye(4), popularity=np.asarray([1.0, 2.0, 3.0, 4.0]),
    )
    scorer = lambda history: np.asarray([0.1, 0.2, 0.3, 0.4])
    single = ranking_metrics(data, scorer, top_k=2)
    batched = batched_ranking_metrics(
        data, lambda histories: np.stack([scorer(history) for history in histories]),
        batch_size=2, top_k=2,
    )
    assert batched == single
