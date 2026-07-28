from ..industrial_p0_2025 import reproduce_industrial_p0


def reproduce_drl_put(dataset_dir, seed=42):
    return reproduce_industrial_p0("drl_put", dataset_dir, seed)
