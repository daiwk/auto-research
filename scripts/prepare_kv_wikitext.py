"""Prepare only the public WikiText test corpus for offline GPU evaluation."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    from datasets import load_dataset
    from huggingface_hub import HfApi

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--parquet", type=Path, help="Fixed-revision public test parquet, downloaded independently")
    args = parser.parse_args()
    dataset_id = "Salesforce/wikitext"
    if args.parquet:
        import pyarrow.parquet as pq

        revision = "b08601e04326c79dfdd32d625aee71d232d685c3"
        expected = "5f1bea067869d04849c0f975a2b29c4ff47d867f484f5010ea5e861eab246d91"
        if hashlib.sha256(args.parquet.read_bytes()).hexdigest() != expected:
            raise ValueError("WikiText fixed-revision parquet checksum mismatch")
        text = "\n".join(pq.read_table(args.parquet)["text"].to_pylist())
    else:
        revision = HfApi().dataset_info(dataset_id, timeout=30).sha
        dataset = load_dataset(dataset_id, "wikitext-2-raw-v1", split="test", revision=revision)
        text = "\n".join(row["text"] for row in dataset)
    payload = {"id": dataset_id, "config": "wikitext-2-raw-v1", "split": "test",
               "revision": revision, "text": text,
               "sha256": hashlib.sha256(text.encode()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload) + "\n")
    print(json.dumps({key: value for key, value in payload.items() if key != "text"}))


if __name__ == "__main__":
    main()
