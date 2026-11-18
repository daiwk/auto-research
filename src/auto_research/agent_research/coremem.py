"""CoReMem v1 success-first reward, traceable-use credit and exact PG kernel.

Inputs are externally observed training rollouts, not gold-bearing actor views.
No coding actor, semantic anchor extractor, memory generator or replay is supplied.
"""
from dataclasses import dataclass
import math
from numbers import Real

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/coremem-a100-20261115.json"
ARMS = ("no_memory", "own_memory", "misplaced")


def _finite(value):
    return not isinstance(value, bool) and isinstance(value, Real) and math.isfinite(value)


@dataclass(frozen=True)
class ReplayOutcome:
    """Evaluator-only result; paired arms must inherit precisely the same state."""
    boundary_id: str
    inherited_state_id: str
    arm: str
    resolved: bool
    steps: int
    fractional_progress: float = 0.

    def __post_init__(self):
        if any(not isinstance(x, str) or not x.strip() for x in (self.boundary_id, self.inherited_state_id)):
            raise ValueError("explicit boundary and inherited-state identities required")
        if self.arm not in ARMS or type(self.resolved) is not bool or type(self.steps) is not int or self.steps < 0:
            raise ValueError("typed replay arm, resolution and nonnegative steps required")
        if not _finite(self.fractional_progress) or not 0 <= self.fractional_progress <= 1:
            raise ValueError("fractional evaluator progress must be in [0,1]")


def success_first_reward(outcome: ReplayOutcome, *, max_steps: int, win=250., alpha=50.):
    """Eq4: W-steps on success, alpha*f on failure; all successes dominate."""
    if not isinstance(outcome, ReplayOutcome) or type(max_steps) is not int or max_steps < 1:
        raise ValueError("typed evaluator outcome and positive step budget required")
    if not _finite(win) or not _finite(alpha) or alpha < 0 or win <= max_steps + alpha:
        raise ValueError("success-first guarantee requires W > max_steps + alpha")
    if outcome.steps > max_steps:
        raise ValueError("observed steps exceed the declared reward budget")
    return win - outcome.steps if outcome.resolved else alpha * outcome.fractional_progress


def paired_step_saving(empty: ReplayOutcome, memory: ReplayOutcome):
    """Eq2's observed saving, not an estimate from nonidentical inherited trees."""
    if not isinstance(empty, ReplayOutcome) or not isinstance(memory, ReplayOutcome):
        raise ValueError("two typed evaluator outcomes required")
    if empty.arm != "no_memory" or memory.arm != "own_memory":
        raise ValueError("compare no-memory against own-memory")
    if (empty.boundary_id, empty.inherited_state_id) != (memory.boundary_id, memory.inherited_state_id):
        raise ValueError("paired replay must use the identical inherited state and boundary")
    return empty.steps - memory.steps


def _anchors(values):
    if isinstance(values, (str, bytes)):
        raise ValueError("explicit externally extracted anchor collections required")
    result = frozenset(values)
    if any(not isinstance(x, str) or not x.strip() for x in result):
        raise ValueError("nonempty exact anchor identities required")
    return result


def provenance_gates(step_anchors, memory_anchors, prior_anchors, no_memory_siblings, *, prefix_steps=8):
    """Eq6: first-use anchor in memory, absent from prior/no-memory prefixes.

    Anchor extraction is external. A true gate is traceable use, not proof that
    memory caused success. Injected memory itself must not be in prior_anchors.
    """
    if type(prefix_steps) is not int or prefix_steps < 1:
        raise ValueError("positive no-memory prefix length required")
    memory, seen = _anchors(memory_anchors), set(_anchors(prior_anchors))
    counterfactual = set()
    for sibling in no_memory_siblings:
        if isinstance(sibling, (str, bytes)):
            raise ValueError("sibling trajectories must be stepwise anchor collections")
        for anchors in tuple(sibling)[:prefix_steps]:
            counterfactual.update(_anchors(anchors))
    gates = []
    for anchors in step_anchors:
        current = _anchors(anchors)
        gates.append(bool((current & memory) - seen - counterfactual))
        seen.update(current)
    return tuple(gates)


def step_advantages(rewards, arms, gates, valid_steps, *, scale=100.):
    """Eq7 with the paper's fixed scale; baselines come from one replay boundary.

    All arguments are trainer-only. The caller must pair inherited states before
    forming a group; ReplayOutcome/paired_step_saving validates individual pairs.
    """
    import torch
    if not all(isinstance(x, torch.Tensor) for x in (rewards, gates, valid_steps)):
        raise ValueError("actual reward and step tensors required")
    if rewards.ndim != 1 or gates.ndim != 2 or gates.shape != valid_steps.shape or gates.shape[0] != len(rewards):
        raise ValueError("reward [session] and matching gate/mask [session,step] required")
    if not rewards.is_floating_point() or gates.dtype != torch.bool or valid_steps.dtype != torch.bool:
        raise ValueError("floating rewards and boolean step masks required")
    if any(x.device != rewards.device for x in (gates, valid_steps)) or not torch.isfinite(rewards).all():
        raise ValueError("finite tensors on one device required")
    arms = tuple(arms)
    if len(arms) != len(rewards) or any(a not in ARMS for a in arms) or not all(a in arms for a in ARMS[:2]):
        raise ValueError("explicit own/no-memory arms and valid arm for every session required")
    if not _finite(scale) or scale <= 0 or not valid_steps.any(dim=1).all() or (gates & ~valid_steps).any():
        raise ValueError("positive fixed scale and nonempty valid session steps required")
    empty = torch.tensor([a == "no_memory" for a in arms], device=rewards.device)
    own = torch.tensor([a == "own_memory" for a in arms], device=rewards.device)
    r = rewards.detach()
    empty_mean, own_mean = r[empty].mean(), r[own].mean()
    value = own_mean - empty_mean
    baseline = torch.where(own, own_mean, empty_mean)
    result = (r - baseline)[:, None].expand_as(gates).clone() / scale
    result += (own[:, None] & gates).to(r.dtype) * value / scale
    return result.masked_fill(~valid_steps, 0), value


def policy_gradient_loss(log_probs, advantages, token_steps, valid_tokens, *, reduction="token_mean", reference_kl=None, beta=.2):
    """AppendixA Eq9: actual token PG plus optional reference KL.

    token_mean is the 27B recipe; session_mean first normalizes each session as
    the 9B recipe. Externally measured reference KL is mandatory for beta>0.
    """
    import torch
    xs = (log_probs, advantages, token_steps, valid_tokens)
    if not all(isinstance(x, torch.Tensor) for x in xs) or log_probs.ndim != 2 or advantages.ndim != 2:
        raise ValueError("actual session/token and session/step tensors required")
    if token_steps.shape != log_probs.shape or valid_tokens.shape != log_probs.shape or advantages.shape[0] != log_probs.shape[0]:
        raise ValueError("matching token map/mask and session count required")
    if not log_probs.is_floating_point() or not advantages.is_floating_point() or token_steps.dtype != torch.long or valid_tokens.dtype != torch.bool:
        raise ValueError("floating log probabilities/advantages, int64 map and boolean mask required")
    if any(x.device != log_probs.device for x in xs) or not torch.isfinite(log_probs).all() or not torch.isfinite(advantages).all() or (log_probs > 0).any():
        raise ValueError("finite valid log probabilities and same-device tensors required")
    if not valid_tokens.any(dim=1).all() or ((token_steps[valid_tokens] < 0) | (token_steps[valid_tokens] >= advantages.shape[1])).any():
        raise ValueError("each session needs tokens mapped to actual valid steps")
    if reduction not in ("token_mean", "session_mean") or not _finite(beta) or beta < 0:
        raise ValueError("explicit paper reduction and nonnegative KL coefficient required")
    safe_steps = token_steps.masked_fill(~valid_tokens, 0)
    token_adv = advantages.detach().gather(1, safe_steps)
    terms = -log_probs * token_adv
    if beta:
        if not isinstance(reference_kl, torch.Tensor) or reference_kl.shape != log_probs.shape or reference_kl.device != log_probs.device or not reference_kl.is_floating_point() or not torch.isfinite(reference_kl).all() or (reference_kl[valid_tokens] < 0).any():
            raise ValueError("explicit finite nonnegative reference KL on generated tokens required")
        terms = terms + beta * reference_kl
    terms = terms.masked_fill(~valid_tokens, 0)
    return terms.sum() / valid_tokens.sum() if reduction == "token_mean" else (terms.sum(1) / valid_tokens.sum(1)).mean()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    import torch
    if type(seed) is not int or device not in ("cpu", "cuda"):
        raise ValueError("integer seed and cpu/cuda required")
    torch.manual_seed(seed)
    gates = provenance_gates([{"old"}, {"new"}, {"new"}, {"sibling"}], {"old", "new", "sibling"}, {"old"}, [[{"sibling"}]])
    rewards = torch.tensor([10., 30., 50., 70.], device=device, requires_grad=True)
    arms = ("no_memory", "no_memory", "own_memory", "own_memory")
    mask = torch.ones((4,2), dtype=torch.bool, device=device)
    gate = torch.tensor([[False,False],[False,False],[True,False],[False,True]], device=device)
    adv, value = step_advantages(rewards, arms, gate, mask)
    logits = torch.randn((4,3,3), device=device, requires_grad=True)
    logs = logits.log_softmax(-1)[...,0]
    token_mask = torch.tensor([[True,True,False]]*4, device=device)
    steps = torch.tensor([[0,1,-1]]*4, device=device)
    loss = policy_gradient_loss(logs, adv, steps, token_mask, beta=0.)
    loss.backward()
    checks = {"actual_tensor_device": logits.device.type == device,
              "first_use_and_sibling_exclusion": gates == (False,True,False,False),
              "fixed_scale_memory_value": math.isclose(value.item(), 40.) and math.isclose(adv[2,0].item(), .3, abs_tol=1e-6),
              "outcome_credit_retained_without_gate": math.isclose(adv[2,1].item(), -.1, abs_tol=1e-6),
              "no_gradient_into_evaluator_rewards": rewards.grad is None,
              "padding_gradient_zero": bool((logits.grad[:,2] == 0).all()),
              "real_policy_gradient": bool((logits.grad[:,:2] != 0).any())}
    return {"seed":seed,"execution_device":logits.device.type,"diagnostic_only":True,"evaluation_tier":"l1_mechanism",
            "checks":checks,"metrics":{"policy_gradient_loss":loss.item(),"memory_value":value.item(),"traceable_use_steps":sum(gates)}}
