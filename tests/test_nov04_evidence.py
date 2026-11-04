import copy
import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from curate_nov04_components import AUDIT, COMPONENTS, metrics, validate_raw  # noqa: E402
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402


def load(name):
    return json.loads((AUDIT/name).read_text())


@pytest.mark.parametrize('device',['cpu','cuda'])
def test_actual_runs_have_fixed_sources_devices_and_seeds(device):
    raw=load(f'raw-{device}.json')
    validate_raw(raw,device,load('frozen-sources.json'))
    assert raw['pretrained_model_calls']==0
    assert raw['formal_comparison'] is False


@pytest.mark.parametrize('field,value',[('code_commit','0'*40),('seeds',[42]),('full_experiments_executed',True),
                                       ('promotion_eligible',True),('accelerator','CPU')])
def test_false_execution_claims_rejected(field,value):
    raw=copy.deepcopy(load('raw-cuda.json'));raw[field]=value
    with pytest.raises(ValueError):
        validate_raw(raw,'cuda',load('frozen-sources.json'))


def test_missing_seed_or_false_check_cannot_be_accepted():
    raw=load('raw-cuda.json')
    raw['components']['proland']['per_seed'][0]['checks']['injected_failure']=False
    with pytest.raises(ValueError):validate_raw(raw,'cuda',load('frozen-sources.json'))


def test_catalog_metrics_and_receipts_agree_with_actual_raw():
    specs={}
    for path in (ROOT/'src/auto_research/paper_specs/catalog').glob('*/*.json'):
        row=json.loads(path.read_text())
        if row['key'] in COMPONENTS:specs[row['key']]=row
    assert set(specs)==set(COMPONENTS)
    for key,spec in specs.items():
        device=COMPONENTS[key][1]
        raw=load(f'raw-{device}.json')
        relative=Path('docs')/Path(spec['detail_path']).parent/f'metrics/component-{device}-seeds42-44.json'
        evidence=json.loads((ROOT/relative).read_text())
        assert evidence['per_seed']==raw['components'][key]['per_seed']
        assert evidence['diagnostic_only'] and not evidence['promotion_eligible']
        assert evidence['provenance']['commit']==raw['code_commit']
        assert evidence['provenance']['raw_runner_artifact_sha256']==hashlib.sha256((AUDIT/f'raw-{device}.json').read_bytes()).hexdigest()
        expected={k:sum(metrics(r)[k] for r in evidence['per_seed'])/3 for k in metrics(evidence['per_seed'][0])}
        assert evidence['metrics']==expected
        if device=='cuda':
            receipt=load_gpu_receipt(ROOT/spec['gpu_validation_artifact'])
            assert receipt['adapter_key']==key and spec['gpu_validation_passed']
            assert receipt['metrics']==evidence['metrics']
            assert receipt['provenance']['commit']==raw['code_commit']
        else:assert not spec['requires_gpu_validation']


def test_google_tpu_paper_is_not_a_cuda_substitute_or_executable_operator():
    spec=json.loads((ROOT/'src/auto_research/paper_specs/catalog/foundation-models/xla-trenches.json').read_text())
    assert spec['first_author_affiliation']=='Google'
    assert spec['implementation_status']=='deferred_high_cost'
    assert spec['full_experiment_status']=='not_reproduced_high_cost'
    assert spec['local_operator'] is None and spec['adapter'] is None
    assert not spec['requires_gpu_validation'] and not spec['evolve_integrated']
    assert spec['gpu_validation_passed'] is False
    assert not (ROOT/'docs'/Path(spec['detail_path']).parent/'metrics').exists()


def test_bounded_source_scope_does_not_claim_global_closure():
    coverage=load('source-coverage.json')
    assert coverage['actual_announced_on']==['2026-11-03']
    assert coverage['review_watermark']=={'before':'2026-10-15','after':'2026-10-15'}
    assert not coverage['all_sources_exhaustive'] and not coverage['full_bulletin_full_text_review_complete']
    receipts=coverage['retrieval_receipts']
    for kind in ['arxiv-new','arxiv-recent']:
        selected=[r for r in receipts if r['kind']==kind]
        assert len(selected)==8 and all(r['parse_complete'] for r in selected)
        assert all(r['parsed_entries']==r['expected_entries'] for r in selected)
    assert len([r for r in receipts if r['kind']=='official'])==45
    assert not load('unreviewed-leads.json')['review_done']


def test_new_papers_have_attributed_original_figures():
    scope=load('task-scope.json')
    manifest=json.loads((ROOT/'docs/paper-figures-manifest.json').read_text())
    for row in scope['papers']:
        page='docs/'+row['detail_path']
        matches=[f for f in manifest if f['page']==page]
        assert len(matches)==1 and matches[0]['visually_inspected']
        assert matches[0]['sha256']==hashlib.sha256((ROOT/matches[0]['asset']).read_bytes()).hexdigest()
        assert '版权' in (ROOT/page).read_text()
