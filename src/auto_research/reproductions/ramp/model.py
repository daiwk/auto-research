from __future__ import annotations

from ..industrial_ranking import require_backend
from ..july_2026_common import item_feature_tensor


def build_privacy_ranker(data, config, ramp: bool):
    torch, nn = require_backend()

    class PrivacyRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.ramp = ramp
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.content = nn.Parameter(
                item_feature_tensor(data, config.dimensions, torch), requires_grad=False
            )
            self.personalized = nn.Sequential(
                nn.Linear(2 * config.dimensions, config.dimensions), nn.SiLU(), nn.LayerNorm(config.dimensions)
            )
            self.nonpersonalized = nn.Sequential(
                nn.Linear(2 * config.dimensions, config.dimensions), nn.SiLU(), nn.LayerNorm(config.dimensions)
            )
            self.alignment = nn.Sequential(
                nn.Linear(2 * config.dimensions, config.dimensions), nn.SiLU(), nn.LayerNorm(config.dimensions)
            )
            self.shared = nn.Sequential(
                nn.Linear(2 * config.dimensions, config.dimensions), nn.SiLU(), nn.LayerNorm(config.dimensions)
            )

        def forward(self, histories, users=None, training_step=0, mode=None, **_):
            behavior = self.item(histories).mean(1)
            public = self.content[histories].mean(1)
            recent_public = self.content[histories[:, -1]]
            catalog = self.item.weight + self.content
            if users is None:
                consent = torch.zeros(histories.shape[0], dtype=torch.bool, device=histories.device)
            else:
                consent = ((users + training_step) % 5) != 0
            if mode == "personalized":
                consent = torch.ones_like(consent)
            elif mode == "non_personalized":
                consent = torch.zeros_like(consent)
            if not self.ramp:
                masked_behavior = behavior * consent[:, None]
                context = self.shared(torch.cat([masked_behavior, public], dim=-1))
                return {"logits": context @ catalog.T, "consent": consent}
            personalized = self.personalized(torch.cat([behavior, public], dim=-1))
            nonpersonalized = self.nonpersonalized(torch.cat([recent_public, public], dim=-1))
            aligned = self.alignment(torch.cat([nonpersonalized, public], dim=-1))
            personalized_logits = personalized @ catalog.T
            nonpersonalized_logits = nonpersonalized @ catalog.T
            aligned_logits = aligned @ catalog.T
            selected = torch.where(consent[:, None], personalized_logits, nonpersonalized_logits)
            return {
                "logits": selected,
                "personalized_logits": personalized_logits,
                "nonpersonalized_logits": nonpersonalized_logits,
                "alignment_logits": aligned_logits,
                "consent": consent,
            }

    return PrivacyRanker()


def ramp_loss(model, extras, logits, targets, histories, users, step, torch):
    ranking = torch.nn.functional.cross_entropy(logits, targets)
    teacher = torch.softmax(extras["personalized_logits"].detach(), dim=-1)
    student = torch.log_softmax(extras["alignment_logits"], dim=-1)
    alignment = torch.nn.functional.kl_div(student, teacher, reduction="batchmean")
    nonpersonalized = ~extras["consent"]
    if nonpersonalized.any():
        restricted = torch.nn.functional.cross_entropy(
            extras["nonpersonalized_logits"][nonpersonalized], targets[nonpersonalized]
        )
    else:
        restricted = ranking.new_zeros(())
    loss = ranking + 0.15 * alignment + 0.25 * restricted
    return loss, {"masked_ranking": ranking, "prediction_alignment": alignment, "restricted_path": restricted}
