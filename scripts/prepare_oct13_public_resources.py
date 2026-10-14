#!/usr/bin/env python3
"""Download only fixed, authorized public resources, with size and SHA gates.

No checkpoint is committed. Each local mirror records upstream identity,
immutable revision and exact downloaded bytes; author checkpoints retain their
own formats rather than being relabelled as Transformers models.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.oct12_public_sources import sha256_file


RESOURCES = {
    "qwen-base": {
        "public_id": "Qwen/Qwen2.5-0.5B", "repo_type": "model",
        "revision": "060db6499f32faf8b98477b0a26969ef7d8b9987",
        "kind": "checkpoint",
        "files": ["config.json", "generation_config.json", "merges.txt", "model.safetensors",
                  "tokenizer.json", "tokenizer_config.json", "vocab.json"],
    },
    "smolwam": {
        "public_id": "timiiowolabi/SmolWAM", "repo_type": "model",
        "revision": "c269c6e3a9c113b2b04187daf977c09486e2eadc", "kind": "public-resource",
        "files": ["config.json", "model.safetensors", "text_cache.safetensors"],
    },
    "wan-vae": {
        "public_id": "Wan-AI/Wan2.1-T2V-1.3B", "repo_type": "model",
        "revision": "37ec512624d61f7aa208f7ea8140a131f93afc9a", "kind": "public-resource",
        "files": ["Wan2.1_VAE.pth"],
    },
    "lewam-toolhang": {
        "public_id": "LeWAM/lewam-toolhang", "repo_type": "model",
        "revision": "39512799122797828f13c29071d3d797852ce9b5", "kind": "public-resource",
        "files": ["lewam_best.pt", "lewam_config.json"],
    },
    "lewam-toolhang-data": {
        "public_id": "LeWAM/lewam-toolhang", "repo_type": "dataset",
        "revision": "465df45efe1b87aead4f423d3f8670833c5ddaf4", "kind": "public-resource",
        "files": ["toolhang.h5"],
    },
    "cosmos-teacher": {
        "public_id": "nvidia/Cosmos-Policy-LIBERO-Predict2-2B", "repo_type": "model",
        "revision": "cb689ec0e3347c13667d70a78a3447388f5c3bb8", "kind": "public-resource",
        "files": ["Cosmos-Policy-LIBERO-Predict2-2B.pt", "libero_t5_embeddings.pkl",
                  "libero_dataset_statistics.json"],
    },
    "cosmos-demo": {
        "public_id": "nvidia/LIBERO-Cosmos-Policy", "repo_type": "dataset",
        "revision": "b463cbd5d114909e4daea65eb03bed9787290042", "kind": "public-resource",
        "files": ["success_only/libero_goal_regen/put_the_cream_cheese_in_the_bowl_demo.hdf5",
                  "success_only/dataset_statistics.json"],
    },
}


def selected_files(info, names):
    by_name = {item.rfilename: item for item in info.siblings}
    missing = set(names) - set(by_name)
    if missing:
        raise ValueError(f"upstream revision misses requested files: {sorted(missing)}")
    selected = {name: by_name[name] for name in names}
    if any(item.size is None or item.size < 0 for item in selected.values()):
        raise ValueError("official upstream byte sizes are required before downloading")
    for name, item in selected.items():
        if item.size > 10_000_000 and (item.lfs is None or not item.lfs.sha256):
            raise ValueError(f"large public resource lacks upstream SHA256: {name}")
    return selected


def prepare(root: Path, names: list[str], *, maximum_bytes: int, download: bool):
    from huggingface_hub import HfApi, snapshot_download

    api = HfApi()
    plans = {}
    total = 0
    for name in names:
        resource = RESOURCES[name]
        info = api.repo_info(resource["public_id"], revision=resource["revision"],
                             repo_type=resource["repo_type"], files_metadata=True)
        if info.sha != resource["revision"]:
            raise ValueError("resolved upstream revision differs from the accepted fixed revision")
        files = selected_files(info, resource["files"])
        size = sum(item.size for item in files.values())
        total += size
        plans[name] = (resource, files, size)
    if total > maximum_bytes:
        raise ValueError(f"requested resources ({total} bytes) exceed remaining authorization budget")
    report = {"resources": {name: {"public_id": r[0]["public_id"], "revision": r[0]["revision"],
                                   "bytes": r[2]} for name, r in plans.items()},
              "total_bytes": total, "downloaded": download}
    if not download:
        return report
    root.mkdir(parents=True, exist_ok=True)
    for name, (resource, files, size) in plans.items():
        destination = root / name
        snapshot_download(resource["public_id"], revision=resource["revision"],
                          repo_type=resource["repo_type"], local_dir=destination,
                          allow_patterns=resource["files"], max_workers=2)
        hashes = {}
        for relative, info in files.items():
            path = destination / relative
            if path.stat().st_size != info.size:
                raise ValueError(f"downloaded byte count mismatch: {name}/{relative}")
            digest = sha256_file(path)
            if info.lfs is not None and digest != info.lfs.sha256:
                raise ValueError(f"upstream SHA256 mismatch: {name}/{relative}")
            hashes[relative] = digest
        provenance = {"kind": resource["kind"], "public_id": resource["public_id"],
                      "revision": resource["revision"], "repo_type": resource["repo_type"],
                      "files": hashes, "bytes": size,
                      "source": f"https://huggingface.co/{'datasets/' if resource['repo_type']=='dataset' else ''}"
                                f"{resource['public_id']}/tree/{resource['revision']}"}
        (destination / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    (root / "resource-budget.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resources", default=",".join(RESOURCES))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-bytes", type=int, default=19_000_000_000,
                        help="remaining download budget; reserve other data/assets from the 20GB grant")
    parser.add_argument("--download", action="store_true", help="without this flag only inspect official metadata")
    args = parser.parse_args()
    names = list(dict.fromkeys(args.resources.split(",")))
    if not names or set(names) - set(RESOURCES) or args.maximum_bytes < 1:
        parser.error("choose known resources and a positive remaining byte budget")
    print(json.dumps(prepare(args.output, names, maximum_bytes=args.maximum_bytes,
                             download=args.download), indent=2))


if __name__ == "__main__":
    main()
