"""StoryScope Appendix D core-feature gate and prompt-block bootstrap.

Actual semantic features, XGBoost training and bootstrap/null-label SHAP
statistics must be supplied externally. Fingerprint thresholds are not fully
specified by v1 Appendix D and are not guessed here.
"""
from __future__ import annotations

import numpy as np

REQUIRES_GPU_VALIDATION = False


def prompt_bootstrap(prompt_ids, *, seed: int, iterations: int = 50):
    ids = tuple(prompt_ids)
    if not ids or any(not isinstance(x, str) or not x for x in ids) or type(seed) is not int or type(iterations) is not int or iterations <= 0:
        raise ValueError("nonempty prompt IDs, integer seed and positive iterations required")
    groups = tuple(dict.fromkeys(ids))
    members = {group: [i for i, value in enumerate(ids) if value == group] for group in groups}
    rng = np.random.default_rng(seed)
    return tuple(tuple(i for group in rng.choice(groups, size=len(groups), replace=True) for i in members[group])
                 for _ in range(iterations))


def select_core_features(mean_abs_shap, stability, top25, null95, permutation_p, human_mean, ai_means):
    """Exact conjunctive thresholds from fixed v1 Appendix D.

    Statistics refer to encoded features. Values and null/permutation estimates
    come from external prompt-block-resampled classifiers, not story-level IID
    pseudo-replicates. The source defines important with strict > top quartile.
    """
    arrays = [np.asarray(x, dtype=np.float64) for x in (mean_abs_shap, stability, top25, null95, permutation_p, human_mean)]
    ai = np.asarray(ai_means, dtype=np.float64)
    if any(x.ndim != 1 or not len(x) or x.shape != arrays[0].shape or not np.isfinite(x).all() for x in arrays):
        raise ValueError("same-sized nonempty finite feature-statistic vectors required")
    if ai.shape != (len(arrays[0]), 5) or not np.isfinite(ai).all():
        raise ValueError("one observed mean for each of five AI sources per encoded feature required")
    shap, stab, top, null, p, human = arrays
    if (shap < 0).any() or (null < 0).any() or any(((x < 0) | (x > 1)).any() for x in (stab, top, p)):
        raise ValueError("nonnegative SHAP/null and probability-valued stability/top25/p required")
    important = shap > np.quantile(shap, .75)
    stable_cut = float(np.median(stab[important])) if important.any() else float("inf")
    null_significant = (shap > null) & (p <= .10)
    stable_important = important & (stab >= stable_cut) & null_significant
    gap = ai.mean(axis=1) - human
    core = stable_important & (stab >= .55) & (top >= .60) & (np.abs(gap) >= .20) & (np.ptp(ai, axis=1) <= .35)
    return {"important": important, "stable_important": stable_important, "core": core,
            "direction": np.where(core, np.where(gap > 0, "AI-leaning", "human-leaning"), "not-core"),
            "importance_threshold": float(np.quantile(shap, .75)), "stability_threshold": stable_cut}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("StoryScope gate/bootstrap is CPU-only")
    shap = [0., .1, .2, .3, .4, .5, 2., 3.]
    stats = select_core_features(shap, [.8]*8, [.7]*8, [.1]*8, [.05]*8, [0.]*8,
                                 [[.1]*5]*6 + [[.4]*5, [.8, .8, .8, .8, 0.]])
    draws = prompt_bootstrap(["p1", "p1", "p2", "p2", "p3", "p3"], seed=seed)
    intact = all(all(draw.count(i) == draw.count(i+1) for i in (0, 2, 4)) for draw in draws)
    checks = {"all_core_conditions_required": stats["core"].tolist() == [False]*6+[True, False],
              "cross_model_spread_rejects_source_only_signal": not bool(stats["core"][-1]),
              "prompt_blocks_not_individual_stories": intact,
              "fifty_bootstrap_draws": len(draws) == 50,
              "signed_role": stats["direction"][6] == "AI-leaning"}
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"selected_core_features": int(stats["core"].sum()), "bootstrap_iterations": len(draws),
                        "pretrained_model_calls": 0, "trained_classifiers": 0}, "checks": checks}
