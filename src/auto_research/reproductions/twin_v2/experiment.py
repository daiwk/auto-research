from pathlib import Path
from ..industrial_gap_p1 import reproduce_twin_v2
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_twin_v2(dataset_dir, seed)
