"""Read-only curation of frozen three-seed ReplaySSM CUDA mechanism evidence."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
from statistics import mean, stdev
import tarfile

COMMIT = "6aabe57a97ec3a586aac7aeea66128750f9441da"
ARCHIVE_SHA256 = "6d791e198e741301ac5d77decc64c0b80a1785cd3680c1a8de3c7b218ff33be3"
SOURCE_HASHES = {
    "scripts/run_replayssm.py": "1e7bd3435279d597e12808cfbb6872d53dea006d82ec0c03f94452a19de9858a",
    "src/auto_research/foundation_models/replayssm.py": "5b03cb60b19bff0d8a324bc3cadf6a3ecb81a61e1b52da949886ba9fdfb93ab7",
    "src/auto_research/oct12_public_sources.py": "4e1150cbe4ea975819c244267180f853c83c4ad4c2c27f9e0ce95cc16793e093",
}
UPSTREAM = "5d3ea597d479ef0c8e9e2eb2845a2adfdb9a8b44"
ORIGINAL_JIT = "7f60e87d974bfea4b5095980599043d8a7a615db4ba1b5fdbf7a0c1d0bfc6ab1"
COMPILED_JIT = "9add48ef24fa9df25a71e5f8a05fc0dac46b35c6b5efdc73012cbeeeae1c8174"
GDN_FILE = "80311d6654584c633db01f76e3be5bc189fbdfab031c1bc0711757e1cd09eec3"


def curate(raw_dir: Path, source_archive: Path) -> dict:
    assert sha256(source_archive.read_bytes()).hexdigest() == ARCHIVE_SHA256
    with tarfile.open(source_archive) as archive:
        for name, expected in SOURCE_HASHES.items():
            source = archive.extractfile(name)
            assert source is not None and sha256(source.read()).hexdigest() == expected
    rows, commands, reports, files = [], [], [], set()
    for seed in (42, 43, 44):
        stem = f"replayssm-seed{seed}"
        names = [stem + suffix for suffix in (".json", ".status.json", ".stdout.log", ".stderr.log")]
        files.update(names)
        report = json.loads((raw_dir / names[0]).read_text())
        status = json.loads((raw_dir / names[1]).read_text())
        command = status["command"]
        assert status["commit"] == COMMIT and status["actual_source_files_sha256"] == SOURCE_HASHES
        assert status["returncode"] == 0 and status["output_exists"] and status["failure"] is None
        assert status["accelerator"] == "NVIDIA A100-SXM4-80GB"
        assert command[1] == "scripts/run_replayssm.py"
        assert int(command[command.index("--seed") + 1]) == report["seed"] == seed
        assert int(command[command.index("--steps") + 1]) == 48
        assert report["diagnostic_only"] and not report["promotion_eligible"]
        assert report["dataset_revision"] == "replayssm-random-input-protocol-v2-gdn-rollback"
        author = report["author_triton"]
        assert author["upstream_revision"] == UPSTREAM and author["steps"] == 48
        assert author["accelerator"] == status["accelerator"]
        assert author["storage_format"] == "dequantized FP32" and not author["native_bandwidth_speedup_claim"]
        compatibility = author["jit_source_compatibility"]
        assert compatibility["original_jit_source_sha256"] == ORIGINAL_JIT
        assert compatibility["compiled_jit_source_sha256"] == COMPILED_JIT
        assert compatibility["original_author_file_sha256"] == GDN_FILE
        assert compatibility["function"] == "_gdn_unf_vf_step_kernel"
        assert compatibility["source_ranges_relative_to_jit_function"] == [{
            "line": 122, "column": 7, "end_line": 122, "end_column": 51,
            "operator": "and", "operands": 3}]
        assert compatibility["associative_boolean_ast_equivalent"]
        assert not compatibility["author_file_modified"] and not compatibility["native_serving_claim"]
        assert author["upstream_source_files_sha256"]["gdn_replay_unf_vf.py"] == GDN_FILE
        for name in ("reference", "reference_gdn"):
            reference = report[name]
            assert reference["accepted_tokens"] == 12 and not reference["native_bandwidth_speedup_claim"]
            assert 0 <= reference["max_output_error"] <= 5e-6
        gdn = report["reference_gdn"]
        assert gdn["acceptance_counts"] == [0, 1, 2, 3, 0, 1, 2, 3]
        assert gdn["checkpoint_refreshes"] == [3, 3]
        assert gdn["high_anchor_read_precision_max_difference"] == 0
        assert gdn["max_committed_state_error"] <= 5e-6
        metrics = {"reference_max_output_error": report["reference"]["max_output_error"],
                   **{"gdn_" + key: gdn[key] for key in (
                       "max_output_error", "max_committed_state_error",
                       "read_precision_output_max_difference", "high_anchor_read_precision_max_difference")}}
        for architecture in ("mamba2", "gdn"):
            assert author["metrics"][architecture + "/independent_read_cast_passed"]
            for mode in ("s32_rs", "tp8_hi32", "tp4_hi16_sr", "f4_sr_rs"):
                for metric in ("output_rmse", "anchor_rmse"):
                    key = f"{architecture}/{mode}/{metric}"
                    value = author["metrics"][key]
                    assert math.isfinite(value) and value >= 0
                    if mode == "s32_rs" or (mode == "tp8_hi32" and metric == "anchor_rmse"):
                        assert value == 0
                    metrics[key] = value
        rows.append({"seed": seed, **metrics, "elapsed_seconds": status["elapsed_seconds"]})
        sanitized = list(command)
        sanitized[0] = "python"
        sanitized[sanitized.index("--upstream") + 1] = "PINNED_PUBLIC_AUTHOR_SOURCE"
        sanitized[sanitized.index("--output") + 1] = "RAW_RESULT"
        commands.append(sanitized)
        reports.append(report)
    assert set(path.name for path in raw_dir.iterdir()) == files
    for report in reports[1:]:
        assert report["author_triton"]["jit_source_compatibility"] == reports[0]["author_triton"]["jit_source_compatibility"]
        assert report["author_triton"]["upstream_source_files_sha256"] == reports[0]["author_triton"]["upstream_source_files_sha256"]
    return {"code_commit": COMMIT, "seeds": [42, 43, 44], "per_seed": rows,
            "aggregate": {key: {"mean": mean(row[key] for row in rows),
                                "sample_std": stdev(row[key] for row in rows)}
                          for key in rows[0] if key != "seed"},
            "commands": commands, "finished_at": max(json.loads(
                (raw_dir / f"replayssm-seed{seed}.status.json").read_text())["finished_at"] for seed in (42, 43, 44)),
            "jit_source_compatibility": reports[0]["author_triton"]["jit_source_compatibility"],
            "upstream_source_files_sha256": reports[0]["author_triton"]["upstream_source_files_sha256"],
            "actual_source_files_sha256": SOURCE_HASHES, "source_archive_sha256": ARCHIVE_SHA256,
            "raw_files_sha256": {name: sha256((raw_dir / name).read_bytes()).hexdigest() for name in sorted(files)}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(curate(args.raw_dir, args.source_archive), indent=2))
