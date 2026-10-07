"""Extracted unchanged from auto_research.agent_research.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def mnemon_view(records, query_terms, *, budget: int):
    """System-1 record judgments build a bounded raw-record view for answering."""
    if budget < 1:
        raise ValueError("budget must be positive")
    terms = {term.casefold() for term in query_terms}
    scored = []
    for index, record in enumerate(records):
        text = record["text"].casefold()
        score = sum(term in text for term in terms)
        scored.append((score, record.get("date", ""), -index, record))
    selected = [item[-1] for item in sorted(scored, reverse=True)[:budget] if item[0] > 0]
    return selected, {"records_scanned": len(records), "view_size": len(selected), "budget": budget}
