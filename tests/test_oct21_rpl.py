from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import runpy

import pytest

from auto_research.agent_research.retrieval_program import (
    Document, RetrievalProgram, RetrievalSDK, continuation_context, dedup, execute,
    mutations, reciprocal_rank_fusion, structural_distance, supervision_spans, verified_mutation,
)


DOCS = tuple(Document(str(i), f"public document {i}") for i in range(50))


def sdk():
    return RetrievalSDK(lambda query, k: DOCS[:k], lambda query, k: tuple(reversed(DOCS))[:k],
        lambda query, docs, k: tuple(reversed(docs))[:k])


def test_actual_fusion_uses_ranks_not_backend_order_and_deduplicates_each_list():
    a, b, c = DOCS[:3]
    assert reciprocal_rank_fusion(((a, b), (c, b))) == (b, a, c)
    assert reciprocal_rank_fusion(((a, a, b), (b,))) == (b, a)
    assert dedup((a, b, a)) == (a, b)
    with pytest.raises(ValueError, match="conflicting"):
        reciprocal_rank_fusion(((a,), (Document(a.identifier, "different"),)))


def test_conflicting_ids_are_rejected_within_single_and_across_rankings():
    original = DOCS[0]
    conflict = Document(original.identifier, "contradictory public content")
    with pytest.raises(ValueError, match="conflicting"):
        dedup((original, conflict))
    with pytest.raises(ValueError, match="conflicting"):
        reciprocal_rank_fusion(((original, conflict), (DOCS[1],)))
    with pytest.raises(ValueError, match="conflicting"):
        reciprocal_rank_fusion(((original,), (conflict,)))
    assert dedup((original, original)) == (original,)
    backend = RetrievalSDK(lambda q, k: (original, conflict), lambda q, k: (original,), lambda q, d, k: d[:k])
    with pytest.raises(ValueError, match="conflicting"):
        execute(RetrievalProgram(("q",), "dense"), backend)
    with pytest.raises(ValueError, match="conflicting"):
        execute(RetrievalProgram(("q",), "fuse"), backend)


def test_breadth_and_observation_are_decoupled_and_no_intermediate_docs_are_exposed():
    program = RetrievalProgram(("question A", "question B"), "fuse", 10, 3, 2)
    result = execute(program, sdk())
    assert result.retrieved_candidates == 40 and result.unique_candidates == 20
    assert result.primitive_calls == 5 and len(result.printed) == 2
    assert set(asdict(result)) == {"printed", "retrieved_candidates", "unique_candidates", "primitive_calls"}


@pytest.mark.parametrize("kwargs", [
    {"queries": ()}, {"queries": ("same", "same")}, {"queries": ("",)},
    {"queries": ["query"]}, {"queries": ("q",), "breadth": True},
    {"queries": ("q",), "breadth": 4}, {"queries": ("q",), "retention": 1},
    {"queries": ("q",), "modality": "exec"}, {"queries": ("q",), "output_limit": 21},
])
def test_grammar_rejects_unbounded_or_invalid_programs(kwargs):
    with pytest.raises(ValueError):
        RetrievalProgram(**kwargs)


def test_query_is_data_not_executable_python():
    malicious_text = "__import__('os').system('touch /tmp/should-not-execute')"
    seen = []
    callback = lambda query, k: seen.append(query) or DOCS[:k]
    result = execute(RetrievalProgram((malicious_text,)), RetrievalSDK(callback, callback, lambda q, docs, k: docs[:k]))
    assert seen == [malicious_text] and len(result.printed) == 3


def test_nearest_mutations_preserve_queries_and_apply_lexicographic_order():
    original = RetrievalProgram(("query-a", "query-b"), "dense", 3, 0, 5)
    candidates = mutations(original)
    assert len(candidates) == 224 and original not in candidates
    assert all(set(item.queries) <= set(original.queries) for item in candidates)
    distances = [structural_distance(item, original) for item in candidates]
    assert distances == sorted(distances)
    # All calls share breadth; fusion is imposed by execute for multiple lists.
    assert all(item.breadth in (3, 5, 10, 20, 50) for item in candidates)


def test_execution_verified_mutation_has_a_real_negative_control_and_budget_failures():
    original = RetrievalProgram(("q",), breadth=3, output_limit=5)
    verifier = lambda result: DOCS[4] in result.printed
    assert not verifier(execute(original, sdk()))
    selected, trials = verified_mutation(original, sdk(), verifier=verifier)
    assert selected is not None and selected.program.breadth == 5
    assert selected.retrieval_verified and verifier(selected.execution) and len(trials) >= 1
    absent, capped = verified_mutation(original, sdk(), verifier=lambda _: False, max_executions=2)
    assert absent is None and len(capped) == 2


def test_reranker_cannot_inject_unretrieved_gold_or_exceed_budget():
    program = RetrievalProgram(("q",), retention=3)
    for invalid in ((DOCS[49],), (DOCS[0], DOCS[0]), DOCS[:4]):
        backend = RetrievalSDK(lambda q, k: DOCS[:k], lambda q, k: DOCS[:k], lambda q, docs, k: invalid)
        with pytest.raises(ValueError):
            execute(program, backend)
    with pytest.raises(ValueError, match="budget"):
        execute(RetrievalProgram(("q",)), RetrievalSDK(lambda q, k: DOCS, lambda q, k: DOCS, lambda q, d, k: d))


def test_reference_verification_does_not_enter_continuation_and_wrong_answer_is_masked():
    selected, _ = verified_mutation(RetrievalProgram(("q",)), sdk(), verifier=lambda result: DOCS[4] in result.printed)
    context = continuation_context("public question", selected)
    assert set(asdict(context)) == {"question", "program", "printed_evidence"}
    assert not hasattr(context, "verifier") and not hasattr(context, "answer")
    assert supervision_spans(retrieval_verified=True, answer_verified=False) == {
        "program": True, "environment_observation": False, "answer": False}
    with pytest.raises(ValueError):
        supervision_spans(retrieval_verified=False, answer_verified=True)


def test_runner_performs_component_execution_without_claiming_neural_retrieval():
    runner = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_oct21_rpl.py"))
    metrics = runner["diagnostic"](42)["metrics"]
    assert metrics["baseline_fixture_support_covered"] == 0
    assert metrics["selected_fixture_support_covered"] == 1
    assert metrics["wide_program_retrieved_candidates"] == 20
    assert metrics["wide_program_printed_documents"] == 3
    assert metrics["actual_llm_calls"] == 0


def test_meta_affiliation_publication_date_and_non_reproduction_catalog_contract():
    root = Path(__file__).resolve().parents[1]
    rows = {key: json.loads((root / "src/auto_research/paper_specs/catalog/agent-research" / f"{key}.json").read_text())
            for key in ("rpl", "cache-engineering")}
    assert rows["rpl"]["published_at"] == "2026-10-17T20:03:09Z"
    assert rows["rpl"]["first_author_affiliation"] == "KAIST AI / Meta Superintelligence Labs"
    assert rows["rpl"]["code"] == "https://github.com/facebookresearch/retrieval-programs"
    assert rows["rpl"]["upstream_revision"] == "992fda1f5f0eb01a8fb70202ff8f7a65aed48465"
    assert "CC BY-NC 4.0" in rows["rpl"]["code_license"]
    assert "不复制到本地或升级既有L1证据" in rows["rpl"]["code_status"]
    assert rows["rpl"]["implementation_status"] == "component_only"
    assert rows["cache-engineering"]["implementation_status"] == "deferred_high_cost"
    assert rows["cache-engineering"]["code"] == "https://github.com/thu-nics/AKV"
    for key, row in rows.items():
        assert row["review_done"] and row["full_experiment_status"] == "not_reproduced_high_cost"
        assert row["diagnostic_only"] and not row["promotion_eligible"] and not row["evolve_integrated"]
        detail = root / "docs" / row["detail_path"]
        text = detail.read_text()
        for label in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "本地 Adapter", "本地复现代码",
                      "成本过高，不复现（审查 DONE）", "paper-figure:start"):
            assert label in text
        provenance = json.loads((detail.parent / "assets/provenance.json").read_text())
        image = (detail.parent / "assets" / provenance["asset"]).read_bytes()
        assert hashlib.sha256(image).hexdigest() == provenance["asset_sha256"]
        if key == "cache-engineering":
            assert "local_operator" not in row and "local_command" not in row
            assert "requires_gpu_validation" not in row and not list((detail.parent / "metrics").glob("*.json"))
