from pathlib import Path

from ...multimodal.papers import reproduce_siglip2


def reproduce(dataset_dir: Path, seed: int = 42):
    return reproduce_siglip2(dataset_dir, seed)
