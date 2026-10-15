"""Minute-scale numerical/parameter-update diagnostics, not LLM pretraining."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import time
from pathlib import Path

import numpy as np
import torch
from torch import Tensor, nn

from auto_research.runtime import DEVICE_ENV, device_for

from .optim import PMRC, SMRC, matrix_sign

PUBLIC_PROTOCOL = "https://arxiv.org/html/2610.19844v1#A5.SS1.SSS1"
PUBLIC_REVISION = "arxiv:2610.19844v1:appendix-E.1.1:equation-30"


def _polar_reference(value: Tensor) -> Tensor:
    """Independent NumPy CPU FP64 oracle, without PyTorch CPU LAPACK.

    GPU-only PyTorch builds can have CUDA SVD but no host LAPACK. Keeping the
    oracle on NumPy also makes it independent of the tested torch.linalg path.
    The sign definition and the numerical acceptance tolerance are unchanged.
    """
    array = value.detach().double().cpu().numpy()
    left, singular, right = np.linalg.svd(array, full_matrices=False)
    cutoff = np.finfo(np.float64).eps * max(value.shape) * singular.max()
    return torch.from_numpy((left * (singular > cutoff)) @ right)


def _numerical_controls(device: str) -> dict[str, float]:
    metrics = {}
    generator = torch.Generator().manual_seed(71)
    gradients = [torch.randn(3, 5, generator=generator, dtype=torch.float64) for _ in range(3)]
    for name, cls in (("smrc", SMRC), ("pmrc", PMRC)):
        param = nn.Parameter(torch.zeros((3, 5), dtype=torch.float64, device=device))
        optimizer = cls([param], lr=0.1, beta=0.3, gamma=0.8, rank=3, refresh_interval=None)
        expected = torch.zeros((3, 5), dtype=torch.float64)
        momentum = torch.zeros_like(expected)
        errors = []
        for gradient in gradients:
            momentum = 0.7 * momentum + 0.3 * gradient
            expected -= 0.1 * (_polar_reference(momentum) if cls is PMRC else momentum)
            param.grad = gradient.to(device)
            optimizer.step()
            errors.append(float((param.detach().cpu() - expected).abs().max()))
        metrics[f"{name}_full_rank_max_abs_error"] = max(errors)

        param = nn.Parameter(torch.zeros((2, 2), dtype=torch.float64, device=device))
        optimizer = cls([param], lr=0.1, beta=0.25, gamma=0.8, rank=1, refresh_interval=2)
        basis = torch.tensor([[1.], [0.]], dtype=torch.float64)
        momentum = torch.zeros((1, 2), dtype=torch.float64)
        expected = torch.zeros((2, 2), dtype=torch.float64)
        for gradient in (torch.diag(torch.tensor([4., 1.], dtype=torch.float64)),
                         torch.tensor([[0., 2.], [0., 3.]], dtype=torch.float64)):
            projected = basis.T @ gradient
            momentum = 0.75 * momentum + 0.25 * projected
            low_rank = _polar_reference(momentum) if cls is PMRC else momentum
            expected -= 0.1 * (basis @ low_rank + 0.8 * (gradient - basis @ projected))
            param.grad = gradient.to(device)
            optimizer.step()
        if cls is SMRC:
            expected -= 0.1 * 3 * (basis @ momentum)
        metrics[f"{name}_boundary_max_abs_error"] = float(
            (param.detach().cpu() - expected).abs().max()
        )
        resumed_param = nn.Parameter(param.detach().clone())
        resumed = cls([resumed_param], rank=1)
        resumed.load_state_dict(copy.deepcopy(optimizer.state_dict()))
        for gradient in gradients:
            grad = gradient[:2, :2].to(device)
            param.grad, resumed_param.grad = grad, grad.clone()
            optimizer.step()
            resumed.step()
        metrics[f"{name}_state_resume_max_abs_error"] = float(
            (param.detach() - resumed_param.detach()).abs().max()
        )
    if max(metrics.values()) > 1e-9:
        raise AssertionError(f"exact-update/state controls failed: {metrics}")
    return metrics


def _paper_quadratic(device: str):
    """The published 30x8 construction, with right-projection noise."""
    signal = torch.eye(30, dtype=torch.float64)[:, :2]
    noise = torch.eye(30, dtype=torch.float64)[:, -2:]
    pattern = torch.tensor([[1.] * 8, [1., -1.] * 4], dtype=torch.float64)
    signal_right = pattern.T / (8 ** 0.5)
    # Host construction must not require LAPACK in the PyTorch build. The
    # tested optimizer's CUDA SVD/QR remains unchanged and still runs on CUDA.
    complete_q = np.linalg.qr(signal_right.numpy(), mode="complete")[0]
    noise_right = torch.from_numpy(complete_q[:, 2:4].copy())
    start = signal @ torch.diag(torch.tensor([1.8, 0.9], dtype=torch.float64)) @ pattern
    return tuple(value.to(device) for value in (signal, noise, pattern, noise_right, start))


def _low_precision_controls(device: str) -> dict:
    """Six real updates, including refresh-boundary FP32-state restoration.

    This is not an AMP training experiment. FP16/BF16 parameter rounding is
    compared with FP32 using declared absolute tolerances; the saved FP32
    basis/momentum and resumed same-dtype trajectory must be exactly equal.
    """
    results = {}
    generator = torch.Generator().manual_seed(113)
    raw_gradients = [torch.randn(4, 6, generator=generator) for _ in range(6)]
    for label, dtype, tolerance in (("fp16", torch.float16, 2e-4),
                                    ("bf16", torch.bfloat16, 2e-3)):
        for name, cls in (("smrc", SMRC), ("pmrc_practical", PMRC)):
            parameter = nn.Parameter(torch.zeros(4, 6, dtype=dtype, device=device))
            full = nn.Parameter(torch.zeros(4, 6, dtype=torch.float32, device=device))
            kwargs = dict(lr=0.01, beta=0.3, gamma=0.8, rank=2, refresh_interval=3)
            if cls is PMRC:
                kwargs["variant"] = "practical"
            optimizer, full_optimizer = cls([parameter], **kwargs), cls([full], **kwargs)
            resumed, resumed_parameter = None, None
            for step, raw in enumerate(raw_gradients):
                gradient = raw.to(device=device, dtype=dtype)
                parameter.grad = gradient
                full.grad = gradient.float()
                optimizer.step()
                full_optimizer.step()
                if step == 1:
                    resumed_parameter = nn.Parameter(parameter.detach().clone())
                    resumed = cls([resumed_parameter], **kwargs)
                    resumed.load_state_dict(copy.deepcopy(optimizer.state_dict()))
                    for field in ("basis", "momentum"):
                        if not torch.equal(optimizer.state[parameter][field],
                                           resumed.state[resumed_parameter][field]):
                            raise AssertionError("low-precision load rounded an FP32 optimizer state")
                elif step > 1:
                    resumed_parameter.grad = gradient.clone()
                    resumed.step()
            resume_error = float((parameter.detach().float() - resumed_parameter.detach().float()).abs().max())
            fp32_error = float((parameter.detach().float() - full.detach()).abs().max())
            if resume_error != 0 or fp32_error > tolerance:
                raise AssertionError(f"{name}/{label} precision control failed: "
                                     f"resume={resume_error}, fp32={fp32_error}, atol={tolerance}")
            changed = bool(torch.count_nonzero(parameter.detach()))
            if not changed:
                raise AssertionError("precision control did not actually update a parameter")
            results[f"{name}_{label}"] = {
                "updates": 6,
                "parameter_changed": changed,
                "state_dtype": "float32",
                "max_abs_error_to_fp32": fp32_error,
                "comparison_atol": tolerance,
                "state_resume_max_abs_error": resume_error,
                "state_restore_exact": True,
            }
    return results


class _FullSpaceControl(SMRC):
    """Dense EMA-SGD / exact Muon controls without storing an identity basis."""

    def __init__(self, parameters, *, muon: bool, **kwargs):
        self.muon = muon
        super().__init__(parameters, refresh_interval=None, **kwargs)

    def _matrix_step(self, param: Tensor, group: dict) -> None:
        state = self.state[param]
        gradient = param.grad.to(torch.float64 if param.dtype == torch.float64 else torch.float32)
        if not state:
            state.update(step=0, momentum=torch.zeros_like(gradient))
        state["momentum"].mul_(1 - group["beta"]).add_(gradient, alpha=group["beta"])
        direction = matrix_sign(state["momentum"]) if self.muon else state["momentum"]
        param.mul_(1 - group["lr"] * group["weight_decay"])
        param.add_(direction.to(param.dtype), alpha=-group["lr"])
        state["step"] += 1


def _optimizer(name: str, parameters):
    common = dict(lr=0.04, beta=0.3, gamma=0.8)
    if name == "smrc":
        return SMRC(parameters, **common, rank=2, refresh_interval=20)
    if name == "pmrc":
        return PMRC(parameters, **common, rank=2, refresh_interval=20)
    if name == "pmrc_practical":
        return PMRC(parameters, **common, rank=2, refresh_interval=20, variant="practical")
    if name == "full_ema_sgd":
        return _FullSpaceControl(parameters, **common, muon=False)
    if name == "full_muon":
        return _FullSpaceControl(parameters, **common, muon=True)
    if name == "adamw":
        return torch.optim.AdamW(parameters, lr=0.04, weight_decay=0)
    raise ValueError(f"unknown diagnostic arm {name}")


def _check_budget(deadline: float) -> None:
    if time.monotonic() > deadline:
        raise TimeoutError("SMRC/PMRC diagnostic exceeded its hard time budget; do not expand it")


def _state_elements(optimizer) -> int:
    return sum(value.numel() for state in optimizer.state.values()
               for value in state.values() if isinstance(value, Tensor) and value.ndim > 0)


def run_diagnostic(
    *, seed: int = 42, device: str = "cpu", steps: int = 80, max_seconds: float = 120,
) -> dict:
    if device != "cpu" and not re.fullmatch(r"cuda(?::[0-9]+)?", device):
        raise ValueError("diagnostic supports cpu, cuda or cuda:<index>")
    resolved = device_for(torch, device)
    device = str(resolved)
    if not isinstance(steps, int) or not 1 <= steps <= 400:
        raise ValueError("steps must be in [1, 400]; full LLM experiments are deliberately absent")
    if not 0 < max_seconds <= 180:
        raise ValueError("max_seconds must be in (0, 180]")
    started = time.monotonic()
    deadline = started + max_seconds
    controls = _numerical_controls(device)
    low_precision = _low_precision_controls(device)
    signal, noise, pattern, noise_right, initial = _paper_quadratic(device)
    generator = torch.Generator().manual_seed(seed)
    signs = (torch.randint(0, 2, (steps,), generator=generator) * 2 - 1).tolist()
    arms = {}
    names = ("smrc", "pmrc", "pmrc_practical", "full_ema_sgd", "full_muon", "adamw")
    for name in names:
        parameter = nn.Parameter(initial.clone())
        optimizer = _optimizer(name, [parameter])
        initial_norm = float((signal.T @ parameter.detach() + 0.5 * pattern).norm())
        for sign in signs:
            _check_budget(deadline)
            optimizer.zero_grad()
            # Exact published noisy-gradient oracle; no learned/agent answers.
            projected = signal.T @ parameter
            objective = 0.5 * projected.square().sum() + (0.5 * signal @ pattern * parameter).sum()
            objective.backward()
            parameter.grad.add_(noise @ noise_right.T, alpha=4 * sign)
            optimizer.step()
        residual = signal.T @ parameter.detach() + 0.5 * pattern
        arms[name] = {
            "initial_true_gradient_norm": initial_norm,
            "final_true_gradient_norm": float(residual.norm()),
            "optimizer_state_elements": _state_elements(optimizer),
            "parameter_elements": parameter.numel(),
            "updates": steps,
        }
    # A second real autograd path exercises several matrices AND AdamW biases.
    generator = torch.Generator().manual_seed(seed + 97)
    data = torch.randn(128, 16, generator=generator)
    teacher = torch.randn(16, 8, generator=generator) / 4
    targets = torch.tanh(data @ teacher)
    train_x, val_x = data[:96].to(device), data[96:].to(device)
    train_y, val_y = targets[:96].to(device), targets[96:].to(device)
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        template = nn.Sequential(nn.Linear(16, 32), nn.Tanh(), nn.Linear(32, 8))
    model_arms = {}
    for name in names:
        model = copy.deepcopy(template).to(device)
        optimizer = _optimizer(name, model.parameters())
        initial_loss = float(nn.functional.mse_loss(model(val_x), val_y).detach())
        for step in range(min(steps, 80)):
            _check_budget(deadline)
            optimizer.zero_grad()
            start = (step * 24) % len(train_x)
            loss = nn.functional.mse_loss(model(train_x[start:start + 24]), train_y[start:start + 24])
            loss.backward()
            optimizer.step()
        model_arms[name] = {
            "initial_validation_mse": initial_loss,
            "final_validation_mse": float(nn.functional.mse_loss(model(val_x), val_y).detach()),
            "optimizer_state_elements": _state_elements(optimizer),
            "parameter_elements": sum(param.numel() for param in model.parameters()),
            "updates": min(steps, 80),
        }
    if resolved.type == "cuda":
        torch.cuda.synchronize(resolved)
    protocol_digest = hashlib.sha256(json.dumps(
        {"revision": PUBLIC_REVISION, "shape": [30, 8], "signs": signs},
        sort_keys=True,
    ).encode())
    for value in (signal, noise, pattern, noise_right, initial):
        protocol_digest.update(value.detach().cpu().contiguous().numpy().tobytes())
    digest = protocol_digest.hexdigest()
    return {
        "schema_version": 2,
        "method": "smrc-pmrc",
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "evolve_eligible": False,
        "device": device,
        "accelerator": torch.cuda.get_device_name(resolved) if resolved.type == "cuda" else "CPU",
        "elapsed_seconds": time.monotonic() - started,
        "dataset": "paper-appendix-E.1.1-quadratic + seeded-small-MLP-regression",
        "dataset_revision": PUBLIC_REVISION,
        "dataset_source": PUBLIC_PROTOCOL,
        "host_reference": "NumPy FP64 SVD oracle and complete-QR protocol construction; torch CUDA kernels tested independently",
        "checkpoint_revision": "none; deterministic matrices and randomly initialized MLP",
        "public_protocol_sha256": digest,
        "budget": {"steps_per_arm": steps, "mlp_steps_per_arm": min(steps, 80),
                   "arms": len(names), "max_seconds": max_seconds},
        "numeric_controls": controls,
        "low_precision_controls": low_precision,
        "paper_quadratic": arms,
        "small_mlp": model_arms,
        "full_experiment": {
            "status": "not_reproduced_high_cost",
            "review_status": "done",
            "reason": "C4 60M–1.3B, 1.162B–26.84B tokens / multi-GPU pretraining and 7B–8B SFT omitted",
        },
        "limitations": [
            "Fixed tiny diagnostic hyperparameters, not the paper grid search or downstream comparison",
            "Synthetic real parameter updates only; not WikiText/C4 capability or wall-clock speed evidence",
            "Practical QR uses torch.linalg.qr, not authors' SCQR performance kernel",
            "No distributed state, AMP scaler/graph capture or torch.compile certification",
        ],
    }


def reproduce(dataset_dir: Path, seed: int = 42) -> dict:
    del dataset_dir
    requested = os.environ.get(DEVICE_ENV, "auto").strip().lower()
    if requested == "auto":
        requested = "cuda" if torch.cuda.is_available() else "cpu"
    if requested != "cpu" and not re.fullmatch(r"cuda(?::[0-9]+)?", requested):
        raise ValueError("SMRC/PMRC diagnostic supports CPU/CUDA; request --device cpu on Mac")
    resolved = device_for(torch, requested)
    return run_diagnostic(seed=seed, device=str(resolved))


def render(result: dict) -> str:
    rows = ["# SMRC / PMRC 低成本组件诊断", "",
            "> L1 核心组件诊断；不支持完整 LLM 预训练复现或能力提升结论。", "",
            f"seed={result['seed']}；device={result['device']}；耗时={result['elapsed_seconds']:.3f}s。", "",
            "## 数值合同", "", "| 检查 | 最大绝对误差 |", "| --- | ---: |"]
    rows += [f"| {name} | {value:.3e} |" for name, value in result["numeric_controls"].items()]
    rows += ["", "## 公开二次问题的实际参数更新", "",
             "| 优化器 | 初始真梯度范数 | 结束真梯度范数 | 持久状态元素数 |",
             "| --- | ---: | ---: | ---: |"]
    rows += [f"| {name} | {values['initial_true_gradient_norm']:.5f} | "
             f"{values['final_true_gradient_norm']:.5f} | {values['optimizer_state_elements']} |"
             for name, values in result["paper_quadratic"].items()]
    rows += ["", "## 小 MLP 实际反向传播", "",
             "| 优化器 | 初始 validation MSE | 结束 validation MSE | 持久状态元素数 |",
             "| --- | ---: | ---: | ---: |"]
    rows += [f"| {name} | {values['initial_validation_mse']:.5f} | "
             f"{values['final_validation_mse']:.5f} | {values['optimizer_state_elements']} |"
             for name, values in result["small_mlp"].items()]
    rows += ["", "完整多卡预训练、7B–8B SFT：**成本过高，不复现（审查 DONE）**。", "",
             "这些是固定预算机制诊断，允许负结果；状态元素数不是峰值显存或速度。", ""]
    return "\n".join(rows)
