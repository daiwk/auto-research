"""ELITE common-parent exploration/integration protocol (arXiv2611.21056).

The reasoning integrator and validity checks are supplied executable callbacks,
not replaced with a compatibility heuristic. This is L0, not a coding agent.
No benchmark outcome or task-solving trajectory is accepted by the interface.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType

REQUIRES_GPU_VALIDATION = False


def snapshot(files: Mapping[str, str]) -> Mapping[str, str]:
    if not files or any(
        not isinstance(k, str) or not k or not isinstance(v, str) for k, v in files.items()
    ):
        raise ValueError("nonempty text-source mapping required")
    return MappingProxyType(dict(files))


@dataclass(frozen=True)
class Exploration:
    hypothesis: str
    files: Mapping[str, str]
    changed_paths: tuple[str, ...]


@dataclass(frozen=True)
class IntegrationRequest:
    parent: Mapping[str, str]
    children: tuple[Exploration, ...]


def generation(
    parent: Mapping[str, str],
    hypotheses: Sequence[str],
    *,
    explore: Callable[[Mapping[str, str], str], Mapping[str, str]],
    exploration_gate: Callable[[Mapping[str, str]], bool],
    integrate: Callable[[IntegrationRequest], Mapping[str, str]],
    acceptance_gate: Callable[[Mapping[str, str]], bool],
    allowed_paths: frozenset[str],
    max_children: int = 7,
) -> dict:
    if type(max_children) is not int or not 1 <= max_children <= 7:
        raise ValueError("bounded exploration population required")
    if (
        not hypotheses
        or len(hypotheses) > max_children
        or any(not isinstance(h, str) or not h.strip() for h in hypotheses)
    ):
        raise ValueError("nonempty bounded focused hypotheses required")
    base = snapshot(parent)
    if not isinstance(allowed_paths, frozenset) or not allowed_paths:
        raise ValueError("explicit immutable edit scope required")
    valid, events = [], []
    for h in hypotheses:
        try:
            child = snapshot(explore(base, h))
            changed = tuple(
                sorted(k for k in set(base) | set(child) if base.get(k) != child.get(k))
            )
            if not changed or not set(changed) <= allowed_paths:
                raise ValueError("empty patch or out-of-scope exploration")
            gate = exploration_gate(child)
            if type(gate) is not bool:
                raise TypeError("validity gate must return strict bool")
            if gate:
                valid.append(Exploration(h, child, changed))
            events.append({"stage": "exploration", "valid": gate})
        except Exception as error:
            events.append(
                {"stage": "exploration", "valid": False, "error_type": type(error).__name__}
            )
    if not valid:
        return {"files": base, "accepted": False, "events": events, "valid_children": 0}
    try:
        # The integrator sees the original parent and independent valid children,
        # never a sequentially patched child or downstream task score.
        candidate = snapshot(integrate(IntegrationRequest(base, tuple(valid))))
        changed = {k for k in set(base) | set(candidate) if base.get(k) != candidate.get(k)}
        if not changed or not changed <= allowed_paths:
            raise ValueError("empty or out-of-scope integration")
        accepted = acceptance_gate(candidate)
        if type(accepted) is not bool:
            raise TypeError("acceptance validity gate must return strict bool")
        events.append({"stage": "acceptance", "valid": accepted})
    except Exception as error:
        accepted = False
        events.append({"stage": "integration", "valid": False, "error_type": type(error).__name__})
    return {
        "files": candidate if accepted else base,
        "accepted": accepted,
        "valid_children": len(valid),
        "events": events,
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    base = {"agent.py": "value = 0\n"}
    seen = []

    def explorer(parent, h):
        seen.append(dict(parent))
        return {"agent.py": parent["agent.py"] + f"{h} = 1\n"}

    def integration(request):
        assert set(vars(request)) == {"parent", "children"}
        return {"agent.py": request.parent["agent.py"] + "combined = 2\n"}

    def valid(files):
        try:
            compile(files["agent.py"], "agent.py", "exec")
            return True
        except SyntaxError:
            return False

    result = generation(
        base,
        ("first", "second"),
        explore=explorer,
        exploration_gate=valid,
        integrate=integration,
        acceptance_gate=lambda _: False,
        allowed_paths=frozenset({"agent.py"}),
    )
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l0_interface",
        "checks": {
            "independent_common_parent": seen == [base, base],
            "failed_acceptance_keeps_parent": not result["accepted"]
            and dict(result["files"]) == base,
            "valid_children_really_explored": result["valid_children"] == 2,
            "no_evaluation_input": set(IntegrationRequest.__dataclass_fields__)
            == {"parent", "children"},
        },
        "metrics": {"explorer_calls": len(seen), "valid_children": result["valid_children"]},
    }
