from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts import curate_oct29_components as c
from scripts.run_oct29_components import execution_spec

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/oct29-components"


def raw_results():
    return {d: json.loads((AUDIT / f"raw-{d}.json").read_text()) for d in ("cpu", "cuda")}


def test_fixed_scope_is_actually_executed_but_not_capability_or_evolve():
    c.check()
    raw = raw_results()
    assert len(raw["cpu"]["components"]) == 8
    assert len(raw["cuda"]["components"]) == 4
    assert raw["cuda"]["accelerator"].startswith("NVIDIA A100")
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    assert scope["counts"]["capability_reproductions_claimed"] == 0
    assert scope["counts"]["components_pending_verification"] == 0
    assert scope["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}
    reference = next(r for r in scope["papers"] if r["key"] == "pailitao-mmsearch2")
    assert reference["component_evidence"] is None and not reference["component_implemented"]
    assert not (ROOT / "docs" / Path(reference["detail_path"]).parent / "metrics").exists()


@pytest.mark.parametrize("fault", ["device", "seed", "check", "metric", "sources", "commit", "gate", "subset"])
def test_actual_cuda_contract_is_fail_closed(fault):
    raw = deepcopy(raw_results())
    first = raw["cuda"]["components"]["rescom"]["per_seed"][0]
    if fault == "device":
        first["execution_device"] = "cpu"
    elif fault == "seed":
        first["seed"] = 0
    elif fault == "check":
        first["checks"].pop(next(iter(first["checks"])))
    elif fault == "metric":
        first["metrics"]["unknown"] = 1
    elif fault == "sources":
        raw["cuda"]["source_sha256"].pop(next(iter(raw["cuda"]["source_sha256"])))
    elif fault == "commit":
        raw["cuda"]["code_commit"] = "0" * 40
    elif fault == "gate":
        first["metrics"]["heldout_error_after"] = first["metrics"]["heldout_error_before"] + 1
    else:
        raw["cuda"]["components"].pop("kl-mopd")
    with pytest.raises(ValueError):
        c.validate_raw(raw, execution_spec())


def test_learning_questions_and_recent_source_dates_are_explicit():
    bank = {}
    for path in (ROOT / "docs/learning/questions").glob("oct29-*.json"):
        bank.update(json.loads(path.read_text())["papers"])
    assert len(bank) == 9
    assert all({q["level"] for q in p["questions"]} == {"basics", "mechanism", "comparison", "implementation"}
               for p in bank.values())
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    assert coverage["actual_announced_on"] == "2026-10-28"
    assert len(coverage["recent_ids_by_category_and_date"]) == 8
    assert all("2026-10-27" in value for value in coverage["recent_ids_by_category_and_date"].values())
    assert coverage["full_bulletin_full_text_review_complete"] is False
    assert coverage["all_sources_exhaustive"] is False


@pytest.mark.parametrize("fault", ["identity", "acceptance", "resolution", "counts", "evidence", "watermark", "reason"])
def test_joint_scope_ledger_edit_cannot_forge_acceptance(fault):
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    batch = next(b for b in json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())["batches"] if b["batch"] == c.BATCH)
    target = "pailitao-mmsearch2" if fault == "reason" else "rescom"
    index = next(i for i, r in enumerate(scope["papers"]) if r["key"] == target)
    for item in (scope["papers"][index], batch["candidates"][index]):
        if fault == "identity":
            item["id"] = "9999.99999"
        elif fault == "acceptance":
            item["component_accepted"] = False
        elif fault == "resolution":
            item["resolution"] = "full_pipeline"
        elif fault == "evidence":
            item["component_evidence"] = "docs/fake.json"
        elif fault == "reason":
            item["reason"] = ""
    for item in (scope, batch):
        if fault == "counts":
            item["counts"]["gpu_validated_components"] = 9
        elif fault == "watermark":
            item["review_watermark"]["after"] = "2026-10-29"
    with pytest.raises(ValueError):
        c.validate_scope(scope, batch, c.catalogue())
