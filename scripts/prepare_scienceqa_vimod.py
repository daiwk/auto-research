"""Import a public ScienceQA TRAIN sample for supervised loss, not evaluation.

Gold labels are written only to the train-only supervised manifest. Neither the
question field nor the inference backend prompt contains the answer. Raw API
responses and labels are never printed or retained as a separate data dump.
"""
import argparse
import json
from pathlib import Path
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    url = ("https://datasets-server.huggingface.co/rows?dataset=derek-thomas%2FScienceQA"
           "&config=default&split=train&offset=0&length=5")
    with urllib.request.urlopen(url, timeout=60) as response:
        rows = json.load(response)["rows"]
    row = next(item for item in rows if item["row"]["image"] is not None)
    value = row["row"]
    args.output_directory.mkdir(parents=True, exist_ok=True)
    image = args.output_directory / "train-image.jpg"
    urllib.request.urlretrieve(value["image"]["src"], image)
    options = "\n".join(f"{chr(65 + i)}. {choice}" for i, choice in enumerate(value["choices"]))
    train_record = {"id": f"scienceqa-train-row-{row['row_idx']}", "image": image.name,
                    "question": value["question"] + "\n" + options + "\nAnswer with one letter.",
                    "response": chr(65 + value["answer"]), "split": "train", "verified": True,
                    "verification": "official supervised training choice label",
                    "dataset_revision": "f18b0a70359ebfb41f658fd564208d0355b013f4"}
    manifest = args.output_directory / "train.jsonl"
    manifest.write_text(json.dumps(train_record) + "\n")
    print(json.dumps({"records": 1, "split": "train", "manifest": str(manifest)}))


if __name__ == "__main__":
    main()
