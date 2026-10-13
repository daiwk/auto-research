"""Synthetic f924 failures; no local evidence/data/checkpoints or CUDA needed."""
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
    source = m.COMMITS['f92413aa']
    for record in (args['contract'], args['audit'], args['launch']):
        record['source_commit'] = source
    args['config_sha256'] = m.CONFIG_SHA
    for record in (args['audit'], args['launch']):
        record['execution_config_sha256'] = m.CONFIG_SHA
    l, f = args['launch'], args['failure']
    l['effective_config']['construction_json_schema'] = True
    l['job']['key'] = 'magicbeanstalk-schema'
    l['launcher_source_sha256'] = m.LAUNCHER_SHA
    l['base_launcher_source_sha256'] = '186a47f0e8a53b17595a52625dafdd0c8d24406c7ffe4631aa182338abd4cf30'
    l['command'][2] = '/private/auto-research-oct14-f92413aa/scripts/run_oct13_post_training.py'
    l['command'][6] = '/private/oct14-mbs-schema-f92413aa-queue/oct14_execution-mbs-schema-v1.json'
    l['command'][10] = '/private/auto-research-oct14-f92413aa/runs/post-training-oct14/oct14-mbs-schema42-attempt06/magicbeanstalk-schema-s42/evidence'
    l['construction_schema_only'] = l['independent_verifier_and_student_unconstrained'] = True
    l['gpu_slot_grant'] = 'A100-post-training-schema-explicit-slot'
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
            'blueprint_and_novelty': '73e3e05f28e47881109e697b3f8ea64b1a8cadafb1231fab0d952b66aedb2ca5',
            'compose': '3c44af604a1fac7a22e27b09d529becb8e33c26ec3cecda014035066aba6f086',
            'harder_leaf': '3c44af604a1fac7a22e27b09d529becb8e33c26ec3cecda014035066aba6f086',
            'propose_children': '0a4eeac64e58ec46fc6333fa3bbd125e53bb62be08f63cf6aa2af3bc0a3d5f43',
            'scaffold_safe': '120398dbde513fb336619f2e3535be7b21ac22f055a8886f2e12dfa5f0fd0e67'}.items()}}
    l['schema_dependency_binding'] = copy.deepcopy(dep)
    l['schema_grammar_binding'] = copy.deepcopy(grammar)
    l['schema_grammar_cpu_audit_sha256'] = 'd' * 64
    l['runner_pythonpath'] = '/private/auto-research-oct14-f92413aa/src:/private/overlay'
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
        child = {'answer': '7', 'question': f'independent fixture {i}', 'trace': 'worked solution'}
        if i % 2 == 0:
            pair = [child, {'answer': '7', 'question': f'independent fixture {i + 1}', 'trace': 'worked solution'}]
            trace('construction_teacher', json.dumps(pair), operation='propose_children', parsing_completed=True,
                parsed_json_kind='list', reject_reason=None, proposed_problem_count=2, schema_valid_problem_count=2,
                schema_reject_reason=None, json_schema_constrained=True, json_schema_backend='xgrammar-hf',
                xgrammar_version='0.2.8', json_schema_sha256=grammar['operations']['propose_children']['schema_sha256'])
        for attempt in (1, 2):
            trace('construction_verification', 'wrong numeric outcome', question_sha256=hashlib.sha256(child['question'].encode()).hexdigest(),
                attempt=attempt, verification_completed=True, accepted=False, reject_reason='incorrect_independent_solution')
    for root in (7, 8):
        for attempt in (1, 2):
            trace('construction_verification', 'root wrong', question_sha256=roots[root]['root_question_sha256'], attempt=attempt,
                verification_completed=True, accepted=False, reject_reason='incorrect_independent_solution')
    for row in f['construction_audits']:
        if row['phase'] == 'decomposition': row['verified_children'] = 0
    f['cost']['generation_calls']['construction_verification'] = 13
    for role in f['cost']['generated_tokens']:
        if role != 'evaluation':
            f['cost']['generated_tokens'][role] = sum(t['generated_tokens'] for t in f['construction_response_audits'] if t['role'] == role)
    return m, args


def test_actual_schema_negative_cannot_be_receipt_or_rebound_to_new_property_order():
    m, args = fixture()
    result = m.curate_bundle(**args)
    assert result['curation_state'] == 'sanitized-negative-record'
    assert result['provenance']['artifact_path'] == 'docs/reproductions/2610.12659-magicbeanstalk/metrics/public-a100-schema-failed-seed42-f92413aa.json'
    assert result['not_gpu_receipt'] and not result['whole_method_gpu_validation_passed']
    metrics = result['seed_results'][0]['metrics']
    assert metrics['method_rl_updates'] == metrics['control_rl_updates'] == metrics['paired_rl_roots'] == 0
    assert metrics['schema_valid_proposed_children'] == 4 and metrics['accepted_independent_verifications'] == 1
    assert metrics['independent_verification_calls'] == 13 and metrics['invalid_outer_json_proposals'] == 0
    assert result['execution_checks']['compiled_property_order'] == ['answer', 'question', 'trace']
    output = json.dumps(result)
    assert '/private/' not in output and 'response_token_ids' not in output and 'response_text"' not in output


@pytest.mark.parametrize('case', ['new_sha', 'source', 'git', 'config', 'bool', 'budget', 'argv', 'rc', 'wall', 'raw',
    'metadata_sha', 'metadata_version', 'metadata_off', 'property_order', 'outer_invalid', 'accepted_child', 'paired',
    'cost', 'text_sha', 'token_count', 'role', 'gold', 'dependency_version', 'dependency_fingerprint', 'dependency_drift',
    'grammar_not_compiled', 'grammar_source', 'grammar_sha', 'grammar_file_sha', 'grammar_cuda', 'fake_pass', 'pythonpath'])
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
    with pytest.raises(ValueError): m.curate_bundle(**args)


def test_committed_actual_native_is_frozen_sorted_schema_failure_not_new_gpu_receipt():
    path = 'docs/reproductions/2610.12659-magicbeanstalk/metrics/public-a100-schema-failed-seed42-f92413aa.json'
    native = json.loads((ROOT / path).read_text())
    assert native['schema_version'] == 2 and native['curation_state'] == 'sanitized-negative-record'
    assert native['not_gpu_receipt'] and not native['whole_method_gpu_validation_passed']
    assert native['diagnostic_only'] and not native['promotion_eligible']
    assert native['provenance']['artifact_path'] == path
    assert native['provenance']['code_commit'] == 'f92413aabaef0a7d84dcddcb3d4064f5c2d464a3'
    assert native['provenance']['execution_config_sha256'] == '6717f5dd647b812e5fc6dcdcd91b3f089e2a55003bc6ee68ac76d88319a7b1df'
    assert len(native['executed_source_sha256']) == 54
    assert native['provenance']['raw_results_sha256'] == {
        'config': 'b5c7201a28db4b58a5603c994beadd94848362beaa2b079f37f0d60559575999',
        'dependency_audit': 'a0c5a4cf13642258131c4e0d1c62a686dcf35f0da37d28b3d2c4f1fd072732b1',
        'exit': 'bf2fd1fe754db64db8b1690a551ee5745c107de45794182909b78680cb9a8286',
        'failure': '63dbc60513bfd4f0b1b7dca907ef345d6ed3a8f8bc09e52c4e94b2ed6d7a332f',
        'grammar_audit': '68998139aef79b7e0ef95490e5f34aff5de93c47b49f21dd631a20f2590484b4',
        'launch': 'bdf35092b865cdbdfe6c6cc38c883bb3e1c2dd137a94202a9fc3db0f98aa0ef3',
        'resource_audit': '6be4b8ba2a7894439cecc29ccd01d9d568b5050dc4ffe26762f0f4c5c7029383',
        'runtime': 'f2bc29975d6842655b71a283d5c7a7d86be18501dd60fcfb8ce8f276765621f7',
        'source_contract': '571f6824ef438fb1d32eebda0df434ebf9df8f6b1ad65884c29832ec66721d28'}
    assert {p: native['executed_source_sha256'][p] for p in (
        'src/auto_research/post_training/response_policy.py', 'src/auto_research/post_training/oct13_common.py',
        'src/auto_research/reproductions/magicbeanstalk/checkpoint.py')} == {
        'src/auto_research/post_training/response_policy.py': '9174b21971e81b15c0cfa17f64c88d7387f2920dc3d0b3830b16d3e84189ff20',
        'src/auto_research/post_training/oct13_common.py': 'bae993fd2322edddbc419cb81a0c039b725f978989eab948fbdd597ca9f250ac',
        'src/auto_research/reproductions/magicbeanstalk/checkpoint.py': 'd9dd5d42e1e07cdb01ed7c22de04989e2a3430995c56e9dcc119d47db0738f92'}
    m = module(ROOT / 'scripts/curate_oct14_mbs_schema_failure.py', 'native_schema_curator')
    assert set(native['executed_source_sha256']) == m.SOURCE_PATHS
    metrics = native['seed_results'][0]['metrics']
    assert metrics == {'verified_hard_roots': 3, 'construction_attempts': 3, 'paired_rl_roots': 0,
        'method_rl_updates': 0, 'control_rl_updates': 0, 'decomposition_proposal_calls': 2,
        'schema_valid_proposed_children': 4, 'invalid_outer_json_proposals': 0,
        'independent_verification_calls': 13, 'accepted_independent_verifications': 1,
        'rejected_independent_verifications': 12, 'generated_response_tokens': 36728,
        'invocation_elapsed_seconds': 374.29659676365554}
    checks = native['execution_checks']
    assert checks['return_code'] == 1 and checks['configured_wall_cap_seconds'] == 1800
    assert checks['compiled_property_order'] == ['answer', 'question', 'trace']
    assert checks['schema_sha256'] == m.SCHEMA_SHAS
    assert checks['dependency_versions'] == m.PINNED
    assert len(checks['sanitized_response_audits']) == 87
    proposals = [r for r in checks['sanitized_response_audits'] if r['role'] == 'construction_teacher']
    assert len(proposals) == 2 and all(r['json_schema_sha256'] == m.SCHEMA_SHAS['propose_children'] for r in proposals)
    assert [r['generated_tokens'] for r in proposals] == [337, 127]
    assert checks['measured_cost']['generated_tokens'] == {'evaluation': 1541, 'target_calibration': 29408,
        'construction_verification': 3046, 'effectivity_student': 1231, 'effectivity_teacher': 1038,
        'construction_teacher': 464}
    assert all(r['verified_children'] == 0 for r in checks['construction_audits'] if r['phase'] == 'decomposition')
    assert native['dataset'] == m.DATASET and native['evaluation_protocol']['formal_comparison'] is False
    def safe(value):
        if isinstance(value, dict):
            assert not {'response_text', 'response_token_ids', 'hostname', 'ssh_alias', 'driver_version'} & value.keys()
            for child in value.values(): safe(child)
        elif isinstance(value, list):
            for child in value: safe(child)
        elif isinstance(value, str):
            assert '/tmp/' not in value and '/Users/' not in value
    safe(native)
