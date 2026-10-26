"""UniAction v1 semantic tokens/native-position interface and Algorithm1.

This is the actual cardinality-calibrated attention equation, not a video
generator, custom accelerated kernel, or counterfactual action benchmark.
"""
import math
from collections.abc import Callable

import torch
from torch import Tensor, nn

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/uniaction-a100-20261026.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or min(x.shape) < 1 or x.numel() > 1_048_576
            or not x.is_floating_point() or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite nonempty floating tensor required")


class ActionTokens(nn.Module):
    """Eq.2--3: shared semantic codebook + caller's *native* positional map.

    No guessed replacement RoPE is supplied. The caller also applies that same
    positional map to video tokens before constructing attention Q/K tensors.
    """

    def __init__(self, vocabulary: int, dimension: int):
        super().__init__()
        if not 1 <= vocabulary <= 4096 or not 1 <= dimension <= 4096:
            raise ValueError("bounded vocabulary and dimension required")
        self.codebook = nn.Embedding(vocabulary, dimension)

    def forward(self, identities: Tensor, coordinates: Tensor,
                native_position: Callable[[Tensor, Tensor], Tensor]) -> Tensor:
        if (identities.ndim != 2 or identities.dtype != torch.long or min(identities.shape) < 1
                or bool(((identities < 0) | (identities >= self.codebook.num_embeddings)).any())):
            raise ValueError("valid [batch,action] semantic identities required")
        _finite(coordinates, 3)
        if (coordinates.shape != identities.shape + (3,) or coordinates.device != identities.device
                or identities.device != self.codebook.weight.device):
            raise ValueError("aligned continuous [t,y,x] coordinates required")
        result = native_position(self.codebook(identities), coordinates)
        _finite(result, 3)
        if result.shape != identities.shape + (self.codebook.embedding_dim,):
            raise ValueError("native position map must preserve token shape")
        return result


def cardinality_attention(query: Tensor, video_keys: Tensor, video_values: Tensor,
                          action_keys: Tensor, action_values: Tensor, *,
                          reference_cardinality: float, action_mask: Tensor | None = None,
                          calibrated: bool = True) -> dict:
    """AppendixB Algorithm1: joint video/action softmax with log(Nref/Na).

    Q/K/V are [B,H,tokens,D]. Padding is removed from Na and zeroed before
    products; it receives -inf logits and zero attention. Every request needs
    at least one real action token. No approximation of the softmax is used.
    """
    for x in (query, video_keys, video_values, action_keys, action_values):
        _finite(x, 4)
        if x.device != query.device or x.dtype != query.dtype:
            raise ValueError("Q/K/V dtype/device must agree")
    if (video_keys.shape != video_values.shape or action_keys.shape != action_values.shape
            or video_keys.shape[:2] != query.shape[:2] or action_keys.shape[:2] != query.shape[:2]
            or video_keys.shape[-1] != query.shape[-1] or action_keys.shape[-1] != query.shape[-1]
            or isinstance(reference_cardinality, bool) or not math.isfinite(reference_cardinality)
            or reference_cardinality <= 0 or not isinstance(calibrated, bool)):
        raise ValueError("aligned Q/K/V and finite positive reference cardinality required")
    b, h, nq, d = query.shape
    na, nv = action_keys.shape[-2], video_keys.shape[-2]
    if b * h * nq * (na + nv) > 1_048_576:
        raise ValueError("cost gate: attention matrix too large")
    if action_mask is None:
        action_mask = torch.ones(b, na, device=query.device, dtype=torch.bool)
    if (action_mask.shape != (b, na) or action_mask.dtype != torch.bool
            or action_mask.device != query.device or not bool(action_mask.any(-1).all())):
        raise ValueError("bool action mask with positive cardinality per request required")
    work = torch.float32 if query.dtype in (torch.float16, torch.bfloat16) else query.dtype
    q, vk, vv, ak, av = [x.to(work) for x in (query, video_keys, video_values, action_keys, action_values)]
    mask = action_mask[:, None, :, None]
    ak, av = torch.where(mask, ak, 0), torch.where(mask, av, 0)
    video_logits = q @ vk.transpose(-2, -1) / math.sqrt(d)
    action_logits = q @ ak.transpose(-2, -1) / math.sqrt(d)
    if calibrated:
        bias = math.log(reference_cardinality) - action_mask.sum(-1).to(work).log()
        action_logits = action_logits + bias[:, None, None, None]
    action_logits = action_logits.masked_fill(~action_mask[:, None, None, :], -torch.inf)
    weights = torch.cat((video_logits, action_logits), -1).softmax(-1)
    output = weights[..., :nv] @ vv + weights[..., nv:] @ av
    if not bool(torch.isfinite(output).all()):
        raise ValueError("nonfinite attention output; no silent clamp")
    return {"output": output, "video_attention": weights[..., :nv],
            "action_attention": weights[..., nv:]}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or actual available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    q = torch.randn(2, 2, 3, 4, generator=gen, device=device, dtype=torch.float64, requires_grad=True)
    vk = torch.randn(2, 2, 5, 4, generator=gen, device=device, dtype=torch.float64)
    vv = torch.randn(2, 2, 5, 4, generator=gen, device=device, dtype=torch.float64)
    ak = torch.randn(2, 2, 2, 4, generator=gen, device=device, dtype=torch.float64, requires_grad=True)
    av = torch.randn(2, 2, 2, 4, generator=gen, device=device, dtype=torch.float64, requires_grad=True)
    args = (q, vk, vv, ak, av)
    result = cardinality_attention(*args, reference_cardinality=3.)
    logits = torch.cat((q @ vk.transpose(-2, -1) / 2,
                        q @ ak.transpose(-2, -1) / 2 + math.log(3 / 2)), -1)
    reference = logits.softmax(-1) @ torch.cat((vv, av), -2)
    error = (result["output"] - reference).abs().max().item()
    doubled = cardinality_attention(q, vk, vv, ak.repeat_interleave(2, -2), av.repeat_interleave(2, -2),
                                    reference_cardinality=3.)
    invariance = (result["output"] - doubled["output"]).abs().max().item()
    uncalibrated = cardinality_attention(*args, reference_cardinality=3., calibrated=False)
    uncalibrated_double = cardinality_attention(q, vk, vv, ak.repeat_interleave(2, -2),
        av.repeat_interleave(2, -2), reference_cardinality=3., calibrated=False)
    negative_gap = (uncalibrated["output"] - uncalibrated_double["output"]).abs().max().item()
    padded_k = torch.cat((ak, torch.full_like(ak[:, :, :1], 1e20)), -2)
    padded_v = torch.cat((av, torch.full_like(av[:, :, :1], 1e20)), -2)
    padded = cardinality_attention(q, vk, vv, padded_k, padded_v, reference_cardinality=3.,
        action_mask=torch.tensor([[True, True, False]] * 2, device=device))
    result["output"].square().mean().backward()
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        torch.manual_seed(seed)
        tokens = ActionTokens(3, 4).to(device=device, dtype=torch.float64)
    identities = torch.tensor([[1, 1, 2]], device=device)
    coordinates = torch.zeros(1, 3, 3, device=device, dtype=torch.float64)
    forwarded = []
    def interface_fixture(t, p):
        # Tests explicit callback transport only, not Wan's native positional map.
        forwarded.append(p)
        return t
    semantic = tokens(identities, coordinates, interface_fixture)
    semantic.sum().backward()
    checks = {"joint_softmax_formula_reference": error < 1e-12,
              "duplicated_action_cardinality_invariant": invariance < 1e-12,
              "uncalibrated_duplication_negative_control": negative_gap > 1e-6,
              "padding_excluded_from_cardinality_and_output": torch.allclose(padded["output"], reference, atol=1e-12, rtol=0),
              "actual_action_key_value_gradients": all(x.grad is not None and bool(torch.isfinite(x.grad).all()) and x.grad.norm().item() > 0 for x in (q, ak, av)),
              "attention_mass_normalized": torch.allclose(result["video_attention"].sum(-1) + result["action_attention"].sum(-1), torch.ones_like(result["video_attention"].sum(-1)), atol=1e-12, rtol=0),
              "semantic_identity_reuses_codebook": torch.equal(semantic[:, 0], semantic[:, 1]) and tokens.codebook.weight.grad[1].abs().sum().item() > 0,
              "native_position_interface_receives_coordinates": len(forwarded) == 1 and torch.equal(forwarded[0], coordinates)}
    if not all(checks.values()):
        raise RuntimeError(f"UniAction mechanism check failed: {checks}")
    return {"seed": seed, "metrics": {"attention_reference_error": error,
        "duplication_invariance_error": invariance, "uncalibrated_duplication_gap": negative_gap,
        "action_key_gradient_norm": ak.grad.norm().item(), "action_value_gradient_norm": av.grad.norm().item(),
        "semantic_codebook_gradient_norm": tokens.codebook.weight.grad.norm().item(),
        "pretrained_video_model_calls": 0}, "checks": checks}
