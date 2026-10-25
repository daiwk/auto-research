"""Combinatorial watermark Eqs.2--5, arXiv:2510.01637v1.

CPU reference: caller supplies the secret vocabulary partition and base logits.
No tokenizer, production secret/key system or LLM; diagnostic is NOT a security
or real edit-localization benchmark. Thresholds require external calibration.
"""
import math
import random
from collections.abc import Sequence


def _tags(tags: Sequence[int], pattern: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    tags, pattern = tuple(tags), tuple(pattern)
    if (not tags or not pattern or len(tags) > 100_000 or len(pattern) > 128
            or any(isinstance(t, bool) or not isinstance(t, int) or t < 0 for t in (*tags, *pattern))
            or not set(tags) <= set(pattern)):
        raise ValueError("nonempty bounded integer tags and a covering cyclic pattern required")
    return tags, pattern


def biased_probabilities(logits: Sequence[float], vocabulary_tags: Sequence[int],
                         pattern: Sequence[int], *, step: int, strength: float) -> list[float]:
    """Eq.2: add delta only to the tag for this position, then stable softmax.

    Zero-based step0 uses pattern[0]; this phase convention does not affect the
    detector, which marginalizes every cyclic phase. Partition is external.
    """
    tags, pattern = _tags(vocabulary_tags, pattern)
    if (len(logits) != len(tags) or len(logits) > 65536
            or isinstance(step, bool) or not isinstance(step, int) or step < 0
            or not math.isfinite(strength) or strength <= 0
            or not all(math.isfinite(v) for v in logits)):
        raise ValueError("aligned finite logits, nonnegative step and positive finite strength required")
    target = pattern[step % len(pattern)]
    shifted = [float(value) + strength * (tag == target) for value, tag in zip(logits, tags)]
    if not all(math.isfinite(v) for v in shifted):
        raise ValueError("nonfinite shifted logits")
    maximum = max(shifted)
    masses = [math.exp(v - maximum) for v in shifted]
    total = sum(masses)
    return [value / total for value in masses]


def pattern_statistics(tags: Sequence[int], pattern: Sequence[int], *, window: int) -> dict:
    """Global Eq.4 and local Eq.5 on INTERIOR tokens with w complete windows.

    Boundary tokens lacking w covering windows are excluded, not zero-padded or
    renormalized. Matching accepts ANY cyclic phase, not absolute token index.
    Local positions are zero-based [w-1, ..., T-w].
    """
    tags, pattern = _tags(tags, pattern)
    if (isinstance(window, bool) or not isinstance(window, int) or not 1 <= window <= len(pattern)
            or len(tags) < 2 * window - 1 or len(tags) * len(pattern) * window > 2_000_000):
        raise ValueError("valid window<=period, nonempty full interior and bounded matching cost required")
    patterns = {tuple(pattern[(phase + j) % len(pattern)] for j in range(window))
                for phase in range(len(pattern))}
    matches = [int(tags[start:start + window] in patterns) for start in range(len(tags) - window + 1)]
    positions = list(range(window - 1, len(tags) - window + 1))
    local = [sum(matches[t - window + 1:t + 1]) / window for t in positions]
    return {"global_score": sum(matches) / len(matches), "matches": matches,
            "local_positions": positions, "local_scores": local}


def detect(tags: Sequence[int], pattern: Sequence[int], *, window: int,
           watermark_threshold: float, edit_threshold: float) -> dict:
    """Watermark>=threshold; local edit<threshold, using externally calibrated cutoffs."""
    if not all(math.isfinite(v) and 0 <= v <= 1 for v in (watermark_threshold, edit_threshold)):
        raise ValueError("finite thresholds in [0,1] required")
    result = pattern_statistics(tags, pattern, window=window)
    positions = [position for position, score in zip(result["local_positions"], result["local_scores"])
                 if score < edit_threshold]
    return {**result, "watermarked": result["global_score"] >= watermark_threshold,
            "edited": bool(positions), "potential_edit_positions": positions}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("pure CPU reference; no advertised CUDA path")
    rng = random.Random(seed)
    pattern = [0, 2, 0, 3, 1, 2, 1, 3]
    phase = rng.randrange(8)
    clean = [pattern[(phase + i) % 8] for i in range(64)]
    edited = clean.copy()
    edited[31] = (edited[31] + 1) % 4
    original = detect(clean, pattern, window=4, watermark_threshold=.8, edit_threshold=.9)
    changed = detect(edited, pattern, window=4, watermark_threshold=.8, edit_threshold=.9)
    # Independent nested-loop phase oracle, not the set/window implementation.
    matches = [int(any(all(edited[i + j] == pattern[(p + j) % 8] for j in range(4))
                       for p in range(8))) for i in range(61)]
    local = [sum(matches[t - offset] for offset in range(4)) / 4 for t in range(3, 61)]
    global_error = abs(changed["global_score"] - sum(matches) / 61)
    local_error = max(abs(a - b) for a, b in zip(changed["local_scores"], local))
    vocab = [i % 4 for i in range(12)]
    logits = [rng.uniform(-1, 1) for _ in vocab]
    probabilities = biased_probabilities(logits, vocab, pattern, step=0, strength=2.)
    base = [math.exp(x) for x in logits]
    base = [v / sum(base) for v in base]
    gain = sum(p - q for p, q, tag in zip(probabilities, base, vocab) if tag == pattern[0])
    checks = {"eq4_global_matches_phase_oracle": global_error == 0,
              "eq5_local_matches_covering_window_oracle": local_error == 0,
              "cyclic_phase_invariance": original["global_score"] == 1,
              "clean_hard_pattern_no_interior_false_alarm": not original["edited"],
              "single_edit_flags_its_interior_position": 31 in changed["potential_edit_positions"],
              "logit_shift_increases_target_tag_mass": gain > 0 and abs(sum(probabilities) - 1) < 1e-12}
    if not all(checks.values()):
        raise RuntimeError(f"combinatorial watermark contract failed: {checks}")
    return {"seed": seed, "metrics": {"global_reference_error": global_error, "local_reference_error": local_error,
        "clean_global_score": original["global_score"], "edited_global_score": changed["global_score"],
        "flagged_interior_positions": len(changed["potential_edit_positions"]), "target_tag_mass_gain": gain,
        "tokens": 64, "window": 4, "pattern_period": 8, "pretrained_model_calls": 0}, "checks": checks}
