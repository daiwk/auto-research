"""MCRT Bernoulli uncertainty and the two actual top-k contractions."""
from __future__ import annotations

import math
import torch


def monte_carlo_uncertainty(outcomes):
    if len(outcomes) < 2 or any(value not in (0, 1) for value in outcomes):
        raise ValueError("MCRT needs actual binary outcomes from >=2 independent continuations")
    p = sum(outcomes)/len(outcomes)
    return {"reachability": p, "uncertainty": 4*p*(1-p), "samples": len(outcomes)}


def contract_teacher_pool(profiles, ratio):
    if not 0 < ratio <= 1 or not profiles:
        raise ValueError("positive verified teacher pool and contraction ratio required")
    count = math.floor(ratio*len(profiles))
    if count < 1:
        raise ValueError("floor(rho*N_verified) is zero; increase verified pool, do not fabricate a member")
    scores = [sum(state["uncertainty"] for state in profile)/len(profile) for profile in profiles]
    selected = sorted(range(len(scores)), key=lambda i:(-scores[i],i))[:count]
    return selected, scores


def route_student(losses, count):
    if not 1 <= count <= len(losses) or any(not math.isfinite(x) for x in losses):
        raise ValueError("finite current learner NLL scores and valid active-set size required")
    return sorted(range(len(losses)), key=lambda i:(-losses[i],i))[:count]


def normalized_response_nll(log_probabilities):
    if not log_probabilities.numel() or not torch.isfinite(log_probabilities).all():
        raise ValueError("actual finite response-token likelihoods required")
    return -log_probabilities.mean()


def paragraph_prefixes(tokens, delimiter_tokens, *, limit=3):
    delimiter = tuple(delimiter_tokens)
    if not delimiter or limit < 1:
        raise ValueError("tokenized paragraph delimiter and positive state budget required")
    cuts = [i+len(delimiter) for i in range(len(tokens)-len(delimiter)+1)
            if tuple(tokens[i:i+len(delimiter)]) == delimiter and i+len(delimiter) < len(tokens)]
    return cuts[:limit]
