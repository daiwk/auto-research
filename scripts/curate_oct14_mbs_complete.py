#!/usr/bin/env python3
"""Strict full MBS evidence curation; fixtures/replays are not GPU execution.

Private raw responses are consumed only by CPU replay/external verification.
The public envelope never includes prompts, labels, token IDs or machine data.
"""
from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import importlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import tarfile

from auto_research.gpu_validation import validate_gpu_receipt

ROOT=Path(__file__).resolve().parents[1]
SOURCE_COMMIT='4c4710cdb82947eddcea4df7c598553238f2c60d'
CHECKPOINT_SOURCE_SHA='ea65949d28c24fd50c57bb1fcdc405245a0c9cc3834c7aae2c3ca501ae071762'
_spec=importlib.util.spec_from_file_location('mbs_historical_contract',ROOT/'scripts/curate_oct14_mbs_schema_failure.py')
_legacy=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_legacy)
CONFIG={**_legacy.CONFIG,'construction_teacher_sample':False}
# Actual new CPU source/config/observer preparation is not a GPU success. Only
# matching real run/exit/response/update evidence can produce a passed receipt.
RUN_BINDING={
    'canonical_config_sha256':'7ec83b1195754077ec80174bed36b0d0db217eee386495496a9cf2f9ebc68a2c',
    'config_raw_sha256':'00cd169f63c9fe00538ebd05cd050b433101d8c94f68d02e3dadecea2de4e90a',
    'source_map_sha256':'8ca56f18f053a07038418c9283356d1d7790c9719e4efa2820519528b405b965',
    'source_contract_sha256':'96f4ba0f67d757afd52dfca5848f1946e49eddb79a34e5c797b815dabb4050b3',
    'source_archive_sha256':'332d1f2c00f8410acf29213e782e0c6b6f47311d9789bf621ed8e4a10f09eba1',
    'plan_sha256':'b103e8fd5bcb1214426139e8775d55cc1edc77643856c09067e64fb40eba7847',
    'resource_audit_sha256':'a8035b0053ca982d7f6d9a50c1a395592724e8cb7b926389fc686e93647b1a4d',
    'grammar_audit_sha256':'8a9405ef3a0e4bb9d7f21504bf9c0970900309ef0a438fc3fc43eb44c59ef60b',
    'dependency_audit_sha256':'a0c5a4cf13642258131c4e0d1c62a686dcf35f0da37d28b3d2c4f1fd072732b1',
    'launcher_sha256':'53e8d5ad1ce1a08e29f3a61bef6f7b3d379a738e626096b291a55bc6856fe5d3',
    'base_launcher_sha256':'186a47f0e8a53b17595a52625dafdd0c8d24406c7ffe4631aa182338abd4cf30',
    'preflight_sha256':'cab2e1a6b251df5e493e89bd0bc2a55e0bf7d896e9ab5f9c1bb08ecad29858b2',
    'compiler_sha256':'5de87a96ec40363ba33f3b316d32e31947e5bade1f7835b9229621df081bfddc',
    'gpu_slot_grant':'A100-post-training-greedy-4c4710cd-explicit-slot',
    'job_key':'magicbeanstalk-schema-greedy','seeds':[42],
    'command':['/tmp/jev-closeout-venv/bin/python','-u','/tmp/auto-research-oct14-4c4710cd/scripts/run_oct13_post_training.py',
        '--method','magicbeanstalk','--config','/tmp/auto-research-post-training-greedy-4c4710cd/oct14_execution-mbs-greedy-4c4710cd-v1.json',
        '--seed','42','--output','/tmp/auto-research-oct14-4c4710cd/runs/post-training-oct14/oct14-mbs-schema-greedy42-attempt08/magicbeanstalk-schema-greedy-s42/evidence']}


def require(condition,message):
    if not condition:raise ValueError(message)


def sha(content):
    return hashlib.sha256(content).hexdigest()


def finite_tree(value):
    if type(value) is float:require(math.isfinite(value),'finite actual evidence required')
    elif isinstance(value,dict):
        for child in value.values():finite_tree(child)
    elif isinstance(value,list):
        for child in value:finite_tree(child)


def optimizer_checks(history,config,*,method):
    require(isinstance(history,list) and len(history)==config['steps'],'all original optimizer groups required')
    updates=zero=0
    for index,step in enumerate(history):
        require(step.get('step')==index+1,'ordered actual optimizer step required')
        rewards=step.get('rewards')
        require(isinstance(rewards,list) and len(rewards)==config['group']
            and all(type(value) in (int,float) and value in (0,1) for value in rewards),'actual binary group outcomes required')
        equal=len(set(rewards))==1
        if equal:
            require(step.get('zero_advantage_group') is True and step.get('optimizer_update_executed') is False,
                'equal rewards must retain a real zero-update group')
            require(not any(step.get('advantages',[])),'zero group cannot carry artificial advantages')
            zero+=1
        else:
            mean=sum(rewards)/len(rewards);expected=[value-mean for value in rewards]
            require(step.get('zero_advantage_group') is False and step.get('optimizer_update_executed') is True
                and isinstance(step.get('advantages'),list) and len(step['advantages'])==len(expected)
                and all(type(value) in (int,float) and math.isfinite(value) and math.isclose(value,target,abs_tol=1e-6)
                    for value,target in zip(step['advantages'],expected,strict=True))
                and type(step.get('loss')) in (int,float) and math.isfinite(step['loss'])
                and type(step.get('gradient_l2_norm')) in (int,float) and math.isfinite(step['gradient_l2_norm'])
                and step['gradient_l2_norm']>0,'actual finite loss/nonzero gradient and original centered rewards required')
            updates+=1
    require(not method or updates>0,'method must execute a genuine nonzero optimizer update')
    return updates,zero


def construction_replay(raw,config,train):
    """Replay the frozen construction calls; never instantiate/generate a model."""
    from auto_research.post_training.oct13_common import CostLedger
    from auto_research.post_training.response_policy import GeneratedResponse
    from auto_research.reproductions.magicbeanstalk import checkpoint
    from auto_research.reproductions.magicbeanstalk.algorithm import MagicBeanStalk
    traces=raw['construction_response_audits']
    require(isinstance(traces,list) and bool(traces),'all original construction response audits required')
    class ReplayPolicy:
        pass  # no model, tokenizer, generate method or answer-bearing policy
    teacher,student=ReplayPolicy(),ReplayPolicy()
    class ReplayLedger(CostLedger):
        def __init__(self):super().__init__();self.position=0
        def sample(self,policy,messages,*,role='student',samples=1,max_tokens=512,sample=True,json_schema=None):
            group=traces[self.position:self.position+samples]
            require(len(group)==samples and max_tokens==config['max_tokens'],'all actual bounded responses must remain')
            responses=[]
            for row in group:
                require(row.get('role')==role and row.get('sample') is sample,'actual role-specific sampling and ordering required')
                tokens=row.get('response_token_ids');text=row.get('response_text')
                require(isinstance(tokens,list) and 0<len(tokens)<=max_tokens and all(type(token) is int and token>=0 for token in tokens)
                    and len(tokens)==row.get('generated_tokens') and isinstance(text,str)
                    and sha(text.encode())==row.get('response_text_sha256') and type(row.get('truncated')) is bool,
                    'actual private response SHA/tokens/termination required')
                if role=='construction_teacher':
                    require(policy is teacher and sample is False and json_schema is not None,'only construction teacher receives fixed schema')
                    expected=sha(json.dumps(json_schema,separators=(',',':'),allow_nan=False).encode())
                    require(row.get('json_schema_constrained') is True and row.get('json_schema_backend')=='xgrammar-hf'
                        and row.get('xgrammar_version')=='0.2.8' and row.get('json_schema_sha256')==expected,
                        'actual structure-only compiler metadata differs')
                    teacher.last_json_schema_generation={'backend':'xgrammar-hf','version':'0.2.8','schema_sha256':expected}
                else:require(json_schema is None,'student and independent verifier must not receive schema')
                responses.append(GeneratedResponse(tuple(tokens),text,row['truncated']))
            self.position+=samples
            self.calls[role]=self.calls.get(role,0)+1
            self.generated_tokens[role]=self.generated_tokens.get(role,0)+sum(len(response.tokens) for response in responses)
            return responses
    ledger=ReplayLedger()
    backend=checkpoint.CheckpointConstruction(teacher,student,ledger,max_tokens=config['max_tokens'],rollouts=config['group'],
        teacher_attempts=config['teacher_attempts'],construction_json_schema=True,construction_teacher_sample=False)
    builder=MagicBeanStalk(backend,depth=config['depth'],decomposition_retries=config['decomposition_retries'],
        synthesis_retries=config['synthesis_retries'])
    try:
        synthetic,controls,selection=checkpoint.construct_paired_hard_roots(train[:config['train_examples']],backend,builder,
            hard_root_limit=config['hard_root_limit'])
    except (KeyError,IndexError,AttributeError,StopIteration,TypeError) as exc:
        raise ValueError('incomplete or malformed actual construction replay') from exc
    require(ledger.position==len(traces) and backend.response_audits==traces,'all actual roles/rewards/schema/gold-scopes must replay exactly')
    require(builder.audit==raw['construction_audits'] and selection==raw['hard_root_selection'],
        'all original hard/effectivity/verification/synthesis/Goldilocks/paired-root gates must replay exactly')
    require(len(synthetic)==len(controls)==raw['synthetic_problem_count'] and len(synthetic)>0,
        'at least one complete verified effectivity/novelty/Goldilocks descendant and matched control required')
    phases=Counter(row['phase'] for row in builder.audit if row.get('accepted') is True)
    require(phases['effectivity']>0 and phases['leaf-synthesis']>=2 and phases['parent-synthesis']>0
        and phases['target-policy-goldilocks']>0,'all defining top-down and bottom-up stages required')
    return ledger,phases,len(synthetic)


def validate_core(raw,config,train):
    """Pure CPU core checks; only outer immutable runtime binding can sign GPU."""
    finite_tree(raw)
    require(all(config.get(key)==value and type(config.get(key)) is type(value) for key,value in CONFIG.items()),
        'original fixed profile and budgets required')
    require(raw.get('method')=='magicbeanstalk' and raw.get('seed') in (42,43,44) and raw.get('device')=='cuda'
        and raw.get('diagnostic_only') is True and raw.get('promotion_eligible') is False
        and raw.get('parameters_changed') is True and raw.get('construction_teacher_sample') is False,
        'actual changed method policy and diagnostic role boundaries required')
    require(raw.get('control',{}).get('method')=='seed-rlvr','actual matched seed-RL control required')
    ledger,phases,count=construction_replay(raw,config,train)
    method_updates,method_zero=optimizer_checks(raw.get('training'),config,method=True)
    control_updates,control_zero=optimizer_checks(raw['control'].get('training'),config,method=False)
    for metric in (raw['baseline'],raw['method_metrics'],raw['control']['metrics']):
        require(set(metric)=={'accuracy','examples','generated_tokens','truncated_responses'}
            and metric['examples']==config['validation_examples']
            and type(metric['accuracy']) in (int,float) and 0<=metric['accuracy']<=1
            and type(metric['generated_tokens']) is int and 0<metric['generated_tokens']<=config['validation_examples']*config['max_tokens']
            and type(metric['truncated_responses']) is int and 0<=metric['truncated_responses']<=config['validation_examples'],
            'all three actual external validation measurements required')
    cost=raw['cost'];calls=cost['generation_calls'];tokens=cost['generated_tokens'];scores=cost['scored_response_tokens']
    expected_calls={**ledger.calls,'mbs_rlvr':config['steps'],'seed_rlvr_control':config['steps'],'evaluation':3*config['validation_examples']}
    require(set(cost)=={'generation_calls','generated_tokens','scored_response_tokens','frozen_encoder_forward_calls',
        'frozen_encoder_input_tokens_including_prompt','scope','includes_rejected_and_profiling_generations'}
        and calls==expected_calls and set(tokens)==set(calls)
        and cost.get('includes_rejected_and_profiling_generations') is True
        and cost.get('scope')=='entire invocation, including training controls, profiling and evaluation'
        and cost.get('frozen_encoder_forward_calls')==cost.get('frozen_encoder_input_tokens_including_prompt')==0,
        'all actual construction/method/control/evaluation costs required')
    for role,value in tokens.items():
        group=config['group'] if role in ('target_calibration','effectivity_student','effectivity_teacher','mbs_rlvr','seed_rlvr_control') else 1
        require(type(value) is int and 0<value<=calls[role]*group*config['max_tokens'],'realized tokens must stay within unchanged group caps')
        if role in ledger.generated_tokens:require(value==ledger.generated_tokens[role],'cost must equal every original construction response length')
    require(tokens['evaluation']==sum(metric['generated_tokens'] for metric in (raw['baseline'],raw['method_metrics'],raw['control']['metrics'])),
        'all original validation tokens must remain charged')
    updates=method_updates+control_updates
    require(set(scores)=={'behavior','student_rl'} and all(type(value) is int and updates*config['group']<=value<=updates*config['group']*config['max_tokens'] for value in scores.values())
        and scores['behavior']==scores['student_rl'] and scores['behavior']<=tokens['mbs_rlvr']+tokens['seed_rlvr_control'],
        'actual scored tokens must correspond to real nonzero policy groups, not fake updates')
    teacher_tokens=sum(value for role,value in tokens.items() if role in ('construction_teacher','construction_verification','effectivity_teacher'))
    student_tokens=sum(tokens.values())-teacher_tokens
    require(teacher_tokens<=_legacy.LAUNCH_BUDGET['teacher_generated_tokens_upper']
        and student_tokens<=_legacy.LAUNCH_BUDGET['student_generated_tokens_upper']
        and sum(scores.values())<=_legacy.LAUNCH_BUDGET['student_scored_response_tokens_upper'],
        'original total generation/scoring safety bounds must remain unchanged')
    return {'full_frozen_construction_replay_exact':True,'synthetic_problem_count':count,'accepted_core_phases':dict(phases),
        'method_optimizer_updates':method_updates,'method_zero_advantage_groups':method_zero,
        'control_optimizer_updates':control_updates,'control_zero_advantage_groups':control_zero,
        'runtime_parameters_changed':True,'parameter_change_basis':'frozen run compares actual trainable digests; raw does not expose those digests',
        'control_parameter_change_hash_claimed':False,'measured_cost':cost}


def validate_binding(*,launch,exit_record,contract,audit,dependency_audit,grammar_audit,config,git_hashes,raw_hashes):
    require(isinstance(RUN_BINDING,dict),'new actual immutable config/observer pins have not yet been supplied')
    for value in (launch,exit_record,contract,audit,dependency_audit,grammar_audit,config):finite_tree(value)
    hashes=contract['source_file_sha256'];canonical=sha(json.dumps(config,sort_keys=True).encode())
    require(contract.get('source_commit')==SOURCE_COMMIT and set(hashes)==_legacy.SOURCE_PATHS
        and all(_legacy.hash_string(value) for value in hashes.values()) and hashes==git_hashes
        and sha(json.dumps(hashes,sort_keys=True).encode())==RUN_BINDING['source_map_sha256']
        and hashes['src/auto_research/reproductions/magicbeanstalk/checkpoint.py']==CHECKPOINT_SOURCE_SHA,
        'all54 source files and actual checkpoint implementation must match frozen Git blobs')
    for record in (launch,audit):
        require(record.get('source_commit')==SOURCE_COMMIT and record.get('source_file_sha256')==hashes
            and record.get('execution_config_sha256')==canonical==RUN_BINDING['canonical_config_sha256'],
            'actual source/config contract, CPU audit and observer must agree')
    require(set(raw_hashes)=={'launch','exit','runtime','result','source_contract','resource_audit','config','grammar_audit','dependency_audit','source_archive',
        'plan','launcher_source','preflight_source','compiler_source','base_launcher_source'}
        and all(_legacy.hash_string(value) for value in raw_hashes.values())
        and raw_hashes['config']==RUN_BINDING['config_raw_sha256']
        and raw_hashes['source_archive']==RUN_BINDING['source_archive_sha256'],
        'all original immutable raw/source/config artifact hashes required')
    for field,pin in (('source_contract','source_contract_sha256'),('resource_audit','resource_audit_sha256'),
        ('grammar_audit','grammar_audit_sha256'),('dependency_audit','dependency_audit_sha256'),('plan','plan_sha256'),
        ('launcher_source','launcher_sha256'),('preflight_source','preflight_sha256'),('compiler_source','compiler_sha256'),
        ('base_launcher_source','base_launcher_sha256')):
        require(raw_hashes[field]==RUN_BINDING[pin],'actual independently hashed observer/audit/source preparation differs: '+field)
    require(audit.get('source_hashes_verified') is True and audit.get('cuda_initialized') is False
        and audit.get('model_instantiated') is False and audit.get('exact_vocabulary_match') is True
        and audit.get('public_train_only_holdout')==_legacy.DATASET,'actual train-only independent CPU audit required')
    require(audit.get('source_marker_verified') is True and audit.get('source_marker_commit')==SOURCE_COMMIT
        and audit.get('preflight_source_sha256')==RUN_BINDING['preflight_sha256'],'actual fresh immutable marker/preflight binding required')
    c=launch['effective_config'];effective={**config['shared'],**config['methods']['magicbeanstalk']}
    require(c==effective and set(c)==set(CONFIG)|_legacy.PATH_FIELDS
        and all(c.get(key)==value and type(c.get(key)) is type(value) for key,value in CONFIG.items())
        and all(isinstance(c.get(key),str) and c[key] for key in _legacy.PATH_FIELDS),'exact original budget and greedy construction-only profile required')
    packages=dependency_audit['packages']
    require(set(packages)==set(_legacy.PINNED) and all(packages[key].get('version')==value for key,value in _legacy.PINNED.items())
        and dependency_audit.get('dependency_fingerprint')==sha(json.dumps(packages,sort_keys=True).encode())
        and launch.get('schema_dependency_binding')==dependency_audit
        and dependency_audit.get('cuda_initialized') is False and dependency_audit.get('model_instantiated_by_audit') is False,
        'actual fixed optional dependency bytes/version audit binding required')
    require(dependency_audit.get('not_gpu_receipt') is True and dependency_audit.get('dependency_modules_imported_by_audit') is False,
        'dependency CPU audit must not be passed model evidence')
    overlay={}
    for package in packages.values():
        files=package.get('package_file_sha256',{})
        require(files and all(_legacy.hash_string(value) for value in files.values()),'all audited dependency file bytes required')
        overlay.update(files)
    require(grammar_audit.get('algorithm_commit')==SOURCE_COMMIT and grammar_audit.get('source_file_sha256')==hashes
        and grammar_audit.get('cuda_initialized') is False and grammar_audit.get('model_loaded') is False
        and grammar_audit.get('tokenizer_sha256')==_legacy.TOKENIZER_SHA and grammar_audit.get('vocab_size')==152064
        and grammar_audit.get('versions')==_legacy.PINNED
        and grammar_audit.get('operations')=={operation:{'actual_compilation_completed':True,'schema_sha256':digest}
            for operation,digest in _legacy.ORDERED_SCHEMA_SHAS.items()}
        and len(grammar_audit.get('overlay_file_sha256',{}))==203
        and all(overlay.get(path)==digest for path,digest in grammar_audit['overlay_file_sha256'].items())
        and launch.get('schema_grammar_binding')==grammar_audit and launch.get('schema_grammar_cpu_audit_sha256')==raw_hashes['grammar_audit'],
        'actual frozen five-schema compilation and overlay audit binding required')
    require(grammar_audit.get('source_marker_verified') is True and grammar_audit.get('source_marker_commit')==SOURCE_COMMIT
        and grammar_audit.get('compiler_helper_source_sha256')==RUN_BINDING['compiler_sha256']
        and grammar_audit.get('resource_audit_sha256')==raw_hashes['resource_audit']
        and grammar_audit.get('construction_schema_imported_from_actual_frozen_checkpoint') is True
        and grammar_audit.get('processor_imported_from_actual_frozen_response_policy') is True,'actual new-source compiler/report binding required')
    checkpoints={}
    for role in ('student','teacher'):
        resource=audit['resources'][role];files=resource['file_sha256']
        require(resource.get('verified') is True and resource.get('public_id')==CONFIG[role+'_id']
            and resource.get('revision')==CONFIG[role+'_revision'] and set(files)==_legacy.RESOURCE_FILES[role]
            and all(_legacy.hash_string(value) for value in files.values())
            and files['tokenizer.json']==_legacy.TOKENIZER_SHA
            and all(files.get(name)==digest for name,digest in _legacy.WEIGHTS[role].items())
            and _legacy.hash_string(resource.get('vocabulary_sha256')),'actual fixed public policy/teacher weights and vocabulary required')
        checkpoints[role]={key:resource[key] for key in ('public_id','revision','file_sha256')}
    require(audit['resources']['student']['vocabulary_sha256']==audit['resources']['teacher']['vocabulary_sha256'],
        'exact student/teacher vocabulary pairing required')
    seed=launch.get('seed')
    require(type(seed) is int and seed in RUN_BINDING['seeds'] and launch.get('actual_accelerator_name')=='NVIDIA A100-SXM4-80GB'
        and launch.get('diagnostic_only') is True and launch.get('formal_comparison') is False
        and launch.get('gpu_grant_received') is True and launch.get('gpu_slot_grant')==RUN_BINDING['gpu_slot_grant']
        and launch.get('launcher_source_sha256')==RUN_BINDING['launcher_sha256']
        and launch.get('base_launcher_source_sha256')==RUN_BINDING['base_launcher_sha256']
        and launch.get('construction_schema_only') is True and launch.get('independent_verifier_and_student_unconstrained') is True,
        'actual authorized diagnostic accelerator and original observer identity required')
    admission=launch.get('gpu_admission',{})
    require(admission.get('name')=='NVIDIA A100-SXM4-80GB' and admission.get('compute_processes')==[]
        and all(type(admission.get(key)) is int for key in ('used_mib','free_mib','total_mib'))
        and 0<=admission['used_mib']<=1024 and admission['free_mib']>=71680
        and admission['total_mib']>=71680 and admission['used_mib']+admission['free_mib']<=admission['total_mib']+16,
        'actual independent idle80GB accelerator admission required')
    require(launch.get('construction_teacher_sample') is False and launch.get('effectivity_and_student_sample') is True
        and launch.get('only_construction_teacher_sampling_profile_changed') is True,'actual isolated sampling profile required')
    for field,key in (('resource_cpu_audit_sha256','resource_audit'),('source_contract_sha256','source_contract'),
        ('plan_sha256','plan'),('execution_config_file_sha256','config'),('preflight_source_sha256','preflight_source')):
        require(launch.get(field)==raw_hashes[key],'actual observer raw-file binding differs: '+field)
    require(launch.get('job')=={'key':RUN_BINDING['job_key'],'method':'magicbeanstalk','overrides':{},
        'priority':'explicit-construction-greedy-single-run','timeout_seconds':1800}
        and all(launch.get('budget',{}).get(key)==value for key,value in _legacy.LAUNCH_BUDGET.items())
        and launch.get('command')==[value.replace('{seed}',str(seed)) for value in RUN_BINDING['command']],
        'actual exact argv/seed/job and original wall/computation bounds required')
    pythonpath=launch.get('runner_pythonpath','').split(':')
    require(len(pythonpath)==2 and pythonpath[0].endswith('/auto-research-oct14-4c4710cd/src')
        and pythonpath[1]==dependency_audit.get('overlay_root'),'actual immutable core/overlay import order required')
    timeout=exit_record.get('timed_out') is True
    require(type(exit_record.get('exit_code')) is int and type(exit_record.get('elapsed_seconds')) in (int,float)
        and 0<exit_record['elapsed_seconds']<=(1810 if timeout else 1800) and exit_record.get('not_a_gpu_validation_receipt') is True,
        'actual bounded launcher exit record required')
    require(exit_record.get('runtime_log_sha256')==raw_hashes['runtime'] and type(exit_record.get('timed_out')) is bool,
        'actual immutable runtime log/termination binding required')
    if exit_record['exit_code']==0:
        require(exit_record.get('raw_returncode')==0 and exit_record['timed_out'] is False
            and exit_record.get('own_process_group_terminated') is False and exit_record.get('status')=='completed',
            'successful actual child exit, not timeout or killed partial execution, required')
    if timeout:
        require(exit_record['exit_code']==124 and exit_record.get('own_process_group_terminated') is True
            and type(exit_record.get('raw_returncode')) is int and exit_record['raw_returncode']<0,
            'timeout must retain the actual killed child, never a passed partial run')
    return c,checkpoints,seed


def sanitize_guard(value):
    forbidden={'response_text','response_token_ids','question','answer','trace','hostname','host','ssh_alias','user',
        'username','driver_version','torch_build','cuda_build','student_path','teacher_path','train_path','validation_path','split_manifest'}
    def visit(item):
        if isinstance(item,dict):
            require(not set(item).intersection(forbidden),'private content/machine/weights paths must not be public')
            for child in item.values():visit(child)
        elif isinstance(item,list):
            for child in item:visit(child)
        elif isinstance(item,str):
            require(not any(text in item.lower() for text in ('/tmp/','/users/','/home/','bytedance','forge-codex','ssh ')),
                'private machine identifiers or raw filesystem paths must not be public')
    finite_tree(value);visit(value)


def curate_bundle(*,launch,exit_record,result,contract,audit,dependency_audit,grammar_audit,config,git_hashes,raw_hashes,train):
    c,checkpoints,seed=validate_binding(launch=launch,exit_record=exit_record,contract=contract,audit=audit,
        dependency_audit=dependency_audit,grammar_audit=grammar_audit,config=config,git_hashes=git_hashes,raw_hashes=raw_hashes)
    positive=exit_record['exit_code']==0
    if positive:
        require(result.get('seed')==seed and result.get('dataset')==_legacy.DATASET,'actual result seed/data pairing required')
        require(result.get('protocol',{}).get('test_opened') is False and result['protocol'].get('gold_in_student_generation') is False
            and result['protocol'].get('max_tokens')==1024 and result['protocol'].get('train_examples')==16
            and result['protocol'].get('validation_examples')==4,'actual evaluated-student gold isolation and protocol required')
        for field,role in (('checkpoint','student'),('teacher','teacher')):
            measured=result[field]
            require(measured.get('public_id')==checkpoints[role]['public_id'] and measured.get('revision')==checkpoints[role]['revision']
                and measured.get('verified_mirror',{}).get('file_sha256')==checkpoints[role]['file_sha256'],
                'actual measured checkpoint weights must equal independently audited bytes')
        # Refuse replay against newer local implementations. The model run is
        # immutable4c; a changed live algorithm must not rebind its evidence.
        for name in ('post_training.oct10_checkpoint','post_training.oct13_common','post_training.proximal_checkpoint',
            'post_training.response_policy','reproductions.magicbeanstalk.algorithm','reproductions.magicbeanstalk.checkpoint'):
            loaded=importlib.import_module('auto_research.'+name)
            relative='src/auto_research/'+name.replace('.','/')+'.py'
            require(sha(Path(loaded.__file__).read_bytes())==git_hashes[relative],
                'loaded CPU replay source must match actual frozen implementation bytes')
        checks=validate_core(result,c,train)
        metrics={phase+'.accuracy':{'mean':record['accuracy'],'std':0.,'n':1}
            for phase,record in (('initial',result['baseline']),('method',result['method_metrics']),('matched_seed_rl',result['control']['metrics']))}
        metrics.update({name:{'mean':checks[name],'std':0.,'n':1} for name in
            ('method_optimizer_updates','control_optimizer_updates','synthetic_problem_count')})
    else:
        require(isinstance(result.get('status'),str) and result['status'].startswith('failed')
            and result.get('diagnostic_only') is True,'nonzero exit must retain original failed native scope')
        finite_tree(result)
        checks={'actual_exit_code':exit_record['exit_code'],'failed_raw_retained':True,'complete_core_or_training_claimed':False}
        metrics={}
    metric_path=f'docs/reproductions/2610.12659-magicbeanstalk/metrics/public-a100-{"complete" if positive else "failed"}-seed{seed}-4c4710cd.json'
    receipt_path=f'docs/gpu-validations/magicbeanstalk-a100-20261014-seed{seed}-4c4710cd.json'
    limits=['Bounded train-only GSM8K MBS mechanism diagnostic, not original scale, formal comparison or stable capability improvement.',
        'Construction teacher sees training answers/traces; independent verifier and evaluated student never see parent gold.',
        'Independent teacher re-solving and safety/novelty judgments are actual model outcomes, not formal proofs of synthetic labels.',
        'Real matched seed-RL control can have zero advantages and zero updates; no positive control update is fabricated.',
        'Raw responses/token IDs and weights remain private; public records contain immutable hashes and measured summaries only.',
        'Raw parameter-change boolean is source-bound to an actual trainable-digest comparison; those before/after digests are not independently exposed.']
    artifact={'schema_version':2,'adapter_key':'magicbeanstalk','manifest_ref':'reproduction:magicbeanstalk','seeds':[seed],
        'measured_locally':True,'diagnostic_only':True,'promotion_eligible':False,'whole_method_gpu_validation_passed':positive,
        'not_gpu_receipt':not positive,'default_three_seed_plan_completed':False,'aggregate_metrics':metrics,
        'execution_checks':checks,'dataset':_legacy.DATASET,'checkpoint':checkpoints,
        'private_original_artifact_hashes':raw_hashes,
        'evaluation_protocol':{'tier':'l1_mechanism','seeds':[seed],'formal_comparison':False,'test_used_for_selection':False,
            'pending_seeds':[value for value in (42,43,44) if value!=seed],
            'claim_policy':'source-bound complete mechanism smoke result only' if positive else 'failed native retained; no passed GPU receipt'},
        'provenance':{'code_commit':SOURCE_COMMIT,'artifact_path':metric_path,'executed_source_sha256':git_hashes,
            'execution_config_sha256':RUN_BINDING['canonical_config_sha256'],'execution_config_raw_sha256':raw_hashes['config'],
            'source_archive_sha256':raw_hashes['source_archive'],'launcher_sha256':launch['launcher_source_sha256'],
            'dataset_fingerprint':sha(json.dumps(_legacy.DATASET,sort_keys=True).encode())},'limitations':limits}
    command=['python','-u','scripts/run_oct13_post_training.py','--method','magicbeanstalk','--config','data/oct14_execution-mbs-greedy-4c4710cd-v1.json',
        '--seed',str(seed),'--output',f'runs/magicbeanstalk-seed{seed}/evidence']
    receipt=None
    if positive:
        receipt={'schema_version':1,'adapter_key':'magicbeanstalk','validated_at':'2026-10-14','seeds':[seed],
            'accelerator':{'vendor':'NVIDIA','model':'NVIDIA A100-SXM4-80GB'},'command':command,'dataset':_legacy.DATASET,
            'checkpoint':checkpoints,'result':'passed','metrics':metrics,'execution_checks':checks,'limitations':limits,
            'executed_source_sha256':git_hashes,'private_original_artifact_hashes':raw_hashes,
            'provenance':{'commit':SOURCE_COMMIT,'artifact_path':receipt_path,'metrics_artifact':metric_path,
                'execution_config_sha256':RUN_BINDING['canonical_config_sha256'],'launcher_sha256':launch['launcher_source_sha256'],
                'checkpoint_committed':False,'command_path_relocations_only':True}}
        require(not validate_gpu_receipt(receipt),'sanitized strict GPU receipt contract failed')
    sanitize_guard(artifact)
    if receipt is not None:sanitize_guard(receipt)
    return artifact,receipt


def archive_hashes(archive_path,contract):
    """Independently derive source hashes; no caller-provided substitute."""
    hashes={}
    with tarfile.open(archive_path) as archive:
        for name in _legacy.SOURCE_PATHS:
            content=subprocess.check_output(['git','show',SOURCE_COMMIT+':'+name],cwd=ROOT)
            require(archive.extractfile(name).read()==content,'deployed source archive must equal every actual Git blob')
            hashes[name]=sha(content)
    require(hashes==contract['source_file_sha256'],'actual archive/source contract mismatch')
    return hashes


def curate_directory(directory,*,contract_path,audit_path,dependency_path,grammar_path,config_path,archive_path,
                     plan_path,launcher_path,preflight_path,compiler_path,base_launcher_path,train_path):
    paths={'launch':directory/'launch.json','exit':directory/'exit.json','runtime':directory/'runtime.log',
        'source_contract':contract_path,'resource_audit':audit_path,'dependency_audit':dependency_path,
        'grammar_audit':grammar_path,'config':config_path,'source_archive':archive_path,'plan':plan_path,
        'launcher_source':launcher_path,'preflight_source':preflight_path,'compiler_source':compiler_path,
        'base_launcher_source':base_launcher_path}
    def read(path):return json.loads(path.read_text())
    exit_record=read(paths['exit'])
    if exit_record['exit_code']==0:
        payload_path=directory/'evidence/result.json'
        require(not (directory/'evidence/failure.json').exists(),'a failed payload cannot coexist with completed evidence')
    else:
        require(not (directory/'evidence/result.json').exists(),'failed exit must not publish a complete result')
        payload_path=directory/'evidence/failure.json'
        if not payload_path.exists():payload_path=directory/'controller-failure.json'
    paths['result']=payload_path
    raw_hashes={key:sha(path.read_bytes()) for key,path in paths.items()}
    contract=read(contract_path);git_hashes=archive_hashes(archive_path,contract)
    # External CPU verification may read TRAIN labels only. Never load model
    # inputs or validation gold to tune sampling/schema or select a seed.
    data=train_path.read_bytes()
    require(sha(data)==_legacy.DATASET['partition_sha256']['train'],'actual fixed original public training bytes required for replay')
    config=read(config_path)
    count={**config['shared'],**config['methods']['magicbeanstalk']}['train_examples']
    train=[json.loads(line) for line in data.splitlines()[:count]]
    require(len(train)==count and all(isinstance(row.get('question'),str) and isinstance(row.get('answer'),str) for row in train),
        'unchanged original training prefix required; no adaptive row selection')
    return curate_bundle(launch=read(paths['launch']),exit_record=exit_record,result=read(payload_path),
        contract=contract,audit=read(audit_path),dependency_audit=read(dependency_path),grammar_audit=read(grammar_path),
        config=config,git_hashes=git_hashes,raw_hashes=raw_hashes,train=train)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-directory',type=Path,required=True)
    for name in ('contract','audit','dependency','grammar','config','archive','plan','launcher','preflight','compiler','base-launcher','train'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--native-output',type=Path,required=True)
    parser.add_argument('--receipt-output',type=Path)
    args=parser.parse_args()
    if (args.native_output.exists() or (args.receipt_output and args.receipt_output.exists())
            or (args.receipt_output and args.receipt_output.resolve()==args.native_output.resolve())):
        raise FileExistsError('prior native evidence/receipts are immutable; do not overwrite')
    artifact,receipt=curate_directory(args.run_directory,contract_path=args.contract,audit_path=args.audit,
        dependency_path=args.dependency,grammar_path=args.grammar,config_path=args.config,archive_path=args.archive,
        plan_path=args.plan,launcher_path=args.launcher,preflight_path=args.preflight,compiler_path=args.compiler,
        base_launcher_path=args.base_launcher,train_path=args.train)
    if receipt is not None and args.receipt_output is None:parser.error('complete actual evidence requires an explicit receipt output')
    args.native_output.parent.mkdir(parents=True,exist_ok=True)
    args.native_output.write_text(json.dumps(artifact,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    if receipt is not None:
        args.receipt_output.parent.mkdir(parents=True,exist_ok=True)
        args.receipt_output.write_text(json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'native':str(args.native_output),'receipt_written':receipt is not None,
        'whole_method_gpu_validation_passed':artifact['whole_method_gpu_validation_passed']}))
