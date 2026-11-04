"""Execute seven fixed, source-bound L1 components, never full experiments."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402

RUNNER = 'scripts/run_nov04_components.py'
PREFLIGHT = 'docs/research-audits/nov04-components/preflight.json'
SEEDS = [42, 43, 44]
COMPONENTS = {
    'wesearch': ('reproductions/wesearch_components.py', 'cpu'),
    'strategist': ('agent_research/strategist.py', 'cpu'),
    'agentheal': ('agent_research/agentheal.py', 'cpu'),
    'proland': ('foundation_models/proland.py', 'cuda'),
    'gavagai': ('foundation_models/gavagai.py', 'cuda'),
    'specopd': ('post_training/specopd.py', 'cuda'),
    'rlid': ('post_training/rlid.py', 'cuda'),
}


def sources():
    return [RUNNER, PREFLIGHT, 'scripts/oct18_frozen_sources.py',
            *sorted('src/auto_research/' + source for source, _ in COMPONENTS.values())]


def validate_diagnostic(row, seed):
    """A checked diagnostic is still NOT a benchmark or capability result."""
    if row.get('seed') != seed or not row.get('checks') or any(
        value is not True for value in row['checks'].values()
    ):
        raise ValueError('all explicit component checks and the actual seed are required')

    def finite(value):
        if isinstance(value, dict):
            return all(finite(v) for v in value.values())
        if isinstance(value, list):
            return all(finite(v) for v in value)
        if type(value) is float:
            return math.isfinite(value)
        return value is None or type(value) in (str, int, bool)

    if not finite(row):
        raise ValueError('diagnostic values must be finite JSON scalars')


def load_component(key):
    source = ROOT / 'src/auto_research' / COMPONENTS[key][0]
    name = '_nov04_' + key
    spec = importlib.util.spec_from_file_location(name, source)
    if spec is None or spec.loader is None:
        raise ValueError('frozen source unavailable')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--device', choices=('cpu', 'cuda'), default='cpu')
    parser.add_argument('--source-commit')
    parser.add_argument('--frozen-proof', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('immutable new output path required')
    commit = args.source_commit or subprocess.check_output(
        ['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    hashes = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources()}
    proof = json.loads(args.frozen_proof.read_text()) if args.frozen_proof else capture_sources(ROOT,commit,sources())
    verify_sources(ROOT,commit,hashes,proof)
    import torch
    torch.set_num_threads(1)
    if args.device == 'cuda' and not torch.cuda.is_available():
        parser.error('actual CUDA required; CPU fallback forbidden')
    accelerator = torch.cuda.get_device_name(0) if args.device == 'cuda' else 'CPU'
    if args.device == 'cuda' and not any(k in accelerator for k in ('A100','A30')):
        parser.error('actual NVIDIA A100/A30 required')
    started, results = time.monotonic(), {}
    for key, (_, required) in COMPONENTS.items():
        if args.device == 'cuda' and required != 'cuda':
            continue
        module = load_component(key)
        if bool(module.REQUIRES_GPU_VALIDATION) != (required == 'cuda'):
            raise ValueError('source device contract differs from fixed preflight')
        rows = []
        for seed in SEEDS:
            row = module.diagnostic(seed, device=args.device)
            if args.device == 'cuda':
                torch.cuda.synchronize()
            validate_diagnostic(row,seed)
            rows.append(row | {'execution_device':args.device,'execution_accelerator':accelerator})
        results[key] = {'per_seed': rows}
    output = {'schema_version':2,'code_commit':commit,'source_sha256':hashes,
              'device':args.device,'accelerator':accelerator,'seeds':SEEDS,'components':results,
              'elapsed_seconds':time.monotonic()-started,'diagnostic_only':True,
              'evaluation_tier':'l1_mechanism','formal_comparison':False,
              'promotion_eligible':False,'evolve_integrated':False,
              'pretrained_model_calls':0,'full_experiments_executed':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(output,handle,ensure_ascii=False,indent=2,allow_nan=False)
        handle.write('\n')
    print(json.dumps({'device':args.device,'components':list(results),'elapsed_seconds':output['elapsed_seconds']}))


if __name__ == '__main__':
    main()
