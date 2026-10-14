"""Download four fixed author-published prediction files (~140 KiB)."""
import argparse
import json
from pathlib import Path

from auto_research.system_one.regional_transfer import fetch_public_predictions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipts = fetch_public_predictions(args.output)
    (args.output / "sources.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(f"{len(receipts)} fixed public benchmark files; no model inference")


if __name__ == "__main__":
    main()
