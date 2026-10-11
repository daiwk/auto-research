#!/usr/bin/env python3
"""Train a real CIFAR flow teacher, then paired DMD; never read test_batch.

This bounded pixel-space convolutional U-Net is an algorithm diagnostic, not
SongUNet/ImageNet, Inception FID-50k, or a paper-scale capability reproduction.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from functools import partial
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import sqrtm
import torch
from torch.nn import functional as F

from auto_research.foundation.data_space_iteration import (
    DMDTrainer, DataSpaceGenerator, FakeFlowNetwork, FlowRenoiseGenerator,
    SmallFlowNetwork, flow_matching_loss, rollout_data_space,
    rollout_flow_renoise, teacher_sample,
)
from auto_research.multimodal.data import (
    CIFAR10_MD5, CIFAR10_URL, _download_with_resume, _md5, _read_cifar_batches,
    _safe_extract,
)

TRAIN_MD5 = (
    "c99cafc152244af753f735de768cd75f", "d4bba439e000b95fd0a9bffe97cbabec",
    "54ebc095f3ab1f0389bbae665268c751", "634d18415352ddfa80567beed471001a",
    "482c414d41f54cd18b22e5b47cb7c3cb",
)


def cifar_train_holdout(directory, *, seed=42, train_size=1024, valid_size=256, offline=False):
    directory = Path(directory)
    extracted = directory / "cifar-10-batches-py"
    files = [extracted / f"data_batch_{i}" for i in range(1, 6)]
    archive = directory / "cifar-10-python.tar.gz"
    if not all(p.exists() for p in files):
        directory.mkdir(parents=True, exist_ok=True)
        if not archive.exists():
            if offline:
                raise FileNotFoundError("official CIFAR-10 training files missing in offline mode")
            partial_file = archive.with_suffix(".download")
            _download_with_resume(CIFAR10_URL, partial_file)
            partial_file.replace(archive)
        if _md5(archive) != CIFAR10_MD5:
            raise ValueError("official CIFAR archive checksum mismatch")
        _safe_extract(archive, directory)
    # Trust boundary before pickle deserialization. test_batch is never opened.
    for path, digest in zip(files, TRAIN_MD5, strict=True):
        if _md5(path) != digest:
            raise ValueError(f"official training file checksum mismatch: {path.name}")
    images, labels = _read_cifar_batches(files)
    if train_size < 10 or valid_size < 10 or train_size + valid_size > len(images):
        raise ValueError("invalid train-only holdout budget")
    rng = np.random.default_rng(seed)
    train_ids, valid_ids = [], []
    for label in range(10):
        ids = rng.permutation(np.flatnonzero(labels == label))
        nt, nv = train_size // 10 + (label < train_size % 10), valid_size // 10 + (label < valid_size % 10)
        train_ids.extend(ids[:nt])
        valid_ids.extend(ids[nt:nt + nv])
    train_ids, valid_ids = rng.permutation(train_ids), rng.permutation(valid_ids)
    if set(train_ids).intersection(valid_ids):
        raise AssertionError("train/validation overlap")
    payload = {"id": "CIFAR-10", "source": CIFAR10_URL, "archive_md5": CIFAR10_MD5,
        "revision": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        "train_indices_sha256": hashlib.sha256(np.asarray(train_ids, dtype="<i8").tobytes()).hexdigest(),
        "validation_indices_sha256": hashlib.sha256(np.asarray(valid_ids, dtype="<i8").tobytes()).hexdigest(),
        "train_examples": len(train_ids), "validation_examples": len(valid_ids),
        "split_seed": seed, "split_source": "official_train_only", "test_read": False}
    pixels = torch.from_numpy(images.astype(np.float32) / 127.5 - 1)
    return pixels[train_ids], pixels[valid_ids], payload


def state_digest(model):
    digest = hashlib.sha256()
    for name, value in sorted(model.state_dict().items()):
        digest.update(name.encode())
        digest.update(value.detach().cpu().numpy().tobytes())
    return digest.hexdigest()


def pixel_feature_distance(generated, reference):
    """Frechet of 8x8 average-pool pixels, deliberately NOT Inception FID."""
    arrays = [F.adaptive_avg_pool2d(x.detach().float().cpu(), (8, 8)).flatten(1).double().numpy()
              for x in (generated, reference)]
    a, b = arrays
    ma, mb, ca, cb = a.mean(0), b.mean(0), np.cov(a, rowvar=False), np.cov(b, rowvar=False)
    root = sqrtm(ca @ cb)
    if np.iscomplexobj(root):
        if abs(root.imag).max() > 1e-4:
            raise FloatingPointError("unstable feature covariance square root")
        root = root.real
    result = float(np.square(ma - mb).sum() + np.trace(ca + cb - 2 * root))
    return max(0., result)


def evaluate_samples(model, noise, validation, rollout):
    rows = []
    model.eval()
    with torch.no_grad():
        for nfe in range(1, 5):
            # Fixed evaluation seeds across every recipe/NFE, outside train RNG.
            with torch.random.fork_rng(devices=[noise.device.index or 0] if noise.is_cuda else []):
                torch.manual_seed(133742)
                sample = rollout(model, noise, nfe - 1, track_grad=False)
            rows.append({"nfe": nfe,
                "pixel_feature_frechet_distance": pixel_feature_distance(sample, validation),
                "out_of_image_range_fraction": float((sample.abs() > 1).float().mean()),
                "sample_rms": float(sample.square().mean().sqrt())})
    return rows


def run(args):
    if args.device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    if args.teacher_steps < 10 or args.distill_steps < 4 or args.batch_size < 2:
        raise ValueError("actual teacher and all four DMD prefixes require nontrivial budgets")
    train, valid, metadata = cifar_train_holdout(args.data, seed=args.split_seed,
        train_size=args.train_examples, valid_size=args.validation_examples, offline=args.offline)
    train, valid = train.to(args.device), valid.to(args.device)
    rows = []
    seeds = [int(x) for x in args.seeds.split(",")]
    if len(set(seeds)) != len(seeds):
        raise ValueError("duplicate training seeds")
    for seed in seeds:
        torch.manual_seed(seed)
        teacher = SmallFlowNetwork(args.width, args.depth).to(args.device)
        teacher_opt = torch.optim.Adam(teacher.parameters(), lr=1e-3, betas=(.9, .95))
        eval_rng = torch.Generator(device=args.device).manual_seed(seed + 20000)
        fixed_noise = torch.randn(valid.shape, generator=eval_rng, device=args.device)
        fixed_time = torch.rand(len(valid), generator=eval_rng, device=args.device)
        with torch.no_grad():
            before = float(flow_matching_loss(teacher, valid, noise=fixed_noise, time=fixed_time))
        teacher_initial = state_digest(teacher)
        for step in range(args.teacher_steps):
            indices = torch.randint(len(train), (args.batch_size,), device=args.device)
            teacher_opt.zero_grad(set_to_none=True)
            loss = flow_matching_loss(teacher, train[indices])
            if not torch.isfinite(loss):
                raise FloatingPointError("teacher training diverged")
            loss.backward()
            if any(not torch.isfinite(p.grad).all() for p in teacher.parameters() if p.grad is not None):
                raise FloatingPointError("nonfinite teacher gradient; update refused")
            teacher_opt.step()
        with torch.no_grad():
            after = float(flow_matching_loss(teacher, valid, noise=fixed_noise, time=fixed_time))
        teacher.requires_grad_(False).eval()
        teacher_sha = state_digest(teacher)
        if teacher_sha == teacher_initial:
            raise AssertionError("teacher was not trained")
        teacher_metrics = {"validation_velocity_mse_before": before,
            "validation_velocity_mse_after": after, "steps": args.teacher_steps,
            "initial_checkpoint_sha256": teacher_initial,
            "checkpoint_sha256": teacher_sha,
            "pixel_feature_frechet_distance": pixel_feature_distance(
                teacher_sample(teacher, fixed_noise, args.teacher_nfe), valid),
            "nfe": args.teacher_nfe}
        # Paired teacher/backbone init and training randomness; extra input/step
        # parameters exist only in data-space, matching the paper architecture.
        for recipe in ("flow-renoise", "data-space"):
            torch.manual_seed(seed + 1000)
            generator = (FlowRenoiseGenerator(teacher) if recipe == "flow-renoise"
                         else DataSpaceGenerator(teacher)).to(args.device)
            fake = FakeFlowNetwork(teacher).to(args.device)
            rollout = (partial(rollout_flow_renoise, refinements=4)
                       if recipe == "flow-renoise" else rollout_data_space)
            initial_generator, initial_fake = state_digest(generator), state_digest(fake)
            initial_generator_backbone = state_digest(generator.backbone)
            initial_fake_backbone = state_digest(fake.backbone)
            trainer = DMDTrainer(generator, teacher, fake,
                torch.optim.Adam(generator.parameters(), lr=1e-4, betas=(0., .95)),
                torch.optim.Adam(fake.parameters(), lr=1e-4, betas=(0., .95)), rollout=rollout)
            # Every recipe starts distillation from the same stochastic state;
            # evaluation consumes no training RNG, test is never read.
            torch.manual_seed(seed + 10000)
            trace = []
            for _ in range(args.distill_steps):
                trace.append(trainer.step(train[:args.batch_size]))  # only shape is consumed by DMD
            if state_digest(teacher) != teacher_sha:
                raise AssertionError("frozen teacher changed during DMD")
            gen_backbone_changed = state_digest(generator.backbone) != initial_generator_backbone
            fake_backbone_changed = state_digest(fake.backbone) != initial_fake_backbone
            if not gen_backbone_changed or not fake_backbone_changed:
                raise AssertionError("actual student/fake flow backbones were not trained")
            row = {"seed": seed, "recipe": recipe, "teacher": deepcopy(teacher_metrics),
                "generator_parameter_changed": state_digest(generator) != initial_generator,
                "fake_parameter_changed": state_digest(fake) != initial_fake,
                "generator_backbone_parameter_changed": gen_backbone_changed,
                "fake_backbone_parameter_changed": fake_backbone_changed,
                "generator_steps": args.distill_steps, "fake_steps": 4 * args.distill_steps,
                "trace": trace, "evaluation": evaluate_samples(trainer.ema, fixed_noise, valid, rollout),
                "checkpoint_sha256": state_digest(trainer.ema)}
            rows.append(row)
            print(json.dumps({k: v for k, v in row.items() if k not in ("trace", "evaluation")}), flush=True)
    return {"schema_version": 1, "paper_id": "2610.12102", "diagnostic_only": True,
        "evaluation_tier": "l1_core_mechanism", "dataset": metadata, "rows": rows,
        "checkpoint": {"id": "auto-research/cifar10-small-flow-unet", "initialization": "from-scratch",
            "width": args.width, "depth": args.depth, "public_pretrained_checkpoint": False},
        "protocol": {"teacher_trained": True, "teacher_frozen_during_dmd": True,
            "generator_refinements": 4, "fake_updates_per_generator": 4, "dmd_beta": [2.5, 1.],
            "dmd_weight": 1., "adam_betas": [0., .95], "ema_decay": .9999,
            "evaluation_uses_ema": True, "test_read": False, "inception_fid_evaluated": False,
            "batch_size": args.batch_size, "split_seed": args.split_seed,
            "teacher_architecture_difference": "two-scale small residual U-Net, not SongUNet-55M",
            "no_improvement_claim": True},
        "accelerator": torch.cuda.get_device_name() if args.device.startswith("cuda") else "CPU"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--split-seed", type=int, default=42)
    parser.add_argument("--train-examples", type=int, default=1024)
    parser.add_argument("--validation-examples", type=int, default=256)
    parser.add_argument("--teacher-steps", type=int, default=200)
    parser.add_argument("--distill-steps", type=int, default=128)
    parser.add_argument("--teacher-nfe", type=int, default=32)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--width", type=int, default=32)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    torch.set_num_threads(2)
    result = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
