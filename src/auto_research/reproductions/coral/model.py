from __future__ import annotations
import numpy as np


def project_budget(proposal: np.ndarray, budget: float, lower: float = 0.25, upper: float = 2.0):
    """Deterministically project a proposal into box and total-budget constraints."""
    value=np.clip(np.asarray(proposal,dtype=float),lower,upper)
    if value.sum()>budget:
        lo,hi=0.0,float(value.max())
        for _ in range(64):
            mid=(lo+hi)/2; candidate=np.clip(value-mid,lower,upper)
            if candidate.sum()>budget: lo=mid
            else: hi=mid
        value=np.clip(value-hi,lower,upper)
    return value


class CoralLoop:
    def __init__(self,sources:int,budget:float,memory_cycles:int=3):
        self.config=np.full(sources,budget/sources); self.budget=budget; self.memory_cycles=memory_cycles; self.memory=[]

    def step(self,conversion,cost):
        efficiency=np.asarray(conversion)/np.maximum(cost,1e-8)
        centered=(efficiency-efficiency.mean())/max(efficiency.std(),1e-8)
        direction=centered
        if self.memory:
            helpful=[x["delta"] for x in self.memory if x["effect"]>0]
            if helpful: direction=.7*direction+.3*np.mean(helpful,axis=0)
        proposed=self.config+.15*direction
        next_config=project_budget(proposed,self.budget)
        effect=float(np.dot(next_config-self.config,efficiency))
        self.memory.append({"delta":next_config-self.config,"effect":effect})
        self.memory=self.memory[-self.memory_cycles:]
        self.config=next_config
        return next_config,effect
