"""LM-built atomic fields, semantic links, field evolution and path retrieval."""
from copy import deepcopy
from dataclasses import dataclass, field
import json

import numpy as np


@dataclass
class SemanticAtom:
    key: str
    owner: str
    timestamp: int
    content: str
    keywords: list[str]
    tags: list[str]
    context: str
    embedding: np.ndarray
    links: dict[str, str] = field(default_factory=dict)
    revisions: list[dict] = field(default_factory=list)

    def public(self):
        return {name: deepcopy(getattr(self, name)) for name in
                ("key", "owner", "timestamp", "content", "keywords", "tags", "context", "links")}


class SemanticAtomicMemory:
    """No default heuristic LM/encoder: both real dependencies are mandatory."""
    def __init__(self, generate, encode, capacity=128, neighbors=4, threshold=0.7):
        self.generate, self.encode = generate, encode
        self.capacity, self.neighbors, self.threshold = capacity, neighbors, threshold
        self.atoms = {}
        self.trace = []
        self.watermark = -1

    def _json(self, purpose, payload):
        text = self.generate(purpose + "\n" + json.dumps(payload))
        if text.strip().startswith("```json") and text.strip().endswith("```"):
            text = text.strip()[7:-3]
        value = json.loads(text)
        if not isinstance(value, dict):
            raise ValueError("memory operation must return a JSON object")
        return value

    def _fields(self, value):
        fields = {name: value[name] for name in ("content", "keywords", "tags", "context")}
        if not all(isinstance(fields[name], str) for name in ("content", "context")):
            raise ValueError("content/context must be strings")
        if not all(isinstance(fields[name], list) and all(isinstance(v, str) for v in fields[name])
                   for name in ("keywords", "tags")):
            raise ValueError("keywords/tags must be string lists")
        # Schema normalization is independent of relevance labels and keeps a
        # verbose checkpoint response from growing the memory without bound.
        fields["content"] = fields["content"][:320]
        fields["context"] = fields["context"][:320]
        for name in ("keywords", "tags"):
            fields[name] = [item[:64] for item in fields[name][:8]]
        embedding = np.asarray(self.encode(json.dumps(fields)), dtype=float)
        if embedding.ndim != 1 or not np.isfinite(embedding).all() or np.linalg.norm(embedding) == 0:
            raise ValueError("invalid text embedding")
        return fields, embedding / np.linalg.norm(embedding)

    def ingest(self, key, owner, timestamp, evidence):
        if timestamp < self.watermark:
            raise ValueError("ingest interactions chronologically")
        if key in self.atoms:
            raise ValueError("new interaction requires a unique atomic key")
        fields, embedding = self._fields(self._json(
            'Extract one grounded atomic note. Return only JSON with content, keywords (list), tags (list), context. '
            'Keep each field brief; do not infer unobserved interactions.', {"evidence": evidence}))
        atom = SemanticAtom(key, owner, timestamp, **fields, embedding=embedding)
        neighbors = sorted(((float(embedding @ old.embedding), old.key)
                            for old in self.atoms.values() if old.timestamp <= timestamp), reverse=True)[:self.neighbors]
        if neighbors:
            links = self._json(
                'Identify supported semantic links. Return only JSON {"links":{"existing_id":"brief relation"}}; '
                'keys must be from allowed_existing_ids, never the new note or a product ID. Empty links are allowed.',
                {"new": {key: value for key, value in atom.public().items() if key != "key"},
                 "allowed_existing_ids": [k for _, k in neighbors],
                 "candidates": [self.atoms[k].public() for _, k in neighbors]},
            ).get("links", {})
            if not isinstance(links, dict) or not set(links) <= {k for _, k in neighbors}:
                raise ValueError("semantic linker invented an identifier")
            if not all(isinstance(value, str) for value in links.values()):
                raise ValueError("semantic link relation must be text")
            atom.links = links
        # Stage all changes. Malformed output cannot partially mutate memory.
        evolved = {}
        for similarity, neighbor in neighbors:
            if neighbor not in atom.links and similarity <= self.threshold:
                continue
            old = self.atoms[neighbor]
            updates, vector = self._fields(self._json(
                'Return ONLY one compact JSON object with exactly content, keywords, tags, context. '
                'Refine the historical note using the new observed note; preserve its meaning, add no external facts, '
                'and keep content/context under 320 characters and each list at most 8 short strings.',
                {"historical": {name: getattr(old, name) for name in
                                ("content", "keywords", "tags", "context")},
                 "new_observation": {name: getattr(atom, name) for name in
                                     ("content", "keywords", "tags", "context")}},
            ))
            replacement = deepcopy(old)
            replacement.revisions.append(old.public())
            for field_name, value in updates.items():
                setattr(replacement, field_name, value)
            replacement.embedding = vector
            replacement.links[key] = atom.links.get(neighbor, "new related evidence")
            evolved[neighbor] = replacement
        self.atoms.update(evolved)
        self.atoms[key] = atom
        self.watermark = timestamp
        while len(self.atoms) > self.capacity:
            victim = min(self.atoms, key=lambda k: (self.atoms[k].timestamp, k))
            del self.atoms[victim]
            for value in self.atoms.values():
                value.links.pop(victim, None)
        self.trace.append({"key": key, "linked": list(atom.links), "evolved": list(evolved)})

    def retrieve(self, query, timestamp, top_k=3, hops=2):
        if timestamp <= self.watermark:
            raise ValueError("query precedes evolved memory; rebuild a pre-target snapshot")
        vector = np.asarray(self.encode(query), dtype=float)
        vector /= max(np.linalg.norm(vector), 1e-12)
        visible = {key: atom for key, atom in self.atoms.items() if atom.timestamp < timestamp}
        ranked = sorted(visible, key=lambda k: float(vector @ visible[k].embedding), reverse=True)[:top_k]
        paths = [(key,) for key in ranked]
        frontier, visited = paths[:], set(ranked)
        for _ in range(hops):
            next_frontier = []
            for path in frontier:
                for neighbor in visible[path[-1]].links:
                    if neighbor in visible and neighbor not in visited:
                        next_frontier.append((*path, neighbor))
                        visited.add(neighbor)
            paths.extend(next_frontier)
            frontier = next_frontier
        return {"notes": [visible[path[-1]].public() for path in paths], "paths": paths}

    def synthesize(self, query, timestamp):
        evidence = self.retrieve(query, timestamp)
        summary = self.generate(
            "Summarize recommendation evidence using only these linked memories; preserve evidence IDs.\n"
            + json.dumps({"query": query, **evidence}))
        return summary, evidence
