import json
from pathlib import Path

import pytest

from auto_research.agent_research.librarian_agents import Workspace, recompute_records

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / "docs/agent-research/2610.22273-librarian-agents/validation/upstream/browsecomp_per_corpus.jsonl"


def test_real_official_compact_records_are_recomputed():
    result = recompute_records(RECORDS, resamples=100, seed=19105)
    assert result["scores"]["base"]["correct"] == 107
    assert result["scores"]["rl"]["correct"] == 282
    assert result["scores"]["base"]["questions"] == 443
    assert result["scores"]["base"]["capped_failure_corpora"] == 14
    assert result["scores"]["rl"]["capped_failure_corpora"] == 0
    assert result["paired_statistics"]["accuracy_difference"]["estimate"] == pytest.approx(175 / 443)
    assert result["paired_statistics"]["ratio_at_10"]["estimate"] == pytest.approx(.662, abs=.001)
    assert result["paired_statistics"]["crossover"]["estimate"] == 31
    assert result["new_model_evaluated"] is False


@pytest.mark.parametrize("corruption", ["duplicate", "missing", "capped", "denominator", "nonfinite", "error"])
def test_ledger_contract_rejects_incomplete_or_corrupt_inputs(tmp_path, corruption):
    rows = [json.loads(line) for line in RECORDS.read_text().splitlines()]
    if corruption == "duplicate":
        rows.append(rows[0])
    elif corruption == "missing":
        rows.pop()
    elif corruption == "capped":
        row = next(r for r in rows if r["status"] == "max_token_capped_failure")
        row["amortization_correct_sum"] = 1
    elif corruption == "denominator":
        rows[0]["expected_questions"] += 1
    elif corruption == "nonfinite":
        rows[0]["builder_tokens"] = float("nan")
    else:
        rows[0]["status"] = "judge_error"
    path = tmp_path / "records.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows))
    with pytest.raises(ValueError):
        recompute_records(path, resamples=10)


def test_real_filesystem_create_merge_delete_preserves_fallback_and_provenance(tmp_path):
    calls = []
    def executor(title, sources):
        calls.append((title, sources))
        return "\n".join(text for _, text in sources)
    workspace = Workspace(tmp_path / "workspace", {"a.txt": "fact alpha", "nested/b.txt": "fact beta"})
    a = workspace.create("alpha", ["raw_docs/a.txt"], executor)
    b = workspace.create("beta", ["raw_docs/nested/b.txt"], executor)
    merged = workspace.merge("combined", [a, b], executor)
    assert workspace.nodes[a]["parent"] == merged
    assert workspace.nodes[merged]["raw_sources"] == ["raw_docs/a.txt", "raw_docs/nested/b.txt"]
    workspace.delete(a)
    assert not workspace.nodes[a]["active"]
    assert workspace.read("raw_docs/a.txt") == "fact alpha"
    assert (workspace.root / "history" / a / "summary.md").exists()
    assert "raw_docs/a.txt" in workspace.nodes[merged]["raw_sources"]
    assert "fact alpha" in workspace.read("synthetic_fs/" + merged + "/summary.md")
    assert (workspace.root / "synthetic_fs" / merged / b / "summary.md").exists()
    digest = workspace.stop()
    assert len(digest) == 64 and (workspace.root / "snapshot.json").exists()
    restored = Workspace.load(workspace.root, expected_sha256=digest)
    assert restored.nodes == workspace.nodes
    assert restored.read("raw_docs/a.txt") == "fact alpha"
    assert len(calls) == 3  # no reference, future question or gold passed to executor
    with pytest.raises(ValueError, match="stopped"):
        workspace.create("late", ["raw_docs/a.txt"], executor)


def test_raw_cannot_be_deleted_and_paths_or_symlinks_cannot_escape(tmp_path):
    workspace = Workspace(tmp_path / "workspace", {"a.txt": "original"})
    with pytest.raises(ValueError):
        workspace.delete("raw_docs/a.txt")
    with pytest.raises(ValueError):
        workspace.read("../outside")
    with pytest.raises(ValueError):
        workspace.create("bad", ["unknown"], lambda *_: "x")
    (workspace.root / "synthetic_fs/escape").symlink_to(tmp_path)
    with pytest.raises(ValueError):
        workspace.read("synthetic_fs/escape/anything")
    (workspace.root / "raw_docs/a.txt").write_text("tampered")
    with pytest.raises(ValueError, match="modified"):
        workspace.stop()


def test_cold_load_detects_synthetic_tampering(tmp_path):
    workspace = Workspace(tmp_path / "workspace", {"a.txt": "original"})
    node = workspace.create("synthetic", ["raw_docs/a.txt"], lambda *_: "summary")
    digest = workspace.stop()
    (workspace.root / "synthetic_fs" / node / "summary.md").write_text("corrupted")
    with pytest.raises(ValueError):
        Workspace.load(workspace.root, expected_sha256=digest)


def test_deleted_parent_promotes_children_and_snapshot_is_content_addressed(tmp_path):
    workspace = Workspace(tmp_path / "workspace", {"a.txt": "original"})
    child = workspace.create("child", ["raw_docs/a.txt"], lambda *_: "summary")
    parent = workspace.merge("parent", [child], lambda *_: "index")
    workspace.delete(parent)
    assert (workspace.root / "synthetic_fs" / child / "summary.md").is_file()
    digest = workspace.stop()
    assert Workspace.load(workspace.root, expected_sha256=digest).nodes[child]["parent"] is None
    with pytest.raises(ValueError, match="hash"):
        Workspace.load(workspace.root, expected_sha256="0" * 64)
