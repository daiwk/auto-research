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


def reproduce_gas(dataset_dir: Path, seed: int = 42):
    """Reproduce GAS's removable generation branch on public image QA.

    The deployed understanding network is identical for the baseline and GAS
    run.  GAS alone receives a training-only MoT upper branch and predicts an
    EMA-stabilised sequence of continuous target-image patch embeddings.
    """
    import copy
    import torch

    data = load_fashion_mnist_qa(dataset_dir, True, maximum_examples=2000)
    device = device_for(torch)
    dimensions = 96

    class UnderstandingModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.patch = torch.nn.Conv2d(3, dimensions, 8, 8)
            self.shared_trunk = torch.nn.Sequential(
                torch.nn.LayerNorm(dimensions),
                torch.nn.Linear(dimensions, dimensions),
                torch.nn.GELU(),
            )
            layer = torch.nn.TransformerEncoderLayer(
                dimensions, 4, dimensions * 2, batch_first=True, dropout=0.0
            )
            self.understanding_upper = torch.nn.TransformerEncoder(layer, 1)
            self.question = torch.nn.Embedding(len(data.question_names), dimensions)
            self.head = torch.nn.Sequential(
                torch.nn.LayerNorm(dimensions * 2),
                torch.nn.Linear(dimensions * 2, len(data.answer_names)),
            )

        def visual_tokens(self, images):
            return self.shared_trunk(self.patch(images).flatten(2).transpose(1, 2))

        def forward(self, images, questions, return_shared=False):
            shared = self.visual_tokens(images)
            understood = self.understanding_upper(shared).mean(1)
            logits = self.head(torch.cat((understood, self.question(questions)), -1))
            return (logits, shared) if return_shared else logits

    class GenerationBranch(torch.nn.Module):
        def __init__(self):
            super().__init__()
            layer = torch.nn.TransformerEncoderLayer(
                dimensions, 4, dimensions * 2, batch_first=True, dropout=0.0
            )
            self.upper = torch.nn.TransformerEncoder(layer, 1)
            self.vision_head = torch.nn.Linear(dimensions, dimensions)

        def forward(self, shared):
            # Position i predicts target embedding i+1, matching NEP's shift.
            return self.vision_head(self.upper(shared)[:, :-1])

    def train(auxiliary: bool):
        torch.manual_seed(seed)
        np.random.seed(seed)
        model = UnderstandingModel().to(device)
        generation = GenerationBranch().to(device) if auxiliary else None
        target = copy.deepcopy(model.patch).to(device).eval()
        for parameter in target.parameters():
            parameter.requires_grad_(False)
        parameters = list(model.parameters())
        if generation is not None:
            parameters += list(generation.parameters())
        optimizer = torch.optim.AdamW(parameters, lr=2e-3)
        rng = np.random.default_rng(seed)
        losses, auxiliary_losses = [], []
        started = time.monotonic()
        model.train()
        for step in range(120):
            indices = rng.integers(0, len(data.train.answers), size=32)
            images = torch.from_numpy(data.train.images[indices]).to(device)
            questions = torch.from_numpy(data.train.questions[indices]).to(device)
            answers = torch.from_numpy(data.train.answers[indices]).to(device)
            optimizer.zero_grad(set_to_none=True)
            logits, shared = model(images, questions, return_shared=True)
            understanding_loss = torch.nn.functional.cross_entropy(logits, answers)
            loss = understanding_loss
            if generation is not None:
                # A correlated generation task: predict the horizontally mirrored
                # image in the same continuous patch space consumed by the model.
                with torch.no_grad():
                    target_tokens = target(images.flip(-1)).flatten(2).transpose(1, 2)
                predicted = generation(shared)
                generation_loss = 1 - torch.nn.functional.cosine_similarity(
                    predicted, target_tokens[:, 1:], dim=-1
                ).mean()
                weight = 0.015 + (1.0 - 0.015) * min(1.0, step / 80)
                loss = loss + weight * generation_loss
                auxiliary_losses.append(float(generation_loss.detach().cpu()))
                with torch.no_grad():
                    for ema, online in zip(target.parameters(), model.patch.parameters()):
                        ema.mul_(0.999).add_(online, alpha=0.001)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(parameters, 1.0)
            optimizer.step()
            losses.append(float(understanding_loss.detach().cpu()))
        metrics = _vqa_metrics(model, data.test)
        metrics.update({
            "deployed_parameters": sum(p.numel() for p in model.parameters()),
            "training_only_parameters": (
                sum(p.numel() for p in generation.parameters()) if generation else 0
            ),
            "initial_understanding_loss": float(np.mean(losses[:10])),
            "final_understanding_loss": float(np.mean(losses[-10:])),
            "final_generation_loss": (
                float(np.mean(auxiliary_losses[-10:])) if auxiliary_losses else None
            ),
            "duration_seconds": time.monotonic() - started,
            "device": device.type,
        })
        return metrics

    baseline = train(False)
    method = train(True)
    return {
        "paper": {"title": "GAS: Generation as Auxiliary Supervision"},
        "dataset": {
            "name": data.name,
            "train_examples": len(data.train.answers),
            "test_examples": len(data.test.answers),
        },
        "baseline": {"name": "understanding-only matched trunk", **baseline},
        "method": {"name": "GAS MoT + NEP", **method},
        "relative": {
            "test_accuracy_points": 100 * (
                method["test_accuracy"] - baseline["test_accuracy"]
            ),
            "deployed_parameter_overhead_percent": 100 * (
                method["deployed_parameters"] / baseline["deployed_parameters"] - 1
            ),
        },
        "stages": {
            "matched_steps": 120,
            "matched_seed": seed,
            "ema_decay": 0.999,
            "generation_branch_discarded_at_inference": True,
            "real_pixels": True,
        },
        "paper_results": {
            "from_scratch_overall_baseline": 47.25,
            "from_scratch_overall_gas": 48.25,
            "inference_overhead_percent": 0.0,
            "training_gpu_hours_overhead_percent": 11.6,
        },
        "scope": (
            "执行共享视觉 trunk、独立 MoT 上层、连续 next-embedding cosine loss、"
            "EMA target 和推理时删除生成分支；未复刻 Qwen3-VL 2B/4B、10M 生成数据与两阶段多机训练。"
        ),
    }


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
