"""BRIAR v1 tree-credit components (Eqs.3,5--10), CPU diagnostics only.

Inputs are an already sampled tree and verifier rewards. This module does not
generate language, run RL, or claim that shared-parameter prefix behavior is
unchanged by a suffix-only loss. Node IDs are in parent-before-child order.
"""

import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _positive(value, name):
    if isinstance(value, (bool, np.bool_)) or not np.isscalar(value):
        raise ValueError(f"{name} must be a finite positive scalar")
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive scalar")
    return value


def _tree(parents, rewards, lengths):
    p = np.asarray(parents)
    r, length = np.asarray(rewards, dtype=float), np.asarray(lengths, dtype=float)
    if (p.ndim != 1 or p.dtype.kind not in "iu" or len(p) < 1 or p[0] != -1
            or np.any(p[1:] < 0) or np.any(p[1:] >= np.arange(1, len(p)))
            or r.shape != p.shape or length.shape != p.shape
            or not np.isfinite(length).all() or length[0] != 0
            or np.any(length[1:] <= 0)):
        raise ValueError("root -1, parent-before-child IDs and finite positive edge lengths required")
    children = [[] for _ in p]
    for c in range(1, len(p)):
        children[int(p[c])].append(c)
    leaves = np.array([not cs for cs in children])
    if (not np.isnan(r[~leaves]).all() or not np.isfinite(r[leaves]).all()
            or not np.isin(r[leaves], [0., 1.]).all()):
        raise ValueError("binary leaf rewards and NaN at all internal nodes required")
    counts = leaves.astype(int)
    successes = np.where(leaves, r, 0.)
    depth = np.zeros(len(p), dtype=int)
    for c in range(1, len(p)):
        depth[c] = depth[p[c]] + 1
    for c in range(len(p)-1, 0, -1):
        counts[p[c]] += counts[c]
        successes[p[c]] += successes[c]
    return p, r, length, children, leaves, counts, successes, depth


def frontier_scores(successes, counts, *, alpha=.5, kappa=.5):
    """Jeffreys Beta posterior and Eq.3; eligibility is returned separately."""
    s, m = np.asarray(successes), np.asarray(counts)
    alpha = _positive(alpha, "alpha")
    kappa = float(kappa)
    if (s.shape != m.shape or s.ndim != 1 or not np.isfinite(s).all()
            or not np.isfinite(m).all() or np.any(m < 1) or np.any(s < 0)
            or np.any(s > m) or np.any(s != np.floor(s)) or np.any(m != np.floor(m))
            or not math.isfinite(kappa) or kappa < 0):
        raise ValueError("integer success/count vectors and nonnegative kappa required")
    probability = (s+alpha)/(m+2*alpha)
    variance = probability*(1-probability)/(m+2*alpha+1)
    return {"probability": probability, "variance": variance,
            "priority": probability*(1-probability)+kappa*np.sqrt(variance),
            "unresolved": (s > 0) & (s < m)}


def smooth_tree(parents, rewards, lengths, *, sigma0_squared=2.2, eta=.4,
                psi_floor=.01, leaf_noise=.05, root_mean=.5, root_variance=100.,
                average_length=None, homoscedastic=False):
    """Exact two-pass Gaussian/LMMSE smoother for fixed empirical edge variances.

Eq.5 modulates variances by a martingale-inspired envelope. It does NOT enforce
the exact bounded-martingale inequality for arbitrary hyperparameters.
"""
    p, r, length, children, leaves, counts, successes, depth = _tree(parents, rewards, lengths)
    sigma0_squared = _positive(sigma0_squared, "sigma0_squared")
    psi_floor, leaf_noise = _positive(psi_floor, "psi_floor"), _positive(leaf_noise, "leaf_noise")
    root_variance = _positive(root_variance, "root_variance")
    eta, root_mean = float(eta), float(root_mean)
    if not math.isfinite(eta) or eta < 0 or not math.isfinite(root_mean):
        raise ValueError("finite root mean and nonnegative eta required")
    average_length = _positive(np.mean(length[1:]) if average_length is None and len(p) > 1
                               else 1. if average_length is None else average_length, "average_length")
    stats = frontier_scores(successes, counts)
    psi = stats["probability"]*(1-stats["probability"])+psi_floor
    edge_variance = np.zeros(len(p))
    if len(p) > 1:
        envelope = np.ones(len(p)-1) if homoscedastic else psi[p[1:]]
        edge_variance[1:] = sigma0_squared*envelope*(1+eta*length[1:]/average_length)
    precision, information = np.zeros(len(p)), np.zeros(len(p))
    precision[leaves], information[leaves] = 1/leaf_noise, r[leaves]/leaf_noise
    attenuation = np.ones(len(p))
    for c in range(len(p)-1, 0, -1):
        attenuation[c] = 1/(1+edge_variance[c]*precision[c])
        precision[p[c]] += attenuation[c]*precision[c]
        information[p[c]] += attenuation[c]*information[c]
    means, variances = np.zeros(len(p)), np.zeros(len(p))
    variances[0] = 1/(1/root_variance+precision[0])
    means[0] = variances[0]*(root_mean/root_variance+information[0])
    gain = 1-attenuation
    for c in range(1, len(p)):
        means[c] = attenuation[c]*means[p[c]]+gain[c]*information[c]/precision[c]
        variances[c] = attenuation[c]**2*variances[p[c]]+edge_variance[c]*attenuation[c]
    if not np.isfinite(means).all() or not np.isfinite(variances).all():
        raise ValueError("nonfinite smoothing output")
    advantages = np.zeros(len(p))
    advantages[1:] = means[1:]-means[p[1:]]
    return {"means": means, "variances": variances, "edge_advantages": advantages,
            "edge_variances": edge_variance, "gain": gain, "counts": counts,
            "successes": successes, "depth": depth, "leaves": leaves,
            "root_mean": root_mean, "root_variance": root_variance, "leaf_noise": leaf_noise}


def dense_reference(parents, rewards, lengths, smoothed):
    """Independent Eq.16 covariance solve, only for small numerical checks."""
    p, r, _, _, leaves, _, _, _ = _tree(parents, rewards, lengths)
    paths = np.zeros((len(p), len(p)))
    for c in range(1, len(p)):
        paths[c] = paths[p[c]]
        paths[c, c] = 1
    covariance = smoothed["root_variance"]+(
        paths*smoothed["edge_variances"]@paths.T)
    observed = np.flatnonzero(leaves)
    cross = covariance[:, observed]
    noise = covariance[np.ix_(observed, observed)]+smoothed["leaf_noise"]*np.eye(len(observed))
    means = smoothed["root_mean"]+cross@np.linalg.solve(noise, r[observed]-smoothed["root_mean"])
    variances = np.diag(covariance)-np.sum(cross*np.linalg.solve(noise, cross.T).T, axis=1)
    return means, variances


def absorbed_suffixes(parents, rewards, lengths, smoothed, *, threshold=.85,
                      confidence_z=1., min_spread=150., min_ratio=1.5, cap=2., epsilon=1e-8):
    """Minimal absorbed frontier and Eq.10, clipping THEN exact recentering.

Returned suffixes identify only post-frontier edges. No loss or gradient is
assigned to prefix tokens; this is not a shared-parameter invariance theorem.
"""
    p, _, length, _, leaves, counts, successes, _ = _tree(parents, rewards, lengths)
    threshold, confidence_z, min_spread = map(float, (threshold, confidence_z, min_spread))
    if (not 0 <= threshold <= 1 or not math.isfinite(confidence_z) or confidence_z < 0
            or not math.isfinite(min_spread) or min_spread < 0):
        raise ValueError("valid confidence and suffix thresholds required")
    min_ratio, cap, epsilon = (_positive(min_ratio, "min_ratio"), _positive(cap, "cap"),
                               _positive(epsilon, "epsilon"))
    if min_ratio < 1:
        raise ValueError("min_ratio must be at least one")
    means, variances = smoothed["means"], smoothed["variances"]
    if means.shape != p.shape or variances.shape != p.shape or np.any(variances < 0):
        raise ValueError("aligned nonnegative posterior variances required")
    qualified = (~leaves) & (successes == counts) & (counts >= 2)
    qualified &= means-confidence_z*np.sqrt(variances) >= threshold
    minimal = qualified.copy()
    minimal[1:] &= ~qualified[p[1:]]
    result = []
    for b in np.flatnonzero(minimal):
        suffix_paths, suffix_lengths, descendant_leaves = [], [], []
        for leaf in np.flatnonzero(leaves):
            node, path = int(leaf), []
            while node != b and node != 0:
                path.append(node)
                node = int(p[node])
            if node == b and path:
                path.reverse()
                suffix_paths.append(path)
                suffix_lengths.append(float(length[path].sum()))
                descendant_leaves.append(int(leaf))
        values = np.array(suffix_lengths)
        if len(values) < 2 or np.ptp(values) < min_spread or values.max()/values.min() < min_ratio:
            continue
        log_lengths = np.log(values)
        advantage = np.clip((log_lengths.mean()-log_lengths)/(log_lengths.std()+epsilon), -cap, cap)
        advantage -= advantage.mean()
        result.append({"frontier": int(b), "leaf_ids": descendant_leaves,
                       "edge_paths": suffix_paths, "lengths": values, "advantages": advantage})
    return result


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    rng = np.random.default_rng(seed)
    parents = np.array([-1]+[(i-1)//2 for i in range(1, 31)])
    rewards = np.r_[np.full(15, np.nan), rng.integers(0, 2, 16)]
    lengths = np.r_[0., rng.integers(160, 481, 30)]
    smoothed = smooth_tree(parents, rewards, lengths)
    reference_mean, reference_var = dense_reference(parents, rewards, lengths, smoothed)
    mean_error = float(np.max(np.abs(reference_mean-smoothed["means"])))
    var_error = float(np.max(np.abs(reference_var-smoothed["variances"])))
    # A separate deterministic tree tests absorbed suffix construction; it is
    # not a benchmark and its terminal rewards are never shown to a policy.
    p2 = np.array([-1, 0, 0]+[1]*64+[2]*2)
    r2 = np.r_[np.full(3, np.nan), np.ones(64), 0., 1.]
    l2 = np.r_[0., 200., 200., np.linspace(160, 600, 64), 250., 300.]
    s2 = smooth_tree(p2, r2, l2)
    suffixes = absorbed_suffixes(p2, r2, l2, s2)
    suffix_error = max([abs(float(row["advantages"].sum())) for row in suffixes], default=0.)
    frontier = frontier_scores([0, 3, 6], [6, 6, 6])
    uniform = smooth_tree([-1, 0, 0], [np.nan, 1., 1.], [0., 200., 300.])
    checks = {
        "rts_matches_dense_posterior_mean": mean_error < 1e-10,
        "rts_matches_dense_posterior_variance": var_error < 1e-10,
        "posterior_variances_are_positive": bool(np.all(smoothed["variances"] > 0)),
        "mixed_frontier_beats_resolved_nodes": bool(frontier["priority"][1] > frontier["priority"][[0, 2]].max()),
        "unanimous_root_is_ineligible": not bool(frontier_scores(uniform["successes"], uniform["counts"])["unresolved"][0]),
        "minimal_absorbed_branch_is_detected": bool(len(suffixes) == 1 and suffixes[0]["frontier"] == 1),
        "suffix_advantages_are_zero_sum": suffix_error < 1e-12,
        "suffix_paths_exclude_prefix_edges": bool(suffixes and all(1 not in path for path in suffixes[0]["edge_paths"])),
    }
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism",
            "diagnostic_only": True, "training_executed": False, "checks": checks,
            "metrics": {"dense_mean_max_abs_error": mean_error, "dense_variance_max_abs_error": var_error,
                        "suffix_advantage_sum_abs": float(suffix_error), "nodes": len(parents)}}
