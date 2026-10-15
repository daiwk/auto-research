"""Bounded real CIFAR TRAIN-only comparison, not the full multi-dataset study."""
from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path
import pickle
import time

import numpy as np
import torch
from torch import Tensor, nn
from torch.nn import functional as F

from auto_research.runtime import device_for

from .algorithm import (
    GaussianAnchors, SphericalAnchors, alignment_loss, in_batch_gaussian_loss,
    simclr_loss, unit_projections,
)

SOURCE_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
TRAIN_BATCH_MD5 = "c99cafc152244af753f735de768cd75f"
PROTOCOL = "oob-cifar10-train-only-bounded-v1"
ARMS = ("sigreg_in_batch", "sigreg_oob", "simclr", "contrastive_oob")


def load_public_images(directory: Path, *, training: int, validation: int):
    """Only deserialize the checksum-verified official data_batch_1, never test."""
    candidates = (directory / "data_batch_1", directory / "cifar-10-batches-py/data_batch_1",
                  directory / "cifar10/cifar-10-batches-py/data_batch_1")
    path = next((p for p in candidates if p.is_file()), None)
    if path is None:
        raise FileNotFoundError("provide existing official CIFAR-10 data_batch_1; no download is performed")
    if path.is_symlink() or path.stat().st_size > 33_000_000:
        raise ValueError("CIFAR batch must be a bounded regular file")
    raw = path.read_bytes()
    if hashlib.md5(raw).hexdigest() != TRAIN_BATCH_MD5:
        raise ValueError("official CIFAR-10 training-batch checksum mismatch; refusing pickle")
    # CIFAR's official Python release is a pickle. Never load caller-supplied
    # arbitrary pickle: exact bytes are authenticated against torchvision's pin.
    payload = pickle.loads(raw, encoding="bytes")
    images = np.asarray(payload[b"data"])
    labels = np.asarray(payload[b"labels"], dtype=np.int64)
    if images.shape != (10000, 3072) or images.dtype != np.uint8 or labels.shape != (10000,):
        raise ValueError("unexpected official training-batch schema")
    if not (2 <= training <= 2048 and 1 <= validation <= 512 and training + validation <= len(images)):
        raise ValueError("bounded split supports 2..2048 train and 1..512 validation images")
    indices = np.random.default_rng(20261016).permutation(len(images))[:training + validation]
    selected = torch.from_numpy(images[indices].copy()).reshape(-1, 3, 32, 32).float() / 255
    y = torch.from_numpy(labels[indices].copy())
    metadata = {
        "id": "CIFAR-10", "source": SOURCE_URL, "source_file": "data_batch_1",
        "source_md5": TRAIN_BATCH_MD5, "source_sha256": hashlib.sha256(raw).hexdigest(),
        "split_revision": hashlib.sha256(indices.astype("<i8").tobytes()).hexdigest(),
        "split_seed": 20261016, "training_examples": training, "validation_examples": validation,
        "official_test_read": False, "validation_used_for_selection": False,
        "labels_used_in_ssl_objective": False,
    }
    return selected[:training], y[:training], selected[training:], y[training:], metadata


class SmallImageEncoder(nn.Module):
    """Deliberately small true image network; not the paper's ViT-S/16."""

    def __init__(self, width: int = 24, dimension: int = 32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, width, 3, padding=1), nn.GroupNorm(4, width), nn.GELU(),
            nn.AvgPool2d(2), nn.Conv2d(width, 2 * width, 3, padding=1),
            nn.GroupNorm(4, 2 * width), nn.GELU(), nn.AdaptiveAvgPool2d(1), nn.Flatten(),
        )
        self.projector = nn.Sequential(nn.Linear(2 * width, 64), nn.LayerNorm(64),
                                       nn.ReLU(), nn.Linear(64, dimension))

    def forward(self, images: Tensor) -> Tensor:
        return self.projector(self.encoder(images))


def augment(images: Tensor, generator: torch.Generator) -> Tensor:
    """Two independently sampled views, identical random stream for paired arms."""
    count = len(images)
    shift = torch.randint(0, 5, (2,), generator=generator).tolist()
    crop = F.pad(images, (2, 2, 2, 2), mode="reflect")[:, :, shift[0]:shift[0] + 32,
                                                         shift[1]:shift[1] + 32]
    flip = (torch.rand(count, generator=generator) < 0.5).to(images.device)
    crop = torch.where(flip[:, None, None, None], crop.flip(-1), crop)
    brightness = (0.7 + 0.6 * torch.rand(count, 1, 1, 1, generator=generator)).to(images.device)
    return (crop * brightness).clamp(0, 1)


@torch.no_grad()
def _represent(model: nn.Module, images: Tensor, device: str, batch_size: int = 64) -> Tensor:
    model.eval()
    values = [model(chunk.to(device)).detach().cpu() for chunk in images.split(batch_size)]
    return torch.cat(values)


def _knn(model, train, labels, validation, validation_labels, device):
    reference = F.normalize(_represent(model, train, device), dim=1)
    query = F.normalize(_represent(model, validation, device), dim=1)
    neighbors = (query @ reference.T).topk(min(5, len(reference)), dim=1).indices
    votes = F.one_hot(labels[neighbors], num_classes=10).sum(1)
    prediction = votes.argmax(1)
    return float((prediction == validation_labels).float().mean())


def run_comparison(directory: Path, *, seed: int = 42, device: str = "cpu", steps: int = 40,
                   training_examples: int = 512, validation_examples: int = 128,
                   batch_size: int = 16, refresh_interval: int = 10,
                   maximum_seconds: float = 120.0) -> dict:
    if device not in {"cpu", "cuda"} or (device == "cuda" and not torch.cuda.is_available()):
        raise ValueError("request an available CPU or real CUDA device; no silent fallback")
    if not (1 <= steps <= 120 and 2 <= batch_size <= 64 and 1 <= refresh_interval <= 40):
        raise ValueError("bounded run allows 1..120 steps, batch 2..64, refresh 1..40")
    if not (math.isfinite(maximum_seconds) and 1 <= maximum_seconds <= 180):
        raise ValueError("single-seed wall-time budget must be 1..180 seconds")
    started = time.monotonic()
    train, labels, validation, validation_labels, metadata = load_public_images(
        Path(directory), training=training_examples, validation=validation_examples,
    )
    torch.manual_seed(seed)
    initial = SmallImageEncoder()
    state = copy.deepcopy(initial.state_dict())
    results = {}
    for arm in ARMS:
        model = SmallImageEncoder().to(device)
        model.load_state_dict(state)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.05)
        generator = torch.Generator().manual_seed(seed + 100)
        cache = None
        directions = None
        refreshes, losses, ages, changed = 0, [], [], False
        for step in range(steps):
            if time.monotonic() - started > maximum_seconds:
                raise TimeoutError(f"bounded OOB budget exceeded; stopped before {arm} step {step}")
            if step % refresh_interval == 0:
                directions = unit_projections(32, 32, seed=seed + 1000 + step)
                if arm.endswith("oob"):
                    refresh_generator = torch.Generator().manual_seed(seed + 2000 + step)
                    observed = augment(train, refresh_generator)
                    representations = _represent(model, observed, device)
                    if arm == "sigreg_oob":
                        cache = GaussianAnchors.build(representations, directions, step=step)
                    else:
                        cache = SphericalAnchors.build(representations, step=step, seed=seed + step,
                                                       previous=cache)
                    refreshes += 1
            indices = torch.randperm(len(train), generator=generator)[:batch_size]
            images = train[indices].to(device)
            first_images, second_images = augment(images, generator), augment(images, generator)
            model.train()
            first, second = model(first_images), model(second_images)
            align = alignment_loss(first, second)
            if arm == "simclr":
                loss = simclr_loss(first, second)
            elif cache is not None:
                regularizer = 0.5 * (cache.loss(first, indices) + cache.loss(second, indices))
                loss = (5 if arm == "sigreg_oob" else 1) * align + regularizer
                ages.append(step - cache.refresh_step)
            else:
                loss = 5 * align + 0.5 * (in_batch_gaussian_loss(first, directions) +
                                         in_batch_gaussian_loss(second, directions))
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            if not torch.isfinite(loss) or not all(
                parameter.grad is None or torch.isfinite(parameter.grad).all() for parameter in model.parameters()
            ):
                raise FloatingPointError(f"non-finite loss or gradient in {arm}")
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1)
            optimizer.step()
            changed |= not torch.equal(model.projector[-1].weight.detach().cpu(), state["projector.3.weight"])
            losses.append(float(loss.detach()))
        if not changed:
            raise AssertionError("the real image training did not update model parameters")
        accuracy = _knn(model, train, labels, validation, validation_labels, device)
        results[arm] = {
            "validation_knn5_accuracy": accuracy, "last_training_loss": losses[-1],
            "mean_training_loss": sum(losses) / len(losses), "optimizer_steps": len(losses),
            "parameter_update_observed": changed, "refreshes": refreshes,
            "maximum_cache_age_steps": max(ages, default=0),
            "cache_cpu_resident": cache is None or cache.targets.device.type == "cpu",
            "cached_targets_require_grad": cache is not None and cache.targets.requires_grad,
            "process_peak_cuda_allocated_bytes": torch.cuda.max_memory_allocated() if device == "cuda" else None,
        }
    return {
        "schema_version": 2, "paper": "oob-regularization", "seed": seed,
        "evaluation_tier": "l2_public_dataset", "fidelity": "core_mechanism",
        "diagnostic_only": True, "promotion_eligible": False,
        "evidence_scope": "bounded public-image training comparison; not full paper capability reproduction",
        "full_experiment_status": "not_reproduced_high_cost", "dataset": metadata,
        "protocol_id": PROTOCOL, "device": device,
        "accelerator": torch.cuda.get_device_name() if device == "cuda" else "CPU",
        "configuration": {"steps_per_arm": steps, "arms": list(ARMS), "batch_size": batch_size,
                          "refresh_interval": refresh_interval, "projection_count": 32,
                          "spherical_anchor_steps": 20, "maximum_seconds": maximum_seconds,
                          "encoder": "small CNN + 64-hidden MLP, 32-dimensional projection",
                          "selection": "fixed config; validation reported only, no test or search"},
        "metrics": results,
        "paired_validation_differences": {
            "sigreg_oob_minus_in_batch": results["sigreg_oob"]["validation_knn5_accuracy"] -
                                        results["sigreg_in_batch"]["validation_knn5_accuracy"],
            "contrastive_oob_minus_simclr": results["contrastive_oob"]["validation_knn5_accuracy"] -
                                           results["simclr"]["validation_knn5_accuracy"],
        },
        "elapsed_seconds": time.monotonic() - started,
        "implementation_sha256": hashlib.sha256(
            Path(__file__).read_bytes() + Path(__file__).with_name("algorithm.py").read_bytes()
        ).hexdigest(),
    }


def reproduce(dataset_dir: Path, seed: int = 42) -> dict:
    device = device_for(torch)
    if device.type == "cuda":
        # The bounded runner uses the current CUDA device. Preserve an explicit
        # cuda:<index> resolved by the shared runtime instead of ignoring it.
        with torch.cuda.device(device):
            return run_comparison(dataset_dir, seed=seed, device="cuda")
    if device.type != "cpu":
        raise ValueError("OOB regularization supports CPU or CUDA; explicitly select --device cpu on MPS")
    return run_comparison(dataset_dir, seed=seed, device="cpu")


def render(result: dict) -> str:
    return "# OOB 有限公开图像训练\n\n非完整论文、多数据集能力比较；不自动晋级。\n\n```json\n" + json.dumps(
        result, ensure_ascii=False, indent=2
    ) + "\n```\n"
