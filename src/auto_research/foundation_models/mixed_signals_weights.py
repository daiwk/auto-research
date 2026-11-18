"""L0 weight-space programming boundary from arXiv:2611.13758v1.

An externally supplied patch is NOT an LLM or a trained biosignal classifier.
The tiny linear module in diagnostic() is a harness, NOT paper TinyEEGNet.
No optimizer, generated code execution, patient records or model API calls.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Mapping

import torch
from torch import Tensor, nn

REQUIRES_GPU_VALIDATION = True


def apply_weight_patch(model: nn.Module, patches: Mapping[str, Tensor]) -> None:
    """Validate all names/shapes/dtypes/values before an atomic parameter edit.

    Registered buffers are deliberately not an editable parameter channel.
    Roll back on a device/copy failure as well as validating before mutation.
    """
    parameters = dict(model.named_parameters())
    if not patches:
        raise ValueError("nonempty explicit patch required")
    staged = {}
    for name, value in patches.items():
        if name not in parameters or not isinstance(value, Tensor):
            raise ValueError("unknown/non-tensor parameter")
        old = parameters[name]
        if value.shape != old.shape or value.dtype != old.dtype or not torch.isfinite(value).all():
            raise ValueError("shape, dtype and finite-value validation failed")
        staged[name] = value.detach().to(old.device).clone()
    backup = {name: parameters[name].detach().clone() for name in staged}
    with torch.no_grad():
        try:
            for name, value in staged.items():
                parameters[name].copy_(value)
        except Exception:
            for name, value in backup.items():
                parameters[name].copy_(value)
            raise


class PracticeBudget:
    """Only this practice callback is exposed; evaluator labels stay external.

    Attempts consume budget before invocation, including callback failure.
    Failed calls are logged and propagated, never converted into fake scores.
    """

    def __init__(self, practice: Callable[[nn.Module], Mapping[str, float]], maximum_calls: int):
        if isinstance(maximum_calls, bool) or not isinstance(maximum_calls, int) or maximum_calls < 0:
            raise ValueError("nonnegative integral budget required")
        self._practice, self.maximum_calls = practice, maximum_calls
        self.calls = 0
        self.outcomes: list[str] = []

    def evaluate(self, model: nn.Module) -> dict[str, float]:
        if self.calls >= self.maximum_calls:
            raise RuntimeError("practice budget exhausted")
        self.calls += 1
        try:
            report = dict(self._practice(model))
            if not report or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in report.values()):
                raise ValueError("finite practice metrics required")
        except Exception:
            self.outcomes.append("failed")
            raise
        self.outcomes.append("completed")
        return report


def balanced_accuracy(predictions: Tensor, labels: Tensor, classes: int) -> float:
    """Evaluator-side metric; it is not exposed to a weight-edit provider."""
    if (predictions.ndim != 1 or labels.shape != predictions.shape or predictions.numel() == 0
            or predictions.dtype != torch.long or labels.dtype != torch.long
            or isinstance(classes, bool) or not isinstance(classes, int) or classes < 2
            or (labels < 0).any() or (labels >= classes).any()
            or (predictions < 0).any() or (predictions >= classes).any()):
        raise ValueError("aligned nonempty integral class predictions/labels required")
    recalls = []
    for c in range(classes):
        selected = labels == c
        if not selected.any():
            raise ValueError("all classes must be represented for fixed-class balanced accuracy")
        recalls.append(float((predictions[selected] == c).float().mean()))
    return math.fsum(recalls) / classes


def recovery_fraction(repaired: float, faulty: float, healthy: float) -> float:
    """Do not clip negative or above-one recovery, nor hide a zero denominator."""
    if any(isinstance(v, bool) or not math.isfinite(v) for v in (repaired, faulty, healthy)) or healthy == faulty:
        raise ValueError("finite metrics and nonzero healthy-faulty gap required")
    return (repaired - faulty) / (healthy - faulty)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"}:
        raise ValueError("cpu/cuda only")
    torch.manual_seed(seed)
    model = nn.Linear(4, 2).to(device)
    data = torch.randn(6, 4, device=device)
    before = model(data).detach().clone()
    snapshot = {name: value.detach().clone() for name, value in model.named_parameters()}
    rejected = False
    try:
        apply_weight_patch(model, {"weight": torch.zeros_like(model.weight), "bias": torch.tensor([float('nan'), 0.], device=device)})
    except ValueError:
        rejected = True
    atomic = all(torch.equal(value, snapshot[name]) for name, value in model.named_parameters())
    # Explicit fixture patch, not a claimed LLM-generated or learned repair.
    apply_weight_patch(model, {"weight": -model.weight.detach(), "bias": torch.zeros_like(model.bias)})
    output = model(data)
    budget = PracticeBudget(lambda network: {"output_norm": float(network(data).norm().detach())}, 1)
    practice = budget.evaluate(model)
    exhausted = False
    try:
        budget.evaluate(model)
    except RuntimeError:
        exhausted = True
    failed = PracticeBudget(lambda _: (_ for _ in ()).throw(ValueError("explicit failure")), 1)
    try:
        failed.evaluate(model)
    except ValueError:
        pass
    score = balanced_accuracy(torch.tensor([0, 0, 0, 1], device=device),
                              torch.tensor([0, 0, 1, 1], device=device), 2)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "checks": {"atomic_invalid_patch": rejected and atomic,
                       "explicit_patch_changes_forward": not bool(torch.equal(before, output)),
                       "budget_enforced": exhausted and budget.calls == 1,
                       "failed_call_consumes_budget": failed.calls == 1 and failed.outcomes == ["failed"],
                       "balanced_accuracy_not_micro": score == .75,
                       "unclipped_recovery": recovery_fraction(.9, .4, .8) > 1},
            "metrics": {"harness_output_norm": practice["output_norm"], "fixture_balanced_accuracy": score,
                        "practice_calls": budget.calls, "failed_calls": failed.calls,
                        "fixture_recovery": recovery_fraction(.9, .4, .8)}}
