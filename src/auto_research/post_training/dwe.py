"""DWE v1 sparse unbiased output-head gradients; small CPU mechanism only.

Implements paired positive/negative mass, a fixed principal-component order,
stratified shared quantiles and sparse chain-rule products (Eqs. 4--15).
It is not an LLM training backend or a claim of measured GPU speedup.
"""

from bisect import bisect_right
import math
import random

REQUIRES_GPU_VALIDATION = False


def _vector(values, name):
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError(f"{name}: nonempty real vector required")
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in values):
        raise ValueError(f"{name}: finite real entries required")
    return tuple(float(x) for x in values)


def _matrix(values):
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError("nonempty output-head matrix required")
    rows = tuple(_vector(row, "output row") for row in values)
    if len({len(row) for row in rows}) != 1:
        raise ValueError("rectangular output-head matrix required")
    return rows


def softmax(logits):
    z = _vector(logits, "logits")
    exps = tuple(math.exp(x - max(z)) for x in z)
    return tuple(x / math.fsum(exps) for x in exps)


def kl_logit_gradient(student_logits, teacher_logits, *, reverse=False):
    """Forward KL p-q; reverse KL p*(log(p/q)-KL), without underflow logs."""
    a, b = _vector(student_logits, "student"), _vector(teacher_logits, "teacher")
    if len(a) != len(b) or type(reverse) is not bool:
        raise ValueError("matched vocabulary and boolean reverse required")
    p, q = softmax(a), softmax(b)
    if not reverse:
        return tuple(x-y for x, y in zip(p, q, strict=True))
    logza = max(a)+math.log(math.fsum(math.exp(x-max(a)) for x in a))
    logzb = max(b)+math.log(math.fsum(math.exp(x-max(b)) for x in b))
    ratios = tuple((x-logza)-(y-logzb) for x, y in zip(a, b, strict=True))
    loss = math.fsum(x*y for x, y in zip(p, ratios, strict=True))
    return _vector(tuple(x*(r-loss) for x, r in zip(p, ratios, strict=True)), "reverse-KL gradient")


def principal_order(weight, *, iterations=128):
    """Cache a centered leading-PC order; exact dense CPU power iteration.

    Multiple coordinate starts avoid an initialization orthogonal to the leading
    eigenspace. Unlike upstream's randomized PCA this is for tiny matrices only.
    Stable index ties and a positive largest component fix sign ambiguity.
    """
    rows = _matrix(weight)
    if type(iterations) is not int or iterations < 1:
        raise ValueError("positive integer iterations required")
    n, d = len(rows), len(rows[0])
    mean = tuple(math.fsum(row[j] for row in rows)/n for j in range(d))
    centered = tuple(tuple(x-y for x, y in zip(row, mean, strict=True)) for row in rows)

    def multiply(v):
        scores = tuple(math.fsum(x*y for x, y in zip(row, v, strict=True)) for row in centered)
        return _vector(tuple(math.fsum(row[j]*score for row, score in zip(centered, scores, strict=True))
                             for j in range(d)), "PCA covariance product")

    candidates = []
    for axis in range(d):
        v = tuple(float(j == axis) for j in range(d))
        for _ in range(iterations):
            nxt = multiply(v)
            norm = math.hypot(*nxt)
            if norm == 0:
                break
            v = tuple(x/norm for x in nxt)
        score = math.fsum(x*y for x, y in zip(v, multiply(v), strict=True))
        candidates.append((score, v))
    _, direction = max(candidates, key=lambda item: item[0])
    largest = max(range(d), key=lambda j: abs(direction[j]))
    sign = -1 if direction[largest] < 0 else 1
    scores = [sign*math.fsum(x*y for x, y in zip(row, direction, strict=True)) for row in centered]
    return tuple(sorted(range(n), key=lambda i: (scores[i], i)))


def _distributions(gradient, order):
    g = _vector(gradient, "gradient")
    if (not isinstance(order, (list, tuple)) or len(order) != len(g)
            or any(type(i) is not int for i in order) or sorted(order) != list(range(len(g)))):
        raise ValueError("order must be a vocabulary permutation")
    pos, neg = math.fsum(max(x, 0) for x in g), math.fsum(max(-x, 0) for x in g)
    if not math.isclose(pos, neg, rel_tol=1e-12, abs_tol=1e-14):
        raise ValueError("DWE requires a zero-sum logit gradient")
    if pos == neg == 0:
        return g, 0., (), ()
    if pos == 0 or neg == 0:
        raise ValueError("both gradient signs required")
    positive, negative, a, b = [], [], 0., 0.
    for index in order:
        a += max(g[index], 0)/pos
        b += max(-g[index], 0)/neg
        positive.append(a)
        negative.append(b)
    positive[-1] = negative[-1] = 1.
    return g, (pos+neg)/2, tuple(positive), tuple(negative)


def paired_gradient(gradient, order, pairs, *, rng, stratified=True):
    """Eqs. 9--12; returns only selected (index, coefficient) entries."""
    g, mass, positive, negative = _distributions(gradient, order)
    if (type(pairs) is not int or pairs < 1 or not isinstance(rng, random.Random)
            or type(stratified) is not bool):
        raise ValueError("positive pairs, Random instance and boolean stratified required")
    if mass == 0:
        return ()
    sparse = {}
    for k in range(pairs):
        draw = rng.random()
        if not 0 <= draw < 1 or not math.isfinite(draw):
            raise ValueError("random quantile must be in [0,1)")
        u = min((k+draw)/pairs, math.nextafter(1., 0.)) if stratified else draw
        i, j = order[bisect_right(positive, u)], order[bisect_right(negative, u)]
        sparse[i] = sparse.get(i, 0.) + mass/pairs
        sparse[j] = sparse.get(j, 0.) - mass/pairs
    return tuple(sorted((i, value) for i, value in sparse.items() if value != 0))


def exact_quantile_expectation(gradient, order):
    """Integrate every shared-quantile interval: no Monte Carlo assertion."""
    g, mass, positive, negative = _distributions(gradient, order)
    result = [0.]*len(g)
    if mass == 0:
        return tuple(result)
    boundaries = sorted(set((0., 1.)+positive+negative))
    for lo, hi in zip(boundaries, boundaries[1:]):
        u = (lo+hi)/2
        i, j = order[bisect_right(positive, u)], order[bisect_right(negative, u)]
        result[i] += mass*(hi-lo)
        result[j] -= mass*(hi-lo)
    return tuple(result)


def sparse_backward(weight, hidden, sparse):
    """Eq.14: gather selected rows and return sparse output-weight gradients."""
    rows, h = _matrix(weight), _vector(hidden, "hidden")
    if len(h) != len(rows[0]) or not isinstance(sparse, (tuple, list)):
        raise ValueError("matched hidden width and sparse entries required")
    entries, seen = [], set()
    for entry in sparse:
        if not isinstance(entry, (tuple, list)) or len(entry) != 2:
            raise ValueError("(index, coefficient) entries required")
        index, coefficient = entry
        if type(index) is not int or not 0 <= index < len(rows) or index in seen:
            raise ValueError("unique valid row index required")
        value = _vector((coefficient,), "coefficient")[0]
        seen.add(index)
        entries.append((index, value))
    dh = tuple(math.fsum(value*rows[i][j] for i, value in entries) for j in range(len(h)))
    dw = tuple((i, tuple(value*x for x in h)) for i, value in entries)
    return dh, dw


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only device required")
    rng = random.Random(seed)
    weight = tuple((float(i-3), (i-3)*.2, rng.uniform(-.1, .1)) for i in range(8))
    order = principal_order(weight)
    g = kl_logit_gradient(tuple(rng.uniform(-1, 1) for _ in range(8)), tuple(rng.uniform(-1, 1) for _ in range(8)))
    expectation = exact_quantile_expectation(g, order)
    error = max(abs(a-b) for a, b in zip(g, expectation, strict=True))
    h = (.2, -.7, .9)
    actual_dh, _ = sparse_backward(weight, h, tuple(enumerate(expectation)))
    expected_dh = tuple(math.fsum(row[j]*value for row, value in zip(weight, g, strict=True)) for j in range(3))
    sparse = paired_gradient(g, order, 2, rng=rng)
    mass_error = abs(math.fsum(value for _, value in sparse))
    # A discarded-coordinate control is biased, unlike the exact expectation.
    top = sorted(range(8), key=lambda i: abs(g[i]), reverse=True)[:4]
    biased_error = max(abs(g[i]) if i not in top else 0. for i in range(8))
    checks = {"exact_quantile_integral_is_unbiased": error < 1e-12,
              "expected_sparse_chain_rule_matches_dense": max(abs(a-b) for a, b in zip(actual_dh, expected_dh, strict=True)) < 1e-12,
              "sample_preserves_zero_sum": mass_error < 1e-12,
              "sample_uses_at_most_two_rows_per_pair": len(sparse) <= 4,
              "top_coordinate_discard_is_biased_control": biased_error > 0,
              "zero_gradient_has_no_sparse_rows": paired_gradient((0.,)*8, order, 2, rng=rng) == ()}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "controls": checks, "metrics": {"exact_expectation_max_abs_error": error,
            "paired_zero_sum_abs_error": mass_error, "top4_discard_max_abs_bias": biased_error,
            "selected_rows": len(sparse), "vocabulary": 8, "hidden_width": 3, "pairs": 2}}
