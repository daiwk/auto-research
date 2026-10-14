"""Synthetic CPU curation contracts only, never GPU/capability evidence."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.post_training.oct13_common import CostLedger
from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.reproductions.magicbeanstalk import checkpoint
from auto_research.reproductions.magicbeanstalk.algorithm import MagicBeanStalk

ROOT=Path(__file__).resolve().parents[1]


def module():
    spec=importlib.util.spec_from_file_location('mbs_complete_cpu',ROOT/'scripts/curate_oct14_mbs_complete.py')
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def core_fixture():
    """Raw structure built by original algorithm with explicitly fake policies."""
    class Policy:
        def __init__(self,teacher):self.teacher=teacher
        def generate(self,messages,*,samples,max_tokens,sample,json_schema=None):
            prompt=messages[0]['content']
            if json_schema is not None:
                self.last_json_schema_generation={'backend':'xgrammar-hf','version':'0.2.8',
                    'schema_sha256':hashlib.sha256(json.dumps(json_schema,separators=(',',':')).encode()).hexdigest()}
                if 'Produce exactly two' in prompt:
                    value=[{'question':'CPU child-a','trace':'CPU trace-a','answer':'7'},
                           {'question':'CPU child-b','trace':'CPU trace-b','answer':'7'}]
                elif 'Check that every child' in prompt:value={'scaffold_safe':True}
                elif 'substantively NEW' in prompt:
                    value={'question':'CPU leaf-a' if 'child-a' in prompt else 'CPU leaf-b','trace':'CPU synthetic trace','answer':'7'}
                elif 'Combine ALL' in prompt:value={'question':'CPU synthetic-parent','trace':'CPU new parent trace','answer':'7'}
                else:value={'blueprint_preserved':True,'substantive_novelty':True}
                texts=[json.dumps(value)]
            elif self.teacher:
                answer='\\boxed{0}' if any('CPU root-'+str(i) in prompt for i in (1,2,3)) else '\\boxed{7}'
                texts=['CPU independent solution to '+prompt+'\n'+answer]*samples
            elif 'Worked example:' in prompt or 'CPU leaf-' in prompt or 'CPU synthetic-parent' in prompt:
                texts=['\\boxed{7}']+['\\boxed{0}']*(samples-1)
            else:texts=['\\boxed{0}']*samples
            return [GeneratedResponse((1,2),text,False) for text in texts]
    c={**module().CONFIG};train=[{'question':'CPU root-'+str(i),'answer':'7'} for i in range(16)]
    ledger=CostLedger();backend=checkpoint.CheckpointConstruction(Policy(True),Policy(False),ledger,
        max_tokens=1024,rollouts=4,teacher_attempts=2,construction_json_schema=True,construction_teacher_sample=False)
    builder=MagicBeanStalk(backend,depth=1,decomposition_retries=2,synthesis_retries=2)
    synthetic,controls,selection=checkpoint.construct_paired_hard_roots(train,backend,builder,hard_root_limit=4)
    assert len(synthetic)==len(controls)==1,builder.audit
    active={'optimizer_update_executed':True,'zero_advantage_group':False,'loss':0.,'gradient_l2_norm':1.,
            'rewards':[1.,0.,0.,0.],'advantages':[.75,-.25,-.25,-.25]}
    zero={'optimizer_update_executed':False,'zero_advantage_group':True,'rewards':[0.,0.,0.,0.]}
    metrics={'accuracy':0.,'examples':4,'generated_tokens':8,'truncated_responses':0}
    cost=ledger.to_dict();cost['generation_calls'].update(evaluation=12,mbs_rlvr=2,seed_rlvr_control=2)
    cost['generated_tokens'].update(evaluation=24,mbs_rlvr=16,seed_rlvr_control=16)
    cost['scored_response_tokens']={'behavior':16,'student_rl':16}
    raw={'method':'magicbeanstalk','seed':42,'device':'cuda','diagnostic_only':True,'promotion_eligible':False,
         'parameters_changed':True,'construction_teacher_sample':False,'synthetic_problem_count':1,
         'construction_audits':builder.audit,'construction_response_audits':backend.response_audits,
         'hard_root_selection':selection,'training':[{'step':i+1,**active} for i in range(2)],
         'control':{'method':'seed-rlvr','training':[{'step':i+1,**zero} for i in range(2)],'metrics':metrics},
         'baseline':metrics,'method_metrics':metrics,'cost':cost}
    return raw,c,train


def test_full_core_replay_preserves_real_method_update_and_zero_control():
    r,c,train=core_fixture();check=module().validate_core(r,c,train)
    assert check['synthetic_problem_count']==1 and check['method_optimizer_updates']==2
    assert check['control_optimizer_updates']==0 and check['control_zero_advantage_groups']==2
    assert check['full_frozen_construction_replay_exact'] is True


@pytest.mark.parametrize('failure',['no_parameter_change','no_method_update','fake_control_update','advantage',
    'nan_loss','inf_gradient','missing_loss','teacher_sample','student_sample','schema_sha','missing_trace',
    'effectivity','leaf_threshold','goldilocks','calibration','pairing','tokens','call_cost','missing_synthesis'])
def test_no_core_threshold_or_actual_cost_can_be_faked(failure):
    r,c,train=core_fixture()
    if failure=='no_parameter_change':r['parameters_changed']=False
    elif failure=='no_method_update':r['training']=copy.deepcopy(r['control']['training'])
    elif failure=='fake_control_update':r['control']['training'][0]['optimizer_update_executed']=True
    elif failure=='advantage':r['training'][0]['advantages']=[0.]*4
    elif failure=='nan_loss':r['training'][0]['loss']=float('nan')
    elif failure=='inf_gradient':r['training'][0]['gradient_l2_norm']=float('inf')
    elif failure=='missing_loss':r['training'][0].pop('loss')
    elif failure=='teacher_sample':next(x for x in r['construction_response_audits'] if x['role']=='construction_verification')['sample']=True
    elif failure=='student_sample':
        next(x for x in r['construction_response_audits'] if x['role']=='effectivity_student')['sample']=False
    elif failure=='schema_sha':
        next(x for x in r['construction_response_audits'] if x['role']=='construction_teacher')['json_schema_sha256']='0'*64
    elif failure=='missing_trace':r['construction_response_audits'].pop()
    elif failure=='effectivity':next(x for x in r['construction_audits'] if x['phase']=='effectivity')['student_rates'][0]['conditioned']=0.
    elif failure=='leaf_threshold':next(x for x in r['construction_audits'] if x['phase']=='leaf-synthesis')['threshold']=1.
    elif failure=='goldilocks':next(x for x in r['construction_audits'] if x['phase']=='target-policy-goldilocks')['rewards']=[0.]*4
    elif failure=='calibration':r['hard_root_selection']['calibration_audits'][0]['rewards']=[1.]*4
    elif failure=='pairing':r['hard_root_selection']['paired_rl_root_indices']=[1]
    elif failure=='tokens':r['construction_response_audits'][0]['response_token_ids'].append(9)
    elif failure=='call_cost':r['cost']['generation_calls']['construction_verification']-=1
    else:r['construction_audits']=[x for x in r['construction_audits'] if x['phase']!='parent-synthesis']
    with pytest.raises(ValueError):module().validate_core(r,c,train)


def bundle_fixture(monkeypatch):
    m=module();r,c,train=core_fixture();c.update({key:'/tmp/CPU-fixture/'+key for key in m._legacy.PATH_FIELDS})
    config={'shared':c,'methods':{'magicbeanstalk':{}}};canonical=m.sha(json.dumps(config,sort_keys=True).encode())
    hashes={key:'a'*64 for key in m._legacy.SOURCE_PATHS};hashes['src/auto_research/reproductions/magicbeanstalk/checkpoint.py']=m.CHECKPOINT_SOURCE_SHA
    for name in ('post_training/oct10_checkpoint','post_training/oct13_common','post_training/proximal_checkpoint',
        'post_training/response_policy','reproductions/magicbeanstalk/algorithm','reproductions/magicbeanstalk/checkpoint'):
        key='src/auto_research/'+name+'.py';hashes[key]=m.sha((ROOT/key).read_bytes())
    contract={'source_commit':m.SOURCE_COMMIT,'source_file_sha256':hashes}
    resources={}
    for role in ('student','teacher'):
        files={key:'b'*64 for key in m._legacy.RESOURCE_FILES[role]};files.update(m._legacy.WEIGHTS[role]);files['tokenizer.json']=m._legacy.TOKENIZER_SHA
        resources[role]={'verified':True,'public_id':c[role+'_id'],'revision':c[role+'_revision'],
            'file_sha256':files,'vocabulary_sha256':'c'*64}
    audit={**contract,'execution_config_sha256':canonical,'source_hashes_verified':True,'cuda_initialized':False,
        'source_marker_verified':True,'source_marker_commit':m.SOURCE_COMMIT,'preflight_source_sha256':'e'*64,
        'model_instantiated':False,'exact_vocabulary_match':True,'public_train_only_holdout':m._legacy.DATASET,'resources':resources}
    packages={key:{'version':value,'package_file_sha256':{key+'/f'+str(i)+'.py':'d'*64 for i in range(29)}} for key,value in m._legacy.PINNED.items()}
    dependency={'packages':packages,'dependency_fingerprint':m.sha(json.dumps(packages,sort_keys=True).encode()),
        'overlay_root':'/tmp/CPU-only-overlay','cuda_initialized':False,'model_instantiated_by_audit':False,
        'not_gpu_receipt':True,'dependency_modules_imported_by_audit':False}
    grammar={'algorithm_commit':m.SOURCE_COMMIT,'source_file_sha256':hashes,'cuda_initialized':False,'model_loaded':False,
        'tokenizer_sha256':m._legacy.TOKENIZER_SHA,'vocab_size':152064,'versions':m._legacy.PINNED,
        'overlay_file_sha256':{key:value for package in packages.values() for key,value in package['package_file_sha256'].items()},
        'operations':{key:{'actual_compilation_completed':True,'schema_sha256':value} for key,value in m._legacy.ORDERED_SCHEMA_SHAS.items()},
        'source_marker_verified':True,'source_marker_commit':m.SOURCE_COMMIT,'compiler_helper_source_sha256':'e'*64,
        'resource_audit_sha256':'e'*64,'construction_schema_imported_from_actual_frozen_checkpoint':True,
        'processor_imported_from_actual_frozen_response_policy':True}
    raw_hashes={key:'e'*64 for key in ('launch','exit','runtime','result','source_contract','resource_audit','config','grammar_audit','dependency_audit','source_archive',
        'plan','launcher_source','preflight_source','compiler_source','base_launcher_source')}
    raw_hashes.update(launcher_source='f'*64,base_launcher_source='1'*64)
    command=['python','-u','scripts/run_oct13_post_training.py','--method','magicbeanstalk','--config','/tmp/CPU-fixture/config.json','--seed','{seed}','--output','/tmp/CPU-fixture/evidence']
    binding={'canonical_config_sha256':canonical,'config_raw_sha256':'e'*64,'source_archive_sha256':'e'*64,
        'gpu_slot_grant':'CPU-fixture-no-GPU','launcher_sha256':'f'*64,'base_launcher_sha256':'1'*64,'job_key':'CPU-fixture-mbs','command':command,
        'source_map_sha256':m.sha(json.dumps(hashes,sort_keys=True).encode()),'source_contract_sha256':'e'*64,
        'plan_sha256':'e'*64,'resource_audit_sha256':'e'*64,'grammar_audit_sha256':'e'*64,
        'dependency_audit_sha256':'e'*64,'preflight_sha256':'e'*64,'compiler_sha256':'e'*64,'seeds':[42]}
    monkeypatch.setattr(m,'RUN_BINDING',binding)
    launch={**contract,'execution_config_sha256':canonical,'effective_config':c,'schema_dependency_binding':dependency,
        'schema_grammar_binding':grammar,'schema_grammar_cpu_audit_sha256':raw_hashes['grammar_audit'],
        'seed':42,'actual_accelerator_name':'NVIDIA A100-SXM4-80GB','diagnostic_only':True,'formal_comparison':False,
        'gpu_grant_received':True,'gpu_slot_grant':binding['gpu_slot_grant'],'launcher_source_sha256':binding['launcher_sha256'],
        'base_launcher_source_sha256':binding['base_launcher_sha256'],'construction_schema_only':True,
        'independent_verifier_and_student_unconstrained':True,
        'job':{'key':binding['job_key'],'method':'magicbeanstalk','overrides':{},'priority':'explicit-construction-greedy-single-run','timeout_seconds':1800},
        'gpu_admission':{'name':'NVIDIA A100-SXM4-80GB','compute_processes':[],'used_mib':0,'free_mib':81920,'total_mib':81920},
        'construction_teacher_sample':False,'effectivity_and_student_sample':True,'only_construction_teacher_sampling_profile_changed':True,
        'resource_cpu_audit_sha256':'e'*64,'source_contract_sha256':'e'*64,'plan_sha256':'e'*64,
        'execution_config_file_sha256':'e'*64,'preflight_source_sha256':'e'*64,
        'budget':m._legacy.LAUNCH_BUDGET,'command':[value.replace('{seed}','42') for value in command],
        'runner_pythonpath':'/tmp/auto-research-oct14-4c4710cd/src:'+dependency['overlay_root']}
    r.update(dataset=m._legacy.DATASET,checkpoint={'public_id':c['student_id'],'revision':c['student_revision'],
        'verified_mirror':{'file_sha256':resources['student']['file_sha256']}},teacher={'public_id':c['teacher_id'],
        'revision':c['teacher_revision'],'verified_mirror':{'file_sha256':resources['teacher']['file_sha256']}},
        protocol={'test_opened':False,'gold_in_student_generation':False,'max_tokens':1024,'train_examples':16,'validation_examples':4})
    value={'launch':launch,'exit_record':{'exit_code':0,'elapsed_seconds':12.,'not_a_gpu_validation_receipt':True,
        'status':'completed','raw_returncode':0,'timed_out':False,'own_process_group_terminated':False,'runtime_log_sha256':'e'*64},
        'result':r,'contract':contract,'audit':audit,'dependency_audit':dependency,'grammar_audit':grammar,'config':config,
        'git_hashes':copy.deepcopy(hashes),'raw_hashes':raw_hashes,'train':train}
    return m,value


def test_source_bound_positive_fixture_is_not_published_and_zero_control_is_honest(monkeypatch):
    m,value=bundle_fixture(monkeypatch);artifact,receipt=m.curate_bundle(**value)
    assert artifact['whole_method_gpu_validation_passed'] is True and receipt['result']=='passed'
    assert artifact['default_three_seed_plan_completed'] is False
    assert artifact['execution_checks']['control_optimizer_updates']==0
    m.sanitize_guard(artifact);m.sanitize_guard(receipt)
    assert 'CPU-fixture' not in json.dumps(artifact) and '/tmp/' not in json.dumps(receipt)


def test_failed_native_never_produces_passed_receipt(monkeypatch):
    m,value=bundle_fixture(monkeypatch);value['exit_record']['exit_code']=1
    value['result']={'status':'failed','diagnostic_only':True,'error':'PRIVATE-HOST-OR-PROMPT','response_token_ids':[1]}
    artifact,receipt=m.curate_bundle(**value)
    assert receipt is None and artifact['whole_method_gpu_validation_passed'] is False
    assert artifact['not_gpu_receipt'] is True and 'PRIVATE-HOST-OR-PROMPT' not in json.dumps(artifact)


@pytest.mark.parametrize('failure',['source','source_sha','checkpoint_source','raw_config','archive_sha','config','overlay',
    'dependency','grammar','resource','vocabulary','launcher','seed','argv','wall','gold','measured_weights','dataset'])
def test_outer_binding_rejects_wrong_actual_source_resource_observer_or_seed(monkeypatch,failure):
    m,v=bundle_fixture(monkeypatch)
    if failure=='source':v['launch']['source_commit']='0'*40
    elif failure=='source_sha':v['git_hashes']['scripts/run_oct13_post_training.py']='0'*64
    elif failure=='checkpoint_source':
        v['contract']['source_file_sha256']['src/auto_research/reproductions/magicbeanstalk/checkpoint.py']='0'*64
        v['git_hashes']=copy.deepcopy(v['contract']['source_file_sha256'])
    elif failure=='raw_config':v['raw_hashes']['config']='0'*64
    elif failure=='archive_sha':v['raw_hashes']['source_archive']='0'*64
    elif failure=='config':v['config']['shared']['max_tokens']=1025
    elif failure=='overlay':v['launch']['runner_pythonpath']='/tmp/outer/src:/tmp/CPU-only-overlay'
    elif failure=='dependency':v['dependency_audit']['packages']['xgrammar']['version']='999'
    elif failure=='grammar':v['grammar_audit']['operations']['compose']['actual_compilation_completed']=False
    elif failure=='resource':v['audit']['resources']['teacher']['file_sha256'].pop('config.json')
    elif failure=='vocabulary':v['audit']['resources']['student']['vocabulary_sha256']='0'*64
    elif failure=='launcher':v['launch']['launcher_source_sha256']='0'*64
    elif failure=='seed':v['launch']['seed']=43
    elif failure=='argv':v['launch']['command'].append('--override')
    elif failure=='wall':v['exit_record']['elapsed_seconds']=1801.
    elif failure=='gold':v['result']['protocol']['gold_in_student_generation']=True
    elif failure=='measured_weights':v['result']['teacher']['verified_mirror']['file_sha256']={}
    else:v['result']['dataset']={}
    with pytest.raises(ValueError):m.curate_bundle(**v)


def test_unfrozen_observer_contract_cannot_sign_any_receipt(monkeypatch):
    m,value=bundle_fixture(monkeypatch);monkeypatch.setattr(m,'RUN_BINDING',None)
    with pytest.raises(ValueError,match='not yet been supplied'):m.curate_bundle(**value)
