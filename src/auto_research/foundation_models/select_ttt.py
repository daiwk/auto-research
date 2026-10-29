"""Select-TTT v1 Eqs.6--12: query-conditioned fast-weight write components.

External frozen-model hidden states, LM-head/RMSNorm weights and NTP-aligned
keys/values are required. No LLM loading, QA benchmark or context-parallel kernel
is implied. Query tokens, not answer labels, control the write strength.
"""
import math

import torch
from torch import Tensor
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/select-ttt-a100-20261029.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or not 0 < x.numel() <= 1_048_576
            or x.dtype not in (torch.float32, torch.float64)
            or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite floating tensor required")


def query_chunk_scores(hidden: Tensor, lm_head: Tensor, query_tokens: Tensor, *,
                       norm_weight: Tensor, norm_eps: float, bias: Tensor | None = None,
                       pooling_ratio: float = .1, vocabulary_block: int = 256) -> Tensor:
    """Eqs.7--9/11--12, lowest-CE top-k MEAN; repeated query tokens count.

    Hidden is [chunks, positions, width]. The model's actual frozen RMSNorm
    weight/epsilon are explicit; no guessed unweighted normalization. Vocabulary
    LSE is blockwise. No gradient from this bounded score-only interface.
    """
    for x, ndim in ((hidden, 3), (lm_head, 2), (norm_weight, 1)):
        _finite(x, ndim)
    if (lm_head.shape[1] != hidden.shape[2] or norm_weight.shape != hidden.shape[2:]
            or any(x.dtype != hidden.dtype or x.device != hidden.device for x in (lm_head, norm_weight))
            or query_tokens.ndim != 1 or query_tokens.numel() < 1 or query_tokens.dtype != torch.long
            or query_tokens.device != hidden.device or bool(((query_tokens < 0) | (query_tokens >= len(lm_head))).any())
            or isinstance(pooling_ratio, bool) or not math.isfinite(pooling_ratio) or not 0 < pooling_ratio <= 1
            or isinstance(norm_eps, bool) or not math.isfinite(norm_eps) or norm_eps <= 0
            or isinstance(vocabulary_block, bool) or not isinstance(vocabulary_block, int) or vocabulary_block < 1):
        raise ValueError("aligned frozen output head/query/RMSNorm and valid pooling/block required")
    if bias is not None:
        _finite(bias, 1)
        if bias.shape != lm_head.shape[:1] or bias.dtype != hidden.dtype or bias.device != hidden.device:
            raise ValueError("aligned optional head bias required")
    with torch.no_grad():
        h = F.rms_norm(hidden, hidden.shape[2:], norm_weight, norm_eps)
        lse = torch.full(hidden.shape[:2], -torch.inf, dtype=h.dtype, device=h.device)
        for start in range(0, len(lm_head), vocabulary_block):
            logits = h @ lm_head[start:start + vocabulary_block].T
            if bias is not None:
                logits = logits + bias[start:start + vocabulary_block]
            lse = torch.logaddexp(lse, torch.logsumexp(logits, -1))
        selected = h @ lm_head[query_tokens].T
        if bias is not None:
            selected = selected + bias[query_tokens]
        ce = lse - selected.mean(-1)
        k = max(1, math.ceil(pooling_ratio * hidden.shape[1]))
        return ce.topk(k, dim=-1, largest=False).values.mean(-1)


def write_multipliers(scores: Tensor, *, temperature: float, maximum: float) -> Tensor:
    """Eq.10 exactly: clip AFTER T*softmax, WITHOUT renormalization.

    The sum is T only if no upper clipping is active. Clipped budgets are below
    T, contrary to interpreting the paper's approximate claim as an invariant.
    """
    _finite(scores, 1)
    if any(isinstance(v, bool) or not math.isfinite(v) or v <= 0 for v in (temperature, maximum)):
        raise ValueError("positive finite temperature and clip required")
    return (len(scores) * torch.softmax(-scores / temperature, 0)).clamp(0, maximum)


def apply_then_write(initial: Tensor, keys: Tensor, values: Tensor,
                     multipliers: Tensor, *, learning_rate: float) -> dict:
    """Eq.6 sequential reference; output i uses W_i, then commits chunk i.

    Keys/values are caller-provided NTP-aligned features, not query answers.
    This reference is not the distributed context-parallel implementation.
    """
    for x, ndim in ((initial, 2), (keys, 3), (values, 3), (multipliers, 1)):
        _finite(x, ndim)
    if (keys.shape[:2] != values.shape[:2] or initial.shape != (values.shape[2], keys.shape[2])
            or len(multipliers) != len(keys) or bool((multipliers < 0).any())
            or any(x.dtype != initial.dtype or x.device != initial.device for x in (keys, values, multipliers))
            or isinstance(learning_rate, bool) or not math.isfinite(learning_rate) or learning_rate < 0):
        raise ValueError("aligned fast-weight state/features and nonnegative learning rate required")
    state = initial
    outputs, states = [], [state]
    for i in range(len(keys)):
        outputs.append(keys[i] @ state.T)
        state = state + learning_rate * multipliers[i] * values[i].T @ keys[i]
        states.append(state)
    return {"outputs": torch.stack(outputs), "states": torch.stack(states), "final_weight": state}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    args = {"generator": gen, "device": device, "dtype": torch.float64}
    hidden, head = torch.randn(4, 5, 6, **args), torch.randn(13, 6, **args)
    norm, bias = torch.randn(6, **args), torch.randn(13, **args)
    query = torch.tensor([1, 1, 7], dtype=torch.long, device=device)
    scores = query_chunk_scores(hidden, head, query, norm_weight=norm, norm_eps=1e-6,
                                bias=bias, pooling_ratio=.4, vocabulary_block=4)
    logp = (F.rms_norm(hidden, (6,), norm, 1e-6) @ head.T + bias).log_softmax(-1)
    reference = (-logp[..., query].mean(-1)).sort(-1).values[:, :2].mean(-1)
    error = (scores - reference).abs().max().item()
    lambdas = write_multipliers(scores, temperature=.7, maximum=4.)
    clipped = write_multipliers(torch.tensor([0., 100., 100.], device=device, dtype=hidden.dtype),
                                temperature=1., maximum=1.2)
    initial = torch.randn(3, 6, **args)
    keys, values = torch.randn(4, 2, 6, **args), torch.randn(4, 2, 3, **args)
    result = apply_then_write(initial, keys, values, lambdas, learning_rate=.03)
    direct = initial + .03 * sum(lambdas[i] * values[i].T @ keys[i] for i in range(4))
    state_error = (result["final_weight"] - direct).abs().max().item()
    unique = query_chunk_scores(hidden, head, torch.tensor([1, 7], device=device),
        norm_weight=norm, norm_eps=1e-6, bias=bias, pooling_ratio=.4, vocabulary_block=13)
    checks = {"blockwise_lse_dense_query_ce_reference": error < 1e-12,
        "query_multiplicity_retained": not torch.allclose(scores, unique),
        "unclipped_budget_sums_to_chunk_count": abs(lambdas.sum().item() - 4) < 1e-12,
        "clip_not_silently_renormalized": abs(clipped.sum().item() - 1.2) < 1e-12,
        "lower_ce_receives_stronger_write": int(lambdas.argmax()) == int(scores.argmin()),
        "apply_precedes_current_chunk_write": torch.allclose(result["outputs"][0], keys[0] @ initial.T),
        "fast_weight_update_independent_reference": state_error < 1e-12,
        "real_fast_weight_state_changes": not torch.equal(result["final_weight"], initial)}
    if not all(checks.values()):
        raise RuntimeError(f"Select-TTT checks failed: {checks}")
    return {"seed": seed, "metrics": {"score_reference_error": error,
        "state_reference_error": state_error, "unclipped_write_budget": lambdas.sum().item(),
        "clipped_write_budget": clipped.sum().item(),
        "weight_delta": (result["final_weight"] - initial).norm().item(),
        "model_calls": 0}, "checks": checks}
