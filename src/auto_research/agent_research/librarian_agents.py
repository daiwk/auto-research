"""Librarian public result recomputation and bounded filesystem contracts.

The filesystem executor is a caller-supplied content function, not a learned
builder. No RL, answerer, judge, or checkpoint is claimed by this module.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import random
import shutil
import statistics

UPSTREAM_REVISION = "455ac88c81c639c10a8404464dabf71a7fbb563e"


def _percentile(values, p):
    ordered = sorted(values)
    position = p * (len(ordered) - 1)
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] * (high - position) + ordered[high] * (position - low) if high != low else ordered[low]


def recompute_records(path: Path, *, resamples=10000, seed=19105) -> dict:
    """Paired corpus bootstrap of the official 50-corpus/443-question ledger."""
    if resamples < 2:
        raise ValueError("at least two bootstrap draws required")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    arms = {"base": {}, "rl": {}}
    for row in rows:
        arm = "rl" if row["arm"] == "ft" else row["arm"]
        cid = row["corpus_id"]
        if arm not in arms or cid in arms[arm]:
            raise ValueError("unexpected arm or duplicate corpus")
        if row["status"] not in {"complete", "max_token_capped_failure"}:
            raise ValueError("answerer/judge/infrastructure errors invalidate a result")
        q, observed, correct = row["expected_questions"], row["observed_questions"], row["amortization_correct_sum"]
        if not isinstance(q, int) or q <= 0 or not isinstance(observed, int) or not 0 <= observed <= q:
            raise ValueError("invalid full question denominator")
        values = (correct, row["builder_tokens"], row["answerer_total_tokens_read"])
        if any(not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0 for v in values):
            raise ValueError("finite nonnegative observed metrics required")
        if correct > observed or row["builder_tokens"] <= 0:
            raise ValueError("correctness/token count invalid")
        if row["status"] == "max_token_capped_failure" and (correct != 0 or observed != 0):
            raise ValueError("incomplete construction must retain all questions with zero score")
        if row["status"] == "complete" and observed != q:
            raise ValueError("complete corpus missing question observations")
        arms[arm][cid] = row
    cids = sorted(arms["base"])
    if len(cids) != 50 or set(cids) != set(arms["rl"]):
        raise ValueError("exactly 50 matched corpora required")
    for cid in cids:
        if arms["base"][cid]["expected_questions"] != arms["rl"][cid]["expected_questions"]:
            raise ValueError("unmatched corpus question denominator")
    if any(sum(r["expected_questions"] for r in arms[a].values()) != 443 for a in arms):
        raise ValueError("official ledger requires all 443 questions")

    def components(ids, arm):
        selected = [arms[arm][cid] for cid in ids]
        q = sum(r["expected_questions"] for r in selected)
        correct = sum(r["amortization_correct_sum"] for r in selected)
        tokens = sum(r["builder_tokens"] for r in selected)
        return {"questions": q, "correct": correct, "accuracy": correct / q,
                "builder_tokens": tokens, "builder_tokens_per_corpus": tokens / len(selected),
                "answer_tokens_per_question": sum(r["answerer_total_tokens_read"] * r["expected_questions"]
                                                  for r in selected) / q,
                "correct_per_million_builder_tokens": correct / tokens * 1e6,
                "capped_failure_corpora": sum(r["status"] == "max_token_capped_failure" for r in selected)}

    def expected_correct_tokens(c, queries):
        if c["accuracy"] <= 0:
            return None
        return (c["builder_tokens_per_corpus"] / queries + c["answer_tokens_per_question"]) / c["accuracy"]

    def crossover(base, rl):
        fixed = rl["builder_tokens_per_corpus"] / rl["accuracy"] - base["builder_tokens_per_corpus"] / base["accuracy"]
        slope = rl["answer_tokens_per_question"] / rl["accuracy"] - base["answer_tokens_per_question"] / base["accuracy"]
        crossing = -fixed / slope if slope else -1
        return max(1, math.ceil(crossing)) if crossing > 0 else None

    scores = {arm: components(cids, arm) for arm in arms}
    samples = {key: [] for key in ("accuracy_difference", "efficiency_ratio", "ratio_at_10", "crossover")}
    accuracy_samples = {arm: [] for arm in arms}
    rng = random.Random(seed)
    zero_accuracy_draws, no_crossover_draws = 0, 0
    for _ in range(resamples):
        ids = [rng.choice(cids) for _ in cids]
        base, rl = components(ids, "base"), components(ids, "rl")
        for arm, c in (("base", base), ("rl", rl)):
            accuracy_samples[arm].append(c["accuracy"])
        samples["accuracy_difference"].append(rl["accuracy"] - base["accuracy"])
        if min(base["accuracy"], rl["accuracy"]) == 0:
            zero_accuracy_draws += 1
            continue
        samples["efficiency_ratio"].append(rl["correct_per_million_builder_tokens"] / base["correct_per_million_builder_tokens"])
        samples["ratio_at_10"].append(expected_correct_tokens(rl, 10) / expected_correct_tokens(base, 10))
        crossing = crossover(base, rl)
        if crossing is None:
            no_crossover_draws += 1
        else:
            samples["crossover"].append(crossing)
    for arm in arms:
        scores[arm]["accuracy_cluster_bootstrap_se"] = statistics.stdev(accuracy_samples[arm])
    base, rl = scores["base"], scores["rl"]
    estimates = {"accuracy_difference": rl["accuracy"] - base["accuracy"],
                 "efficiency_ratio": rl["correct_per_million_builder_tokens"] / base["correct_per_million_builder_tokens"],
                 "ratio_at_10": expected_correct_tokens(rl, 10) / expected_correct_tokens(base, 10),
                 "crossover": crossover(base, rl)}
    statistics_out = {key: {"estimate": value,
                           "ci95": [_percentile(samples[key], .025), _percentile(samples[key], .975)]
                           if samples[key] else None} for key, value in estimates.items()}
    return {"schema_version": 2, "implementation_status": "evaluation_protocol_interface",
            "evidence_kind": "official_compact_records_recomputation", "new_model_evaluated": False,
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "upstream_revision": UPSTREAM_REVISION, "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "corpora": 50, "scores": scores, "paired_statistics": statistics_out,
            "bootstrap": {"unit": "paired_corpus", "resamples": resamples, "seed": seed,
                          "zero_accuracy_draws": zero_accuracy_draws, "no_crossover_draws": no_crossover_draws},
            "reuse": {str(n): {arm: {"tokens_per_query": c["builder_tokens_per_corpus"] / n + c["answer_tokens_per_question"],
                                     "tokens_per_expected_correct": expected_correct_tokens(c, n)}
                               for arm, c in scores.items()} for n in (1, 2, 5, 10, 20, 25, 50, 100)}}


class Workspace:
    """Real bounded on-disk workspace; raw fallback and provenance are immutable.

    Only explicit create/merge/delete/stop methods mutate synthetic artifacts.
    No shell, arbitrary code execution, or gold/query argument is accepted.
    """

    def __init__(self, root: Path, documents: dict[str, str]):
        self.root = root.resolve()
        if self.root.exists() or not documents:
            raise ValueError("new workspace root and nonempty raw corpus required")
        self.root.mkdir(parents=True)
        (self.root / "raw_docs").mkdir()
        (self.root / "synthetic_fs").mkdir()
        (self.root / "history").mkdir()
        self.raw_hashes, self.nodes, self.stopped = {}, {}, False
        for name, content in documents.items():
            self._relative(name)
            path = self.root / "raw_docs" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            self.raw_hashes["raw_docs/" + name] = hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def _relative(path):
        parts = PurePosixPath(path)
        if not isinstance(path, str) or not path or parts.is_absolute() or ".." in parts.parts or "\\" in path:
            raise ValueError("unsafe relative path")
        return parts

    def _check_raw(self):
        for name, digest in self.raw_hashes.items():
            path = self.root / name
            if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != self.root.parent):
                raise ValueError("symlink source is forbidden")
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError("raw source modified")

    def _node_path(self, node_id):
        node = self.nodes[node_id]
        if not node["active"]:
            return self.root / "history" / node_id / "summary.md"
        chain, seen = [node_id], {node_id}
        parent = node["parent"]
        while parent is not None:
            if parent in seen:
                raise ValueError("cyclic filesystem hierarchy")
            seen.add(parent)
            chain.append(parent)
            parent = self.nodes[parent]["parent"]
        return self.root.joinpath("synthetic_fs", *reversed(chain), "summary.md")

    def _write(self, node_id):
        node = self.nodes[node_id]
        metadata = json.dumps({k: v for k, v in node.items() if k != "content"}, sort_keys=True)
        path = self._node_path(node_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(metadata + "\n\n" + node["content"])

    def create(self, title: str, sources: list[str], executor) -> str:
        if self.stopped:
            raise ValueError("construction already stopped")
        self._check_raw()
        if not title.strip() or not sources or len(sources) != len(set(sources)):
            raise ValueError("title and distinct source references required")
        texts, raw = [], set()
        for source in sources:
            self._relative(source)
            if source in self.raw_hashes:
                texts.append((source, (self.root / source).read_text()))
                raw.add(source)
            elif source in self.nodes:
                node = self.nodes[source]
                texts.append((source, node["content"]))
                raw.update(node["raw_sources"])
            else:
                raise ValueError("unknown provenance source")
        # Executor receives source material, not future queries or references.
        content = executor(title, tuple(texts))
        if not isinstance(content, str) or not content.strip():
            raise ValueError("executor must return nonempty synthetic content")
        identity = hashlib.sha256(json.dumps([title, sources, content, len(self.nodes)], sort_keys=True).encode()).hexdigest()[:20]
        self.nodes[identity] = {"id": identity, "title": title, "content": content,
                                "creation_index": len(self.nodes),
                                "direct_sources": list(sources), "raw_sources": sorted(raw),
                                "children": [], "parent": None, "active": True}
        self._write(identity)
        return identity

    def merge(self, title, children, executor):
        if not children or any(child not in self.nodes or not self.nodes[child]["active"] for child in children):
            raise ValueError("merge requires active synthetic children")
        if any(self.nodes[child]["parent"] is not None for child in children):
            raise ValueError("child already nested; no implicit reparenting")
        identity = self.create(title, list(children), executor)
        self.nodes[identity]["children"] = list(children)
        for child in children:
            old = self._node_path(child).parent
            self.nodes[child]["parent"] = identity
            shutil.move(str(old), str(self._node_path(child).parent))
            self._write(child)
        self._write(identity)
        return identity

    def delete(self, identity):
        if self.stopped or identity not in self.nodes or not self.nodes[identity]["active"]:
            raise ValueError("only active synthetic nodes may be deleted")
        self._check_raw()
        node = self.nodes[identity]
        if node["parent"] is not None:
            parent = self.nodes[node["parent"]]
            parent["children"].remove(identity)
            self._write(parent["id"])
        for child in node["children"]:
            old = self._node_path(child).parent
            self.nodes[child]["parent"] = None
            shutil.move(str(old), str(self._node_path(child).parent))
            self._write(child)
        old = self._node_path(identity).parent
        node["active"], node["parent"], node["children"] = False, None, []
        shutil.move(str(old), str(self._node_path(identity).parent))
        self._write(identity)

    def read(self, path: str):
        self._relative(path)
        self._check_raw()
        target = self.root / path
        if not target.resolve().is_relative_to(self.root) or target.is_symlink():
            raise ValueError("workspace escape")
        return target.read_text()

    def stop(self):
        self._check_raw()
        self.stopped = True
        snapshot = {"schema_version": 1, "raw_hashes": self.raw_hashes,
                    "nodes": deepcopy(self.nodes), "stopped": True}
        path = self.root / "snapshot.json"
        with path.open("x") as handle:
            json.dump(snapshot, handle, sort_keys=True)
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @classmethod
    def load(cls, root: Path, *, expected_sha256: str):
        """Cold-load data only; validate raw hashes, hierarchy, and disk contents."""
        instance = cls.__new__(cls)
        instance.root = root.resolve()
        snapshot_path = instance.root / "snapshot.json"
        if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != expected_sha256:
            raise ValueError("snapshot hash mismatch")
        snapshot = json.loads(snapshot_path.read_text())
        if snapshot.get("schema_version") != 1 or snapshot.get("stopped") is not True:
            raise ValueError("unsupported workspace snapshot")
        instance.raw_hashes, instance.nodes, instance.stopped = snapshot["raw_hashes"], snapshot["nodes"], True
        for raw in instance.raw_hashes:
            cls._relative(raw)
            if not raw.startswith("raw_docs/"):
                raise ValueError("raw path outside raw_docs")
        instance._check_raw()
        memo, visiting = {}, set()

        def provenance(identity):
            if identity in instance.raw_hashes:
                return {identity}
            if identity in memo:
                return memo[identity]
            if identity not in instance.nodes or identity in visiting:
                raise ValueError("missing/cyclic provenance")
            visiting.add(identity)
            sources = instance.nodes[identity]["direct_sources"]
            if not sources or len(sources) != len(set(sources)):
                raise ValueError("empty/duplicate provenance")
            result = set().union(*(provenance(source) for source in sources))
            visiting.remove(identity)
            memo[identity] = result
            return result

        for identity, node in instance.nodes.items():
            if node["id"] != identity or len(identity) != 20 or any(c not in "0123456789abcdef" for c in identity):
                raise ValueError("invalid synthetic identity")
            if node["parent"] is not None and node["parent"] not in instance.nodes:
                raise ValueError("missing parent")
            if not set(node["raw_sources"]) <= set(instance.raw_hashes):
                raise ValueError("unknown raw provenance")
            if not set(node["direct_sources"]) <= set(instance.nodes) | set(instance.raw_hashes):
                raise ValueError("unknown direct provenance")
            expected_id = hashlib.sha256(json.dumps(
                [node["title"], node["direct_sources"], node["content"], node["creation_index"]],
                sort_keys=True).encode()).hexdigest()[:20]
            if expected_id != identity or set(node["raw_sources"]) != provenance(identity):
                raise ValueError("identity/provenance mismatch")
            for child in node["children"]:
                if child not in instance.nodes or instance.nodes[child]["parent"] != identity:
                    raise ValueError("inconsistent parent/child hierarchy")
            path = instance._node_path(identity)
            if not path.resolve().is_relative_to(instance.root) or path.is_symlink():
                raise ValueError("snapshot path escape")
            metadata, content = path.read_text().split("\n\n", 1)
            if json.loads(metadata) != {k: v for k, v in node.items() if k != "content"} or content != node["content"]:
                raise ValueError("synthetic content/snapshot mismatch")
        return instance
