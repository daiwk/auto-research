"""SHPO v1 DPO-plus-antisymmetric-plane objective and analytic CPU gradients.

Explicit response hidden states and sequence log probabilities are inputs.
Gradients are returned for hidden states, projection, planes and logprobs;
no language model, QLoRA trainer, GPT judge or graph-level Hodge solver exists.
"""

import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _array(value, ndim):
    result = np.asarray(value, dtype=np.float64)
    if result.ndim != ndim or not result.size or not np.isfinite(result).all():
        raise ValueError("nonempty finite array of required rank expected")
    return result


def _real(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("finite real number required")
    return float(value)


def mean_pool_response(token_states, response_mask):
    """SectionIII-D: last-layer hidden states, response tokens only."""
    states = _array(token_states, 3)
    mask = np.asarray(response_mask)
    if mask.dtype != np.bool_ or mask.shape != states.shape[:2] or not mask.any(axis=1).all():
        raise ValueError("boolean response masks with at least one token per response required")
    with np.errstate(over="raise", invalid="raise"):
        try:
            result = np.where(mask[:, :, None], states, 0.).sum(axis=1)/mask.sum(axis=1)[:, None]
        except FloatingPointError as exc:
            raise ValueError("pooling overflow") from exc
    if not np.isfinite(result).all():
        raise ValueError("pooling overflow")
    return result


def curl_embeddings(hidden, projection):
    """Bias-free W^T h and L2 normalization; exactly-zero maps to zero."""
    h, w = _array(hidden, 2), _array(projection, 2)
    if h.shape[1] != w.shape[0] or w.shape[1] % 2:
        raise ValueError("matched hidden width and an even positive curl width required")
    try:
        with np.errstate(over="raise", invalid="raise"):
            raw = h@w
    except FloatingPointError as exc:
        raise ValueError("projection overflow") from exc
    if not np.isfinite(raw).all():
        raise ValueError("projection overflow")
    scale = np.max(np.abs(raw), axis=1, keepdims=True)
    safe = np.where(scale == 0, 1., scale)
    scaled = raw/safe
    norm = np.linalg.norm(scaled, axis=1, keepdims=True)
    v = scaled/np.where(norm == 0, 1., norm)
    # Keep a reciprocal norm for the analytic normalization Jacobian, avoiding
    # overflow of scale*norm. Zero's derivative is a declared local convention.
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            inverse_norm = np.divide(1., safe, out=np.zeros_like(safe), where=scale != 0)/np.where(norm == 0, 1., norm)
    except FloatingPointError as exc:
        raise ValueError("normalization derivative overflow") from exc
    if not np.isfinite(v).all() or not np.isfinite(inverse_norm).all():
        raise ValueError("normalization derivative overflow")
    return v, inverse_norm


def plane_features(left_embeddings, right_embeddings):
    left, right = _array(left_embeddings, 2), _array(right_embeddings, 2)
    if left.shape != right.shape or left.shape[1] % 2:
        raise ValueError("matched even-width curl embeddings required")
    try:
        with np.errstate(over="raise", invalid="raise"):
            result = left[:, 0::2]*right[:, 1::2]-left[:, 1::2]*right[:, 0::2]
    except FloatingPointError as exc:
        raise ValueError("plane feature overflow") from exc
    return result


def loss_gradients(chosen_hidden, rejected_hidden, projection, gamma,
                   chosen_logp, rejected_logp, chosen_reference_logp, rejected_reference_logp,
                   *, beta=.1, alpha=.5, regularization=.001):
    """Eqs.5--8, including L1 subgradient and non-detached hidden gradients.

    The zero subgradient is chosen at gamma=0; at W^T h=0 the normalized
    embedding is zero and this CPU kernel chooses a zero backward derivative.
    Those are explicit local boundary conventions, not an upstream default.
    """
    left, right, w = _array(chosen_hidden, 2), _array(rejected_hidden, 2), _array(projection, 2)
    planes = _array(gamma, 1)
    values = [_array(x, 1) for x in (chosen_logp, rejected_logp, chosen_reference_logp, rejected_reference_logp)]
    b, a, lam = _real(beta), _real(alpha), _real(regularization)
    if (left.shape != right.shape or w.shape != (left.shape[1], 2*len(planes))
            or any(len(x) != len(left) for x in values) or any(np.any(x > 0) for x in values)
            or b <= 0 or lam < 0):
        raise ValueError("matched hidden/logprob batches, d-by-2K projection, beta>0 and L1>=0 required")
    vl, il = curl_embeddings(left, w)
    vr, ir = curl_embeddings(right, w)
    features = plane_features(vl, vr)
    cp, rp, cr, rr = values
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            dpo = b*((cp-cr)-(rp-rr))
            logits = dpo+a*(features@planes)
            # Stable -log sigmoid(logit), with no unnecessary exp overflow.
            loss = float(np.logaddexp(0., -logits).mean()+lam*np.abs(planes).sum())
            sigmoid_negative = np.exp(-np.logaddexp(0., logits))
            derivative = -sigmoid_negative/len(left)
            dgamma = a*(features.T@derivative)+lam*np.sign(planes)
            dvl, dvr = np.zeros_like(vl), np.zeros_like(vr)
            factor = a*derivative[:, None]*planes[None, :]
            dvl[:, 0::2], dvl[:, 1::2] = factor*vr[:, 1::2], -factor*vr[:, 0::2]
            dvr[:, 0::2], dvr[:, 1::2] = -factor*vl[:, 1::2], factor*vl[:, 0::2]
            draw_left = (dvl-vl*np.sum(vl*dvl, axis=1, keepdims=True))*il
            draw_right = (dvr-vr*np.sum(vr*dvr, axis=1, keepdims=True))*ir
            dw = left.T@draw_left+right.T@draw_right
            dh_left, dh_right = draw_left@w.T, draw_right@w.T
    except FloatingPointError as exc:
        raise ValueError("SHPO objective/gradient intermediate overflow") from exc
    result = {"loss": loss, "logits": logits, "curl_scores": features@planes,
              "projection_gradient": dw, "gamma_gradient": dgamma,
              "chosen_hidden_gradient": dh_left, "rejected_hidden_gradient": dh_right,
              "chosen_logp_gradient": b*derivative, "rejected_logp_gradient": -b*derivative}
    if any(not np.isfinite(value).all() for value in result.values()):
        raise ValueError("SHPO objective/gradient overflow")
    return result


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    rng = np.random.default_rng(seed)
    left, right, w = rng.normal(size=(2, 3)), rng.normal(size=(2, 3)), rng.normal(size=(3, 4))
    gamma = np.array([.3, -.2])
    logs = ([-2., -3.], [-3., -2.], [-2.5, -2.5], [-2.5, -2.5])
    def evaluate(x=left, y=right, matrix=w, planes=gamma):
        return loss_gradients(x, y, matrix, planes, *logs)
    result = evaluate()
    step, errors = 1e-6, []
    for array, field, argument in ((w, "projection_gradient", "matrix"), (gamma, "gamma_gradient", "planes"),
                                    (left, "chosen_hidden_gradient", "x"), (right, "rejected_hidden_gradient", "y")):
        for index in np.ndindex(array.shape):
            delta = np.zeros_like(array)
            delta[index] = step
            numerical = (evaluate(**{argument: array+delta})["loss"]-evaluate(**{argument: array-delta})["loss"])/(2*step)
            errors.append(abs(numerical-result[field][index]))
    # Unit vectors at 0,120,240 degrees produce a genuine oriented triangle.
    v = np.array([[1., 0.], [-.5, math.sqrt(3)/2], [-.5, -math.sqrt(3)/2]])
    cycle = plane_features(v, np.roll(v, -1, axis=0))[:, 0]
    reverse = plane_features(np.roll(v, -1, axis=0), v)[:, 0]
    base = loss_gradients(left, right, w, [0., 0.], *logs, regularization=0.)
    no_curl = loss_gradients(left, right, w, gamma, *logs, alpha=0., regularization=0.)
    checks = {"all_head_and_hidden_gradients_match_finite_difference": bool(max(errors) < 1e-8),
              "antisymmetric_swap_negates_pair_score": bool(np.allclose(cycle, -reverse)),
              "three_pair_cycle_has_nonzero_circulation": bool(np.all(cycle > 0)),
              "zero_planes_reduce_to_dpo_loss": math.isclose(base["loss"], no_curl["loss"]),
              "curl_gradient_reaches_input_hidden": bool(np.linalg.norm(result["chosen_hidden_gradient"]) > 0),
              "zero_projection_maps_to_zero_embeddings": bool(np.all(curl_embeddings(left, np.zeros_like(w))[0] == 0))}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"gradient_max_abs_error": float(max(errors)),
            "triangle_circulation": float(cycle.sum()), "hidden_gradient_norm": float(np.linalg.norm(result["chosen_hidden_gradient"])),
            "loss": result["loss"], "pairs": 2, "curl_planes": 2}, "training_executed": False}
