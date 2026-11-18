"""RS-JEPA scan views, adversarial partition and relational loss, not a Vim model."""
import math

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/rs-jepa-a100-20261111.json"


def scan_path(height: int, width: int, path: str) -> tuple[int, ...]:
    """Paper's four traversals, not full-sequence reversal or a snake traversal."""
    if type(height) is not int or type(width) is not int or min(height, width) < 1:
        raise ValueError("positive patch-grid dimensions required")
    rows, columns = range(height), range(width)
    if path == "row":
        return tuple(r * width + c for r in rows for c in columns)
    if path == "column":
        return tuple(r * width + c for c in columns for r in rows)
    if path == "row_mirror":
        return tuple(r * width + c for r in rows for c in reversed(columns))
    if path == "column_mirror":
        return tuple(r * width + c for c in columns for r in reversed(rows))
    raise ValueError("expected row, column, row_mirror or column_mirror")


def reverse_gradient(value):
    import torch

    class Reverse(torch.autograd.Function):
        @staticmethod
        def forward(ctx, tensor):
            return tensor.view_as(tensor)

        @staticmethod
        def backward(ctx, gradient):
            return -gradient

    return Reverse.apply(value)


def adversarial_partition(tokens, scorer_weight, scorer_bias=None):
    """Equation 5: hard equal split, identity forward, reversed scorer gradient.

    Tokens are visible stem tokens in context order, shaped (batch, even_tokens,
    width). A/B retain that context order, not descending scorer order. No encoder
    or predictor is substituted by this component.
    """
    import torch
    if (tokens.ndim != 3 or tokens.shape[1] < 2 or tokens.shape[1] % 2
            or not torch.is_floating_point(tokens)
            or scorer_weight.shape != (tokens.shape[-1],)
            or scorer_weight.device != tokens.device or scorer_weight.dtype != tokens.dtype
            or not bool(torch.isfinite(tokens).all()) or not bool(torch.isfinite(scorer_weight).all())):
        raise ValueError("finite colocated floating tokens and width-vector scorer required")
    scores = tokens @ scorer_weight
    if scorer_bias is not None:
        if (scorer_bias.ndim != 0 or scorer_bias.device != tokens.device
                or scorer_bias.dtype != tokens.dtype or not bool(torch.isfinite(scorer_bias))):
            raise ValueError("a finite colocated scalar bias is required")
        scores = scores + scorer_bias
    ranked = torch.argsort(scores.detach(), dim=1, descending=True, stable=True)
    half = tokens.shape[1] // 2
    indices_a = ranked[:, :half].sort(dim=1).values
    indices_b = ranked[:, half:].sort(dim=1).values
    member_a = torch.zeros_like(scores, dtype=torch.bool).scatter_(1, indices_a, True)
    probability = torch.sigmoid(reverse_gradient(scores))
    omega = torch.where(member_a, probability, 1 - probability)
    weighted = tokens * (1 + (omega - omega.detach())).unsqueeze(-1)
    a = weighted.gather(1, indices_a.unsqueeze(-1).expand(-1, -1, tokens.shape[-1]))
    b = weighted.gather(1, indices_b.unsqueeze(-1).expand(-1, -1, tokens.shape[-1]))
    return a, b, indices_a, indices_b


def neighbourhood_consensus(uni_1, uni_2, cross_1, cross_2, *, temperature: float = .1):
    """Equations 8-9: four twin-excluded KL terms towards detached uni consensus."""
    import torch
    from torch.nn import functional as functional
    embeddings = (uni_1, uni_2, cross_1, cross_2)
    if type(temperature) not in {int, float} or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("positive finite relational temperature required")
    if (uni_1.ndim != 2 or uni_1.shape[0] < 2 or uni_1.shape[1] < 1
            or any(x.shape != uni_1.shape or x.device != uni_1.device or x.dtype != uni_1.dtype
                   or not torch.is_floating_point(x) or not bool(torch.isfinite(x).all())
                   or bool((x.norm(dim=-1) == 0).any()) for x in embeddings)):
        raise ValueError("four finite nonzero, equally shaped colocated embedding matrices required")
    u1, u2, c1, c2 = (functional.normalize(x, dim=-1) for x in embeddings)
    count = uni_1.shape[0]
    off_diagonal = ~torch.eye(count, device=uni_1.device, dtype=torch.bool)

    def log_distribution(query, gallery):
        logits = ((query @ gallery.T) / temperature)[off_diagonal].reshape(count, count - 1)
        return functional.log_softmax(logits, dim=-1)

    logs = (log_distribution(u1, u1), log_distribution(u2, u2),
            log_distribution(c1, c2), log_distribution(c2, c1))
    target = ((logs[0].exp() + logs[1].exp()) / 2).detach()
    target_log = target.clamp_min(torch.finfo(target.dtype).tiny).log()
    return sum((target * (target_log - log_prob)).sum(dim=-1).mean() for log_prob in logs) / 4


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Tiny tensor reference controls; CUDA means real CUDA forward/backward work."""
    import torch
    selected_device = torch.device(device)
    if selected_device.type not in {"cpu", "cuda"}:
        raise ValueError("only explicit CPU or CUDA tensor diagnostics are supported")
    if selected_device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA is unavailable; no CPU fallback")
    if selected_device.type == "cuda" and selected_device.index is None:
        selected_device = torch.device("cuda", torch.cuda.current_device())
    generator = torch.Generator(device=selected_device).manual_seed(seed)
    tokens = torch.randn(2, 6, 4, device=selected_device, dtype=torch.float64,
                         generator=generator, requires_grad=True)
    weight = torch.randn(4, device=selected_device, dtype=torch.float64,
                         generator=generator, requires_grad=True)
    a, b, ia, ib = adversarial_partition(tokens, weight)
    loss = a.square().sum() + b.sin().sum()
    loss.backward()
    with torch.no_grad():
        x = tokens.detach()
        member_a = torch.zeros(x.shape[:2], device=selected_device, dtype=torch.bool).scatter_(1, ia, True)
        probability = torch.sigmoid(x @ weight.detach())
        coefficients = torch.where(member_a, (2 * x.square()).sum(-1), (x * x.cos()).sum(-1))
        sign = torch.where(member_a, 1., -1.)
        expected_gradient = -(coefficients * sign * probability * (1 - probability)).unsqueeze(-1) * x
        error = (weight.grad - expected_gradient.sum((0, 1))).abs().max()
        identity_forward = (torch.equal(a, x.gather(1, ia.unsqueeze(-1).expand(-1, -1, 4)))
                            and torch.equal(b, x.gather(1, ib.unsqueeze(-1).expand(-1, -1, 4))))
    matrices = [torch.randn(5, 4, device=selected_device, dtype=torch.float64,
                            generator=generator, requires_grad=True) for _ in range(4)]
    relational = neighbourhood_consensus(*matrices)
    relational.backward()
    same = neighbourhood_consensus(*(matrices[0] for _ in range(4)))
    swapped = neighbourhood_consensus(matrices[1], matrices[0], matrices[3], matrices[2])
    paths = [scan_path(3, 3, name) for name in ("row", "column", "row_mirror", "column_mirror")]
    if selected_device.type == "cuda":
        torch.cuda.synchronize(selected_device)
    return {"seed": seed, "device": str(tokens.device), "diagnostic_only": True,
            "evaluation_tier": "l1_mechanism",
            "metrics": {"relational_loss": float(relational.detach()),
                        "identical_distribution_loss": float(same.detach()),
                        "scorer_gradient_reference_error": float(error), "scan_paths": len(set(paths))},
            "checks": {"actual_requested_tensor_device": tokens.device == selected_device,
                       "hard_partition_identity_forward": identity_forward,
                       "disjoint_equal_partition": bool(torch.equal(
                           torch.cat((ia, ib), 1).sort(1).values,
                           torch.arange(6, device=selected_device).expand(2, -1))),
                       "gradient_reversal_matches_reference": float(error) < 1e-10,
                       "all_four_losses_backpropagate": all(
                           x.grad is not None and bool(torch.isfinite(x.grad).all()) for x in matrices),
                       "consensus_zero_when_all_agree": abs(float(same.detach())) < 1e-12,
                       "sensor_swap_invariance": bool(torch.allclose(relational, swapped, atol=1e-12)),
                       "four_distinct_scan_views": len(set(paths)) == 4}}
