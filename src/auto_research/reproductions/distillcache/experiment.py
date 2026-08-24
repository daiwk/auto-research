from pathlib import Path

from ..historical_b07 import reproduce as _reproduce


def reproduce(dataset_dir: Path, seed: int = 42):
    return _reproduce('distillcache', dataset_dir, seed)
