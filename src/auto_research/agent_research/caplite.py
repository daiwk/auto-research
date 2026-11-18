"""CapLite v1 schema-derived authority and committed-write enforcement core.

Only flat object schemas with scalar/scalar-array arguments are supported. No
LLM planner/reader/binder/composer, AgentDojo or universal security claim exists.
Tool schemas and explicit user confirmations must be trusted externally.
"""
from copy import deepcopy
from dataclasses import dataclass
import math
import re

REQUIRES_GPU_VALIDATION = False
READ_VERBS = frozenset("get read search find list check view lookup fetch retrieve return show query count".split())
EFFECT_VERBS = frozenset("send delete create cancel reschedule add append share update book reserve make pay transfer schedule invite remove post set write move upload edit modify rename publish submit purchase order grant revoke".split())
PAYLOAD = frozenset("body content subject title description message text note notes comment comments".split())
DESTINATION = frozenset(("url","uri","link","webpage","website"))


def canonical(value):
    if isinstance(value,bool):
        text = "true" if value else "false"
    elif isinstance(value,(str,int,float)):
        if isinstance(value,float) and not math.isfinite(value):
            raise ValueError("nonfinite arguments are not groundable")
        text = str(value)
    else:
        raise ValueError("only scalar strings/numbers/booleans have grounding identities")
    return re.sub(r"^https?://", "", " ".join(text.lower().split()))


def grounding_set(request):
    """Section3: explicit identifiers plus all token n-grams up to eight.

    Equality after canonicalization, never substring membership. This bounded
    implementation uses Unicode word tokens and separately retains explicit
    emails, URLs, IBANs, ISO dates, quoted spans and numeric literals.
    """
    if not isinstance(request,str) or not request.strip():
        raise ValueError("nonempty trusted user request required")
    tokens = re.findall(r"\w+",request,flags=re.UNICODE)
    result = {canonical(' '.join(tokens[i:i+n])) for n in range(1,9) for i in range(len(tokens)-n+1)}
    patterns = (r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",r"https?://[^\s<>\"']+",r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]){10,30}\b",r"\b\d{4}-\d{2}-\d{2}\b",r'"([^"\n]+)"',r"'([^'\n]+)'",r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])")
    for pattern in patterns:
        for match in re.findall(pattern,request):
            result.add(canonical(match.rstrip('.,;') if pattern.startswith('https') else match))
    return frozenset(result)


def _verb(text):
    words = re.findall(r"[a-z]+",text.lower())
    return words[0] if words else ""


def _effect(verb):
    # AppendixA explicitly includes third-person forms; irregular `pays` etc.
    return verb in EFFECT_VERBS or verb in {v+'s' for v in EFFECT_VERBS} or verb in {v[:-1]+'ies' for v in EFFECT_VERBS if v.endswith('y')}


def _kind(name, schema):
    key = name.lower()
    words = set(re.findall(r"[a-z]+",key.replace('_',' ')))
    if any(term in key for term in DESTINATION):
        return "authority"
    if words & PAYLOAD:
        return "payload"
    if any(term in key for term in ('date','time','day')) or any(term in schema.get('description','') for term in ('YYYY-MM-DD','ISO')):
        return "temporal"
    if schema.get('type') == 'boolean' or 'enum' in schema:
        return "control"
    return "authority"


def _valid_schema(schema):
    if not isinstance(schema,dict) or schema.get('type') not in ('string','integer','number','boolean','array'):
        raise ValueError("unsupported schema: only explicit scalar/scalar-array types")
    if schema['type'] == 'array':
        item = schema.get('items',{})
        if item.get('type') == 'array':
            raise ValueError("nested argument schemas are not supported")
        _valid_schema(item)
    if 'enum' in schema and (not isinstance(schema['enum'],list) or not schema['enum']):
        raise ValueError("nonempty explicit enum required")


def _typed(value,schema):
    kind = schema['type']
    valid = ((kind == 'string' and isinstance(value,str)) or (kind == 'integer' and type(value) is int) or
             (kind == 'number' and type(value) in (int,float) and math.isfinite(value)) or
             (kind == 'boolean' and type(value) is bool) or
             (kind == 'array' and isinstance(value,(list,tuple)) and all(_typed(v,schema['items']) for v in value)))
    return valid and ('enum' not in schema or value in schema['enum'])


def _leaves(value):
    return tuple(value) if isinstance(value,(list,tuple)) else (value,)


class ToolPolicy:
    """Fail-closed schema snapshot. No untrusted tool text can modify it."""
    def __init__(self,name,description,parameters):
        if not isinstance(name,str) or not name or not isinstance(description,str):
            raise ValueError("trusted tool name/docstring required")
        if not isinstance(parameters,dict) or parameters.get('type') != 'object' or not isinstance(parameters.get('properties'),dict):
            raise ValueError("explicit flat object tool schema required")
        self.name = name
        self._schema = deepcopy(parameters)
        self._props = self._schema['properties']
        for schema in self._props.values():
            _valid_schema(schema)
        self._required = frozenset(self._schema.get('required',()))
        if not self._required <= self._props.keys():
            raise ValueError("required fields must exist in the trusted schema")
        nv,dv = _verb(name),_verb(description)
        self.operation = 'write' if _effect(nv) or _effect(dv) else ('read' if nv in READ_VERBS and dv in READ_VERBS else 'unknown')
        self.kinds = {k:_kind(k,v) for k,v in self._props.items()}

    def validate(self,arguments):
        return isinstance(arguments,dict) and self._required <= arguments.keys() and arguments.keys() <= self._props.keys() and all(_typed(v,self._props[k]) for k,v in arguments.items())

    def permits(self,arguments,grounded,confirmed=()):
        if self.operation == 'unknown' or not self.validate(arguments):
            return False
        authority = {k for k,kind in self.kinds.items() if kind == 'authority' and (self.operation == 'write' or any(x in k.lower() for x in DESTINATION))}
        trusted = frozenset(grounded) | frozenset(canonical(x) for x in confirmed)
        return all(canonical(v) in trusted for k in authority if k in arguments for v in _leaves(arguments[k]))

    def bind_candidates(self,field,candidates,grounded):
        """At most32 existing candidates; filter authority AND control values."""
        if field not in self._props:
            raise ValueError("unknown binding field")
        rows = tuple(candidates)
        if len(rows) > 32 or any(not isinstance(c,Candidate) for c in rows) or len({c.identity for c in rows}) != len(rows):
            raise ValueError("at most32 unique typed extracted candidates required")
        return tuple(c for c in rows if _typed(c.value,self._props[field]) and
                     (self.kinds[field] not in ('authority','control') or all(canonical(v) in grounded for v in _leaves(c.value))))


@dataclass(frozen=True)
class Candidate:
    identity: str
    value: object
    source_ref: str

    def __post_init__(self):
        if any(not isinstance(x,str) or not x.strip() for x in (self.identity,self.source_ref)):
            raise ValueError("candidate identity and source/keypath provenance required")


@dataclass(frozen=True)
class Placeholder:
    identity: str


class CommittedWrites:
    """Immutable pre-read write plan; execute only its successful prefix.

    This object must be constructed by the trusted harness before any untrusted
    result is exposed. It does not prove that external event ordering occurred.
    """
    def __init__(self,request,plan,policies):
        self._grounded = grounding_set(request)
        self._policies = dict(policies)
        rows = tuple(plan)
        if len(rows) > 10:
            raise ValueError("at most10 committed writes")
        for tool,args in rows:
            if tool not in self._policies or self._policies[tool].operation != 'write' or not isinstance(args,dict):
                raise ValueError("plan must commit known write tools and argument slots")
            policy = self._policies[tool]
            if not policy._required <= args.keys() or not args.keys() <= policy._props.keys():
                raise ValueError("committed fields must match trusted schema")
            if any(not isinstance(v,Placeholder) and not _typed(v,policy._props[k]) for k,v in args.items()):
                raise ValueError("typed literal or explicit placeholder required")
        self._plan,self._cursor,self._stopped = deepcopy(rows),0,False

    @property
    def executed_count(self):
        return self._cursor

    @property
    def stopped(self):
        return self._stopped

    def execute_next(self,tool,arguments,*,execute,confirmed=()):
        if self._stopped:
            return False
        allowed = self._cursor < len(self._plan) and isinstance(arguments,dict)
        if allowed:
            expected,slots = self._plan[self._cursor]
            allowed = tool == expected and arguments.keys() == slots.keys()
            allowed = allowed and all(isinstance(v,Placeholder) or v == arguments[k] for k,v in slots.items())
            allowed = allowed and self._policies[tool].permits(arguments,self._grounded,confirmed)
        if not allowed:
            self._stopped = True
            return False
        try:
            execute(tool,deepcopy(arguments))
        except Exception:
            self._stopped = True
            raise
        self._cursor += 1
        return True

    def ask_or_deny(self):
        self._stopped = True


def diagnostic(seed: int, device: str = 'cpu') -> dict:
    if type(seed) is not int or device != 'cpu':
        raise ValueError("integer seed and CPU-only enforcement kernel required")
    schema = {'type':'object','properties':{'recipient':{'type':'string'},'amount':{'type':'integer'},'message':{'type':'string'}},'required':['recipient','amount','message']}
    policy = ToolPolicy('send_payment','Send a payment',schema)
    request = 'Send 100 to alice@example.com with message "hello"'
    grounded = grounding_set(request)
    rows = [Candidate('good','alice@example.com','result:email'),Candidate('attack','evil@example.com','result:injection')]
    accepted = policy.bind_candidates('recipient',rows,grounded)
    plan = [('send_payment',{'recipient':Placeholder('to'),'amount':100,'message':Placeholder('payload')})]*2
    writes = CommittedWrites(request,plan,{'send_payment':policy})
    effects = []
    ok = writes.execute_next('send_payment',{'recipient':'alice@example.com','amount':100,'message':'unrestricted payload'},execute=lambda t,a:effects.append((t,a)))
    denied = writes.execute_next('send_payment',{'recipient':'evil@example.com','amount':100,'message':'attack'},execute=lambda t,a:effects.append((t,a)))
    later = writes.execute_next('send_payment',{'recipient':'alice@example.com','amount':100,'message':'x'},execute=lambda t,a:effects.append((t,a)))
    read = ToolPolicy('fetch_url','Fetch a URL',{'type':'object','properties':{'url':{'type':'string'}},'required':['url']})
    checks = {'schema_not_model_authority':policy.operation == 'write', 'candidate_ids_not_free_values':tuple(c.identity for c in accepted) == ('good',),
              'exact_numeric_grounding':canonical(1) not in grounded and canonical(100) in grounded,
              'prefix_stops_on_denial':ok and not denied and not later and len(effects) == 1 and writes.stopped,
              'payload_outside_authority_guarantee':effects[0][1]['message'] == 'unrestricted payload',
              'read_destination_checked':not read.permits({'url':'https://evil.example'},grounded),
              'unknown_tool_fail_closed':ToolPolicy('calculate','Compute value',schema).operation == 'unknown'}
    return {'seed':seed,'execution_device':'cpu','diagnostic_only':True,'evaluation_tier':'l1_mechanism','checks':checks,
            'metrics':{'actual_effect_calls':len(effects),'accepted_candidates':len(accepted),'committed_writes':2}}
