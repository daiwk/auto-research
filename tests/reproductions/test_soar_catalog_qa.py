"""L0 preparation contracts; no checkpoint or capability evidence."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest


SCRIPT=Path(__file__).resolve().parents[2]/"scripts/prepare_soar_catalog_qa.py"


def module():
    spec=importlib.util.spec_from_file_location("soar_catalog_prepare",SCRIPT)
    value=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def fixture_rows():
    return [{"uid":"catalog-identifier-"+str(i),"name":"Public Tool "+str(i),
             "source":"public-collection","url":"https://example.org/docs/tool/"+str(i),
             "tags":"tool-doc","description":"Original independent description "+str(i),
             "answer":"DO NOT EXPOSE","label":"1","reliability_score":"0.9"} for i in range(100)]


def catalog_file(tmp_path,rows):
    path=tmp_path/"tools_clean_with_reliability.csv"
    with path.open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_label_and_quality_changes_cannot_change_independent_kb():
    prepare=module()
    rows=fixture_rows()
    original=prepare.encode_rows(prepare.independent_documents(rows))
    for row in rows:
        row.update(answer="CHANGED SECRET GOLD",label="0",reliability_score="0.01",ground_truth="PLAN")
    assert original==prepare.encode_rows(prepare.independent_documents(rows))
    assert b"SECRET" not in original and b"DO NOT EXPOSE" not in original
    selected,groups=prepare.partition_questions(rows,train_tools=4,validation_tools=3)
    assert len(selected["train"])==4 and len(selected["validation"])==3
    assert set(groups["train"]).isdisjoint(groups["validation"])


def test_same_uid_never_crosses_question_splits_and_duplicate_catalog_rejected(tmp_path,monkeypatch):
    prepare=module()
    rows=fixture_rows()
    _,groups=prepare.partition_questions(rows,train_tools=8,validation_tools=4)
    assert set(groups["train"]).isdisjoint(groups["validation"])
    rows[-1]["uid"]=rows[0]["uid"]
    path=catalog_file(tmp_path,rows)
    monkeypatch.setattr(prepare,"CATALOG_SHA",hashlib.sha256(path.read_bytes()).hexdigest())
    output=tmp_path/"cannot-exist"
    monkeypatch.setattr(sys,"argv",[str(SCRIPT),"--catalog",str(path),"--output",str(output)])
    with pytest.raises(ValueError,match="identifiers are not unique"):
        prepare.main()
    assert not output.exists()


def test_preparation_reads_only_catalog_and_own_generator_not_train_pairs_or_test(tmp_path,monkeypatch):
    prepare=module()
    path=catalog_file(tmp_path,fixture_rows())
    (tmp_path/"train_pairs.csv").write_text("MUST NOT OPEN")
    (tmp_path/"eval_real_test.jsonl").write_text("MUST NOT OPEN")
    monkeypatch.setattr(prepare,"CATALOG_SHA",hashlib.sha256(path.read_bytes()).hexdigest())
    original_open=Path.open
    reads=[]
    def tracked_open(self,mode="r",*args,**kwargs):
        if "r" in mode:
            reads.append(self.resolve())
            assert self.resolve() in {path.resolve(),SCRIPT.resolve()}
        return original_open(self,mode,*args,**kwargs)
    output=tmp_path/"prepared"
    monkeypatch.setattr(Path,"open",tracked_open)
    monkeypatch.setattr(sys,"argv",[str(SCRIPT),"--catalog",str(path),"--output",str(output)])
    prepare.main()
    assert path.resolve() in reads and SCRIPT.resolve() in reads
    monkeypatch.setattr(Path,"open",original_open)
    kb=json.loads((output/"kb/provenance.json").read_text())
    split=json.loads((output/"split.json").read_text())
    assert kb["qa_selection_input_read"] is False and kb["train_pairs_input_read"] is False
    assert kb["official_test_opened"] is False and split["test_opened"] is False
    assert split["tool_groups_disjoint"] is True
    assert "NOT an EcoAgent official train split" in split["source_split_semantics"]
    for name,value in split["partition_sha256"].items():
        assert hashlib.sha256((output/(name+".jsonl")).read_bytes()).hexdigest()==value
    assert hashlib.sha256((output/"kb/documents.jsonl").read_bytes()).hexdigest()==kb["files"]["documents.jsonl"]


def test_bad_catalog_hash_and_caller_revision_override_fail_closed(tmp_path,monkeypatch):
    prepare=module()
    assert prepare.REVISION=="bc5db40a20b254c5249401d2220ea71b06c86a5c"
    assert prepare.CATALOG_SHA=="1b388d317aeb1004c266eb65ff64a4864e7907412a2fbfb4667c492a871e8d8e"
    path=catalog_file(tmp_path,fixture_rows())
    output=tmp_path/"must-not-exist"
    argv=[str(SCRIPT),"--catalog",str(path),"--output",str(output)]
    monkeypatch.setattr(sys,"argv",argv)
    with pytest.raises(ValueError,match="fixed official public catalogue bytes mismatch"):
        prepare.main()
    assert not output.exists()
    monkeypatch.setattr(sys,"argv",argv+["--revision","unverified-latest"])
    with pytest.raises(SystemExit) as exc:
        prepare.main()
    assert exc.value.code==2 and not output.exists()
