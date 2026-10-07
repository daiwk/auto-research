"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def suffix_cache_reuse(previous_tokens, current_tokens):
    """Return the longest reusable prefix and unmatched CLM suffix."""
    matched = 0
    for left, right in zip(previous_tokens, current_tokens):
        if left != right:
            break
        matched += 1
    return matched, tuple(current_tokens[matched:])
