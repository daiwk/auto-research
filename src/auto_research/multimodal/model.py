from __future__ import annotations


def build_micro_vlm(
    architecture: str,
    dimensions: int,
    heads: int = 4,
    num_questions: int = 3,
    num_answers: int = 9,
):
    import torch

    if architecture not in {
        "micro_vlm_linear", "micro_vlm_mlp", "micro_vlm_query",
        "micro_vlm_qformer", "micro_vlm_gated", "micro_vlm_pixelshuffle",
    }:
        raise ValueError(f"unknown micro-vlm architecture: {architecture}")
    if dimensions % heads:
        raise ValueError("micro-vlm dimensions must be divisible by heads")

    class MicroVLM(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.architecture = architecture
            self.patch = torch.nn.Conv2d(3, dimensions, kernel_size=8, stride=8)
            self.question = torch.nn.Embedding(num_questions, dimensions)
            if architecture in {"micro_vlm_mlp", "micro_vlm_gated"}:
                self.connector = torch.nn.Sequential(
                    torch.nn.Linear(dimensions, dimensions * 2),
                    torch.nn.GELU(),
                    torch.nn.Linear(dimensions * 2, dimensions),
                )
            else:
                self.connector = torch.nn.Linear(dimensions, dimensions)
            if architecture in {"micro_vlm_query", "micro_vlm_qformer"}:
                query_tokens = 4 if architecture == "micro_vlm_qformer" else 1
                self.query = torch.nn.Parameter(
                    torch.zeros(1, query_tokens, dimensions)
                )
                torch.nn.init.normal_(self.query, std=0.02)
            else:
                self.register_parameter("query", None)
            self.cross_attention = (
                torch.nn.MultiheadAttention(dimensions, heads, batch_first=True)
                if architecture == "micro_vlm_qformer" else None
            )
            self.pixel_projection = (
                torch.nn.Linear(dimensions * 4, dimensions)
                if architecture == "micro_vlm_pixelshuffle" else None
            )
            if architecture == "micro_vlm_gated":
                self.gate = torch.nn.Parameter(torch.tensor(0.0))
            else:
                self.register_parameter("gate", None)
            self.fusion = torch.nn.Sequential(
                torch.nn.LayerNorm(dimensions * 2),
                torch.nn.Linear(dimensions * 2, dimensions),
                torch.nn.GELU(),
                torch.nn.Linear(dimensions, num_answers),
            )

        def forward(self, images, questions):
            patches = self.patch(images).flatten(2).transpose(1, 2)
            if self.architecture == "micro_vlm_qformer":
                queries = self.query.expand(len(images), -1, -1)
                visual = self.cross_attention(queries, patches, patches)[0].mean(1)
                visual = self.connector(visual)
            elif self.architecture == "micro_vlm_pixelshuffle":
                batch, _, dimensions = patches.shape
                grid = patches.reshape(batch, 4, 4, dimensions)
                groups = grid.reshape(batch, 2, 2, 2, 2, dimensions)
                groups = groups.permute(0, 1, 3, 2, 4, 5).reshape(
                    batch, 4, dimensions * 4
                )
                visual = self.pixel_projection(groups).mean(1)
                visual = self.connector(visual)
            elif self.architecture == "micro_vlm_query":
                scale = patches.shape[-1] ** -0.5
                weights = torch.softmax(
                    (patches * self.query).sum(-1) * scale, dim=-1
                )
                visual = (patches * weights.unsqueeze(-1)).sum(1)
                visual = self.connector(visual)
            elif self.architecture == "micro_vlm_gated":
                pooled = patches.mean(1)
                visual = pooled + torch.tanh(self.gate) * self.connector(pooled)
            else:
                visual = patches.mean(1)
                visual = self.connector(visual)
            return self.fusion(torch.cat((visual, self.question(questions)), dim=-1))

        def architecture_stats(self):
            return {
                "connector": self.architecture.removeprefix("micro_vlm_"),
                "patch_size": 8,
                "visual_tokens": (
                    4 if self.architecture in {
                        "micro_vlm_qformer", "micro_vlm_pixelshuffle"
                    } else 16
                ),
                "trainable_queries": (
                    4 if self.architecture == "micro_vlm_qformer" else
                    1 if self.architecture == "micro_vlm_query" else 0
                ),
            }

    return MicroVLM()
