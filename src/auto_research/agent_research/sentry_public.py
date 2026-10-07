"""Sentry on a public HotpotQA-backed read-only retrieval environment.

This is a new bounded evaluation, not WebShop/AppWorld/SWE-bench reproduction.
Answer labels and supporting-fact annotations never enter the environment,
agent, detector, verifier or memory summarizer.
"""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import string

from .sentry import PublicStep, Sentry, json_object


DATASET_ID = "hotpotqa/hotpot_qa"
DATASET_REVISION = "1908d6afbbead072334abe2965f91bd2709910ab"
DATASET_SHA256 = "c20b638ca82b21d04fe12e14ff417ad05153d4d215a65de54497fca4e972f7c6"
ACTION_SCHEMA = json.dumps({
    "type": "object", "additionalProperties": False,
    "required": ["reasoning", "action", "argument"],
    "properties": {
        "reasoning": {"type": "string"},
        "action": {"type": "string", "enum": ["search", "read", "finish"]},
        "argument": {"type": "string", "minLength": 1},
    },
})


def public_case(row: dict) -> dict:
    context = row["context"]
    return {"id": row["id"], "question": row["question"],
            "documents": dict(zip(context["title"], map("".join, context["sentences"])))}


def load_cases(path: Path, count: int) -> list[dict]:
    import pyarrow.parquet as pq

    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != DATASET_SHA256:
        raise ValueError("HotpotQA file does not match pinned official content hash")
    rows = pq.read_table(path).to_pylist()
    # Split membership fixed before any run, independent of score/model output.
    rows.sort(key=lambda row: hashlib.sha256(row["id"].encode()).hexdigest())
    if count < 1 or count > len(rows):
        raise ValueError("invalid case count")
    return rows[:count]


class RetrievalEnvironment:
    def __init__(self, documents: dict[str, str]):
        self.documents = dict(documents)
        self.read_titles: set[str] = set()

    def execute(self, action: str, argument: str) -> tuple[str, bool, bool]:
        if action == "finish":
            if not self.read_titles:
                return "Read at least one available page before submitting an evidence-based answer.", False, False
            return "Answer submitted; no correctness feedback is exposed.", True, True
        if action == "read":
            if argument not in self.documents:
                return "Unknown title. Use a title from a search result.", False, False
            self.read_titles.add(argument)
            return self.documents[argument][:6000], True, False
        if action == "search":
            tokens = set(re.findall(r"\w+", argument.lower()))
            ranked = sorted(self.documents, key=lambda title: (
                -len(tokens & set(re.findall(r"\w+", title.lower()))), title))
            hits = [title for title in ranked if tokens & set(re.findall(r"\w+", title.lower()))][:4]
            return json.dumps({"titles": hits}), True, False
        return "Unsupported tool; use search, read or finish.", False, False


def run_episode(case: dict, generate, *, sentry: Sentry | None, seed: int,
                max_steps: int = 14) -> dict:
    if set(case) != {"id", "question", "documents"}:
        raise ValueError("runner accepts only an explicit public-case projection")
    if max_steps < 1:
        raise ValueError("max_steps must be positive")
    environment = RetrievalEnvironment(case["documents"])
    if sentry is not None:
        sentry.start_task(case["question"], ACTION_SCHEMA)
    steps, answer, guidance, outputs = [], "", None, []
    for index in range(max_steps):
        prompt = ("Answer the question by searching document TITLES, then reading matching pages. "
                  "Use evidence from observations; do not invent tool results. Return ONLY JSON "
                  "matching this JSON Schema, no Markdown. Choose ONE action: search searches titles; "
                  "read reads an exact returned title; finish submits only a short answer. "
                  'Example call: {"reasoning":"Find relevant evidence","action":"search",'
                  '"argument":"entity from question"}. Schema: ' + ACTION_SCHEMA
                  + "\nQUESTION: " + case["question"]
                  + "\nAVAILABLE PAGE TITLES (the read tool can open any of these): "
                  + json.dumps(list(case["documents"]))
                  + "\nRead at least one page before finish. Tools are available; a missing trajectory "
                  "does not mean missing evidence. Use a read action to obtain that evidence."
                  + "\nPUBLIC TRAJECTORY: " + json.dumps([asdict(step) for step in steps])
                  + ("\nCONDITIONAL RECOVERY: " + guidance if guidance else ""))
        completion = generate(prompt, 256, seed + index)
        outputs.append(asdict(completion))
        reasoning, action, argument = "", "", ""
        parsed_ok = schema_valid = accepted = terminal = False
        try:
            obj = json_object(completion.text)
            parsed_ok = True
            if set(obj) != {"reasoning", "action", "argument"} or any(not isinstance(v, str) for v in obj.values()):
                raise ValueError("expected exactly three string fields")
            reasoning, action, argument = obj["reasoning"], obj["action"], obj["argument"]
            schema_valid = action in {"search", "read", "finish"} and bool(argument.strip())
            if not schema_valid:
                raise ValueError("invalid action or empty argument")
            observation, accepted, terminal = environment.execute(action, argument)
        except (ValueError, TypeError, KeyError) as exc:
            observation = "Action rejected: " + str(exc)
        step = PublicStep(reasoning, json.dumps({"action": action, "argument": argument})
                          if parsed_ok else completion.text, observation,
                          parsed_ok=parsed_ok, schema_valid=schema_valid, accepted=accepted)
        steps.append(step)
        guidance = sentry.observe(step, terminal=terminal) if sentry is not None else None
        if terminal:
            answer = argument
            break
    if sentry is not None:
        sentry.finalize()
    return {"id": case["id"], "prediction": answer, "steps": [asdict(step) for step in steps],
            "agent_generations": outputs, "completed": bool(answer),
            "tool_steps": len(steps), "invalid_actions": sum(not step.accepted for step in steps)}


def exact_match(prediction: str, reference: str) -> int:
    def normalize(text):
        text = text.lower().translate(str.maketrans("", "", string.punctuation))
        return " ".join(re.sub(r"\b(a|an|the)\b", " ", text).split())
    return int(normalize(prediction) == normalize(reference))
