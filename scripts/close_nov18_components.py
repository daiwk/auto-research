"""Bind fourteen bounded implementations to their prior closed review scope.

Append a delivery observation, never rewrite review decisions or advance scan
coverage. Full experiments remain unexecuted; L0/L1 is not capability evidence.
"""
from __future__ import annotations

import hashlib
import json
import re

from PIL import Image

from curate_nov18_evidence import validate_admission
from english_learning_sources import deep_dive_units, question_units
from oct18_frozen_sources import verify_sources
from run_nov18_components import AUDIT, BATCH, COMPONENTS, CUDA_KEYS, ROOT, load, source_hashes, tier


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _reviewed_english(payload, units):
    entries = payload["units"]
    if set(entries) != set(units):
        raise ValueError("reviewed English learning scope differs from actual authored units")
    for key, unit in units.items():
        entry = entries[key]
        if (entry.get("reviewed") is not True or entry.get("source_sha256") != unit.source_sha256
                or set(entry.get("fields", {})) != set(unit.fields)
                or any(not isinstance(text, str) or not text.strip() or re.search(r"[\u3400-\u9fff]", text)
                       for text in entry["fields"].values())):
            raise ValueError("missing, stale or unreviewed English learning unit: " + key)


def learning_counts():
    expected = {f"{domain}:{key}" for key, (domain, _) in COMPONENTS.items()}
    questions, english, proposals = {}, {}, []
    for name in ("root", "data", "agent", "eval"):
        bundle = load(ROOT / f"docs/learning/questions/nov18-{name}.json")["papers"]
        if set(questions) & set(bundle):
            raise ValueError("duplicate learning papers")
        questions.update({identity: row["questions"] for identity, row in bundle.items()})
        overlay = load(ROOT / f"docs/en/learning/translations/qa-nov18-{name}.json")["units"]
        if set(english) & set(overlay):
            raise ValueError("duplicate English questions")
        english.update(overlay)
        proposals.extend(load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"])
    if set(questions) != expected or {row["paper"] for row in proposals} != expected or len(proposals) != len(expected):
        raise ValueError("fourteen-paper learning scope missing or duplicated")
    if any(len(rows) != 4 or {row["level"] for row in rows} != {
            "basics", "mechanism", "comparison", "implementation"} for rows in questions.values()):
        raise ValueError("actual four-level authored questions incomplete")
    _reviewed_english({"units": english}, question_units(questions))
    dive_units = {}
    for proposal in proposals:
        theme, topic = proposal["target_card"].split("/", 1)
        membership = load(ROOT / f"docs/learning/topics/{theme}.json")
        members = next(row["papers"] for row in membership["topics"] if row["id"] == topic)
        record = load(ROOT / f"docs/learning/deep-dives/{theme}.json")["topics"][topic]
        update = proposal["update"] | {"source_revisions": {
            identity: proposal["source_revisions"][identity] for identity in proposal["update"]["papers"]}}
        if (proposal["paper"] not in members or proposal["paper"] not in record["reviewed_papers"]
                or {"paper": proposal["paper"], **proposal["comparison"]} not in record["comparisons"]
                or proposal["analysis"] not in record["analysis"] or proposal["question"] not in record["questions"]
                or update not in record["updates"]):
            raise ValueError("authored comparison was not actually integrated: " + proposal["paper"])
        card = proposal["target_card"]
        keys = [f"dive/{card}/comparison/{proposal['paper']}",
                f"dive/{card}/analysis/{record['analysis'].index(proposal['analysis'])}",
                f"dive/{card}/question/{proposal['question']['id']}",
                f"dive/{card}/update/{update['date']}/{record['updates'].index(update)}"]
        actual = deep_dive_units({card: record})
        dive_units.update({key: actual[key] for key in keys})
    _reviewed_english(load(ROOT / "docs/en/learning/translations/dive-nov18-components.json"), dive_units)
    return {"authored_four_level_questions": sum(map(len, questions.values())),
            "same_topic_deep_dive_updates": len(proposals)}


def main():
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("execution files changed after actual run")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device in ("cpu", "cuda"):
        validate_admission(load(AUDIT / f"raw-{device}.json"), frozen)
    intake = load(AUDIT / "intake-scope.json")
    if set(intake["accepted_papers"]) != {f"{domain}:{key}" for key, (domain, _) in COMPONENTS.items()}:
        raise ValueError("fixed fourteen-paper scope differs")
    actual_learning = learning_counts()
    figures = load(ROOT / "docs/paper-figures-manifest.json")
    papers = []
    for key, (domain, module) in COMPONENTS.items():
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json")
        page = ROOT / "docs" / spec["detail_path"]
        if (not page.is_file() or not page.with_name("README-en.md").is_file()
                or spec["evaluation_tier"] != tier(key) or not spec["review_done"]
                or spec.get("automatic_implementation_queue") is not False
                or spec.get("promotion_eligible") is not False or spec.get("evolve_integrated") is not False):
            raise ValueError("incomplete or overstated implementation: " + key)
        for device in (("cpu", "cuda") if key in CUDA_KEYS else ("cpu",)):
            if not (page.parent / f"metrics/component-{device}-seeds42-44.json").is_file():
                raise ValueError("actual per-paper evidence missing: " + key)
        if key in CUDA_KEYS and (spec.get("gpu_validation_passed") is not True
                                 or not (ROOT / spec["gpu_validation_artifact"]).is_file()):
            raise ValueError("GPU acceptance missing: " + key)
        aid = re.search(r"\d{4}\.\d{4,5}", spec["paper_url"]).group()
        asset = page.parent / "assets/paper-figure-01.png"
        provenance = load(asset.with_name("provenance.json"))
        if "figures" in provenance:
            matches = [row for row in provenance["figures"] if row.get("file") == asset.name]
            if len(matches) != 1:
                raise ValueError("original figure provenance is ambiguous: " + key)
            provenance = matches[0]
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()
        if provenance.get("asset_sha256") != digest:
            raise ValueError("original figure provenance changed: " + key)
        width, height = Image.open(asset).size
        figure = {"page": page.relative_to(ROOT).as_posix(), "paper_url": spec["paper_url"],
                  "arxiv_id": aid, "figure": (f"Figure {provenance['figure']}" if type(provenance.get("figure")) is int
                                               else provenance.get("figure", "Original figure")),
                  "original_caption": provenance.get("caption", ""),
                  "source_url": provenance["source_url"], "extraction": "original_source_reviewed",
                  "asset": asset.relative_to(ROOT).as_posix(), "width": width, "height": height,
                  "score": 0, "error": "", "asset_sha256": digest}
        figures = [old for old in figures if old["page"] != figure["page"]] + [figure]
        papers.append(spec | {"id": aid, "status": "implemented", "resolution": "bounded_component_accepted",
                             "reason": spec["summary"], "component_implemented": True,
                             "full_capability_reproduced": False, "doc": spec["detail_path"],
                             "execution_module": "src/auto_research/" + module,
                             "review_scope": "implementation_delivery_of_previously_closed_review"})
    scope = intake | {"batch": BATCH, "selected_scope_complete": True, "delivery_status": "fixed_scope_complete",
                      "scan_coverage_changed": False, "full_capability_reproductions": 0,
                      "counts": {"low_cost_components": len(COMPONENTS), "cuda_components": len(CUDA_KEYS),
                                 **actual_learning, "full_capability_reproductions": 0},
                      "papers": papers}
    write(AUDIT / "task-scope.json", scope)
    write(ROOT / "docs/paper-figures-manifest.json", figures)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [row for row in ledger["batches"] if row.get("batch") != BATCH]
    ledger["batches"].append({key: value for key, value in scope.items() if key != "papers"} | {"candidates": papers})
    write(ledger_path, ledger)
    print(json.dumps(scope["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
