from copy import deepcopy
import importlib.util
from pathlib import Path
import json

import pytest

SOURCE = Path(__file__).resolve().parents[2] / 'scripts/curate_vcola_evidence.py'
spec = importlib.util.spec_from_file_location('curate_vcola_evidence', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def report():
    rows = []
    for recipe, merged in zip(module.RECIPES, (8, 4, 2), strict=True):
        compressed = recipe != 'dense'
        layers = [{'layer': i, 'visual_tokens': 8 if i == 1 or not compressed else merged if i <= 24 else 0,
                   'sequence_tokens': 10 + (8 if i == 1 or not compressed else merged if i <= 24 else 0)}
                  for i in range(1, 33)]
        rows.append({'sampling_seed': 42, 'example_id': 499,
            'recipe': recipe, 'restricted_first_token_correct': not compressed,
            'restricted_choice_probability_mass': .3, 'restricted_choice_kl_to_dense': .2 if compressed else 0.,
            'dense_backend_relative_error': .001, 'forward': {'layers': layers,
                'recurrence_relative_error': .001, 'cache_used': False,
                'original_text_positions_preserved': True, 'importance_mean': .5,
                'uniqueness_mean': .4, 'score_std': .03,
                'merge': {'original_visual_tokens': 8, 'merged_visual_tokens': merged,
                          'chunk_sizes': [8 // merged] * merged} if compressed else None}})
    return {'adapter_key': 'vcola', 'diagnostic_only': True, 'evaluation_tier': 'l1_core_mechanism',
        'protocol': {'first_layer_real_delta_state_capture': True, 'state_scores_not_feature_proxy': True,
            'query_probe_window': [0, 4], 'uniqueness_weight': .1, 'merge_temperature': 1., 'exit_layer': 24,
            'text_original_mrope_preserved': True, 'no_cache_reference_backend': True,
            'prefill_speedup_claim': False, 'full_generated_answer_accuracy': False,
            'inference_gold_read': False, 'restricted_first_token_only': True,
            'test_read': False, 'sampling_seeds_not_training_replicates': True},
        'checkpoint': {'id': 'Qwen/Qwen3.5-9B', 'revision': module.REVISION},
        'datasets': [{'id': 'CIFAR-10', 'test_read': False,
            'revision': {f'data_batch_{i}': 'b' * 64 for i in range(1, 6)},
            'split': 'fixed_official_train_only_class_tail_holdout',
            'selected_indices_sha256': 'c' * 64, 'sampling_seed': 42, 'examples': 1}], 'rows': rows}


def test_actual_negative_quality_and_physical_lengths_preserved():
    metrics, seeds = module.summarize(report())
    assert seeds == [42]
    assert metrics['dense_sampling_seed42']['restricted_first_token_accuracy'] == 1.
    assert metrics['vcola-25-exit24_sampling_seed42']['restricted_first_token_accuracy'] == 0.
    assert metrics['vcola-25-exit24_sampling_seed42']['layer2_visual_tokens_mean'] == 2.
    assert metrics['vcola-25-exit24_sampling_seed42']['layer25_visual_tokens_mean'] == 0.


def test_dataset_fingerprint_stable_mapping_order_and_binds_sampling():
    datasets = report()['datasets']
    reordered = [{key: item[key] for key in reversed(item)} for item in datasets]
    assert module.dataset_fingerprint(datasets) == module.dataset_fingerprint(reordered)
    changed = deepcopy(datasets)
    changed[0]['selected_indices_sha256'] = 'd' * 64
    assert module.dataset_fingerprint(datasets) != module.dataset_fingerprint(changed)


def test_new_curated_metric_is_schema_v2_migration_idempotent(tmp_path, monkeypatch):
    """Fixture validates serializer/provenance only; never a GPU receipt claim."""
    payload = report()
    payload['accelerator'] = 'NVIDIA A100'
    input_path = tmp_path / 'mechanism-validation-fixture.json'
    input_path.write_text(json.dumps(payload))
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    monkeypatch.setattr('sys.argv', ['curate_vcola_evidence', '--input', str(input_path),
                                   '--source-commit', 'test-only'])

    def mocked_source_lookup(command, **kwargs):
        return 'a' * 40 if kwargs.get('text') else b'validator-test source, not GPU execution'

    monkeypatch.setattr(module.subprocess, 'check_output', mocked_source_lookup)
    module.main()
    migration_path = SOURCE.parent / 'migrate_metric_schema_v2.py'
    migration_spec = importlib.util.spec_from_file_location('vcola_schema_migration_test', migration_path)
    migration = importlib.util.module_from_spec(migration_spec)
    migration_spec.loader.exec_module(migration)
    monkeypatch.setattr(migration, 'ROOT', tmp_path)
    metric_path = tmp_path / 'docs/multimodal-models/2610.11251-vcola/metrics/cifar10-a100.json'
    original = metric_path.read_text()
    metric = json.loads(original)
    assert metric['provenance']['dataset_fingerprint'] == module.dataset_fingerprint(payload['datasets'])
    migrated = migration.migrate_payload(metric_path, metric)
    assert migrated == metric
    assert json.dumps(migrated, ensure_ascii=False, indent=2) + '\n' == original
    assert migration.migrate_payload(metric_path, migrated) == migrated


@pytest.mark.parametrize('tamper', ['proxy', 'gold', 'full_accuracy', 'test', 'revision', 'baseline',
                                   'state', 'text', 'merge', 'exit', 'drop_case', 'nonfinite'])
def test_rejects_unsupported_or_corrupt_actual_evidence(tamper):
    value = deepcopy(report())
    if tamper == 'proxy':
        value['protocol']['state_scores_not_feature_proxy'] = False
    elif tamper == 'gold':
        value['protocol']['inference_gold_read'] = True
    elif tamper == 'full_accuracy':
        value['protocol']['full_generated_answer_accuracy'] = True
    elif tamper == 'test':
        value['datasets'][0]['test_read'] = True
    elif tamper == 'revision':
        value['checkpoint']['revision'] = 'main'
    elif tamper == 'baseline':
        value['rows'][0]['dense_backend_relative_error'] = .1
    elif tamper == 'state':
        value['rows'][1]['forward']['recurrence_relative_error'] = .2
    elif tamper == 'text':
        value['rows'][1]['forward']['layers'][10]['sequence_tokens'] -= 1
    elif tamper == 'merge':
        value['rows'][1]['forward']['merge']['chunk_sizes'] = [1] * 4
    elif tamper == 'exit':
        value['rows'][1]['forward']['layers'][24]['visual_tokens'] = 4
    elif tamper == 'drop_case':
        value['rows'].pop()
    else:
        value['rows'][1]['restricted_choice_kl_to_dense'] = float('nan')
    with pytest.raises(ValueError):
        module.summarize(value)
