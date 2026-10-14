"""SynthSelf Algorithm 1 and Eq. 6; construction teacher is not evaluated student."""
from __future__ import annotations

import math


def family(public_id):
    return public_id.split("/")[-1].split("-", 1)[0].casefold()


def validate_aligner(student_id, aligner_id, student_parameters, aligner_parameters):
    if family(student_id) != family(aligner_id):
        raise ValueError("SynthSelf requires a same-family aligner")
    if aligner_parameters <= student_parameters:
        raise ValueError("aligner must be larger than the student")


def rewrite_messages(question, training_demonstration):
    # Appendix A Prompt A. Only called for the training split construction.
    return ({"role": "user", "content":
             "Rewrite the following response in your own words. Keep the SAME final answer and the SAME format exactly.\n"
             f"Question: {question}\nResponse to rewrite: {training_demonstration}"},)


def complete_response_tokens(tokens,*,eos_token_id):
    """Canonical full-response target: original token IDs plus exactly one EOS."""
    if type(eos_token_id) is not int or eos_token_id<0:
        raise ValueError("explicit valid EOS token identity required")
    values=tuple(tokens)
    while values and values[-1]==eos_token_id:
        values=values[:-1]
    if eos_token_id in values:
        raise ValueError("internal EOS cannot be silently truncated or re-encoded")
    return values+(eos_token_id,)


def naturally_complete_response(tokens,*,truncated,eos_token_id):
    """Only actual normal termination can supply full rewrite-sequence evidence."""
    if type(eos_token_id) is not int or eos_token_id<0:
        raise ValueError("explicit valid EOS token identity required")
    values=tuple(tokens)
    return (not truncated and bool(values) and values[-1]==eos_token_id
            and values.count(eos_token_id)==1)


def select_aligner(candidates, *, gold_nll, self_quality):
    """Measured validation-of-training-construction constraints, never test selection."""
    if not math.isfinite(gold_nll) or not 0 <= self_quality <= 1:
        raise ValueError("finite empirical gold NLL and quality required")
    eligible = [row for row in candidates if math.isfinite(row["nll"]) and row["nll"] < gold_nll
                and row["quality"] > self_quality]
    return min(eligible, key=lambda row: (row["nll"], row["id"])) if eligible else None
