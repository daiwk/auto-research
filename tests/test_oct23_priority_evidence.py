from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/'docs/research-audits/oct23-priority-components'


def module():
    return runpy.run_path(str(ROOT/'scripts/build_oct23_priority_artifacts.py'))


def raw_runs():
    return {d: json.loads((AUDIT/f'raw-{d}.json').read_text()) for d in ('cpu', 'cuda')}


def test_actual_frozen_three_seed_component_evidence_and_scope():
    m = module()
    m['check']()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    assert scope['selected_scope_complete'] and scope['component_count'] == 8
    assert scope['gpu_validated_component_count'] == 5 and scope['capability_reproductions_claimed'] == 0
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    assert coverage['delivery_status'] == 'bounded_scope_complete'
    assert coverage['counts']['components_accepted'] == 8
    assert coverage['counts']['components_pending_gpu_and_integration'] == 0
    assert coverage['counts']['components_pending_verification'] == 0
    assert not coverage['review_watermark_advanced'] and not coverage['all_sources_exhaustive']
    assert coverage['review_watermark'] == {'before': '2026-10-15', 'after': '2026-10-15'}


@pytest.mark.parametrize('key', ['gemma-priority-protocol', 'rkl-policy-distillation', 'openattention', 'moezip', 'aopd', 'gift', 'pair', 'jev-dlc'])
def test_defining_check_names_and_metrics_not_replaced_by_unrelated_true(key):
    m, raw = module(), raw_runs()
    rows = raw['cpu']['components'][key]['per_seed']
    rows[0]['checks'] = {'unrelated': True}
    with pytest.raises(ValueError, match='defining checks'):
        m['gates'](key, rows)


@pytest.mark.parametrize('key', ['openattention', 'moezip', 'aopd', 'gift', 'pair'])
def test_new_gpu_paths_cannot_use_cpu_or_unbound_commit(key):
    m, raw = module(), raw_runs()
    raw['cuda']['accelerator'] = 'CPU'
    with pytest.raises(ValueError, match='raw device'):
        m['validate_raw'](raw)
    raw = raw_runs()
    raw['cuda']['code_commit'] = '0'*40
    with pytest.raises(ValueError, match='frozen source identity'):
        m['validate_raw'](raw)


@pytest.mark.parametrize('key', ['gemma-priority-protocol', 'rkl-policy-distillation', 'openattention', 'moezip', 'aopd', 'gift', 'pair', 'jev-dlc'])
@pytest.mark.parametrize('field,value', [('adapter', {'spec_key': 'fake'}), ('evaluation_tier', 'l3_pipeline'),
    ('diagnostic_only', False), ('promotion_eligible', True), ('evolve_integrated', True),
    ('review_done', False), ('full_experiment_review_done', False), ('automatic_retry', True),
    ('automatic_implementation_queue', True), ('implementation_status', 'full_pipeline')])
def test_catalog_must_not_upgrade_claims_or_reopen_costly_experiments(key, field, value):
    m = module()
    catalog = deepcopy(m['records']())
    catalog[key][field] = value
    with pytest.raises(ValueError, match='catalog boundary'):
        m['validate_catalog'](catalog)


@pytest.mark.parametrize('key', ['gemma-priority-protocol', 'rkl-policy-distillation', 'openattention', 'moezip', 'aopd', 'gift', 'pair', 'jev-dlc'])
def test_exact_cost_and_gpu_catalog_contract(key):
    m = module()
    catalog = deepcopy(m['records']())
    catalog[key]['gpu_validation_artifact'] = 'docs/gpu-validations/unrelated.json'
    with pytest.raises(ValueError, match='cost/GPU'):
        m['validate_catalog'](catalog)
    catalog = deepcopy(m['records']())
    catalog[key]['full_experiment_status'] = 'reproduced'
    with pytest.raises(ValueError, match='cost/GPU'):
        m['validate_catalog'](catalog)


@pytest.mark.parametrize('key', ['gemma-priority-protocol', 'rkl-policy-distillation', 'openattention', 'moezip', 'aopd', 'gift', 'pair', 'jev-dlc'])
@pytest.mark.parametrize('field,value', [('local_operator', 'auto_research.post_training.unrelated'), ('local_command', 'python unrelated.py')])
def test_catalog_entry_cannot_redirect_to_another_algorithm(key, field, value):
    m = module()
    catalog = deepcopy(m['records']())
    catalog[key][field] = value
    with pytest.raises(ValueError, match='executed-entry binding'):
        m['validate_catalog'](catalog)


@pytest.mark.parametrize('target', ['scope', 'ledger'])
@pytest.mark.parametrize('mutation', ['empty', 'missing', 'duplicate', 'wrong_id', 'wrong_url', 'reference_promoted'])
def test_scope_and_ledger_require_every_exact_paper_identity(target, mutation):
    m = module()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    ledger = json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())
    batch = next(b for b in ledger['batches'] if b['batch'] == m['BATCH'])
    rows = scope['papers'] if target == 'scope' else batch['candidates']
    if mutation == 'empty':
        rows.clear()
    elif mutation == 'missing':
        rows.pop()
    elif mutation == 'duplicate':
        rows[-1] = deepcopy(rows[0])
    elif mutation == 'wrong_id':
        rows[0]['id'] = '9999.99999'
    elif mutation == 'wrong_url':
        rows[0]['paper_url'] = 'https://arxiv.org/abs/9999.99999'
    else:
        next(r for r in rows if r['key'] == 'onelatent')['component_implemented'] = True
    with pytest.raises(ValueError, match='scope/ledger'):
        m['validate_scope_identity'](scope, batch, m['records']())


@pytest.mark.parametrize('field,value', [('implementation_status', 'component_only'), ('local_operator', 'fake'),
    ('local_command', 'fake'), ('requires_gpu_validation', True), ('promotion_eligible', True),
    ('evolve_integrated', True), ('automatic_retry', True), ('full_experiment_status', 'reproduced')])
def test_onelatent_is_terminal_documentation_only(field, value):
    m = module()
    catalog = deepcopy(m['records']())
    catalog['onelatent'][field] = value
    with pytest.raises(ValueError, match='terminal reference-only'):
        m['validate_catalog'](catalog)


def test_every_figure_and_metadata_is_bound_without_org_aliasing():
    m = module()
    catalog = m['records']()
    figures = json.loads((ROOT/'docs/paper-figures-manifest.json').read_text())
    for key in (*m['MODULES'], 'onelatent'):
        page = 'docs/'+catalog[key]['detail_path']
        rows = [r for r in figures if r['page'] == page]
        assert len(rows) == 1 and rows[0]['visually_inspected']
        assert hashlib.sha256((ROOT/rows[0]['asset']).read_bytes()).hexdigest() == rows[0]['sha256']
        text = (ROOT/page).read_text()
        assert '## 论文信息' in text and '原作者代码' in text and '本地' in text
    assert catalog['gemma-priority-protocol']['first_author_affiliation'] == 'Google'
    assert catalog['rkl-policy-distillation']['first_author_affiliation'] == 'University of Virginia'
    assert catalog['moezip']['first_author_affiliation'] == 'Korea University'
