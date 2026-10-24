from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/'docs/research-audits/oct25-priority-components'
KEYS = ['minimal-edit-opd', 'inside-jepa', 'group-dpo']


def curator():
    return runpy.run_path(str(ROOT/'scripts/build_oct25_component_artifacts.py'))


def raw_runs():
    return {device: json.loads((AUDIT/f'raw-{device}.json').read_text()) for device in ('cpu', 'cuda')}


def scope_and_batch(c):
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    batch = next(b for b in json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())['batches'] if b['batch'] == c['BATCH'])
    return scope, batch


def test_frozen_three_seed_exact_claims_and_selected_scope():
    c = curator()
    c['check']()
    scope, _ = scope_and_batch(c)
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    assert scope['selected_scope_complete'] and scope['component_count'] == 3
    assert scope['gpu_validated_component_count'] == 3 and scope['capability_reproductions_claimed'] == 0
    assert coverage['counts']['components_pending_verification'] == 0
    assert coverage['counts']['recent_overlap_backfills'] == 2
    assert coverage['counts']['historical_official_source_backfills'] == 1
    assert coverage['counts']['new_first_publications_after_previous_capture'] == 0
    assert coverage['counts']['snapshot_added_base_identities_not_new_paper_count'] == 0
    assert coverage['actual_announced_on'] == '2026-10-23' and not coverage['new_announcement_batch_available']
    assert coverage['review_watermark'] == {'before': '2026-10-15', 'after': '2026-10-15'}
    assert not coverage['review_watermark_advanced'] and not coverage['all_sources_exhaustive']


def test_failed_priority_directory_deltas_are_unknown_not_zero():
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    rows = {r['organization']: r for r in coverage['official_directory_deltas']}
    for organization in ('Google', 'Meta'):
        assert not rows[organization]['delta_known']
        assert rows[organization]['new_directory_urls'] is None and rows[organization]['changed_records'] is None
        assert rows[organization]['status'] == 'source_unavailable_not_zero_delta'
    assert rows['Google DeepMind']['delta_known']
    assert rows['Google DeepMind']['new_directory_urls'] == []
    assert coverage['counts']['official_directory_delta_unknown'] == 2


@pytest.mark.parametrize('key', KEYS)
def test_named_defining_checks_and_metrics_are_not_replaceable(key):
    c = curator()
    rows = raw_runs()['cpu']['components'][key]['per_seed']
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
    raw['cuda']['components'] = deepcopy(raw['cpu']['components'])
    with pytest.raises(ValueError, match='per-seed execution device'):
        c['validate_raw'](raw)


@pytest.mark.parametrize('key', KEYS)
@pytest.mark.parametrize('field,value', [('promotion_eligible', True), ('evolve_integrated', True),
    ('evaluation_tier', 'l3_pipeline'), ('diagnostic_only', False), ('automatic_retry', True),
    ('automatic_implementation_queue', True), ('full_experiment_status', 'reproduced')])
def test_no_claim_promotion_or_reopening_full_experiments(key, field, value):
    c = curator()
    catalog = deepcopy(c['records']())
    catalog[key][field] = value
    with pytest.raises(ValueError, match='catalog boundary'):
        c['validate_catalog'](catalog)


@pytest.mark.parametrize('field,value', [('local_operator', 'unrelated.fake'), ('local_command', 'python fake.py'),
    ('gpu_validation_artifact', 'docs/gpu-validations/unrelated.json')])
def test_exact_executed_entry_and_gpu_binding(field, value):
    c = curator()
    catalog = deepcopy(c['records']())
    catalog['minimal-edit-opd'][field] = value
    with pytest.raises(ValueError, match='binding|GPU boundary'):
        c['validate_catalog'](catalog)


@pytest.mark.parametrize('path', ['/tmp/evidence-redirect/README.md', '../outside/README.md', 'post-training/unrelated/README.md'])
def test_catalog_cannot_redirect_evidence_paths(path):
    c = curator()
    catalog = deepcopy(c['records']())
    catalog['minimal-edit-opd']['detail_path'] = path
    with pytest.raises(ValueError, match='catalog boundary'):
        c['validate_catalog'](catalog)


@pytest.mark.parametrize('mutation', ['completion_false', 'delivery_status', 'doc', 'catalog_detail', 'catalog_key'])
def test_complete_state_and_all_ledger_aliases_are_bound(mutation):
    c = curator()
    scope, batch = scope_and_batch(c)
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
def test_scope_requires_complete_correct_accepted_identity(target, mutation):
    c = curator()
    scope, batch = scope_and_batch(c)
    rows = scope['papers'] if target == 'scope' else batch['candidates']
    if mutation == 'empty':
        rows.clear()
    elif mutation == 'duplicate':
        rows[-1] = deepcopy(rows[0])
    elif mutation == 'wrong_id':
        rows[0]['id'] = '9999.99999'
    elif mutation == 'wrong_date':
        rows[0]['original_published_at'] = '2026-10-25T00:00:00Z'
    else:
        rows[0]['component_accepted'] = False
    with pytest.raises(ValueError, match='scope/ledger'):
        c['validate_scope'](scope, batch, c['records']())


def test_three_original_figures_and_priority_backfill_dates():
    c = curator()
    catalog = c['records']()
    figures = json.loads((ROOT/'docs/paper-figures-manifest.json').read_text())
    for key in KEYS:
        selected = [r for r in figures if r['page'] == 'docs/'+catalog[key]['detail_path']]
        assert len(selected) == 1 and selected[0]['visually_inspected']
        assert hashlib.sha256((ROOT/selected[0]['asset']).read_bytes()).hexdigest() == selected[0]['sha256']
    scope, _ = scope_and_batch(c)
    by_key = {r['key']: r for r in scope['papers']}
    assert by_key['minimal-edit-opd']['verified_priority_organizations'] == ['Meta']
    assert by_key['group-dpo']['verified_priority_organizations'] == ['Google', 'Google DeepMind']
    assert by_key['group-dpo']['intake_class'] == 'historical-official-conference-backfill'
    assert catalog['group-dpo']['published_at'].startswith('2026-04-')
    assert catalog['group-dpo']['first_author_affiliation'] == 'Carnegie Mellon University'


def test_conference_metadata_leads_are_not_new_or_accepted_delivery():
    audit = json.loads((AUDIT/'google-emnlp-title-identity-audit.json').read_text())
    assert audit['counts'] == {
        'conference_paper_entries': 31, 'already_cataloged_including_current_group_dpo': 2,
        'historical_metadata_leads_not_accepted_for_implementation': 25, 'source_identity_exceptions': 4,
        'newly_accepted_implementation_items_from_this_followup': 0}
    leads = audit['historical_metadata_leads']
    exceptions = audit['source_identity_exceptions']
    assert len(leads) == len({r['id'] for r in leads}) == 25 and len(exceptions) == 4
    assert sum(r['year'] == 2026 for r in leads) == 19 and sum(r['year'] == 2025 for r in leads) == 6
    assert all(r['status'] == 'metadata_only_not_fulltext_reviewed' for r in leads)
    assert all(r['accepted_for_implementation'] is False and r['automatic_implementation_queue'] is False
               for r in leads + exceptions)
    dispositions = json.loads((AUDIT/'source-coverage.json').read_text())['additional_dispositions']
    assert {r['id'] for r in dispositions} == {'2610.30425', '2610.12388', 'official:facebookresearch/AmbiGUI'}
    for row in dispositions:
        assert row['review_done'] and not row['automatic_retry'] and not row['automatic_implementation_queue']
    costs = [r for r in dispositions if r['decision'] == 'not_reproduced_high_cost']
    assert len(costs) == 2 and all(r['full_experiment_review_done'] for r in costs)
    source_only = next(r for r in dispositions if r['id'].startswith('official:'))
    assert source_only['paper_url'] is None and source_only['original_published_at'] is None


def test_source_builder_cannot_overwrite_accepted_scope_or_ledger():
    builder = runpy.run_path(str(ROOT/'scripts/build_oct25_source_audit.py'))
    with pytest.raises(ValueError, match='batch already exists'):
        builder['build'](Path('/nonexistent-input'), Path('/nonexistent-input'))
