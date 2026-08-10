from __future__ import annotations


def build_micro_vlm(architecture: str, dimensions: int, heads: int = 4):
    import torch

    if architecture not in {
        "micro_vlm_linear", "micro_vlm_mlp", "micro_vlm_query",
    }:
        raise ValueError(f"unknown micro-vlm architecture: {architecture}")
    if dimensions % heads:
        raise ValueError("micro-vlm dimensions must be divisible by heads")

    class MicroVLM(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.architecture = architecture
            self.patch = torch.nn.Conv2d(3, dimensions, kernel_size=8, stride=8)
            self.question = torch.nn.Embedding(3, dimensions)
            if architecture == "micro_vlm_mlp":
                self.connector = torch.nn.Sequential(
                    torch.nn.Linear(dimensions, dimensions * 2),
                    torch.nn.GELU(),
                    torch.nn.Linear(dimensions * 2, dimensions),
                )
            else:
                self.connector = torch.nn.Linear(dimensions, dimensions)
            self.query = torch.nn.Parameter(torch.zeros(1, 1, dimensions))
            torch.nn.init.normal_(self.query, std=0.02)
            self.fusion = torch.nn.Sequential(
                torch.nn.LayerNorm(dimensions * 2),
                torch.nn.Linear(dimensions * 2, dimensions),
                torch.nn.GELU(),
                torch.nn.Linear(dimensions, 9),
            )

        def forward(self, images, questions):
            patches = self.patch(images).flatten(2).transpose(1, 2)
            if self.architecture == "micro_vlm_query":
                scale = patches.shape[-1] ** -0.5
                weights = torch.softmax(
                    (patches * self.query).sum(-1) * scale, dim=-1
                )
                visual = (patches * weights.unsqueeze(-1)).sum(1)
            else:
                visual = patches.mean(1)
            visual = self.connector(visual)
            return self.fusion(torch.cat((visual, self.question(questions)), dim=-1))

        def architecture_stats(self):
            return {
                "connector": self.architecture.removeprefix("micro_vlm_"),
                "patch_size": 8,
                "visual_tokens": 16,
            }

    return MicroVLM()
