"""SPAR RQ-PIB frozen-codebook repair, equations 13-15 and Algorithm 1.

Embeddings, training-only interaction counts and converged residual codebooks
are inputs. No claim is made to implement PATH Decoder or generative training.
"""
from __future__ import annotations

import numpy as np


def rebalance_prefixes(residuals, centers, assignments, weights, prefixes, *, tolerance=1.0):
    r, c = np.asarray(residuals, float), np.asarray(centers, float)
    z0 = np.asarray(assignments)
    w = np.asarray(weights, float)
    if (r.ndim != 2 or c.ndim != 2 or r.shape[1] != c.shape[1] or not c.shape[0]
            or z0.shape != (len(r),) or w.shape != (len(r),) or len(prefixes) != len(r)):
        raise ValueError("shape mismatch")
    if (not np.issubdtype(z0.dtype, np.integer) or np.any(z0 < 0) or np.any(z0 >= len(c))
            or np.any(w < 0) or not np.isfinite(w).all() or not np.isfinite(r).all()
            or not np.isfinite(c).all() or not np.isfinite(tolerance) or tolerance < 1):
        raise ValueError("invalid codebook, assignments, weights or tolerance")
    z = z0.copy()
    distances = ((r[:, None, :] - c[None, :, :]) ** 2).sum(-1)
    groups = {}
    for i, prefix in enumerate(prefixes):
        groups.setdefault(tuple(prefix), []).append(i)
    reports = []
    for prefix, indices in sorted(groups.items()):
        ids = np.asarray(indices, dtype=int)
        loads = np.bincount(z[ids], weights=w[ids], minlength=len(c))
        before = loads.copy()
        average = float(w[ids].sum()) / len(c)
        largest = float(w[ids].max(initial=0))
        bound = max(tolerance * average, average + (1 - 1/len(c)) * largest)
        epsilon = 1e-12 * max(1.0, bound)
        moves = []
        moved = set()
        while np.any(loads > bound + epsilon):
            source = int(np.flatnonzero(loads > bound + epsilon)[0])
            choices = []
            for i in ids:
                if z[i] != source or w[i] <= 0 or int(i) in moved:
                    continue
                feasible = np.flatnonzero((loads + w[i] <= bound + epsilon)
                                          & (np.arange(len(c)) != source))
                if feasible.size:
                    destination = min(feasible, key=lambda q: (distances[i, q], int(q)))
                    delta = distances[i, destination] - distances[i, source]
                    choices.append((float(delta), int(i), int(destination)))
            if not choices:
                raise RuntimeError("no feasible move under the paper's indivisible-load bound")
            delta, i, destination = min(choices)
            z[i] = destination
            loads[source] -= w[i]
            loads[destination] += w[i]
            moved.add(i)
            moves.append({"item_index": i, "from": source, "to": destination,
                          "distortion_increase": delta})
            if len(moves) > len(ids):
                raise RuntimeError("termination invariant violated")
        reports.append({"prefix": list(prefix), "bound": bound,
                        "loads_before": before.tolist(), "loads_after": loads.tolist(),
                        "moves": moves})
    return z, reports
