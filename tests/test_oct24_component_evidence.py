from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/'docs/research-audits/oct24-overlap-components'


def curator():
    return runpy.run_path(str(ROOT/'scripts/build_oct24_component_artifacts.py'))


def raw_runs():
    return {d: json.loads((AUDIT/f'raw-{d}.json').read_text()) for d in ('cpu', 'cuda')}


def test_frozen_three_seed_exact_claims_and_selected_scope():
    c = curator()
    c['check']()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    assert scope['selected_scope_complete'] and scope['component_count'] == 4
    assert scope['gpu_validated_component_count'] == 3 and scope['capability_reproductions_claimed'] == 0
    assert coverage['counts']['components_pending_verification'] == 0
    assert coverage['counts']['components_pending_gpu_and_integration'] == 0
    assert coverage['counts']['new_first_publications_after_previous_capture'] == 0
    assert coverage['counts']['snapshot_added_base_identities_not_new_paper_count'] == 0
    assert coverage['actual_announced_on'] == '2026-10-23' and not coverage['new_announcement_batch_available']
    assert coverage['review_watermark'] == {'before': '2026-10-15', 'after': '2026-10-15'}
    assert not coverage['review_watermark_advanced'] and not coverage['all_sources_exhaustive']


def test_failed_priority_sources_are_unknown_not_zero_delta():
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    by_org = {r['organization']: r for r in coverage['official_directory_deltas']}
    for org in ('Google', 'Meta'):
        assert not by_org[org]['delta_known']
        assert by_org[org]['new_directory_urls'] is None and by_org[org]['changed_records'] is None
        assert by_org[org]['status'] == 'source_unavailable_not_zero_delta'
    assert by_org['Google DeepMind']['delta_known']
    assert by_org['Google DeepMind']['new_directory_urls'] == []
    assert coverage['counts']['official_directory_delta_unknown'] == 2
    assert coverage['independent_retry_receipts']


@pytest.mark.parametrize('key', ['physical-engineering-exam', 'ttr-compressor', 'userarena-optd', 'moer'])
def test_named_defining_checks_and_metric_schema_are_not_replaceable(key):
    c, raw = curator(), raw_runs()
    rows = raw['cpu']['components'][key]['per_seed']
    rows[0]['checks'] = {'unrelated': True}
    with pytest.raises(ValueError, match='defining checks'):
        c['gates'](key, rows)
    rows = raw_runs()['cpu']['components'][key]['per_seed']
    rows[0]['metrics']['unrelated'] = 1
    with pytest.raises(ValueError, match='metric schema'):
        c['gates'](key, rows)


@pytest.mark.parametrize('field,value', [('accelerator', 'CPU'), ('code_commit', '0'*40)])
def test_cuda_device_and_frozen_source_cannot_be_substituted(field, value):
    c, raw = curator(), raw_runs()
    raw['cuda'][field] = value
    with pytest.raises(ValueError, match='raw device|frozen identity'):
        c['validate_raw'](raw)


def test_cpu_seed_rows_cannot_be_copied_into_cuda_header():
    c, raw = curator(), raw_runs()
    for key in c['CUDA_KEYS']:
        raw['cuda']['components'][key] = deepcopy(raw['cpu']['components'][key])
    with pytest.raises(ValueError, match='per-seed execution device'):
        c['validate_raw'](raw)


@pytest.mark.parametrize('key', ['physical-engineering-exam', 'ttr-compressor', 'userarena-optd', 'moer'])
@pytest.mark.parametrize('field,value', [('promotion_eligible', True), ('evolve_integrated', True),
    ('evaluation_tier', 'l3_pipeline'), ('diagnostic_only', False), ('automatic_retry', True),
    ('automatic_implementation_queue', True), ('full_experiment_status', 'reproduced')])
def test_no_component_claim_promotion_or_reopening_full_experiment(key, field, value):
    c = curator()
    catalog = deepcopy(c['records']())
    catalog[key][field] = value
    with pytest.raises(ValueError, match='catalog boundary'):
        c['validate_catalog'](catalog)


@pytest.mark.parametrize('field,value', [('local_operator', 'unrelated.fake'), ('local_command', 'python fake.py'),
    ('gpu_validation_artifact', 'docs/gpu-validations/unrelated.json')])
def test_catalog_exact_executed_entry_and_gpu_binding(field, value):
    c = curator()
    catalog = deepcopy(c['records']())
    catalog['userarena-optd'][field] = value
    with pytest.raises(ValueError, match='binding|GPU boundary'):
        c['validate_catalog'](catalog)


@pytest.mark.parametrize('path', ['/tmp/evidence-redirect/README.md', '../outside/README.md', 'post-training/unrelated/README.md'])
def test_catalog_cannot_redirect_evidence_paths(path):
    c = curator()
    catalog = deepcopy(c['records']())
    catalog['userarena-optd']['detail_path'] = path
    with pytest.raises(ValueError, match='catalog boundary'):
        c['validate_catalog'](catalog)


@pytest.mark.parametrize('mutation', ['completion_false', 'delivery_status', 'doc', 'catalog_detail', 'catalog_key'])
def test_complete_state_and_all_ledger_aliases_are_bound(mutation):
    c = curator()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    batch = next(b for b in json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())['batches'] if b['batch'] == c['BATCH'])
    if mutation == 'completion_false':
        scope['selected_scope_complete'] = False
        batch['candidates'][0]['component_accepted'] = False
    elif mutation == 'delivery_status':
        scope['delivery_status'] = 'pending_component_verification'
    else:
        batch['candidates'][0][mutation] = 'unrelated'
    with pytest.raises(ValueError, match='scope/ledger'):
        c['validate_scope'](scope, batch, c['records']())


@pytest.mark.parametrize('target', ['scope', 'ledger'])
@pytest.mark.parametrize('mutation', ['empty', 'duplicate', 'wrong_id', 'wrong_date', 'unaccepted'])
def test_scope_ledger_require_complete_correct_accepted_identity(target, mutation):
    c = curator()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    batch = next(b for b in json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())['batches'] if b['batch'] == c['BATCH'])
    rows = scope['papers'] if target == 'scope' else batch['candidates']
    if mutation == 'empty':
        rows.clear()
    elif mutation == 'duplicate':
        rows[-1] = deepcopy(rows[0])
    elif mutation == 'wrong_id':
        rows[0]['id'] = '9999.99999'
    elif mutation == 'wrong_date':
        rows[0]['original_published_at'] = '2026-10-24T00:00:00Z'
    else:
        rows[0]['component_accepted'] = False
    with pytest.raises(ValueError, match='scope/ledger'):
        c['validate_scope'](scope, batch, c['records']())


def test_four_original_figures_and_non_reproduction_dispositions():
    c = curator()
    catalog = c['records']()
    figures = json.loads((ROOT/'docs/paper-figures-manifest.json').read_text())
    for key in c['MODULES']:
        page = 'docs/'+catalog[key]['detail_path']
        selected = [r for r in figures if r['page'] == page]
        assert len(selected) == 1 and selected[0]['visually_inspected']
        assert hashlib.sha256((ROOT/selected[0]['asset']).read_bytes()).hexdigest() == selected[0]['sha256']
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    assert {r['id'] for r in coverage['additional_dispositions']} == {'2610.30933', '2610.31276'}
    assert all(r['review_done'] and r['decision'] == 'not_reproduced_high_cost'
               and not r['automatic_retry'] and not r['automatic_implementation_queue']
               for r in coverage['additional_dispositions'])
    assert catalog['physical-engineering-exam']['first_author_affiliation'] == 'Google Cloud AI Research'
    assert catalog['userarena-optd']['first_author_affiliation'] == 'Leiden University'
