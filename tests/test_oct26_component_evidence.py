from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/oct26-components"


def curator():
    return runpy.run_path(str(ROOT / "scripts/curate_oct26_components.py"))


def inputs():
    c = curator()
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    batch = next(b for b in json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())["batches"] if b["batch"] == c["BATCH"])
    spec = json.loads((AUDIT / "execution-spec.json").read_text())
    return c, scope, batch, spec


def test_fixed_scope_has_actual_evidence_and_no_full_capability_claims():
    c, scope, batch, _ = inputs()
    c["check"]()
    assert len(scope["papers"]) == 16
    assert scope["counts"]["components_accepted"] == scope["counts"]["gpu_validated_components"] == 8
    assert scope["counts"]["reference_only_high_cost_done"] == 8
    assert scope["counts"]["components_pending_verification"] == scope["counts"]["capability_reproductions_claimed"] == 0
    c["validate_scope"](scope, batch, c["catalogue"]())


@pytest.mark.parametrize("mutation", ["remove", "duplicate", "id", "date", "priority", "acceptance", "counts", "watermark", "alias"])
def test_scope_and_ledger_cannot_drift(mutation):
    c, scope, batch, _ = inputs()
    row = next(r for r in scope["papers"] if r["key"] in c["COMPONENT_KEYS"])
    if mutation == "remove":
        scope["papers"].pop()
    elif mutation == "duplicate":
        scope["papers"][-1] = deepcopy(scope["papers"][0])
    elif mutation == "id":
        row["id"] = "9999.99999"
    elif mutation == "date":
        row["original_published_at"] = "2026-10-26T00:00:00Z"
    elif mutation == "priority":
        row["priority"] = "P2"
    elif mutation == "acceptance":
        row["component_accepted"] = False
    elif mutation == "counts":
        scope["counts"]["components_accepted"] = 99
    elif mutation == "watermark":
        scope["review_watermark"]["after"] = "2026-10-26"
    else:
        batch["candidates"][0]["catalog_detail"] = "wrong/README.md"
    with pytest.raises(ValueError):
        c["validate_scope"](scope, batch, c["catalogue"]())


@pytest.mark.parametrize("mutation", ["device", "seed", "checks", "metrics", "commit", "source", "gate"])
def test_cuda_cannot_be_cpu_relabeling_or_missing_numerical_contract(mutation):
    c, _, _, spec = inputs()
    raw = {d: json.loads((AUDIT / f"raw-{d}.json").read_text()) for d in ("cpu", "cuda")}
    key = spec["components"][0]["key"]
    row = raw["cuda"]["components"][key]["per_seed"][0]
    if mutation == "device":
        row["execution_device"] = "cpu"
    elif mutation == "seed":
        row["seed"] = 0
    elif mutation == "checks":
        row["checks"] = {"unrelated": True}
    elif mutation == "metrics":
        row["metrics"]["fabricated"] = 1
    elif mutation == "commit":
        raw["cuda"]["code_commit"] = "0" * 40
    elif mutation == "source":
        raw["cuda"]["source_sha256"].pop(next(iter(raw["cuda"]["source_sha256"])))
    else:
        gate = spec["components"][0]["gates"][0]
        row["metrics"][gate["metric"]] = float("inf")
    with pytest.raises(ValueError):
        c["validate_raw"](raw, spec)


@pytest.mark.parametrize("field,value", [("id", "9999.99999"), ("decision", "full_reproduction_verified"),
    ("resolution", "full_reproduced"), ("component_evidence", "docs/gpu-validations/unrelated.json"),
    ("title", "unrelated title"), ("domain", "unrelated")])
def test_joint_scope_ledger_corruption_still_fails_canonical_binding(field, value):
    c, scope, batch, _ = inputs()
    for rows in (scope["papers"], batch["candidates"]):
        next(r for r in rows if r["key"] == "dt-jepa")[field] = value
    with pytest.raises(ValueError):
        c["validate_scope"](scope, batch, c["catalogue"]())


@pytest.mark.parametrize("field,value", [("promotion_eligible", True), ("evolve_integrated", True),
    ("diagnostic_only", False), ("automatic_retry", True), ("full_experiment_status", "reproduced"),
    ("local_command", "python fake.py")])
def test_catalog_cannot_promote_unmeasured_capability(field, value):
    c, _, _, spec = inputs()
    catalog = deepcopy(c["catalogue"]())
    catalog["hge"][field] = value
    with pytest.raises(ValueError):
        c["validate_catalog"](catalog, {r["key"]: r for r in spec["components"]})


def test_source_counts_are_announcements_not_fabricated_new_paper_counts():
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    pages = [p for p in coverage["retrieval_receipts"] if p["kind"] == "arxiv"]
    assert len(pages) == 8 and all(p["parse_complete"] and p["announced_on"] == "2026-10-26" for p in pages)
    assert sum(p["parsed_entries"] for p in pages) == 1180
    ids = {v.split("v")[0] for values in coverage["bulletin_ids_by_category"].values() for v in values}
    assert len(ids) == 835
    assert not coverage["all_sources_exhaustive"] and not coverage["full_bulletin_full_text_review_complete"]
    assert coverage["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}
    google = next(r for r in coverage["official_directory_deltas"] if r["organization"] == "Google")
    assert google["attempted_pages"] == google["retrieved_pages"] == 29
    assert google["unique_records"] == 430 and google["baseline_records"] == 428
    assert len(google["new_directory_urls"]) == 2


def test_all_documented_papers_have_reviewed_original_figures():
    c, scope, _, _ = inputs()
    catalog = c["catalogue"]()
    figures = json.loads((ROOT / "docs/paper-figures-manifest.json").read_text())
    for paper in scope["papers"]:
        page = "docs/" + catalog[paper["key"]]["detail_path"]
        text = (ROOT / page).read_text()
        assert "```bash\\n" not in text
        assert "<!-- paper-figure:start -->" in text and "<!-- paper-figure:end -->" in text
        assert "assets/paper-figure-01.png" in text and "### 原论文关键图" in text
        matches = [f for f in figures if f["page"] == page]
        assert len(matches) == 1 and matches[0]["visually_inspected"]
        assert hashlib.sha256((ROOT / matches[0]["asset"]).read_bytes()).hexdigest() == matches[0]["sha256"]


def test_duplicate_build_cannot_erase_accepted_delivery():
    c = curator()
    with pytest.raises(ValueError, match="batch already exists"):
        c["build_review"](Path("/nonexistent-input"))
