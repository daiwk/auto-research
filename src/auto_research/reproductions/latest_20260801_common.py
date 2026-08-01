from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import time

import numpy as np

from auto_research.runtime import device_for

from .llm_training import require_torch, seed_everything
from .recent_20260728_common import (
    full_catalog_metrics,
    load_recent_movielens,
    padded_histories,
    relative,
    training_rows,
)


@dataclass(frozen=True)
class Config:
    dimensions: int = 32
    maximum_history: int = 24
    steps: int = 45
    batch_size: int = 48
    learning_rate: float = 8e-4


def _sequence_model(data, config: Config, mode: str):
    torch = require_torch()
    nn = torch.nn
    feature_count = data.features.shape[1]

    class SequenceMini(nn.Module):
        def __init__(self):
            super().__init__()
            self.mode = mode
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.feature = nn.Linear(feature_count, config.dimensions, bias=False)
            self.encoder = nn.GRU(config.dimensions, config.dimensions, batch_first=True)
            self.norm = nn.LayerNorm(config.dimensions)
            self.cross_gate = nn.Linear(2 * config.dimensions, config.dimensions)
            self.mask_token = nn.Parameter(torch.zeros(config.dimensions))
            self.register_buffer(
                "item_features", torch.tensor(data.features, dtype=torch.float32)
            )
            self.last_sequence_tokens = config.maximum_history

        def encode(self, histories):
            item = self.item(histories)
            fields = self.feature(self.item_features[histories])
            if self.mode == "ccformer":
                # Field-separated cross interaction: content is never folded
                # into the ID before its own projection and learned gate.
                gate = torch.sigmoid(self.cross_gate(torch.cat((item, fields), -1)))
                item = item + gate * fields
                # Compress in representation space: each old window retains
                # the mean ID/content signal, while the most recent eight
                # tokens remain lossless. Averaging raw IDs would be invalid.
                old, recent = item[:, :-8], item[:, -8:]
                if old.shape[1] >= 4:
                    summaries = torch.stack(
                        [chunk.mean(dim=1) for chunk in torch.chunk(old, 4, dim=1)],
                        dim=1,
                    )
                    item = torch.cat((summaries, recent), dim=1)
            encoded, _ = self.encoder(item)
            self.last_sequence_tokens = item.shape[1]
            return self.norm(encoded[:, -1])

        def forward(self, histories):
            context = self.encode(histories)
            candidates = self.item.weight
            if self.mode == "rocs":
                # DCA-like late interaction: request representation is encoded
                # once, then candidate-dependent interaction is deferred here.
                candidates = candidates + 0.25 * self.feature(self.item_features)
            return context @ candidates.T

    return SequenceMini()


def _train(model, data, config, seed, *, pretrain=False):
    torch = require_torch()
    device = device_for(torch)
    seed_everything(seed, torch)
    model.to(device).train()
    rows = training_rows(data, config.maximum_history)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    pretrain_updates = 0
    for step in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories(
            [row[0] for row in batch], config.maximum_history, torch, device
        )
        targets = torch.tensor([row[1] for row in batch], device=device)
        logits = model(histories)
        loss = torch.nn.functional.cross_entropy(logits, targets)
        if pretrain and step < config.steps // 2:
            # Open-web UFM uses MLM plus sequence-level contrast. On MovieLens,
            # held-out next items provide MLM targets and two history crops are
            # the positive pair; negatives are other rows in the batch.
            cropped = histories.clone()
            cropped[:, : config.maximum_history // 3] = cropped[:, config.maximum_history // 3 : config.maximum_history // 3 + 1]
            first, second = model.encode(histories), model.encode(cropped)
            contrast = first @ second.T / 0.2
            labels = torch.arange(len(batch), device=device)
            loss = loss + 0.25 * torch.nn.functional.cross_entropy(contrast, labels)
            pretrain_updates += 1
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:8])),
        "final_loss": float(np.mean(losses[-8:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "pretraining_updates": pretrain_updates,
        "device": device.type,
    }


def _scores(model, history, config):
    torch = require_torch()
    device = next(model.parameters()).device
    tensor = padded_histories([history], config.maximum_history, torch, device)
    model.eval()
    with torch.inference_mode():
        return model(tensor)[0].cpu().numpy()


def _run_pair(dataset_dir, seed, method_mode, *, pretrain=False):
    torch = require_torch()
    data = load_recent_movielens(dataset_dir, maximum_users=240, maximum_items=400)
    config = Config()
    variants = {}
    for name, mode, use_pretrain in (
        ("same-budget GRU baseline", "baseline", False),
        (method_mode, method_mode, pretrain),
    ):
        seed_everything(seed, torch)
        model = _sequence_model(data, config, mode)
        training = _train(model, data, config, seed, pretrain=use_pretrain)
        variants[name] = {
            **training,
            **full_catalog_metrics(
                data, lambda history, model=model: _scores(model, history, config)
            ),
            "encoded_sequence_tokens": model.last_sequence_tokens,
        }
    baseline, method = variants.values()
    return data, config, variants, relative(method, baseline)


def reproduce_ccformer(dataset_dir: Path, seed: int = 42) -> dict:
    data, config, variants, comparison = _run_pair(dataset_dir, seed, "ccformer")
    return {
        "paper": {"arxiv_id": "2607.28070", "title": "CCFormer", "url": "https://arxiv.org/abs/2607.28070", "organization": "Tencent"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "steps_per_model": config.steps},
        "variants": variants,
        "relative": comparison,
        "paper_results": {"ctr_lift_percent": 3.57, "ad_revenue_lift_percent": 1.71, "training_speedup_x": 2.21},
        "scope": "实际训练 field-separated content/ID interaction、分层旧序列压缩与 recent-token 保留；未复刻腾讯 40 亿样本、千长序列、并行多 target kernel 和线上流量。",
    }


def reproduce_open_web_ufm(dataset_dir: Path, seed: int = 42) -> dict:
    data, config, variants, comparison = _run_pair(dataset_dir, seed, "open-web-ufm", pretrain=True)
    return {
        "paper": {"arxiv_id": "2607.28019", "title": "Building a User Foundation Model for the Open Web", "url": "https://arxiv.org/abs/2607.28019", "organization": "Teads"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "steps_per_model": config.steps},
        "variants": variants,
        "relative": comparison,
        "paper_results": {"ctr_lift_percent": 2.13, "ecpc_percent": -1.13, "ctr_ranker_rig_percent": 1.354},
        "scope": "实际执行共享序列 encoder、裁剪双视图对比预训练与 next-item masked proxy，再同预算微调；未复刻 Teads RTB 特征、LLM lifter 搜索和生产 GDCN adapter。",
    }


def reproduce_rocs(dataset_dir: Path, seed: int = 42) -> dict:
    data, config, variants, comparison = _run_pair(dataset_dir, seed, "rocs")
    torch = require_torch()
    model = _sequence_model(data, config, "rocs")
    model.eval()
    histories = padded_histories([data.train[0]], config.maximum_history, torch, torch.device("cpu"))
    candidates = min(128, data.item_count)
    with torch.inference_mode():
        start = time.perf_counter()
        for candidate in range(candidates):
            _ = model(histories)[0, candidate]
        repeated_seconds = time.perf_counter() - start
        start = time.perf_counter()
        _ = model(histories)[0, :candidates]
        shared_seconds = time.perf_counter() - start
    return {
        "paper": {"arxiv_id": "2607.27744", "title": "ROCS", "url": "https://arxiv.org/abs/2607.27744", "organization": "Meta AI"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "steps_per_model": config.steps, "timed_candidates": candidates},
        "variants": variants,
        "relative": comparison,
        "request_sharing": {"repeated_seconds": repeated_seconds, "shared_seconds": shared_seconds, "measured_speedup_x": repeated_seconds / max(shared_seconds, 1e-9)},
        "paper_results": {"retrieval_qps_speedup_x": 3.0, "ranking_logloss_percent": -0.5, "ranking_qps_percent": 50.0},
        "scope": "实际执行 request encoder 单次计算、candidate late interaction 和批量候选打分，并测量同进程重复/共享路径；未复刻 Meta GLM mask、IKBO CUDA kernel 和生产集群。",
    }


def render_latest(result: dict) -> str:
    lines = [
        f"# {result['paper']['title']}", "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['users']} users / {result['dataset']['items']} items）。", "",
        "| Variant | Hit@10 | NDCG@10 | Head share@10 | Params |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | {row['head_share_at_10']:.4f} | {row['parameters']} |")
    lines += ["", f"相对同预算基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。"]
    if "request_sharing" in result:
        lines += ["", f"本地 request-sharing 微基准：{result['request_sharing']['measured_speedup_x']:.2f}x（仅解释执行路径，不代表生产 QPS）。"]
    lines += ["", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
