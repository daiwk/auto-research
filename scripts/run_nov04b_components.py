"""Execute the fixed November4 bulletin's small L1 components; no full runs."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_nov04_components import validate_diagnostic  # noqa: E402

RUNNER = 'scripts/run_nov04b_components.py'
PREFLIGHT = 'docs/research-audits/nov04-bulletin-components/preflight.json'
SEEDS = [42,43,44]
COMPONENTS = {
    'reusegr': ('reproductions/reusegr_components.py','cpu'),
    'spade-local-search': ('reproductions/spade_components.py','cpu'),
    'onetrans-gsr': ('reproductions/onetrans_gsr_components.py','cpu'),
    'meta-square': ('agent_research/meta_square.py','cpu'),
    'continual-autoresearch': ('agent_research/continual_autoresearch.py','cpu'),
    'runtime-tickets': ('agent_research/runtime_tickets.py','cpu'),
    'semantic-block-sparse-attention': ('foundation_models/semantic_block_sparse_attention.py','cuda'),
    'anchor-kv': ('foundation_models/anchor_kv.py','cuda'),
    'dars': ('post_training/dars.py','cuda'),
    'p2-mopd': ('post_training/p2_mopd.py','cuda'),
    'shuffled-opsd': ('post_training/shuffled_opsd.py','cuda'),
    'targeted-guidance': ('post_training/targeted_guidance.py','cuda'),
}


def sources():
    return [RUNNER,PREFLIGHT,'scripts/oct18_frozen_sources.py','scripts/run_nov04_components.py',
            *sorted('src/auto_research/'+source for source,_ in COMPONENTS.values())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--device',choices=('cpu','cuda'),default='cpu')
    parser.add_argument('--source-commit')
    parser.add_argument('--frozen-proof',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('immutable new output path required')
    commit = args.source_commit or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    hashes = {path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in sources()}
    proof = json.loads(args.frozen_proof.read_text()) if args.frozen_proof else capture_sources(ROOT,commit,sources())
    verify_sources(ROOT,commit,hashes,proof)
    preflight = json.loads((ROOT/PREFLIGHT).read_text())
    if preflight['seeds']!=SEEDS or set(preflight['component_keys'])!=set(COMPONENTS):
        raise ValueError('fixed preflight identities differ')
    import torch
    torch.set_num_threads(1)
    if args.device=='cuda' and not torch.cuda.is_available():
        parser.error('actual CUDA required; CPU fallback forbidden')
    accelerator = torch.cuda.get_device_name(0) if args.device=='cuda' else 'CPU'
    if args.device=='cuda' and not accelerator.startswith(('NVIDIA A100','NVIDIA A30')):
        parser.error('actual NVIDIA A100/A30 required')
    started, results = time.monotonic(), {}
    for key,(relative,required) in COMPONENTS.items():
        if args.device=='cuda' and required!='cuda':
            continue
        name = '_nov04b_'+key.replace('-','_')
        spec = importlib.util.spec_from_file_location(name,ROOT/'src/auto_research'/relative)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        if bool(module.REQUIRES_GPU_VALIDATION)!=(required=='cuda'):
            raise ValueError('source device contract differs from preflight')
        rows = []
        for seed in SEEDS:
            if time.monotonic()-started>preflight['maximum_run_seconds']:
                raise ValueError('bounded preflight runtime exceeded; no automatic expansion/retry')
            row = module.diagnostic(seed,device=args.device)
            if args.device=='cuda':
                torch.cuda.synchronize()
            validate_diagnostic(row,seed)
            rows.append(row|{'execution_device':args.device,'execution_accelerator':accelerator})
        results[key] = {'per_seed':rows}
    output = {'schema_version':2,'code_commit':commit,'source_sha256':hashes,
              'device':args.device,'accelerator':accelerator,'seeds':SEEDS,'components':results,
              'elapsed_seconds':time.monotonic()-started,'diagnostic_only':True,'evaluation_tier':'l1_mechanism',
              'formal_comparison':False,'pretrained_model_calls':0,'full_experiments_executed':False,
              'promotion_eligible':False,'evolve_integrated':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(output,handle,ensure_ascii=False,indent=2,allow_nan=False)
        handle.write('\n')
    print(json.dumps({'device':args.device,'components':list(results),'elapsed_seconds':output['elapsed_seconds']}))


if __name__=='__main__':
    main()
