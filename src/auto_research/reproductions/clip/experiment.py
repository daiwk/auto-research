from pathlib import Path
from ..foundation_p1 import reproduce_clip
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_clip(dataset_dir, seed)
