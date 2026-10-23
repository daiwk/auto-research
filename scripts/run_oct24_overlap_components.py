"""Frozen-source four-component overlap diagnostics, with no model/data downloads."""
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

RUNNER = 'scripts/run_oct24_overlap_components.py'
MODULES = {
    'physical-engineering-exam': 'src/auto_research/agent_research/physical_engineering_exam.py',
    'ttr-compressor': 'src/auto_research/foundation_models/ttr_compressor.py',
    'userarena-optd': 'src/auto_research/post_training/userarena_optd.py',
    'moer': 'src/auto_research/post_training/moer.py',
}
CUDA_KEYS = {'ttr-compressor', 'userarena-optd', 'moer'}
SOURCES = [RUNNER, 'scripts/oct18_frozen_sources.py', *MODULES.values()]
SEEDS = [42, 43, 44]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--device', choices=('cpu', 'cuda'), default='cpu')
    parser.add_argument('--source-commit')
    parser.add_argument('--frozen-proof', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('new immutable output required')
    commit = args.source_commit or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    hashes = {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in SOURCES}
    proof = json.loads(args.frozen_proof.read_text()) if args.frozen_proof else capture_sources(ROOT, commit, SOURCES)
    verify_sources(ROOT, commit, hashes, proof)
    import torch

    torch.set_num_threads(1)
    if args.device == 'cuda' and not torch.cuda.is_available():
        parser.error('requested CUDA unavailable; no CPU fallback')
    accelerator = torch.cuda.get_device_name(0) if args.device == 'cuda' else 'CPU'
    if args.device == 'cuda' and not any(n in accelerator for n in ('A100', 'A30')):
        parser.error('real NVIDIA A100/A30 required')
    started = time.monotonic()
    components = {}
    for key, path in MODULES.items():
        if args.device == 'cuda' and key not in CUDA_KEYS:
            continue
        module = importlib.import_module(path.removeprefix('src/').removesuffix('.py').replace('/', '.'))
        rows = [module.diagnostic(seed, device=args.device) if key in CUDA_KEYS else module.diagnostic(seed) for seed in SEEDS]
        for expected_seed, row in zip(SEEDS, rows):
            if row.get('seed') != expected_seed or not row.get('checks') or not all(v is True for v in row['checks'].values()):
                raise RuntimeError(f'{key}: missing/failed defining contract')
            if not row.get('metrics') or not all(type(v) in (float, int, bool) and math.isfinite(v) for v in row['metrics'].values()):
                raise RuntimeError(f'{key}: nonfinite/nonscalar metrics')
            row['execution_device'] = args.device
            row['execution_accelerator'] = accelerator
        components[key] = {'per_seed': rows}
    if args.device == 'cuda':
        torch.cuda.synchronize()
    result = {'schema_version': 2, 'device': args.device, 'accelerator': accelerator,
        'seeds': SEEDS, 'code_commit': commit, 'source_sha256': hashes, 'components': components,
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
