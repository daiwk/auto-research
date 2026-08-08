from pathlib import Path
from ..foundation_p1 import reproduce_awq
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_awq(dataset_dir, seed)
