"""CAMAR Eq5-7/9-15 on supplied domain states/candidates; no item backbone.

One shared attention layer, bias-free linear factor maps, width-preserving
two-layer PCNs/classifier and epsilon1e-12 normalization are local architectural
choices where the source leaves implementation detail unspecified.
"""
from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


class _Reverse(torch.autograd.Function):
    @staticmethod
    def forward(ctx, value, coefficient):
        ctx.coefficient = coefficient
        return value.view_as(value)

    @staticmethod
    def backward(ctx, gradient):
        return -ctx.coefficient * gradient, None


def reverse(value, coefficient: float):
    if not 0 <= coefficient <= 1:
        raise ValueError("GRL warmup coefficient must be in [0,1]")
    return _Reverse.apply(value, coefficient)


class PreferenceCore(nn.Module):
    def __init__(self, domains: int, width: int):
        super().__init__()
        if domains < 3 or width < 1:
            raise ValueError("CAMAR requires at least three domains and positive width")
        self.domains, self.width = domains, width
        self.pcn = nn.ModuleDict({f"{s}_{t}": nn.Sequential(nn.Linear(width, width), nn.ReLU(), nn.Linear(width, width))
                                  for s in range(domains) for t in range(domains) if s != t})
        self.invariant = nn.ModuleList(nn.Linear(width, width, bias=False) for _ in range(domains))
        self.specific = nn.ModuleList(nn.Linear(width, width, bias=False) for _ in range(domains))
        self.attention = nn.MultiheadAttention(width, 1, dropout=0, batch_first=True)
        self.gates = nn.ModuleList(nn.Linear(2*width, width) for _ in range(domains))
        self.classifier = nn.Sequential(nn.Linear(width, width), nn.ReLU(), nn.Linear(width, domains))

    def _check(self, states, active):
        if states.ndim != 3 or states.shape[1:] != (self.domains, self.width):
            raise ValueError("expected [users,domains,width] states")
        if active.shape != states.shape[:2] or active.dtype != torch.bool or active.device != states.device:
            raise ValueError("aligned same-device boolean active mask required")
        if not bool(active.any(1).all()) or not bool(torch.isfinite(states).all()):
            raise ValueError("finite states and at least one active domain per user required")

    def complete(self, states, active):
        self._check(states, active)
        count = active.sum(1, keepdim=True).to(states.dtype)
        outputs = []
        for t in range(self.domains):
            guesses = sum(self.pcn[f"{s}_{t}"](states[:, s].detach()) * active[:, s, None]
                          for s in range(self.domains) if s != t)
            outputs.append(torch.where(active[:, t, None], states[:, t], guesses/count))
        return torch.stack(outputs, 1)

    def representation_loss(self, states, active):
        self._check(states, active)
        terms = []
        for s in range(self.domains):
            for t in range(self.domains):
                overlap = active[:, s] & active[:, t]
                if s != t and bool(overlap.any()):
                    prediction = self.pcn[f"{s}_{t}"](states[overlap, s].detach())
                    terms.append((prediction-states[overlap, t].detach()).square().sum(-1).mean())
        if not terms:
            raise ValueError("representation supervision needs overlapping active domains")
        return torch.stack(terms).mean()

    def mix_factors(self, invariant, specific, active):
        self._check(invariant, active)
        self._check(specific, active)
        attended, _ = self.attention(invariant, invariant, invariant, key_padding_mask=~active, need_weights=False)
        attended = torch.where(active[:, :, None], attended, invariant)
        shared = (attended*active[:, :, None]).sum(1)/active.sum(1, keepdim=True)
        users = []
        for d in range(self.domains):
            gate = self.gates[d](torch.cat((shared, specific[:, d]), -1)).sigmoid()
            users.append(F.normalize(gate*shared + (1-gate)*specific[:, d], dim=-1, eps=1e-12))
        return {"users": torch.stack(users, 1), "shared": shared, "invariant": invariant,
                "specific": specific, "attended": attended}

    def forward(self, states, active):
        completed = self.complete(states, active)
        invariant = torch.stack([layer(completed[:, d]) for d, layer in enumerate(self.invariant)], 1)
        specific = torch.stack([layer(completed[:, d]) for d, layer in enumerate(self.specific)], 1)
        return self.mix_factors(invariant, specific, active)

    def orthogonality_loss(self, invariant, specific, active):
        self._check(invariant, active)
        self._check(specific, active)
        dots = (invariant*specific).sum(-1).square()
        # Dataset Ud can be empty in a mini-batch: local zero contribution,
        # retaining Eq10's denominator |D| rather than reweighting active domains.
        return sum(dots[active[:, d], d].mean() if bool(active[:, d].any()) else dots[:, d].sum()*0
                   for d in range(self.domains))/self.domains

    def adversarial_loss(self, invariant, coefficient):
        logits = self.classifier(reverse(invariant, coefficient))
        labels = torch.arange(self.domains, device=invariant.device).expand(invariant.shape[0], -1)
        return F.cross_entropy(logits.reshape(-1, self.domains), labels.reshape(-1))

    def recall_loss(self, users, candidates, active):
        self._check(users, active)
        if candidates.ndim != 4 or candidates.shape[:2] != users.shape[:2] or candidates.shape[-1] != self.width or candidates.shape[2] < 2:
            raise ValueError("candidates require [users,domains,positive+negatives,width]")
        if not bool(torch.isfinite(candidates).all()):
            raise ValueError("finite candidate vectors required")
        scores = (users[:, :, None, :]*candidates).sum(-1)
        return sum(F.cross_entropy(scores[active[:, d], d], torch.zeros(int(active[:, d].sum()), dtype=torch.long, device=users.device))
                   if bool(active[:, d].any()) else scores[:, d].sum()*0 for d in range(self.domains))


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"}:
        raise ValueError("diagnostic supports cpu or cuda")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable")
    torch.manual_seed(seed)
    core = PreferenceCore(3, 8).to(device=device, dtype=torch.float64)
    states = torch.randn(4, 3, 8, dtype=torch.float64, device=device, requires_grad=True)
    active = torch.tensor([[True, True, True], [True, False, True], [False, True, False], [True, True, False]], device=device)
    completion = core.complete(states, active)
    isolated_grad = torch.autograd.grad(completion[~active].sum(), states, allow_unused=True)[0]
    rep = core.representation_loss(states, active)
    rep_grad = torch.autograd.grad(rep, states, allow_unused=True)[0]
    inv = torch.randn_like(states).detach().requires_grad_()
    positive = F.cross_entropy(core.classifier(inv).reshape(-1, 3), torch.arange(3, device=device).expand(4, -1).reshape(-1))
    gp = torch.autograd.grad(positive, inv)[0]
    gn = torch.autograd.grad(core.adversarial_loss(inv, .6), inv)[0]
    specific = torch.randn_like(states)
    factors = core.mix_factors(inv.detach(), specific, active)
    altered = specific.clone(); altered[:, 1] += 5
    shifted = core.mix_factors(inv.detach(), altered, active)
    imputed = inv.detach().clone(); imputed[~active] += 1000
    masked = core.mix_factors(imputed, specific, active)
    output = core(states, active)
    candidates = torch.randn(4, 3, 5, 8, dtype=torch.float64, device=device)
    loss = core.recall_loss(output["users"], candidates, active) + .1*rep + .2*core.orthogonality_loss(output["invariant"], output["specific"], active) + .1*core.adversarial_loss(output["invariant"], .6)
    optimizer = torch.optim.Adam(core.parameters(), lr=.001)
    before = core.invariant[0].weight.detach().clone()
    optimizer.zero_grad(); loss.backward(); optimizer.step()
    checks = {"inactive_imputation_stops_source_gradient": isolated_grad is None or bool((isolated_grad == 0).all()),
              "representation_targets_and_sources_stopped": rep_grad is None or bool((rep_grad == 0).all()),
              "grl_reverses_only_adversarial_input": torch.allclose(gn, -.6*gp, atol=1e-12, rtol=1e-10),
              "specific_factor_does_not_cross_domains": torch.allclose(factors["users"][:, 0], shifted["users"][:, 0], atol=1e-12),
              "specific_factor_changes_own_output": not torch.allclose(factors["users"][:, 1], shifted["users"][:, 1]),
              "inactive_invariant_cannot_contaminate_shared": torch.allclose(factors["shared"], masked["shared"], atol=1e-12),
              "finite_actual_update": bool(torch.isfinite(loss)) and not torch.equal(before, core.invariant[0].weight),
              "l2_user_vectors": torch.allclose(output["users"].norm(dim=-1), torch.ones(4, 3, device=device, dtype=torch.float64), atol=1e-12)}
    if device == "cuda":
        torch.cuda.synchronize()
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"synthetic_joint_loss": float(loss.detach()), "representation_loss": float(rep.detach()),
             "grl_max_error": float((gn+.6*gp).abs().max().detach()), "specific_cross_domain_max_error": float((factors["users"][:, 0]-shifted["users"][:, 0]).abs().max().detach())}}
