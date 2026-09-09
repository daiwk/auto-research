"""Real LM-built AtomRec memory on chronological Amazon Beauty candidates.

Uses a frozen Qwen checkpoint as both generator and dense text encoder instead
of the paper's GPT/SentenceT5 pair. Scores are a bounded candidate-ranking
experiment, not full-catalog retrieval or an original-benchmark reproduction.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import time

from .atomrec_semantic import SemanticAtomicMemory
from .coskill_checkpoint import MODEL, REVISION


def product_cases(directory, users=6):
    """Return private targets separately from pre-target public interactions."""
    histories = defaultdict(list)
    reviews = directory / "reviews_Beauty_5.json.gz"
    metadata_file = directory / "meta_Beauty.json.gz"
    with gzip.open(reviews, "rt") as stream:
        for line in stream:
            row = json.loads(line)
            histories[row["reviewerID"]].append((int(row["unixReviewTime"]), row["asin"]))
    sequences = []
    for user in sorted(histories):
        seen, sequence = set(), []
        for timestamp, item in sorted(histories[user]):
            if item not in seen:
                seen.add(item)
                sequence.append((timestamp, item))
        if len(sequence) >= 5 and sequence[-3][0] < sequence[-2][0] < sequence[-1][0]:
            sequences.append(sequence)
    counts = Counter(item for sequence in sequences for _, item in sequence[:-2])
    catalog = {item for item, _ in counts.most_common(2000)}
    metadata = {}
    with gzip.open(metadata_file, "rt") as stream:
        for line in stream:
            row = ast.literal_eval(line)
            if row.get("asin") in catalog:
                metadata[row["asin"]] = {"id": row["asin"], "title": str(row.get("title", ""))[:240],
                                         "description": str(row.get("description", ""))[:400],
                                         "categories": row.get("categories", [])}
    cases = []
    for sequence in sequences:
        if not all(item in metadata for _, item in sequence[-5:]):
            continue
        for split, offset in (("validation", -2), ("test", -1)):
            prefix = sequence[:offset]
            timestamp, target = sequence[offset]
            cases.append({"user": len(cases) // 2, "split": split, "timestamp": timestamp,
                          "history": prefix[-3:], "seen": [item for _, item in prefix], "target": target})
        if len(cases) == users * 2:
            break
    if len(cases) < users * 2:
        raise ValueError("insufficient strictly chronological users")
    hashes = {}
    for path in (reviews, metadata_file):
        with path.open("rb") as stream:
            hashes[path.name] = hashlib.file_digest(stream, "sha256").hexdigest()
    return cases, metadata, hashes


class FrozenMemoryCheckpoint:
    def __init__(self):
        import torch
        from huggingface_hub import snapshot_download
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        path = snapshot_download(MODEL, revision=REVISION, local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            path, local_files_only=True, torch_dtype=torch.bfloat16,
            attn_implementation="eager").cuda().eval().requires_grad_(False)
        self.calls = 0
        self.outputs = []

    def generate(self, prompt):
        self.calls += 1
        rendered = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(rendered, return_tensors="pt").to("cuda")
        with self.torch.inference_mode():
            ids = self.model.generate(**inputs, do_sample=False, max_new_tokens=512,
                                      pad_token_id=self.tokenizer.eos_token_id)
        output = self.tokenizer.decode(ids[0, inputs.input_ids.shape[-1]:], skip_special_tokens=True)
        self.outputs.append({"prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                             "purpose": prompt.split("\n", 1)[0], "output": output})
        return output

    def encode(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to("cuda")
        with self.torch.inference_mode():
            states = self.model.model(**inputs, use_cache=False).last_hidden_state
            vector = states.float().mean(dim=1)[0]
            return self.torch.nn.functional.normalize(vector, dim=0).cpu().numpy()


def rank(encode, evidence, candidates):
    """Frozen semantic ranker over only the supplied candidate set.

    This keeps the downstream scorer executable and total without parsing a
    generated permutation.  It never receives the held-out target label.
    """
    query = encode(json.dumps(evidence, sort_keys=True))
    vectors = [encode(json.dumps({key: value for key, value in row.items() if key != "id"},
                                 sort_keys=True)) for row in candidates]
    scores = [float(query @ vector) for vector in vectors]
    return [candidates[index]["id"] for index in sorted(
        range(len(candidates)), key=lambda index: (-scores[index], candidates[index]["id"]),
    )]


def run(directory, output, users=6, seeds=(42, 43, 44), split="both"):
    import math
    import torch

    cases, metadata, hashes = product_cases(directory, users)
    checkpoint = FrozenMemoryCheckpoint()
    records = []
    started = time.monotonic()
    for case in cases:
        if split != "both" and case["split"] != split:
            continue
        # Memory is rebuilt for each held-out timestamp. Future interactions and
        # the target ID are never provided to extraction, linking or synthesis.
        memory = SemanticAtomicMemory(checkpoint.generate, checkpoint.encode)
        history = [{"timestamp": stamp, "product": metadata[item]} for stamp, item in case["history"]]
        error, summary = None, None
        try:
            for index, interaction in enumerate(history):
                memory.ingest(f"interaction-{index}", str(case["user"]), interaction["timestamp"], interaction)
            summary = memory.synthesize("Predict the user's next beauty product from observed preferences.", case["timestamp"])
        except (ValueError, KeyError, TypeError) as exc:
            error = f"{type(exc).__name__}: {exc}"
        for seed in seeds:
            rng = random.Random(f"{seed}:{case['user']}:{case['split']}")
            pool = sorted(set(metadata) - set(case["seen"]) - {case["target"]})
            ids = rng.sample(pool, 9) + [case["target"]]
            rng.shuffle(ids)
            candidates = [metadata[item] for item in ids]
            for method, evidence in (("recent-history", history), ("atomrec", summary)):
                failure = error if method == "atomrec" else None
                ranking = []
                if failure is None:
                    try:
                        ranking = rank(checkpoint.encode, evidence, candidates)
                    except (ValueError, KeyError, TypeError) as exc:
                        failure = f"{type(exc).__name__}: {exc}"
                position = ranking.index(case["target"]) + 1 if ranking else 0
                row = {"user": case["user"], "split": case["split"], "seed": seed,
                       "method": method, "candidate_count": len(ids), "valid": failure is None,
                       "hit_at_3": int(0 < position <= 3),
                       "ndcg_at_3": 1 / math.log2(position + 1) if 0 < position <= 3 else 0,
                       "error": failure, "ranking": ranking,
                       "candidate_sha256": hashlib.sha256(json.dumps(ids).encode()).hexdigest(),
                       "memory_operations": memory.trace if method == "atomrec" else []}
                records.append(row)
                print(json.dumps({key: row[key] for key in ("user", "split", "seed", "method", "valid", "hit_at_3", "error")}), flush=True)
    result = {"checkpoint": {"id": MODEL, "revision": REVISION}, "dataset": "Amazon Beauty 2014 5-core",
              "dataset_sha256": hashes, "records": records, "generator_calls": checkpoint.calls,
              "generation_outputs": checkpoint.outputs,
              "accelerator": torch.cuda.get_device_name(), "elapsed_seconds": time.monotonic() - started,
              "scope": "bounded 10-candidate next-product experiment; frozen Qwen generator/mean-hidden-state encoder; not original benchmark",
              "selection": "fixed configuration; validation and test reported separately; no test tuning",
              "failure_policy": "malformed generations score zero; never use gold fallback"}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--users", type=int, default=6)
    parser.add_argument("--split", choices=("both", "validation", "test"), default="both")
    args = parser.parse_args()
    run(**vars(args))
