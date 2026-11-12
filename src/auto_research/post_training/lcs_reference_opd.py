"""Same-task LCS reference selection and failure-only OPD (2611.13135).

No teacher, student policy, environment or answer is returned by this selector.
Reference trajectories are training-only teacher inputs, not student context.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from collections.abc import Sequence
import numpy as np

REQUIRES_GPU_VALIDATION = False


def canonical_tool_call(name: str, arguments: dict) -> str:
    """Exact parsed-action identity; argument key order is irrelevant.

    This is not an ALFWorld action parser or fuzzy semantic tool equivalence.
    Values must be JSON-compatible and finite; repeated calls remain repeated.
    """
    if not isinstance(name, str) or not name or not isinstance(arguments, dict) or any(not isinstance(k, str) for k in arguments):
        raise ValueError("nonempty tool name and string-keyed argument mapping required")
    try:
        return json.dumps([name, arguments], sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("finite JSON tool arguments required") from error


def _actions(actions: Sequence[str]) -> tuple[str, ...]:
    if not isinstance(actions, Sequence) or isinstance(actions, str) or any(not isinstance(a, str) or not a for a in actions):
        raise ValueError("sequence of nonempty parsed-action strings required")
    return tuple(actions)


def lcs_length(failed: Sequence[str], reference: Sequence[str]) -> int:
    """Order-preserving exact LCS, O(Tminus*Tplus) time and O(Tplus) memory."""
    failed, reference = _actions(failed), _actions(reference)
    previous = [0] * (len(reference) + 1)
    for action in failed:
        current = [0]
        for j, ref_action in enumerate(reference):
            current.append(previous[j] + 1 if action == ref_action else max(previous[j + 1], current[-1]))
        previous = current
    return previous[-1]


def compatibility(failed: Sequence[str], reference: Sequence[str], *, normalizer: str) -> float:
    """Appendix D: 'shorter' for ALFWorld, 'failed' for tau3-bench.

    The paper assumes a positive denominator. Empty parsed sequences are an
    explicit local boundary: return zero compatibility, never divide by zero.
    """
    failed, reference = _actions(failed), _actions(reference)
    if normalizer not in {"shorter", "failed"}:
        raise ValueError("normalizer must be shorter or failed")
    denominator = len(failed) if normalizer == "failed" else min(len(failed), len(reference))
    return lcs_length(failed, reference) / denominator if denominator else 0.


@dataclass(frozen=True)
class Trajectory:
    task_id: str
    actions: tuple[str, ...]
    success: bool

    def __post_init__(self):
        if not isinstance(self.task_id, str) or not self.task_id or type(self.success) is not bool:
            raise ValueError("task instance ID and evaluated Boolean success required")
        object.__setattr__(self, "actions", _actions(self.actions))


def reference_pool(offline_rollouts: Sequence[Trajectory]) -> dict[str, tuple[Trajectory, ...]]:
    """Keep evaluated successes; deduplicate complete sequences within a task."""
    pool: dict[str, list[Trajectory]] = {}
    seen: dict[str, set[tuple[str, ...]]] = {}
    for rollout in offline_rollouts:
        if not isinstance(rollout, Trajectory):
            raise ValueError("evaluated Trajectory records required")
        if rollout.success and rollout.actions not in seen.setdefault(rollout.task_id, set()):
            seen[rollout.task_id].add(rollout.actions)
            pool.setdefault(rollout.task_id, []).append(rollout)
    return {key: tuple(value) for key, value in pool.items()}


def select_reference(rollout: Trajectory, pool: dict[str, tuple[Trajectory, ...]], *, normalizer: str) -> dict:
    """Independent free-target argmax; ties retain first offline sequence.

    There is no balanced target marginal or capacity limit. Many failures may
    choose the same successful reference. Successful students skip OPD entirely.
    """
    if normalizer not in {"shorter", "failed"}:
        raise ValueError("normalizer must be shorter or failed")
    if rollout.success:
        return {"update": False, "teacher_reference": None, "compatibility": 0., "mode": "skip_success"}
    candidates = pool.get(rollout.task_id, ())
    if any(not r.success or r.task_id != rollout.task_id for r in candidates):
        raise ValueError("pool may contain only evaluated same-task successes")
    if not candidates:
        return {"update": True, "teacher_reference": None, "compatibility": 0., "mode": "reference_free"}
    scores = [compatibility(rollout.actions, r.actions, normalizer=normalizer) for r in candidates]
    index = max(range(len(scores)), key=scores.__getitem__)
    return {"update": True, "teacher_reference": candidates[index], "compatibility": scores[index], "mode": "reference_conditioned"}


def failure_only_mean(losses: Sequence[float], success: Sequence[bool]) -> float | None:
    """Algorithm 1 normalizes by failures, not the entire collected batch.

    None means no optimizer step. Ignored successes may carry absent/NaN losses.
    """
    if len(losses) != len(success) or any(type(s) is not bool for s in success):
        raise ValueError("aligned losses and evaluated Boolean success flags required")
    active = [float(loss) for loss, passed in zip(losses, success) if not passed]
    if not all(math.isfinite(v) for v in active):
        raise ValueError("finite losses for failed trajectories required")
    return sum(active) / len(active) if active else None


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("LCS reference selector is CPU-only")
    rng = np.random.default_rng(seed)
    failure = Trajectory("same-instance", ("open", "take-a", "redundant-look", "put-a", "take-b"), False)
    compatible = Trajectory("same-instance", ("open", "take-a", "put-a", "take-b", "finish"), True)
    incompatible = Trajectory("same-instance", ("open", "take-a", "put-c", "finish"), True)
    other = Trajectory("different-instance", failure.actions, True)
    pool = reference_pool([incompatible, compatible, compatible, other])
    decision = select_reference(failure, pool, normalizer="failed")
    absent = select_reference(Trajectory("no-reference", ("look",), False), pool, normalizer="failed")
    skipped = select_reference(compatible, pool, normalizer="shorter")
    losses = rng.uniform(.1, 2., 2).tolist()
    average = failure_only_mean([losses[0], float("nan"), losses[1]], [False, True, False])
    checks = {
        "lcs_retains_agreement_after_detour": lcs_length(failure.actions, compatible.actions) == 4,
        "same_task_highest_compatibility_selected": decision["teacher_reference"] == compatible,
        "complete_sequence_duplicates_removed": len(pool["same-instance"]) == 2,
        "cross_task_exact_match_not_selected": decision["teacher_reference"] != other,
        "successful_student_skips_update": skipped["update"] is False,
        "no_same_task_success_falls_back_reference_free": absent["mode"] == "reference_free",
        "only_failed_losses_enter_mean": bool(np.isclose(average, sum(losses) / 2)),
        "all_success_batch_has_no_optimizer_step": failure_only_mean([float("nan")], [True]) is None,
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"selected_lcs_coverage": decision["compatibility"], "same_task_references": len(pool["same-instance"]), "failure_only_mean_loss": average, "lcs_length": lcs_length(failure.actions, compatible.actions)}, "checks": checks}
