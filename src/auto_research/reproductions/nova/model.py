from __future__ import annotations

import numpy as np

from ..industrial_2026 import evaluate


def verified_candidate_search(data, candidates):
    """Four-level verification cascade over executable ranking candidates."""
    records, accepted = [], []
    for name, scorer in candidates:
        gates = {"schema": False, "execution": False, "finite": False, "offline": False}
        try:
            probe = np.asarray(scorer(data.sequences.train[0]))
            gates["schema"] = probe.shape == (data.item_count,)
            gates["execution"] = True
            gates["finite"] = bool(np.isfinite(probe).all())
            metrics = evaluate(data, scorer, target_split="validation")
            gates["offline"] = metrics["ndcg_at_10"] >= 0.0
            if all(gates.values()):
                accepted.append((name, scorer, metrics))
        except Exception as exc:
            records.append({"candidate": name, "gates": gates, "error": str(exc)})
            continue
        records.append({"candidate": name, "gates": gates, "validation": metrics})
    if not accepted:
        raise RuntimeError("NOVA verification cascade rejected every candidate")
    winner = max(accepted, key=lambda value: value[2]["ndcg_at_10"] + 0.25 * value[2]["hit_at_10"])
    return winner[1], {
        "verification_cascade": records,
        "selected_candidate": winner[0],
        "accepted_candidates": len(accepted),
    }
