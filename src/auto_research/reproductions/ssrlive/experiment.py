from pathlib import Path

from ..historical_p0_h04 import reproduce_h04


def reproduce_ssrlive(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h04("ssrlive", dataset_dir, seed)
