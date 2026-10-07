"""Extracted unchanged from auto_research.agent_research.latest_20261002; stable mechanism boundary."""
from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses import dataclass, field

@dataclass
class NonDestructiveMemory:
    """Mem++-style full-document store with time-aware hybrid retrieval."""

    documents: list[dict] = field(default_factory=list)

    def write(self, *, text: str, date: str, author: str) -> None:
        self.documents.append({"text": text, "date": date, "author": author})

    def retrieve(self, query_terms, semantic_scores, *, as_of: str, limit: int = 3):
        terms = {str(term).lower() for term in query_terms}
        eligible = [item for item in self.documents if item["date"] <= as_of]
        ranked = []
        for item in eligible:
            lexical = sum(term in item["text"].lower() for term in terms)
            semantic = float(semantic_scores.get(item["text"], 0.0))
            ranked.append((lexical + semantic, item["date"], item))
        return [item for _, _, item in sorted(ranked, reverse=True)[:limit]]
