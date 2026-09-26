"""Small, reproducible offline LLM nomination and explanation audit."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .data import cf_candidates, load_lastfm
from .llm import LocalGenerator, MODEL_ID, REVISION
from .pipeline import annotate_baseline, generate_profile, serve


def reproduce(root: Path, seed: int = 42, *, split: str = "validation",
              users: int = 20, device: str = "cpu",
              model_path: str | None = None) -> dict:
    if split not in {"validation", "test"}:
        raise ValueError("select validation or test; never train")
    data = load_lastfm(root, seed=seed)
    holdout = getattr(data, split)
    eligible = sorted(user for user, history in data.train.items()
                      if len(history) >= 20 and holdout[user])
    if users < 1 or not eligible:
        raise ValueError("requested users must be positive and the dataset must contain eligible users")
    selected = np.random.default_rng(seed).choice(
        eligible, min(users, len(eligible)), replace=False)
    generator = LocalGenerator(device=device, max_new_tokens=256,
                               model_path=model_path)
    cache = {}
    generated_hits, served_hits, baseline_hits = [], [], []
    summaries = []
    accepted_total = 0
    rejected_total = 0
    annotated_slots = 0
    total_baseline_slots = 0
    for user in selected:
        key = int(user)
        profile, stats = generate_profile(data, key, generator,
                                          candidate_limit=10, output_limit=5)
        accepted_total += stats["accepted"]
        rejected_total += sum(stats["rejected"].values())
        cache[key] = profile
        targets = holdout[key]
        baseline = cf_candidates(data, key, limit=5)
        annotation_only = annotate_baseline(data, key, cache)
        assert [row.artist_id for row in annotation_only] == baseline
        generated_set = {row.artist_id for row in profile.nominations}
        annotated_slots += sum(row.artist_id in generated_set for row in annotation_only)
        total_baseline_slots += len(annotation_only)
        generated = [row.artist_id for row in profile.nominations]
        served = [row.artist_id for row in serve(data, key, cache)]
        baseline_hits.append(float(bool(set(baseline) & targets)))
        generated_hits.append(float(bool(set(generated) & targets)))
        served_hits.append(float(bool(set(served) & targets)))
        summaries.append({"user_id": key, "accepted": stats["accepted"],
                          "rejected": stats["rejected"],
                          "generated_hit_at_5": generated_hits[-1],
                          "cf_hit_at_5": baseline_hits[-1]})
    return {"paper": {"arxiv_id": "2609.23877", "url": "https://arxiv.org/abs/2609.23877"},
            "setup": {"dataset": "HetRec Last.fm 2K", "seed": seed,
                      "split": f"per-user seeded random 80/10/10; scoring {split}",
                      "users": len(selected), "artists": len(data.artists),
                      "interactions": data.total_interactions,
                      "model": MODEL_ID, "revision": REVISION, "device": device,
                      "candidate_limit": 10, "output_limit": 5},
            "results": {"cf_hit_at_5": float(np.mean(baseline_hits)),
                        "generated_hit_at_5": float(np.mean(generated_hits)),
                        "served_hit_at_5_with_fallback": float(np.mean(served_hits)),
                        "accepted_nominations": accepted_total,
                        "rejected_nominations": rejected_total,
                        "catalog_grounded_share": accepted_total / max(1, accepted_total + rejected_total),
                        "annotation_only_hit_at_5": float(np.mean(baseline_hits)),
                        "annotation_coverage_at_5": annotated_slots / max(1, total_baseline_slots),
                        "cache_coverage": float(np.mean([bool(cache[int(user)].nominations)
                                                         for user in selected]))},
            "per_user": summaries,
            "scope": "Public-data LLM nomination and catalog-grounded rationale diagnostic. "
                     "The public archive lacks YouTube Music online outcomes; rationale "
                     "effects on user trust and engagement cannot be measured offline."}
