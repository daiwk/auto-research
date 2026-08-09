from __future__ import annotations

import math

from .common import _correlation, _rotary, _sinkhorn


def build_blocks(torch, nn, config, architecture, modern, parallel, kv_heads, head_dim, RMSNorm, norm, Attention, LoopedLatentAttention, GaugeQuantizer, ConditionalMemory, FFN):
    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.first_norm, self.second_norm = norm(), norm()
            if architecture == "looped_latent_attention":
                self.attention = LoopedLatentAttention()
            elif architecture in {
                "native_sparse_attention", "nsa_gated_attention"
            }:
                from ..llm_attention_2025 import build_native_sparse_attention

                self.attention = build_native_sparse_attention(
                    torch=torch,
                    nn=nn,
                    config=config,
                    head_dim=head_dim,
                    rotary=_rotary,
                    gated=architecture == "nsa_gated_attention",
                )
            else:
                self.attention = Attention()
            self.ffn = FFN()

        def forward(self, values):
            if parallel:
                normalized = self.first_norm(values)
                return values + self.attention(normalized) + self.ffn(normalized)
            values = values + self.attention(self.first_norm(values))
            return values + self.ffn(self.second_norm(values))

    class AttentionResidualBlock(nn.Module):
        """Block AttnRes parent and role-decoupled QK/V depth routing.

        Every layer reads from all preceding residual sources. `block_attnres`
        shares one content-dependent route, while `rd_attnres` learns separate
        routes for query/key and value roles and therefore changes no residual
        source topology.
        """

        def __init__(self, source_count: int):
            super().__init__()
            self.source_count = source_count
            self.route_norm = norm()
            self.qk_route = nn.Linear(config.dimensions, source_count, bias=False)
            self.v_route = (
                nn.Linear(config.dimensions, source_count, bias=False)
                if architecture == "rd_attnres" else self.qk_route
            )
            self.attention_norm = norm()
            self.attention = Attention()
            self.ffn_norm = norm()
            self.ffn = FFN()
            self.last_route_js = 0.0

        def _route(self, stacked, router):
            current = stacked[:, :, -1]
            weights = torch.softmax(router(self.route_norm(current)), dim=-1)
            mixed = torch.einsum("btk,btkd->btd", weights, stacked)
            return mixed, weights

        def forward(self, sources):
            stacked = torch.stack(sources, dim=2)
            qk_values, qk_weights = self._route(stacked, self.qk_route)
            value_values, value_weights = self._route(stacked, self.v_route)
            midpoint = 0.5 * (qk_weights + value_weights)
            js = 0.5 * (
                qk_weights
                * torch.log((qk_weights + 1e-8) / (midpoint + 1e-8))
                + value_weights
                * torch.log((value_weights + 1e-8) / (midpoint + 1e-8))
            ).sum(-1).mean()
            self.last_route_js = float(js.detach().cpu())
            current = sources[-1]
            attended = self.attention(
                self.attention_norm(qk_values), self.attention_norm(value_values)
            )
            values = current + attended
            return values + self.ffn(self.ffn_norm(values))

    class HyperLayer(nn.Module):
        """Paper-faithful dynamic HC/mHC wrapper around one Transformer sublayer."""

        def __init__(self, function):
            super().__init__()
            streams = config.residual_streams
            self.function = function
            self.function_norm = norm()
            self.mapping_norm = nn.RMSNorm(streams * config.dimensions)
            self.dynamic = nn.Linear(
                streams * config.dimensions, streams * streams + 2 * streams,
                bias=False,
            )
            self.pre_bias = nn.Parameter(torch.zeros(streams))
            self.post_bias = nn.Parameter(torch.zeros(streams))
            self.residual_bias = nn.Parameter(torch.eye(streams))
            self.dynamic_scale = nn.Parameter(torch.tensor(0.01))

        def mappings(self, values):
            streams = config.residual_streams
            flat = self.mapping_norm(values.flatten(-2))
            raw = self.dynamic_scale * self.dynamic(flat)
            pre_raw, post_raw, residual_raw = torch.split(
                raw, (streams, streams, streams * streams), dim=-1
            )
            residual_raw = residual_raw.view(*values.shape[:-2], streams, streams)
            if architecture == "mhc":
                pre = torch.sigmoid(pre_raw + self.pre_bias)
                post = 2.0 * torch.sigmoid(post_raw + self.post_bias)
                residual = _sinkhorn(
                    residual_raw + self.residual_bias,
                    config.sinkhorn_iterations,
                    torch,
                )
            else:
                pre = pre_raw + torch.softmax(self.pre_bias, dim=-1)
                post = post_raw + torch.ones_like(self.post_bias)
                residual = residual_raw + self.residual_bias
            return pre, post, residual

        def forward(self, values):
            pre, post, residual = self.mappings(values)
            function_input = torch.einsum("...s,...sd->...d", pre, values)
            update = self.function(self.function_norm(function_input))
            carried = torch.einsum("...ij,...jd->...id", residual, values)
            return carried + post.unsqueeze(-1) * update.unsqueeze(-2)

    class HyperBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.attention = HyperLayer(Attention())
            self.ffn = HyperLayer(FFN())

        def forward(self, values):
            return self.ffn(self.attention(values))

    class LocalizedLatentRecurrence(nn.Module):
        """Penelope-style refinement localized to one decoder boundary."""

        def __init__(self, steps: int = 2):
            super().__init__()
            self.steps = steps
            self.refiner = Block()
            self.recurrent = nn.GRUCell(config.dimensions, config.dimensions)
            self.time_gate = nn.Parameter(torch.linspace(-0.5, 0.5, steps))
            self.readout = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.last_latent_steps = 0

        def forward(self, boundary):
            state = boundary
            flat_boundary = boundary.reshape(-1, config.dimensions)
            for step in range(self.steps):
                refined = self.refiner(state).reshape(-1, config.dimensions)
                recurrent = self.recurrent(refined, state.reshape(-1, config.dimensions))
                gate = torch.sigmoid(self.time_gate[step])
                state = (
                    flat_boundary + gate * self.readout(recurrent - flat_boundary)
                ).reshape_as(boundary)
            self.last_latent_steps = self.steps
            return state

    class NajuBlock(nn.Module):
        """Native-discrete selective SSM with independent retain/write gates."""

        def __init__(self):
            super().__init__()
            dimensions = config.dimensions
            self.inner = 2 * dimensions
            self.state_size = max(8, dimensions // config.heads)
            self.norm = RMSNorm()
            self.input = nn.Linear(dimensions, 2 * self.inner, bias=False)
            self.content_conv = nn.Conv1d(
                self.inner, self.inner, kernel_size=3, groups=self.inner, bias=True
            )
            self.forget = nn.Linear(self.inner, self.inner)
            self.write = nn.Linear(self.inner, self.inner)
            self.forget_conv = nn.Conv1d(
                self.inner, self.inner, kernel_size=3, groups=self.inner, bias=False
            )
            self.write_conv = nn.Conv1d(
                self.inner, self.inner, kernel_size=3, groups=self.inner, bias=False
            )
            self.bc = nn.Linear(self.inner, 2 * self.state_size, bias=False)
            self.feedthrough = nn.Parameter(torch.full((self.inner,), 0.01))
            self.output = nn.Linear(self.inner, dimensions, bias=False)
            self.readout_scale = self.state_size ** -0.5
            nn.init.constant_(self.forget.bias, 5.0)
            nn.init.constant_(self.write.bias, -2.0)
            self.last_gate_statistics = {}

        @staticmethod
        def _causal_convolution(module, values):
            width = module.kernel_size[0] - 1
            return module(torch.nn.functional.pad(values.transpose(1, 2), (width, 0))).transpose(1, 2)

        def forward(self, values):
            content, modulation = self.input(self.norm(values)).chunk(2, dim=-1)
            content = torch.nn.functional.silu(
                self._causal_convolution(self.content_conv, content)
            )
            forget = torch.sigmoid(
                self.forget(content)
                + self._causal_convolution(self.forget_conv, content)
            )
            write = torch.sigmoid(
                self.write(content)
                + self._causal_convolution(self.write_conv, content)
            )
            direction_write, direction_read = self.bc(content).chunk(2, dim=-1)
            state = torch.zeros(
                values.shape[0], self.inner, self.state_size,
                dtype=values.dtype, device=values.device,
            )
            outputs = []
            for index in range(values.shape[1]):
                state = (
                    forget[:, index, :, None] * state
                    + write[:, index, :, None]
                    * content[:, index, :, None]
                    * direction_write[:, index, None, :]
                )
                memory = torch.einsum(
                    "bis,bs->bi", state, direction_read[:, index]
                ) * self.readout_scale
                outputs.append(memory + self.feedthrough * content[:, index])
            mixed = torch.stack(outputs, dim=1)
            self.last_gate_statistics = {
                "forget_mean": float(forget.detach().mean().cpu()),
                "write_mean": float(write.detach().mean().cpu()),
                "gate_correlation": float(_correlation(forget, write, torch)),
            }
            return values + self.output(
                mixed * torch.nn.functional.silu(modulation)
            )

    class MambaBlock(nn.Module):
        """Input-dependent selective state-space recurrence (Mamba core)."""

        def __init__(self):
            super().__init__()
            d = config.dimensions
            self.norm = RMSNorm()
            self.input = nn.Linear(d, 2 * d, bias=False)
            self.conv = nn.Conv1d(d, d, 4, groups=d)
            self.delta = nn.Linear(d, d)
            self.b = nn.Linear(d, d)
            self.c = nn.Linear(d, d)
            self.a_log = nn.Parameter(torch.zeros(d))
            self.skip = nn.Parameter(torch.ones(d))
            self.output = nn.Linear(d, d, bias=False)
            self.last_selectivity = 0.0

        def forward(self, values):
            content, gate = self.input(self.norm(values)).chunk(2, dim=-1)
            content = self.conv(
                torch.nn.functional.pad(content.transpose(1, 2), (3, 0))
            ).transpose(1, 2)
            content = torch.nn.functional.silu(content)
            delta = torch.nn.functional.softplus(self.delta(content))
            decay = torch.exp(-delta * torch.exp(self.a_log))
            write = delta * self.b(content) * content
            read = self.c(content)
            state = torch.zeros_like(content[:, 0])
            outputs = []
            for index in range(content.shape[1]):
                state = decay[:, index] * state + write[:, index]
                outputs.append(read[:, index] * state + self.skip * content[:, index])
            self.last_selectivity = float(delta.detach().std().cpu())
            mixed = torch.stack(outputs, dim=1)
            return values + self.output(
                mixed * torch.nn.functional.silu(gate)
            )
    return Block, AttentionResidualBlock, HyperLayer, HyperBlock, LocalizedLatentRecurrence, NajuBlock, MambaBlock
