"""DISCO v1, Algorithm 2: unboosted, binary-coarsened CPU reference.

This is a statistical component, not an LLM behavior-discovery agent. The
caller must supply valid, query-invariant, memoryless null p-values and a
selector respecting the coarsened interface (Assumptions 1--4). We calculate
Theorems 1/2 from a small *exact finite null law*, never from uncorrected Monte
Carlo estimates. Multi-bin/boosted extensions and the paper's models are absent.
"""

from dataclasses import asdict, dataclass, field
import math
import random

REQUIRES_GPU_VALIDATION = False


def _real(value, name):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name}: finite real number required")
    return float(value)


def _positive_int(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name}: positive integer required")
    return value


def _reaches(value, boundary):
    """Inclusive log boundary, allowing four ulps of arithmetic roundoff."""
    return value >= boundary or (
        math.isfinite(value) and math.isfinite(boundary)
        and abs(value - boundary) <= 4 * max(math.ulp(value), math.ulp(boundary))
    )


def log_p_to_e(p_value, kappa=.5):
    """Section 3.1: log(kappa * p**(kappa-1)); p=0 is infinite evidence."""
    p = _real(p_value, "p_value")
    k = _real(kappa, "kappa")
    if not 0 <= p <= 1 or not 0 < k < 1:
        raise ValueError("p in [0,1] and kappa in (0,1) required")
    return math.inf if p == 0 else math.log(k) + (k - 1) * math.log(p)


def _ebh_from_logs(log_values, alpha, k_bar):
    level = _real(alpha, "alpha")
    if not 0 <= level <= 1:
        raise ValueError("alpha in [0,1] required")
    if not log_values:
        if type(k_bar) is not int or k_bar < 0:
            raise ValueError("nonnegative k_bar required")
        return ()
    _positive_int(k_bar, "k_bar")
    if k_bar < len(log_values):
        raise ValueError("the supported upper-bound weighting requires k_bar >= K")
    if level == 0:
        return ()
    ranked = sorted(log_values, key=lambda h: -log_values[h])
    count = 0
    for rank, name in enumerate(ranked, 1):
        if _reaches(math.log(rank) + log_values[name] - math.log(k_bar), -math.log(level)):
            count = rank
    return tuple(ranked[:count])


def weighted_ebh(e_values, *, alpha=.1, k_bar=None):
    """Equation 2, deterministic insertion-order ties; no adaptive-K guarantee.

    Using observed K after output-dependent selection requires DISCO's
    restrictions and correction, not merely this final step-up function.
    """
    logs = {}
    for name, value in e_values.items():
        if type(value) not in (int, float) or math.isnan(value) or value < 0:
            raise ValueError("nonnegative e-values required")
        logs[name] = -math.inf if value == 0 else math.log(value)
    return _ebh_from_logs(logs, alpha, len(logs) if k_bar is None else k_bar)


@dataclass(frozen=True)
class NullCalibration:
    kappa: float
    e_max: float
    n_max: int
    active_means: tuple
    exit_probabilities: tuple
    exact_path_enumeration: bool = True

    @property
    def epsilon(self):
        return max(self.active_means)

    @property
    def exit_probability(self):
        return self.exit_probabilities[-1]


def exact_null_calibration(pmf, *, kappa=.5, e_max=50., n_max=3,
                           max_paths=100_000):
    """Eq.4 via exact enumeration of an explicitly known finite null law.

    This limited calculator rejects laws that are not super-uniform and caps
    enumeration before work. A finite-law diagnostic does not validate the
    p-value distribution of a real model/test. No sampled approximation is
    represented as a rigorous bound.
    """
    k = _real(kappa, "kappa")
    threshold = _real(e_max, "e_max")
    limit = _positive_int(n_max, "n_max")
    _positive_int(max_paths, "max_paths")
    if not 0 < k < 1 or threshold <= 1 or not pmf:
        raise ValueError("kappa in (0,1), e_max > 1 and a finite null law required")
    law = {}
    for p_value, probability in pmf:
        p = _real(p_value, "p_value")
        probability = _real(probability, "probability")
        if not 0 < p <= 1 or probability <= 0:
            raise ValueError("finite null support must have p in (0,1] and positive mass")
        law[p] = law.get(p, 0.) + probability
    if not math.isclose(math.fsum(law.values()), 1., abs_tol=1e-12, rel_tol=0.):
        raise ValueError("null probabilities must sum to one")
    cumulative = 0.
    for p in sorted(law):
        cumulative += law[p]
        if cumulative > p + 1e-12:
            raise ValueError("the supplied null p-value law is not super-uniform")
    if limit > max_paths or len(law) ** limit > max_paths:
        raise ValueError("exact null enumeration exceeds the declared path budget")
    active = [(0., 1.)]
    exit_mass = 0.
    means, exits = [], []
    log_boundary = math.log(threshold)
    for _ in range(limit):
        next_active = []
        for old_log, old_mass in active:
            for p, mass in law.items():
                log_e, probability = old_log + log_p_to_e(p, k), old_mass * mass
                if _reaches(log_e, log_boundary):
                    exit_mass += probability
                else:
                    next_active.append((log_e, probability))
        active = next_active
        survival = math.fsum(mass for _, mass in active)
        if survival == 0:
            raise ValueError("no active paths: conditional active mean is undefined")
        means.append(math.fsum(math.exp(log_e) * mass for log_e, mass in active) / survival)
        exits.append(exit_mass)
    return NullCalibration(k, threshold, limit, tuple(means), tuple(exits))


@dataclass(frozen=True)
class HypothesisView:
    name: str
    updates: int
    bin_history: tuple
    frozen: bool


@dataclass
class _Hypothesis:
    log_e: float = 0.
    updates: int = 0
    bins: list = field(default_factory=list)
    frozen: bool = False


@dataclass(frozen=True)
class Certificate:
    kind: str
    alpha_star: float
    epsilon: float
    delta: float
    bound: float
    conditional_on_no_null_exit: bool


class Disco:
    """Frozen e-processes with binary status-only hypothesis selection.

    ``run`` passes immutable views, never p-values, observations or exact
    wealth, to the selector. This is an API/data-flow contract, not a Python
    security sandbox: callers must not capture other channels of target data.
    The test provider owns query generation and valid statistical testing.
    """

    def __init__(self, *, kappa=.5, e_max=50., n_max=3, query_budget=30,
                 batch_size=1):
        self.kappa = _real(kappa, "kappa")
        self.e_max = _real(e_max, "e_max")
        self.n_max = _positive_int(n_max, "n_max")
        self.query_budget = _positive_int(query_budget, "query_budget")
        self.batch_size = _positive_int(batch_size, "batch_size")
        if not 0 < self.kappa < 1 or self.e_max <= 1:
            raise ValueError("kappa in (0,1), e_max > 1 required")
        self.queries_used = 0
        self._hypotheses = {}
        self._finished = False

    def selector_view(self):
        return tuple(HypothesisView(name, row.updates, tuple(row.bins), row.frozen)
                     for name, row in self._hypotheses.items())

    def observe(self, name, p_value, *, queries=None):
        """Low-level settlement; caller must choose name without hidden data."""
        if self._finished:
            raise ValueError("finished DISCO cannot consume more evidence")
        if not isinstance(name, str) or not name:
            raise ValueError("nonempty hypothesis name required")
        expected = min(self.batch_size, self.query_budget - self.queries_used)
        queries = expected if queries is None else _positive_int(queries, "queries")
        increment = log_p_to_e(p_value, self.kappa)
        if expected == 0 or queries != expected:
            raise ValueError("one complete batch (or the final remaining batch) required")
        row = self._hypotheses.get(name)
        if row is not None and row.frozen:
            raise ValueError("a frozen hypothesis cannot be queried again")
        if row is None:
            row = self._hypotheses[name] = _Hypothesis()
        row.log_e += increment
        row.updates += 1
        row.bins.append("H" if _reaches(row.log_e, math.log(self.e_max)) else "A")
        row.frozen = row.bins[-1] == "H" or row.updates == self.n_max
        self.queries_used += queries

    def run(self, selector, p_value_provider):
        """Algorithm 2 loop; provider(name, actual_batch) returns one p-value.

        A selector may return None to stop under budget. The provider must
        retain the calibrated null law even for a partial final batch.
        """
        if self._finished:
            raise ValueError("finished DISCO cannot run new queries")
        while self.queries_used < self.query_budget:
            name = selector(self.selector_view())
            if name is None:
                break
            if not isinstance(name, str) or not name:
                raise ValueError("selector must return a hypothesis name or None")
            old = self._hypotheses.get(name)
            if old is not None and old.frozen:
                raise ValueError("selector chose a frozen hypothesis")
            batch = min(self.batch_size, self.query_budget - self.queries_used)
            p = p_value_provider(name, batch)
            self.observe(name, p, queries=batch)
        return self.selector_view()

    def finish(self, calibration, *, alpha=.1, mode="pre_hoc"):
        """Theorem 1 unconditional bound OR Theorem 2 conditional certificate.

        The post-hoc delta is a null-exit *failure probability*, not part of
        the conditional FDR bound. It is not silently promoted into an
        unconditional level-alpha guarantee.
        """
        if self._finished:
            raise ValueError("finish is terminal")
        level = _real(alpha, "alpha")
        if not 0 < level <= 1 or mode not in ("pre_hoc", "post_hoc"):
            raise ValueError("alpha in (0,1] and a supported certificate mode required")
        if (not isinstance(calibration, NullCalibration)
                or (calibration.kappa, calibration.e_max, calibration.n_max)
                != (self.kappa, self.e_max, self.n_max)
                or not calibration.exact_path_enumeration):
            raise ValueError("matching exact null calibration required")
        count = len(self._hypotheses)
        upper = math.ceil(self.query_budget / self.batch_size)
        if mode == "pre_hoc":
            epsilon = calibration.epsilon
            delta = upper * calibration.exit_probability
            corrected = min(1., max(0., (level - delta) / epsilon))
            bound = corrected * epsilon + delta
        else:
            epsilon = (math.fsum(calibration.active_means[row.updates - 1]
                                for row in self._hypotheses.values()
                                if row.bins[-1] == "A") / count) if count else 0.
            delta = count * calibration.exit_probability
            corrected = min(1., level / epsilon) if epsilon else 1.
            bound = corrected * epsilon
        certificate = Certificate(mode, corrected, epsilon, delta, bound, mode == "post_hoc")
        logs = {name: row.log_e for name, row in self._hypotheses.items()}
        rejected = _ebh_from_logs(logs, corrected, count)
        self._finished = True
        return {"rejected": list(rejected), "hypotheses": count,
                "queries_used": self.queries_used, "certificate": asdict(certificate),
                "log_e_values": logs}


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU device required")
    calibration = exact_null_calibration(((.01, .01), (1., .99)), e_max=10., n_max=2)
    names = ["h0", "h1", "h2"]
    random.Random(seed).shuffle(names)
    cursor = {name: 0 for name in names}
    # Deliberately supplied p streams: not outputs from a real evaluated model.
    streams = {"h0": (.0001,), "h1": (1., 1.), "h2": (.04, .04)}

    def selector(views):
        known = {view.name: view for view in views}
        for name in names:
            if name not in known or not known[name].frozen:
                return name
        return None

    def provider(name, batch):
        assert batch == 1
        p = streams[name][cursor[name]]
        cursor[name] += 1
        return p

    state = Disco(e_max=10., n_max=2, query_budget=6)
    views = state.run(selector, provider)
    result = state.finish(calibration, mode="post_hoc")
    checks = {
        "selector_has_only_coarse_data": set(asdict(views[0])) == {"name", "updates", "bin_history", "frozen"},
        "freezes_on_exit_and_limit": all(view.frozen for view in views),
        "bounded_queries": result["queries_used"] == 5,
        "post_hoc_remains_conditional": result["certificate"]["conditional_on_no_null_exit"],
        "exact_null_calibration": math.isclose(calibration.exit_probability, .0001),
        "no_cuda_or_model_claim": REQUIRES_GPU_VALIDATION is False,
    }
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "controls": dict.fromkeys(checks, True),
            "metrics": {"hypotheses": result["hypotheses"], "queries_used": result["queries_used"],
                        "rejections": len(result["rejected"]),
                        "post_hoc_epsilon": result["certificate"]["epsilon"],
                        "null_exit_probability": calibration.exit_probability},
            "certificate": result["certificate"]}
