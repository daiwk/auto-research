from pathlib import Path

from ..historical_b01_b03 import reproduce as _reproduce
from .model import Model


def reproduce(dataset_dir: Path, seed: int = 42):
    return _reproduce('feedback-policy', dataset_dir, seed, Model)
