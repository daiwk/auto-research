"""2603.24917 top-k CBS: exact path mass and epsilon-viable edit pruning.

An external next-token-logit callback sees only prefix+generated continuation,
never the audit target. No model, corpus, KV cache or extraction experiment is
included. Optional tau_min early stopping is deliberately not implemented.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import math
import random

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Continuation:
    tokens: tuple[int, ...]
    log_probability: float


@dataclass(frozen=True)
class SearchResult:
    continuations: tuple[Continuation, ...]
    lower_bound: float
    upper_bound: float
    banked_pruned_mass: float
    model_calls: int


def _tokens(values):
    result = tuple(values)
    if any(type(x) is not int or x < 0 for x in result):
        raise ValueError("nonnegative integer token IDs required")
    return result


def _top_k(logits: Sequence[float], k: int):
    logits = tuple(float(x) for x in logits)
    if not logits or k > len(logits) or any(math.isnan(x) or x == math.inf for x in logits):
        raise ValueError("valid finite-or-negative-infinite logits and k <= vocabulary required")
    order = sorted(range(len(logits)), key=lambda i: (-logits[i], i))[:k]
    finite = [i for i in order if math.isfinite(logits[i])]
    if not finite:
        raise ValueError("top-k support cannot be empty")
    maximum = logits[finite[0]]
    log_z = maximum + math.log(sum(math.exp(logits[i] - maximum) for i in finite))
    return tuple((i, logits[i] - log_z) for i in finite)


def _edit_row(previous: dict[int, int], token: int, depth: int, target: tuple[int, ...], epsilon: int):
    inf = len(target) + epsilon + 2
    row = {}
    for j in range(max(0, depth-epsilon), min(len(target), depth+epsilon)+1):
        if j == 0:
            row[j] = depth
        else:
            row[j] = min(previous.get(j, inf)+1, row.get(j-1, inf)+1,
                         previous.get(j-1, inf)+(token != target[j-1]))
    return row


def search(next_logits: Callable[[tuple[int, ...]], Sequence[float]], prefix, target, *,
           beam_width: int, top_k: int, epsilon: int = 0, distance: str = "levenshtein",
           eos_token_id: int | None = None) -> SearchResult:
    prefix, target = _tokens(prefix), _tokens(target)
    if not callable(next_logits) or not target or any(type(n) is not int or n <= 0 for n in (beam_width, top_k)):
        raise ValueError("logit callback, nonempty fixed target and positive beam/k required")
    if type(epsilon) is not int or epsilon < 0 or distance not in {"levenshtein", "hamming"}:
        raise ValueError("nonnegative integer edit budget and supported token distance required")
    if eos_token_id is not None and (type(eos_token_id) is not int or eos_token_id < 0):
        raise ValueError("explicit nonnegative EOS ID or None required")
    initial = {j: j for j in range(min(len(target), epsilon)+1)} if distance == "levenshtein" else 0
    beam = [((), 0., initial)]
    bank = 0.; calls = 0
    for depth in range(1, len(target)+1):
        candidates = []
        for tokens, log_p, aux in beam:
            distribution = _top_k(next_logits(prefix + tokens), top_k); calls += 1
            for token, log_conditional in distribution:
                if distance == "hamming":
                    state = aux + int(token != target[depth-1]); viable = state <= epsilon
                else:
                    state = _edit_row(aux, token, depth, target, epsilon); viable = min(state.values()) <= epsilon
                if viable:
                    candidates.append((tokens + (token,), log_p + log_conditional, state))
        # Final expansions are NOT pruned back to B. Levenshtein still needs its
        # full-target final cell; row-min viability alone is not acceptance.
        if depth == len(target):
            finals = tuple(Continuation(tokens, lp) for tokens, lp, state in candidates
                           if distance == "hamming" or state.get(len(target), epsilon+1) <= epsilon)
            lower = math.fsum(math.exp(x.log_probability) for x in finals)
            return SearchResult(finals, lower, min(1., lower+bank), bank, calls)
        candidates = [row for row in candidates if eos_token_id is None or row[0][-1] != eos_token_id]
        if not candidates:
            return SearchResult((), 0., min(1., bank), bank, calls)
        candidates.sort(key=lambda row: (-row[1], row[0]))
        bank += math.fsum(math.exp(row[1]) for row in candidates[beam_width:])
        beam = candidates[:beam_width]
    raise AssertionError("nonempty target must return a result")


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU callback execution required")
    rng = random.Random(seed)
    p = .6 + rng.random() * .1
    def logits(_history):
        return [math.log(p), math.log(1-p), -30.]
    complete = search(logits, [9], [0, 0], beam_width=4, top_k=2, epsilon=1, distance="hamming")
    narrow = search(logits, [9], [0, 0], beam_width=1, top_k=2, epsilon=1, distance="hamming")
    exact = p*p + 2*p*(1-p)
    lev = search(logits, [], [0, 1], beam_width=4, top_k=2, epsilon=1)
    checks = {"renormalized_mass_exact": math.isclose(complete.lower_bound, exact, abs_tol=1e-12),
              "narrow_beam_lower_bound": narrow.lower_bound <= exact + 1e-12,
              "bank_covers_unexplored_viable_mass": exact <= narrow.upper_bound + 1e-12,
              "final_expansion_not_pruned_to_B": len(narrow.continuations) == 2,
              "levenshtein_final_check": all(len(x.tokens) == 2 for x in lev.continuations)}
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"mass_error": abs(complete.lower_bound-exact), "narrow_lower_bound": narrow.lower_bound,
                        "narrow_upper_bound": narrow.upper_bound, "pretrained_model_calls": 0}, "checks": checks}
