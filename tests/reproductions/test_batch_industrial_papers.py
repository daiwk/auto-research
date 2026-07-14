import numpy as np
import pytest

from auto_research.reproductions.industrial_batch import CompactSequences
from auto_research.reproductions.registry import get_adapter


PAPERS = (
    "seral", "leadre", "cobra", "argus", "gr4ad", "cross-domain-kd", "mm-llm"
)


def fixture_data():
    return CompactSequences(
        train=((0, 1, 2, 3), (1, 2, 4, 5)),
        validation=(4, 6),
        test=(5, 7),
        features=np.asarray([
            [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 1],
            [0, 0, 1], [1, 0, 1], [1, 1, 0], [0, 1, 1],
        ], dtype=np.float32),
        popularity=np.arange(1, 9, dtype=np.float32),
    )


def test_all_batch_papers_have_quantified_online_ab():
    for key in PAPERS:
        assert get_adapter(key).paper.has_online_ab


def test_sparse_dense_and_lazy_models_score_the_full_catalog():
    torch = pytest.importorskip("torch")
    data = fixture_data()
    histories = torch.tensor([[0, 1, 2], [1, 2, 4]])

    from auto_research.reproductions.cobra.model import build_model as cobra_model
    from auto_research.reproductions.gr4ad.model import build_lazy

    codes = np.column_stack((np.arange(8) % 8, np.arange(8) // 2 % 8))
    assert cobra_model(data, codes, True).score(histories).shape == (2, 8)
    ua_codes = np.column_stack((codes, np.arange(8) % 8, np.arange(8) % 16))
    assert build_lazy(data, ua_codes)(histories).shape == (2, 8)


def test_profile_and_feedback_models_execute_their_auxiliary_heads():
    torch = pytest.importorskip("torch")
    data = fixture_data()
    histories = torch.tensor([[0, 1, 2], [1, 2, 4]])

    from auto_research.reproductions.argus.model import build_model as argus_model
    from auto_research.reproductions.seral.model import build_model as seral_model

    item_logits, feedback = argus_model(data, True)(histories)
    assert item_logits.shape == (2, 8)
    assert feedback.shape == (2, 3)
    assert seral_model(data)(histories).shape == (2, 8)


def test_shared_din_initialization_is_reproducible():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.din.model import DINConfig, train_model

    config = DINConfig(dimensions=8, sequence_length=3, batch_size=2, steps=1)
    first, _ = train_model("din", fixture_data(), config, seed=42)
    torch.rand(100)
    second, _ = train_model("din", fixture_data(), config, seed=42)
    for left, right in zip(first.parameters(), second.parameters()):
        assert torch.equal(left.detach().cpu(), right.detach().cpu())
