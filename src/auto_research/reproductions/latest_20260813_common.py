"""Core-mechanism reproductions selected by the 2026-08-13 audit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random

import numpy as np

from auto_research.runtime import device_for

from .llm_training import require_torch, seed_everything
from .recent_20260728_common import (
    full_catalog_metrics, load_recent_movielens, padded_histories, relative,
    training_rows,
)


@dataclass(frozen=True)
class Config:
    dimensions: int = 32
    maximum_history: int = 24
    steps: int = 50
    batch_size: int = 48
    learning_rate: float = 8e-4


def _strategy_model(data, config: Config, *, executable: bool):
    torch = require_torch(); nn = torch.nn

    class StrategyRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.encoder = nn.GRU(config.dimensions, config.dimensions, batch_first=True)
            self.policy = nn.Linear(config.dimensions, 3) if executable else None
            popularity = torch.tensor(data.popularity, dtype=torch.float32)
            popularity = popularity / popularity.max().clamp_min(1)
            self.register_buffer("popularity", popularity)

        def forward(self, histories):
            values, _ = self.encoder(self.item(histories))
            context = values[:, -1]
            relevance = context @ self.item.weight.T
            if self.policy is None:
                return relevance, None
            weights = torch.softmax(self.policy(context), dim=-1)
            novelty = -self.popularity[None].expand_as(relevance)
            category = torch.arange(data.item_count, device=relevance.device) % 8
            history_category = histories[:, -1] % 8
            affinity = (category[None] == history_category[:, None]).float()
            features = torch.stack((relevance, novelty, affinity), dim=-1)
            compiled = (features * weights[:, None]).sum(-1)
            return compiled, weights

    return StrategyRanker()


def _train_strategy(model, data, config, seed):
    torch = require_torch(); device = next(model.parameters()).device
    rows = training_rows(data, config.maximum_history); rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses, bundles = [], []
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories([row[0] for row in batch], config.maximum_history, torch, device)
        targets = torch.tensor([row[1] for row in batch], device=device)
        logits, weights = model(histories)
        loss = torch.nn.functional.cross_entropy(logits, targets)
        optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
        if weights is not None: bundles.append(weights.detach().mean(0).cpu().numpy())
    return {
        "initial_loss": float(np.mean(losses[:8])), "final_loss": float(np.mean(losses[-8:])),
        "parameters": sum(p.numel() for p in model.parameters()),
        "compiled_strategy_bundles": len(bundles) * config.batch_size,
        "mean_objective_weights": np.mean(bundles, axis=0).tolist() if bundles else None,
        "device": device.type,
    }


def _score_strategy(model, history, config):
    torch = require_torch(); device = next(model.parameters()).device
    x = padded_histories([history], config.maximum_history, torch, device)
    model.eval()
    with torch.inference_mode(): return model(x)[0][0].cpu().numpy()


def reproduce_metastrategy(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch(); data = load_recent_movielens(dataset_dir, maximum_users=260, maximum_items=420)
    config = Config(); variants = {}
    for name, executable in (("single-objective ranker", False), ("typed executable strategy", True)):
        seed_everything(seed, torch); model = _strategy_model(data, config, executable=executable).to(device_for(torch))
        variants[name] = {**_train_strategy(model, data, config, seed), **full_catalog_metrics(data, lambda h, m=model: _score_strategy(m, h, config))}
    baseline, method = variants.values()
    return {
        "paper": {"arxiv_id": "2608.09440", "title": "MetaStrategy", "url": "https://arxiv.org/abs/2608.09440", "organization": "Alibaba / Taobao"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "steps_per_model": config.steps}, "variants": variants,
        "relative": relative({k: method[k] for k in ("hit_at_10", "ndcg_at_10", "head_share_at_10")}, {k: baseline[k] for k in ("hit_at_10", "ndcg_at_10", "head_share_at_10")}),
        "paper_results": {"click_pv_percent": 2.11, "ipv_percent": 3.12, "transaction_amount_percent": 2.83},
        "scope": "实际训练 context-conditioned objective-weight policy，并把其 JSON 等价 typed bundle 通过确定性 compiler 组合 relevance、novelty 与 category affinity 后全库排序；未复刻淘宝私有生产 replay、4B→0.8B 教师蒸馏和 diff-triggered nearline serving。",
    }


def _sona_model(data, config: Config, *, semantic: bool):
    torch = require_torch(); nn = torch.nn; radix = int(np.ceil(data.item_count ** (1 / 3)))

    class Sona(nn.Module):
        def __init__(self):
            super().__init__(); self.semantic = semantic; self.radix = radix
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.encoder = nn.GRU(config.dimensions, config.dimensions, batch_first=True)
            self.codes = nn.ModuleList(nn.Linear(config.dimensions, radix) for _ in range(3))
            self.ranker = nn.Linear(3 * config.dimensions, 1)
            ids = torch.arange(data.item_count)
            self.register_buffer("sid", torch.stack((ids % radix, (ids // radix) % radix, ids // (radix * radix)), 1))

        def encode(self, histories):
            embedded = self.item(histories)
            if self.semantic and embedded.shape[1] >= 4:
                embedded = embedded.unfold(1, 4, 4).mean(-1)
            values, _ = self.encoder(embedded); return values[:, -1]

        def forward(self, histories):
            context = self.encode(histories)
            if not self.semantic: return context @ self.item.weight.T, None
            token_logp = [torch.log_softmax(head(context), -1) for head in self.codes]
            sid_score = sum(logp[:, self.sid[:, level]] for level, logp in enumerate(token_logp))
            items = self.item.weight[None].expand(len(histories), -1, -1)
            ctx = context[:, None].expand_as(items)
            rank = self.ranker(torch.cat((ctx, items, ctx * items), -1)).squeeze(-1)
            return sid_score + 0.25 * rank, token_logp

    return Sona()


def _train_sona(model, data, config, seed):
    torch = require_torch(); device = next(model.parameters()).device
    rows = training_rows(data, config.maximum_history); rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate); losses=[]; sid_targets=0
    model.train()
    for _ in range(config.steps):
        batch=[rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories=padded_histories([r[0] for r in batch], config.maximum_history, torch, device)
        targets=torch.tensor([r[1] for r in batch], device=device); logits, token_logp=model(histories)
        loss=torch.nn.functional.cross_entropy(logits, targets)
        if token_logp is not None:
            sid=model.sid[targets]
            loss += 0.2 * sum(torch.nn.functional.nll_loss(lp, sid[:, level]) for level, lp in enumerate(token_logp))
            sid_targets += int(sid.numel())
        optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return {"initial_loss":float(np.mean(losses[:8])),"final_loss":float(np.mean(losses[-8:])),"parameters":sum(p.numel() for p in model.parameters()),"semantic_id_token_targets":sid_targets,"history_compression_ratio":4.0 if model.semantic else 1.0,"device":device.type}


def reproduce_sona(dataset_dir: Path, seed: int = 42) -> dict:
    torch=require_torch(); data=load_recent_movielens(dataset_dir,maximum_users=260,maximum_items=420); config=Config(); variants={}
    for name,semantic in (("shared encoder ranker",False),("sona compressed sid + ranker",True)):
        seed_everything(seed,torch); model=_sona_model(data,config,semantic=semantic).to(device_for(torch)); training=_train_sona(model,data,config,seed)
        variants[name]={**training,**full_catalog_metrics(data,lambda h,m=model:_score_strategy(m,h,config))}
    baseline,method=variants.values()
    return {"paper":{"arxiv_id":"2608.11015","title":"Sona","url":"https://arxiv.org/abs/2608.11015","organization":"Yandex"},"dataset":{"name":"MovieLens-1M","users":len(data.train),"items":data.item_count},"setup":{"seed":seed,"steps_per_model":config.steps},"variants":variants,"relative":relative({k:method[k] for k in ("hit_at_10","ndcg_at_10","head_share_at_10")},{k:baseline[k] for k in ("hit_at_10","ndcg_at_10","head_share_at_10")}),"paper_results":{"active_users_percent":4.53,"listening_time_percent":6.30,"likes_percent":11.42},"scope":"实际训练 chronology encoder、4-event history compression、三层 autoregressive semantic-ID heads 与 item ranker；未复刻 Yandex 私有音乐语义 tokenizer、15+ 生产召回器流量和线上 serving。"}


def render_latest(result: dict) -> str:
    lines=[f"# {result['paper']['title']}","",f"公开数据：{result['dataset']['name']}（{result['dataset']['users']} users / {result['dataset']['items']} items）。","","| Variant | Hit@10 | NDCG@10 | Head share@10 | Params |","|---|---:|---:|---:|---:|"]
    for name,row in result["variants"].items(): lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | {row['head_share_at_10']:.4f} | {row['parameters']} |")
    lines += ["",f"相对同预算基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。","","## 复现边界","",result["scope"],""]
    return "\n".join(lines)
