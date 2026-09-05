from pathlib import Path

from ..historical_p0_h06_h07 import reproduce_h06_h07


def reproduce_rq_gmm(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h06_h07("rq_gmm", dataset_dir, seed)
