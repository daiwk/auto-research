import numpy as np
import pytest

from auto_research.reproductions.akt_rec.data import AKTData, CTRRow
from auto_research.reproductions.industrial_batch import CompactSequences


def sequence_fixture():
    return CompactSequences(
        train=((0, 1, 2, 3, 4), (1, 2, 4, 5, 6)),
        validation=(5, 7),
        test=(6, 0),
        features=np.eye(8, dtype=np.float32),
        popularity=np.ones(8, dtype=np.float32),
    )


def ctr_fixture():
    rows = tuple(
        CTRRow(index % 2, (0, 1, 2), 3 + index % 2, float(index % 2))
        for index in range(20)
    )
    return AKTData(
        train=rows,
        validation=rows[:4],
        test=rows[4:8],
        sequences=((0, 1, 2, 3), (1, 2, 4, 5)),
        titles=tuple(str(index) for index in range(8)),
        genres=tuple(("genre",) for _ in range(8)),
        item_activity=np.arange(1, 9, dtype=np.float32),
        user_activity=np.asarray([4, 4], dtype=np.float32),
    )


def test_nontp_executes_all_three_losses_and_keeps_inference_shape():
    pytest.importorskip("torch")
    from auto_research.reproductions.nontp.model import (
        NONTPConfig,
        score_all,
        train_model,
    )

    data = sequence_fixture()
    config = NONTPConfig(
        dimensions=8,
        heads=2,
        layers=1,
        sequence_length=4,
        batch_size=2,
        steps=1,
        future_steps=2,
    )
    model, metrics = train_model("nontp", data, np.arange(8) % 3, config, 42)
    assert metrics["loss_components"]["ntp"] > 0
    assert metrics["loss_components"]["tcl"] > 0
    assert metrics["loss_components"]["tdl"] > 0
    assert score_all(model, (0, 1, 2), config).shape == (8,)


def test_akt_rec_executes_gates_transfer_and_orthogonality():
    pytest.importorskip("torch")
    from auto_research.reproductions.akt_rec.model import AKTConfig, train_model

    data = ctr_fixture()
    item_codes = np.column_stack(
        (np.arange(8) % 2, np.arange(8) % 4, np.arange(8) % 8)
    )
    user_codes = np.asarray([[0, 0], [1, 1]])
    config = AKTConfig(dimensions=8, sequence_length=3, batch_size=8, steps=1)
    _, metrics = train_model("akt_rec", data, item_codes, user_codes, config, 42)
    assert metrics["loss_components"]["main"] > 0
    assert metrics["loss_components"]["asymmetric_transfer"] > 0
    assert metrics["loss_components"]["orthogonal"] > 0
