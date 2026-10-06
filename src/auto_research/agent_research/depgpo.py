"""DepGPO credit assignment on *recorded* terminal-agent traces.

This is a CPU mechanism implementation of Eqs. (10)--(21) in arXiv:2610.03634.
It consumes structured tracer output; it does not infer reads from shell text,
run a verifier, or train a language-model policy.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from math import isfinite


WHOLE_FILE = -1
FileRecord = tuple[str, int]


@dataclass(frozen=True)
class CommandTrace:
    command_id: str
    step: int
    read_files: tuple[str, ...] = ()
    written_records: tuple[FileRecord, ...] = ()
    resource_writes: tuple[str, ...] = ()
    # Earlier stdout producers confirmed by a trusted typed-value matcher.
    stdout_source_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class CreditResult:
    command_credit: dict[str, float]
    step_credit: tuple[float, ...]
    step_factor: tuple[float, ...]
    token_weight: tuple[float, ...]
    redistributed_advantage: tuple[float, ...]
    fallback: bool


def assign_dependency_credit(
    commands: list[CommandTrace],
    *,
    verifier_files: set[str],
    verifier_resources: set[str] | None = None,
    token_counts: tuple[int, ...],
    group_advantage: float,
    beta: float = 0.5,
) -> CreditResult:
    """Reweight an observed GRPO advantage using dependency evidence.

    ``written_records`` are per-command diff positions, or ``WHOLE_FILE``
    where line resolution is unavailable. ``stdout_source_ids`` must already
    exclude prompt-provided values. No gold answer, plan, or test label enters.
    """
    if not token_counts or any(not isinstance(n, int) or n < 0 for n in token_counts):
        raise ValueError("token_counts must contain nonnegative integer lengths")
    if not 0 < beta <= 1 or not isfinite(group_advantage):
        raise ValueError("beta and group_advantage must be finite and valid")
    if not verifier_files and not verifier_resources:
        return _unit_result(commands, token_counts, group_advantage)

    ids: set[str] = set()
    owner: dict[FileRecord, str] = {}
    graph: dict[str, set[str]] = defaultdict(set)
    # Each qualifying input record retains the consuming write command.
    qualifying: dict[tuple[str, FileRecord], set[str]] = defaultdict(set)
    traces: dict[str, CommandTrace] = {}
    for command in commands:
        if not command.command_id or command.command_id in ids:
            raise ValueError("command IDs must be unique and nonempty")
        if not 0 <= command.step < len(token_counts):
            raise ValueError("command step is outside token_counts")
        ids.add(command.command_id)
        traces[command.command_id] = command
        writes = set(command.written_records)
        if len(writes) != len(command.written_records) or any(
            not path or not isinstance(position, int) for path, position in writes
        ):
            raise ValueError("invalid or duplicate written record")
        for source in command.stdout_source_ids:
            if source not in ids or source == command.command_id:
                raise ValueError("stdout source must be an earlier command")
            graph[source].add(command.command_id)
        for path in command.read_files:
            if not path:
                raise ValueError("read file path cannot be empty")
            for record, writer in owner.items():
                if record[0] != path:
                    continue
                graph[writer].add(command.command_id)
                if writes and any(out_path != path for out_path, _ in writes) and record not in writes:
                    qualifying[(writer, record)].add(command.command_id)
        for record in writes:
            owner[record] = command.command_id

    endpoints = set(verifier_resources or ())
    directly_relevant = {
        writer for (path, _), writer in owner.items() if path in verifier_files
    }
    directly_relevant.update(
        command.command_id
        for command in commands
        if endpoints.intersection(command.resource_writes)
    )
    reverse_qualifying: dict[str, set[str]] = defaultdict(set)
    for (writer, _), consumers in qualifying.items():
        for consumer in consumers:
            reverse_qualifying[consumer].add(writer)
    relevant = set(directly_relevant)
    queue = deque(directly_relevant)
    while queue:
        for predecessor in reverse_qualifying[queue.popleft()]:
            if predecessor not in relevant:
                relevant.add(predecessor)
                queue.append(predecessor)

    credits: dict[str, float] = {}
    for command in commands:
        records = set(command.written_records)
        if records:
            direct = {
                record for record in records
                if record[0] in verifier_files and owner.get(record) == command.command_id
            }
            indirect = {
                record for record in records
                if qualifying[(command.command_id, record)].intersection(relevant)
            }
            credits[command.command_id] = len(direct | indirect) / len(records)
        elif command.resource_writes:
            credits[command.command_id] = float(command.command_id in relevant)
    # Read commands receive shortest-path credit from *distinct* write descendants.
    for command in commands:
        if command.command_id in credits:
            continue
        distances = {command.command_id: 0}
        queue = deque([command.command_id])
        while queue:
            current = queue.popleft()
            for successor in graph[current]:
                if successor not in distances:
                    distances[successor] = distances[current] + 1
                    queue.append(successor)
        credits[command.command_id] = sum(
            beta ** distance * credits.get(target, 0.0)
            for target, distance in distances.items()
            if distance and (traces[target].written_records or traces[target].resource_writes)
        )

    step_credit = [0.0] * len(token_counts)
    traced_steps: set[int] = set()
    for command in commands:
        traced_steps.add(command.step)
        step_credit[command.step] += credits[command.command_id]
    factors = [1.0] * len(token_counts)
    fallback = True
    if traced_steps:
        minimum = min(step_credit[step] for step in traced_steps)
        excess = sum(step_credit[step] - minimum for step in traced_steps)
        if excess > 1e-9:
            fallback = False
            for step in traced_steps:
                factors[step] = len(traced_steps) * (step_credit[step] - minimum) / excess
    total_tokens = sum(token_counts)
    denominator = sum(count * factor for count, factor in zip(token_counts, factors))
    # Eq. (19) cannot normalize a zero denominator; retain baseline advantage.
    if total_tokens == 0 or denominator <= 1e-9:
        factors = [1.0] * len(token_counts)
        fallback = True
        weights = [1.0] * len(token_counts)
    else:
        mean_factor = denominator / total_tokens
        weights = [factor / mean_factor for factor in factors]
    return CreditResult(
        command_credit=credits,
        step_credit=tuple(step_credit),
        step_factor=tuple(factors),
        token_weight=tuple(weights),
        redistributed_advantage=tuple(group_advantage * weight for weight in weights),
        fallback=fallback,
    )


def _unit_result(
    commands: list[CommandTrace], token_counts: tuple[int, ...], group_advantage: float
) -> CreditResult:
    zeros = tuple(0.0 for _ in token_counts)
    ones = tuple(1.0 for _ in token_counts)
    return CreditResult(
        command_credit={command.command_id: 0.0 for command in commands},
        step_credit=zeros,
        step_factor=ones,
        token_weight=ones,
        redistributed_advantage=tuple(group_advantage for _ in token_counts),
        fallback=True,
    )
