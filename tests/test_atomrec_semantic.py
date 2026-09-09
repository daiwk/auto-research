import json

import pytest

from auto_research.agent_research.atomrec_semantic import SemanticAtomicMemory


def generator(prompt):
    payload = json.loads(prompt.split("\n", 1)[1])
    if prompt.startswith("Identify"):
        return json.dumps({"links": {row["key"]: "shared intent" for row in payload["candidates"]}})
    return json.dumps({"content": "grounded evidence", "keywords": ["care"],
                       "tags": ["product"], "context": "observed"})


def test_semantic_links_and_field_updates_are_executed_with_lineage():
    memory = SemanticAtomicMemory(generator, lambda text: [1.0, 0.5])
    memory.ingest("first", "user", 1, "old preference")
    memory.ingest("second", "item", 2, "new evidence")
    assert memory.atoms["first"].timestamp == 1
    assert len(memory.atoms["first"].revisions) == 1
    assert memory.atoms["second"].links == {"first": "shared intent"}
    assert any(len(path) == 2 for path in memory.retrieve("care", 3, top_k=1)["paths"])
    with pytest.raises(ValueError, match="pre-target"):
        memory.retrieve("care", 2)


def test_invalid_link_cannot_partially_mutate_graph():
    memory = SemanticAtomicMemory(generator, lambda text: [1.0, 0.5])
    memory.ingest("first", "user", 1, "old")
    memory.generate = lambda prompt: ('{"links":{"invented":"bad"}}' if prompt.startswith("Identify")
                                      else generator(prompt))
    with pytest.raises(ValueError, match="invented"):
        memory.ingest("second", "user", 2, "new")
    assert list(memory.atoms) == ["first"] and memory.watermark == 1


def test_generated_fields_are_normalized_to_the_public_memory_budget():
    def verbose(prompt):
        return json.dumps({"content": "c" * 400, "context": "x" * 400,
                           "keywords": ["k" * 80] * 10, "tags": ["t"] * 10})

    memory = SemanticAtomicMemory(verbose, lambda text: [1.0, 0.5])
    memory.ingest("first", "user", 1, "observed")
    atom = memory.atoms["first"]
    assert len(atom.content) == len(atom.context) == 320
    assert len(atom.keywords) == len(atom.tags) == 8
    assert len(atom.keywords[0]) == 64
