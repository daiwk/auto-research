"""Bind the Nov4 bulletin's bounded components to actual immutable executions."""

import copy
import hashlib
import json
import math
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from curate_nov04b_components import (  # noqa: E402
    AUDIT, COMPONENTS, EXECUTION_KEYS, aggregate_metrics, catalogue,
    evaluation_protocol, generated_input_fingerprint, metrics, validate_raw,
)
from migrate_metric_schema_v2 import migrate_payload  # noqa: E402
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402

SOURCE_COMMIT = '0b1fe011eda69ed0e75c6583ac9c01c463f20124'
REFERENCES = {'multi-layer-indexer', 'rsi-dojo'}
CATEGORY_COUNTS = {
    'cs.AI': 413, 'cs.CL': 162, 'cs.CV': 260, 'cs.IR': 35,
    'cs.LG': 445, 'cs.RO': 125, 'cs.SD': 20, 'eess.AS': 12,
}


def load(name):
    return json.loads((AUDIT / name).read_text())


@pytest.mark.parametrize('device', ['cpu', 'cuda'])
def test_actual_runs_keep_frozen_sources_devices_and_three_seeds(device):
    raw, frozen = load(f'raw-{device}.json'), load('frozen-sources.json')
    validate_raw(raw, device, frozen)
    assert raw['code_commit'] == frozen['commit'] == SOURCE_COMMIT
    assert raw['seeds'] == [42, 43, 44]
    assert len(raw['components']) == (12 if device == 'cpu' else 6)
    assert len(frozen['source_sha256']) == 16
    assert raw['pretrained_model_calls'] == 0
    assert raw['full_experiments_executed'] is False
    assert raw['formal_comparison'] is False
    assert raw['promotion_eligible'] is False
    assert raw['evolve_integrated'] is False


@pytest.mark.parametrize('field,value', [
    ('code_commit', '0' * 40), ('seeds', [42]), ('device', 'cpu'),
    ('full_experiments_executed', True), ('pretrained_model_calls', 1),
    ('promotion_eligible', True), ('evolve_integrated', True),
    ('formal_comparison', True), ('accelerator', 'CPU'),
    ('elapsed_seconds', 301), ('elapsed_seconds', float('nan')),
])
def test_tampered_execution_or_promotion_claims_are_rejected(field, value):
    raw = copy.deepcopy(load('raw-cuda.json'))
    raw[field] = value
    with pytest.raises(ValueError):
        validate_raw(raw, 'cuda', load('frozen-sources.json'))


@pytest.mark.parametrize('mutation', [
    'missing-seed', 'different-seed', 'failed-check', 'wrong-device',
    'wrong-accelerator', 'wrong-tier', 'changed-source',
])
def test_incomplete_or_false_per_seed_execution_cannot_be_accepted(mutation):
    raw = copy.deepcopy(load('raw-cuda.json'))
    rows = raw['components']['anchor-kv']['per_seed']
    if mutation == 'missing-seed':
        rows.pop()
    elif mutation == 'different-seed':
        rows[0]['seed'] = 123
    elif mutation == 'failed-check':
        rows[0]['checks']['injected_failure'] = False
    elif mutation == 'wrong-device':
        rows[0]['execution_device'] = 'cpu'
    elif mutation == 'wrong-accelerator':
        rows[0]['execution_accelerator'] = 'CPU'
    elif mutation == 'wrong-tier':
        rows[0]['evaluation_tier'] = 'l2_capability'
    else:
        first_source = next(iter(raw['source_sha256']))
        raw['source_sha256'][first_source] = '0' * 64
    with pytest.raises(ValueError):
        validate_raw(raw, 'cuda', load('frozen-sources.json'))


def test_catalog_metrics_receipts_and_exact_means_match_actual_raw():
    specifications = catalogue()
    assert len(specifications) == 12
    for key, (_, spec) in specifications.items():
        module, device = COMPONENTS[key]
        execution_key = EXECUTION_KEYS[key]
        raw = load(f'raw-{device}.json')
        relative = (Path('docs') / Path(spec['detail_path']).parent
                    / f'metrics/component-{device}-seeds42-44.json')
        evidence = json.loads((ROOT / relative).read_text())
        assert evidence['method'] == key
        assert evidence['manifest_ref'] == spec['domain'] + ':' + key
        assert evidence['per_seed'] == raw['components'][execution_key]['per_seed']
        assert evidence['diagnostic_only'] and evidence['fixture_demo']
        assert evidence['formal_comparison'] is False
        assert evidence['promotion_eligible'] is False
        assert evidence['evolve_integrated'] is False
        assert evidence['provenance']['commit'] == SOURCE_COMMIT
        assert evidence['provenance']['executed_source_sha256'] == raw['source_sha256']
        assert evidence['provenance']['raw_runner_artifact_sha256'] == hashlib.sha256(
            (AUDIT / f'raw-{device}.json').read_bytes()).hexdigest()
        expected = {
            metric: math.fsum(metrics(row)[metric] for row in evidence['per_seed']) / 3
            for metric in metrics(evidence['per_seed'][0])
        }
        assert evidence['metrics'] == expected == aggregate_metrics(evidence['per_seed'])
        assert evidence['evaluation_protocol'] == evaluation_protocol()
        assert evidence['dataset']['revision'] == 'sha256:' + raw['source_sha256'][
            'src/auto_research/' + module]
        assert evidence['dataset']['capability_benchmark'] is False
        assert evidence['provenance']['dataset_fingerprint'] == generated_input_fingerprint(
            evidence['dataset'], raw['source_sha256'])
        assert migrate_payload(ROOT / relative, evidence) == evidence
        assert spec['implementation_status'] == 'component_only'
        assert spec['review_done'] is True
        assert spec['full_experiment_status'] == 'not_reproduced_high_cost'
        assert spec['full_experiment_review_done'] is True
        if device == 'cuda':
            receipt = load_gpu_receipt(ROOT / spec['gpu_validation_artifact'])
            assert spec['requires_gpu_validation'] and spec['gpu_validation_passed']
            assert receipt['adapter_key'] == key
            assert receipt['metrics'] == evidence['metrics']
            assert receipt['seeds'] == [42, 43, 44]
            assert receipt['provenance']['commit'] == SOURCE_COMMIT
            assert receipt['dataset'] == evidence['dataset']
            assert receipt['accelerator']['model'] == raw['accelerator']
            assert receipt['accelerator']['model'].startswith(('NVIDIA A100', 'NVIDIA A30'))
            assert receipt['checkpoint']['pretrained'] is False
        else:
            assert not spec['requires_gpu_validation']
            assert not spec['gpu_validation_passed']


def test_density_dars_identity_does_not_overwrite_dependency_dars_or_raw_execution():
    catalog = ROOT / 'src/auto_research/paper_specs/catalog/post-training'
    original = json.loads((catalog / 'dars.json').read_text())
    density = json.loads((catalog / 'dars-density.json').read_text())
    assert original['key'] == 'dars'
    assert original['paper_url'] == 'https://arxiv.org/abs/2610.01207'
    assert density['key'] == 'dars-density'
    assert density['paper_url'] == 'https://arxiv.org/abs/2611.04792'
    assert EXECUTION_KEYS['dars-density'] == 'dars'
    assert 'dars' not in COMPONENTS
    raw = load('raw-cuda.json')
    assert 'dars' in raw['components'] and 'dars-density' not in raw['components']
    receipt = load_gpu_receipt(ROOT / density['gpu_validation_artifact'])
    assert receipt['provenance']['execution_component_key'] == 'dars'
    assert receipt['dataset']['id'] == 'synthetic:nov04b-dars-v1'


@pytest.mark.parametrize('key', sorted(REFERENCES))
def test_high_cost_reference_only_decisions_are_terminal_not_fake_implementations(key):
    records = [json.loads(path.read_text()) for path in
               (ROOT / 'src/auto_research/paper_specs/catalog').glob('*/*.json')]
    matches = [row for row in records if row['key'] == key]
    assert len(matches) == 1
    spec = matches[0]
    assert spec['implementation_status'] == 'deferred_high_cost'
    assert spec['full_experiment_status'] == 'not_reproduced_high_cost'
    assert spec['full_experiment_review_done'] and spec['review_done']
    assert spec['local_operator'] is None and spec['adapter'] is None
    assert not spec['requires_gpu_validation'] and not spec['gpu_validation_passed']
    assert not spec['promotion_eligible'] and not spec['evolve_integrated']
    assert not spec['automatic_retry'] and not spec['automatic_implementation_queue']
    assert spec['cost_assessment']['estimated_cost_basis']
    assert not (ROOT / 'docs' / Path(spec['detail_path']).parent / 'metrics').exists()


def test_two_bulletin_routes_have_actual_counts_without_claiming_full_review():
    coverage = load('source-coverage.json')
    assert coverage['actual_announced_on'] == '2026-11-04'
    assert coverage['review_watermark'] == {'before': '2026-10-15', 'after': '2026-10-15'}
    assert coverage['all_sources_exhaustive'] is False
    assert coverage['full_bulletin_full_text_review_complete'] is False
    assert coverage['review_watermark_advanced'] is False
    assert coverage['direct_and_parameterized_identities_equal'] is True
    receipts = [row for row in coverage['retrieval_receipts'] if row['kind'] == 'arxiv']
    assert len(receipts) == 16
    for query_route in (False, True):
        pages = [row for row in receipts if ('?' in row['url']) is query_route]
        assert len(pages) == 8
        assert {row['source']: row['parsed_entries'] for row in pages} == CATEGORY_COUNTS
        assert all(row['parse_complete'] and row['status'] == 'retrieved' for row in pages)
        assert all(row['parsed_entries'] == row['expected_entries'] for row in pages)
        assert all(row['announced_on'] == '2026-11-04' for row in pages)
    counts = coverage['counts']
    assert counts['category_entries_including_crosslists_and_replacements'] == 1472
    assert counts['unique_bulletin_identities'] == 1094
    assert counts['selected_papers'] == 14
    assert counts['component_implementations'] == 12
    assert counts['cuda_validated_components'] == counts['cpu_only_components'] == 6
    assert counts['reference_only_high_cost_review_done'] == 2
    assert counts['newly_announced_first_collections'] == 13
    assert counts['new_section_first_collections'] == 12
    assert counts['crosslisted_first_collections'] == 1
    assert counts['late_announced_backfills'] == 1
    assert counts['selected_first_publications_after_previous_capture'] == 0
    assert counts['full_capability_reproductions'] == 0
    priorities = {row['organization']: row for row in coverage['official_directory_status']}
    for name, attempted in [('Google', 30), ('Meta', 6)]:
        receipt = priorities[name]
        assert receipt['attempted_pages'] == attempted
        assert receipt['retrieved_pages'] == 0
        assert receipt['status'] == 'source_unavailable_not_zero_delta'
        assert receipt['delta_known'] is False and receipt['new_directory_urls'] is None


def test_fixed_delivery_scope_is_complete_but_does_not_erase_broader_unknowns():
    scope = load('task-scope.json')
    assert scope['selected_scope_complete'] is True
    assert scope['all_sources_exhaustive'] is False
    assert set(scope['fixed_component_keys']) == set(COMPONENTS)
    assert set(scope['reference_only_keys']) == REFERENCES
    assert len(scope['papers']) == 14
    runtime_tickets = next(row for row in scope['papers'] if row['key'] == 'runtime-tickets')
    assert runtime_tickets['intake_class'] == 'newly_crosslisted_first_collection'
    for paper in scope['papers']:
        component = paper['key'] in COMPONENTS
        assert paper['component_implemented'] is component
        assert paper['component_accepted'] is component
        assert paper['status'] == ('implemented' if component else 'deferred')
        assert paper['review_done'] and paper['full_experiment_review_done']
        assert paper['full_experiment_status'] == 'not_reproduced_high_cost'
        assert paper['verified_priority_organizations'] == []
        assert paper['promotion_eligible'] is False and paper['evolve_integrated'] is False
        assert paper['full_text_review']['full_article_read'] is False


def test_selected_papers_have_original_figures_and_four_specific_question_levels():
    scope = load('task-scope.json')
    manifest = json.loads((ROOT / 'docs/paper-figures-manifest.json').read_text())
    questions = {}
    for path in (ROOT / 'docs/learning/questions').glob('nov04b-*.json'):
        for identity, paper in json.loads(path.read_text())['papers'].items():
            assert identity not in questions
            questions[identity] = paper['questions']
    identities = {row['domain'] + ':' + row['key'] for row in scope['papers']}
    assert set(questions) == identities
    assert sum(len(rows) for rows in questions.values()) == 56
    for row in scope['papers']:
        page = 'docs/' + row['detail_path']
        matches = [figure for figure in manifest if figure['page'] == page]
        assert len(matches) == 1 and matches[0]['visually_inspected']
        assert matches[0]['sha256'] == hashlib.sha256(
            (ROOT / matches[0]['asset']).read_bytes()).hexdigest()
        assert '版权' in (ROOT / page).read_text()
        paper_questions = questions[row['domain'] + ':' + row['key']]
        assert {question['level'] for question in paper_questions} == {
            'basics', 'mechanism', 'comparison', 'implementation',
        }
        assert all(question['question'] and question['answer'] and question['example']
                   and question['source_sections'] for question in paper_questions)
