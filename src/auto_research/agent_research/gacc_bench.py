"""Question-withheld goal-adaptive compression protocol, no LLM implementation.

Official comparisons require a real cl100k_base codec. Tests may supply an
explicitly named fixed-token fixture codec; such results are diagnostic only.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Callable


@dataclass(frozen=True)
class TokenCodec:
    name: str
    revision: str
    encode: Callable
    decode: Callable


@dataclass(frozen=True)
class Question:
    question_id: str
    text: str
    reference_answer: str


@dataclass(frozen=True)
class GoalCase:
    context_id: str
    goal_id: str
    context: str
    goal: str
    questions: tuple[Question, ...]


@dataclass(frozen=True)
class CompressorInput:
    context: str
    goal: str
    token_budget: int


@dataclass(frozen=True)
class ReaderInput:
    memory: str
    question: str


@dataclass(frozen=True)
class JudgeInput:
    source_context: str
    question: str
    reference_answer: str
    candidate_answer: str


def _tokens(codec, text):
    values = tuple(codec.encode(text))
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in values):
        raise ValueError("codec must expose nonnegative integer token IDs")
    return values


def evaluate(cases, *, compressor, reader, judge, codec: TokenCodec, retention_ratio,
             compressor_revision, reader_revision, judge_revision, cache=None):
    """One memory per context/goal/budget/revision; fixed reader/judge per run.

    Reference answers are provided exclusively to JudgeInput. Callbacks are
    trusted in-process functions, not security-isolated agents.
    """
    cases = tuple(cases)
    if (not 1 <= len(cases) <= 1000 or not math.isfinite(retention_ratio)
            or not 0 <= retention_ratio <= 1
            or not all((codec.name, codec.revision, compressor_revision,
                        reader_revision, judge_revision))):
        raise ValueError("bounded cases, retention ratio and explicit revisions required")
    identities, contexts = set(), {}
    for case in cases:
        identity = (case.context_id, case.goal_id)
        if (not all(identity) or identity in identities or not case.goal
                or not case.questions or len(case.questions) > 1000):
            raise ValueError("unique identified goals with nonempty question groups required")
        identities.add(identity)
        if case.context_id in contexts and contexts[case.context_id] != case.context:
            raise ValueError("one source context per context ID required")
        contexts[case.context_id] = case.context
        if (len({q.question_id for q in case.questions}) != len(case.questions)
                or any(not q.question_id or not q.text for q in case.questions)):
            raise ValueError("unique nonempty question identities required per goal")
    memories = {} if cache is None else cache
    rows, goal_success, compressions = [], [], 0
    for case in cases:
        source = _tokens(codec, case.context)
        if not source:
            raise ValueError("source context cannot be empty")
        budget = math.floor(retention_ratio * len(source))
        content_hash = hashlib.sha256((case.context + "\0" + case.goal).encode()).hexdigest()
        key = (case.context_id, case.goal_id, content_hash, budget, codec.name,
               codec.revision, compressor_revision)
        if key not in memories:
            text = compressor(CompressorInput(case.context, case.goal, budget))
            if not isinstance(text, str):
                raise ValueError("compressor must return text")
            tokens = _tokens(codec, text)
            retained = tokens[:budget]
            # No length-based regeneration or rewriting is permitted.
            memory = codec.decode(list(retained))
            if not isinstance(memory, str) or len(_tokens(codec, memory)) > budget:
                raise ValueError("codec round trip violated the retained token budget")
            memories[key] = (memory, len(tokens), len(retained))
            compressions += 1
        memory, proposed, retained_count = memories[key]
        if len(_tokens(codec, memory)) > budget:
            raise ValueError("cached memory exceeds current token budget")
        successes = []
        for question in case.questions:
            answer = reader(ReaderInput(memory, question.text))
            if not isinstance(answer, str):
                raise ValueError("reader must return a text answer")
            correct = judge(JudgeInput(case.context, question.text,
                                      question.reference_answer, answer))
            if not isinstance(correct, bool):
                raise ValueError("fixed judge must return a binary correctness decision")
            successes.append(correct)
            rows.append({"context_id": case.context_id, "goal_id": case.goal_id,
                         "question_id": question.question_id, "correct": correct,
                         "source_tokens": len(source), "token_budget": budget,
                         "proposed_tokens": proposed, "retained_tokens": retained_count,
                         "unused_token_budget": budget - retained_count, "padding_tokens": 0,
                         "memory_tokens_reencoded": len(_tokens(codec, memory))})
        goal_success.append(all(successes))
    return {"questions": len(rows), "goals": len(cases), "compressions": compressions,
            "micro_accuracy": sum(row["correct"] for row in rows) / len(rows),
            "macro_all_question_success": sum(goal_success) / len(goal_success),
            "rows": rows, "tokenizer": {"name": codec.name, "revision": codec.revision,
                 "identity_verified": False, "required_paper_tokenizer": "cl100k_base",
                 "identity_policy": "caller declaration only; a matching name does not verify the codec"},
            "reader_revision": reader_revision, "judge_revision": judge_revision,
            "diagnostic_only": True, "promotion_eligible": False}
