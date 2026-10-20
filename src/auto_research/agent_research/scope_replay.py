"""SCOPE's instance-bound stateful API replay for a restricted object language.

Trusted callbacks only, not a sandbox. Mutable dict/list aliases and mutations
are preserved; arrays/views, custom objects and unrecorded external I/O are not
supported and must not receive a certificate. No gold enters the program API.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import random
from typing import Callable


class Unavailable(ValueError):
    pass


class Diverged(ValueError):
    pass


EXCEPTIONS = {name: cls for name, cls in (("ValueError", ValueError), ("KeyError", KeyError),
    ("RuntimeError", RuntimeError), ("IndexError", IndexError), ("TypeError", TypeError))}


class Graph:
    """Identity-aware snapshots, with stable node IDs from pre-state to post-state."""

    def __init__(self):
        self.ids, self.objects = {}, {}

    def snapshot(self, roots):
        nodes, visiting = {}, set()
        def encode(value):
            if type(value) in (type(None), bool, int, str):
                return [type(value).__name__, value]
            if type(value) is float and math.isfinite(value):
                # Preserve signed zero, observable through math.copysign.
                return ["float", value.hex()]
            if type(value) not in (dict, list, tuple):
                raise Unavailable("unsupported object; only finite scalar/dict/list/tuple graphs")
            oid = id(value)
            if oid not in self.ids:
                index = len(self.ids)
                self.ids[oid], self.objects[index] = index, value
            index = self.ids[oid]
            if index not in visiting:
                visiting.add(index)
                if type(value) is dict:
                    if any(type(key) is not str for key in value):
                        raise Unavailable("only string-keyed dictionaries supported")
                    # Python APIs can observe dictionary insertion order; a
                    # sorted snapshot would falsely equate distinct requests.
                    nodes[index] = ["dict", [[key, encode(item)] for key, item in value.items()]]
                else:
                    nodes[index] = [type(value).__name__, [encode(item) for item in value]]
            return ["ref", index]
        encoded = [encode(root) for root in roots]
        return {"roots": encoded, "nodes": nodes}

    def restore(self, snapshot):
        nodes = snapshot["nodes"]
        for index, (kind, _data) in nodes.items():
            expected = {"dict": dict, "list": list, "tuple": tuple}.get(kind)
            if expected is None:
                raise Unavailable("unsupported snapshot container")
            if index not in self.objects and kind != "tuple":
                obj = {} if kind == "dict" else []
                self.objects[index] = obj
                self.ids[id(obj)] = index
            elif index in self.objects and type(self.objects[index]) is not expected:
                raise Unavailable("container type changed across API boundary")
        building = set()
        def materialize(index):
            if index in self.objects:
                return self.objects[index]
            if index in building:
                raise Unavailable("invalid direct tuple cycle")
            building.add(index)
            kind, data = nodes[index]
            if kind != "tuple":
                raise Unavailable("missing mutable snapshot node")
            obj = tuple(decode(value) for value in data)
            building.remove(index)
            self.objects[index], self.ids[id(obj)] = obj, index
            return obj
        def decode(value):
            kind, data = value
            if kind == "ref":
                return materialize(data)
            if kind == "float":
                return float.fromhex(data)
            return data
        for index in nodes:
            materialize(index)
        # Decode references to existing containers first, then fill in place.
        # Clearing a referenced child does not replace it, so aliases survive.
        for index, (kind, data) in nodes.items():
            obj = self.objects[index]
            if kind == "tuple":
                continue
            obj.clear()
            if kind == "dict":
                obj.update((key, decode(value)) for key, value in data)
            else:
                obj.extend(decode(value) for value in data)
        return tuple(decode(root) for root in snapshot["roots"])


@dataclass(frozen=True)
class Event:
    name: str
    before: dict
    after: dict
    exception: tuple[str, tuple] | None


@dataclass(frozen=True)
class Witness:
    source_sha256: str
    instance: str
    initial: dict
    events: tuple[Event, ...]
    final: dict


def _source(source: str) -> str:
    if not isinstance(source, str) or not source:
        raise ValueError("nonempty source identifier required")
    return hashlib.sha256(source.encode()).hexdigest()


def record(program: Callable, *, source: str, instance: str, state: dict,
           api: Callable, native_grader: Callable[[dict], bool]) -> Witness:
    """Record a successful development execution; private grader never reaches program.

    Any callback exception, unrecorded effect or failed grader is not a witness.
    The caller must guarantee that all behavior-relevant I/O crosses `call`.
    """
    if type(state) is not dict or not isinstance(instance, str) or not instance:
        raise ValueError("public state dict and recorded instance required")
    initial = Graph().snapshot((state,))
    events = []
    def call(name, *args):
        if not isinstance(name, str) or not name:
            raise ValueError("named API required")
        graph = Graph()
        before = graph.snapshot((state, args))
        try:
            value = api(name, state, *args)
        except Exception as error:
            if type(error).__name__ not in EXCEPTIONS or type(error) is not EXCEPTIONS[type(error).__name__]:
                raise Unavailable("unsupported exception type") from error
            Graph().snapshot((error.args,))
            after = graph.snapshot((state, args, error.args))
            events.append(Event(name, before, after, (type(error).__name__, error.args)))
            raise
        after = graph.snapshot((state, args, value))
        events.append(Event(name, before, after, None))
        return value
    program(call, state)
    final = Graph().snapshot((state,))
    if native_grader(state) is not True:
        raise ValueError("only native-graded successful normal execution is a witness")
    return Witness(_source(source), instance, initial, tuple(events), final)


@dataclass(frozen=True)
class Certification:
    status: str
    matched_events: int
    source_sha256: str
    recorded_instance: str
    reason: str


def certify(program: Callable, witness: Witness, *, candidate_source: str,
            instance: str) -> Certification:
    """Full trace only; divergence/unavailable is not an environment failure."""
    source = _source(candidate_source)
    if instance != witness.instance:
        raise ValueError("certificate cannot transfer to a different recorded instance")
    graph = Graph()
    state, = graph.restore(witness.initial)
    index, failure = 0, None
    def call(name, *args):
        nonlocal index, failure
        try:
            if index >= len(witness.events):
                raise Diverged("extra API call")
            event = witness.events[index]
            local = Graph()
            current = local.snapshot((state, args))
            if name != event.name or current != event.before:
                raise Diverged("API request or public pre-state differs")
            _state, _args, result = local.restore(event.after)
            index += 1
            if event.exception:
                raise EXCEPTIONS[event.exception[0]](*result)
            return result
        except (Diverged, Unavailable) as error:
            failure = error
            raise
    try:
        program(call, state)
        if failure is not None:
            raise failure
        if index != len(witness.events):
            raise Diverged("normal termination before full tape consumption")
        if Graph().snapshot((state,)) != witness.final:
            raise Diverged("terminal public state differs after the final API call")
        return Certification("certified", index, source, instance, "recorded instance only")
    except Unavailable as error:
        return Certification("unavailable", index, source, instance, str(error))
    except Exception as error:
        return Certification("diverged", index, source, instance, str(error))


def witness_subset(witnesses: tuple[Witness, ...], *, seed: int, limit: int = 3):
    if type(limit) is not int or not 0 <= limit <= 3:
        raise ValueError("at most three witnesses")
    return tuple(random.Random(seed).sample(witnesses, min(limit, len(witnesses))))


class AcceptedPrograms:
    """Environment successes, not replay certificates, update accepted source."""

    def __init__(self, source: str):
        _source(source)
        self.accepted_source, self.witnesses = source, []

    def observe(self, source: str, *, success: bool, witness: Witness | None = None):
        _source(source)
        if type(success) is not bool:
            raise ValueError("observed boolean environment outcome required")
        if not success:
            return False
        if witness is not None and witness.source_sha256 != _source(source):
            raise ValueError("successful outcome must bind a matching witness")
        changed = source != self.accepted_source
        self.accepted_source = source
        if witness is not None:
            self.witnesses.append(witness)
        return changed


def tape_hash(witness: Witness) -> str:
    from dataclasses import asdict
    return hashlib.sha256(json.dumps(asdict(witness), sort_keys=True, allow_nan=False).encode()).hexdigest()
