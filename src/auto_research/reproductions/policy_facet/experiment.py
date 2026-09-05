from pathlib import Path

from ..historical_p0_h04 import reproduce_h04


def reproduce_policy_facet(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h04("policy_facet", dataset_dir, seed)
