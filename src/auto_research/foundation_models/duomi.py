"""CPU-only paired shared-expert component for arXiv:2611.33952v1.

Eq. (10)-(15) and Appendix B.2, not OLMoE pretraining or LM evaluation.
Two distinct routers operate on successive hidden states of the same expert pool.
"""
from __future__ import annotations

import math
import torch
from torch import nn

REQUIRES_GPU_VALIDATION = False


def _cpu(tensor):
    if tensor.device.type != "cpu" or not tensor.is_floating_point() or not torch.isfinite(tensor).all():
        raise ValueError("finite floating CPU tensors required")


def jsd_bits(p, q):
    """JSD in bits with the continuous zero-mass convention."""
    _cpu(p)
    _cpu(q)
    if p.shape != q.shape or p.ndim < 1 or (p < 0).any() or (q < 0).any():
        raise ValueError("matching nonnegative distributions required")
    if not torch.allclose(p.sum(-1), torch.ones_like(p.sum(-1))) or not torch.allclose(q.sum(-1), torch.ones_like(q.sum(-1))):
        raise ValueError("distributions must sum to one")
    m = (p + q) / 2
    tiny = torch.finfo(p.dtype).tiny
    kl = lambda a: (a * (a.clamp_min(tiny).log() - m.clamp_min(tiny).log())).sum(-1)
    return (kl(p) + kl(q)) / (2 * math.log(2))


def duomi_penalty(logits1, logits2, valid, *, group_size=8, temperature=1.,
                  g_max=.02, d_min=.05, d_max=.30, weights=(.1,.1,.1)):
    """Pool-wise grouped penalty; average returned pool losses only afterwards.

Groups contain exactly eight sequences by default, not eight dispatched tokens.
Both invocations share one mask. Padding is removed before either statistic.
"""
    _cpu(logits1)
    _cpu(logits2)
    if logits1.shape != logits2.shape or logits1.ndim != 3 or min(logits1.shape) < 1:
        raise ValueError("paired [sequences, tokens, experts] logits required")
    if valid.device.type != "cpu" or valid.dtype != torch.bool or valid.shape != logits1.shape[:2]:
        raise ValueError("one aligned boolean CPU valid-token mask required")
    if type(group_size) is not int or group_size < 1 or logits1.shape[0] % group_size:
        raise ValueError("complete fixed-size sequence groups required")
    values = [temperature,g_max,d_min,d_max,*weights]
    if len(weights) != 3 or not all(math.isfinite(v) for v in values) or temperature <= 0:
        raise ValueError("finite temperature, thresholds and three penalty weights required")
    if not 0 <= g_max <= 1 or not 0 <= d_min <= d_max <= 1 or min(weights) < 0:
        raise ValueError("thresholds are bits in [0,1], weights are nonnegative")
    p, q = (z.div(temperature).softmax(-1) for z in (logits1,logits2))
    gs, ds, penalties = [], [], []
    for start in range(0,len(p),group_size):
        mask = valid[start:start+group_size]
        if not mask.any():
            raise ValueError("each statistical group must contain valid positions")
        a, b = p[start:start+group_size][mask], q[start:start+group_size][mask]
        g = jsd_bits(a.mean(0),b.mean(0))
        d = jsd_bits(a,b).mean()
        penalty = weights[0]*(g-g_max).relu().square() + weights[1]*(d_min-d).relu().square() + weights[2]*(d-d_max).relu().square()
        gs.append(g); ds.append(d); penalties.append(penalty)
    return torch.stack(penalties).mean(), {"g":torch.stack(gs), "d":torch.stack(ds), "penalties":torch.stack(penalties)}


class PairedSharedExperts(nn.Module):
    """Real two-round FFN dispatch; a component, not a Transformer substitute.

Norms/routers are separate. The expert ModuleList is invoked twice and shared.
The regularizer reads pre-dispatch all-expert logits; it never changes Top-k.
"""
    def __init__(self, width=8, experts=8, top_k=2):
        super().__init__()
        if min(width,experts,top_k) < 1 or top_k > experts:
            raise ValueError("positive dimensions and top_k <= experts required")
        self.top_k = top_k
        self.routers = nn.ModuleList([nn.Linear(width,experts,bias=False) for _ in range(2)])
        self.norms = nn.ModuleList([nn.LayerNorm(width) for _ in range(2)])
        self.experts = nn.ModuleList([nn.Sequential(nn.Linear(width,2*width),nn.GELU(),nn.Linear(2*width,width)) for _ in range(experts)])

    def forward(self, x):
        _cpu(x)
        if any(p.device.type != "cpu" for p in self.parameters()):
            raise ValueError("CPU-only component")
        if x.ndim != 3 or x.shape[-1] != self.routers[0].in_features:
            raise ValueError("[sequences,tokens,width] input required")
        logits, selected = [], []
        for norm, router in zip(self.norms,self.routers):
            h = norm(x)
            z = router(h)
            scores, indices = z.topk(self.top_k,dim=-1)
            probabilities = scores.softmax(-1)
            update = torch.zeros_like(x)
            for e, expert in enumerate(self.experts):
                token_weight = ((indices == e)*probabilities).sum(-1)
                active = token_weight > 0
                if active.any():
                    update[active] = update[active] + token_weight[active].unsqueeze(-1)*expert(h[active])
            x = x + update
            logits.append(z); selected.append(indices)
        return x, tuple(logits), tuple(selected)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only execution required")
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        model = PairedSharedExperts().double()
        x = torch.randn(16,4,8,dtype=torch.float64)
        valid = torch.ones(16,4,dtype=torch.bool); valid[:, -1] = False
        before = [r.weight.detach().clone() for r in model.routers]
        optimizer = torch.optim.SGD(model.parameters(),lr=.1)
        output, logits, picks = model(x)
        penalty, stats = duomi_penalty(*logits,valid,d_min=.5,d_max=.8)
        penalty.backward()
        gradients = [float(r.weight.grad.norm()) for r in model.routers]
        expert_gradient = sum(float(p.grad.norm()) for p in model.experts.parameters() if p.grad is not None)
        optimizer.step()
        # The same forward has no regularizer argument: dispatch is unchanged.
        with torch.no_grad():
            repeat, repeat_logits, repeat_picks = model(x)
            duomi_penalty(*repeat_logits,valid)
            repeat2, _, repeat_picks2 = model(x)
        detached = {k: v.detach() for k,v in stats.items()}
        p = torch.tensor([[1.,0.],[0.,1.]],dtype=torch.float64)
        q = p.flip(0)
        return {"seed":seed,"device":device,"evaluation_tier":"l1_mechanism","diagnostic_only":True,
                "checks":{"distinct_routers": model.routers[0] is not model.routers[1],
                          "two_router_gradients": all(g > 0 for g in gradients),
                          "shared_experts_receive_coupled_gradient": expert_gradient > 0,
                          "both_routers_updated": all(not torch.equal(a,r.weight) for a,r in zip(before,model.routers)),
                          "mi_ordering": bool(torch.all(detached['g'] <= detached['d']+1e-12)),
                          "aggregate_cancellation_not_token_agreement": bool(jsd_bits(p.mean(0),q.mean(0)) == 0 and jsd_bits(p,q).mean() == 1),
                          "regularizer_does_not_mutate_dispatch": bool(torch.equal(repeat,repeat2) and all(torch.equal(a,b) for a,b in zip(repeat_picks,repeat_picks2))),
                          "successive_states_not_same_logits": not torch.equal(logits[0],logits[1])},
                "metrics":{"penalty":float(penalty.detach()),"g_mean_bits":float(detached['g'].mean()),
                           "d_mean_bits":float(detached['d'].mean()),"router1_gradient_norm":gradients[0],
                           "router2_gradient_norm":gradients[1],"shared_expert_gradient_norm":expert_gradient,
                           "statistical_groups":len(stats['g']),"valid_positions":int(valid.sum())}}
