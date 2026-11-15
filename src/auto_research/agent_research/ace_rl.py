"""ACE-RL v1 task-local playbook controls and role-specific GRPO loss.

No model, reflection generator, environment verifier or benchmark bridge is
supplied. Rewards are trainer/evaluator inputs, never exposed to an actor view.
"""
from dataclasses import dataclass
import math
from numbers import Real
import random

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/ace-rl-a100-20261115.json"


def _text(x):
    return isinstance(x, str) and bool(x.strip())


@dataclass(frozen=True)
class Edit:
    operation: str
    tip: str = ""
    bullet_id: int | None = None

    def __post_init__(self):
        if self.operation not in ("ADD", "UPDATE", "REMOVE"):
            raise ValueError("ordered ADD/UPDATE/REMOVE only")
        if self.operation != "REMOVE" and not _text(self.tip):
            raise ValueError("ADD/UPDATE require an explicit tip")
        if self.operation == "ADD" and self.bullet_id is not None:
            raise ValueError("ADD does not target an existing bullet")
        if self.operation != "ADD" and (type(self.bullet_id) is not int or self.bullet_id < 0):
            raise ValueError("UPDATE/REMOVE require zero-based bullet identity")


def apply_edits(playbook, edits, *, tokenize, max_tokens=2048):
    """Ordered edits; skip inapplicable IDs, deduplicate then renumber.

    IDs refer to the original stable bullets while applying the operation list;
    numbering is compacted only after all edits. None means inadmissible.
    tokenize must return real token IDs, not a character-count surrogate.
    """
    original = tuple(playbook)
    if any(not _text(x) for x in original) or len(set(original)) != len(original):
        raise ValueError("unique nonempty initial playbook tips required")
    if not callable(tokenize) or type(max_tokens) is not int or max_tokens < 1:
        raise ValueError("external tokenizer and positive token budget required")
    rows, applied = {i:tip for i,tip in enumerate(original)}, False
    next_id = len(rows)
    for edit in edits:
        if not isinstance(edit, Edit):
            raise ValueError("parsed typed edits required")
        if edit.operation == "ADD":
            rows[next_id] = edit.tip
            next_id += 1
            applied = True
        elif edit.bullet_id in rows:
            if edit.operation == "UPDATE":
                rows[edit.bullet_id] = edit.tip
            else:
                del rows[edit.bullet_id]
            applied = True
    result = tuple(dict.fromkeys(rows.values()))
    token_ids = tuple(tokenize("\n".join(f"[{i}] {tip}" for i,tip in enumerate(result))))
    if any(type(i) is not int or i < 0 for i in token_ids):
        raise ValueError("tokenizer must return explicit nonnegative integer token IDs")
    return result if applied and result != original and len(token_ids) <= max_tokens else None


def reflection_reward(candidate_values):
    """Eq7: mean of admissible downstream values; no candidate yields zero."""
    values = tuple(candidate_values)
    if any(isinstance(x, bool) or not isinstance(x, Real) or not math.isfinite(x) or not 0 <= x <= 1 for x in values):
        raise ValueError("only externally evaluated admissible candidate values in [0,1]")
    return sum(values)/len(values) if values else 0.


@dataclass(frozen=True)
class RoleSample:
    identity: str
    role: str
    task_id: str
    seed_id: str
    reflection_id: str
    reward: float

    def __post_init__(self):
        if not all(_text(x) for x in (self.identity,self.task_id,self.seed_id)) or self.role not in ("actor","reflector","curator"):
            raise ValueError("explicit role and task/seed provenance required")
        if self.role == "curator" and not _text(self.reflection_id):
            raise ValueError("curator must retain its source reflection")
        if isinstance(self.reward, bool) or not isinstance(self.reward, Real) or not math.isfinite(self.reward) or not 0 <= self.reward <= 1:
            raise ValueError("external evaluator reward in [0,1] required")

    def group(self):
        return (self.role,self.task_id) if self.role == "actor" else ((self.role,self.task_id,self.seed_id) if self.role == "reflector" else (self.role,self.task_id,self.seed_id,self.reflection_id))


def role_advantages(samples, *, filter_mode="threshold", epsilon=1e-6):
    """AppendixD.3 filters and role-group normalization, including singletons.

    threshold: discard all<=0 or all>=1; fractional singleton => reward itself.
    range: MiniSWEBench requires a nonzero reward range, including singletons.
    Population standard deviation is explicit here (ddof=0).
    """
    samples = tuple(samples)
    if any(not isinstance(s, RoleSample) for s in samples) or len({s.identity for s in samples}) != len(samples):
        raise ValueError("unique typed role sample identities required")
    if filter_mode not in ("threshold","range") or not isinstance(epsilon, Real) or isinstance(epsilon,bool) or not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("explicit paper group filter and positive epsilon required")
    groups = {}
    for s in samples:
        groups.setdefault(s.group(), []).append(s)
    result = {}
    for rows in groups.values():
        rewards = [s.reward for s in rows]
        keep = (max(rewards) > 0 and min(rewards) < 1) if filter_mode == "threshold" else max(rewards) > min(rewards)
        if not keep:
            continue
        if len(rows) == 1:
            result[rows[0].identity] = rewards[0]
            continue
        mean = sum(rewards)/len(rows)
        std = math.sqrt(sum((r-mean)**2 for r in rewards)/len(rows))
        result.update({s.identity:(s.reward-mean)/(std+epsilon) for s in rows})
    return result


class PlaybookStore:
    """Training-only state; independent evaluation stores are never reset here."""
    def __init__(self, *, seed=42, reset_every=3):
        if type(seed) is not int or type(reset_every) is not int or reset_every < 1:
            raise ValueError("integer seed and positive task encounter reset period required")
        self._rng, self._period = random.Random(seed), reset_every
        self._books, self._encounters = {}, {}

    def begin(self, task_id):
        if not _text(task_id):
            raise ValueError("explicit task identity required")
        count = self._encounters.get(task_id,0)+1
        self._encounters[task_id] = count
        if count % self._period == 0:
            self._books[task_id] = ()
        return self._books.get(task_id,())

    def retain(self, task_id, seed_reward, evaluated_candidates):
        """Eq8: best admissible candidate >= seed; retain independent of credit."""
        if task_id not in self._encounters or not 0 <= seed_reward <= 1:
            raise ValueError("begin task encounter before retaining evaluated candidates")
        candidates = []
        for book,value in evaluated_candidates:
            if book is None:
                continue
            book = tuple(book)
            if any(not _text(t) for t in book) or len(set(book)) != len(book) or not isinstance(value,Real) or isinstance(value,bool) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError("admissible playbooks and external verifier values required")
            if value >= seed_reward:
                candidates.append((book,value))
        if candidates:
            best = max(v for _,v in candidates)
            self._books[task_id] = self._rng.choice([b for b,v in candidates if v == best])
        return self._books.get(task_id,())


def joint_policy_loss(new_log_probs, old_log_probs, advantages, generated_mask, *, clip_low=.2, clip_high=.28, dual_clip=3.):
    """Eq24 negative token-mean surrogate; no role weight, KL or critic."""
    import torch
    xs = (new_log_probs,old_log_probs,advantages,generated_mask)
    if not all(isinstance(x,torch.Tensor) for x in xs) or new_log_probs.ndim != 2 or old_log_probs.shape != new_log_probs.shape or generated_mask.shape != new_log_probs.shape or advantages.shape != (len(new_log_probs),):
        raise ValueError("matching [output,token] logs/mask and per-output advantages required")
    if not all(x.is_floating_point() for x in xs[:3]) or generated_mask.dtype != torch.bool or any(x.device != new_log_probs.device for x in xs):
        raise ValueError("floating same-device inputs and boolean generated-token mask required")
    if any(not torch.isfinite(x).all() for x in xs[:3]) or (new_log_probs > 0).any() or (old_log_probs > 0).any() or not generated_mask.any():
        raise ValueError("finite log probabilities<=0 and nonempty generated tokens required")
    if any(isinstance(x,bool) or not isinstance(x,Real) or not math.isfinite(x) for x in (clip_low,clip_high,dual_clip)) or not 0 < clip_low < 1 or clip_high <= 0 or dual_clip <= 1:
        raise ValueError("valid asymmetric and dual clip constants required")
    ratio = (new_log_probs-old_log_probs.detach()).exp()
    advantage = advantages.detach()[:,None]
    unclipped = ratio*advantage
    clipped = ratio.clamp(1-clip_low,1+clip_high)*advantage
    surrogate = torch.minimum(unclipped,clipped)
    surrogate = torch.where(advantage < 0,torch.maximum(surrogate,dual_clip*advantage),surrogate)
    return -surrogate[generated_mask].mean()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    import torch
    if type(seed) is not int or device not in ("cpu","cuda"):
        raise ValueError("integer seed and cpu/cuda required")
    rows = [RoleSample("a","actor","q","s1","",0.),RoleSample("b","actor","q","s2","",1.),RoleSample("c","curator","q","s1","z",.5)]
    adv = role_advantages(rows)
    store = PlaybookStore(seed=seed)
    store.begin("q")
    store.retain("q",0.,[(('tip',),1.)])
    second, third = store.begin("q"),store.begin("q")
    new = torch.tensor([[-1.,-1.,-1.],[-1.,-1.,-1.]],device=device,requires_grad=True)
    old = torch.full_like(new,-1.,requires_grad=True)
    advantages = torch.tensor([1.,-1.],device=device,requires_grad=True)
    mask = torch.tensor([[True,True,False],[True,False,False]],device=device)
    loss = joint_policy_loss(new,old,advantages,mask)
    loss.backward()
    checks = {"actual_tensor_device":new.device.type == device,
              "task_actor_group_cross_seed":adv['a'] < 0 < adv['b'],
              "fractional_singleton_outcome_update":adv['c'] == .5,
              "range_filter_drops_singleton":'c' not in role_advantages(rows,filter_mode='range'),
              "third_task_encounter_resets":second == ('tip',) and third == (),
              "admissible_only_reflection_mean":reflection_reward([]) == 0. and reflection_reward([.2,.8]) == .5,
              "generated_tokens_only":bool((new.grad[~mask] == 0).all()),
              "evaluator_and_old_policy_detached":advantages.grad is None and old.grad is None,
              "token_not_output_mean":math.isclose(loss.item(),-1/3,abs_tol=1e-6)}
    return {"seed":seed,"execution_device":new.device.type,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","checks":checks,
            "metrics":{"joint_policy_loss":loss.item(),"retained_role_outputs":len(adv),"reflection_value":.5}}
