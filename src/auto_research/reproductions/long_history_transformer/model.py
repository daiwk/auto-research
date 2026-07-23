from __future__ import annotations

from ..industrial_ranking import require_backend
from ..july_2026_common import item_feature_tensor


def build_long_history_model(data, config, recent_events: int = 4):
    torch, nn = require_backend()

    class LongHistoryRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            self.content = nn.Parameter(
                item_feature_tensor(data, config.dimensions, torch), requires_grad=False
            )
            offline_layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 3 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            online_layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 2 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.offline = nn.TransformerEncoder(offline_layer, config.layers)
            self.runtime = nn.TransformerEncoder(online_layer, 1)
            self.fusion = nn.Sequential(
                nn.Linear(3 * config.dimensions, config.dimensions),
                nn.SiLU(),
                nn.LayerNorm(config.dimensions),
            )
            self.feedback = nn.Linear(config.dimensions, data.item_features.shape[1])

        def forward(self, histories, **_):
            positions = torch.arange(histories.shape[1], device=histories.device)
            tokens = self.item(histories) + self.position(positions)
            boundary = max(1, histories.shape[1] - recent_events)
            offline_tokens = tokens[:, :boundary]
            recent_tokens = tokens[:, boundary:]
            cached = self.offline(offline_tokens)[:, -1]
            runtime = self.runtime(recent_tokens)[:, -1]
            context = self.fusion(torch.cat([cached, runtime, tokens.mean(1)], dim=-1))
            catalog = self.item.weight + self.content
            return {
                "logits": context @ catalog.T,
                "offline_logits": cached @ catalog.T,
                "feedback_logits": self.feedback(cached),
                "cache_dimensions": cached.shape[-1],
            }

    return LongHistoryRanker()


def dual_objective_loss(model, extras, logits, targets, histories, users, step, torch):
    ranking = torch.nn.functional.cross_entropy(logits, targets)
    next_item = torch.nn.functional.cross_entropy(extras["offline_logits"], targets)
    target_feedback = model.content[targets]
    feedback = torch.nn.functional.mse_loss(
        torch.sigmoid(extras["feedback_logits"]),
        torch.sigmoid(target_feedback[:, : extras["feedback_logits"].shape[1]]),
    )
    loss = ranking + 0.15 * next_item + 0.05 * feedback
    return loss, {"ranking": ranking, "next_item_pretraining": next_item, "feedback_pretraining": feedback}
