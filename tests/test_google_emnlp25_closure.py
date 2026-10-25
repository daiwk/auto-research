from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/'docs/research-audits/google-emnlp25-closure'


def curator():
    return runpy.run_path(str(ROOT/'scripts/curate_google_emnlp25_evidence.py'))


def inputs():
    c = curator()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    batch = next(b for b in json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())['batches'] if b['batch'] == c['BATCH'])
    return c, scope, batch, c['catalogue'](), c['spec_rows']()


def raw_runs():
    return {device: json.loads((AUDIT/f'raw-{device}.json').read_text()) for device in ('cpu', 'cuda')}


def test_all25_approved_leads_have_exactly_one_review_disposition():
    c, scope, batch, catalog, specs = inputs()
    c['check']()
    assert len(scope['papers']) == 25
    assert scope['selected_scope_complete'] and scope['review_scope_closed']
    assert scope['counts']['component_only'] == scope['counts']['components_accepted'] == len(specs) == 14
    assert scope['counts']['not_reproduced_high_cost'] == 8
    assert scope['counts']['not_selected'] == 3
    assert scope['counts']['gpu_validated_components'] == 10
    assert scope['counts']['components_pending_verification'] == scope['counts']['gpu_components_pending'] == 0
    assert scope['counts']['new_first_publications'] == scope['counts']['capability_reproductions_claimed'] == 0
    assert json.loads((AUDIT/'review-decisions.json').read_text()) == scope['papers']
    assert all(r['priority'] in {'P0', 'P1', 'P2'} for r in scope['papers'])
    assert scope['review_watermark'] == {'before': '2026-10-15', 'after': '2026-10-15'}
    assert not scope['review_watermark_advanced'] and not scope['all_sources_exhaustive']
    c['validate_scope'](scope, batch, specs, catalog)


def test_cost_closure_does_not_turn_into_implementation_or_gpu_requirement():
    c, scope, _, catalog, _ = inputs()
    for row in scope['papers']:
        assert row['review_done'] and not row['automatic_retry'] and not row['automatic_implementation_queue']
        assert row['cost_assessment'] and row['method_review'] and row['sources']
        if row['decision'] == 'not_reproduced_high_cost':
            item = catalog[row['catalog_key']]
            assert not row['accepted_for_implementation'] and not row['implemented']
            assert item['implementation_status'] == 'deferred_high_cost'
            assert not item.get('requires_gpu_validation') and not item.get('local_operator')
            assert '不复现（审查 DONE）' in item['deferral_reason']
    rejected = {r['id'] for r in scope['papers'] if r['decision'] == 'not_selected'}
    assert rejected == {'2605.29442', '2602.05945', '2609.15191'}
    original, digest = c['approved_input']()
    assert len(original) == 25 and digest == scope['input_sha256']


@pytest.mark.parametrize('target', ['scope', 'ledger'])
@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'wrong_id', 'wrong_date', 'missing_priority', 'wrong_priority', 'unaccepted'])
def test_no_missing_duplicate_or_wrongly_accepted_paper(target, mutation):
    c, scope, batch, catalog, specs = inputs()
    rows = scope['papers'] if target == 'scope' else batch['candidates']
    if mutation == 'missing':
        rows.pop()
    elif mutation == 'duplicate':
        rows[-1] = deepcopy(rows[0])
    elif mutation == 'wrong_id':
        rows[0]['id'] = '9999.99999'
    elif mutation == 'wrong_date':
        next(r for r in rows if r['decision'] == 'component_only')['published_at'] = '2026-10-25T00:00:00Z'
    elif mutation == 'missing_priority':
        next(r for r in rows if r['decision'] == 'component_only').pop('priority')
    elif mutation == 'wrong_priority':
        next(r for r in rows if r['decision'] == 'component_only')['priority'] = 'P2'
    else:
        next(r for r in rows if r['decision'] == 'component_only')['component_accepted'] = False
    with pytest.raises((ValueError, KeyError)):
        c['validate_scope'](scope, batch, specs, catalog)


@pytest.mark.parametrize('mutation', ['completion', 'counts', 'component_set', 'watermark', 'alias'])
def test_scope_ledger_closure_is_not_a_label_only(mutation):
    c, scope, batch, catalog, specs = inputs()
    if mutation == 'completion':
        scope['selected_scope_complete'] = False
    elif mutation == 'counts':
        scope['counts']['components_accepted'] = 999
    elif mutation == 'component_set':
        scope['fixed_component_keys'].pop()
    elif mutation == 'watermark':
        scope['review_watermark']['after'] = '2026-10-25'
    else:
        next(r for r in batch['candidates'] if r['decision'] == 'component_only')['catalog_detail'] = 'unrelated/README.md'
    with pytest.raises(ValueError):
        c['validate_scope'](scope, batch, specs, catalog)


@pytest.mark.parametrize('field,value', [('promotion_eligible', True), ('evolve_integrated', True),
    ('diagnostic_only', False), ('evaluation_tier', 'l3_pipeline'), ('automatic_retry', True),
    ('automatic_implementation_queue', True), ('full_experiment_status', 'reproduced')])
def test_no_unmeasured_capability_or_retry_promotion(field, value):
    c, _, _, catalog, specs = inputs()
    changed = deepcopy(catalog)
    changed[next(iter(specs))][field] = value
    with pytest.raises(ValueError, match='catalog boundary'):
        c['validate_catalog'](changed, specs)


@pytest.mark.parametrize('field,value', [('local_operator', 'unrelated.fake'), ('local_command', 'python fake.py'),
    ('detail_path', '/tmp/outside/README.md'), ('detail_path', '../outside/README.md')])
def test_executed_entry_and_evidence_path_cannot_be_redirected(field, value):
    c, _, _, catalog, specs = inputs()
    changed = deepcopy(catalog)
    changed[next(iter(specs))][field] = value
    with pytest.raises(ValueError):
        c['validate_catalog'](changed, specs)


def test_cpu_rows_cannot_be_copied_into_cuda_header():
    c = curator()
    specs, raw = c['spec_rows'](), raw_runs()
    for key in list(raw['cuda']['components']):
        raw['cuda']['components'][key] = deepcopy(raw['cpu']['components'][key])
    with pytest.raises(ValueError, match='per-seed execution device'):
        c['validate_raw'](raw, specs)


@pytest.mark.parametrize('mutation', ['checks', 'metrics', 'seed', 'source', 'commit'])
def test_defining_checks_metrics_and_frozen_identity_are_required(mutation):
    c, raw = curator(), raw_runs()
    specs = c['spec_rows']()
    row = raw['cpu']['components'][next(iter(specs))]['per_seed'][0]
    if mutation == 'checks':
        row['checks'] = {'unrelated': True}
    elif mutation == 'metrics':
        row['metrics']['unrelated'] = 1
    elif mutation == 'seed':
        row['seed'] = 99
    elif mutation == 'source':
        raw['cpu']['source_sha256'].pop(next(iter(raw['cpu']['source_sha256'])))
    else:
        raw['cuda']['code_commit'] = '0'*40
    with pytest.raises(ValueError):
        c['validate_raw'](raw, specs)


def test_all22_documented_papers_have_original_reviewed_figures():
    _, scope, _, catalog, _ = inputs()
    figures = json.loads((ROOT/'docs/paper-figures-manifest.json').read_text())
    selected = [r for r in scope['papers'] if r['decision'] in {'component_only', 'not_reproduced_high_cost'}]
    assert len(selected) == 22
    for row in selected:
        matches = [f for f in figures if f['page'] == 'docs/'+catalog[row['catalog_key']]['detail_path']]
        assert len(matches) == 1 and matches[0]['visually_inspected']
        assert hashlib.sha256((ROOT/matches[0]['asset']).read_bytes()).hexdigest() == matches[0]['sha256']


def test_duplicate_builder_run_cannot_erase_accepted_delivery():
    builder = runpy.run_path(str(ROOT/'scripts/build_google_emnlp25_closure.py'))
    with pytest.raises(ValueError, match='batch already exists'):
        builder['build']([Path('/nonexistent-input')])
