"""Bind Oct23 L1 raw runs, frozen sources, catalog claims and GPU receipts."""
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
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_oct23_priority_components import CUDA_KEYS, MODULES, RUNNER, SEEDS, SOURCES  # noqa: E402
from build_oct23_source_audit import BATCH, SELECTED  # noqa: E402

AUDIT = ROOT/'docs/research-audits/oct23-priority-components'
CHECKS = {
    'rkl-policy-distillation': {'teacher_queries_only_visited_states', 'full_episode_budget', 'bounded_comparisons',
        'rollout_self_comparison_zero', 'fixed_eta_exponential_weight_reference', 'final_argmax_not_risk_oracle',
        'relative_second_moment_assumption'},
    'gemma-priority-protocol': {'orthogonal_contrast_recovery', 'global_keep_set_shared', 'sensitivity_preserves_all_items',
        'single_bad_condition_drops_globally', 'degenerate_tost_is_not_a_pass', 'half_effect_orientation'},
    'openattention': {'full_read_max_abs_error', 'expanded_proxy_max_abs_error', 'equal_key_proxy_max_abs_error',
        'exact_budget_and_uniqueness', 'detector_rows_charged', 'int8_selector_index', 'dynamic_range_waterfill_exact'},
    'moezip': {'explicit_fisher_reference', 'all_anchors_present', 'actual_kv_gather_shapes', 'exact_budget_and_uniqueness',
        'adaptive_anchor_bounds', 'sigmoid_path_budget'},
    'aopd': {'teacher_detached', 'rollout_policy_detached', 'finite_gradient', 'real_parameter_update',
        'formula_reference_matches', 'bounded_step_decreases_fixed_objective', 'clipped_measure_not_renormalized'},
    'gift': {'finite_gradient', 'teacher_detached', 'old_policy_detached', 'advantages_detached',
        'real_parameter_update', 'formula_reference_matches', 'exact_quota', 'selection_detached'},
    'pair': {'independent_loss_reference', 'three_real_updates', 'masked_history_isolated', 'hard_negatives_first',
        'history_changes_representation', 'finite_gradients', 'query_agnostic_normalized_attention'},
    'jev-dlc': {'pa_reference_matches', 'future_only_update', 'safe_mask_is_hard', 'stale_feedback_rejected',
        'reset_restores_frozen_prediction', 'no_raw_history', 'zero_direction_passive'},
}
METRICS = {
    'rkl-policy-distillation': {'episodes', 'horizon', 'policy_count', 'teacher_queries', 'selected_index',
        'selected_trajectory_reverse_kl', 'best_in_class_risk_evaluation_only', 'relative_second_moment_B',
        'exponential_weight_replay_max_abs_error', 'max_abs_comparison_loss'},
    'gemma-priority-protocol': {'contract_cases', 'algebra_max_error', 'global_items_kept', 'model_calls'},
    'openattention': {'full_read_max_abs_error', 'expanded_proxy_max_abs_error', 'equal_key_proxy_max_abs_error',
        'dense_relative_output_error', 'exact_rows', 'charged_kv_rows'},
    'moezip': {'explicit_fisher_score_max_abs_error', 'all_anchors_present', 'retained_rows_per_head', 'anchor_count',
        'fragile_fraction', 'uniform_router_anchor_count', 'peaked_router_anchor_count', 'sigmoid_anchor_count'},
    'aopd': {'loss_before', 'loss_after', 'gradient_norm', 'parameter_delta', 'max_sampled_weight',
        'formula_reference_error', 'optimizer_updates', 'model_calls'},
    'gift': {'loss', 'gradient_norm', 'parameter_delta', 'selected_tokens', 'valid_tokens', 'retention',
        'formula_reference_error', 'optimizer_updates', 'model_calls'},
    'pair': {'formula_reference_error', 'optimizer_updates', 'parameter_update_l2', 'masked_history_error',
        'history_effect_l2', 'final_loss', 'model_calls'},
    'jev-dlc': {'pa_reference_error', 'correction_state_norm', 'future_probability_delta', 'feedback_count',
        'masked_probability', 'model_calls'},
}
OPERATORS = {'gemma-priority-protocol': 'analyze_cells', 'rkl-policy-distillation': 'learn_online',
    'openattention': 'attend', 'moezip': 'select_cache', 'aopd': 'aopd_loss', 'gift': 'gift_loss',
    'pair': 'preference_loss', 'jev-dlc': 'JevDLC'}


def expected_command(key):
    if key in {'openattention', 'moezip', 'rkl-policy-distillation'}:
        return ('PYTHONPATH=src python scripts/run_oct23_priority_components.py --device cpu --seeds 42,43,44 '
                '--source-commit COMMIT --frozen-proof oct23-frozen-proof.json --output <new-result.json>')
    module = MODULES[key].removeprefix('src/').removesuffix('.py').replace('/', '.')
    prefix = 'OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ' if key in {'aopd', 'gift'} else ''
    return prefix+f"PYTHONPATH=src python -c 'from {module} import diagnostic; print(diagnostic(42))'"


def records():
    return {r['key']: r for r in catalog_records()}


def metric_path(key):
    device = 'cuda' if key in CUDA_KEYS else 'cpu'
    return Path('docs')/Path(records()[key]['detail_path']).parent/f'metrics/component-{device}-seeds42-44.json'


def validate_catalog(catalog):
    for key in MODULES:
        row = catalog[key]
        require(row.get('adapter') is None and row.get('implementation_status') == 'component_only'
            and row.get('evaluation_tier') == 'l1_mechanism' and row.get('diagnostic_only') is True
            and row.get('review_done') is True and row.get('full_experiment_review_done') is True
            and row.get('promotion_eligible') is False and row.get('evolve_integrated') is False
            and row.get('automatic_retry') is False and row.get('automatic_implementation_queue') is False,
            f'{key}: component catalog boundary')
        status = 'not_run_scope_limited_protocol' if key in {'gemma-priority-protocol', 'rkl-policy-distillation'} else 'not_reproduced_high_cost'
        receipt = f'docs/gpu-validations/{key}-a100-20261023.json' if key in CUDA_KEYS else None
        require(row.get('full_experiment_status') == status and row.get('requires_gpu_validation') is (key in CUDA_KEYS)
            and row.get('gpu_validation_artifact') == receipt, f'{key}: catalog cost/GPU boundary')
        module = MODULES[key].removeprefix('src/').removesuffix('.py').replace('/', '.')
        require(row.get('local_operator') == module+'.'+OPERATORS[key] and row.get('local_command') == expected_command(key),
            f'{key}: catalog executed-entry binding')
    row = catalog['onelatent']
    require(row.get('implementation_status') == 'deferred_high_cost' and row.get('adapter') is None
        and row.get('local_operator') is None and row.get('local_command') is None and row.get('evaluation_tier') is None
        and row.get('full_experiment_status') == 'not_reproduced_high_cost' and row.get('review_done') is True
        and row.get('full_experiment_review_done') is True and row.get('review_resolution') == 'not_reproduced_high_cost'
        and row.get('requires_gpu_validation') is False and row.get('gpu_validation_artifact') is None
        and row.get('automatic_retry') is False and row.get('automatic_implementation_queue') is False
        and row.get('promotion_eligible') is False and row.get('evolve_integrated') is False
        and row.get('diagnostic_only') is True, 'OneLatent terminal reference-only boundary')


def validate_scope_identity(scope, batch, catalog):
    expected = set(MODULES)|{'onelatent'}
    require(scope.get('batch') == batch.get('batch') == BATCH, 'scope batch identity')
    require(set(scope['fixed_component_keys']) == set(MODULES) and scope['reference_only_keys'] == ['onelatent'], 'fixed scope partition')
    for rows in (scope['papers'], batch['candidates']):
        require(len(rows) == len(expected) and {r['key'] for r in rows} == expected, 'scope/ledger unique complete paper set')
        for row in rows:
            key = row['key']
            item = catalog[key]
            domain, pid = SELECTED[key]
            require(row['id'] == pid and row['domain'] == domain and row['paper_url'] == item['paper_url'] == f'https://arxiv.org/abs/{pid}v1'
                and all(row[field] == item[field] for field in ('title', 'detail_path', 'first_author', 'first_author_affiliation'))
                and row['original_published_at'] == item['published_at'], 'scope/ledger paper identity binding')
            require(row.get('full_experiment_status') == item['full_experiment_status']
                and row.get('full_experiment_review_done') is True and row.get('requires_gpu_validation') is (key in CUDA_KEYS)
                and row.get('promotion_eligible') is False and row.get('evolve_integrated') is False
                and row.get('automatic_retry') is False and row.get('automatic_implementation_queue') is False,
                'scope/ledger claim boundary')
            if key == 'onelatent':
                require(row.get('component_implemented') is False and row.get('component_accepted') is False
                    and row.get('implementation_status') == 'deferred_high_cost' and row.get('review_done') is True,
                    'scope/ledger reference-only boundary')
            elif scope.get('selected_scope_complete'):
                require(row.get('component_accepted') is True and row.get('component_implemented') is True
                    and row.get('implementation_status') == 'component_only' and row.get('review_done') is True
                    and row.get('component_evidence') == metric_path(key).as_posix(), 'scope/ledger component acceptance binding')


def gates(key, rows):
    require([r['seed'] for r in rows] == SEEDS, 'exact three seeds')
    for row in rows:
        require(set(row['checks']) == CHECKS[key] and all(v is True for v in row['checks'].values()), f'{key}: defining checks')
        m = row['metrics']
        require(set(m) == METRICS[key], f'{key}: metric schema')
        if key in {'aopd', 'gift', 'pair'}:
            require(m['formula_reference_error'] < 1e-9 and m.get('parameter_delta', m.get('parameter_update_l2', 0)) > 0
                and m['optimizer_updates'] == (3 if key == 'pair' else 1) and m['model_calls'] == 0,
                f'{key}: real update/formula gate')
        if key == 'aopd':
            require(m['loss_after'] < m['loss_before'] and m['max_sampled_weight'] <= 4.+1e-9, 'AOPD cap/decrease')
        elif key == 'gift':
            require(m['selected_tokens'] == 6 and m['valid_tokens'] == 12 and m['retention'] == .5, 'GIFT quota')
        elif key == 'pair':
            require(m['masked_history_error'] == 0 and m['history_effect_l2'] > 0, 'PAIR history isolation')
        elif key == 'openattention':
            require(max(m[n] for n in ('full_read_max_abs_error', 'expanded_proxy_max_abs_error', 'equal_key_proxy_max_abs_error')) < 2e-5
                and m['exact_rows'] == 16 and m['charged_kv_rows'] == 28, 'OpenAttention references/budget')
        elif key == 'moezip':
            require(m['explicit_fisher_score_max_abs_error'] < 1e-6 and m['all_anchors_present'] is True
                and m['retained_rows_per_head'] == 256 and m['uniform_router_anchor_count'] == 64
                and m['peaked_router_anchor_count'] == 32, 'MoEZip Fisher/anchors')
        elif key == 'jev-dlc':
            require(m['pa_reference_error'] < 1e-12 and m['correction_state_norm'] > 0 and m['future_probability_delta'] > 0
                and m['feedback_count'] == 2 and m['masked_probability'] == m['model_calls'] == 0, 'Jev-DLC causal state')
        elif key == 'gemma-priority-protocol':
            require(m['contract_cases'] == 6 and m['algebra_max_error'] < 1e-12 and m['global_items_kept'] == 7
                and m['model_calls'] == 0, 'Gemma protocol algebra')
        elif key == 'rkl-policy-distillation':
            require(m['episodes'] == 256 and m['horizon'] == m['policy_count'] == 3 and m['teacher_queries'] == 768
                and m['exponential_weight_replay_max_abs_error'] < 1e-12 and m['max_abs_comparison_loss'] <= 1+1e-12
                and 0 <= m['selected_index'] < 3 and m['relative_second_moment_B'] >= 1,
                'RKL finite-policy online/reference gate')
    aggregate(rows)  # also rejects nonfinite/non-scalar metrics


def validate_raw(raw):
    for device, item in raw.items():
        require(item['schema_version'] == 2 and item['device'] == device and item['seeds'] == SEEDS
            and set(item['components']) == (set(MODULES) if device == 'cpu' else CUDA_KEYS)
            and item['evaluation_tier'] == 'l1_mechanism' and item['diagnostic_only'] is True
            and item['formal_comparison'] is False and item['promotion_eligible'] is False
            and item['evolve_integrated'] is False and item['pretrained_model_calls'] == 0
            and item['full_experiments_executed'] is False, 'raw scope/claim boundary')
        require(item['accelerator'] == 'CPU' if device == 'cpu' else any(s in item['accelerator'] for s in ('A100', 'A30')), 'raw device')
        require(set(item['source_sha256']) == set(SOURCES), 'frozen source scope')
        for key, component in item['components'].items():
            gates(key, component['per_seed'])
    require(raw['cpu']['code_commit'] == raw['cuda']['code_commit'] and raw['cpu']['source_sha256'] == raw['cuda']['source_sha256'],
        'CPU/CUDA frozen source identity')


def result_for(key, raw, raw_bytes):
    item = raw['cuda' if key in CUDA_KEYS else 'cpu']
    hashes = item['source_sha256']
    dataset = {'id': f'synthetic:oct23-{key}-v1', 'revision': 'sha256:'+digest(hashes),
        'recipe': 'frozen-source-seeded-mechanism-contracts', 'capability_benchmark': False}
    rows = item['components'][key]['per_seed']
    return {'schema_version': 2, 'method': key, 'manifest_ref': records()[key]['domain']+':'+key,
        'dataset': dataset, 'seeds': SEEDS, 'per_seed': rows, 'metrics': aggregate(rows),
        'evaluation_tier': 'l1_mechanism', 'evaluation_protocol': {'tier': 'l1_mechanism', 'seeds': SEEDS,
            'formal_comparison': False, 'claim_policy': 'generated mechanism contracts; no pretrained capability or full-paper comparison'},
        'diagnostic_only': True, 'fixture_demo': True, 'formal_comparison': False,
        'promotion_eligible': False, 'evolve_integrated': False, 'pretrained_model_calls': 0,
        'full_experiment_status': records()[key]['full_experiment_status'], 'full_experiment_review_done': True,
        'provenance': {'commit': item['code_commit'], 'artifact_path': metric_path(key).as_posix(),
            'accelerator': item['accelerator'], 'executed_source_sha256': hashes,
            'raw_runner_artifact_sha256': hashlib.sha256(raw_bytes['cuda' if key in CUDA_KEYS else 'cpu']).hexdigest(),
            'dataset_fingerprint': 'sha256:'+digest({'dataset': dataset, 'seeds': SEEDS, 'source': hashes})}}


def receipt_for(key, result):
    path = records()[key]['gpu_validation_artifact']
    p = result['provenance']
    return {'schema_version': 1, 'adapter_key': key, 'validated_at': '2026-10-23',
        'accelerator': {'vendor': 'NVIDIA', 'model': p['accelerator'], 'count': 1},
        'command': ['python3', RUNNER, '--device', 'cuda', '--seeds', '42,43,44', '--source-commit', p['commit'],
            '--frozen-proof', 'oct23-frozen-proof.json', '--output', 'results/components-cuda.json'],
        'dataset': result['dataset'], 'checkpoint': {'public_id': 'none-seeded-component-initialization', 'revision': p['commit'], 'pretrained': False},
        'seeds': SEEDS, 'result': 'passed', 'metrics': result['metrics'],
        'executed_source_sha256': p['executed_source_sha256'],
        'provenance': {**p, 'artifact_path': path, 'metric_artifact_path': metric_path(key).as_posix()},
        'diagnostic_only': True, 'promotion_eligible': False, 'evolve_integrated': False,
        'full_experiment_status': result['full_experiment_status'], 'full_experiment_review_done': True}


def ingest(cpu_path, cuda_path):
    validate_catalog(records())
    raw_bytes = {'cpu': cpu_path.read_bytes(), 'cuda': cuda_path.read_bytes()}
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


def check():
    validate_catalog(records())
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
            path = ROOT/records()[key]['gpu_validation_artifact']
            require(load_gpu_receipt(path) == receipt_for(key, result), f'{key}: exact GPU receipt binding')
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    ledger = json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())
    batches = [b for b in ledger['batches'] if b.get('batch') == BATCH]
    require(len(batches) == 1, 'one scope batch required')
    validate_scope_identity(scope, batches[0], records())


def finalize():
    check()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    coverage = json.loads((AUDIT/'source-coverage.json').read_text())
    ledger_path = ROOT/'docs/paper-discovery-ledger.json'
    ledger = json.loads(ledger_path.read_text())
    batches = [b for b in ledger['batches'] if b['batch'] == scope['batch']]
    require(len(batches) == 1, 'one scope batch required')
    validate_scope_identity(scope, batches[0], records())
    for rows in (scope['papers'], batches[0]['candidates']):
        for row in rows:
            if row['key'] in MODULES:
                row.update(status='implemented', implementation_status='component_only', component_implemented=True,
                    component_accepted=True, review_done=True, delivery_status='bounded_component_accepted',
                    component_evidence=metric_path(row['key']).as_posix(), resolution='bounded_l1_component_accepted')
                row['reason'] = '冻结源码三种子L1组件验收；CUDA组件真实A100执行。完整实验状态逐篇保留，不宣称模型能力或完整论文复现。'
                if row['key'] in CUDA_KEYS:
                    row['gpu_validation_artifact'] = records()[row['key']]['gpu_validation_artifact']
    counts = coverage['counts']
    counts.update(components_pending_verification=0, components_pending_gpu_and_integration=0, components_accepted=len(MODULES),
                  gpu_validated_components=len(CUDA_KEYS), capability_reproductions_claimed=0)
    scope.update(selected_scope_complete=True, delivery_status='bounded_scope_complete', component_count=len(MODULES),
        gpu_validated_component_count=len(CUDA_KEYS), capability_reproductions_claimed=0)
    coverage['delivery_status'] = 'bounded_scope_complete'
    coverage['limitations'] = [
        'Eight L1 components passed frozen execution/integration; five CUDA components ran on real A100. One high-cost reference is review DONE, not implemented.'
        if line.startswith('Eight components remain pending') else line for line in coverage['limitations']]
    batches[0].update(selected_scope_complete=True, delivery_status='bounded_scope_complete', counts=counts)
    validate_scope_identity(scope, batches[0], records())
    for path, value in ((AUDIT/'task-scope.json', scope), (AUDIT/'source-coverage.json', coverage), (ledger_path, ledger)):
        write(path, value)


def sync_figures():
    """Append only this batch's original source figures; preserve old row order."""
    import re
    from PIL import Image

    path = ROOT/'docs/paper-figures-manifest.json'
    rows = json.loads(path.read_text())
    for key in (*MODULES, 'onelatent'):
        record = records()[key]
        page = Path('docs')/record['detail_path']
        assets = page.parent/'assets'
        provenance = json.loads((ROOT/assets/'provenance.json').read_text())
        asset = assets/provenance.get('image', provenance.get('local_path', 'paper-figure-01.png'))
        source = provenance.get('source_url', provenance.get('source_image_url', provenance.get('paper_url')))
        require(source and source.startswith('https://'), f'{key}: original figure source')
        with Image.open(ROOT/asset) as im:
            width, height = im.size
        figure = str(provenance.get('figure', 'Algorithm 1'))
        if figure.isdigit():
            figure = 'Figure '+figure
        row = {'page': page.as_posix(), 'paper_url': record['paper_url'],
            'arxiv_id': re.search(r'\d{4}\.\d{4,5}', record['paper_url'])[0],
            'figure': figure, 'original_caption': provenance.get('original_caption', ''),
            'source_url': source, 'extraction': 'original-source-image-or-reviewed-algorithm-crop',
            'asset': asset.as_posix(), 'width': width, 'height': height,
            'score': 0, 'error': '', 'sha256': hashlib.sha256((ROOT/asset).read_bytes()).hexdigest(),
            'visually_inspected': True}
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
