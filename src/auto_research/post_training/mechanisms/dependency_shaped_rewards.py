"""Extracted unchanged from auto_research.post_training.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def dependency_shaped_rewards(events, prerequisites, *, discount: float = 0.5):
    """DARS potential differences over verified, broken and repaired predicates.

    ``events`` is a sequence of mappings with optional ``verify``, ``invalidate``
    and ``repair`` predicate lists.  A broken prerequisite attenuates dependent
    predicates while independent verified work retains credit.
    """
    if not 0 <= discount <= 1:
        raise ValueError("discount must be in [0, 1]")
    verified: set[str] = set()
    broken: set[str] = set()

    def potential() -> float:
        score = 0.0
        for predicate in verified:
            frontier = [predicate]
            seen: set[str] = set()
            distance = 0
            weight = 1.0
            while frontier:
                if any(node in broken for node in frontier):
                    weight = discount ** max(distance, 1)
                    break
                seen.update(frontier)
                frontier = [
                    parent
                    for node in frontier
                    for parent in prerequisites.get(node, ())
                    if parent not in seen
                ]
                distance += 1
            score += weight
        return score

    rewards = []
    previous = potential()
    for event in events:
        for predicate in event.get("invalidate", ()):
            broken.add(predicate)
            verified.discard(predicate)
        for predicate in event.get("repair", ()):
            broken.discard(predicate)
        for predicate in event.get("verify", ()):
            verified.add(predicate)
            broken.discard(predicate)
        current = potential()
        rewards.append(current - previous)
        previous = current
    return rewards, {"verified": tuple(sorted(verified)), "broken": tuple(sorted(broken))}
