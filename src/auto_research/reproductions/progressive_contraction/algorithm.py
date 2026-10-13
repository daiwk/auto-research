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


def paragraph_prefixes(tokens, delimiter_tokens=(), *, limit=3, tokenizer=None):
    """Map actual decoded paragraph ends to ORIGINAL token-prefix indices.

    BPE may fuse punctuation and newlines into one token. Decoding is only
    used to locate boundaries; no generated prefix is ever re-tokenized.
    The tuple-delimiter branch remains for existing deterministic fixtures.
    """
    if limit<1:
        raise ValueError("positive paragraph state budget required")
    if tokenizer is not None:
        original=tuple(tokens)
        def decode(prefix):
            return tokenizer.decode(prefix,skip_special_tokens=True,clean_up_tokenization_spaces=False)
        text=decode(original)
        ends=[]
        begin=0
        while (found:=text.find("\n\n",begin))>=0:
            end=found+2
            if text[end:].strip():
                ends.append(end)
            begin=end
        cuts=[]
        boundary=0
        for cut in range(1,len(original)):
            if boundary==len(ends):
                break
            prefix=decode(original[:cut])
            # Partial UTF-8 byte tokens can decode to replacement characters.
            # Only map a boundary at a stable actual prefix of the full text.
            if not text.startswith(prefix):
                continue
            while boundary<len(ends) and ends[boundary]<=len(prefix):
                if not cuts or cuts[-1]!=cut:
                    cuts.append(cut)
                    if len(cuts)==limit:
                        return cuts
                boundary+=1
        return cuts
    delimiter = tuple(delimiter_tokens)
    if not delimiter or limit < 1:
        raise ValueError("tokenized paragraph delimiter and positive state budget required")
    cuts = [i+len(delimiter) for i in range(len(tokens)-len(delimiter)+1)
            if tuple(tokens[i:i+len(delimiter)]) == delimiter and i+len(delimiter) < len(tokens)]
    return cuts[:limit]
