"""SkillDreamer v2 Eqs. 6–17; pseudo skills are retrieval cues, never executable."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
import re

import numpy as np


@dataclass(frozen=True)
class Skill:
    id: str
    name: str
    description: str
    body: str


def parse_object(text: str) -> dict:
    decoder = json.JSONDecoder()
    found = []
    for match in re.finditer(r"\{", text):
        try:
            value, _ = decoder.raw_decode(text[match.start():])
            if isinstance(value, dict):
                found.append(value)
        except json.JSONDecodeError:
            continue
    for value in found:
        if "capabilities" in value or "tool" in value:
            return value
    raise ValueError("model did not produce a valid capability/action JSON object")


def prospective_skills(goal: str, generate) -> tuple[list[str], list[str]]:
    response = generate(
        "Infer 1–5 independent specialized capability requirements and semantic anchors grounded only in "
        "the task. Do not invent requirements. Return JSON only: "
        '{"capabilities":[{"name":"...","requirement":"..."}],"semantic_anchors":["..."]}. '
        "Task: " + goal)
    output = parse_object(response)
    capabilities = output.get("capabilities")
    anchors = output.get("semantic_anchors")
    if not isinstance(capabilities, list) or not 1 <= len(capabilities) <= 5:
        raise ValueError("PSG requires 1–5 model-inferred capabilities; no heuristic fallback")
    if (not isinstance(anchors, list) or not anchors
            or not all(isinstance(x, str) and x.strip() for x in anchors)):
        raise ValueError("PSG requires nonempty semantic anchors")
    pseudo = []
    for capability in capabilities:
        if (not isinstance(capability, dict)
                or not all(isinstance(capability.get(key), str) and capability[key].strip()
                           for key in ("name", "requirement"))):
            raise ValueError("each model-inferred capability requires its nonempty name and requirement")
        procedure = generate(
            "Write one concise hypothetical SKILL.md describing concrete procedural guidance to realize "
            "this capability. Preserve the supplied anchors, do not broaden the task. This text is only "
            "a retrieval proxy, not an executable skill. Capability: " + capability["requirement"]
            + "\nSemantic anchors: " + ", ".join(anchors))
        if not isinstance(procedure, str) or not procedure.strip():
            raise ValueError("model-generated pseudo procedure must be nonempty; no fallback")
        pseudo.append(procedure)
    return pseudo, anchors


def _words(text):
    return re.findall(r"\w+", text.lower())


def bm25(query: str, documents: list[str]) -> np.ndarray:
    counts = [Counter(_words(d)) for d in documents]
    lengths = np.asarray([sum(c.values()) for c in counts])
    average = max(1.0, float(lengths.mean()))
    scores = np.zeros(len(documents))
    for word in _words(query):
        frequency = sum(word in c for c in counts)
        idf = np.log(1 + (len(documents) - frequency + 0.5) / (frequency + 0.5))
        tf = np.asarray([c[word] for c in counts])
        scores += idf * tf * 2.5 / (tf + 1.5 * (0.25 + 0.75 * lengths / average))
    return scores


def _minmax(x):
    return (x - x.min()) / max(float(x.max() - x.min()), 1e-12)


def hybrid_retrieval(goal: str, pseudo: list[str], anchors: list[str], skills: list[Skill], encode,
                     *, alpha: float = 2, preliminary: int = 20, top_k: int = 5) -> list[Skill]:
    if not pseudo or top_k < 1:
        raise ValueError("PSG pseudo skills and a positive retrieval budget required")
    texts = [s.name + "\n" + s.description + "\n" + s.body for s in skills]
    embeddings = encode([goal, *pseudo, *texts])
    q, p, gallery = embeddings[0], embeddings[1:1 + len(pseudo)], embeddings[1 + len(pseudo):]
    raw = gallery @ q
    lexical = bm25(" ".join(anchors), texts)
    rankings = []
    for proxy in p:
        prospective = gallery @ proxy
        candidates = np.argsort(-(alpha * raw + prospective), kind="stable")[:preliminary]
        rerank = (alpha * _minmax(raw[candidates]) + _minmax(prospective[candidates])
                  + _minmax(lexical[candidates]))
        rankings.append(candidates[np.argsort(-rerank, kind="stable")])
    result, seen = [], set()
    # Algorithm 1's rank matrix is traversed row-first, not capability-first.
    for rank in range(max(map(len, rankings))):
        for ranking in rankings:
            if rank < len(ranking) and int(ranking[rank]) not in seen:
                index = int(ranking[rank])
                seen.add(index)
                result.append(skills[index])
                if len(result) == min(top_k, len(skills)):
                    return result
    return result


def capability_context(goal: str, observations: list[str], candidates: list[Skill],
                       loaded: dict[str, str], executed_actions: int, budget: int) -> str:
    metadata = [{"id": s.id, "name": s.name, "description": s.description} for s in candidates]
    checkpoint = (f"RUNTIME CAPABILITY CHECKPOINT: {executed_actions} actions completed; "
                  f"{budget - executed_actions} remaining. Recheck unresolved requirements and skill gaps.\n"
                  if executed_actions % 5 == 0 else "")
    return (checkpoint + "Task: " + goal + "\nObserved execution history: " + json.dumps(observations)
            + "\nCandidate skill metadata: " + json.dumps(metadata)
            + "\nLoaded verified gallery skill procedures: " + json.dumps(loaded)
            + "\nBefore the next action output SUBGOAL, EVIDENCE, CAPABILITY, DECISION and NEXT on five lines. "
            "Reassess capability from unresolved evidence, not from a tool already chosen. For MATCH or "
            "PARTIAL_MATCH choose a candidate skill_id to load before acting. Otherwise use skill_id=null. "
            'Then output JSON: {"skill_id":null,"tool":"calculator","arguments":{"expression":"..."}} '
            'or {"skill_id":null,"tool":"finish","arguments":{"answer":"..."}}. '
            "Do not search/install/create skills; use only the fixed candidates. Pseudo skills are not available here.")


def parse_capability_assessment(response: str) -> dict[str, str]:
    lines = [line.strip() for line in response.strip().splitlines() if line.strip()]
    labels = ("SUBGOAL", "EVIDENCE", "CAPABILITY", "DECISION", "NEXT")
    if len(lines) < 5 or any(not line.startswith(label + ":")
                             for line, label in zip(lines[:5], labels, strict=True)):
        raise ValueError("CSI requires the five actual model-produced capability-assessment lines")
    values = {label: line.split(":", 1)[1].strip() for label, line in zip(labels, lines[:5], strict=True)}
    if any(not value for value in values.values()):
        raise ValueError("empty CSI assessment is not a capability reevaluation")
    decision = values["DECISION"].split()[0].strip(",;")
    if decision not in {"MATCH", "PARTIAL_MATCH", "NO_MATCH", "NO_CAPABILITY_GAP"}:
        raise ValueError("unknown capability decision")
    return values


def execute_agent(goal: str, generate, candidates: list[Skill], *, mode: str = "skilldreamer",
                  action_budget: int = 8) -> dict:
    from ..state_opd.environment import ArithmeticEnvironment, SYSTEM_PROMPT
    env = ArithmeticEnvironment(goal)
    observations, loaded, checks, generation_errors, tool_errors = [env.reset()], {}, [], 0, 0
    candidate_map = {skill.id: skill for skill in candidates}
    calls = 0
    # Every loaded skill is an actual gallery body, not PSG-generated guidance.
    while env.executed_actions < action_budget and calls < action_budget * 3:
        if mode == "skilldreamer":
            prompt = capability_context(goal, observations, candidates, loaded,
                                        env.executed_actions, action_budget)
        else:
            prompt = (SYSTEM_PROMPT + "\nTask: " + goal + "\nObserved history: " + json.dumps(observations)
                      + "\nAvailable skills: " + json.dumps([
                          {"id": s.id, "description": s.description} for s in candidates])
                      + "\nLoaded skill procedures: " + json.dumps(loaded)
                      + '\nYou may request a candidate skill_id in the same JSON, or use skill_id=null.')
        response = generate(prompt)
        calls += 1
        try:
            action = parse_object(response)
            assessment = parse_capability_assessment(response) if mode == "skilldreamer" else None
        except ValueError:
            generation_errors += 1
            observations.append("Invalid JSON/capability assessment; no tool was executed. Follow the complete schema.")
            continue
        if mode == "skilldreamer":
            checks.append({"executed_actions": env.executed_actions,
                           "periodic_checkpoint": env.executed_actions % 5 == 0,
                           "assessment": assessment})
        skill_id = action.get("skill_id")
        if skill_id is not None and skill_id not in candidate_map:
            generation_errors += 1
            observations.append("Unknown skill ID rejected; only retrieved candidates are available.")
            continue
        if skill_id is not None and skill_id not in loaded:
            loaded[skill_id] = candidate_map[skill_id].body
            observations.append("Skill loaded: " + skill_id + "; reread the procedure before selecting the next action.")
            continue  # get a new model action after it has actually read the skill
        try:
            observation, done = env.step(action)
        except (KeyError, TypeError):
            generation_errors += 1
            observation, done = "Invalid tool argument schema; no successful execution.", False
        if observation.startswith(("Calculator error:", "Invalid action schema.", "Invalid tool argument")):
            tool_errors += 1
        observations.append(observation)
        if done:
            break
    return {"submitted_answer": env.finished_answer, "executed_actions": env.executed_actions,
            "loaded_skills": list(loaded), "capability_checks": checks,
            "generation_errors": generation_errors, "tool_errors": tool_errors, "model_calls": calls,
            "observations": observations}
