from pathlib import Path

from ..historical_p0_h06_h07 import reproduce_h06_h07


def reproduce_harmonrank(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h06_h07("harmonrank", dataset_dir, seed)
