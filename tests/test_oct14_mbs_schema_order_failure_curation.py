"""Synthetic ce4 failures; no local evidence/data/checkpoints or CUDA needed."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def fixture():
    m = module(ROOT / 'scripts/curate_oct14_mbs_schema_failure.py', 'schema_negative_curator')
    old = module(ROOT / 'tests/test_oct14_mbs_trace_failure_curation.py', 'historical_negative_fixtures')
    _, args = old.fixture('b9086275')
    source = m.COMMITS['ce4a4a34']
    for record in (args['contract'], args['audit'], args['launch']):
        record['source_commit'] = source
    args['config_sha256'] = m.CONFIG_SHA
    for record in (args['audit'], args['launch']):
        record['execution_config_sha256'] = m.CONFIG_SHA
    l, f = args['launch'], args['failure']
    l['effective_config']['construction_json_schema'] = True
    l['job']['key'] = 'magicbeanstalk-schema-order'
    l['launcher_source_sha256'] = '8595c54dd0b675e83acc20d92c07bb562a76968037492824262f9a1796a6acbc'
    l['base_launcher_source_sha256'] = '186a47f0e8a53b17595a52625dafdd0c8d24406c7ffe4631aa182338abd4cf30'
    l['command'][2] = '/private/auto-research-oct14-ce4a4a34/scripts/run_oct13_post_training.py'
    l['command'][6] = '/private/oct14-mbs-order-ce4a4a34-queue/oct14_execution-mbs-schema-v1.json'
    l['command'][10] = '/private/auto-research-oct14-ce4a4a34/runs/post-training-oct14/oct14-mbs-schema-order42-attempt07/magicbeanstalk-schema-order-s42/evidence'
    l['construction_schema_only'] = l['independent_verifier_and_student_unconstrained'] = True
    l['gpu_slot_grant'] = 'A100-post-training-schema-order-explicit-slot'
    l['actual_accelerator_name'] = 'NVIDIA A100-SXM4-80GB'
    packages = {name: {'version': version, 'package_file_sha256': {name + '/fixture.py': 'a' * 64}}
        for name, version in {'xgrammar': '0.2.8', 'apache-tvm-ffi': '0.1.11', 'pydantic': '2.12.5',
            'pydantic-core': '2.41.5', 'annotated-types': '0.7.0', 'typing-inspection': '0.4.2', 'typing-extensions': '4.15.0'}.items()}
    packages['xgrammar']['package_file_sha256'].update({f'xgrammar/cpu_fixture_{i}.py': 'a' * 64 for i in range(196)})
    dep = {'not_gpu_receipt': True, 'overlay_root': '/private/overlay', 'cuda_initialized': False,
        'dependency_modules_imported_by_audit': False, 'model_instantiated_by_audit': False,
        'packages': packages, 'dependency_fingerprint': hashlib.sha256(json.dumps(packages, sort_keys=True).encode()).hexdigest()}
    grammar = {'algorithm_commit': source, 'source_file_sha256': copy.deepcopy(args['git_hashes']),
        'cuda_initialized': False, 'model_loaded': False, 'vocab_size': 152064, 'tokenizer_sha256': m.TOKENIZER_SHA,
        'versions': {k: v['version'] for k, v in packages.items()},
        'overlay_file_sha256': {p: h for v in packages.values() for p, h in v['package_file_sha256'].items()},
        'operations': {op: {'actual_compilation_completed': True, 'schema_sha256': digest} for op, digest in {
            'blueprint_and_novelty': 'c4f8a00e63a0417315216e6e6afd0333324604f38dfa5a823dc267a131efc3bf',
            'compose': '8768cc6bbb0654c28b9b457654cddb07fde9ae9e7a7a11f8198cf41856835e55',
            'harder_leaf': '8768cc6bbb0654c28b9b457654cddb07fde9ae9e7a7a11f8198cf41856835e55',
            'propose_children': 'b60afb6eb71743e2e47aec78354124df48a40d97b48591592c0214c0c30b29d4',
            'scaffold_safe': 'deb8fa68986813699f24e819d86090e5a964f48dffb3937a6388ef08de11e9c6'}.items()}}
    l['schema_dependency_binding'] = copy.deepcopy(dep)
    l['schema_grammar_binding'] = copy.deepcopy(grammar)
    l['schema_grammar_cpu_audit_sha256'] = 'd' * 64
    l['runner_pythonpath'] = '/private/auto-research-oct14-ce4a4a34/src:/private/overlay'
    args['dependency_audit'], args['grammar_audit'] = dep, grammar
    args['raw_hashes'].update({k: 'd' * 64 for k in ('source_contract', 'resource_audit', 'config', 'grammar_audit', 'dependency_audit')})
    f['construction_response_audits'] = [t for t in f['construction_response_audits'] if t['role'] not in {'construction_verification', 'construction_teacher'}]
    def trace(role, text, **extra):
        f['construction_response_audits'].append({'role': role, 'input_gold_scope': m.GOLD_SCOPES[role],
            'response_text': text, 'response_text_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'response_token_ids': [1, 2], 'generated_tokens': 2, 'truncated': False, **extra})
    roots = f['hard_root_selection']['calibration_audits']
    trace('construction_verification', 'root correct', question_sha256=roots[4]['root_question_sha256'], attempt=1,
        verification_completed=True, accepted=True, reject_reason=None)
    for i in range(4):
        child = {'question': f'independent fixture {i}', 'trace': 'worked solution', 'answer': '7'}
        if i % 2 == 0:
            pair = [child, {'question': f'independent fixture {i + 1}', 'trace': 'worked solution', 'answer': '7'}]
            trace('construction_teacher', json.dumps(pair), operation='propose_children', parsing_completed=True,
                parsed_json_kind='list', reject_reason=None, proposed_problem_count=2, schema_valid_problem_count=2,
                schema_reject_reason=None, json_schema_constrained=True, json_schema_backend='xgrammar-hf',
                xgrammar_version='0.2.8', json_schema_sha256=grammar['operations']['propose_children']['schema_sha256'])
        for attempt in ((1,) if i == 3 else (1, 2)):
            trace('construction_verification', 'wrong numeric outcome', question_sha256=hashlib.sha256(child['question'].encode()).hexdigest(),
                attempt=attempt, verification_completed=True, accepted=i == 3, reject_reason=None if i == 3 else 'incorrect_independent_solution')
    for root in (7, 8):
        for attempt in (1, 2):
            trace('construction_verification', 'root wrong', question_sha256=roots[root]['root_question_sha256'], attempt=attempt,
                verification_completed=True, accepted=False, reject_reason='incorrect_independent_solution')
    for row in f['construction_audits']:
        if row['phase'] == 'decomposition': row['verified_children'] = 0 if row['attempt'] == 1 else 1
    f['cost']['generation_calls']['construction_verification'] = 12
    for role in f['cost']['generated_tokens']:
        if role != 'evaluation':
            f['cost']['generated_tokens'][role] = sum(t['generated_tokens'] for t in f['construction_response_audits'] if t['role'] == role)
    return m, args


def test_actual_schema_negative_cannot_be_receipt_or_rebound_to_new_property_order():
    m, args = fixture()
    result = m.curate_bundle(**args)
    assert result['curation_state'] == 'sanitized-negative-record'
    assert result['provenance']['artifact_path'] == 'docs/reproductions/2610.12659-magicbeanstalk/metrics/public-a100-schema-order-failed-seed42-ce4a4a34.json'
    assert result['not_gpu_receipt'] and not result['whole_method_gpu_validation_passed']
    metrics = result['seed_results'][0]['metrics']
    assert metrics['method_rl_updates'] == metrics['control_rl_updates'] == metrics['paired_rl_roots'] == 0
    assert metrics['schema_valid_proposed_children'] == 4 and metrics['accepted_independent_verifications'] == 2
    assert metrics['independent_verification_calls'] == 12 and metrics['invalid_outer_json_proposals'] == 0
    assert result['execution_checks']['compiled_property_order'] == ['question', 'trace', 'answer']
    output = json.dumps(result)
    assert '/private/' not in output and 'response_token_ids' not in output and 'response_text"' not in output


@pytest.mark.parametrize('case', ['new_sha', 'source', 'git', 'config', 'bool', 'budget', 'argv', 'rc', 'wall', 'raw',
    'metadata_sha', 'metadata_version', 'metadata_off', 'property_order', 'outer_invalid', 'accepted_child', 'paired',
    'cost', 'text_sha', 'token_count', 'role', 'gold', 'dependency_version', 'dependency_fingerprint', 'dependency_drift',
    'grammar_not_compiled', 'grammar_source', 'grammar_sha', 'grammar_file_sha', 'grammar_cuda', 'fake_pass', 'pythonpath',
    'old_schema', 'reject_good_child', 'erase_second_verified_child'])
def test_schema_evidence_rejects_drift_repair_or_fake_success(case):
    m, args = fixture()
    l, f, d, g = args['launch'], args['failure'], args['dependency_audit'], args['grammar_audit']
    teacher = next(t for t in f['construction_response_audits'] if t['role'] == 'construction_teacher')
    if case == 'new_sha': args['contract']['source_commit'] = 'a' * 40
    elif case == 'source': l['source_commit'] = 'a' * 40
    elif case == 'git': args['git_hashes'][next(iter(args['git_hashes']))] = 'f' * 64
    elif case == 'config': args['config_sha256'] = 'f' * 64
    elif case == 'bool': l['effective_config']['construction_json_schema'] = 'true'
    elif case == 'budget': l['effective_config']['max_tokens'] += 1
    elif case == 'argv': l['command'].append('--new-retry')
    elif case == 'rc': args['exit_record']['exit_code'] = 0
    elif case == 'wall': args['exit_record']['elapsed_seconds'] = float('nan')
    elif case == 'raw': args['raw_hashes'].pop('failure')
    elif case == 'metadata_sha': teacher['json_schema_sha256'] = 'f' * 64
    elif case == 'metadata_version': teacher['xgrammar_version'] = '0.3.0'
    elif case == 'metadata_off': teacher['json_schema_constrained'] = False
    elif case == 'property_order':
        values = json.loads(teacher['response_text']); values[0] = dict(reversed(list(values[0].items())))
        teacher['response_text'] = json.dumps(values); teacher['response_text_sha256'] = hashlib.sha256(teacher['response_text'].encode()).hexdigest()
    elif case == 'outer_invalid':
        teacher['response_text'] = '[invalid ' + teacher['response_text']; teacher['response_text_sha256'] = hashlib.sha256(teacher['response_text'].encode()).hexdigest()
    elif case == 'accepted_child':
        t = [r for r in f['construction_response_audits'] if r['role'] == 'construction_verification'][1]
        t['accepted'] = True; t['reject_reason'] = None
    elif case == 'paired': f['hard_root_selection']['paired_rl_root_indices'] = [4]
    elif case == 'cost': f['cost']['generated_tokens']['construction_teacher'] += 1
    elif case == 'text_sha': teacher['response_text'] += 'changed'
    elif case == 'token_count': teacher['generated_tokens'] += 1
    elif case == 'role': teacher['role'] = 'mbs-rlvr'
    elif case == 'gold': teacher['input_gold_scope'] = 'validation-answer'
    elif case == 'dependency_version': d['packages']['xgrammar']['version'] = '0.3.0'
    elif case == 'dependency_fingerprint': d['dependency_fingerprint'] = 'f' * 64
    elif case == 'dependency_drift': l['schema_dependency_binding']['packages']['xgrammar']['package_file_sha256']['xgrammar/fixture.py'] = 'f' * 64
    elif case == 'grammar_not_compiled': g['operations']['propose_children']['actual_compilation_completed'] = False
    elif case == 'grammar_source': g['algorithm_commit'] = 'a' * 40
    elif case == 'grammar_sha': g['operations']['propose_children']['schema_sha256'] = 'f' * 64
    elif case == 'grammar_file_sha': g['overlay_file_sha256']['xgrammar/fixture.py'] = 'f' * 64
    elif case == 'grammar_cuda': g['cuda_initialized'] = True
    elif case == 'fake_pass': f['status'] = 'passed'
    elif case == 'pythonpath': l['runner_pythonpath'] = '/private/new-source:/private/overlay'
    elif case == 'old_schema': teacher['json_schema_sha256'] = m.SCHEMA_SHAS['propose_children']
    elif case == 'reject_good_child':
        accepted = [r for r in f['construction_response_audits'] if r['role'] == 'construction_verification' and r['accepted']][-1]
        accepted['accepted'] = False; accepted['reject_reason'] = 'incorrect_independent_solution'
    elif case == 'erase_second_verified_child': f['construction_audits'][2]['verified_children'] = 0
    with pytest.raises((ValueError, KeyError)):
        m.curate_bundle(**args)


def test_actual_ordered_native_keeps_failed_scope_and_exact_frozen_evidence():
    path = 'docs/reproductions/2610.12659-magicbeanstalk/metrics/public-a100-schema-order-failed-seed42-ce4a4a34.json'
    native = json.loads((ROOT / path).read_text())
    assert native['curation_state'] == 'sanitized-negative-record'
    assert native['not_gpu_receipt'] and not native['whole_method_gpu_validation_passed']
    assert native['diagnostic_only'] and not native['promotion_eligible']
    assert native['provenance']['artifact_path'] == path
    assert native['provenance']['code_commit'] == 'ce4a4a34520419a50fb730d93967aaed5024fa77'
    assert native['provenance']['execution_config_sha256'] == '6717f5dd647b812e5fc6dcdcd91b3f089e2a55003bc6ee68ac76d88319a7b1df'
    assert native['provenance']['raw_results_sha256'] == {"launch":"66bdda2cf75638de21d4d4067b76fe2e48b9029d86e99e6b2048a31bc8e2a874","exit":"dc5b4735e8d595a3434ca44a4a4051ebfe118e558bd6eaa41430eb6201049512","runtime":"c5a25cb305d7732c8a04e0e0f6a9c31e64d1d14c8552ca4ddb1509bfebccb301","failure":"19c56c036b6dd87f7658c14a7c45c53065a662c920cc807532ce6bbbdba6151d","source_contract":"b0c209ac4a09317441b5a38c5f15c5869d28dc532a15ad1c05c75bca5d2a2aa0","resource_audit":"7fdd91ab379a774193a6614082c3bacd34f025ecd372d1d0e32243d06cbe0d13","config":"b5c7201a28db4b58a5603c994beadd94848362beaa2b079f37f0d60559575999","dependency_audit":"a0c5a4cf13642258131c4e0d1c62a686dcf35f0da37d28b3d2c4f1fd072732b1","grammar_audit":"80ddb3bb012c15e6bb4de32a781342fb50de80f8a3a3fc7afe85837fa5d2cbea"}
    assert native['seed_results'][0]['metrics'] == {"verified_hard_roots":3,"construction_attempts":3,"paired_rl_roots":0,"method_rl_updates":0,"control_rl_updates":0,"decomposition_proposal_calls":2,"schema_valid_proposed_children":4,"invalid_outer_json_proposals":0,"independent_verification_calls":12,"accepted_independent_verifications":2,"rejected_independent_verifications":10,"generated_response_tokens":36425,"invocation_elapsed_seconds":351.71331273019314}
    m = module(ROOT / 'scripts/curate_oct14_mbs_schema_failure.py', 'actual_ordered_curator')
    assert len(native['executed_source_sha256']) == 54 and set(native['executed_source_sha256']) == m.SOURCE_PATHS
    assert native['executed_source_sha256']['src/auto_research/post_training/response_policy.py'] == '4f44d4e28b8bcd94aa6876122ec6c1b6539a67be274f513a2e92a127ac57ae42'
    assert native['executed_source_sha256']['src/auto_research/reproductions/magicbeanstalk/checkpoint.py'] == '2d289489a8822a360d2c02f2bf2f65ad5029191901a1d94ba65c67a6d8e0c85f'
    checks = native['execution_checks']
    assert checks['return_code'] == 1 and checks['configured_wall_cap_seconds'] == 1800
    assert checks['compiled_property_order'] == ['question', 'trace', 'answer']
    assert checks['schema_sha256'] == m.ORDERED_SCHEMA_SHAS
    assert checks['schema_sha256']['propose_children'] != m.SCHEMA_SHAS['propose_children']
    assert len(checks['sanitized_response_audits']) == 86
    proposals = [r for r in checks['sanitized_response_audits'] if r['role'] == 'construction_teacher']
    assert [r['generated_tokens'] for r in proposals] == [204, 246]
    assert all(r['json_schema_sha256'] == m.ORDERED_SCHEMA_SHAS['propose_children'] for r in proposals)
    assert [r['verified_children'] for r in checks['construction_audits'] if r['phase'] == 'decomposition'] == [0, 1]
    assert checks['measured_cost']['generated_tokens'] == {'evaluation': 1541, 'target_calibration': 29408,
        'construction_verification': 2757, 'effectivity_student': 1231, 'effectivity_teacher': 1038, 'construction_teacher': 450}
    output = json.dumps(native)
    assert '/tmp/' not in output and '/Users/' not in output and 'response_token_ids' not in output and 'response_text"' not in output
    assert native['dataset'] == m.DATASET and native['evaluation_protocol']['formal_comparison'] is False
