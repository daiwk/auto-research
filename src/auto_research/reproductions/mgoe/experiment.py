from ..industrial_p0_2025 import reproduce_industrial_p0


def reproduce_mgoe(dataset_dir, seed=42):
    return reproduce_industrial_p0("mgoe", dataset_dir, seed)
