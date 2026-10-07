"""Extracted unchanged from auto_research.agent_research.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



class MemFitStore:
    """Append-only turns with LLM-free lexical/semantic retrieval hooks."""

    def __init__(self):
        self.turns = []

    def append(self, text, *, segment):
        self.turns.append({"text": text, "segment": segment})

    def retrieve(self, query_terms, semantic_scores, *, limit):
        rows = []
        for index, turn in enumerate(self.turns):
            lexical = sum(term.lower() in turn["text"].lower() for term in query_terms)
            rows.append((lexical + semantic_scores.get(index, 0), turn))
        return tuple(turn for _, turn in sorted(rows, key=lambda row: row[0], reverse=True)[:limit])
