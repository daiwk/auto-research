"""LSER point-in-time and asynchronous handoff interfaces, not an LLM encoder."""

from __future__ import annotations

import math
import random

REQUIRES_GPU_VALIDATION = False


def _time(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("finite timestamp required")
    return float(value)


def point_in_time(events, *, cutoff, session_start, history_start, current_session,
                  session_limit, history_limit):
    """Explicit session boundary; retain only strict pre-cutoff events.

    Caller supplies eligible, catalog-mapped events for one user. The function
    has no user_id authorization or cross-user isolation. Sessionization and
    mapping are external unreleased policies. Input records remain unchanged.
    """
    cutoff, session_start, history_start = _time(cutoff), _time(session_start), _time(history_start)
    if not history_start <= session_start <= cutoff:
        raise ValueError("history_start <= session_start <= cutoff required")
    if not isinstance(current_session, str) or not current_session:
        raise ValueError("explicit logged current session ID required")
    if any(type(x) is not int or x < 1 for x in (session_limit, history_limit)):
        raise ValueError("positive caps required")
    ordered = sorted(enumerate(events), key=lambda x: (_time(x[1]["timestamp"]), x[0]))
    past = [dict(e) for _, e in ordered if _time(e["timestamp"]) < cutoff]
    return {"session": [e for e in past if e["timestamp"] >= session_start
                        and e["session_id"] == current_session][-session_limit:],
            "history": [e for e in past if history_start <= e["timestamp"] < session_start][-history_limit:]}


def cached_payload(records, *, request_time, include_llm=True):
    """Read available records only; report missing required vectors explicitly.

    Choosing the greatest as_of is a local out-of-order completion safeguard,
    not a paper-prescribed TTL. No vectors are fabricated and no encoder runs.
    Omitting optional LLM requires a caller's compatible baseline fusion head.
    """
    request_time = _time(request_time)
    if type(include_llm) is not bool:
        raise ValueError("boolean LLM toggle required")
    selected = {}
    families = {"session", "history", "llm_session", "llm_history"}
    for row in records:
        family = row["family"]
        if family not in families:
            raise ValueError("unknown vector family")
        as_of, written = _time(row["as_of"]), _time(row["written_at"])
        if as_of > written:
            raise ValueError("vector cannot be written before its input cutoff")
        values = tuple(row["values"])
        if not values or any(isinstance(v, bool) or not isinstance(v, (int, float))
                             or not math.isfinite(v) for v in values):
            raise ValueError("nonempty finite vector required")
        if written > request_time or as_of > request_time or (not include_llm and family.startswith("llm")):
            continue
        if family not in selected or (as_of, written) > (selected[family]["as_of"], selected[family]["written_at"]):
            selected[family] = {"as_of": as_of, "written_at": written, "values": values}
    missing = sorted({"session", "history"} - selected.keys())
    llm_complete = {"llm_session", "llm_history"} <= selected.keys()
    if not llm_complete:
        selected = {k: v for k, v in selected.items() if not k.startswith("llm")}
    return {"vectors": selected, "missing_required": missing,
            "requires_external_cold_start": bool(missing),
            "requires_baseline_fusion": not llm_complete,
            "encoder_calls": 0}


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU interface required")
    n = random.Random(seed).randrange(1, 10)
    events = [{"item_id": str(i), "timestamp": t, "session_id": "current"}
              for i, t in enumerate([0, 2, 5, 10, 11])]
    window = point_in_time(events, cutoff=10, session_start=5, history_start=0,
                           current_session="current", session_limit=n, history_limit=10)
    rows = [{"family": f, "as_of": 5, "written_at": 6, "values": [float(n)]}
            for f in ("session", "history")]
    future = {"family": "session", "as_of": 9, "written_at": 12, "values": [99.]}
    payload = cached_payload([*rows, future], request_time=10)
    checks = {"target_and_future_excluded": all(e["timestamp"] < 10 for es in window.values() for e in es),
              "windows_disjoint": window["session"] == [events[2]] and window["history"] == events[:2],
              "unavailable_refresh_not_read": payload["vectors"]["session"]["values"] == (float(n),),
              "optional_llm_falls_back": payload["requires_baseline_fusion"],
              "no_fabricated_cold_start": cached_payload([], request_time=10)["requires_external_cold_start"],
              "no_sync_encoder": payload["encoder_calls"] == 0}
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "checks": checks, "metrics": {"precutoff_events": sum(map(len, window.values())),
                                           "payload_vector_families": len(payload["vectors"]),
                                           "encoder_calls": 0}}
