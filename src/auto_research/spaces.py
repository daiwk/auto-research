from __future__ import annotations

import itertools
import random
from typing import Any, Iterator


DEFAULT_SPACES: dict[str, dict[str, list[Any]]] = {
    "llm": {
        "order": [2, 3, 4, 5],
        "alpha": [0.01, 0.1, 0.5, 1.0],
        "train_chars": [20000, 50000, 100000],
    },
    "recommendation": {
        "factors": [8, 16, 32],
        "learning_rate": [0.005, 0.01, 0.03],
        "regularization": [0.01, 0.05, 0.1],
        "epochs": [4, 8, 12],
    },
}


def candidate_params(
    space: dict[str, list[Any]], max_trials: int, seed: int
) -> Iterator[dict[str, Any]]:
    if not space:
        yield {}
        return
    keys = sorted(space)
    values = [space[key] for key in keys]
    combinations = list(itertools.product(*values))
    random.Random(seed).shuffle(combinations)
    for combination in combinations[:max_trials]:
        # ``combination`` is produced from exactly one value list per key, so
        # lengths are guaranteed equal. Avoid ``strict=True`` to keep the CLI
        # usable on the project's still-supported Python 3.9 environments.
        yield dict(zip(keys, combination))
