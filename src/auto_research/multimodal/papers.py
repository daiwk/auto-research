from __future__ import annotations

from pathlib import Path
import time

import numpy as np

from auto_research.runtime import device_for
from .data import load_fashion_mnist_qa
from .model import build_micro_vlm


def reproduce_clip(dataset_dir: Path, seed: int = 42):
    return _contrastive_reproduction(dataset_dir, seed, "clip")


def reproduce_siglip2(dataset_dir: Path, seed: int = 42):
    return _contrastive_reproduction(dataset_dir, seed, "siglip2")


def reproduce_llava(dataset_dir: Path, seed: int = 42):
    return _connector_reproduction(
        dataset_dir,
        seed,
        "micro_vlm_mlp",
        "LLaVA MLP projector",
        {"scienceqa_accuracy": 92.53, "synthetic_gpt4_relative_score_percent": 85.1},
        "执行真实像素 patch encoder、两层 projector 与 instruction 分类；未复刻 CLIP ViT-L/14、GPT-4 指令生成和 LLaMA-13B。",
    )


def reproduce_blip2(dataset_dir: Path, seed: int = 42):
    return _connector_reproduction(
        dataset_dir,
        seed,
        "micro_vlm_qformer",
        "BLIP-2 four-query Q-Former",
        {"zero_shot_vqav2_over_flamingo80b_points": 8.7, "fewer_trainable_parameters_x": 54},
        "执行四个可学习 query 对视觉 patch 的 multi-head cross-attention；未复刻冻结 ViT-g/OPT/FlanT5、两阶段大规模预训练。",
    )


def reproduce_smolvlm(dataset_dir: Path, seed: int = 42):
    return _connector_reproduction(
        dataset_dir,
        seed,
        "micro_vlm_pixelshuffle",
        "SmolVLM pixel-shuffle connector",
        {"smallest_model_parameters_million": 256, "reported_inference_memory_gb": 1.0},
        "执行 2×2 pixel shuffle，把 16 个视觉 patch 压缩为 4 个 token 后投影；未复刻 256M–2.2B decoder、视频和大规模数据配方。",
    )


def _connector_reproduction(
    dataset_dir: Path,
    seed: int,
    architecture: str,
    method_name: str,
    paper_results: dict,
    scope: str,
):
    data = load_fashion_mnist_qa(dataset_dir, True, maximum_examples=2000)
    baseline = _train_vqa(data, "micro_vlm_linear", seed)
    method = _train_vqa(data, architecture, seed)
    metric = "test_accuracy"
    return {
        "paper": {"title": method_name},
        "dataset": {
            "name": data.name,
            "train_examples": len(data.train.answers),
            "validation_examples": len(data.validation.answers),
            "test_examples": len(data.test.answers),
        },
        "baseline": {"name": "linear mean-pooled connector", **baseline},
        "method": {"name": method_name, **method},
        "relative": {
            "test_accuracy_points": 100 * (method[metric] - baseline[metric]),
            "visual_token_reduction_percent": 100 * (
                1 - method["visual_tokens"] / baseline["visual_tokens"]
            ),
        },
        "stages": {
            "real_pixels": True,
            "matched_steps": 120,
            "matched_seed": seed,
            "mandatory_visual_controls": True,
        },
        "paper_results": paper_results,
        "scope": scope,
    }


def _train_vqa(data, architecture: str, seed: int, steps: int = 120):
    import torch

    torch.manual_seed(seed)
    np.random.seed(seed)
    device = device_for(torch)
    model = build_micro_vlm(
        architecture,
        96,
        4,
        num_questions=len(data.question_names),
        num_answers=len(data.answer_names),
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3)
    rng = np.random.default_rng(seed)
    split = data.train
    started = time.monotonic()
    model.train()
    for _ in range(steps):
        indices = rng.integers(0, len(split.answers), size=32)
        images = torch.from_numpy(split.images[indices]).to(device)
        questions = torch.from_numpy(split.questions[indices]).to(device)
        answers = torch.from_numpy(split.answers[indices]).to(device)
        optimizer.zero_grad(set_to_none=True)
        loss = torch.nn.functional.cross_entropy(model(images, questions), answers)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    metrics = _vqa_metrics(model, data.test)
    metrics.update({
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "visual_tokens": model.architecture_stats()["visual_tokens"],
        "device": device.type,
        "duration_seconds": time.monotonic() - started,
    })
    return metrics


def _vqa_metrics(model, split):
    import torch

    device = next(model.parameters()).device
    images = torch.from_numpy(split.images).to(device)
    questions = torch.from_numpy(split.questions).to(device)
    answers = torch.from_numpy(split.answers).to(device)
    model.eval()
    with torch.no_grad():
        original = model(images, questions).argmax(-1)
        shuffled = model(images.roll(1, 0), questions).argmax(-1)
        blank = model(torch.zeros_like(images), questions).argmax(-1)
    accuracy = float((original == answers).float().mean().cpu())
    shuffled_accuracy = float((shuffled == answers).float().mean().cpu())
    blank_accuracy = float((blank == answers).float().mean().cpu())
    return {
        "test_accuracy": accuracy,
        "shuffled_image_accuracy": shuffled_accuracy,
        "blank_image_accuracy": blank_accuracy,
        "visual_dependency_delta": accuracy - shuffled_accuracy,
    }


def _contrastive_reproduction(dataset_dir: Path, seed: int, objective: str):
    import torch

    data = load_fashion_mnist_qa(dataset_dir, True, maximum_examples=2000)
    torch.manual_seed(seed)
    np.random.seed(seed)
    device = device_for(torch)

    class DualEncoder(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.image = torch.nn.Sequential(
                torch.nn.Conv2d(3, 48, 4, 2),
                torch.nn.GELU(),
                torch.nn.Conv2d(48, 96, 4, 2),
                torch.nn.GELU(),
                torch.nn.AdaptiveAvgPool2d(1),
                torch.nn.Flatten(),
                torch.nn.Linear(96, 96),
            )
            self.text = torch.nn.Embedding(len(data.answer_names), 96)

        def encode_image(self, images):
            return torch.nn.functional.normalize(self.image(images), dim=-1)

        def encode_text(self):
            labels = torch.arange(len(data.answer_names), device=self.text.weight.device)
            return torch.nn.functional.normalize(self.text(labels), dim=-1)

    model = DualEncoder().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3)
    rng = np.random.default_rng(seed)
    started = time.monotonic()
    losses = []
    for _ in range(150):
        indices = rng.integers(0, len(data.train.answers), size=64)
        images = torch.from_numpy(data.train.images[indices]).to(device)
        labels = torch.from_numpy(data.train.answers[indices]).to(device)
        image_features = model.encode_image(images)
        text_features = model.encode_text()
        logits = image_features @ text_features.T / 0.10
        if objective == "clip":
            image_loss = torch.nn.functional.cross_entropy(logits, labels)
            text_losses = []
            for class_index in range(len(data.answer_names)):
                positives = labels == class_index
                if positives.any():
                    column = logits[:, class_index]
                    text_losses.append(-(
                        torch.logsumexp(column[positives], 0)
                        - torch.logsumexp(column, 0)
                    ))
            loss = 0.5 * (image_loss + torch.stack(text_losses).mean())
        else:
            signs = 2 * torch.nn.functional.one_hot(
                labels, len(data.answer_names)
            ).float() - 1
            loss = torch.nn.functional.softplus(-signs * logits).mean()
            masked = images.clone()
            masked[:, :, 8:24, 8:24] = 0
            masked_logits = model.encode_image(masked) @ text_features.T / 0.10
            loss = loss + 0.15 * torch.nn.functional.mse_loss(
                torch.sigmoid(masked_logits), torch.sigmoid(logits.detach())
            )
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))

    test_images = torch.from_numpy(data.test.images).to(device)
    test_labels = torch.from_numpy(data.test.answers).to(device)
    with torch.no_grad():
        text_features = model.encode_text()
        logits = model.encode_image(test_images) @ text_features.T
        shuffled = model.encode_image(test_images.roll(1, 0)) @ text_features.T
        accuracy = float((logits.argmax(-1) == test_labels).float().mean().cpu())
        shuffled_accuracy = float((shuffled.argmax(-1) == test_labels).float().mean().cpu())
    names = {
        "clip": "symmetric CLIP-style contrastive encoder",
        "siglip2": "SigLIP 2 sigmoid + masked-view self-distillation",
    }
    paper_results = (
        {"imagenet_zero_shot_top1": 76.2, "pretraining_pairs_million": 400}
        if objective == "clip"
        else {
            "reported_improvement_over_siglip_at_all_scales": True,
            "released_model_sizes": 4,
        }
    )
    return {
        "paper": {"title": names[objective]},
        "dataset": {"name": data.name, "pairs": len(data.train.answers), "test": len(data.test.answers)},
        "baseline": {"name": "uniform label retrieval", "test_accuracy": 0.1},
        "method": {
            "name": names[objective], "test_accuracy": accuracy,
            "shuffled_image_accuracy": shuffled_accuracy,
            "visual_dependency_delta": accuracy - shuffled_accuracy,
            "parameters": sum(parameter.numel() for parameter in model.parameters()),
        },
        "relative": {"test_accuracy_points": 100 * (accuracy - 0.1)},
        "stages": {
            "steps": 150, "initial_loss": float(np.mean(losses[:10])),
            "final_loss": float(np.mean(losses[-10:])), "device": device.type,
            "duration_seconds": time.monotonic() - started,
        },
        "paper_results": paper_results,
        "scope": (
            "在 Fashion-MNIST 真实图像/类别文本对上训练双塔与对称多正例 InfoNCE；未复刻 4 亿图文对和大型 ViT。"
            if objective == "clip" else
            "在真实图文对上训练 sigmoid 对比目标和 masked-view 自蒸馏；未复刻多语言 web 数据、caption decoder 与 dense localization。"
        ),
    }
