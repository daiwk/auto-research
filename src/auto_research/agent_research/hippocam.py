"""Intent-structured context consolidation and one-layer recall (2610.12124).

LLM callbacks perform Janus/Precip/Palim. No heuristic summarizer is substituted.
Complete interaction rounds are atomic, including assistant tool calls/results.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class Message:
    identifier: str
    role: str
    content: str
    round_id: str | None = None
    complete: bool = True
    direct_intent: bool = False


@dataclass(frozen=True)
class Intent:
    purpose: str
    exit_condition: str
    boundary: str


class CapacityExhausted(RuntimeError):
    pass


class Hippocam:
    def __init__(self, tokenize, summarize, *, capacity=32768, rounds=4,
                 minimum_tail=1024, tail_fraction=.25, quantile=.75,
                 pressure=.8, min_saving=8192, refinements=2,
                 min_intents=3, min_prefix_tokens=16384):
        if capacity <= 0 or rounds < 1 or minimum_tail < 0 or min_saving < 1:
            raise ValueError("invalid context budget")
        if not 0 < tail_fraction <= 1 or not 0 < pressure <= 1 or not 0 <= quantile <= 1:
            raise ValueError("invalid context fractions")
        self.tokenize, self.summarize = tokenize, summarize
        self.capacity, self.rounds, self.minimum_tail = capacity, rounds, minimum_tail
        self.tail_fraction, self.quantile, self.pressure = tail_fraction, quantile, pressure
        self.min_saving, self.refinements = min_saving, refinements
        self.min_intents, self.min_prefix_tokens = min_intents, min_prefix_tokens
        self.context, self.intents, self.archive, self.pending = [], [], {}, []
        self.round_sizes, self.serial = [], 0

    def _id(self):
        self.serial += 1
        return f"memory-{self.serial}"

    def tokens(self, messages):
        return sum(len(self.tokenize(m.content)) for m in messages)

    def append(self, role, content, *, round_id=None, complete=True):
        message = Message(self._id(), role, content, round_id, complete)
        self.context.append(message)
        return message.identifier

    def complete_round(self, round_id):
        from dataclasses import replace
        matching = [m for m in self.context if m.round_id == round_id]
        if not matching:
            raise ValueError("unknown round")
        self.context = [replace(m, complete=True) if m.round_id == round_id else m
                        for m in self.context]
        self.round_sizes.append(self.tokens(matching))

    def janus(self, *, close=0, open_intents=(), guidance):
        """Record closures before inference; commit after response, before tools."""
        if self.pending or not 0 <= close <= len(self.intents) or not guidance.strip():
            raise ValueError("invalid or uncommitted Janus stack operation")
        boundary = self.append("assistant", guidance)
        if close:
            self.pending = [(intent, boundary) for intent in reversed(self.intents[-close:])]
            del self.intents[-close:]
        for purpose, exit_condition in open_intents:
            if not purpose.strip() or not exit_condition.strip():
                raise ValueError("intent requires purpose and exit condition")
            self.intents.append(Intent(purpose, exit_condition, boundary))

    def _replace(self, start, end, text, *, direct=False):
        children = tuple(self.context[start:end])
        identifier = self._id()
        self.archive[identifier] = children
        replacement = Message(identifier, "assistant", text, direct_intent=direct)
        self.context[start:end] = [replacement]
        affected = {m.identifier for m in children}
        self.intents = [Intent(i.purpose, i.exit_condition,
                               identifier if i.boundary in affected else i.boundary)
                        for i in self.intents]
        self.pending = [(Intent(i.purpose, i.exit_condition,
                                identifier if i.boundary in affected else i.boundary),
                         identifier if boundary in affected else boundary)
                        for i, boundary in self.pending]
        return identifier

    def after_response(self):
        """Closed spans end at completion guidance, excluding new response/tools."""
        while self.pending:
            intent, boundary = self.pending.pop(0)
            ids = [m.identifier for m in self.context]
            start, end = ids.index(intent.boundary), ids.index(boundary) + 1
            end = self._eligible_end(start, end)
            if end <= start:
                # Never archive half a tool exchange to satisfy a close event.
                continue
            source = tuple(self.context[start:end])
            text = self.summarize("precip", source, tuple(self.intents), intent.purpose, 0)
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Precip must return a nonempty grounded summary")
            self._replace(start, end, text, direct=True)
        self.ordinary_check()

    def recall(self, identifier):
        """Return immediate children only; caller chooses any deeper descent."""
        if identifier not in self.archive:
            raise KeyError(identifier)
        return self.archive[identifier]

    def _tail_start(self, emergency=False):
        unfinished = [i for i, m in enumerate(self.context) if m.round_id and not m.complete]
        if emergency:
            return min(unfinished, default=len(self.context))
        q = float(np.quantile(self.round_sizes, self.quantile)) if self.round_sizes else 0.
        budget = min(self.tail_fraction * self.capacity,
                     max(self.minimum_tail, self.rounds * q))
        seen, count, start = set(), 0, len(self.context)
        for i in range(len(self.context) - 1, -1, -1):
            message = self.context[i]
            count += self.tokens((message,))
            if message.round_id:
                seen.add(message.round_id)
            start = i
            if len(seen) >= self.rounds and count >= budget:
                break
        # Extend to the beginning of any intersected tool exchange.
        intersected = {m.round_id for m in self.context[start:] if m.round_id}
        positions = [i for i, m in enumerate(self.context) if m.round_id in intersected]
        return min([start, *positions, *unfinished])

    def _regions(self):
        ids = [m.identifier for m in self.context]
        boundaries = sorted({0, len(ids), *(ids.index(i.boundary) for i in self.intents)})
        return list(zip(boundaries[:-1], boundaries[1:]))

    def _eligible_end(self, start, end):
        """Never split a complete tool exchange or include unfinished rounds."""
        while end > start:
            span = self.context[start:end]
            rounds = {m.round_id for m in span if m.round_id}
            unsafe = [r for r in rounds if any(
                m.round_id == r and (not m.complete or j < start or j >= end)
                for j, m in enumerate(self.context))]
            if not unsafe:
                return end
            end = min(j for j, m in enumerate(self.context) if m.round_id in unsafe)
        return start

    def _fold(self, start, end):
        end = self._eligible_end(start, end)
        if end <= start:
            return False
        source = tuple(self.context[start:end])
        original = self.tokens(source)
        for attempt in range(self.refinements + 1):
            text = self.summarize("palim", source, tuple(self.intents), "", attempt)
            if isinstance(text, str) and text.strip() and original - len(self.tokenize(text)) >= self.min_saving:
                self._replace(start, end, text)
                return True
        return False

    def ordinary_check(self):
        tail = self._tail_start()
        # Reverse order preserves earlier region indices during replacements.
        for start, end in reversed(self._regions()):
            end = min(end, tail)
            source = self.context[start:end]
            if (sum(m.direct_intent for m in source) >= self.min_intents
                    and self.tokens(source) >= self.min_prefix_tokens):
                self._fold(start, end)

    def pressure_control(self, overhead_tokens=0):
        if overhead_tokens < 0:
            raise ValueError("request overhead must be nonnegative")
        next_round = math.ceil(float(np.quantile(self.round_sizes, self.quantile))) if self.round_sizes else 0
        usage = lambda: self.tokens(self.context) + overhead_tokens + next_round
        if usage() <= self.pressure * self.capacity:
            return
        for emergency in (False, True):
            # Recompute regions after every fold, root to innermost.
            region_index = 0
            while region_index < len(self._regions()):
                start, end = self._regions()[region_index]
                end = min(end, self._tail_start(emergency))
                if self.tokens(self.context[start:end]) > self.min_saving:
                    self._fold(start, end)
                region_index += 1
            if usage() <= self.capacity:
                return
        raise CapacityExhausted("context capacity exhausted before next main-agent inference")
