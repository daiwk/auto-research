import importlib.util
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_request_receipt_records_bootstrap_role_not_training_seed(tmp_path):
    module = load_script("run_jev_request_audit")
    source = tmp_path / "paired.jsonl"
    source.write_text(json.dumps({"year": 2019, "query_id": "q1", "scenario": "one",
                                  "before": {"A": .7, "B": .6}, "after": {"A": .6, "B": .7},
                                  "positive_labels": ["A"]}) + "\n")
    output = tmp_path / "result.json"
    module.main(["--predictions", str(source), "--resamples", "100", "--output", str(output)])
    report = json.loads(output.read_text())
    assert report["evaluation_protocol"]["seeds"] == [20260928]
    assert report["evaluation_protocol"]["seed_roles"] == [{"role": "query_cluster_bootstrap_rng", "value": 20260928}]
    assert report["evaluation_protocol"]["tier"] == "paired_prediction_protocol"
    assert report["evaluation_protocol"]["model_training_seeds"] == []
    assert report["provenance"]["dataset_fingerprint"] == f"sha256:{report['input_sha256']}"
    assert report["provenance"]["model_checkpoint_origin_verified"] is False


def test_committed_receipts_separate_seed_roles_and_keep_nonformal_claims():
    for folder, filename in (("2610.14112-regional-transfer", "public-predictions-cpu.json"),
                             ("2610.14631-request-audit", "protocol-validation.json")):
        report = json.loads((ROOT / "docs/system-one" / folder / "metrics" / filename).read_text())
        protocol = report["evaluation_protocol"]
        assert protocol["seeds"] and protocol["claim_policy"]
        assert protocol["model_training_seeds"] == []
        assert protocol["formal_comparison"] is False
        assert report["manifest_ref"]
        assert report["provenance"]["artifact_path"]
        assert report["provenance"]["dataset_fingerprint"]
        assert all(isinstance(seed, int) and seed != 42 for seed in protocol["seeds"])
        assert protocol["seed_roles"] and protocol["tier"]


def test_regional_generation_preserves_deterministic_role_and_external_origin(tmp_path, monkeypatch):
    from auto_research.system_one.regional_transfer import Prediction

    module = load_script("run_jev_regional_transfer")
    validation = tmp_path / "validation.parquet"
    test = tmp_path / "test.parquet"
    validation.write_bytes(b"external validation bytes")
    test.write_bytes(b"external test bytes")

    def read(path, *, split, language=None):
        return (Prediction("nusax_senti", split, "jav", str(path), "negative", "negative", (.8, .1, .1)),)

    monkeypatch.setattr(module, "read_parquet", read)
    output = tmp_path / "result.json"
    module.main(["--validation", str(validation), "--test", str(test), "--output", str(output)])
    report = json.loads(output.read_text())
    assert report["evaluation_protocol"]["seeds"] == []
    assert report["evaluation_protocol"]["seed_roles"] == [{"role": "local_deterministic_reanalysis", "value": None}]
    assert report["evaluation_protocol"]["tier"] == "public_prediction_reanalysis"
    assert report["evaluation_protocol"]["model_training_seeds"] == []
    assert report["upstream_revision"] is None
    assert report["provenance"]["dataset_fingerprint"].startswith("sha256:")


def test_committed_fingerprints_bind_real_sources():
    regional = json.loads((ROOT / "docs/system-one/2610.14112-regional-transfer/metrics/public-predictions-cpu.json").read_text())
    hashes = {name: record["sha256"] for name, record in sorted(regional["source_files"].items())}
    digest = hashlib.sha256(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert regional["provenance"]["dataset_fingerprint"] == f"sha256:{digest}"
    protocol = json.loads((ROOT / "docs/system-one/2610.14631-request-audit/metrics/protocol-validation.json").read_text())
    digest = hashlib.sha256((ROOT / protocol["provenance"]["fixture_source_path"]).read_bytes()).hexdigest()
    assert protocol["provenance"]["dataset_fingerprint"] == f"sha256:{digest}"


def test_metric_migration_is_idempotent_for_both_new_receipts():
    migration = load_script("migrate_metric_schema_v2")
    for folder, filename in (("2610.14112-regional-transfer", "public-predictions-cpu.json"),
                             ("2610.14631-request-audit", "protocol-validation.json")):
        path = ROOT / "docs/system-one" / folder / "metrics" / filename
        payload = json.loads(path.read_text())
        migrated = migration.migrate_payload(path, payload)
        assert migrated == payload
        assert json.dumps(migrated, ensure_ascii=False, indent=2) + "\n" == path.read_text()
