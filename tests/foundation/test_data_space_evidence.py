from copy import deepcopy
import importlib.util
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[2] / 'scripts/curate_data_space_evidence.py'
spec = importlib.util.spec_from_file_location('curate_data_space_evidence', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def report():
    teacher = {'steps': 20, 'checkpoint_sha256': 'a' * 64,
        'initial_checkpoint_sha256': 'd' * 64,
        'validation_velocity_mse_before': 2., 'validation_velocity_mse_after': 1.,
        'pixel_feature_frechet_distance': 10.}
    row = {'seed': 42, 'teacher': teacher, 'generator_steps': 4, 'fake_steps': 16,
        'generator_parameter_changed': True, 'fake_parameter_changed': True,
        'generator_backbone_parameter_changed': True, 'fake_backbone_parameter_changed': True,
        'trace': [{'refinement': i, 'fake_losses': [1.] * 4, 'fake_gradient_norms': [.1] * 4,
                   'generator_loss': -.1, 'generator_gradient_norm': .1} for i in range(4)],
        'evaluation': [{'nfe': i, 'pixel_feature_frechet_distance': 20. + i} for i in range(1, 5)]}
    return {'paper_id': '2610.12102', 'diagnostic_only': True,
        'protocol': {'test_read': False, 'inception_fid_evaluated': False, 'teacher_trained': True,
            'teacher_frozen_during_dmd': True, 'generator_refinements': 4,
            'fake_updates_per_generator': 4, 'dmd_beta': [2.5, 1.], 'dmd_weight': 1.,
            'adam_betas': [0., .95], 'ema_decay': .9999, 'evaluation_uses_ema': True},
        'dataset': {'test_read': False, 'split_source': 'official_train_only',
            'revision': {f'data_batch_{i}': 'b' * 64 for i in range(1, 6)}},
        'rows': [{**deepcopy(row), 'recipe': recipe} for recipe in ('flow-renoise', 'data-space')]}


def test_negative_outcome_kept_and_valid_actual_pair():
    value = report()
    metrics, seeds = module.summarize(value)
    assert seeds == [42]
    assert metrics['data-space_seed42']['pixel_feature_frechet_nfe4'] == 24.


@pytest.mark.parametrize('tamper', ['gold', 'test', 'teacher', 'frozen_copy', 'unchanged_teacher',
                                   'fake_count', 'prefix', 'nonfinite', 'missing_seed', 'mismatch'])
def test_rejects_proxy_or_corrupt_evidence(tamper):
    value = report()
    if tamper == 'gold':
        value['diagnostic_only'] = False
    elif tamper == 'test':
        value['dataset']['test_read'] = True
    elif tamper == 'teacher':
        value['rows'][0]['teacher']['validation_velocity_mse_after'] = 2.
    elif tamper == 'frozen_copy':
        value['rows'][0]['generator_backbone_parameter_changed'] = False
    elif tamper == 'unchanged_teacher':
        value['rows'][0]['teacher']['initial_checkpoint_sha256'] = 'a' * 64
    elif tamper == 'fake_count':
        value['rows'][0]['fake_steps'] = 4
    elif tamper == 'prefix':
        value['rows'][0]['trace'][1]['refinement'] = 0
    elif tamper == 'nonfinite':
        value['rows'][0]['trace'][0]['fake_losses'][0] = float('inf')
    elif tamper == 'missing_seed':
        value['rows'].pop()
    else:
        value['rows'][0]['teacher']['checkpoint_sha256'] = 'c' * 64
    with pytest.raises(ValueError):
        module.summarize(value)
