"""LoopCache v1 scheduling/update interface, explicitly L0, not a decoder.

This policy never commits tokens: an external exact KV branch must recompute
the candidate prefix. No mock verifier or future/gold token is supplied.
"""

import math

REQUIRES_GPU_VALIDATION = False


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(name + " must be a positive integer")


def scheduled_loop(global_step, loops):
    _positive(global_step, "global_step")
    _positive(loops, "loops")
    return 1 + (global_step - 1) % loops


def next_verification_cycle(global_step, loops):
    """Nearest not-yet-passed loop1 slot; exact branch traverses loops1..R."""
    current = scheduled_loop(global_step, loops)
    return global_step if current == 1 else global_step + loops - current + 1


def speculative_cache_loop(layer, draft_loop, cycle_loop, *, shallow_layers, gap_threshold, loops):
    for x, name in (
        (layer, "layer"),
        (draft_loop, "draft_loop"),
        (cycle_loop, "cycle_loop"),
        (gap_threshold, "gap_threshold"),
        (loops, "loops"),
    ):
        _positive(x, name)
    if (
        draft_loop > loops
        or cycle_loop > loops
        or any(type(x) is not int or x < 1 for x in shallow_layers)
    ):
        raise ValueError("loop range and positive shallow-layer indices required")
    return (
        draft_loop
        if layer in shallow_layers and abs(draft_loop - cycle_loop) >= gap_threshold
        else cycle_loop
    )


def update_draft(current_token, logits, *, threshold):
    """Return (new_token, prune_all_descendants); equality at threshold updates."""
    if (
        not isinstance(logits, (list, tuple))
        or not logits
        or any(type(x) not in (int, float) or not math.isfinite(x) for x in logits)
        or type(current_token) is not int
        or not 0 <= current_token < len(logits)
        or type(threshold) not in (int, float)
        or not math.isfinite(threshold)
        or threshold < 0
    ):
        raise ValueError("finite logits, valid current token and nonnegative threshold required")
    candidate = max(range(len(logits)), key=lambda i: logits[i])
    replace = candidate != current_token and logits[candidate] - logits[current_token] >= threshold
    return (candidate, True) if replace else (current_token, False)


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("CPU-only interface with nonnegative integer seed")
    cycle = [scheduled_loop(t, 4) for t in range(1, 10)]
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l0_interface",
        "checks": {
            "cycle_wrap": cycle == [1, 2, 3, 4, 1, 2, 3, 4, 1],
            "threshold_boundary_updates": update_draft(0, [0.0, 0.125], threshold=0.125)
            == (1, True),
            "weak_switch_retained": update_draft(0, [0.0, 0.124], threshold=0.125) == (0, False),
            "shallow_mismatch_decoupled": speculative_cache_loop(
                1, 4, 1, shallow_layers={1, 2}, gap_threshold=1, loops=4
            )
            == 4,
            "deep_layer_shares_cycle": speculative_cache_loop(
                3, 4, 1, shallow_layers={1, 2}, gap_threshold=1, loops=4
            )
            == 1,
            "verification_waits_for_full_cycle": next_verification_cycle(6, 4) == 9,
        },
        "metrics": {
            "distinct_cycle_slots": len(set(cycle)),
            "verification_cycle_wait": next_verification_cycle(6, 4) - 6,
            "tokens_committed": 0,
            "model_calls": 0,
        },
    }
