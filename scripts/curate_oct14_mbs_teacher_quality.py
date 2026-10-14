#!/usr/bin/env python3
"""Stdlib-only frozen teacher-quality curation; stdout draft, never a receipt."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess

_spec = importlib.util.spec_from_file_location('quality_resource_contract', Path(__file__).with_name('curate_oct14_mbs_schema_failure.py'))
BASE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BASE)
RUNNER_COMMIT = 'dd54035dd3d52f2c841d633b4d494ce471b6ead4'
CORE_COMMIT = 'ce4a4a34520419a50fb730d93967aaed5024fa77'
RUNNER = 'scripts/diagnose_oct14_mbs_teacher_quality.py'
RUNNER_SHA = '6f863bbb4ea2f7f386875b1249cc0b326e534cf651627db461326de53d3724d5'
LAUNCHER_SHA = 'a784061d811380e002f52cd15ffa6c5006acec2b79552fcab3869d1caf215761'
TEACHER_ID, TEACHER_REVISION = BASE.CONFIG['teacher_id'], BASE.CONFIG['teacher_revision']
SCHEMA_SHA = 'b60afb6eb71743e2e47aec78354124df48a40d97b48591592c0214c0c30b29d4'
ROOT_HASHES = {4: 'd38bacc8724a241927dec39e1459b3c17295f79d244c7ec4a518303968c9dc01',
    7: 'a13430e732d2c1e663238de0e34daf75abd640df18ff2ab97d0d55479204c2d1',
    8: '699ab79580f3d4e07173fdf9ff3b39ab4d4aa99e3efdf92ea650753c03c27a4d'}
VALIDATION_HASHES = ['16f83fb4320c9faf79cc5ef0cf235beb70b19a06e9e4dc4f03dd9d0ca78d5e75',
    '09296cd5e0fc1cb5a7c241379aa53704fca1c2d3cf3e106fdf539f2f88d050c1',
    '0d821abd5ff6387beebe8e03e8b65d7d60b768da13413eead9e6040c9f308df5',
    '0483f22415df4974ea7a835bd7aa7d80ae6cd41c0d70ec27518875a1579d8b3a']
CAPS = {'training_roots': [4, 7, 8], 'validation_prefix': 4, 'response_cap': 1024, 'outputs_upper': 14,
    'generated_tokens_upper': 14336, 'wall_cap_seconds': 600, 'student_generation_calls': 0, 'optimizer_updates': 0}
CALLS = {'train_root_greedy': 3, 'construction_teacher': 1, 'train_child_greedy': 2,
    'validation_current-t1': 4, 'validation_greedy': 4}
DATASET = {'source_revision': '3101c7d5072418e28b9008a6636bde82a006892c',
    'split_manifest_sha256': 'c0b9b2424d9b497e4b7f6c0188ac0c0a9235bf151a046d559fb181f44e10bcbd',
    'partition_sha256': BASE.DATASET['partition_sha256'], 'validation_content_read': True, 'test_content_read': False,
    'training_prefix': 16, 'selected_training_indices': [4, 7, 8], 'validation_prefix': 4,
    'prior_calibration_failure_sha256': '19c56c036b6dd87f7658c14a7c45c53065a662c920cc807532ce6bbbdba6151d',
    'target_hardness_recalibrated': False}
GOLD_SCOPES = {'root_and_child_solving': 'question only; gold external scorer',
    'construction_teacher': 'verified TRAIN parent trace and train answer allowed',
    'validation_teacher': 'question only; validation answer external scorer'}
OPERATOR_PATHS = {'src/auto_research/public_holdout.py', 'src/auto_research/oct12_public_sources.py',
    *{'src/auto_research/post_training/' + p + '.py' for p in ('oct10_checkpoint', 'response_policy', 'proximal_checkpoint', 'oct13_common')},
    *{'src/auto_research/reproductions/' + p for p in ('gppo_framework/__init__.py', 'gppo_framework/objective.py',
        'tapo_trajectory/__init__.py', 'tapo_trajectory/objective.py', 'magicbeanstalk/__init__.py',
        'magicbeanstalk/algorithm.py', 'magicbeanstalk/checkpoint.py')}}
REQUIRED_FLAGS = {'artifact_kind': 'mbs_teacher_quality_diagnostic_not_gpu_receipt', 'method': 'magicbeanstalk',
    'seed': 42, 'diagnostic_only': True, 'not_gpu_receipt': True, 'whole_method_gpu_validation_passed': False,
    'formal_comparison': False, 'promotion_eligible': False, 'validation_content_read': True, 'test_content_read': False,
    'student_instantiated': False, 'student_generation_calls': 0, 'lora_updates': 0, 'optimizer_updates': 0,
    'concurrent_latency_comparison_eligible': False, 'formal_mbs_sampling_changed': False, 'scaffold_safety_executed': False,
    'effectivity_executed': False, 'synthesis_executed': False, 'goldilocks_executed': False,
    'greedy_construction_wrapper_is_diagnostic_only': True, 'backbone_parameters_frozen': True,
    'unreturned_generation_cost_measured': True, 'formal_mbs_assessment_executed': False,
    'student_assessment_executed': False, 'teacher_validation_executed': True, 'diagnostic_outputs_usable': True}
SOLVER_PREFIX = 'Solve the problem carefully and end with the numerical answer in \\boxed{...}.\n'
RAW_KEYS = {'launch', 'exit', 'runtime', 'diagnosis', 'runner_contract', 'cpu_audit', 'core_contract', 'core_audit', 'config', 'dependency_audit'}
EXPECTED_ARGV = ['/tmp/jev-closeout-venv/bin/python', '-u', '/tmp/auto-research-oct14-dd54035d/' + RUNNER,
    '--config', '/tmp/oct14-mbs-order-ce4a4a34-queue/oct14_execution-mbs-schema-v1.json',
    '--algorithm-root', '/tmp/auto-research-oct14-ce4a4a34', '--algorithm-contract', '/tmp/oct14-mbs-order-ce4a4a34-queue/source-contract-ce4a4a34.json',
    '--algorithm-audit', '/tmp/oct14-mbs-order-ce4a4a34-queue/resource-audit-a100-cpu-ce4a4a34-mbs-order-01.json',
    '--source-root', '/tmp/auto-research-oct14-dd54035d', '--contract', '/tmp/oct14-mbs-quality-dd54035d/mbs-quality-source-dd54035d.json',
    '--audit', '/tmp/oct14-mbs-quality-dd54035d/cpu-audit-dd54035d.json', '--overlay-root', '/tmp/auto-research-oct14-xgrammar028',
    '--dependency-audit', '/tmp/oct14-mbs-order-ce4a4a34-queue/schema-dependency-audit-a100-xgrammar028-01.json',
    '--output', '/tmp/oct14-mbs-quality-dd54035d/attempt01/evidence', '--execute', '--gpu-grant', 'A100-MBS-teacher-quality-explicit-slot']


def require(condition, message):
    if not condition: raise ValueError(message)


def sha(content):
    return hashlib.sha256(content).hexdigest()


def canonical(value):
    return sha(json.dumps(value, sort_keys=True).encode())


def numeric_answer(text):
    """Same frozen strict extraction; no arithmetic repair or float equivalence."""
    if '####' in text: text = text.rsplit('####', 1)[-1]
    boxed = re.findall(r'\\boxed\{([^{}]+)\}', text)
    if boxed: text = boxed[-1]
    values = re.findall(r'-?\d[\d,]*(?:\.\d+)?', text)
    return values[-1].replace(',', '') if values else None


def solver_question(attempt):
    messages = attempt['actual_messages']
    require(isinstance(messages, list) and len(messages) == 1 and set(messages[0]) == {'role', 'content'}
        and messages[0]['role'] == 'user' and isinstance(messages[0]['content'], str)
        and messages[0]['content'].startswith(SOLVER_PREFIX), 'exact question-only solver interface required')
    return messages[0]['content'][len(SOLVER_PREFIX):]


def curate_bundle(*, launch, exit_record, diagnosis, runner_contract, cpu_audit, core_contract, core_audit,
                  source_git_hashes, algorithm_git_hashes, config_sha256, raw_hashes):
    for value in (launch, exit_record, diagnosis, runner_contract, cpu_audit, core_contract, core_audit): BASE.finite_tree(value)
    d = diagnosis
    require(set(raw_hashes) == RAW_KEYS and all(BASE.hash_string(v) for v in raw_hashes.values()), 'all ten actual source/audit/raw hashes required')
    runner_hashes = {RUNNER: RUNNER_SHA}
    require(runner_contract == {'source_commit': RUNNER_COMMIT, 'source_file_sha256': runner_hashes}
        and source_git_hashes == runner_hashes and d['source_commit'] == RUNNER_COMMIT
        and d['diagnostic_runner_sha256'] == RUNNER_SHA, 'actual dd540 runner Git/source binding required')
    hashes = core_contract['source_file_sha256']
    require(core_contract['source_commit'] == CORE_COMMIT and set(hashes) == BASE.SOURCE_PATHS and len(hashes) == 54
        and all(BASE.hash_string(v) for v in hashes.values()) and algorithm_git_hashes == hashes
        and d['algorithm_commit'] == CORE_COMMIT and d['algorithm_source_file_sha256'] == hashes, 'all 54 actual ce4 Git blobs required')
    require(cpu_audit['source_commit'] == RUNNER_COMMIT and cpu_audit['source_file_sha256'] == runner_hashes
        and cpu_audit['artifact_kind'] == 'read_only_cpu_resource_audit_not_gpu_receipt'
        and cpu_audit['source_hashes_verified'] is True and cpu_audit['cuda_initialized'] is False
        and cpu_audit['model_instantiated'] is False and cpu_audit['algorithm_commit'] == CORE_COMMIT
        and cpu_audit['algorithm_source_sha256'] == hashes and cpu_audit['teacher_checkpoint_verified_again'] is True
        and cpu_audit['not_gpu_receipt'] is True and cpu_audit['actual_prefix_counts'] == {'train': 16, 'validation': 4}, 'independent frozen CPU audit required')
    imported = {p: hashes[p] for p in OPERATOR_PATHS}
    require(d['actually_imported_operator_files_sha256'] == imported == cpu_audit['actually_imported_operator_files_sha256'], 'actual imported operator scope mismatch')
    require(config_sha256 == BASE.CONFIG_SHA == d['execution_config_sha256'] == cpu_audit['execution_config_sha256']
        == core_audit['execution_config_sha256'] and core_audit['source_commit'] == CORE_COMMIT
        and core_audit['source_file_sha256'] == hashes and core_audit['source_hashes_verified'] is True
        and core_audit['cuda_initialized'] is False and core_audit['model_instantiated'] is False, 'original config/core CPU audit required')
    require(d['dataset'] == DATASET == cpu_audit['dataset'] and core_audit['public_train_only_holdout'] == BASE.DATASET, 'unchanged public partition/revision boundary required')
    require(d['configured_caps'] == CAPS == cpu_audit['diagnostic_caps'] and d['wall_cap_seconds'] == d['external_controller_wall_cap_required_seconds'] == 600, 'unchanged teacher-only bounds required')
    require(all(d.get(k) == v and type(d.get(k)) is type(v) for k, v in REQUIRED_FLAGS.items())
        and d['diagnosis_status'] == 'completed-teacher-quality-diagnostic' and d['gold_access_roles'] == GOLD_SCOPES, 'diagnostic/gold/frozen/no-student/no-optimizer scope must remain explicit')
    require(launch['argv'] == EXPECTED_ARGV and launch['launcher_sha256'] == LAUNCHER_SHA
        and launch['cpu_audit_sha256'] == raw_hashes['cpu_audit'] and launch['diagnostic_source_commit'] == RUNNER_COMMIT
        and launch['diagnostic_source_sha256'] == RUNNER_SHA and launch['algorithm_commit'] == CORE_COMMIT
        and launch['seed'] == 42 and launch['wall_cap_seconds'] == 600 and launch['outputs_upper'] == 14
        and launch['tokens_upper'] == 14336 and launch['gpu_grant'] == EXPECTED_ARGV[-1]
        and launch['auto_retry'] is False and launch['not_gpu_receipt'] is True, 'exact actual bounded argv/launch required')
    require(type(exit_record['exit_code']) is int and type(exit_record['raw_returncode']) is int
        and exit_record['exit_code'] == exit_record['raw_returncode'] == 0 and exit_record['status'] == 'completed'
        and exit_record['not_gpu_receipt'] is True and exit_record['runtime_sha256'] == raw_hashes['runtime']
        and type(d['actual_elapsed_seconds']) in (int, float) and type(exit_record['elapsed_seconds']) in (int, float)
        and 0 < d['actual_elapsed_seconds'] <= exit_record['elapsed_seconds'] <= 600, 'actual completed bounded diagnostic exit/wall required')
    require(d['accelerator'] == {'vendor': 'NVIDIA', 'model': 'NVIDIA A100-SXM4-80GB'}
        and type(d['actual_max_memory_allocated_bytes']) is int and type(d['actual_max_memory_reserved_bytes']) is int
        and 0 < d['actual_max_memory_allocated_bytes'] <= d['actual_max_memory_reserved_bytes'] <= 24 * 1024**3, 'actual bounded A100 allocator observation required')
    admission = launch['admission']
    require(admission['model'] == 'NVIDIA A100-SXM4-80GB' and admission['existing_compute_process_count'] == 1
        and admission['exclusive_latency_comparison'] is False and BASE.hash_string(launch['concurrent_skill_launch_sha256']), 'actual non-exclusive admission; no latency comparison required')
    dep = d['schema_dependency_binding']; packages = dep['packages']
    require(set(packages) == set(BASE.PINNED) and all(packages[k]['version'] == v for k, v in BASE.PINNED.items())
        and canonical(packages) == dep['dependency_fingerprint'] == cpu_audit['dependency_fingerprint']
        and dep['cuda_initialized'] is False and dep['model_instantiated_by_audit'] is False
        and dep['dependency_modules_imported_by_audit'] is False and d['schema_dependency_audit_sha256'] == raw_hashes['dependency_audit'], 'fixed XGrammar dependency audit binding required')
    checkpoint = d['checkpoint']; mirrored = checkpoint['verified_mirror']; resource = core_audit['resources']['teacher']
    files = mirrored['file_sha256']
    require(checkpoint['public_id'] == mirrored['public_id'] == resource['public_id'] == TEACHER_ID
        and checkpoint['revision'] == mirrored['revision'] == resource['revision'] == TEACHER_REVISION
        and resource['verified'] is True and files == resource['file_sha256'] and set(files) == BASE.RESOURCE_FILES['teacher']
        and all(BASE.hash_string(h) for h in files.values()) and files['tokenizer.json'] == BASE.TOKENIZER_SHA
        and all(files[p] == h for p, h in BASE.WEIGHTS['teacher'].items()), 'fixed full teacher bytes/revision required')
    responses, attempts = d['response_audits'], d['generation_attempts']
    require(d['actual_output_count'] == len(responses) == len(attempts) == 14, 'all fourteen outputs/attempts must remain')
    roles, tokens, safe = Counter(), Counter(), []
    questions = []
    for r, a in zip(responses, attempts, strict=True):
        role = r['role']; constrained = role == 'construction_teacher'; sampled = role == 'validation_current-t1'
        require(role in CALLS and a['role'] == role and r['sample'] is sampled and a['sample'] is sampled
            and a['completed'] is True and a['actual_responses'] == 1 and a['max_tokens'] == 1024
            and a['json_schema_constrained'] is constrained
            and a['input_gold_scope'] == ('training-construction-context' if constrained else 'question-only-no-answer-or-trace'), 'actual role/gold/sampling bound mismatch')
        ids = r['response_token_ids']
        require(isinstance(r['response_text'], str) and sha(r['response_text'].encode()) == r['response_text_sha256']
            and isinstance(ids, list) and 0 < len(ids) <= 1024 and all(type(x) is int and 0 <= x < 152064 for x in ids)
            and type(r['generated_tokens']) is int and r['generated_tokens'] == len(ids)
            and r['truncated'] is False, 'actual response SHA/token count/nontruncation mismatch')
        roles[role] += 1; tokens[role] += len(ids)
        question = None if constrained else solver_question(a); questions.append(question)
        safe.append({'role': role, 'sample': sampled, 'response_text_sha256': r['response_text_sha256'],
            'response_token_ids_sha256': sha(json.dumps(ids, separators=(',', ':')).encode()), 'generated_tokens': len(ids),
            'truncated': False, 'question_sha256': None if question is None else sha(question.encode()), 'input_gold_scope': a['input_gold_scope']})
    require(dict(roles) == CALLS and [r['role'] for r in responses] == [role for role, n in CALLS.items() for _ in range(n)], 'fixed all-output sequence required')
    require(questions[6:10] == questions[10:14] and [sha(q.encode()) for q in questions[6:10]] == VALIDATION_HASHES,
        'paired fixed validation questions must match exact original hashes')
    roots = d['training_root_solves']
    require(all(type(r['correct']) in (int, float) for r in roots)
        and roots == [{'training_index': i, 'correct': float(i == 4), 'truncated': False, 'question_sha256': ROOT_HASHES[i]} for i in (4, 7, 8)]
        and all(sha(q.encode()) == ROOT_HASHES[i] for i, q in zip((4, 7, 8), questions[:3])), 'three original TRAIN roots and all negative root results required')
    construction_messages = attempts[3]['actual_messages']
    require(len(construction_messages) == 1 and construction_messages[0]['role'] == 'user', 'original single construction message required')
    content = construction_messages[0]['content']; boundary = content.rfind('\n{"parent":')
    require(boundary >= 0, 'actual construction parent context required')
    try: context = json.loads(content[boundary + 1:])
    except json.JSONDecodeError as exc: raise ValueError('no construction-context repair') from exc
    require(set(context) == {'parent', 'ineffective_decompositions'} and context['ineffective_decompositions'] == []
        and set(context['parent']) == {'question', 'answer', 'trace'} and context['parent']['question'] == questions[0]
        and context['parent']['trace'] == responses[0]['response_text']
        and isinstance(context['parent']['answer'], str)
        and numeric_answer(context['parent']['answer']) is not None
        and numeric_answer(responses[0]['response_text']) == numeric_answer(context['parent']['answer']),
        'construct teacher sees only the actual independently solved TRAIN root4 context')
    try: children = json.loads(responses[3]['response_text'])
    except json.JSONDecodeError as exc: raise ValueError('no response repair or inner JSON extraction') from exc
    require(isinstance(children, list) and len(children) == 2 and all(BASE.schema_valid_problem(c) and list(c) == ['question', 'trace', 'answer'] for c in children), 'actual ordered two-child schema required')
    construction = d['construction_response_audits']
    require(len(construction) == 1 and construction[0]['json_schema_sha256'] == SCHEMA_SHA
        and construction[0]['diagnostic_greedy_override'] is True and construction[0]['input_gold_scope'] == 'training-construction-context'
        and construction[0]['response_text_sha256'] == responses[3]['response_text_sha256']
        and construction[0]['response_token_ids'] == responses[3]['response_token_ids']
        and construction[0]['parsing_completed'] is True and construction[0]['parsed_json_kind'] == 'list'
        and construction[0]['operation'] == 'propose_children' and construction[0]['proposed_problem_count'] == construction[0]['schema_valid_problem_count'] == 2
        and construction[0]['schema_reject_reason'] is None, 'actual greedy diagnostic construction audit required')
    proposal = d['proposal']
    require(proposal['attempted'] is True and proposal['proposed_child_count'] == proposal['verified_child_count'] == 2
        and proposal['reject_reason'] is None and len(proposal['children']) == 2, 'actual two independently correct TRAIN children required')
    for i, (child, row) in enumerate(zip(children, proposal['children'], strict=True)):
        require(type(row['independent_correct']) in (int, float)
            and row == {'question': child['question'], 'proposed_answer': str(child['answer']), 'proposed_trace': child['trace'],
            'independent_correct': 1.0, 'truncated': False} and questions[4 + i] == child['question'], 'actual proposal/independent child question mismatch')
        require(numeric_answer(str(child['answer'])) is not None
            and numeric_answer(responses[4 + i]['response_text']) == numeric_answer(str(child['answer'])),
            'independent child solver must pass the original strict numeric extraction')
    profiles = d['validation_profiles']
    expected_values = {'current-t1': [0., 1., 0., 1.], 'greedy': [1., 1., 0., 1.]}
    require(set(profiles) == set(expected_values), 'both four-row profiles must remain')
    for profile, values in expected_values.items():
        p = profiles[profile]
        sampling = {'sample': True, 'temperature': 1.0, 'top_p': 1.0, 'top_k': 0} if profile == 'current-t1' else {'sample': False}
        require(p['completed'] is True and p['sampling'] == sampling and all(type(r['correct']) in (int, float) for r in p['rows'])
            and p['rows'] == [{'validation_index': i, 'correct': v, 'truncated': False} for i, v in enumerate(values)]
            and p['accuracy'] == sum(values) / 4, 'all fixed validation successes and failures must match recorded accuracy')
    cost = d['cost']
    require(cost['generation_calls'] == CALLS and cost['generated_tokens'] == dict(tokens) and sum(tokens.values()) <= 14336
        and cost['scored_response_tokens'] == {} and cost['frozen_encoder_forward_calls'] == cost['frozen_encoder_input_tokens_including_prompt'] == 0
        and cost['includes_rejected_and_profiling_generations'] is True, 'complete actual teacher generation costs required')
    metrics = {'actual_outputs': 14, 'generated_tokens': sum(tokens.values()), 'training_root_total': 3, 'training_root_correct': 1,
        'proposed_children': 2, 'independently_correct_children': 2, 'validation_current_t1_accuracy': .5, 'validation_greedy_accuracy': .75,
        'student_generation_calls': 0, 'optimizer_updates': 0, 'diagnostic_wall_seconds': d['actual_elapsed_seconds'], 'invocation_wall_seconds': exit_record['elapsed_seconds']}
    command = ['python', '-u', RUNNER]
    for index in range(3, len(EXPECTED_ARGV)):
        value = EXPECTED_ARGV[index]
        if value.startswith('/tmp/'):
            flag = EXPECTED_ARGV[index - 1]
            value = '<' + flag.removeprefix('--') + '>' + ('/' + Path(value).name if value.endswith('.json') else '')
        command.append(value)
    dataset = {'public_id': 'openai/grade-school-math', **DATASET}
    return {'schema_version': 2, 'adapter_key': 'magicbeanstalk', 'manifest_ref': 'reproduction:magicbeanstalk',
        'method': 'mbs-teacher-quality-diagnostic', 'seeds': [42], 'diagnostic_only': True, 'promotion_eligible': False,
        'not_gpu_receipt': True, 'whole_method_gpu_validation_passed': False, 'curation_state': 'cache-draft-not-published',
        'seed_results': [{'seed': 42, 'device': 'cuda', 'return_code': 0, 'diagnostic_only': True, 'metrics': metrics}],
        'aggregate_metrics': {k: {'mean': v, 'std': 0.0, 'n': 1} for k, v in metrics.items()},
        'dataset': dataset,
        'checkpoint': {'public_id': TEACHER_ID, 'revision': TEACHER_REVISION, 'file_sha256': files},
        'accelerator': d['accelerator'], 'execution_checks': {'configured_caps': CAPS, 'actual_cost': cost,
            'actual_output_count': 14, 'sanitized_response_audits': safe, 'training_root_solves': roots,
            'validation_profiles': profiles, 'proposed_child_question_sha256': [sha(c['question'].encode()) for c in children],
            'ordered_schema_sha256': SCHEMA_SHA, 'dependency_versions': BASE.PINNED,
            'dependency_fingerprint': dep['dependency_fingerprint'], 'latency_or_throughput_comparison_eligible': False,
            'launch_admitted_with_existing_compute_process': True, 'concurrent_skill_launch_sha256': launch['concurrent_skill_launch_sha256'],
            'actual_max_memory_allocated_bytes': d['actual_max_memory_allocated_bytes'], 'actual_max_memory_reserved_bytes': d['actual_max_memory_reserved_bytes'],
            'student_instantiated': False, 'student_generation_calls': 0, 'optimizer_updates': 0, 'backbone_parameters_frozen': True,
            'formal_mbs_assessment_executed': False, 'effectivity_executed': False, 'synthesis_executed': False, 'goldilocks_executed': False,
            'gold_access_roles': GOLD_SCOPES},
        'evaluation_protocol': {'tier': 'l1_mechanism', 'seeds': [42], 'formal_comparison': False, 'promotion_eligible': False,
            'validation_content_read': True, 'test_content_read': False, 'greedy_override_is_diagnostic_only': True,
            'claim_policy': 'four validation examples/single seed: no stable gain, full MBS or student-training claim'},
        'provenance': {'code_commit': RUNNER_COMMIT, 'algorithm_commit': CORE_COMMIT,
            'dataset_fingerprint': canonical(dataset),
            'executed_runner_source_sha256': runner_hashes, 'executed_algorithm_source_sha256': hashes,
            'actually_imported_operator_files_sha256': imported, 'execution_config_sha256': BASE.CONFIG_SHA,
            'actual_command_sanitized': command, 'command_path_relocations_only': True,
            'raw_results_sha256': raw_hashes, 'artifact_path': '.cache/oct14-mbs-quality-dd54035d-native-draft.json',
            'raw_responses_committed': False, 'checkpoint_committed': False},
        'limitations': ['All fourteen responses and negative roots/validation rows retained; raw text/token IDs/messages omitted.',
            'Teacher-only greedy diagnostic wrapper: no student, optimizer, effectivity, scaffold safety, synthesis or Goldilocks execution.',
            'Four paired validation cases/single seed do not establish stable benefit or authorize changing formal sampling.',
            'Launch observed another compute process; walls are not exclusive latency/throughput or total-compute-savings evidence.']}


def validate_partials(records, diagnosis):
    expected = {f'{i:02d}-{stage}.json' for i in range(1, 15) for stage in ('started', 'completed')}
    require(set(records) == expected, 'all fourteen started/completed snapshots required')
    for i in range(1, 15):
        for stage in ('started', 'completed'):
            s = records[f'{i:02d}-{stage}.json']; n = i if stage == 'completed' else i - 1
            last = dict(diagnosis['generation_attempts'][i - 1])
            if stage == 'started': last.pop('actual_responses'); last['completed'] = False
            prefix = diagnosis['response_audits'][:n]
            calls = Counter(r['role'] for r in prefix); tokens = Counter()
            for r in prefix: tokens[r['role']] += r['generated_tokens']
            require(s['source_commit'] == RUNNER_COMMIT and s['algorithm_commit'] == CORE_COMMIT and s['partial_snapshot'] is True
                and s['diagnostic_runner_sha256'] == RUNNER_SHA and s['algorithm_source_file_sha256'] == diagnosis['algorithm_source_file_sha256']
                and s['diagnostic_outputs_usable'] is False and s['not_gpu_receipt'] is True and s['whole_method_gpu_validation_passed'] is False
                and s['student_generation_calls'] == s['optimizer_updates'] == 0 and s['student_instantiated'] is False
                and s['configured_caps'] == CAPS and s['actual_output_count'] == n and s['response_audits'] == prefix
                and s['generation_attempts'] == [*diagnosis['generation_attempts'][:i - 1], last]
                and s['cost']['generation_calls'] == dict(calls) and s['cost']['generated_tokens'] == dict(tokens)
                and s['unreturned_generation_cost_measured'] is (stage == 'completed'), 'actual partial progression/cost cannot be rewritten')


def curate(directory, runner_contract, cpu_audit, core_contract, core_audit, config, dependency_audit, *, repo):
    paths = {'launch': Path(directory) / 'launch.json', 'exit': Path(directory) / 'exit.json', 'runtime': Path(directory) / 'runtime.log',
        'diagnosis': Path(directory) / 'evidence/diagnosis.json', 'runner_contract': Path(runner_contract), 'cpu_audit': Path(cpu_audit),
        'core_contract': Path(core_contract), 'core_audit': Path(core_audit), 'config': Path(config), 'dependency_audit': Path(dependency_audit)}
    read = lambda p: json.loads(p.read_text())
    runner, core = read(paths['runner_contract']), read(paths['core_contract'])
    git_hashes = lambda c: {p: sha(subprocess.check_output(['git', 'show', c['source_commit'] + ':' + p], cwd=repo)) for p in c['source_file_sha256']}
    d = read(paths['diagnosis']); dep = read(paths['dependency_audit'])
    require(d['schema_dependency_binding'] == dep, 'actual dependency audit bytes must match diagnosis binding')
    result = curate_bundle(launch=read(paths['launch']), exit_record=read(paths['exit']), diagnosis=d,
        runner_contract=runner, cpu_audit=read(paths['cpu_audit']), core_contract=core, core_audit=read(paths['core_audit']),
        source_git_hashes=git_hashes(runner), algorithm_git_hashes=git_hashes(core), config_sha256=canonical(read(paths['config'])),
        raw_hashes={k: sha(p.read_bytes()) for k, p in paths.items()})
    partials = Path(directory) / 'evidence/generation-partials'
    records = {p.name: read(p) for p in partials.iterdir() if p.is_file()}
    validate_partials(records, d)
    result['provenance']['generation_partial_sha256'] = {name: sha((partials / name).read_bytes()) for name in sorted(records)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('directory', 'runner-contract', 'cpu-audit', 'core-contract', 'core-audit', 'config', 'dependency-audit', 'repo'):
        parser.add_argument('--' + name, type=Path, required=True)
    a = parser.parse_args()
    print(json.dumps(curate(a.directory, a.runner_contract, a.cpu_audit, a.core_contract, a.core_audit, a.config,
        a.dependency_audit, repo=a.repo), ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__': main()
