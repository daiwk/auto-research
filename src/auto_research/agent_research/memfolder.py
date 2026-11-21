"""RecordFolder's explicit-input grouping kernel, arXiv:2611.26427v1 §3.3.

CPU L1 mathematics only. Embeddings and already-grounded entity labels are
caller inputs; there is no LLM extractor/merger, ContextFolder, answer checker,
file access or model. The small-record cap prevents accidental large runs.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False
MAX_RECORDS = 512


def _positive_integer(value, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _normalized(embeddings: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    if len(embeddings) == 0 or len(embeddings) > MAX_RECORDS:
        raise ValueError(f"between one and {MAX_RECORDS} explicit records required")
    size = len(embeddings[0])
    if not size:
        raise ValueError("nonempty embedding vectors required")
    result = []
    for row in embeddings:
        if len(row) != size or any(isinstance(x, bool) or not isinstance(x, (int, float))
                                   or not math.isfinite(x) for x in row):
            raise ValueError("equal-sized finite numeric embedding vectors required")
        norm = math.hypot(*row)
        if not math.isfinite(norm) or norm == 0:
            raise ValueError("finite nonzero embedding norms required")
        result.append(tuple(x / norm for x in row))
    return tuple(result)


def _similarities(vectors):
    cosine = [[max(-1.0, min(1.0, math.fsum(x * y for x, y in zip(a, b, strict=True))))
               for b in vectors] for a in vectors]
    distances = [[max(0.0, 2.0 - 2.0 * c) for c in row] for row in cosine]
    return cosine, distances


def _separation(index: int, density, candidates, distances) -> float:
    higher = [j for j in candidates if density[j] > density[index]]
    return min(distances[index][j] for j in higher) if higher else max(
        distances[index][j] for j in candidates)


def progressive_anchors(embeddings: Sequence[Sequence[float]], count: int, *,
                        neighbors: int = 5) -> tuple[int, ...]:
    """DPC first anchor, then Eq.1 novelty-density peaks; ties use input order."""
    vectors = _normalized(embeddings)
    n = len(vectors)
    _positive_integer(count, "anchor count")
    _positive_integer(neighbors, "neighbor cap")
    if count > n:
        raise ValueError("anchor count must not exceed record count")
    if n == 1:
        return (0,)
    _, distances = _similarities(vectors)
    k = min(neighbors, n - 1)
    density = [math.exp(-math.fsum(sorted(distances[i][j] for j in range(n) if j != i)[:k]) / k)
               for i in range(n)]
    all_indices = list(range(n))
    anchors = [max(all_indices, key=lambda i: density[i] * _separation(i, density, all_indices, distances))]
    while len(anchors) < count:
        candidates = [i for i in range(n) if i not in anchors]
        k_prime = min(neighbors, len(anchors))
        novelty = {i: -math.expm1(-math.fsum(sorted(distances[i][a] for a in anchors)[:k_prime]) / k_prime)
                   for i in candidates}
        anchors.append(max(candidates, key=lambda i: novelty[i] * _separation(i, novelty, candidates, distances)))
    return tuple(anchors)


def entity_affinity(embeddings: Sequence[Sequence[float]], entity_sets: Sequence[Sequence[str]], *,
                    window: int = 50, variance_floor: float = 1e-6) -> tuple[list[list[float]], dict]:
    """IDF-weighted Jaccard/cosine blend; variances use all window pairs first."""
    vectors = _normalized(embeddings)
    _positive_integer(window, "predecessor window")
    if isinstance(variance_floor, bool) or not isinstance(variance_floor, (int, float)) or not math.isfinite(variance_floor) or variance_floor <= 0:
        raise ValueError("finite positive variance floor required")
    if len(entity_sets) != len(vectors):
        raise ValueError("one explicit grounded-entity set per record required")
    entities = []
    for row in entity_sets:
        if isinstance(row, str) or any(not isinstance(e, str) or not e.strip() for e in row):
            raise ValueError("nonempty entity labels required; labels are not extracted here")
        entities.append(frozenset(row))
    n = len(vectors)
    counts = Counter(e for row in entities for e in row)
    weights = {entity: math.log(n / count) for entity, count in counts.items()}
    cosine, _ = _similarities(vectors)
    shared = [[math.fsum(weights[e] for e in entities[i] & entities[j]) for j in range(n)] for i in range(n)]
    similarity = []
    for i in range(n):
        row = []
        for j in range(n):
            union = math.fsum(weights[e] for e in entities[i] | entities[j])
            row.append(shared[i][j] / union if union else 0.0)
        similarity.append(row)
    pairs = [(p, s) for s in range(n) for p in range(max(0, s - window), s)]

    def variance(values):
        if not values:
            return variance_floor
        average = math.fsum(values) / len(values)
        return max(variance_floor, math.fsum((x - average) ** 2 for x in values) / len(values))

    # Population variances are an explicit local convention; the paper says
    # variance over all pairs without a finite-sample ddof convention.
    sigma_e = variance([similarity[p][s] for p, s in pairs])
    sigma_c = variance([cosine[p][s] for p, s in pairs])
    affinity = []
    for i in range(n):
        row = []
        for j in range(n):
            alpha = shared[i][j] * sigma_c / (shared[i][j] * sigma_c + sigma_e)
            row.append(alpha * similarity[i][j] + (1 - alpha) * cosine[i][j])
        affinity.append(row)
    return affinity, {"entity_variance": sigma_e, "cosine_variance": sigma_c,
                      "variance_pairs": len(pairs), "variance_convention": "population_ddof0",
                      "common_entity_zero_weight": all(weights[e] == 0 for e, count in counts.items() if count == n)}


@dataclass(frozen=True)
class Partition:
    anchors: tuple[int, ...]
    initial: tuple[int, ...]
    assignments: tuple[int, ...]
    links: tuple[tuple[int, int, float], ...]
    groups: tuple[tuple[int, ...], ...]
    variance_pairs: int


def record_partition(embeddings: Sequence[Sequence[float]], entity_sets: Sequence[Sequence[str]], *,
                     keep_ratio: float = 0.5, neighbors: int = 5, window: int = 50,
                     max_links: int = 8, variance_floor: float = 1e-6) -> Partition:
    """Return exact explicit-input grouping, not synthesized memory text.

    Input order is chronological. Equal scores use the earliest input/anchor.
    Anchors are pinned to their own groups even for duplicate embeddings. The
    small kernel uses existing ``research-components`` SciPy for Hungarian
    matching; it never substitutes greedy matching for the paper's optimizer.
    """
    from scipy.optimize import linear_sum_assignment

    vectors = _normalized(embeddings)
    _positive_integer(max_links, "candidate-link cap")
    if isinstance(keep_ratio, bool) or not isinstance(keep_ratio, (int, float)) or not math.isfinite(keep_ratio) or not 0 < keep_ratio <= 1:
        raise ValueError("keep ratio must be in (0,1]")
    n = len(vectors)
    count = max(1, round(keep_ratio * n))
    anchors = progressive_anchors(vectors, count, neighbors=neighbors)
    cosine, _ = _similarities(vectors)
    affinity, metadata = entity_affinity(vectors, entity_sets, window=window, variance_floor=variance_floor)
    initial = tuple(i if i in anchors else max(anchors, key=lambda a: cosine[i][a]) for i in range(n))
    # Zero-valued dummy successors permit unmatched predecessors. Noncandidate
    # zero entries are ignored after matching; only strictly positive gains link.
    gains = [[0.0] * (2 * n) for _ in range(n)]
    for successor in range(n):
        if successor in anchors:
            continue
        candidates = [(p, affinity[p][successor] - cosine[successor][initial[successor]])
                      for p in range(max(0, successor - window), successor)]
        candidates = sorted((x for x in candidates if x[1] > 0), key=lambda x: (-x[1], x[0]))[:max_links]
        for predecessor, gain in candidates:
            gains[predecessor][successor] = gain
    rows, cols = linear_sum_assignment(gains, maximize=True)
    links = tuple((int(p), int(s), gains[p][s]) for p, s in zip(rows, cols, strict=True)
                  if s < n and gains[p][s] > 0)
    outgoing = {p: s for p, s, _ in links}
    incoming = {s for _, s, _ in links}
    assignments = list(initial)
    for root in range(n):
        if root in incoming or root not in outgoing:
            continue
        chain, node = [root], root
        while node in outgoing:
            node = outgoing[node]
            chain.append(node)
        chosen = root if root in anchors else max(anchors, key=lambda a: math.fsum(cosine[i][a] for i in chain))
        for i in chain:
            assignments[i] = chosen
    groups = tuple(tuple(i for i, assigned in enumerate(assignments) if assigned == a) for a in anchors)
    return Partition(anchors, initial, tuple(assignments), links, groups, metadata["variance_pairs"])


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU-only component; no CUDA path advertised")
    embeddings = [(1.0, .1), (.9, .2), (-1.0, .1), (-.9, .2), (.2, 1.0), (.1, .9)]
    entities = [{"shared", "a"}, {"shared", "a"}, {"shared", "b"}, {"shared", "b"}, {"shared", "c"}, {"shared", "c"}]
    partition = record_partition(embeddings, entities)
    cosine, _ = _similarities(_normalized(embeddings))
    no_entities, metadata = entity_affinity(embeddings, [set() for _ in embeddings])
    duplicate = record_partition([(1., 0.)] * 4, [set()] * 4, keep_ratio=.5)
    all_items = [i for group in partition.groups for i in group]
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"input_records": len(embeddings), "output_groups": len(partition.groups),
                        "matched_links": len(partition.links), "variance_pairs": partition.variance_pairs},
            "checks": {"all_records_once": sorted(all_items) == list(range(len(embeddings))),
                       "anchors_preserved": all(a in group for a, group in zip(partition.anchors, partition.groups, strict=True)),
                       "forward_links_only": all(p < s and s not in partition.anchors for p, s, _ in partition.links),
                       "nonbranching": len({p for p, _, _ in partition.links}) == len(partition.links) == len({s for _, s, _ in partition.links}),
                       "no_entities_reduces_to_cosine": all(math.isclose(no_entities[i][j], cosine[i][j]) for i in range(6) for j in range(6)),
                       "variances_before_filtering": metadata["variance_pairs"] == 15,
                       "duplicate_groups_nonempty": all(duplicate.groups),
                       "singleton_identity": record_partition([(1.,)], [set()]).groups == ((0,),)}}
