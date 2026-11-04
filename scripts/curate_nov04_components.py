"""Generate source proofs and admit actual bounded November component runs."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_nov04_components import COMPONENTS, PREFLIGHT, RUNNER, SEEDS, sources, validate_diagnostic  # noqa: E402

AUDIT = ROOT/'docs/research-audits/nov04-components'


def write_new(path, value):
    if path.exists():
        raise ValueError(f'accepted artifact is immutable: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        json.dump(value,handle,ensure_ascii=False,indent=2,allow_nan=False)
        handle.write('\n')


def freeze():
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources()}
    proof=capture_sources(ROOT,commit,sources())
    verify_sources(ROOT,commit,hashes,proof)
    write_new(AUDIT/'frozen-sources.json',{'schema_version':1,'commit':commit,'source_sha256':hashes,'proof':proof})
    print(f'frozen {len(hashes)} public execution files at {commit}')


def metrics(row):
    values=row.get('metrics',row)
    return {k:v for k,v in values.items() if type(v) in (int,float) and k!='seed'}


def aggregate_metrics(rows):
    """Keep accepted means identical across Python 3.11/3.12 sum algorithms."""
    values=[metrics(row) for row in rows]
    keys=set(values[0]) if values else set()
    if not keys or any(set(row)!=keys for row in values):
        raise ValueError('metric keys differ across seeds')
    if any(not math.isfinite(value) for row in values for value in row.values()):
        raise ValueError('metric values must be finite')
    return {key:math.fsum(row[key] for row in values)/len(values) for key in sorted(keys)}


def evaluation_protocol():
    return {'tier':'l1_mechanism','seeds':list(SEEDS),'formal_comparison':False,
            'claim_policy':'three-seed synthetic mechanism diagnostic; not a capability comparison'}


def generated_input_fingerprint(dataset, hashes):
    # This identifies the synthetic recipe, seeds and exact generators, not
    # downloaded data or a public capability benchmark that was never run.
    recipe={'dataset':dataset,'seeds':SEEDS,'executed_source_sha256':hashes}
    return 'sha256:'+hashlib.sha256(json.dumps(recipe,sort_keys=True).encode()).hexdigest()


def validate_raw(raw, device, frozen):
    expected=set(COMPONENTS) if device=='cpu' else {k for k,(_,d) in COMPONENTS.items() if d=='cuda'}
    if (raw.get('device')!=device or set(raw.get('components',{}))!=expected
            or raw.get('seeds')!=SEEDS or raw.get('code_commit')!=frozen['commit']
            or raw.get('source_sha256')!=frozen['source_sha256']
            or raw.get('diagnostic_only') is not True or raw.get('full_experiments_executed') is not False
            or raw.get('promotion_eligible') is not False or raw.get('evolve_integrated') is not False):
        raise ValueError('raw execution identity, source scope or diagnostic boundary differs')
    accelerator=raw.get('accelerator','')
    if (device=='cpu' and accelerator!='CPU') or (device=='cuda' and not accelerator.startswith(('NVIDIA A100','NVIDIA A30'))):
        raise ValueError('actual required accelerator stamp missing')
    verify_sources(ROOT,frozen['commit'],raw['source_sha256'],frozen['proof'])
    for result in raw['components'].values():
        rows=result['per_seed']
        if len(rows)!=3 or [r['seed'] for r in rows]!=SEEDS:
            raise ValueError('exactly three actual seed rows required')
        for row,seed in zip(rows,SEEDS):
            validate_diagnostic(row,seed)
            if row['execution_device']!=device or row['execution_accelerator']!=accelerator or not metrics(row):
                raise ValueError('per-seed device or numerical diagnostics absent')


def ingest(cpu_path, cuda_path):
    frozen=json.loads((AUDIT/'frozen-sources.json').read_text())
    blobs={'cpu':cpu_path.read_bytes(),'cuda':cuda_path.read_bytes()}
    raw={d:json.loads(blob) for d,blob in blobs.items()}
    for device in raw:validate_raw(raw[device],device,frozen)
    specs={}
    for path in (ROOT/'src/auto_research/paper_specs/catalog').glob('*/*.json'):
        spec=json.loads(path.read_text())
        if spec['key'] in COMPONENTS:specs[spec['key']]=(path,spec)
    if set(specs)!=set(COMPONENTS):raise ValueError('fixed seven component catalog records required')
    pending=[]
    for key,(_,device) in COMPONENTS.items():
        path,spec=specs[key]
        if spec.get('requires_gpu_validation') is not (device=='cuda'):
            raise ValueError('catalog does not declare the actual device contract')
        rows=raw[device]['components'][key]['per_seed']
        aggregate=aggregate_metrics(rows)
        relative=Path('docs')/Path(spec['detail_path']).parent/f'metrics/component-{device}-seeds42-44.json'
        dataset={'id':f'synthetic:nov04-{key}-v1','revision':'sha256:'+frozen['source_sha256']['src/auto_research/'+COMPONENTS[key][0]],
                 'recipe':'small seeded mechanism/state/index contracts; no public capability benchmark','capability_benchmark':False}
        result={'schema_version':2,'method':key,'manifest_ref':spec['domain']+':'+key,'dataset':dataset,'seed':SEEDS,'seeds':SEEDS,
                'per_seed':rows,'metrics':aggregate,'diagnostic_only':True,'fixture_demo':True,'formal_comparison':False,
                'evaluation_tier':'l1_mechanism','promotion_eligible':False,'evolve_integrated':False,
                'evaluation_protocol':evaluation_protocol(),
                'full_experiment_status':'not_reproduced_high_cost','full_experiment_review_done':True,
                'automatic_retry':False,'automatic_implementation_queue':False,
                'provenance':{'commit':frozen['commit'],'artifact_path':relative.as_posix(),'accelerator':raw[device]['accelerator'],
                              'dataset_fingerprint':generated_input_fingerprint(dataset,frozen['source_sha256']),
                              'executed_source_sha256':frozen['source_sha256'],'raw_runner_artifact_sha256':hashlib.sha256(blobs[device]).hexdigest()}}
        pending.append((ROOT/relative,result))
        if device=='cuda':
            receipt_path=f'docs/gpu-validations/{key}-a100-20261104.json'
            if spec['gpu_validation_artifact']!=receipt_path:raise ValueError('receipt target differs')
            receipt={'schema_version':1,'adapter_key':key,'validated_at':'2026-11-04',
                     'accelerator':{'vendor':'NVIDIA','model':raw[device]['accelerator'],'count':1},
                     'command':['python3',RUNNER,'--device','cuda','--source-commit',frozen['commit'],
                                '--frozen-proof','nov04-proof.json','--output','raw-cuda.json'],
                     'dataset':dataset,'checkpoint':{'public_id':'none-seeded-component-initialization','revision':frozen['commit'],'pretrained':False},
                     'seeds':SEEDS,'result':'passed','metrics':aggregate,'diagnostic_only':True,'promotion_eligible':False,
                     'evolve_integrated':False,'full_experiment_status':'not_reproduced_high_cost',
                     'provenance':result['provenance']|{'artifact_path':receipt_path,'metric_artifact_path':relative.as_posix()}}
            sys.path.insert(0,str(ROOT/'src'))
            from auto_research.gpu_validation import validate_gpu_receipt
            if errors:=validate_gpu_receipt(receipt):raise ValueError(str(errors))
            pending.append((ROOT/receipt_path,receipt))
        specs[key]=(path,spec|{'gpu_validation_passed':device=='cuda','implementation_status':'component_only','review_done':True})
    for device,blob in blobs.items():pending.append((AUDIT/f'raw-{device}.json',json.loads(blob)))
    if any(path.exists() for path,_ in pending):raise ValueError('refuse to overwrite accepted execution artifacts')
    for path,value in pending:write_new(path,value)
    # Only mechanically synchronize the evidence flags after validated runs.
    for path,spec in specs.values():path.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
    print('accepted seven L1 components: four actual CUDA, three CPU; no capabilities claimed')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze',action='store_true')
    parser.add_argument('--cpu',type=Path)
    parser.add_argument('--cuda',type=Path)
    args=parser.parse_args()
    if args.freeze:freeze()
    elif args.cpu and args.cuda:ingest(args.cpu,args.cuda)
    else:parser.error('--freeze or both --cpu/--cuda required')
