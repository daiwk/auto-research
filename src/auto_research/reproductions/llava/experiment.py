from pathlib import Path
from ..foundation_p1 import reproduce_llava
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_llava(dataset_dir, seed)
