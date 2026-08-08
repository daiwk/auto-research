from pathlib import Path
from ..foundation_p1 import reproduce_speculative_decoding
def reproduce(dataset_dir: Path, seed: int = 42): return reproduce_speculative_decoding(dataset_dir, seed)
