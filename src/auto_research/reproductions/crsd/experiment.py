from pathlib import Path
from ..industrial_gap_p1 import reproduce_crsd
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_crsd(dataset_dir, seed)
