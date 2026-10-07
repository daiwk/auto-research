"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def ireko_nested_subnetwork(weight, projection, *, width: int):
    """Expose a nested post-hoc subnetwork without discarding the projection."""
    if width <= 0 or width > projection.shape[1]:
        raise ValueError("invalid requested width")
    basis = projection[:, :width]
    return basis.transpose(-1, -2) @ weight @ basis, basis
