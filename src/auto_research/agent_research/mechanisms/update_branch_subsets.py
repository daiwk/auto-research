"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def update_branch_subsets(branch_scores):
    """Retain cases solved more often by one branch and drop globally solved cases."""
    branches = sorted(branch_scores)
    cases = sorted({case for scores in branch_scores.values() for case in scores})
    retained = {branch: [] for branch in branches}
    for case in cases:
        values = {branch: float(branch_scores[branch].get(case, 0.0)) for branch in branches}
        if values and all(value >= 1.0 for value in values.values()):
            continue
        best = max(values.values(), default=0.0)
        for branch, value in values.items():
            if value == best and value > 0:
                retained[branch].append(case)
    return {branch: tuple(cases) for branch, cases in retained.items()}
