from pathlib import Path

from ..historical_p0_h04 import reproduce_h04


def reproduce_causal_representation(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h04("causal_representation", dataset_dir, seed)
