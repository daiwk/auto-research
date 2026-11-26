"""FEAST v1 CPU allocation components, not an LLM/GRPO training system.

Policy hidden vectors are explicit inputs, never replaced by task labels.
Persistent atomic histories survive policy-adaptive PCA/GMM regrouping.
The diagnostic uses named synthetic arrays, not model-capability evidence.
"""

import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _vectors(value):
    x = np.asarray(value, dtype=float)
    if x.ndim != 2 or min(x.shape) < 1 or not np.isfinite(x).all():
        raise ValueError("nonempty finite vector matrix required")
    return x


def _integer(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def kmeans(vectors, clusters, *, seed=42, restarts=10, max_iterations=300, tolerance=1e-4):
    """Euclidean K-means++, Lloyd iterations, ten independent restarts."""
    x = _vectors(vectors)
    _integer(clusters, "clusters")
    _integer(seed, "seed", 0)
    _integer(restarts, "restarts")
    _integer(max_iterations, "max_iterations")
    if clusters > len(x) or len(np.unique(x, axis=0)) < clusters or not 0 < tolerance < math.inf:
        raise ValueError("enough distinct vectors and a finite positive tolerance required")
    rng, best = np.random.default_rng(seed), None
    for _ in range(restarts):
        centers = [x[rng.integers(len(x))].copy()]
        while len(centers) < clusters:
            d = ((x[:, None]-np.array(centers))**2).sum(axis=2).min(axis=1)
            centers.append(x[rng.choice(len(x), p=d/d.sum())].copy())
        centers = np.array(centers)
        for _ in range(max_iterations):
            d = ((x[:, None]-centers)**2).sum(axis=2)
            labels = np.argmin(d, axis=1)
            # Empty centroids are deterministically reseeded at farthest points.
            new = centers.copy()
            claimed = set()
            for k in range(clusters):
                if np.any(labels == k):
                    new[k] = x[labels == k].mean(axis=0)
                else:
                    order = np.argsort(-d.min(axis=1), kind="stable")
                    index = next(int(i) for i in order if int(i) not in claimed)
                    claimed.add(index)
                    new[k] = x[index]
            shift = float(np.sum((new-centers)**2))
            centers = new
            if shift <= tolerance*float(x.var(axis=0).mean()):
                break
        d = ((x[:, None]-centers)**2).sum(axis=2)
        labels = np.argmin(d, axis=1)
        inertia = float(d[np.arange(len(x)), labels].sum())
        if np.unique(labels).size == clusters and (best is None or inertia < best[0]):
            best = inertia, labels.copy(), centers.copy()
    if best is None:
        raise ValueError("K-means could not produce nonempty atomic units")
    return best[1], best[2]


def _logsumexp(x):
    maximum = x.max(axis=1, keepdims=True)
    return maximum+np.log(np.exp(x-maximum).sum(axis=1, keepdims=True))


def _gaussian_mixture(x, components, seed):
    labels, means = kmeans(x, components, seed=seed)
    d, n = x.shape[1], len(x)
    variances = np.array([x[labels == k].var(axis=0)+1e-6 for k in range(components)])
    weights = np.bincount(labels, minlength=components)/n
    previous = -math.inf
    for _ in range(100):
        logp = np.log(weights)[None, :]-.5*(
            d*np.log(2*np.pi)+np.log(variances).sum(axis=1)[None, :]
            +((x[:, None, :]-means[None, :, :])**2/variances[None, :, :]).sum(axis=2))
        normalizer = _logsumexp(logp)
        responsibilities = np.exp(logp-normalizer)
        log_likelihood = float(normalizer.sum())
        if abs(log_likelihood-previous)/n < 1e-3:
            break
        previous = log_likelihood
        mass = responsibilities.sum(axis=0)+10*np.finfo(float).eps
        weights = mass/mass.sum()
        means = responsibilities.T@x/mass[:, None]
        variances = (responsibilities.T@(x*x)/mass[:, None]-means*means).clip(0)+1e-6
    # Evaluate final fitted likelihood (BIC is deliberately computed BEFORE repair).
    logp = np.log(weights)[None, :]-.5*(d*np.log(2*np.pi)+np.log(variances).sum(axis=1)[None, :]
            +((x[:, None, :]-means[None, :, :])**2/variances[None, :, :]).sum(axis=2))
    log_responsibility = logp-_logsumexp(logp)
    parameters = components*(2*d)+components-1
    bic = -2*float(_logsumexp(logp).sum())+parameters*np.log(n)
    return log_responsibility, float(bic)


def regroup(atomic_vectors, smoothed_trend, *, seed=42, components=range(8, 17), semantic_dimensions=8):
    """Appendix A.2.1: centered PCA/std + signed trend, diagonal GMM/BIC.

Repair always moves the least log-posterior-cost atom from a donor with >2
members. This deterministic repair ordering is local: v1 specifies posterior-
based repair and minimum size, but does not specify its tie/order convention.
"""
    x, trend = _vectors(atomic_vectors), np.asarray(smoothed_trend, dtype=float)
    _integer(seed, "seed", 0)
    _integer(semantic_dimensions, "semantic_dimensions")
    if trend.shape != (len(x),) or not np.isfinite(trend).all() or np.any(np.abs(trend) > 1):
        raise ValueError("one finite smoothed trend in [-1,1] per atom required")
    centered = x-x.mean(axis=0)
    _, _, axes = np.linalg.svd(centered, full_matrices=False)
    projected = centered@axes[:min(semantic_dimensions, len(axes))].T
    scale = projected.std(axis=0)  # Population empirical std; zero PCA coordinates stay zero.
    semantic = projected/np.where(scale > 1e-12, scale, 1.)
    features = np.column_stack((semantic, trend))
    best = None
    candidates = list(components)
    if not candidates:
        raise ValueError("at least one component count required")
    for k in candidates:
        _integer(k, "component count")
        if 2*k > len(x):
            continue
        log_r, bic = _gaussian_mixture(features, k, seed+k)
        labels = np.argmax(log_r, axis=1)
        for target in range(k):
            while np.count_nonzero(labels == target) < 2:
                counts = np.bincount(labels, minlength=k)
                movable = np.flatnonzero(counts[labels] > 2)
                if not len(movable):
                    raise ValueError("infeasible minimum-two-atom repair")
                costs = log_r[movable, labels[movable]]-log_r[movable, target]
                labels[movable[np.argmin(costs)]] = target
        if best is None or bic < best[0]:
            best = bic, labels.copy(), features.copy()
    if best is None:
        raise ValueError("no feasible mixture with at least two atoms per group")
    return {"groups": best[1], "features": best[2], "bic_before_repair": best[0]}


class FeastScheduler:
    """Persistent atomic state, lifetime-unseen capacity and stable prompt cycles."""

    def __init__(self, prompt_vectors, *, atoms=64, seed=42):
        self.vectors = _vectors(prompt_vectors).copy()
        self.assignment, _ = kmeans(self.vectors, atoms, seed=seed)
        self.atoms, self.rng = atoms, np.random.default_rng(seed)
        self.groups = np.arange(atoms)  # Must regroup before a normal FEAST draw.
        self.m, self.u, self.trend, self.slow_trend, self.shortfall = [np.zeros(atoms) for _ in range(5)]
        self.observed = np.zeros(atoms, dtype=bool)
        self.unseen = np.ones(len(self.vectors), dtype=bool)
        self.cycles = [np.flatnonzero(self.assignment == i).tolist() for i in range(atoms)]
        self.cursor = np.zeros(atoms, dtype=int)
        self.equal_share = None

    def regroup(self, current_prompt_vectors, **kwargs):
        vectors = _vectors(current_prompt_vectors)
        if vectors.shape != self.vectors.shape:
            raise ValueError("current policy vectors must align with the unchanged prompt pool")
        centroids = np.array([vectors[self.assignment == i].mean(axis=0) for i in range(self.atoms)])
        result = regroup(centroids, self.slow_trend, **kwargs)
        self.groups = result["groups"].copy()
        return result

    def priorities(self):
        if self.equal_share is None:
            shortfall = np.zeros(self.atoms)
        else:
            shortfall = np.minimum(1., self.shortfall/(10*self.equal_share))
        phi = np.exp(-.5*((self.m-.5)/.22)**2)
        psi = 1+.20/(1+np.exp((self.m-.5)/.05))
        return .05+self.u*phi*psi*(1+.50*np.abs(self.trend))+.05*shortfall

    def group_weights(self, *, prompts_per_group=32, temperature=1.):
        _integer(prompts_per_group, "prompts_per_group")
        if not math.isfinite(temperature) or temperature <= 0:
            raise ValueError("positive finite temperature required")
        priority = self.priorities()
        unseen = np.bincount(self.assignment, weights=self.unseen, minlength=self.atoms)
        groups, weights = np.unique(self.groups), []
        for c in groups:
            members = self.groups == c
            capacity = unseen[members].sum()
            mean = (np.dot(unseen[members], priority[members])/capacity if capacity else priority[members].mean())
            weights.append((.05+min(1., capacity/prompts_per_group)*(mean-.05))**(1/temperature))
        return groups, np.array(weights)

    def plan(self, *, selected_groups=4, prompts_per_group=32, temperature=1.):
        """Use ONLY historical observations, then reserve each selected group's slots."""
        _integer(selected_groups, "selected_groups")
        groups, weights = self.group_weights(prompts_per_group=prompts_per_group, temperature=temperature)
        if selected_groups > len(groups):
            raise ValueError("not enough groups")
        selected = self.rng.choice(groups, size=selected_groups, replace=False, p=weights/weights.sum())
        priority, result = self.priorities(), {}
        for c in selected:
            members = np.flatnonzero(self.groups == c)
            if np.isin(self.assignment, members).sum() < prompts_per_group:
                raise ValueError("selected cluster has insufficient unique prompt capacity")
            chosen = []
            for _ in range(prompts_per_group):
                unseen = np.bincount(self.assignment, weights=self.unseen, minlength=self.atoms)[members]
                if unseen.sum():
                    capacity = unseen
                else:
                    capacity = np.array([np.count_nonzero(self.assignment == i)-sum(self.assignment[j] == i for j in chosen)
                                         for i in members])
                mass = priority[members]*capacity
                atom = int(self.rng.choice(members, p=mass/mass.sum()))
                cycle = self.cycles[atom]
                while cycle[self.cursor[atom] % len(cycle)] in chosen:
                    self.cursor[atom] += 1
                prompt = cycle[self.cursor[atom] % len(cycle)]
                self.cursor[atom] += 1
                self.unseen[prompt] = False
                chosen.append(prompt)
            result[int(c)] = chosen
        return result

    def observe(self, rewards_by_prompt, *, total_budget):
        """Pilot-equal EMAs; signal-exposure-normalized trend; ALL rollout shortfalls."""
        _integer(total_budget, "total_budget")
        if not rewards_by_prompt:
            raise ValueError("nonempty observed batch required")
        generated = np.zeros(self.atoms)
        samples = [[] for _ in range(self.atoms)]
        for prompt, values in rewards_by_prompt.items():
            if type(prompt) is not int or not 0 <= prompt < len(self.assignment):
                raise ValueError("prompt IDs must belong to the pool")
            values = np.asarray(values, dtype=float)
            if values.ndim != 1 or len(values) < 2 or not np.isfinite(values).all() or np.any((values < 0) | (values > 1)):
                raise ValueError("at least two raw rewards in [0,1] per prompt required")
            atom = self.assignment[prompt]
            generated[atom] += len(values)
            samples[atom].append(values)
        if generated.sum() != total_budget:
            raise ValueError("budget must count every generated trajectory, including zero-signal groups")
        for atom, batches in enumerate(samples):
            if not batches:
                continue
            attainment = float(np.mean([r[:2].mean() for r in batches]))
            disagreement = float(np.mean([(r[0]-r[1])**2 for r in batches]))
            signal_count = sum(len(r) for r in batches if np.var(r) > 0)
            old = self.m[atom]
            if not self.observed[atom]:
                self.m[atom], self.u[atom], trend = attainment, disagreement, 0.
            else:
                self.m[atom] = .9*old+.1*attainment
                self.u[atom] = .9*self.u[atom]+.1*disagreement
                trend = float(np.clip((self.m[atom]-old)/(signal_count/8), -1, 1)) if signal_count else 0.
            self.trend[atom] = trend
            self.slow_trend[atom] = .7*self.slow_trend[atom]+.3*trend
            self.observed[atom] = True
        self.equal_share = total_budget/self.atoms
        self.shortfall = np.maximum(0., self.shortfall+self.equal_share-generated)


def progressive_rollouts(plan, sample_rewards, *, increments=(2, 4, 16)):
    """Generate real callback samples; promote by cumulative raw-reward variance.

The caller must hold its policy fixed across all rounds. Ties retain original
prompt order. Reservations cannot move between clusters. No refill is used.
"""
    if len(increments) != 3 or increments[0] != 2 or any(type(n) is not int or n < 1 for n in increments):
        raise ValueError("three positive increments with two pilot samples required")
    all_prompts = [p for prompts in plan.values() for p in prompts]
    if not plan or len(all_prompts) != len(set(all_prompts)):
        raise ValueError("nonempty plan with globally unique prompt IDs required")
    output, spent = {}, {}
    for group, prompts in plan.items():
        if len(prompts) < 4 or len(prompts) % 4:
            raise ValueError("prompt count must be a positive multiple of four")
        active = list(prompts)
        for stage, additional in enumerate(increments):
            for prompt in active:
                values = np.asarray(sample_rewards(prompt, additional), dtype=float)
                if values.shape != (additional,) or not np.isfinite(values).all() or np.any((values < 0) | (values > 1)):
                    raise ValueError("sampler must return exactly n finite raw rewards in [0,1]")
                output.setdefault(prompt, []).extend(values.tolist())
            if stage < 2:
                variance = np.array([np.var(output[p]) for p in active])
                order = np.argsort(-variance, kind="stable")[:len(active)//2]
                active = [active[i] for i in order]
        spent[group] = sum(len(output[p]) for p in prompts)
    return {"rewards": output, "spent_per_group": spent,
            "total_rollouts": sum(spent.values()),
            "signal_prompts": [p for p, rewards in output.items() if np.var(rewards) > 0]}


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    rng = np.random.default_rng(seed)
    vectors = rng.normal(size=(256, 12))
    scheduler = FeastScheduler(vectors, atoms=16, seed=seed)
    grouping = scheduler.regroup(vectors, seed=seed, components=range(4, 7))
    assignment = scheduler.assignment.copy()
    plan = scheduler.plan(selected_groups=2, prompts_per_group=8)
    # Explicit stochastic callback diagnostic, not task labels or a language model.
    output = progressive_rollouts(plan, lambda prompt, n: rng.binomial(1, .2+.6*(prompt % 7)/6, n))
    scheduler.observe(output["rewards"], total_budget=output["total_rollouts"])
    before = [x.copy() for x in (scheduler.m, scheduler.u, scheduler.trend, scheduler.shortfall)]
    scheduler.regroup(vectors+.1*rng.normal(size=vectors.shape), seed=seed+1, components=range(4, 7))
    all_spent = list(output["spent_per_group"].values())
    checks = {
        "mixtures_repaired_to_two_atoms": bool(np.bincount(grouping["groups"]).min() >= 2),
        "atomic_assignment_is_persistent": bool(np.array_equal(assignment, scheduler.assignment)),
        "regrouping_preserves_all_history": bool(all(np.array_equal(a, b) for a, b in zip(before, (scheduler.m, scheduler.u, scheduler.trend, scheduler.shortfall)))),
        "exact_reserved_rollout_budget": bool(all(n == 64 for n in all_spent) and output["total_rollouts"] == 128),
        "all_generated_samples_in_history": bool(sum(map(len, output["rewards"].values())) == 128),
        "progressive_group_sizes_are_two_six_twenty_two": bool(sorted(map(len, output["rewards"].values())) == [2]*8+[6]*4+[22]*4),
        "positive_bounded_atomic_priorities": bool(np.all((scheduler.priorities() >= .05) & (scheduler.priorities() <= 1.90))),
        "shortfalls_count_zero_signal_exposure": bool(np.all(scheduler.shortfall >= 0)),
    }
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism",
            "diagnostic_only": True, "training_executed": False, "checks": checks,
            "metrics": {"generated_rollouts": output["total_rollouts"], "selected_groups": len(plan),
                        "atoms": scheduler.atoms, "mixture_bic_before_repair": grouping["bic_before_repair"],
                        "maximum_shortfall": float(scheduler.shortfall.max())}}
