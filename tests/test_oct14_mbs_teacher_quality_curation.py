"""Pure synthetic CPU evidence; never model/CUDA or a GPU receipt fixture."""
import copy
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def module():
    p = ROOT / 'scripts/curate_oct14_mbs_teacher_quality.py'
    s = importlib.util.spec_from_file_location('quality_curator', p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def fixture():
    m = module()
    hashes = {p: hashlib.sha256(p.encode()).hexdigest() for p in m.BASE.SOURCE_PATHS}
    runner = {'source_commit': m.RUNNER_COMMIT, 'source_file_sha256': {m.RUNNER: m.RUNNER_SHA}}
    core = {'source_commit': m.CORE_COMMIT, 'source_file_sha256': hashes}
    dataset = copy.deepcopy(m.DATASET)
    dependency = {'packages': {k: {'version': v, 'package_file_sha256': {k + '/fixture.py': 'a' * 64}}
        for k, v in m.BASE.PINNED.items()}, 'cuda_initialized': False, 'model_instantiated_by_audit': False,
        'dependency_modules_imported_by_audit': False}
    dependency['dependency_fingerprint'] = m.canonical(dependency['packages'])
    checkpoint = {'public_id': m.TEACHER_ID, 'revision': m.TEACHER_REVISION,
        'verified_mirror': {'public_id': m.TEACHER_ID, 'revision': m.TEACHER_REVISION,
            'file_sha256': {k: 'b' * 64 for k in m.BASE.RESOURCE_FILES['teacher']}}}
    checkpoint['verified_mirror']['file_sha256'].update(m.BASE.WEIGHTS['teacher'])
    checkpoint['verified_mirror']['file_sha256']['tokenizer.json'] = m.BASE.TOKENIZER_SHA
    audit = {**runner, 'artifact_kind': 'read_only_cpu_resource_audit_not_gpu_receipt', 'source_hashes_verified': True,
        'cuda_initialized': False, 'model_instantiated': False, 'execution_config_sha256': m.BASE.CONFIG_SHA,
        'algorithm_commit': m.CORE_COMMIT, 'algorithm_source_sha256': hashes,
        'actually_imported_operator_files_sha256': {p: hashes[p] for p in m.OPERATOR_PATHS},
        'teacher_checkpoint_verified_again': True, 'dependency_fingerprint': dependency['dependency_fingerprint'],
        'dataset': dataset, 'actual_prefix_counts': {'train': 16, 'validation': 4}, 'diagnostic_caps': copy.deepcopy(m.CAPS), 'not_gpu_receipt': True}
    core_audit = {**core, 'source_hashes_verified': True, 'cuda_initialized': False, 'model_instantiated': False,
        'execution_config_sha256': m.BASE.CONFIG_SHA, 'public_train_only_holdout': m.BASE.DATASET,
        'resources': {'teacher': {'verified': True, 'public_id': m.TEACHER_ID, 'revision': m.TEACHER_REVISION,
            'file_sha256': checkpoint['verified_mirror']['file_sha256']}}}
    d = {**{k: v for k, v in m.REQUIRED_FLAGS.items()}, 'source_commit': m.RUNNER_COMMIT,
        'diagnostic_runner_sha256': m.RUNNER_SHA, 'algorithm_commit': m.CORE_COMMIT,
        'algorithm_source_file_sha256': hashes, 'actually_imported_operator_files_sha256': audit['actually_imported_operator_files_sha256'],
        'execution_config_sha256': m.BASE.CONFIG_SHA, 'dataset': dataset, 'configured_caps': copy.deepcopy(m.CAPS),
        'wall_cap_seconds': 600, 'external_controller_wall_cap_required_seconds': 600,
        'schema_dependency_binding': dependency, 'schema_dependency_audit_sha256': 'd' * 64,
        'accelerator': {'vendor': 'NVIDIA', 'model': 'NVIDIA A100-SXM4-80GB'}, 'checkpoint': checkpoint,
        'actual_elapsed_seconds': 12.0, 'actual_max_memory_allocated_bytes': 100,
        'actual_max_memory_reserved_bytes': 200, 'gold_access_roles': m.GOLD_SCOPES,
        'diagnosis_status': 'completed-teacher-quality-diagnostic', 'response_audits': [], 'generation_attempts': []}
    roots = ['CPU root four', 'CPU root seven', 'CPU root eight']
    m.ROOT_HASHES = {i: m.sha(q.encode()) for i, q in zip((4, 7, 8), roots)}
    m.VALIDATION_HASHES = [m.sha(('CPU val ' + str(i)).encode()) for i in range(4)]
    children = [{'question': 'CPU child one', 'trace': 'worked 7', 'answer': '7'},
        {'question': 'CPU child two', 'trace': 'worked 7', 'answer': '7'}]
    context = {'parent': {'question': roots[0], 'answer': '7', 'trace': '\\boxed{7}'}, 'ineffective_decompositions': []}
    groups = [('train_root_greedy', roots), ('construction_teacher', ['construction\n' + json.dumps(context)]),
        ('train_child_greedy', [c['question'] for c in children]), ('validation_current-t1', ['CPU val ' + str(i) for i in range(4)]),
        ('validation_greedy', ['CPU val ' + str(i) for i in range(4)])]
    for role, questions in groups:
        for question in questions:
            constrained = role == 'construction_teacher'
            text = json.dumps(children) if constrained else '\\boxed{7}'
            d['response_audits'].append({'role': role, 'sample': role == 'validation_current-t1', 'response_text': text,
                'response_text_sha256': m.sha(text.encode()), 'response_token_ids': [1, 2], 'generated_tokens': 2, 'truncated': False})
            d['generation_attempts'].append({'role': role, 'sample': role == 'validation_current-t1', 'completed': True,
                'actual_responses': 1, 'max_tokens': 1024, 'actual_messages': [{'role': 'user', 'content': question if constrained else m.SOLVER_PREFIX + question}],
                'json_schema_constrained': constrained, 'input_gold_scope': 'training-construction-context' if constrained else 'question-only-no-answer-or-trace'})
    d['actual_output_count'] = 14
    d['cost'] = {'generation_calls': m.CALLS, 'generated_tokens': {k: 2 * n for k, n in m.CALLS.items()},
        'scored_response_tokens': {}, 'frozen_encoder_forward_calls': 0, 'frozen_encoder_input_tokens_including_prompt': 0,
        'scope': 'entire invocation, including training controls, profiling and evaluation', 'includes_rejected_and_profiling_generations': True}
    d['training_root_solves'] = [{'training_index': i, 'correct': float(i == 4), 'truncated': False,
        'question_sha256': m.ROOT_HASHES[i]} for i in (4, 7, 8)]
    d['proposal'] = {'attempted': True, 'verified_child_count': 2, 'proposed_child_count': 2, 'reject_reason': None,
        'children': [{'question': c['question'], 'proposed_answer': c['answer'], 'proposed_trace': c['trace'],
            'independent_correct': 1.0, 'truncated': False} for c in children]}
    d['construction_response_audits'] = [{**d['response_audits'][3], 'json_schema_sha256': m.SCHEMA_SHA,
        'input_gold_scope': 'training-construction-context', 'operation': 'propose_children', 'diagnostic_greedy_override': True,
        'parsing_completed': True, 'parsed_json_kind': 'list', 'proposed_problem_count': 2, 'schema_valid_problem_count': 2,
        'schema_reject_reason': None}]
    d['validation_profiles'] = {p: {'completed': True, 'rows': [{'validation_index': i, 'correct': float(v), 'truncated': False}
        for i, v in enumerate(values)], 'accuracy': sum(values) / 4,
        'sampling': {'sample': True, 'temperature': 1.0, 'top_p': 1.0, 'top_k': 0} if p == 'current-t1' else {'sample': False}}
        for p, values in [('current-t1', [0, 1, 0, 1]), ('greedy', [1, 1, 0, 1])]}
    raw = {k: 'd' * 64 for k in m.RAW_KEYS}
    launch = {'argv': m.EXPECTED_ARGV, 'launcher_sha256': m.LAUNCHER_SHA, 'cpu_audit_sha256': raw['cpu_audit'],
        'diagnostic_source_commit': m.RUNNER_COMMIT, 'diagnostic_source_sha256': m.RUNNER_SHA, 'algorithm_commit': m.CORE_COMMIT,
        'seed': 42, 'wall_cap_seconds': 600, 'outputs_upper': 14, 'tokens_upper': 14336,
        'gpu_grant': 'A100-MBS-teacher-quality-explicit-slot', 'auto_retry': False, 'not_gpu_receipt': True,
        'concurrent_skill_launch_sha256': 'e' * 64,
        'admission': {'model': 'NVIDIA A100-SXM4-80GB', 'existing_compute_process_count': 1, 'exclusive_latency_comparison': False}}
    return m, {'launch': launch, 'exit_record': {'exit_code': 0, 'raw_returncode': 0, 'status': 'completed',
        'elapsed_seconds': 13.0, 'not_gpu_receipt': True, 'runtime_sha256': raw['runtime']}, 'diagnosis': d,
        'runner_contract': runner, 'cpu_audit': audit, 'core_contract': core, 'core_audit': core_audit,
        'source_git_hashes': runner['source_file_sha256'], 'algorithm_git_hashes': hashes,
        'config_sha256': m.BASE.CONFIG_SHA, 'raw_hashes': raw}


def test_all_fourteen_outputs_are_diagnostic_and_sanitized_not_a_gpu_receipt():
    m, args = fixture(); result = m.curate_bundle(**args)
    assert result['not_gpu_receipt'] and not result['whole_method_gpu_validation_passed']
    assert not result['promotion_eligible'] and not result['evaluation_protocol']['formal_comparison']
    assert result['evaluation_protocol']['seeds'] == [42]
    assert result['provenance']['dataset_fingerprint'] == m.canonical(result['dataset'])
    metrics = result['seed_results'][0]['metrics']
    assert metrics['training_root_correct'] == 1 and metrics['training_root_total'] == 3
    assert metrics['independently_correct_children'] == 2 and metrics['actual_outputs'] == 14
    assert metrics['validation_current_t1_accuracy'] == .5 and metrics['validation_greedy_accuracy'] == .75
    assert result['execution_checks']['latency_or_throughput_comparison_eligible'] is False
    output = json.dumps(result)
    assert '/tmp/' not in output and 'response_text"' not in output and 'actual_messages' not in output
    assert 'CPU root' not in output and 'CPU child' not in output and 'response_token_ids"' not in output


@pytest.mark.parametrize('case', ['runner', 'runner_git', 'core', 'core_git', 'cpu', 'runtime', 'rc', 'wall', 'nan',
    'argv', 'budget', 'student', 'optimizer', 'full_chain', 'formal', 'root', 'root_hash', 'profile', 'profile_score',
    'profile_pair', 'token', 'response_sha', 'token_length', 'cost', 'gold_scope', 'sample', 'schema', 'repair',
    'children', 'child_prompt', 'resource', 'dataset', 'dependency', 'raw', 'peak', 'overlap', 'construction_parent',
    'both_validation_prompts', 'child_verifier_numeric'])
def test_actual_curator_rejects_drift_without_relaxing_diagnostic_scope(case):
    m, a = fixture(); d = a['diagnosis']
    if case == 'runner': d['source_commit'] = 'a' * 40
    elif case == 'runner_git': a['source_git_hashes'] = {m.RUNNER: 'f' * 64}
    elif case == 'core': d['algorithm_commit'] = 'a' * 40
    elif case == 'core_git': a['algorithm_git_hashes'] = {**a['algorithm_git_hashes'], next(iter(a['algorithm_git_hashes'])): 'f' * 64}
    elif case == 'cpu': a['cpu_audit']['cuda_initialized'] = True
    elif case == 'runtime': a['exit_record']['runtime_sha256'] = 'f' * 64
    elif case == 'rc': a['exit_record']['exit_code'] = 1
    elif case == 'wall': a['exit_record']['elapsed_seconds'] = 601
    elif case == 'nan': d['actual_elapsed_seconds'] = float('nan')
    elif case == 'argv': a['launch']['argv'] = m.EXPECTED_ARGV + ['--retry']
    elif case == 'budget': d['configured_caps']['outputs_upper'] = 15
    elif case == 'student': d['student_instantiated'] = True
    elif case == 'optimizer': d['optimizer_updates'] = 1
    elif case == 'full_chain': d['effectivity_executed'] = True
    elif case == 'formal': d['formal_comparison'] = True
    elif case == 'root': d['training_root_solves'][1]['correct'] = 1.0
    elif case == 'root_hash': d['training_root_solves'][0]['question_sha256'] = 'f' * 64
    elif case == 'profile': d['validation_profiles']['greedy']['rows'].pop()
    elif case == 'profile_score': d['validation_profiles']['greedy']['accuracy'] = 1.0
    elif case == 'profile_pair': d['generation_attempts'][10]['actual_messages'][0]['content'] += 'changed'
    elif case == 'token': d['response_audits'][0]['response_token_ids'][0] = -1
    elif case == 'response_sha': d['response_audits'][0]['response_text'] += 'changed'
    elif case == 'token_length': d['response_audits'][0]['generated_tokens'] += 1
    elif case == 'cost': d['cost']['generated_tokens']['construction_teacher'] += 1
    elif case == 'gold_scope': d['generation_attempts'][0]['input_gold_scope'] = 'training-construction-context'
    elif case == 'sample': d['generation_attempts'][0]['sample'] = True
    elif case == 'schema': d['construction_response_audits'][0]['json_schema_sha256'] = 'f' * 64
    elif case == 'repair':
        text = 'malformed ' + d['response_audits'][3]['response_text']
        d['response_audits'][3]['response_text'] = text; d['response_audits'][3]['response_text_sha256'] = m.sha(text.encode())
    elif case == 'children': d['proposal']['verified_child_count'] = 1
    elif case == 'child_prompt': d['generation_attempts'][4]['actual_messages'][0]['content'] += 'changed'
    elif case == 'resource': d['checkpoint']['revision'] = 'a' * 40
    elif case == 'dataset': d['dataset']['test_content_read'] = True
    elif case == 'dependency': d['schema_dependency_binding']['packages']['xgrammar']['version'] = '0.3.0'
    elif case == 'raw': a['raw_hashes'].pop('diagnosis')
    elif case == 'peak': d['actual_max_memory_reserved_bytes'] = 25 * 1024**3
    elif case == 'overlap': a['launch']['admission']['exclusive_latency_comparison'] = True
    elif case == 'construction_parent': d['generation_attempts'][3]['actual_messages'][0]['content'] = 'construction\n' + json.dumps({
        'parent': {'question': 'wrong parent', 'answer': '7', 'trace': '\\boxed{7}'}, 'ineffective_decompositions': []})
    elif case == 'both_validation_prompts':
        for i in (6, 10): d['generation_attempts'][i]['actual_messages'][0]['content'] += 'GOLD-INJECTED'
    elif case == 'child_verifier_numeric':
        d['response_audits'][4]['response_text'] = '\\boxed{8}'
        d['response_audits'][4]['response_text_sha256'] = m.sha(d['response_audits'][4]['response_text'].encode())
    with pytest.raises((ValueError, KeyError)): m.curate_bundle(**a)


def partial_fixture(m, diagnosis):
    records = {}
    for i in range(1, 15):
        for stage in ('started', 'completed'):
            n = i if stage == 'completed' else i - 1
            s = copy.deepcopy(diagnosis)
            s.update(partial_snapshot=True, diagnostic_outputs_usable=False, actual_output_count=n,
                response_audits=s['response_audits'][:n], generation_attempts=s['generation_attempts'][:i],
                unreturned_generation_cost_measured=stage == 'completed')
            if stage == 'started':
                s['generation_attempts'][-1].pop('actual_responses')
                s['generation_attempts'][-1]['completed'] = False
            calls = Counter(r['role'] for r in s['response_audits']); tokens = Counter()
            for r in s['response_audits']: tokens[r['role']] += r['generated_tokens']
            s['cost']['generation_calls'] = dict(calls); s['cost']['generated_tokens'] = dict(tokens)
            records[f'{i:02d}-{stage}.json'] = s
    return records


def test_all_started_completed_snapshots_remain_partial_not_gpu_evidence():
    m, a = fixture(); m.validate_partials(partial_fixture(m, a['diagnosis']), a['diagnosis'])


@pytest.mark.parametrize('case', ['missing', 'extra', 'source', 'response', 'cost', 'attempt', 'usable', 'unknown_cost'])
def test_partial_prefixes_and_unreturned_cost_cannot_be_rewritten(case):
    m, a = fixture(); records = partial_fixture(m, a['diagnosis']); s = records['07-started.json']
    if case == 'missing': records.pop('14-completed.json')
    elif case == 'extra': records['15-started.json'] = copy.deepcopy(s)
    elif case == 'source': s['source_commit'] = 'a' * 40
    elif case == 'response': s['response_audits'][0]['response_text'] += 'changed'
    elif case == 'cost': s['cost']['generated_tokens']['construction_teacher'] += 1
    elif case == 'attempt': s['generation_attempts'][-1]['completed'] = True
    elif case == 'usable': s['diagnostic_outputs_usable'] = True
    elif case == 'unknown_cost': s['unreturned_generation_cost_measured'] = True
    with pytest.raises((ValueError, KeyError)): m.validate_partials(records, a['diagnosis'])
