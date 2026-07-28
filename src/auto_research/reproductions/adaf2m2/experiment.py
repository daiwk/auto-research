from ..industrial_p0_2025 import reproduce_industrial_p0


def reproduce_adaf2m2(dataset_dir, seed=42):
    return reproduce_industrial_p0("adaf2m2", dataset_dir, seed)
