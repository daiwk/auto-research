"""Anchor's shared-state/read-map/gate component (arXiv:2611.04327).

An external writer owns the actual TTT/LaCT/Muon update. This module does not
replace that optimizer with a fixture or claim a complete linearized LLM.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn

REQUIRES_GPU_VALIDATION = True


@dataclass(frozen=True)
class KVState:
    matrix: torch.Tensor  # [heads, input dimension, value dimension]
    revision: int


class SharedKVReadout(nn.Module):
    """One externally written state; identity writer and learned reader bases."""
    def __init__(self, heads, key_dim, value_dim, model_dim, *, layers=(0, 1, 2), writer=0):
        super().__init__()
        if (any(type(x) is not int or x < 1 for x in (heads, key_dim, value_dim, model_dim))
                or not layers or len(set(layers)) != len(layers) or writer not in layers
                or any(type(x) is not int or x < 0 for x in layers)):
            raise ValueError('positive dimensions and distinct layers including the writer required')
        self.heads, self.key_dim, self.value_dim = heads, key_dim, value_dim
        self.layers, self.writer = tuple(layers), writer
        self.read_maps = nn.ParameterDict({str(layer): nn.Parameter(torch.eye(value_dim).repeat(heads, 1, 1))
                                          for layer in layers if layer != writer})
        self.gates = nn.ModuleDict({str(layer): nn.Linear(model_dim, heads) for layer in layers})
        for gate in self.gates.values():
            nn.init.zeros_(gate.weight)
            nn.init.constant_(gate.bias, -3.)

    def _state(self, state):
        parameter = next(self.parameters())
        if (not isinstance(state, KVState) or state.matrix.shape != (self.heads, self.key_dim, self.value_dim)
                or state.matrix.dtype != parameter.dtype or state.matrix.device != parameter.device
                or not bool(torch.isfinite(state.matrix).all()) or type(state.revision) is not int or state.revision < 0):
            raise ValueError('finite compatible same-device/dtype KVState with nonnegative integer revision required')

    def accept_write(self, old, updated, *, layer, revision):
        """Accept one external TTT result; reject reader writes and stale versions.

        No detach: callers decide whether outer-loop gradients cross their update.
        Cloning prevents subsequent mutation of the caller's source buffer.
        """
        self._state(old)
        new = KVState(updated, revision)
        self._state(new)
        if layer != self.writer or revision <= old.revision:
            raise ValueError('only the designated writer may advance the state revision')
        return KVState(updated.clone(), revision)

    def forward(self, query, local_output, hidden, state, *, layer):
        self._state(state)
        if layer not in self.layers:
            raise ValueError('unknown reader layer')
        if (query.ndim != 3 or query.shape[1:] != (self.heads, self.key_dim)
                or local_output.shape != (len(query), self.heads, self.value_dim)
                or hidden.shape != (len(query), self.gates[str(layer)].in_features)
                or not len(query) or any(t.device != state.matrix.device or t.dtype != state.matrix.dtype
                                       or not bool(torch.isfinite(t).all()) for t in (query, local_output, hidden))):
            raise ValueError('finite compatible query/local/hidden inputs required')
        raw = torch.einsum('bhd,hdv->bhv', query, state.matrix)
        memory = raw if layer == self.writer else torch.einsum('bhv,hvw->bhw', raw, self.read_maps[str(layer)])
        gate = torch.sigmoid(self.gates[str(layer)](hidden))[..., None]
        return local_output + gate * memory


def diagnostic(seed=42, device='cpu'):
    generator = torch.Generator(device=device).manual_seed(seed)
    def rand(*shape):
        return torch.randn(shape, dtype=torch.float64, device=device, generator=generator)
    model = SharedKVReadout(2, 3, 3, 4).to(device=device, dtype=torch.float64)
    old = KVState(torch.zeros(2, 3, 3, device=device, dtype=torch.float64), 0)
    # External matrix is an explicit observed KV association, not a LaCT update.
    matrix = rand(2, 3, 3)
    state = model.accept_write(old, matrix, layer=0, revision=1)
    query, hidden = rand(5, 2, 3), rand(5, 4)
    local = rand(5, 2, 3)
    writer = model(query, local, hidden, state, layer=0)
    reader = model(query, local, hidden, state, layer=1)
    identity_error = float((writer - reader).detach().abs().max())
    target = writer.detach() + .1 * rand(5, 2, 3)
    loss = (reader - target).square().mean()
    loss.backward()
    read_gradient = float(model.read_maps['1'].grad.abs().sum())
    gate_gradient = float(model.gates['1'].bias.grad.abs().sum())
    unchanged = torch.equal(old.matrix, torch.zeros_like(old.matrix))
    return {'seed': seed, 'diagnostic_only': True, 'evaluation_tier': 'l1_mechanism',
            'metrics': {'identity_reader_error': identity_error, 'read_map_gradient_l1': read_gradient,
                        'gate_gradient_l1': gate_gradient, 'written_revision': state.revision},
            'checks': {'identity_initialized_readers': identity_error < 1e-12,
                       'learnable_reader_receives_gradient': read_gradient > 0,
                       'learnable_gate_receives_gradient': gate_gradient > 0,
                       'old_state_preserved': unchanged, 'one_shared_matrix': state.matrix.numel() == 18}}
