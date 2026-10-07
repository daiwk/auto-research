"""Extracted unchanged from auto_research.recommendation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def basis_vq(latents, basis, codebook):
    """GEAR BasisVQ assignment in a shared orthogonal coordinate system."""
    import torch

    if basis.ndim != 2 or codebook.ndim != 2 or latents.shape[-1] != basis.shape[0]:
        raise ValueError("incompatible BasisVQ shapes")
    rotated = latents @ basis
    distances = torch.cdist(rotated, codebook)
    indices = distances.argmin(-1)
    quantized = codebook[indices] @ basis.T
    return quantized, indices
