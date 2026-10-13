"""CPU stub contracts for opt-in decoding; no real XGrammar/CUDA/model claims."""
import builtins
import copy
import hashlib
import json
import sys
import importlib.metadata
from types import ModuleType, SimpleNamespace

import pytest
import torch

from auto_research.post_training.oct13_common import CostLedger
from auto_research.post_training.response_policy import GeneratedResponse, ResponsePolicy
from auto_research.reproductions.magicbeanstalk.checkpoint import CheckpointConstruction, Problem
from auto_research.reproductions.magicbeanstalk import checkpoint


def bare_policy(text='[{"question":"generic","answer":"7","trace":"worked"}]', eos=True):
    policy = object.__new__(ResponsePolicy)
    class Model:
        config = SimpleNamespace(vocab_size=12345)
        def __init__(self):
            self.calls = []
        def eval(self):
            return self
        def generate(self, prompt, **kwargs):
            self.calls.append((prompt.clone(), copy.copy(kwargs)))
            tokens = [5, 6, 0] if eos else [5, 6, 7]
            return torch.cat((prompt, torch.tensor([tokens])), dim=-1).repeat(kwargs['num_return_sequences'], 1)
    policy.model = Model()
    policy.device = 'cpu'
    policy.context_limit = 12
    policy.tokenizer = SimpleNamespace(eos_token_id=0, pad_token_id=0, decode=lambda _tokens, **_kw: text)
    policy.prompt_ids = lambda _messages: torch.tensor([[9, 10]])
    return policy


def xgrammar_stub(monkeypatch):
    module = ModuleType('xgrammar')
    hf = ModuleType('xgrammar.contrib.hf')
    calls = []
    class TokenizerInfo:
        @staticmethod
        def from_huggingface(tokenizer, *, vocab_size):
            calls.append(('tokenizer', tokenizer, vocab_size))
            return 'tokenizer-info'
    class Compiler:
        def __init__(self, info):
            calls.append(('compiler', info))
        def compile_json_schema(self, schema):
            calls.append(('compile', schema))
            return object()
    class Processor:
        def __init__(self, compiled):
            self.compiled = compiled
            calls.append(('processor', self))
    module.TokenizerInfo = TokenizerInfo
    module.GrammarCompiler = Compiler
    hf.LogitsProcessor = Processor
    monkeypatch.setitem(sys.modules, 'xgrammar', module)
    monkeypatch.setitem(sys.modules, 'xgrammar.contrib', ModuleType('xgrammar.contrib'))
    monkeypatch.setitem(sys.modules, 'xgrammar.contrib.hf', hf)
    original_version = importlib.metadata.version
    monkeypatch.setattr(importlib.metadata, 'version', lambda name: '0.2.8' if name == 'xgrammar' else original_version(name))
    return calls


def test_default_policy_and_ledger_keep_original_generation_kwargs_without_import(monkeypatch):
    original = builtins.__import__
    def guarded(name, *args, **kwargs):
        assert not name.startswith('xgrammar')
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, '__import__', guarded)
    policy = bare_policy()
    ledger = CostLedger()
    responses = ledger.sample(policy, [], samples=2, max_tokens=3)
    _, kwargs = policy.model.calls[0]
    assert kwargs.keys() == {'attention_mask', 'max_new_tokens', 'do_sample', 'num_return_sequences',
                            'temperature', 'top_p', 'top_k', 'pad_token_id', 'use_cache'}
    assert kwargs['max_new_tokens'] == 3 and kwargs['num_return_sequences'] == 2
    assert [r.tokens for r in responses] == [(5, 6, 0)] * 2
    assert ledger.calls == {'student': 1} and ledger.generated_tokens == {'student': 6}


def test_schema_caches_compilation_not_stateful_processor_and_charges_actual_tokens(monkeypatch):
    calls = xgrammar_stub(monkeypatch)
    policy = bare_policy()
    ledger = CostLedger()
    schema = {'type': 'array', 'items': {'type': 'string'}}
    first = ledger.sample(policy, [], role='construction_teacher', max_tokens=3, json_schema=schema)
    second = ledger.sample(policy, [], role='construction_teacher', max_tokens=3, json_schema=copy.deepcopy(schema))
    assert sum(x[0] == 'tokenizer' for x in calls) == sum(x[0] == 'compiler' for x in calls) == 1
    assert next(x for x in calls if x[0] == 'tokenizer')[2] == 12345
    assert sum(x[0] == 'compile' for x in calls) == 1
    processors = [kwargs['logits_processor'][0] for _, kwargs in policy.model.calls]
    assert processors[0] is not processors[1] and processors[0].compiled is processors[1].compiled
    assert first[0].tokens == second[0].tokens == (5, 6, 0)
    assert ledger.calls == {'construction_teacher': 2} and ledger.generated_tokens == {'construction_teacher': 6}
    ledger.sample(policy, [], json_schema={'type': 'object'})
    assert sum(x[0] == 'compile' for x in calls) == 2
    assert policy.model.calls[-1][1]['logits_processor'][0].compiled is not processors[0].compiled


def test_compile_cache_and_actual_schema_digest_preserve_nested_property_order(monkeypatch):
    calls = xgrammar_stub(monkeypatch)
    policy = bare_policy()
    properties = {'question': {'type': 'string'}, 'trace': {'type': 'string'}, 'answer': {'type': 'string'}}
    schema = {'type': 'object', 'properties': properties, 'required': list(properties)}
    policy.generate([], json_schema=schema)
    first_digest = policy.last_json_schema_generation['schema_sha256']
    first_processor = policy.model.calls[-1][1]['logits_processor'][0]
    first_string = [c[1] for c in calls if c[0] == 'compile'][0]
    assert list(json.loads(first_string)['properties']) == ['question', 'trace', 'answer']
    assert first_string == json.dumps(schema, separators=(',', ':'), allow_nan=False)
    assert first_digest == hashlib.sha256(first_string.encode()).hexdigest()
    assert first_digest != hashlib.sha256(json.dumps(schema, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    different_order = copy.deepcopy(schema)
    different_order['properties'] = dict(reversed(list(properties.items())))
    policy.generate([], json_schema=different_order)
    second_processor = policy.model.calls[-1][1]['logits_processor'][0]
    assert policy.last_json_schema_generation['schema_sha256'] != first_digest
    assert second_processor.compiled is not first_processor.compiled
    policy.generate([], json_schema=copy.deepcopy(schema))
    third_processor = policy.model.calls[-1][1]['logits_processor'][0]
    assert third_processor is not first_processor and third_processor.compiled is first_processor.compiled
    assert policy.last_json_schema_generation['schema_sha256'] == first_digest
    assert sum(c[0] == 'compile' for c in calls) == 2


def test_missing_dependency_fails_before_model_generation_or_fake_ledger_cost(monkeypatch):
    original = builtins.__import__
    def missing(name, *args, **kwargs):
        if name.startswith('xgrammar'):
            raise ModuleNotFoundError('CPU fixture missing optional dependency')
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, '__import__', missing)
    policy = bare_policy()
    policy.last_json_schema_generation = {'backend': 'stale'}
    ledger = CostLedger()
    with pytest.raises(RuntimeError, match='xgrammar'):
        ledger.sample(policy, [], json_schema={'type': 'object'})
    assert policy.model.calls == [] and ledger.calls == {} and ledger.generated_tokens == {}
    assert policy.last_json_schema_generation == {}


@pytest.mark.parametrize('schema', ['not a schema', {'minimum': float('nan')}, {'default': object()}])
def test_invalid_schema_fails_closed_without_generation(monkeypatch, schema):
    xgrammar_stub(monkeypatch)
    policy = bare_policy()
    with pytest.raises(ValueError):
        policy.generate([], json_schema=schema)
    assert policy.model.calls == []


@pytest.mark.parametrize('vocab_size', [None, 0, True, '12345'])
def test_token_masks_require_actual_positive_integer_model_vocabulary(monkeypatch, vocab_size):
    calls = xgrammar_stub(monkeypatch)
    policy = bare_policy()
    policy.model.config = SimpleNamespace(vocab_size=vocab_size)
    with pytest.raises(ValueError, match='vocab_size'):
        policy.generate([], json_schema={'type': 'object'})
    assert policy.model.calls == [] and calls == []


def test_compile_error_does_not_fall_back_to_unconstrained_generation(monkeypatch):
    xgrammar_stub(monkeypatch)
    def reject(_self, _schema):
        raise ValueError('CPU fixture unsupported schema')
    monkeypatch.setattr(sys.modules['xgrammar'].GrammarCompiler, 'compile_json_schema', reject)
    policy = bare_policy()
    ledger = CostLedger()
    with pytest.raises(ValueError, match='unsupported schema'):
        ledger.sample(policy, [], json_schema={'type': 'object'})
    assert policy.model.calls == [] and ledger.calls == {} and ledger.generated_tokens == {}


class RecordingPolicy:
    def __init__(self, text='[]', truncated=False):
        self.text = text
        self.truncated = truncated
        self.calls = []
    def generate(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        if 'json_schema' in kwargs:
            self.last_json_schema_generation = {'backend': 'xgrammar-hf', 'version': '0.2.8-CPU-STUB',
                'schema_sha256': hashlib.sha256(json.dumps(kwargs['json_schema'], separators=(',', ':'), allow_nan=False).encode()).hexdigest()}
        return [GeneratedResponse((1, 2), self.text, self.truncated)] * kwargs['samples']


@pytest.mark.parametrize('operation,type_', [('propose_children', 'array'), ('harder_leaf', 'object'),
    ('compose', 'object'), ('scaffold_safe', 'object'), ('blueprint_and_novelty', 'object')])
def test_only_opt_in_construction_teacher_receives_operation_schema_and_audit(operation, type_):
    teacher, student = RecordingPolicy(), RecordingPolicy('\\boxed{0}')
    backend = CheckpointConstruction(teacher, student, CostLedger(), construction_json_schema=True)
    backend.teacher_json('unchanged instruction', {'parent': {'answer': 'PRIVATE_TRAIN_GOLD'}}, operation=operation)
    messages, kwargs = teacher.calls[0]
    schema = kwargs['json_schema']
    assert schema['type'] == type_
    if operation == 'propose_children':
        assert schema['minItems'] == schema['maxItems'] == 2
    if operation in ('propose_children', 'harder_leaf', 'compose'):
        problem = schema['items'] if operation == 'propose_children' else schema
        assert set(problem['required']) == {'question', 'answer', 'trace'}
        assert list(problem['properties']) == problem['required'] == ['question', 'trace', 'answer']
        answer = problem['properties']['answer']
        assert 'enum' not in json.dumps(answer) and 'const' not in json.dumps(answer)
        assert 'pattern' not in json.dumps(answer) and 'minimum' not in json.dumps(answer)
    assert 'PRIVATE_TRAIN_GOLD' in str(messages)
    digest = hashlib.sha256(json.dumps(schema, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    assert backend.response_audits[-1]['json_schema_sha256'] == digest
    assert backend.response_audits[-1]['json_schema_constrained'] is True
    assert backend.response_audits[-1]['xgrammar_version'] == '0.2.8-CPU-STUB'
    parent = Problem('public question', '7', 'PRIVATE_PARENT_PLAN')
    backend.verify(parent)
    backend.target_outcomes(parent)
    backend.student_rates(parent, worked_examples=())
    for messages, kwargs in teacher.calls[1:] + student.calls:
        assert 'json_schema' not in kwargs
        assert 'PRIVATE_PARENT_PLAN' not in str(messages) and 'PRIVATE_TRAIN_GOLD' not in str(messages)


def test_default_construction_kwargs_and_audit_remain_unchanged():
    teacher = RecordingPolicy('[]')
    backend = CheckpointConstruction(teacher, None, CostLedger())
    assert backend.propose_children(Problem('q', '7', 'trace'), []) == []
    assert set(teacher.calls[0][1]) == {'samples', 'max_tokens', 'sample'}
    assert 'json_schema_constrained' not in backend.response_audits[-1]


@pytest.mark.parametrize('value', ['true', 1, None])
def test_opt_in_flag_is_explicit_boolean(value):
    with pytest.raises(ValueError):
        CheckpointConstruction(None, None, CostLedger(), construction_json_schema=value)


@pytest.mark.parametrize('value', ['true', 1, None])
def test_bad_run_flag_is_rejected_before_data_or_checkpoint_loading(monkeypatch, value):
    def forbidden(_config):
        pytest.fail('must not load data for invalid opt-in flag')
    monkeypatch.setattr(checkpoint, 'load_split', forbidden)
    with pytest.raises(ValueError, match='explicit boolean'):
        checkpoint.run({'construction_json_schema': value})


def test_structural_boolean_schema_does_not_force_safety_or_novelty_acceptance():
    teacher = RecordingPolicy('{"scaffold_safe":false}')
    backend = CheckpointConstruction(teacher, None, CostLedger(), construction_json_schema=True)
    assert backend.teacher_json('judge', {}, operation='scaffold_safe') == {'scaffold_safe': False}
    teacher.text = '{"blueprint_preserved":false,"substantive_novelty":false}'
    assert backend.teacher_json('judge', {}, operation='blueprint_and_novelty') == {
        'blueprint_preserved': False, 'substantive_novelty': False}


def test_missing_actual_backend_metadata_keeps_response_trace_and_real_cost():
    class NoMetadata(RecordingPolicy):
        def generate(self, messages, **kwargs):
            result = super().generate(messages, **kwargs)
            self.last_json_schema_generation = {}
            return result
    ledger = CostLedger()
    backend = CheckpointConstruction(NoMetadata(), None, ledger, construction_json_schema=True)
    with pytest.raises(ValueError, match='metadata'):
        backend.propose_children(Problem('q', '7', 't'), [])
    assert ledger.generated_tokens == {'construction_teacher': 2}
    assert backend.response_audits[-1]['response_text'] == '[]'
    assert backend.response_audits[-1]['response_token_ids'] == [1, 2]
    assert backend.response_audits[-1]['parsing_completed'] is False


@pytest.mark.parametrize('text,truncated', [('malformed [{"question":"q","answer":7,"trace":"t"}', False),
    ('[{"question":"q","answer":7,"trace":"t"}]', True)])
def test_constrained_path_does_not_repair_json_or_accept_truncated_prefix(text, truncated):
    teacher = RecordingPolicy(text, truncated)
    ledger = CostLedger()
    backend = CheckpointConstruction(teacher, None, ledger, max_tokens=1024, construction_json_schema=True)
    assert backend.propose_children(Problem('q', '7', 't'), []) == []
    assert ledger.calls == {'construction_teacher': 1} and ledger.generated_tokens == {'construction_teacher': 2}
    assert backend.response_audits[-1]['response_text'] == text
    assert backend.response_audits[-1]['response_token_ids'] == [1, 2]


def test_constrained_unknown_operation_cannot_silently_generate_unconstrained():
    teacher = RecordingPolicy()
    backend = CheckpointConstruction(teacher, None, CostLedger(), construction_json_schema=True)
    with pytest.raises(ValueError, match='operation'):
        backend.teacher_json('instruction', {}, operation='unknown')
    assert teacher.calls == []
