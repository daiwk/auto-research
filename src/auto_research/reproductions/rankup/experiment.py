from pathlib import Path

from ..historical_p0_h05 import reproduce_h05


def reproduce_rankup(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h05("rankup", dataset_dir, seed)
