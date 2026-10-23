"""Bind four overlap components to immutable CPU/CUDA runs and exact claims."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
sys.path.insert(0, str(ROOT/'scripts'))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from build_oct24_source_audit import AUDIT_REL, BATCH, SELECTED  # noqa: E402
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_oct24_overlap_components import CUDA_KEYS, MODULES, RUNNER, SEEDS, SOURCES  # noqa: E402

AUDIT = ROOT/AUDIT_REL
OPERATORS = {'physical-engineering-exam': 'audit_artifacts', 'ttr-compressor': 'TTRCompressor',
             'userarena-optd': 'optd_loss', 'moer': 'moer_loss'}
CHECKS = {
    'physical-engineering-exam': {'declared_deliverable_usable', 'missing_task_not_usable', 'manifest_reward_not_a_grade',
        'hard_constraint_gate_caps_score', 'full_task_denominator_and_three_runs', 'blob_provenance_consistent', 'strict_reproduction_threshold'},
    'ttr-compressor': {'dual_matches_independent_primal', 'outer_a_gradient_eq9', 'outer_rho_gradient_eq9',
        'token_gradient_finite_nonzero', 'base_token_permutation_invariance', 'unnormalized_target_scale_response',
        'normalized_target_negative_control_differs', 'repeated_evidence_closed_form',
        'actual_outer_step_updates_both_parameters', 'outer_step_finite_nonincreasing_fixture_loss'},
    'userarena-optd': {'teacher_detached', 'formula_reference_matches', 'per_token_trust_budget',
        'zero_budget_recovers_unconditioned', 'bounded_jsd', 'finite_gradients', 'real_parameter_update',
        'separate_grounding_branch_updated', 'padding_gradient_zero', 'fixed_objective_decreases'},
    'moer': {'formula_reference_matches', 'gradient_reference_matches', 'old_policy_detached', 'rewards_detached',
        'finite_gradient', 'real_parameter_update', 'padding_zero_gradient', 'union_group_mean_no_std',
        'global_token_normalization', 'guided_completion_is_off_policy', 'trust_region_gradient_not_cancelled',
        'rollback_replaces_only_failed_candidate', 'cosine_schedule_endpoints'},
}
METRICS = {
    'physical-engineering-exam': {'contract_cases', 'model_calls', 'container_runs', 'external_commands'},
    'ttr-compressor': {'primal_dual_max_abs_error', 'a_gradient_max_abs_error', 'rho_gradient_max_abs_error',
        'permutation_max_abs_error', 'global_scale_max_abs_error', 'normalized_target_negative_control_gap',
        'repeated_evidence_max_abs_error', 'token_gradient_norm', 'outer_fixture_loss_before', 'outer_fixture_loss_after',
        'groups', 'tokens_per_group', 'dimension', 'outer_steps'},
    'userarena-optd': {'loss_before', 'loss_after', 'formula_reference_error', 'parameter_delta', 'max_teacher_kl',
        'max_lambda', 'distillation', 'grounding', 'optimizer_updates', 'model_calls'},
    'moer': {'loss_before', 'loss_after', 'gradient_norm', 'parameter_delta', 'formula_reference_error',
        'gradient_reference_error', 'valid_tokens', 'optimizer_updates', 'model_calls'},
}


def records():
    return {r['key']: r for r in catalog_records()}


def expected_command(key):
    module = MODULES[key].removeprefix('src/').removesuffix('.py').replace('/', '.')
    return f"PYTHONPATH=src python -c 'from {module} import diagnostic; print(diagnostic(42))'"


def metric_path(key):
    device = 'cuda' if key in CUDA_KEYS else 'cpu'
    return Path('docs')/Path(records()[key]['detail_path']).parent/f'metrics/component-{device}-seeds42-44.json'


def validate_catalog(catalog):
    for key, (domain, paper_id) in SELECTED.items():
        row = catalog[key]
        require(row['domain'] == domain and row['paper_url'] == f'https://arxiv.org/abs/{paper_id}v1'
            and row['detail_path'] == f'{domain}/{paper_id}-{key}/README.md'
            and row.get('adapter') is None and row.get('implementation_status') == 'component_only'
            and row.get('evaluation_tier') == 'l1_mechanism' and row.get('diagnostic_only') is True
            and row.get('promotion_eligible') is False and row.get('evolve_integrated') is False
            and row.get('review_done') is True and row.get('full_experiment_review_done') is True
            and row.get('full_experiment_status') == 'not_reproduced_high_cost'
            and row.get('automatic_retry') is False and row.get('automatic_implementation_queue') is False,
            f'{key}: catalog boundary')
        receipt = f'docs/gpu-validations/{key}-a100-20261024.json' if key in CUDA_KEYS else None
        require(row.get('requires_gpu_validation') is (key in CUDA_KEYS) and row.get('gpu_validation_artifact') == receipt,
                f'{key}: catalog GPU boundary')
        module = MODULES[key].removeprefix('src/').removesuffix('.py').replace('/', '.')
        require(row.get('local_operator') == module+'.'+OPERATORS[key]
            and row.get('local_command') == expected_command(key), f'{key}: executed-entry binding')


def gates(key, rows):
    require([r['seed'] for r in rows] == SEEDS, 'exact three seeds')
    for row in rows:
        require(set(row['checks']) == CHECKS[key] and all(v is True for v in row['checks'].values()), f'{key}: defining checks')
        m = row['metrics']
        require(set(m) == METRICS[key], f'{key}: metric schema')
        if key == 'physical-engineering-exam':
            require(m['contract_cases'] == 7 and m['model_calls'] == m['container_runs'] == m['external_commands'] == 0, 'PLE protocol only')
        elif key == 'ttr-compressor':
            require(max(m[n] for n in ('primal_dual_max_abs_error', 'permutation_max_abs_error', 'global_scale_max_abs_error',
                'repeated_evidence_max_abs_error')) < 2e-5 and max(m['a_gradient_max_abs_error'], m['rho_gradient_max_abs_error']) < 2e-4
                and m['normalized_target_negative_control_gap'] > 1e-3 and m['token_gradient_norm'] > 0
                and m['groups'] == 4 and m['tokens_per_group'] == 7 and m['dimension'] == 12 and m['outer_steps'] == 1
                and m['outer_fixture_loss_after'] <= m['outer_fixture_loss_before'] + 1e-6, 'TTR exact references/update')
        else:
            require(m['formula_reference_error'] < 1e-10 and m['parameter_delta'] > 0
                and m['optimizer_updates'] == 1 and m['model_calls'] == 0, f'{key}: formula/update')
            if key == 'userarena-optd':
                require(m['max_teacher_kl'] <= .02 + 1e-12 and 0 <= m['max_lambda'] <= 1
                    and m['loss_after'] < m['loss_before'] and -1e-12 <= m['distillation'] <= .69314718056 + 1e-12,
                    'OPTD trust region and fixed objective')
            else:
                require(m['gradient_reference_error'] < 1e-10 and m['valid_tokens'] == 17 and m['gradient_norm'] > 0, 'MOER gradient/normalization')
    aggregate(rows)


def validate_raw(raw):
    for device, item in raw.items():
        require(item['schema_version'] == 2 and item['device'] == device and item['seeds'] == SEEDS
            and set(item['components']) == (set(MODULES) if device == 'cpu' else CUDA_KEYS)
            and item['evaluation_tier'] == 'l1_mechanism' and item['diagnostic_only'] is True
            and item['formal_comparison'] is False and item['promotion_eligible'] is False
            and item['evolve_integrated'] is False and item['pretrained_model_calls'] == 0
            and item['full_experiments_executed'] is False, 'raw scope boundary')
        require(item['accelerator'] == 'CPU' if device == 'cpu' else any(n in item['accelerator'] for n in ('A100', 'A30')), 'raw device')
        require(set(item['source_sha256']) == set(SOURCES), 'source scope')
        for key, value in item['components'].items():
            require(all(row.get('execution_device') == device and row.get('execution_accelerator') == item['accelerator']
                for row in value['per_seed']), f'{key}: per-seed execution device binding')
            gates(key, value['per_seed'])
    require(raw['cpu']['code_commit'] == raw['cuda']['code_commit'] and raw['cpu']['source_sha256'] == raw['cuda']['source_sha256'], 'CPU/CUDA frozen identity')


def validate_scope(scope, batch, catalog, *, allow_pending=False):
    require(scope.get('batch') == batch.get('batch') == BATCH and set(scope['fixed_component_keys']) == set(MODULES)
        and scope['reference_only_keys'] == [], 'scope batch identity')
    complete = scope.get('selected_scope_complete')
    require(type(complete) is bool and batch.get('selected_scope_complete') is complete
        and scope.get('delivery_status') == batch.get('delivery_status') == ('bounded_scope_complete' if complete else 'pending_component_verification')
        and (complete or allow_pending), 'scope/ledger completion-state binding')
    if complete:
        require(scope.get('component_count') == 4 and scope.get('gpu_validated_component_count') == 3
            and scope.get('capability_reproductions_claimed') == 0
            and batch['counts'].get('components_accepted') == 4
            and batch['counts'].get('components_pending_verification') == 0, 'scope/ledger completion counts')
    for rows in (scope['papers'], batch['candidates']):
        require(len(rows) == len(MODULES) and {r['key'] for r in rows} == set(MODULES), 'scope/ledger exact paper set')
        for row in rows:
            item = catalog[row['key']]
            domain, paper_id = SELECTED[row['key']]
            require(row['domain'] == domain and row['id'] == paper_id and row['paper_url'] == item['paper_url']
                and row['original_published_at'] == item['published_at']
                and all(row[f] == item[f] for f in ('title', 'detail_path', 'first_author', 'first_author_affiliation'))
                and row['full_experiment_status'] == 'not_reproduced_high_cost' and row['full_experiment_review_done'] is True
                and row['requires_gpu_validation'] is (row['key'] in CUDA_KEYS)
                and row['automatic_retry'] is False and row['automatic_implementation_queue'] is False
                and row['promotion_eligible'] is False and row['evolve_integrated'] is False,
                'scope/ledger identity or claim')
            if rows is batch['candidates']:
                require(row.get('doc') == row.get('catalog_detail') == item['detail_path']
                    and row.get('catalog_key') == row['key'], 'scope/ledger canonical alias binding')
            if complete:
                require(row['component_accepted'] is True and row['component_implemented'] is True and row['review_done'] is True
                    and row['implementation_status'] == 'component_only'
                    and row['component_evidence'] == metric_path(row['key']).as_posix(), 'scope/ledger acceptance')
            else:
                require(row['component_accepted'] is False and row['component_implemented'] is False
                    and row['implementation_status'] == 'component_validation_pending', 'scope/ledger pending boundary')


def result_for(key, raw, raw_bytes):
    device = 'cuda' if key in CUDA_KEYS else 'cpu'
    item = raw[device]
    dataset = {'id': f'synthetic:oct24-{key}-v1', 'revision': 'sha256:'+digest(item['source_sha256']),
        'recipe': 'seeded-frozen-source-mechanism-contracts', 'capability_benchmark': False}
    rows = item['components'][key]['per_seed']
    return {'schema_version': 2, 'method': key, 'manifest_ref': records()[key]['domain']+':'+key,
        'dataset': dataset, 'seeds': SEEDS, 'per_seed': rows, 'metrics': aggregate(rows),
        'evaluation_tier': 'l1_mechanism', 'evaluation_protocol': {'tier': 'l1_mechanism', 'seeds': SEEDS,
            'formal_comparison': False, 'claim_policy': 'mechanism/protocol diagnostics; not pretrained capability or full reproduction'},
        'diagnostic_only': True, 'fixture_demo': True, 'formal_comparison': False,
        'promotion_eligible': False, 'evolve_integrated': False, 'pretrained_model_calls': 0,
        'full_experiment_status': 'not_reproduced_high_cost', 'full_experiment_review_done': True,
        'provenance': {'commit': item['code_commit'], 'artifact_path': metric_path(key).as_posix(),
            'accelerator': item['accelerator'], 'executed_source_sha256': item['source_sha256'],
            'raw_runner_artifact_sha256': hashlib.sha256(raw_bytes[device]).hexdigest(),
            'dataset_fingerprint': 'sha256:'+digest({'dataset': dataset, 'seeds': SEEDS, 'source': item['source_sha256']})}}


def receipt_for(key, result):
    provenance = result['provenance']
    path = records()[key]['gpu_validation_artifact']
    return {'schema_version': 1, 'adapter_key': key, 'validated_at': '2026-10-24',
        'accelerator': {'vendor': 'NVIDIA', 'model': provenance['accelerator'], 'count': 1},
        'command': ['python3', RUNNER, '--device', 'cuda', '--source-commit', provenance['commit'],
            '--frozen-proof', 'oct24-frozen-proof.json', '--output', 'results/components-cuda.json'],
        'dataset': result['dataset'], 'checkpoint': {'public_id': 'none-seeded-component-initialization', 'revision': provenance['commit'], 'pretrained': False},
        'seeds': SEEDS, 'result': 'passed', 'metrics': result['metrics'], 'executed_source_sha256': provenance['executed_source_sha256'],
        'provenance': {**provenance, 'artifact_path': path, 'metric_artifact_path': metric_path(key).as_posix()},
        'diagnostic_only': True, 'promotion_eligible': False, 'evolve_integrated': False,
        'full_experiment_status': 'not_reproduced_high_cost', 'full_experiment_review_done': True}


def ingest(cpu, cuda):
    validate_catalog(records())
    raw_bytes = {'cpu': cpu.read_bytes(), 'cuda': cuda.read_bytes()}
    raw = {d: json.loads(b) for d, b in raw_bytes.items()}
    validate_raw(raw)
    proof = capture_sources(ROOT, raw['cpu']['code_commit'], SOURCES)
    verify_sources(ROOT, raw['cpu']['code_commit'], raw['cpu']['source_sha256'], proof)
    for key in MODULES:
        result = result_for(key, raw, raw_bytes)
        write(ROOT/metric_path(key), result)
        if key in CUDA_KEYS:
            write(ROOT/records()[key]['gpu_validation_artifact'], receipt_for(key, result))
    write(AUDIT/'frozen-sources.json', {'schema_version': 1, 'commit': raw['cpu']['code_commit'], 'proof': proof})
    for device, data in raw_bytes.items():
        (AUDIT/f'raw-{device}.json').write_bytes(data)


def check(*, allow_pending=False):
    catalog = records()
    validate_catalog(catalog)
    raw_bytes = {d: (AUDIT/f'raw-{d}.json').read_bytes() for d in ('cpu', 'cuda')}
    raw = {d: json.loads(b) for d, b in raw_bytes.items()}
    validate_raw(raw)
    frozen = json.loads((AUDIT/'frozen-sources.json').read_text())
    require(frozen['commit'] == raw['cpu']['code_commit'], 'frozen commit binding')
    verify_sources(ROOT, frozen['commit'], raw['cpu']['source_sha256'], frozen['proof'])
    for key in MODULES:
        result = json.loads((ROOT/metric_path(key)).read_text())
        require(result == result_for(key, raw, raw_bytes), f'{key}: exact raw/result binding')
        if key in CUDA_KEYS:
            require(load_gpu_receipt(ROOT/catalog[key]['gpu_validation_artifact']) == receipt_for(key, result), f'{key}: receipt binding')
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    batches = [b for b in json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())['batches'] if b['batch'] == BATCH]
    require(len(batches) == 1, 'exactly one batch')
    validate_scope(scope, batches[0], catalog, allow_pending=allow_pending)


def finalize():
    check(allow_pending=True)
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    ledger_path = ROOT/'docs/paper-discovery-ledger.json'
    ledger = json.loads(ledger_path.read_text())
    batch = next(b for b in ledger['batches'] if b['batch'] == BATCH)
    for rows in (scope['papers'], batch['candidates']):
        for row in rows:
            row.update(status='implemented', implementation_status='component_only', component_implemented=True,
                component_accepted=True, review_done=True, delivery_status='bounded_component_accepted',
                component_evidence=metric_path(row['key']).as_posix(), resolution='bounded_l1_component_accepted',
                reason='四项冻源三种子L1验收，三个张量组件真实A100执行；高成本完整实验不复现，不宣称能力。')
            if row['key'] in CUDA_KEYS:
                row['gpu_validation_artifact'] = records()[row['key']]['gpu_validation_artifact']
    coverage['counts'].update(components_pending_verification=0, components_pending_gpu_and_integration=0,
        components_accepted=4, gpu_validated_components=3, capability_reproductions_claimed=0)
    scope.update(selected_scope_complete=True, delivery_status='bounded_scope_complete', component_count=4,
        gpu_validated_component_count=3, capability_reproductions_claimed=0)
    coverage['delivery_status'] = 'bounded_scope_complete'
    coverage['limitations'] = [line.replace('Four L1 components require frozen execution and integration before acceptance',
        'Four L1 components passed frozen execution and integration; three ran on real A100') for line in coverage['limitations']]
    batch.update(selected_scope_complete=True, delivery_status='bounded_scope_complete', counts=coverage['counts'])
    validate_scope(scope, batch, records())
    for path, item in ((AUDIT/'task-scope.json', scope), (AUDIT/'source-coverage.json', coverage), (ledger_path, ledger)):
        write(path, item)


def sync_figures():
    from PIL import Image

    path = ROOT/'docs/paper-figures-manifest.json'
    rows = json.loads(path.read_text())
    for key, (_, paper_id) in SELECTED.items():
        record = records()[key]
        page = Path('docs')/record['detail_path']
        assets = page.parent/'assets'
        p = json.loads((ROOT/assets/'provenance.json').read_text())
        asset = assets/p.get('image', p.get('local_path', 'paper-figure-01.png'))
        source = p.get('source_url', p.get('source_image_url', p.get('paper_url')))
        require(source and source.startswith('https://'), 'original figure source')
        with Image.open(ROOT/asset) as im:
            width, height = im.size
        row = {'page': page.as_posix(), 'paper_url': record['paper_url'], 'arxiv_id': paper_id,
            'figure': str(p.get('figure', 'Figure 1')), 'original_caption': p.get('original_caption', ''),
            'source_url': source, 'extraction': 'original-reviewed-paper-figure', 'asset': asset.as_posix(),
            'width': width, 'height': height, 'score': 0, 'error': '',
            'sha256': hashlib.sha256((ROOT/asset).read_bytes()).hexdigest(), 'visually_inspected': True}
        existing = [i for i, old in enumerate(rows) if old['page'] == row['page']]
        require(len(existing) <= 1, 'duplicate figure page')
        if existing:
            rows[existing[0]] = row
        else:
            rows.append(row)
    write(path, rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cpu', type=Path)
    parser.add_argument('--cuda', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--finalize', action='store_true')
    parser.add_argument('--sync-figures', action='store_true')
    args = parser.parse_args()
    if args.cpu and args.cuda:
        ingest(args.cpu, args.cuda)
    if args.check:
        check()
    if args.finalize:
        finalize()
    if args.sync_figures:
        sync_figures()
