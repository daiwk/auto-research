from pathlib import Path
from ..foundation_p1 import reproduce_medusa
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_medusa(dataset_dir, seed)
