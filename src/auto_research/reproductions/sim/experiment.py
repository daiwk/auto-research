from pathlib import Path
from ..industrial_gap_p1 import reproduce_sim
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_sim(dataset_dir, seed)
