from pathlib import Path

from ..historical_p0_h06_h07 import reproduce_h06_h07


def reproduce_airbnb_ebr(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h06_h07("airbnb_ebr", dataset_dir, seed)
