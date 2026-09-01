from pathlib import Path

from ..historical_p0_h03 import reproduce_h03

def reproduce_onerank(dataset_dir: Path, seed: int = 42) -> dict:
    return reproduce_h03("onerank", dataset_dir, seed)
