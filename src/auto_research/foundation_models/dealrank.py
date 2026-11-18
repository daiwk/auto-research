"""DealRank v1 §2.1: parallel callback schedules, not an LLM ranker."""

from concurrent.futures import ThreadPoolExecutor
import math

REQUIRES_GPU_VALIDATION = False


def split_candidates(candidates: list[str], hands: int, *, dealt: bool = True) -> list[list[str]]:
    if (
        len(candidates) != len(set(candidates))
        or type(hands) is not int
        or not 1 <= hands <= len(candidates)
    ):
        raise ValueError("unique candidates and valid positive hand count required")
    if dealt:
        return [candidates[i::hands] for i in range(hands)]
    width = math.ceil(len(candidates) / hands)
    return [
        candidates[i * width : (i + 1) * width]
        for i in range(hands)
        if candidates[i * width : (i + 1) * width]
    ]


def quota_cuts(groups: list[list[str]], true_top: set[str], quota: int) -> int:
    """Evaluator-only consistent-ranker diagnostic; never passed to schedule/ranker."""
    if type(quota) is not int or quota < 1:
        raise ValueError("positive quota required")
    return sum(max(0, len(set(group) & true_top) - quota) for group in groups)


def schedule(candidates: list[str], ranker, *, workers: int = 5) -> dict:
    """Execute supplied ranker in actual concurrent rounds and validate every permutation.

    Exact paper schedules: up to100 -> 5x20 keep4;500 ->25x20 keep3,
    then4x20 keep5;1000 ->50x20 keep2,then5x20 keep4. Other large
    sizes are rejected rather than silently inventing a new schedule.
    """
    n = len(candidates)
    if not n or len(set(candidates)) != n or type(workers) is not int or not 1 <= workers <= 16:
        raise ValueError("nonempty unique IDs and bounded worker count required")
    if n > 100 and n not in (500, 1000):
        raise ValueError("only paper-defined large schedules500/1000 are supported")
    order = {item: i for i, item in enumerate(candidates)}
    current = candidates[:]
    eliminated = []
    trace = []

    def checked(group):
        result = list(ranker(tuple(group)))
        if len(result) != len(group) or set(result) != set(group):
            raise ValueError("ranker must return exactly the same candidate IDs once each")
        return result

    stages = (
        [(25, 3), (4, 5)]
        if n == 500
        else [(50, 2), (5, 4)]
        if n == 1000
        else [(math.ceil(n / 20), 4)]
        if n > 20
        else []
    )
    for hands, quota in stages:
        current.sort(key=order.__getitem__)
        groups = split_candidates(current, hands)
        if max(map(len, groups)) > 20:
            raise ValueError("ranker window exceeded paper budget")
        with ThreadPoolExecutor(max_workers=workers) as pool:
            ranked = list(pool.map(checked, groups))
        retained = [
            (rank, order[item], item) for group in ranked for rank, item in enumerate(group[:quota])
        ]
        cut = [
            (rank, order[item], item)
            for group in ranked
            for rank, item in enumerate(group[quota:], start=quota)
        ]
        current = [item for _, _, item in sorted(retained)]
        eliminated.insert(0, [item for _, _, item in sorted(cut)])
        trace.append(
            {
                "calls": len(groups),
                "input_count": sum(map(len, groups)),
                "survivors": len(current),
                "quota": quota,
            }
        )
    if len(current) > 20:
        raise ValueError("final window exceeded20")
    if n > 100:
        # The hierarchical schedule's final call uses retriever order (§2.1),
        # unlike N=100's place-in-hand then retriever-order presentation.
        current.sort(key=order.__getitem__)
    final = checked(current)
    trace.append(
        {"calls": 1, "input_count": len(current), "survivors": len(current), "quota": len(current)}
    )
    return {
        "ranking": final + [item for layer in eliminated for item in layer],
        "rounds": trace,
        "calls": sum(row["calls"] for row in trace),
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int:
        raise ValueError("integer seed required")
    if device != "cpu":
        raise ValueError("CPU callback schedule only")
    ids = [f"d{i}" for i in range(100)]
    rank = {item: i for i, item in enumerate(ids)}
    run = schedule(ids, lambda group: sorted(group, key=rank.__getitem__))
    true = set(ids[:10])
    dealt = quota_cuts(split_candidates(ids, 5), true, 4)
    chunk = quota_cuts(split_candidates(ids, 5, dealt=False), true, 4)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "paper_two_rounds": len(run["rounds"]) == 2,
            "six_calls": run["calls"] == 6,
            "quota4_exact_top4": run["ranking"][:4] == ids[:4],
            "no_candidate_lost_or_duplicated": set(run["ranking"]) == set(ids)
            and len(run["ranking"]) == 100,
            "dealing_avoids_prefix_cut": dealt == 0,
            "chunks_have_six_cuts": chunk == 6,
        },
        "metrics": {
            "schedule_calls": run["calls"],
            "dealt_top10_cuts": dealt,
            "contiguous_top10_cuts": chunk,
        },
    }
