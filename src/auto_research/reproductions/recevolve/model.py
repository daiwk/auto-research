from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    temperature: float=1.0
    watch_power: float=0.0
    cross_strength: float=0.0
    cosine_decay: bool=False


class ResearchLoop:
    """Knowledge queue, critic gate, isolated trial and rollback controller."""
    def __init__(self,baseline:Candidate):
        self.champion=baseline; self.score=float("-inf"); self.knowledge=[]; self.rollbacks=0; self.reward_hacks=0

    def evaluate(self,candidate:Candidate,evaluator):
        # Smaller batches are a known invalid shortcut in the paper; the public
        # controller rejects the equivalent candidate before scoring.
        if candidate.temperature<.05:
            self.reward_hacks+=1; self.rollbacks+=1; return False,self.score
        score=float(evaluator(candidate))
        accepted=score>self.score
        self.knowledge.append({"candidate":candidate,"score":score,"accepted":accepted})
        if accepted: self.champion,self.score=candidate,score
        else: self.rollbacks+=1
        return accepted,score
