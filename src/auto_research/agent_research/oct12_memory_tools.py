"""Query-conditioned memory, neural tool retrieval and paired workflow audits."""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
import time
import numpy as np


class T2Mem:
    """Metadata first, then interleaved SearchMeta/ReadRaw/memory construction."""
    def __init__(self, backend, sessions, *, top_k=2, max_steps=4):
        if not sessions or top_k < 1 or max_steps < 1:
            raise ValueError("nonempty history and positive retrieval/step budgets required")
        self.backend, self.sessions = backend, dict(sessions)
        self.top_k, self.max_steps = top_k, max_steps
        self.metadata = {key: backend.generate([{"role": "user", "content": json.dumps({
            "session": text, "source_id": key,
            "instruction": "Extract lightweight events/entities/facts/temporal cues with source ID. "
            "Do not answer any future query or build a consolidated memory."})}], sample=False)
            for key, text in self.sessions.items()}

    def search(self, query, seen):
        query_embedding = self.backend.embedding(query)
        unseen = [key for key in self.metadata if key not in seen]
        ranked = sorted(unseen, key=lambda key: float(
            self.backend.embedding(self.metadata[key]) @ query_embedding), reverse=True)
        keys = ranked[:self.top_k]
        return keys, {key: self.metadata[key] for key in keys}

    def answer(self, query):
        seen, memory, trace = set(), [], []
        keys, observation = self.search(query, seen)
        seen.update(keys)
        for step in range(self.max_steps):
            messages = [{"role": "user", "content": json.dumps({"query": query,
                "memory": memory, "new_observation": observation,
                "instruction": "Distill only query-relevant evidence from observation; preserve uncertainty, "
                    "time order and source IDs. Do not invent unseen session content."})}]
            cache = self.backend.generate(messages, sample=False)
            memory.append(cache)
            available = ("Answer", "SearchMeta", "ReadRaw") if seen else ("Answer", "SearchMeta")
            action_messages = [{"role": "user", "content": json.dumps({"query": query,
                "memory": memory, "seen_metadata_ids": sorted(seen), "tools": available,
                "instruction": "Choose needed next evidence access, or Answer when sufficient."})}]
            action = self.backend.sample_choice(action_messages, available)
            entry = {"step": step, "memory_cache": cache, "action": action,
                     "observed_ids": keys}
            if action == "Answer":
                trace.append(entry)
                break
            if action == "SearchMeta":
                search_query = self.backend.generate(action_messages + [{"role": "user",
                    "content": "State missing information as a metadata search query."}], sample=False)
                keys, observation = self.search(search_query, seen)
                seen.update(keys)
                entry["search_query"] = search_query
            else:
                key = self.backend.sample_choice(action_messages + [{"role": "user",
                    "content": "Choose observed source ID to read in full."}], tuple(sorted(seen)))
                observation, keys = {key: self.sessions[key]}, [key]
                entry["raw_source_id"] = key
            trace.append(entry)
        answer = self.backend.generate([{"role": "user", "content": json.dumps({
            "query": query, "query_specific_memory": memory,
            "instruction": "Answer using this constructed memory. If insufficient, say so."})}], sample=False)
        return {"answer": answer, "memory": memory, "trace": trace,
                "seen_metadata": sorted(seen), "construction_steps": len(memory)}


class DiscountedLinUCB:
    """Paper's diagonal per-arm discounted update; selected arm feedback only."""
    def __init__(self, priors, dimension, *, alpha=.1, gamma=.95, weights=(.75,.15,.10)):
        if not 0 < gamma < 1 or alpha < 0 or dimension < 1 or len(weights) != 3 or (
                min(weights) < 0 or not math.isclose(sum(weights), 1.)):
            raise ValueError("invalid bandit configuration")
        self.priors = dict(priors)
        if any(not 0 <= prior <= 1 for prior in priors.values()):
            raise ValueError("metadata priors outside [0,1]")
        self.alpha, self.gamma, self.weights = alpha, gamma, weights
        self.a = {key: np.ones(dimension) for key in priors}
        self.b = {key: np.full(dimension, prior / math.sqrt(dimension)) for key, prior in priors.items()}

    def rank(self, context, semantic):
        context = np.asarray(context, dtype=float)
        if not np.isfinite(context).all():
            raise ValueError("nonfinite query embedding")
        w1, w2, w3 = self.weights
        def score(key):
            inverse = 1 / self.a[key]
            bandit = float((inverse * self.b[key]) @ context + self.alpha *
                           math.sqrt(float((context * inverse) @ context)))
            return w1 * semantic[key] + w2 * bandit + w3 * self.priors[key]
        return sorted(semantic, key=score, reverse=True)

    def update(self, selected, context, outcome):
        if outcome not in (0, 1):
            raise ValueError("binary actual execution outcome required")
        context = np.asarray(context, dtype=float)
        self.a[selected] = self.gamma * self.a[selected] + context**2
        self.b[selected] = self.gamma * self.b[selected] + outcome * context


class DualEncoder:
    """Separate real checkpoint encoders, CLS normalization and InfoNCE."""
    def __init__(self, query_checkpoint, tool_checkpoint, *, device="cpu", seed=42):
        import torch
        from transformers import AutoModel, AutoTokenizer
        torch.manual_seed(seed)
        self.query_model = AutoModel.from_pretrained(query_checkpoint, local_files_only=True,
            trust_remote_code=False,use_safetensors=True).to(device)
        self.tool_model = AutoModel.from_pretrained(tool_checkpoint, local_files_only=True,
            trust_remote_code=False,use_safetensors=True).to(device)
        self.query_tokenizer = AutoTokenizer.from_pretrained(query_checkpoint,local_files_only=True,trust_remote_code=False)
        self.tool_tokenizer = AutoTokenizer.from_pretrained(tool_checkpoint,local_files_only=True,trust_remote_code=False)
        self.device = device

    def encode(self, texts, *, tool=False):
        import torch
        model = self.tool_model if tool else self.query_model
        tokenizer = self.tool_tokenizer if tool else self.query_tokenizer
        tokens = tokenizer(texts, padding=True, truncation=True, max_length=256,
                           return_tensors="pt").to(self.device)
        vectors = model(**tokens).last_hidden_state[:, 0].float()
        return torch.nn.functional.normalize(vectors, dim=-1)

    def fit(self, pairs, *, steps=2, temperature=.05, lr=1e-5):
        import torch
        if len(pairs) < 2 or any(pair.get("split") != "train" for pair in pairs):
            raise ValueError("contrastive training requires at least two training-only positive pairs")
        parameters = list(self.query_model.parameters()) + list(self.tool_model.parameters())
        optimizer = torch.optim.AdamW(parameters, lr=lr)
        history = []
        for _ in range(steps):
            queries = self.encode([row["query"] for row in pairs])
            tools = self.encode([row["tool_text"] for row in pairs], tool=True)
            logits = queries @ tools.T / temperature
            # Explicit hard negatives extend the denominator, not supervision.
            hard = [row["hard_negative"] for row in pairs if row.get("hard_negative")]
            if hard:
                logits = torch.cat((logits, queries @ self.encode(hard, tool=True).T / temperature), 1)
            loss = torch.nn.functional.cross_entropy(logits, torch.arange(len(pairs), device=self.device))
            optimizer.zero_grad()
            loss.backward()
            norm = torch.nn.utils.clip_grad_norm_(parameters, 1.)
            optimizer.step()
            history.append({"loss": float(loss.detach()), "gradient_norm": float(norm)})
        self.query_model.eval()
        self.tool_model.eval()
        for parameter in parameters:
            parameter.requires_grad_(False)
        return history


class RATED:
    def __init__(self, encoder, tools, execute, *, top_k=10, weights=(.75,.15,.10)):
        import torch
        self.encoder, self.tools, self.execute, self.top_k = encoder, dict(tools), execute, top_k
        self.keys = tuple(tools)
        with torch.no_grad():
            self.vectors = encoder.encode([tools[key]["text"] for key in self.keys], tool=True).cpu().numpy()
        self.bandit = DiscountedLinUCB({key: tools[key]["prior"] for key in tools},
                                      self.vectors.shape[1], weights=weights)

    def run(self, queries):
        import torch
        history = []
        for row in queries:
            # Reference tool is never passed to encoder, ranking or execution.
            with torch.no_grad():
                context = self.encoder.encode([row["query"]]).cpu().numpy()[0]
            scores = self.vectors @ context
            indices = np.argsort(scores)[::-1][:self.top_k]
            semantic = {self.keys[i]: float(scores[i]) for i in indices}
            selected = self.bandit.rank(context, semantic)[0]
            start = time.perf_counter()
            try:
                result = self.execute(selected, row["query"])
                outcome = int(result["success"])
                error = result.get("error")
            except (RuntimeError, ValueError, TimeoutError, OSError) as exc:
                if str(exc).startswith("sandbox setup failed"):
                    raise  # infrastructure failure is not observed arm utility
                outcome, error = 0, str(exc)
            elapsed = time.perf_counter() - start
            self.bandit.update(selected, context, outcome)
            history.append({"selected": selected, "outcome": outcome,
                            "execution_seconds": elapsed, "error": error})
        return {"steps": len(history), "execution_success_rate": sum(
            row["outcome"] for row in history) / max(1, len(history)), "history": history}


@dataclass(frozen=True)
class WorkflowOutcome:
    task_id: str
    run_id: int
    configuration: str
    success: bool
    decision_seconds: float
    task_seconds: float
    inference_cost: float
    failed_recovery: bool = False
    premature_completion: bool = False


def audit_workflows(outcomes):
    """Aggregate actual paired executions, never paper numbers as local runs."""
    if not outcomes:
        raise ValueError("actual workflow execution records required")
    groups = {}
    for row in outcomes:
        values = (row.decision_seconds, row.task_seconds, row.inference_cost)
        if any(not math.isfinite(value) or value < 0 for value in values):
            raise ValueError("finite nonnegative measured resources required")
        if row.task_seconds < row.decision_seconds:
            raise ValueError("task time cannot be smaller than decision time")
        key = (row.task_id, row.run_id, row.configuration)
        if key in groups:
            raise ValueError("duplicate task/run/configuration")
        groups[key] = row
    configurations = sorted({row.configuration for row in outcomes})
    if len(configurations) != 2:
        raise ValueError("two explicit paired configurations required")
    pair_keys = {configuration: {(r.task_id, r.run_id) for r in outcomes if
                                r.configuration == configuration} for configuration in configurations}
    if pair_keys[configurations[0]] != pair_keys[configurations[1]]:
        raise ValueError("unmatched task/run pairs cannot establish paired comparison")
    metrics = {}
    for configuration in configurations:
        rows = [row for row in outcomes if row.configuration == configuration]
        successes = sum(row.success for row in rows)
        cost = sum(row.inference_cost for row in rows)
        seconds = sum(row.task_seconds for row in rows)
        metrics[configuration] = {"executions": len(rows), "successes": successes,
            "success_rate": successes / len(rows), "mean_decision_seconds": sum(
                row.decision_seconds for row in rows) / len(rows), "mean_task_seconds": seconds / len(rows),
            "cost_per_success": cost / successes if successes else None,
            "time_per_success": seconds / successes if successes else None,
            "failed_recovery_executions": sum(row.failed_recovery for row in rows),
            "premature_completion_executions": sum(row.premature_completion for row in rows),
            "failure_cost_share": sum(row.inference_cost for row in rows if not row.success) /
                                  cost if cost else None}
    matched = [key for key in pair_keys[configurations[0]] if all(
        groups[(*key, configuration)].success for configuration in configurations)]
    return {"configurations": metrics, "matched_success_pairs": len(matched),
            "paired_executions": len(pair_keys[configurations[0]]),
            "model_claim": "evaluation infrastructure; supplied configurations are not automatically Jev"}
