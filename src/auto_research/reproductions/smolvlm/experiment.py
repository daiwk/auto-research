from pathlib import Path

from ...multimodal.papers import reproduce_smolvlm


def reproduce(dataset_dir: Path, seed: int = 42):
    return reproduce_smolvlm(dataset_dir, seed)
