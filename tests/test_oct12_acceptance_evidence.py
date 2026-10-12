"""Protect the frozen sixteen-item handoff, not original benchmark success."""
import hashlib
import json
from pathlib import Path
import re

import pytest

from auto_research.gpu_validation import load_gpu_receipt
from auto_research.paper_specs.schema import load_spec

ROOT = Path(__file__).resolve().parents[1]
KEYS = ('evo2','forte','rsi-anything','branch-opd','cast-opd','road-mopd','msar',
        'orthros','dualquant','boundary-evo','janus','t2mem','rated','jev-workflow','woven','umrm')


def metric(key):
    spec = load_spec(ROOT/'src/auto_research/reproductions'/key.replace('-','_')/'paper.yaml')
    files = list((ROOT/spec.documentation).parent.glob('metrics/*.json'))
    assert len(files) == 1, 'historical failures belong in assets, not measured capability cards'
    return spec, files[0], json.loads(files[0].read_text())


@pytest.mark.parametrize('key',KEYS)
def test_all_frozen_items_have_actual_sanitized_protocol_and_source_evidence(key):
    spec,path,payload = metric(key)
    receipt_path = ('docs/gpu-validations/oct12-jev-workflow-measurement-a100.json'
                    if key == 'jev-workflow' else spec.execution['gpu_validation_artifact'])
    receipt = load_gpu_receipt(ROOT/receipt_path)
    assert receipt['accelerator']['vendor'] == 'NVIDIA'
    assert 'A100' in receipt['accelerator']['model'] or 'A30' in receipt['accelerator']['model']
    assert receipt['executed_source_sha256']
    assert all(re.fullmatch('[a-f0-9]{64}',value) for value in receipt['executed_source_sha256'].values())
    assert payload['schema_version'] == 2 and payload['adapter_key'] == key
    assert payload['measured_locally'] is True and payload['diagnostic_only'] is True
    assert payload['metrics'] and payload['manifest_ref'] == 'reproduction:'+key
    protocol = payload['evaluation_protocol']
    assert isinstance(protocol,dict) and protocol['claim_policy']
    assert protocol['formal_comparison'] is False and protocol['seeds'] == payload['seeds']
    provenance = payload['provenance']
    assert provenance['artifact_path'] == path.relative_to(ROOT).as_posix()
    assert provenance['dataset_fingerprint'] != 'not recorded in historical artifact'
    assert provenance['executed_code_commit'] == receipt['provenance']['commit']
    assert provenance['gpu_validation_artifact'] == receipt_path
    assert 'paper_reported' not in payload or payload['paper_reported'] is False
    if provenance.get('dataset_fingerprint_kind','').startswith('sha256 of canonical JSON'):
        serialized = json.dumps(payload['dataset'],sort_keys=True,ensure_ascii=False,separators=(',',':'))
        assert provenance['dataset_fingerprint'] == hashlib.sha256(serialized.encode()).hexdigest()


def test_boundary_acceptance_is_not_priming_only_and_opd_core_operators_really_ran():
    _,_,boundary = metric('boundary-evo')
    assert boundary['metrics']['evolution_optimizer_steps'] > 0
    assert boundary['metrics']['boundary_rounds_with_updates'] > 0
    _,_,branch = metric('branch-opd')
    assert branch['metrics']['pbr_constraints'] > 0 and branch['metrics']['sampled_branches'] > 0
    _,_,road = metric('road-mopd')
    assert road['metrics']['projected_tensors'] > 0 and road['metrics']['conflicting_tensors'] > 0


def test_evo_acceptance_keeps_genuine_gradient_gates_and_prior_failure_evidence():
    _,_,payload = metric('evo2')
    run = payload['run']
    assert run['warmup']['parameters_changed']
    assert any(step['gradient_norm'] > 0 for step in run['warmup']['steps'])
    assert any(step['updated'] and step['parameters_changed'] and step['gradient_norm'] > 0
               for step in run['training'])
    assert payload['evaluation_protocol']['formal_comparison'] is False
    assert (ROOT/'docs/reproductions/2610.13025-evo2/assets/historical-circle-failures.json').is_file()
    assert (ROOT/'docs/reproductions/2610.13194-janus/assets/historical-eager-oom.json').is_file()
