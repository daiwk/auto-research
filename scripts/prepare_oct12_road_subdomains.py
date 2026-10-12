"""Annotate verified GSM train-only holdouts with question-only subdomains.

This is a bounded routing diagnostic, not the paper's medical/math benchmark.
The original labels, partition and immutable revision are preserved.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from auto_research.public_holdout import validate_holdout


def domain(question: str) -> str:
    return 'monetary-arithmetic' if re.search(
        r'\$|\b(?:money|dollars?|costs?|prices?|earns?|paid|profit)\b', question, re.I
    ) else 'nonmonetary-arithmetic'


def prepare(source: Path, output: Path) -> dict:
    original = json.loads((source/'split.json').read_text())
    verify = validate_holdout(source/'split.json',source/'train.jsonl',source/'validation.jsonl',
                              dataset_revision=original['source_revision'])
    if not verify['verified'] or original['source_id']!='openai/grade-school-math':
        raise ValueError('verified official GSM training-only holdout required')
    if output.exists():
        raise FileExistsError('choose a fresh immutable output directory')
    transformed = {}
    counts = {}
    for split in ('train','validation'):
        # JSONL records are delimited by LF, not Unicode U+0085/U+2028/U+2029
        # which may legitimately occur inside JSON string values.
        rows = [json.loads(line) for line in (source/f'{split}.jsonl').read_text(
            encoding='utf-8').split('\n') if line.strip()]
        for row in rows:
            row['domain'] = domain(row['question'])
        counts[split] = dict(Counter(row['domain'] for row in rows))
        if len(counts[split])!=2:
            raise ValueError('both declared subdomains must occur; no arbitrary alternating labels')
        # Escape Unicode in transport only; json.loads recovers identical text.
        # This also makes the output compatible with existing text.splitlines
        # consumers without changing the shared checkpoint runtime.
        transformed[split] = ''.join(json.dumps(row,ensure_ascii=True)+'\n' for row in rows).encode('utf-8')
    manifest = dict(original)
    manifest['partition_sha256'] = {split:hashlib.sha256(raw).hexdigest() for split,raw in transformed.items()}
    manifest['original_partition_sha256'] = original['partition_sha256']
    manifest['domain_transformation'] = 'question-only monetary term regex; answer never used; original train-only partition unchanged'
    manifest['domain_counts'] = counts
    manifest['jsonl_serialization'] = 'LF-delimited UTF-8 JSON; ensure_ascii=True escapes preserve decoded Unicode strings'
    manifest['limitation'] = 'two arithmetic subdomains and general frozen teachers, not original specialized medical/math domains'
    output.mkdir(parents=True)
    for split,raw in transformed.items():
        (output/f'{split}.jsonl').write_bytes(raw)
    (output/'split.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    validate_holdout(output/'split.json',output/'train.jsonl',output/'validation.jsonl',
                     dataset_revision=original['source_revision'])
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=prepare(args.input,args.output)
    print(json.dumps(result['domain_counts']))


if __name__=='__main__':
    main()
