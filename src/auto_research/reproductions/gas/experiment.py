from pathlib import Path

from ...multimodal.papers import reproduce_gas


def reproduce(dataset_dir: Path, seed: int = 42):
    return reproduce_gas(dataset_dir, seed)
