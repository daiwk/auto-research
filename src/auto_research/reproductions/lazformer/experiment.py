from auto_research.reproductions.latest_20260916 import reproduce


def run(dataset_dir, seed=42):
    return reproduce("lazformer", dataset_dir, seed)
