from ..industrial_p0_2025 import reproduce_industrial_p0


def reproduce_fuxi_alpha(dataset_dir, seed=42):
    return reproduce_industrial_p0("fuxi_alpha", dataset_dir, seed)
