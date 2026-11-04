"""Admit source-bound actual low-cost runs without fabricating capability evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from curate_nov04_components import (  # noqa: E402
    aggregate_metrics, evaluation_protocol, generated_input_fingerprint, metrics, write_new,
)
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_nov04_components import validate_diagnostic  # noqa: E402
from run_nov04b_components import COMPONENTS, PREFLIGHT, RUNNER, SEEDS, sources  # noqa: E402

AUDIT = ROOT/'docs/research-audits/nov04-bulletin-components'


def freeze():
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    hashes = {path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in sources()}
    proof = capture_sources(ROOT,commit,sources())
    verify_sources(ROOT,commit,hashes,proof)
    write_new(AUDIT/'frozen-sources.json',{'schema_version':1,'commit':commit,'source_sha256':hashes,'proof':proof})
    print(f'frozen {len(hashes)} execution inputs at {commit}')


def catalogue():
    rows = {}
    for path in (ROOT/'src/auto_research/paper_specs/catalog').glob('*/*.json'):
        spec = json.loads(path.read_text())
        if spec['key'] in COMPONENTS:
            rows[spec['key']] = (path,spec)
    if set(rows)!=set(COMPONENTS):
        raise ValueError('exact fixed component catalogue required')
    return rows


def validate_raw(raw,device,frozen):
    expected = set(COMPONENTS) if device=='cpu' else {key for key,(_,required) in COMPONENTS.items() if required=='cuda'}
    if (device not in ('cpu','cuda') or raw.get('device')!=device or set(raw.get('components',{}))!=expected
            or raw.get('seeds')!=SEEDS or raw.get('code_commit')!=frozen['commit']
            or raw.get('source_sha256')!=frozen['source_sha256']
            or raw.get('diagnostic_only') is not True or raw.get('formal_comparison') is not False
            or raw.get('full_experiments_executed') is not False or raw.get('pretrained_model_calls')!=0
            or raw.get('promotion_eligible') is not False or raw.get('evolve_integrated') is not False):
        raise ValueError('execution identity/source/diagnostic boundary mismatch')
    preflight = json.loads((ROOT/PREFLIGHT).read_text())
    elapsed = raw.get('elapsed_seconds')
    if type(elapsed) not in (int,float) or not 0<=elapsed<=preflight['maximum_run_seconds']:
        raise ValueError('actual run exceeded bounded cost or elapsed time absent')
    accelerator = raw.get('accelerator','')
    if (device=='cpu' and accelerator!='CPU') or (device=='cuda' and not accelerator.startswith(('NVIDIA A100','NVIDIA A30'))):
        raise ValueError('actual required accelerator stamp missing')
    verify_sources(ROOT,frozen['commit'],raw['source_sha256'],frozen['proof'])
    for result in raw['components'].values():
        rows = result['per_seed']
        if len(rows)!=3 or [row['seed'] for row in rows]!=SEEDS:
            raise ValueError('three actual independent seed rows required')
        for row,seed in zip(rows,SEEDS):
            validate_diagnostic(row,seed)
            if (row.get('diagnostic_only') is not True or row.get('evaluation_tier')!='l1_mechanism'
                    or row.get('execution_device')!=device or row.get('execution_accelerator')!=accelerator
                    or not metrics(row)):
                raise ValueError('per-seed measurement, device or evidence tier differs')


def ingest(cpu_path,cuda_path):
    frozen = json.loads((AUDIT/'frozen-sources.json').read_text())
    blobs = {'cpu':cpu_path.read_bytes(),'cuda':cuda_path.read_bytes()}
    raw = {device:json.loads(blob) for device,blob in blobs.items()}
    for device in raw:
        validate_raw(raw[device],device,frozen)
    pending, specifications = [], catalogue()
    for key,(module,device) in COMPONENTS.items():
        path,spec = specifications[key]
        if (spec.get('requires_gpu_validation') is not (device=='cuda')
                or spec.get('full_experiment_status')!='not_reproduced_high_cost'
                or spec.get('full_experiment_review_done') is not True):
            raise ValueError('cost/device contract must be declared before evidence admission')
        rows = raw[device]['components'][key]['per_seed']
        aggregate = aggregate_metrics(rows)
        relative = Path('docs')/Path(spec['detail_path']).parent/f'metrics/component-{device}-seeds42-44.json'
        dataset = {'id':f'synthetic:nov04b-{key}-v1','revision':'sha256:'+frozen['source_sha256']['src/auto_research/'+module],
                   'recipe':'small seeded tensor/arithmetic/state contracts; no public capability benchmark','capability_benchmark':False}
        result = {'schema_version':2,'method':key,'manifest_ref':spec['domain']+':'+key,
                  'dataset':dataset,'seed':SEEDS,'seeds':SEEDS,'per_seed':rows,'metrics':aggregate,
                  'diagnostic_only':True,'fixture_demo':True,'formal_comparison':False,
                  'evaluation_tier':'l1_mechanism','evaluation_protocol':evaluation_protocol(),
                  'promotion_eligible':False,'evolve_integrated':False,
                  'full_experiment_status':'not_reproduced_high_cost','full_experiment_review_done':True,
                  'automatic_retry':False,'automatic_implementation_queue':False,
                  'provenance':{'commit':frozen['commit'],'artifact_path':relative.as_posix(),
                                'accelerator':raw[device]['accelerator'],
                                'dataset_fingerprint':generated_input_fingerprint(dataset,frozen['source_sha256']),
                                'executed_source_sha256':frozen['source_sha256'],
                                'raw_runner_artifact_sha256':hashlib.sha256(blobs[device]).hexdigest()}}
        pending.append((ROOT/relative,result))
        if device=='cuda':
            receipt_path=f'docs/gpu-validations/{key}-a100-20261104.json'
            if spec.get('gpu_validation_artifact')!=receipt_path:
                raise ValueError('catalog receipt target differs')
            receipt = {'schema_version':1,'adapter_key':key,'validated_at':'2026-11-04',
                       'accelerator':{'vendor':'NVIDIA','model':raw[device]['accelerator'],'count':1},
                       'command':['timeout','300','python3',RUNNER,'--device','cuda','--source-commit',frozen['commit'],
                                  '--frozen-proof','nov04b-proof.json','--output','raw-cuda.json'],
                       'dataset':dataset,'checkpoint':{'public_id':'none-seeded-component-initialization',
                                                     'revision':frozen['commit'],'pretrained':False},
                       'seeds':SEEDS,'result':'passed','metrics':aggregate,'diagnostic_only':True,
                       'promotion_eligible':False,'evolve_integrated':False,'full_experiment_status':'not_reproduced_high_cost',
                       'provenance':result['provenance']|{'artifact_path':receipt_path,'metric_artifact_path':relative.as_posix()}}
            sys.path.insert(0,str(ROOT/'src'))
            from auto_research.gpu_validation import validate_gpu_receipt
            if errors:=validate_gpu_receipt(receipt):
                raise ValueError(str(errors))
            pending.append((ROOT/receipt_path,receipt))
        specifications[key] = (path,spec|{'gpu_validation_passed':device=='cuda',
                                         'implementation_status':'component_only','review_done':True})
    pending.extend((AUDIT/f'raw-{device}.json',json.loads(blob)) for device,blob in blobs.items())
    if any(path.exists() for path,_ in pending):
        raise ValueError('refuse accepted execution-artifact overwrite')
    for path,value in pending:
        write_new(path,value)
    for path,spec in specifications.values():
        path.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
    print('accepted twelve L1 components: six actual CUDA, six CPU; no capability or Evolve claims')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze',action='store_true')
    parser.add_argument('--cpu',type=Path)
    parser.add_argument('--cuda',type=Path)
    args=parser.parse_args()
    if args.freeze:
        freeze()
    elif args.cpu and args.cuda:
        ingest(args.cpu,args.cuda)
    else:
        parser.error('--freeze or both --cpu/--cuda required')
