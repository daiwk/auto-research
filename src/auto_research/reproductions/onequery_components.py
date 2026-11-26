"""OneQuery Eq5-13 arithmetic, not a query model or a GRPO trainer.

References belong only to this reward/evaluator boundary. QT uses an explicit
typed tuple list, not an invented parser for the authors' private tag grammar.
"""
from __future__ import annotations

import json
import math
import random
import unicodedata
from collections.abc import Mapping, Sequence

REQUIRES_GPU_VALIDATION = False
FIELDS = ("lang", "spell", "trans", "qt")
DEFAULT_WEIGHTS = (0.35, 0.25, 0.25, 0.15)


def normalize(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text fields must be strings")
    return " ".join(unicodedata.normalize("NFKC", text).lower().split())


def edit_similarity(left: str, right: str) -> float:
    a, b = normalize(left), normalize(right)
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        nxt = [i]
        for j, cb in enumerate(b, 1):
            nxt.append(min(nxt[-1] + 1, row[j] + 1, row[j-1] + (ca != cb)))
        row = nxt
    # Both-empty is the explicit local extension of Eq11's zero denominator.
    return 1.0 if not a and not b else 1.0 - row[-1] / max(len(a), len(b))


def tuple_set(value: Sequence[tuple[str, str]]) -> frozenset[tuple[str, str]]:
    if isinstance(value, (str, bytes, Mapping)) or not isinstance(value, Sequence):
        raise TypeError("QT must be an explicit sequence of (type, text) pairs")
    out = []
    for pair in value:
        if isinstance(pair, (str, bytes)) or not isinstance(pair, Sequence) or len(pair) != 2:
            raise ValueError("each QT entry must contain type and text")
        out.append((normalize(pair[0]), normalize(pair[1])))
    return frozenset(out)


def reward(query: str, prediction: Mapping, reference: Mapping,
           weights: Sequence[float] = DEFAULT_WEIGHTS) -> dict[str, float]:
    if set(prediction) != set(FIELDS) or set(reference) != set(FIELDS):
        raise ValueError("the typed schema requires exactly four fields")
    if len(weights) != 4 or any(not math.isfinite(w) or w < 0 for w in weights) or sum(weights) <= 0:
        raise ValueError("four finite nonnegative weights with positive sum required")
    x, target, predicted = normalize(query), normalize(reference["spell"]), normalize(prediction["spell"])
    correction_needed = x != target
    spelling = (1.0 if predicted == target else 0.3 * edit_similarity(predicted, target)) if correction_needed else float(predicted == x)
    parts = {
        "lang": float(normalize(prediction["lang"]) == normalize(reference["lang"])),
        "spell": spelling,
        "trans": float(normalize(prediction["trans"]) == normalize(reference["trans"])),
        "qt": float(tuple_set(prediction["qt"]) == tuple_set(reference["qt"])),
    }
    # Eq7 is a weighted sum, not an automatic re-normalization of user weights.
    return parts | {"total": sum(w * parts[k] for w, k in zip(weights, FIELDS))}


def group_advantages(rewards: Sequence[float], delta: float = 1e-8) -> tuple[float, ...]:
    if len(rewards) < 2 or not math.isfinite(delta) or delta <= 0 or any(not math.isfinite(r) for r in rewards):
        raise ValueError("finite group of at least two rewards and positive delta required")
    mean = sum(rewards) / len(rewards)
    # Population standard deviation and delta are declared local conventions.
    std = math.sqrt(sum((r-mean)**2 for r in rewards) / len(rewards))
    return tuple((r-mean)/(std+delta) for r in rewards)


def clipped_objective(ratios: Sequence[float], advantages: Sequence[float], epsilon: float = .2) -> float:
    if len(ratios) != len(advantages) or not ratios or not 0 < epsilon < 1:
        raise ValueError("aligned nonempty sequences and epsilon in (0,1) required")
    if any(not math.isfinite(r) or r <= 0 for r in ratios) or any(not math.isfinite(a) for a in advantages):
        raise ValueError("finite positive ratios and finite advantages required")
    return sum(min(r*a, min(1+epsilon, max(1-epsilon, r))*a) for r, a in zip(ratios, advantages))/len(ratios)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("OneQuery arithmetic diagnostic is CPU-only")
    rng = random.Random(seed)
    reference = {"lang": "de", "spell": "adidas schuhe", "trans": "adidas shoes", "qt": [("brand", "adidas"), ("product", "shoes")]}
    exact = reward("addidas schuhe", reference, reference)
    partial = reward("addidas schuhe", reference | {"spell": "addidas schuhe"}, reference)
    dropped = reward("addidas schuhe", reference | {"qt": [("brand", "adidas")]}, reference)
    unchanged = reference | {"spell": "adidas schuhe"}
    overcorrected = reward("adidas schuhe", unchanged | {"spell": "adidas shoe"}, unchanged)
    normalized = reference | {"lang": " ＤＥ  ", "trans": " ADIDAS   SHOES ", "qt": list(reversed(reference["qt"]))}
    adv = group_advantages([rng.random() for _ in range(8)])
    value = clipped_objective([1.5, .5], [1.0, -1.0])
    checks = {"exact_all_fields": exact["total"] == 1.0,
              "partial_spelling_is_capped": 0 < partial["spell"] <= .3,
              "qt_requires_whole_set": dropped["qt"] == 0,
              "unneeded_correction_rejected": overcorrected["spell"] == 0,
              "normalization_and_set_order": reward("addidas schuhe", normalized, reference)["total"] == 1,
              "advantages_centered": abs(sum(adv)) < 1e-10,
              "constant_group_zero": group_advantages([1., 1.]) == (0., 0.),
              "signed_ratio_clipping": abs(value - .2) < 1e-12}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"exact_reward": exact["total"], "partial_spelling_reward": partial["spell"],
             "missing_qt_reward": dropped["total"], "advantage_mean": sum(adv)/len(adv), "clipped_objective": value}}


if __name__ == "__main__":
    print(json.dumps(diagnostic(), ensure_ascii=False, allow_nan=False))
