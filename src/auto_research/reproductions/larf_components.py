"""LARF v1 CPU reward and objective components, not the industrial pipeline.

Dynamic attribute weights and rule-checker outcomes must be supplied. The
paper does not specify enough to reconstruct those systems. No evaluated
agent receives labels here: these are training-loss/reward diagnostics.
"""

import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _finite(value, rank):
    x = np.asarray(value, dtype=np.float64)
    if x.ndim != rank or not x.size or not np.isfinite(x).all():
        raise ValueError("nonempty finite array of the required rank expected")
    return x


def _labels(value, shape=None):
    x = np.asarray(value)
    if x.dtype.kind not in "iu" or not x.size or np.any(x < 0) or np.any(x > 5) or (shape and x.shape != shape):
        raise ValueError("integer ordinal labels in 0..5 required")
    return x.astype(np.int64)


def attribute_reward(gold, predicted, *, weights):
    """Eq.2; caller supplies omega_k(t), with no invented schedule."""
    y = _labels(gold)
    pred = _labels(predicted, y.shape)
    w = _finite(weights, 1)
    if y.ndim != 2 or y.shape[1] != 5 or w.shape != (5,) or np.any(w < 0):
        raise ValueError("five label dimensions and nonnegative supplied weights required")
    return (np.exp(-np.abs(y-pred))*w).sum(axis=1)


def listwise_reward(gold, predicted, *, mean_group_size):
    """Eqs.3--5 for ONE query's documents, excluding equal-gold pairs.

    A group with no comparable pairs has undefined c_d in fixed v1 and is
    rejected, not silently scored as random or perfect.
    """
    y = _labels(gold)
    pred = _labels(predicted, y.shape)
    if (y.ndim != 1 or len(y) < 2 or type(mean_group_size) not in (int, float)
            or not math.isfinite(mean_group_size) or mean_group_size <= 1):
        raise ValueError("query group of at least two documents and mean_group_size>1 required")
    truth = np.sign(y[:, None]-y[None, :])
    guessed = np.sign(pred[:, None]-pred[None, :])
    comparable = truth != 0
    denominators = comparable.sum(axis=1)
    if np.any(denominators == 0):
        raise ValueError("no unequal-gold pairs: fixed-v1 concordance is undefined")
    positive = ((guessed == truth) & comparable).sum(axis=1)
    ties = ((guessed == 0) & comparable).sum(axis=1)
    concordance = (positive+.5*ties)/denominators
    confidence = min(1., math.sqrt((len(y)-1)/(mean_group_size-1)))
    return {"reward": confidence*(2*concordance-1), "concordance": concordance,
            "group_weight": confidence, "comparable_pairs_per_document": denominators}


def combined_reward(gold, predicted, *, weights, rule_consistent, mean_group_size):
    """Eq.7, receiving (not approximating) the external Eq.6 checker."""
    att = attribute_reward(gold, predicted, weights=weights)
    rule = np.asarray(rule_consistent)
    if rule.shape != att.shape or rule.dtype != np.bool_:
        raise ValueError("one externally checked boolean per document required")
    ranking = listwise_reward(np.asarray(gold)[:, -1], np.asarray(predicted)[:, -1],
                              mean_group_size=mean_group_size)["reward"]
    rule_reward = np.where(rule, 1., -1.)
    return {"attribute": att, "listwise": ranking, "rule": rule_reward,
            "total": att+ranking+rule_reward}


def terminal_margin(logits, gold, terminal_mask, *, digit_indices, margin=1.):
    """Eqs.8--10; only one marked position and an integer 0..5 gold are valid.

    The full-logit gradient is zero outside the six digits at the unique
    terminal position. At competitor ties choose the first digit; at the
    hinge boundary choose zero, both explicit local subgradient conventions.
    """
    z = _finite(logits, 3)
    y = np.asarray(gold)
    marked = np.asarray(terminal_mask)
    digits = np.asarray(digit_indices)
    if (y.shape != (len(z),) or y.dtype.kind not in "iu" or marked.shape != z.shape[:2]
            or marked.dtype != np.bool_ or digits.shape != (6,) or digits.dtype.kind not in "iu"
            or len(set(digits.tolist())) != 6 or np.any(digits < 0) or np.any(digits >= z.shape[-1])
            or type(margin) not in (int, float) or not math.isfinite(margin) or margin <= 0):
        raise ValueError("aligned labels/terminal mask, six unique digit indices and positive margin required")
    valid = (marked.sum(axis=1) == 1) & (y >= 0) & (y < 6)
    if not valid.any():
        raise ValueError("empty valid terminal-label subset is unspecified by Eq.10")
    gradient = np.zeros_like(z)
    losses = []
    for i in np.flatnonzero(valid):
        t = int(np.flatnonzero(marked[i])[0])
        scores = z[i, t, digits]
        wrong = scores.copy()
        wrong[y[i]] = -np.inf
        competitor = int(wrong.argmax())
        hinge = max(0., margin-float(scores[y[i]]-scores[competitor]))
        losses.append(hinge)
        if hinge > 0:
            gradient[i, t, digits[y[i]]] = -1./valid.sum()
            gradient[i, t, digits[competitor]] = 1./valid.sum()
    return {"loss": float(np.mean(losses)), "gradient": gradient, "valid": valid}


def _cross_entropy(logits, targets, mask):
    shifted = logits-logits.max(axis=-1, keepdims=True)
    lp = shifted-np.log(np.exp(shifted).sum(axis=-1, keepdims=True))
    probability = np.exp(lp)
    flat_p = probability.reshape(-1, probability.shape[-1])
    flat_y, flat_m = targets.ravel(), mask.ravel()
    ix = np.arange(len(flat_p))
    loss = -float(lp.reshape(flat_p.shape)[ix[flat_m], flat_y[flat_m]].mean())
    gradient = flat_p.copy()
    gradient[ix, flat_y] -= 1.
    gradient *= flat_m[:, None]/flat_m.sum()
    return loss, gradient.reshape(logits.shape)


def dual_head_objective(classification_logits, labels, reasoning_logits, reasoning_targets,
                        reasoning_mask, *, classification_weight=1., generation_weight=1.):
    """Eq.12 on supplied logits, not a reconstructed backbone/MLP or student.

    Sum five independently batch-mean classification CEs; masked LM CE is
    mean over valid rationale tokens. The LM reduction is a stated local
    convention, as Eq.12 does not spell it out. Both gradients are returned.
    """
    cls, gen = _finite(classification_logits, 3), _finite(reasoning_logits, 3)
    y = _labels(labels, cls.shape[:2])
    target, mask = np.asarray(reasoning_targets), np.asarray(reasoning_mask)
    weights = (classification_weight, generation_weight)
    if (cls.shape[1:] != (5, 6) or gen.shape[0] != cls.shape[0] or target.shape != gen.shape[:2]
            or target.dtype.kind not in "iu" or np.any(target < 0) or np.any(target >= gen.shape[-1])
            or mask.shape != target.shape or mask.dtype != np.bool_ or not mask.any()
            or any(type(w) not in (int, float) or not math.isfinite(w) or w < 0 for w in weights)):
        raise ValueError("five six-class heads, aligned rationale tokens/mask and nonnegative weights required")
    cls_loss, cls_grad = _cross_entropy(cls, y, np.ones_like(y, dtype=bool))
    cls_loss, cls_grad = 5*cls_loss, 5*cls_grad
    gen_loss, gen_grad = _cross_entropy(gen, target, mask)
    return {"loss": classification_weight*cls_loss+generation_weight*gen_loss,
            "classification_loss": cls_loss, "generation_loss": gen_loss,
            "classification_gradient": classification_weight*cls_grad,
            "generation_gradient": generation_weight*gen_grad}


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    rng = np.random.default_rng(seed)
    gold = np.tile(np.array([0, 2, 5])[:, None], (1, 5))
    perfect = listwise_reward(gold[:, -1], gold[:, -1], mean_group_size=3.)
    inverted = listwise_reward(gold[:, -1], gold[::-1, -1], mean_group_size=3.)
    ties = listwise_reward(gold[:, -1], [2, 2, 2], mean_group_size=3.)
    z = rng.normal(size=(3, 2, 9))
    marked = np.array([[False, True], [True, False], [True, True]])
    terminal = terminal_margin(z, [0, 2, 5], marked, digit_indices=[0, 1, 2, 3, 4, 5])
    numerical = np.zeros_like(z)
    step = 1e-6
    for coordinate in np.ndindex(z.shape):
        change = np.zeros_like(z)
        change[coordinate] = step
        numerical[coordinate] = (terminal_margin(z+change, [0, 2, 5], marked, digit_indices=list(range(6)))["loss"]-
                                 terminal_margin(z-change, [0, 2, 5], marked, digit_indices=list(range(6)))["loss"])/(2*step)
    err = float(np.max(np.abs(numerical-terminal["gradient"])))
    cls, gen = rng.normal(size=(2, 5, 6)), rng.normal(size=(2, 3, 7))
    labels = rng.integers(0, 6, size=(2, 5))
    target = rng.integers(0, 7, size=(2, 3))
    mask = np.array([[True, True, False], [True, False, False]])
    joint = dual_head_objective(cls, labels, gen, target, mask)
    checks = {"perfect_order_has_positive_one_reward": bool(np.allclose(perfect["reward"], 1.)),
              "inverted_order_has_negative_one_reward": bool(np.allclose(inverted["reward"], -1.)),
              "predicted_ties_are_zero_centered": bool(np.allclose(ties["reward"], 0.)),
              "margin_gradient_matches_finite_difference": err < 1e-8,
              "ambiguous_terminal_positions_are_excluded": bool(np.all(terminal["gradient"][2] == 0)),
              "non_digit_logits_receive_no_margin_gradient": bool(np.all(terminal["gradient"][:, :, 6:] == 0)),
              "both_joint_training_heads_receive_gradient": bool(np.any(joint["classification_gradient"]) and np.any(joint["generation_gradient"])),
              "masked_reasoning_tokens_have_zero_gradient": bool(np.all(joint["generation_gradient"][~mask] == 0))}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"margin_finite_difference_max_abs_error": err,
            "documents": 3, "classification_heads": 5, "ordinal_classes": 6}, "training_executed": False}
