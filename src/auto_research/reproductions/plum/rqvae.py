from __future__ import annotations

import random
from pathlib import Path

import numpy as np


def train_rqvae(
    title_features: np.ndarray,
    genre_features: np.ndarray,
    cooccurrences: np.ndarray,
    cardinalities: tuple[int, ...],
    seed: int,
    pretrain_steps: int = 100,
    quantization_steps: int = 300,
    batch_size: int = 256,
    checkpoint_dir: Path | None = None,
) -> tuple[np.ndarray, dict[str, float]]:
    """Train the PLUM SID-v2 content RQ-VAE on public MovieLens modalities.

    The warm-up learns the two modality encoders and co-occurrence geometry.
    Residual codebooks are then initialized with k-means and jointly optimized
    with reconstruction, RQ commitment/codebook, contrastive, and progressive
    masking objectives.
    """

    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as functional
    except ImportError as exc:
        raise RuntimeError(
            "PLUM RQ-VAE needs the optional LLM dependencies; install `.[plum]`."
        ) from exc

    from .model import residual_kmeans

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    title = torch.tensor(title_features, device=device)
    genre = torch.tensor(genre_features, device=device)
    pairs = torch.tensor(cooccurrences, dtype=torch.long, device=device)

    class RQVAE(nn.Module):
        def __init__(self):
            super().__init__()
            self.title_encoder = nn.Sequential(
                nn.Linear(title.shape[1], 96), nn.GELU(), nn.Linear(96, 32)
            )
            self.genre_encoder = nn.Sequential(
                nn.Linear(genre.shape[1], 48), nn.GELU(), nn.Linear(48, 32)
            )
            self.project = nn.Sequential(nn.Linear(64, 64), nn.GELU(), nn.Linear(64, 32))
            self.title_decoder = nn.Sequential(
                nn.Linear(32, 96), nn.GELU(), nn.Linear(96, title.shape[1])
            )
            self.genre_decoder = nn.Sequential(
                nn.Linear(32, 48), nn.GELU(), nn.Linear(48, genre.shape[1])
            )
            self.codebooks = nn.ParameterList(
                [nn.Parameter(torch.empty(size, 32)) for size in cardinalities]
            )
            for codebook in self.codebooks:
                nn.init.normal_(codebook, std=0.05)

        def encode(self, title_input, genre_input):
            return self.project(
                torch.cat(
                    (self.title_encoder(title_input), self.genre_encoder(genre_input)),
                    dim=-1,
                )
            )

        def quantize(self, z, progressive: bool):
            residual = z
            quantized = torch.zeros_like(z)
            rq_loss = z.new_zeros(())
            codes = []
            depths = (
                torch.randint(1, len(self.codebooks) + 1, (len(z),), device=z.device)
                if progressive
                else torch.full((len(z),), len(self.codebooks), device=z.device)
            )
            for level, codebook in enumerate(self.codebooks):
                distances = (
                    (residual * residual).sum(-1, keepdim=True)
                    + (codebook * codebook).sum(-1)[None, :]
                    - 2.0 * residual @ codebook.T
                )
                code = distances.argmin(dim=-1)
                selected = codebook[code]
                rq_loss = rq_loss + 0.25 * functional.mse_loss(
                    residual, selected.detach()
                ) + functional.mse_loss(residual.detach(), selected)
                mask = (depths > level).to(z.dtype).unsqueeze(-1)
                quantized = quantized + mask * selected
                residual = residual - selected
                codes.append(code)
            straight_through = z + (quantized - z).detach()
            return straight_through, rq_loss, torch.stack(codes, dim=1)

        def reconstruct(self, representation):
            return self.title_decoder(representation), self.genre_decoder(representation)

    model = RQVAE().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    rng = np.random.default_rng(seed)
    warm_losses: list[float] = []
    for _ in range(pretrain_steps):
        items = torch.tensor(
            rng.integers(0, len(title), batch_size), dtype=torch.long, device=device
        )
        pair_rows = torch.tensor(
            rng.integers(0, len(pairs), batch_size), dtype=torch.long, device=device
        )
        selected_pairs = pairs[pair_rows]
        z = model.encode(title[items], genre[items])
        reconstructed_title, reconstructed_genre = model.reconstruct(z)
        reconstruction = functional.mse_loss(
            reconstructed_title, title[items]
        ) + functional.mse_loss(reconstructed_genre, genre[items])
        contrastive = _contrastive_loss(
            model.encode(title[selected_pairs[:, 0]], genre[selected_pairs[:, 0]]),
            model.encode(title[selected_pairs[:, 1]], genre[selected_pairs[:, 1]]),
            functional,
            torch,
        )
        loss = reconstruction + 0.1 * contrastive
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        warm_losses.append(float(loss.detach().cpu()))

    with torch.inference_mode():
        latent = model.encode(title, genre).detach().cpu().numpy()
    _, initial_codebooks = residual_kmeans(latent, cardinalities, seed, iterations=30)
    with torch.no_grad():
        for parameter, values in zip(model.codebooks, initial_codebooks, strict=True):
            parameter.copy_(torch.tensor(values, dtype=parameter.dtype, device=device))

    train_losses: list[float] = []
    reconstruction_losses: list[float] = []
    contrastive_losses: list[float] = []
    for _ in range(quantization_steps):
        items = torch.tensor(
            rng.integers(0, len(title), batch_size), dtype=torch.long, device=device
        )
        pair_rows = torch.tensor(
            rng.integers(0, len(pairs), batch_size), dtype=torch.long, device=device
        )
        selected_pairs = pairs[pair_rows]
        z = model.encode(title[items], genre[items])
        quantized, rq_loss, _ = model.quantize(z, progressive=True)
        reconstructed_title, reconstructed_genre = model.reconstruct(quantized)
        reconstruction = functional.mse_loss(
            reconstructed_title, title[items]
        ) + functional.mse_loss(reconstructed_genre, genre[items])
        contrastive = _contrastive_loss(
            model.encode(title[selected_pairs[:, 0]], genre[selected_pairs[:, 0]]),
            model.encode(title[selected_pairs[:, 1]], genre[selected_pairs[:, 1]]),
            functional,
            torch,
        )
        loss = reconstruction + rq_loss + 0.1 * contrastive
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        train_losses.append(float(loss.detach().cpu()))
        reconstruction_losses.append(float(reconstruction.detach().cpu()))
        contrastive_losses.append(float(contrastive.detach().cpu()))

    model.eval()
    with torch.inference_mode():
        latent = model.encode(title, genre).cpu().numpy()
    # Re-fit the deployed codebooks on the final learned latent space. This is
    # the same residual nearest-code assignment used during training, while
    # avoiding dead codes left by minibatch gradient updates on a small corpus.
    codes, deployed_codebooks = residual_kmeans(
        latent, cardinalities, seed + 1009, iterations=30
    )
    metrics = {
        "warmup_initial_loss": float(np.mean(warm_losses[:20])),
        "warmup_final_loss": float(np.mean(warm_losses[-20:])),
        "rqvae_initial_loss": float(np.mean(train_losses[:20])),
        "rqvae_final_loss": float(np.mean(train_losses[-20:])),
        "reconstruction_final_loss": float(np.mean(reconstruction_losses[-20:])),
        "contrastive_final_loss": float(np.mean(contrastive_losses[-20:])),
        "pretrain_steps": float(pretrain_steps),
        "quantization_steps": float(quantization_steps),
        "deployed_codebook_vectors": float(sum(len(x) for x in deployed_codebooks)),
    }
    if checkpoint_dir is not None:
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), checkpoint_dir / "rqvae.pt")
        np.save(checkpoint_dir / "semantic_ids.npy", codes)
    return codes.astype(np.int64), metrics


def _contrastive_loss(left, right, functional, torch):
    left = functional.normalize(left, dim=-1)
    right = functional.normalize(right, dim=-1)
    logits = left @ right.T / 0.1
    labels = torch.arange(len(left), device=left.device)
    return 0.5 * (
        functional.cross_entropy(logits, labels)
        + functional.cross_entropy(logits.T, labels)
    )
