from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MosaicConfig:
    dimensions: int = 32
    maximum_history: int = 32
    specialists: int = 4
    steps: int = 120
    batch_size: int = 64
    learning_rate: float = 8e-4
    redundancy_weight: float = 0.08


def build_model(data, config: MosaicConfig, *, fleet: bool):
    import torch
    from torch import nn

    features = torch.tensor(data.features, dtype=torch.float32)
    popularity = torch.tensor(data.popularity, dtype=torch.float32)
    popularity = torch.log1p(popularity) / torch.log1p(popularity.max().clamp_min(1))

    class MosaicModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.fleet = fleet
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.register_buffer("features", features)
            self.register_buffer("popularity", popularity)
            self.content = nn.Linear(features.shape[1], config.dimensions, bias=False)
            self.position = nn.Embedding(config.maximum_history, config.dimensions)
            self.sequence = nn.GRU(
                config.dimensions, config.dimensions, batch_first=True
            )
            self.memory = nn.Linear(config.dimensions, config.dimensions)
            self.dense = nn.Sequential(
                nn.Linear(features.shape[1] + 1, 2 * config.dimensions),
                nn.GELU(),
                nn.Linear(2 * config.dimensions, config.dimensions),
            )
            self.experts = nn.ModuleList(
                [
                    nn.Sequential(
                        nn.Linear(config.dimensions, 2 * config.dimensions),
                        nn.GELU(),
                        nn.Linear(2 * config.dimensions, config.dimensions),
                    )
                    for _ in range(4)
                ]
            )
            self.router = nn.Linear(config.dimensions, len(self.experts))
            specialist_count = config.specialists if fleet else 1
            self.fuse = nn.Linear(
                specialist_count * config.dimensions, config.dimensions
            )
            self.mrm = nn.Linear(
                specialist_count * config.dimensions, 4
            )

        def item_values(self, items=None):
            if items is None:
                items = torch.arange(data.item_count, device=self.features.device)
            return self.item(items) + self.content(self.features[items])

        def specialist_embeddings(self, histories):
            values = self.item_values(histories)
            positions = torch.arange(histories.shape[1], device=histories.device)
            sequential = self.sequence(values + self.position(positions))[0][:, -1]
            if not self.fleet:
                return (sequential,)
            memorization = self.memory(values[:, -1])
            mean_features = self.features[histories].mean(1)
            mean_popularity = self.popularity[histories].mean(1, keepdim=True)
            dense = self.dense(torch.cat((mean_features, mean_popularity), -1))
            base = values.mean(1)
            routing = torch.softmax(self.router(base), -1)
            expert_values = torch.stack([expert(base) for expert in self.experts], 1)
            cotrain = (routing[..., None] * expert_values).sum(1)
            return memorization, dense, sequential, cotrain

        def encode(self, histories, return_specialists=False):
            specialists = self.specialist_embeddings(histories)
            joined = torch.cat(specialists, -1)
            encoded = self.fuse(joined)
            if return_specialists:
                return encoded, specialists, self.mrm(joined)
            return encoded

        def forward(self, histories, return_specialists=False):
            encoded = self.encode(histories, return_specialists)
            if return_specialists:
                user, specialists, mrm = encoded
                return user @ self.item_values().T, specialists, mrm
            return encoded @ self.item_values().T

    return MosaicModel()


def cosine_redundancy(specialists, torch):
    values = torch.stack(
        [torch.nn.functional.normalize(value, dim=-1) for value in specialists], 1
    )
    similarity = values @ values.transpose(1, 2)
    count = similarity.shape[1]
    mask = ~torch.eye(count, dtype=torch.bool, device=similarity.device)
    return similarity[:, mask].mean()
