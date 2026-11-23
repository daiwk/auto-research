"""Lossless retokenization v1: exact tabular full-gradient diagnostic.

This implements Appendix E's prefix-softmax policies, not an LLM, a tokenizer
repair algorithm, or a sampled-logit-only surrogate pretending to be full PG.
"""

import itertools
import math
import random

REQUIRES_GPU_VALIDATION = False


def _real(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("finite real number required")
    return float(value)


def _softmax(values):
    shift = max(values)
    exps = [math.exp(x-shift) for x in values]
    return tuple(x/math.fsum(exps) for x in exps)


class PrefixPolicy:
    """One independent softmax row per token prefix, initialized by chain rule."""

    def __init__(self, string_probabilities, block_size):
        if not isinstance(string_probabilities, dict) or not string_probabilities:
            raise ValueError("positive complete binary-string distribution required")
        if any(not isinstance(w, str) or not w or set(w)-set("ab") for w in string_probabilities):
            raise ValueError("nonempty binary strings required")
        words = tuple(sorted(string_probabilities))
        n = len(words[0])
        if any(len(w) != n for w in words) or set(words) != {"".join(x) for x in itertools.product("ab", repeat=n)}:
            raise ValueError("all equal-length binary strings required")
        if type(block_size) is not int or block_size < 1 or n % block_size:
            raise ValueError("block size must divide string length")
        probabilities = {w: _real(string_probabilities[w]) for w in words}
        if any(p <= 0 for p in probabilities.values()) or not math.isclose(math.fsum(probabilities.values()), 1., rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("strictly positive probabilities summing to one required")
        self.block_size, self.length, self.words = block_size, n, words
        self.tokens = tuple("".join(x) for x in itertools.product("ab", repeat=block_size))
        self.logits = {}
        for length in range(0, n, block_size):
            for chars in itertools.product("ab", repeat=length):
                prefix = "".join(chars)
                mass = math.fsum(p for w, p in probabilities.items() if w.startswith(prefix))
                self.logits[prefix] = tuple(math.log(math.fsum(p for w, p in probabilities.items() if w.startswith(prefix+t))/mass)
                                            for t in self.tokens)

    def string_distribution(self):
        result = {}
        for word in self.words:
            probability = 1.
            for position in range(0, self.length, self.block_size):
                token = word[position:position+self.block_size]
                probability *= _softmax(self.logits[word[:position]])[self.tokens.index(token)]
            result[word] = probability
        return result

    def full_gradient_step(self, word, scalars):
        """Add lambda_t*(one_hot(token)-pi_row) at VISITED rows only."""
        if word not in self.words or not isinstance(scalars, (list, tuple)) or len(scalars) != self.length//self.block_size:
            raise ValueError("known sampled word and one scalar per token required")
        scales = tuple(_real(value) for value in scalars)
        updates = {}
        for step, position in enumerate(range(0, self.length, self.block_size)):
            prefix, token = word[:position], word[position:position+self.block_size]
            probabilities = _softmax(self.logits[prefix])
            updates[prefix] = tuple(scales[step]*(float(t == token)-p) for t, p in zip(self.tokens, probabilities, strict=True))
        for prefix, update in updates.items():
            self.logits[prefix] = tuple(x+dx for x, dx in zip(self.logits[prefix], update, strict=True))
        return updates


def normalized_distance(left, right):
    """Eq.1: distance / mean norm; both zero is an undefined measurement."""
    if not isinstance(left, (list, tuple)) or not isinstance(right, (list, tuple)) or not left or len(left) != len(right):
        raise ValueError("matched nonempty update vectors required")
    a, b = tuple(_real(x) for x in left), tuple(_real(x) for x in right)
    scale = max(abs(x) for x in a+b)
    if scale == 0:
        raise ValueError("two zero updates have undefined normalized distance")
    a, b = tuple(x/scale for x in a), tuple(x/scale for x in b)
    denominator = (math.hypot(*a)+math.hypot(*b))/2
    return math.hypot(*(x-y for x, y in zip(a, b, strict=True)))/denominator


def displacement_ratio(canonical, reencoded, reference):
    """Eq.2: ratio of mean distances, NOT mean of per-batch ratios.

    All vectors must be in the same parameter space; independent coarse/fine
    tabular parameters must never be passed as if they shared LLM weights.
    """
    if (not isinstance(canonical, (list, tuple)) or not canonical
            or len(canonical) != len(reencoded) or len(canonical) != len(reference)):
        raise ValueError("matched nonempty batches required")
    first = [normalized_distance(a, b) for a, b in zip(canonical, reencoded, strict=True)]
    second = [normalized_distance(a, b) for a, b in zip(canonical, reference, strict=True)]
    denominator = math.fsum(second)
    if denominator == 0:
        raise ValueError("different-batch reference must be nonzero")
    return math.fsum(first)/denominator


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only device required")
    rng = random.Random(seed)
    raw = [rng.uniform(.2, 1.2) for _ in range(4)]
    probabilities = {w: x/math.fsum(raw) for w, x in zip(("aa", "ab", "ba", "bb"), raw, strict=True)}
    coarse, fine = PrefixPolicy(probabilities, 2), PrefixPolicy(probabilities, 1)
    initial_error = max(abs(coarse.string_distribution()[w]-fine.string_distribution()[w]) for w in probabilities)
    before = math.log(probabilities["ba"]/probabilities["bb"])
    untouched = fine.logits["b"]
    scalar = .2
    coarse.full_gradient_step("ab", (scalar,))
    fine.full_gradient_step("ab", (scalar*.7, scalar*1.3))
    c, f = coarse.string_distribution(), fine.string_distribution()
    coarse_change = math.log(c["ba"]/c["bb"])-before
    fine_change = math.log(f["ba"]/f["bb"])-before
    expected_change = -scalar*(probabilities["ba"]-probabilities["bb"])
    total_variation = math.fsum(abs(c[w]-f[w]) for w in probabilities)/2
    checks = {"same_initial_string_distribution": initial_error < 1e-12,
              "unvisited_prefix_row_is_untouched": fine.logits["b"] == untouched,
              "fine_unsampled_sibling_log_ratio_is_fixed": abs(fine_change) < 1e-12,
              "coarse_log_ratio_matches_full_gradient_equation": abs(coarse_change-expected_change) < 1e-12,
              "nonzero_steps_disagree_despite_identical_strings": total_variation > 1e-6,
              "same_update_distance_is_zero": normalized_distance((1., 2.), (1., 2.)) == 0,
              "ratio_is_common_scale_invariant": math.isclose(displacement_ratio(((1., 0.),), ((0., 1.),), ((-1., 0.),)), displacement_ratio(((3., 0.),), ((0., 3.),), ((-3., 0.),)))}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "controls": checks, "metrics": {"initial_distribution_max_abs_error": initial_error,
            "coarse_unsampled_log_ratio_change": coarse_change, "fine_unsampled_log_ratio_change": fine_change,
            "full_gradient_identity_abs_error": abs(coarse_change-expected_change), "string_total_variation": total_variation,
            "strings": 4, "word_length": 2}}
