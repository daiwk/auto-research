from pathlib import Path

from ..historical_b04_b06 import reproduce as _reproduce
from .model import Model


def reproduce(dataset_dir: Path, seed: int = 42):
    return _reproduce('ltv-video-ranking', dataset_dir, seed, Model)
