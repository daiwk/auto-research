import pytest


def test_mba_starts_as_exact_zero():
    torch = pytest.importorskip("torch")
    import numpy as np
    from auto_research.reproductions.saviorrec.model import SaviorConfig, build_ranker

    config = SaviorConfig(dimensions=8, codebooks=2, codebook_size=4)
    model = build_ranker(5, np.ones((5, 8), dtype=np.float32), np.zeros((5, 2), dtype=np.int64), config, True)
    assert all(torch.count_nonzero(table) == 0 for table in model.mba)
