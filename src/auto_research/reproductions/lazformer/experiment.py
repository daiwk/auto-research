from auto_research.reproductions.mechanisms.gese_candidate_scores import reproduce


def run(dataset_dir, seed=42):
    return reproduce("lazformer", dataset_dir, seed)
