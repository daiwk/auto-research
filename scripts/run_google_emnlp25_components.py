"""Execute only the fixed, frozen Google EMNLP historical component scope."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
sys.path.insert(0, str(ROOT/'scripts'))
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402

RUNNER = 'scripts/run_google_emnlp25_components.py'
SPEC_PATH = 'docs/research-audits/google-emnlp25-closure/execution-spec.json'
HELPER = 'scripts/oct18_frozen_sources.py'
SEEDS = [42, 43, 44]


def execution_spec():
    spec = json.loads((ROOT/SPEC_PATH).read_text())
    if spec['schema_version'] != 1 or spec['seeds'] != SEEDS or not spec['components']:
        raise ValueError('nonempty fixed three-seed execution spec required')
    if len({r['key'] for r in spec['components']}) != len(spec['components']):
        raise ValueError('duplicate component key')
    for row in spec['components']:
        path = Path(row['source'])
        if (path.is_absolute() or '..' in path.parts or not row['source'].startswith('src/auto_research/')
                or path.suffix != '.py' or row['device'] not in ('cpu', 'cuda')
                or not row['checks'] or not row['metrics']):
            raise ValueError('bounded relative module path, device and defining schema required')
    return spec


def sources(spec):
    return [RUNNER, SPEC_PATH, HELPER, *sorted({r['source'] for r in spec['components']})]


def validate_row(row, expected, seed):
    if row.get('seed') != seed or set(row.get('checks', {})) != set(expected['checks']):
        raise ValueError(f"{expected['key']}: exact seed and defining checks required")
    if not all(v is True for v in row['checks'].values()):
        raise ValueError(f"{expected['key']}: failed defining check")
    metrics = row.get('metrics', {})
    if set(metrics) != set(expected['metrics']) or not all(type(v) in (float, int, bool) and math.isfinite(v) for v in metrics.values()):
        raise ValueError(f"{expected['key']}: exact finite scalar metric schema required")
    comparisons = {'eq': lambda a, b: a == b, 'lt': lambda a, b: a < b,
                   'le': lambda a, b: a <= b, 'gt': lambda a, b: a > b, 'ge': lambda a, b: a >= b}
    for gate in expected['gates']:
        bound = metrics[gate['other_metric']] if 'other_metric' in gate else gate['value']
        if not comparisons[gate['op']](metrics[gate['metric']], bound):
            raise ValueError(f"{expected['key']}: numerical gate failed: {gate['metric']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--device', choices=('cpu', 'cuda'), default='cpu')
    parser.add_argument('--source-commit')
    parser.add_argument('--frozen-proof', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('new immutable output required')
    spec = execution_spec()
    paths = sources(spec)
    commit = args.source_commit or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    hashes = {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths}
    proof = json.loads(args.frozen_proof.read_text()) if args.frozen_proof else capture_sources(ROOT, commit, paths)
    verify_sources(ROOT, commit, hashes, proof)
    import torch

    torch.set_num_threads(1)
    if args.device == 'cuda' and not torch.cuda.is_available():
        parser.error('requested CUDA unavailable; CPU fallback forbidden')
    accelerator = torch.cuda.get_device_name(0) if args.device == 'cuda' else 'CPU'
    if args.device == 'cuda' and not any(name in accelerator for name in ('A100', 'A30')):
        parser.error('real NVIDIA A100/A30 required')
    started = time.monotonic()
    components = {}
    for expected in spec['components']:
        if args.device == 'cuda' and expected['device'] != 'cuda':
            continue
        module = importlib.import_module(expected['source'].removeprefix('src/').removesuffix('.py').replace('/', '.'))
        rows = []
        for seed in SEEDS:
            row = module.diagnostic(seed, device=args.device)
            validate_row(row, expected, seed)
            row.update(execution_device=args.device, execution_accelerator=accelerator)
            rows.append(row)
        components[expected['key']] = {'per_seed': rows}
    if args.device == 'cuda':
        torch.cuda.synchronize()
    result = {'schema_version': 2, 'device': args.device, 'accelerator': accelerator, 'seeds': SEEDS,
        'code_commit': commit, 'source_sha256': hashes, 'components': components,
        'elapsed_seconds': time.monotonic()-started, 'evaluation_tier': 'l1_mechanism',
        'diagnostic_only': True, 'formal_comparison': False, 'promotion_eligible': False,
        'evolve_integrated': False, 'pretrained_model_calls': 0, 'full_experiments_executed': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'device': args.device, 'components': list(components), 'elapsed_seconds': result['elapsed_seconds']}))


if __name__ == '__main__':
    main()
