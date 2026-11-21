"""e-RWSC v1: prefix-causal answer-level certification, pure CPU reference.

An anytime certificate concerns majority probability under a fixed iid policy,
not truth, usefulness, or a benchmark's gold answer. No generator or reward
model is substituted with a fixture; supplied observations are explicit.
"""

from dataclasses import dataclass
import math
import random

REQUIRES_GPU_VALIDATION = False


def _real(value, name):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name}: finite real number required")
    return float(value)


def rwsc_masses(observations, temperature=1.):
    """Eq.1 with population reward standardization and stable softmax.

    Equal rewards use uniform response weights, an explicit equal-score
    convention for the otherwise undefined zero-variance normalization.
"""
    tau = _real(temperature, "temperature")
    if tau <= 0 or not isinstance(observations, (tuple, list)) or not observations:
        raise ValueError("positive temperature and nonempty observations required")
    checked = []
    for row in observations:
        if (not isinstance(row, (tuple, list)) or len(row) != 2
                or not isinstance(row[0], str) or not row[0]):
            raise ValueError("nonempty canonical answer and finite reward required")
        checked.append((row[0], _real(row[1], "reward")))
    scale = max(abs(row[1]) for row in checked) or 1.
    scaled = [row[1]/scale for row in checked]
    mean = math.fsum(scaled)/len(scaled)
    sd = math.sqrt(math.fsum((x-mean)**2 for x in scaled)/len(scaled))
    standardized = [(x-mean)/sd for x in scaled] if sd else [0.]*len(scaled)
    largest = max(standardized)
    weights = [math.exp((x-largest)/tau) for x in standardized]
    total = math.fsum(weights)
    masses = dict.fromkeys((row[0] for row in checked), 0.)
    for (answer, _), weight in zip(checked, weights, strict=True):
        masses[answer] += weight/total
    return masses


@dataclass
class AnswerEvidence:
    first_seen: int
    rank: int
    post_appearance_agreements: int = 0
    log_wealth: float = 0.


@dataclass(frozen=True)
class Selection:
    answer: str
    response_index: int
    certified: bool
    samples: int
    log_weighted_wealth: float
    reason: str


class ERWSC:
    """Algorithm2, supporting the paper's strict-majority threshold range.

    Observations must come independently from the same policy distribution.
    The caller owns answer canonicalization and reward-model execution. Ties
    are resolved by first answer/response appearance, an explicit local rule.
    """

    def __init__(self, *, alpha=.05, threshold=.5, clip=.9, prior_strength=4.,
                 max_samples=512, temperature=1.):
        self.alpha = _real(alpha, "alpha")
        self.threshold = _real(threshold, "threshold")
        self.clip = _real(clip, "clip")
        self.prior_strength = _real(prior_strength, "prior_strength")
        self.temperature = _real(temperature, "temperature")
        if (not 0 < self.alpha < 1 or not .5 <= self.threshold < 1 or not 0 < self.clip < 1
                or self.prior_strength <= 0 or self.temperature <= 0
                or type(max_samples) is not int or max_samples < 1):
            raise ValueError("valid majority-certification parameters required")
        self.max_samples = max_samples
        self.observations = []
        self.evidence = {}
        self.last_bets = {}
        self.result = None

    def predictable_bets(self):
        """Eq.10: only the already-observed prefix enters the next stake."""
        if not self.observations:
            return {}
        masses = rwsc_masses(self.observations, self.temperature)
        n = len(self.observations)
        p, m = self.threshold, self.prior_strength
        return {
            answer: min(self.clip/p, max(0.,
                ((state.post_appearance_agreements+m*masses[answer])/
                 (n-state.first_seen+m)-p)/(p*(1-p))))
            for answer, state in self.evidence.items()
        }

    def _weighted_wealth(self, answer):
        state = self.evidence[answer]
        return state.log_wealth-math.log(state.rank)-math.log(state.rank+1)

    def _select(self, answer, certified, reason):
        candidates = [i for i, row in enumerate(self.observations) if row[0] == answer]
        index = max(candidates, key=lambda i: (self.observations[i][1], -i))
        self.result = Selection(answer, index, certified, len(self.observations),
                                self._weighted_wealth(answer), reason)
        return self.result

    def observe(self, answer, reward):
        """Settle old stakes, then register a new answer with unit capital."""
        if self.result is not None:
            raise ValueError("cannot consume observations after a terminal selection")
        if not isinstance(answer, str) or not answer:
            raise ValueError("nonempty canonical answer required")
        score = _real(reward, "reward")
        self.last_bets = self.predictable_bets()
        for old_answer, state in self.evidence.items():
            agreement = int(old_answer == answer)
            increment = self.last_bets[old_answer]*(agreement-self.threshold)
            state.log_wealth += math.log1p(increment)
            state.post_appearance_agreements += agreement
        self.observations.append((answer, score))
        if answer not in self.evidence:
            self.evidence[answer] = AnswerEvidence(len(self.observations), len(self.evidence)+1)
        boundary = -math.log(self.alpha)
        certified = [a for a in self.evidence if self._weighted_wealth(a) >= boundary]
        if certified:
            chosen = max(certified, key=self._weighted_wealth)
            return self._select(chosen, True, "majority_certified_not_correctness")
        if len(self.observations) == self.max_samples:
            masses = rwsc_masses(self.observations, self.temperature)
            return self._select(max(masses, key=masses.get), False, "budget_exhausted_uncertified")
        return None


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU device required")
    rng = random.Random(seed)
    repeated = ERWSC(max_samples=64)
    repeated.observe("deliberately_wrong", 1.)
    first = repeated.evidence["deliberately_wrong"]
    first_skipped = first.log_wealth == 0 and first.post_appearance_agreements == 0
    while repeated.result is None:
        repeated.observe("deliberately_wrong", rng.random())
    exhausted = ERWSC(alpha=1e-12, max_samples=24)
    for n in range(24):
        exhausted.observe("a" if n % 2 else "b", rng.random())
    left, right = ERWSC(max_samples=32), ERWSC(max_samples=32)
    for answer, reward in (("a", 1.), ("b", 0.), ("a", .5)):
        left.observe(answer, reward)
        right.observe(answer, reward)
    left.observe("a", 1e10)
    right.observe("c", -1e10)
    shifted = ERWSC(alpha=1e-12, max_samples=32)
    for _ in range(3):
        shifted.observe("a", 0.)
    previous = shifted.evidence["a"].log_wealth
    stake = shifted.predictable_bets()["a"]
    shifted.observe("b", 100.)
    expected = previous+math.log1p(-stake*shifted.threshold)
    masses = rwsc_masses([("a", 2.), ("b", 3.), ("a", -1.)])
    affine = rwsc_masses([("a", 24.), ("b", 31.), ("a", 3.)])
    extreme = rwsc_masses([("a", 1e308), ("b", -1e308)])
    checks = {
        "first_appearance_does_not_bet_on_its_forced_success": first_skipped,
        "fixed_concentrated_policy_can_certify_a_wrong_answer": repeated.result.certified,
        "budget_fallback_is_explicitly_uncertified": not exhausted.result.certified,
        "budget_is_not_silently_extended": exhausted.result.samples == 24,
        "bets_use_only_previous_prefix_not_new_reward_or_answer": left.last_bets == right.last_bets,
        "leader_shift_does_not_reset_old_answer_evidence": abs(shifted.evidence["a"].log_wealth-expected) < 1e-12
            and shifted.evidence["a"].log_wealth != 0,
        "positive_affine_reward_transform_preserves_masses": max(abs(masses[k]-affine[k]) for k in masses) < 1e-12,
        "equal_rewards_use_uniform_response_weights": rwsc_masses([("a", 1.), ("b", 1.), ("a", 1.)])["a"] == 2/3,
        "large_finite_rewards_do_not_overflow_softmax": all(math.isfinite(x) for x in extreme.values()),
    }
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "controls": checks, "metrics": {
                "concentrated_stream_stopping_samples": repeated.result.samples,
                "uncertified_fallback_samples": exhausted.result.samples,
                "active_answer_count": len(exhausted.evidence),
                "affine_mass_max_abs_error": max(abs(masses[k]-affine[k]) for k in masses),
            }}
