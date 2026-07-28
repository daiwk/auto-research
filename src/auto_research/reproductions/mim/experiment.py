from ..industrial_p0_2025 import reproduce_industrial_p0


def reproduce_mim(dataset_dir, seed=42):
    return reproduce_industrial_p0("mim", dataset_dir, seed)
