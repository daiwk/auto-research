"""Bounded, real-checkpoint runtimes for BranchOPD, CAST, Road and BoundaryEvo.

Gold references never enter student/teacher/expert generation. BoundaryEvo's
separate frozen analyzer is an external judge, not the evaluated policy. Runs
write honest runtime diagnostics, even when boundary acquisition is empty.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re

import torch

from auto_research.public_holdout import validate_holdout
from auto_research.agent_research.oct12_provenance import verify_local_checkpoint
from auto_research.oct12_public_sources import checkpoint_source
from .oct10_checkpoint import _logits, _prompt, install_lora, load_public_rows, verified_reward
from .oct12_objectives import (
    BoundaryAssessment, actor_loss, boundary_selection, branch_forks, branch_loss,
    cast_credit, credit_chunks, decoded_alignment, preventive_projection,
    project_teacher_scores, protocol_boundary_loss, road_credit, selective_anchor,
)

OBJECTIVES = ("branch-opd", "cast", "road-mopd", "boundary-evo")


@dataclass
class ModelRole:
    model: object
    tokenizer: object
    identity: dict
    device: str


def load_role(path, identifier, revision, device):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if not path or not identifier or not revision:
        raise ValueError("each model role needs a local path, public ID and pinned revision")
    if not re.fullmatch(r"[0-9a-fA-F]{40}",revision):
        raise ValueError("public model revision must be an immutable 40-character commit, not main/latest")
    path = Path(path)
    if (path/"provenance.json").is_file():
        source,kwargs,provenance = checkpoint_source(identifier,revision,path)
        identity = {"id":identifier,"revision":revision,"immutable_revision_verified":True,
                    "verification":"pinned public-source manifest with exact file SHA256",
                    "file_sha256":provenance["file_sha256"]}
    else:
        identity = verify_local_checkpoint(path,identifier,revision)
        source,kwargs = str(path),{"local_files_only":True}
    tokenizer = AutoTokenizer.from_pretrained(source,trust_remote_code=False,**kwargs)
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        source, trust_remote_code=False, **kwargs, dtype=torch.bfloat16 if device.startswith("cuda") else torch.float32,
        attn_implementation="eager").to(device).eval()
    model.requires_grad_(False)
    return ModelRole(model, tokenizer, identity, device)


def sample_path(role, question, max_tokens, *, prefix=None, greedy=False):
    """The generation interface intentionally cannot receive a reference answer."""
    prompt = _prompt(role.tokenizer, question, role.device) if prefix is None else prefix
    with torch.no_grad():
        ids = role.model.generate(prompt, attention_mask=torch.ones_like(prompt),
            max_new_tokens=max_tokens, do_sample=not greedy, temperature=1. if not greedy else None,
            top_p=1. if not greedy else None, top_k=0 if not greedy else None,
            pad_token_id=role.tokenizer.pad_token_id, use_cache=True)
    # Single-response generation contains no batch padding; include real EOS.
    return ids, prompt.shape[-1]


def decoded_response(role, ids, prompt_length):
    return role.tokenizer.decode(ids[0, prompt_length:], skip_special_tokens=True,
                                 clean_up_tokenization_spaces=False)


def sampled_logp(model, ids):
    logits = _logits(model, ids)
    return logits, logits.log_softmax(-1).gather(-1, ids[:, 1:, None]).squeeze(-1)


@contextmanager
def initial_policy(model):
    """Temporarily disable zero-initialized LoRA, recovering frozen pi_0 exactly."""
    saved = {name: p.detach().clone() for name, p in model.named_parameters()
             if name.endswith(".b") and p.requires_grad}
    with torch.no_grad():
        for name, p in model.named_parameters():
            if name in saved:
                p.zero_()
    try:
        yield
    finally:
        with torch.no_grad():
            for name, p in model.named_parameters():
                if name in saved:
                    p.copy_(saved[name])


def reference_logp(student, ids):
    with torch.no_grad(), initial_policy(student.model):
        _, values = sampled_logp(student.model, ids)
        return values.detach()


def response_mask(ids, prompt_length, *, fork=None):
    mask = torch.zeros_like(ids[:, 1:], dtype=torch.bool)
    start = prompt_length-1 if fork is None else fork-1
    mask[:, start:] = True
    return mask


def math_protocol_constraints(tokenizer, response, *, prompt_length, fork=0):
    """After a complete boxed answer, encourage EOS, without checking correctness."""
    constraints = []
    for end in range(1, len(response)+1):
        text = tokenizer.decode(response[:end], skip_special_tokens=True,
                                clean_up_tokenization_spaces=False)
        if re.search(r"\\boxed\{[^{}]+\}\s*$", text):
            position = prompt_length+end-1
            if position >= fork:
                constraints.append((position, (tokenizer.eos_token_id,), True))
            break
    return constraints


def branch_step(student, teacher, question, optimizer, *, max_tokens, forks, continuations,
                pbr_weight, min_fork_gap):
    # Declare the mathematical response protocol rather than waiting for a
    # small checkpoint to spontaneously choose LaTeX. No labels enter this path.
    question = question + "\nPut your final numeric result in \\boxed{...}, then end the response."
    main, prompt_length = sample_path(student, question, max_tokens)
    with torch.no_grad():
        rollout_logits, old = sampled_logp(student.model, main)
        _, teacher_lp = sampled_logp(teacher.model, main)
    response = main[0, prompt_length:]
    local_logits = rollout_logits[0, prompt_length-1:]
    top = local_logits.log_softmax(-1).topk(min(20, local_logits.shape[-1]), -1).values
    entropy = -(top.exp()*top).sum(-1)
    eligible = entropy >= .5
    for i, token in enumerate(response.tolist()):
        if token in student.tokenizer.all_special_ids:
            eligible[i] = False
        if re.search(r"\\boxed\{[^{}]+\}", student.tokenizer.decode(response[:i+1])):
            eligible[i:] = False
            break
    selected, _, _ = branch_forks(local_logits, old[0,prompt_length-1:],
        teacher_lp[0,prompt_length-1:], eligible, budget=forks, min_gap=min_fork_gap)
    paths = [(main, prompt_length, prompt_length, old, teacher_lp)]
    prefix_tokens_saved = 0
    for index in selected:
        prefix_length = prompt_length+index
        prefix = main[:, :prefix_length]
        for _ in range(continuations):
            ids, _ = sample_path(student, question, max(1,max_tokens-index), prefix=prefix)
            with torch.no_grad():
                _, old_branch = sampled_logp(student.model, ids)
                _, scored = sampled_logp(teacher.model, ids)
            paths.append((ids, prompt_length, prefix_length, old_branch, scored))
            prefix_tokens_saved += index
    tokens = sum(ids.shape[-1]-fork for ids, _, fork, _, _ in paths)
    losses, repair_losses, constraints_count = [], [], 0
    optimizer.zero_grad(set_to_none=True)
    for ids, prompt_length, fork, old, teacher_lp in paths:
        logits, current = sampled_logp(student.model, ids)
        mask = response_mask(ids, prompt_length, fork=fork)
        losses.append(branch_loss(current, old, teacher_lp, mask)*mask.sum()/tokens)
        constraints = math_protocol_constraints(student.tokenizer, ids[0,prompt_length:].tolist(),
                                                prompt_length=prompt_length, fork=fork)
        if constraints:
            # Full forward includes the prediction AFTER the final response token.
            full_logits = student.model(input_ids=ids, use_cache=False).logits[0].float()
            repair_losses.append(protocol_boundary_loss(full_logits, constraints)*len(constraints))
            constraints_count += len(constraints)
    loss = sum(losses)
    if constraints_count:
        loss = loss+pbr_weight*sum(repair_losses)/constraints_count
    loss.backward()
    gradient = float(torch.nn.utils.clip_grad_norm_([p for p in student.model.parameters() if p.requires_grad],1.))
    optimizer.step()
    return {"loss": float(loss.detach()), "gradient_l2": gradient, "response_tokens": tokens,
            "selected_forks": selected, "branches": len(paths)-1,
            "shared_prefix_tokens_excluded": prefix_tokens_saved, "pbr_constraints": constraints_count}


def teacher_text_scores(teacher, question, response_text):
    prefix = _prompt(teacher.tokenizer, question, teacher.device)
    response = teacher.tokenizer(response_text, return_tensors="pt", add_special_tokens=False).input_ids.to(teacher.device)
    if not response.numel():
        return [], torch.zeros(0, device=teacher.device)
    ids = torch.cat((prefix,response),-1)
    with torch.no_grad():
        _, values = sampled_logp(teacher.model, ids)
    return response[0].tolist(), values[0,prefix.shape[-1]-1:]


def cast_step(student, teacher, question, optimizer, *, max_tokens, group, credit_size, kl_weight):
    paths = []
    for _ in range(group):
        ids, length = sample_path(student, question, max_tokens)
        with torch.no_grad():
            logits, old = sampled_logp(student.model,ids)
            distribution = logits[0,length-1:].log_softmax(-1)
            entropy = -(distribution.exp()*distribution).sum(-1)
        reference = reference_logp(student,ids)[0,length-1:]
        response = ids[0,length:].tolist()
        text = decoded_response(student,ids,length)
        teacher_ids, teacher_lp = teacher_text_scores(teacher,question,text)
        alignment = decoded_alignment(response,teacher_ids,
            lambda values: student.tokenizer.decode(values,skip_special_tokens=True,clean_up_tokenization_spaces=False),
            lambda values: teacher.tokenizer.decode(values,skip_special_tokens=True,clean_up_tokenization_spaces=False))
        projected, aligned = project_teacher_scores(len(response),teacher_lp,alignment)
        advantage, weights = cast_credit(old[0,length-1:],projected,entropy,credit_chunks(aligned,credit_size))
        paths.append((ids,length,old,reference,aligned,advantage,weights,len(alignment)))
    total_aligned = sum(int(p[4].sum()) for p in paths)
    total_unaligned = sum(int((~p[4]).sum()) for p in paths)
    optimizer.zero_grad(set_to_none=True)
    loss = 0
    for ids,length,old,reference,aligned,advantage,weights,_ in paths:
        _, current = sampled_logp(student.model,ids)
        current = current[0,length-1:]
        loss = loss+actor_loss(current,old[0,length-1:],advantage,aligned)*aligned.sum()/max(1,total_aligned)
        loss = loss+kl_weight*selective_anchor(current,reference,~aligned)*(~aligned).sum()/max(1,total_unaligned)
    loss.backward()
    gradient = float(torch.nn.utils.clip_grad_norm_([p for p in student.model.parameters() if p.requires_grad],1.))
    optimizer.step()
    return {"loss": float(loss.detach()), "gradient_l2": gradient,
            "aligned_tokens":total_aligned,"unaligned_tokens":total_unaligned,
            "alignment_chunks":sum(p[-1] for p in paths), "rollouts":group,
            "response_tokens":total_aligned+total_unaligned}


def road_step(student, teachers, domain_rows, optimizer, *, max_tokens, retention):
    params = [p for p in student.model.parameters() if p.requires_grad]
    domain_gradients = []
    losses, conflicts, projected_count, tokens = [], 0, 0, 0
    for domain, row in enumerate(domain_rows):
        ids,length = sample_path(student,row["question"],max_tokens)
        mask = response_mask(ids,length)
        with torch.no_grad():
            _, old = sampled_logp(student.model,ids)
            _, routed = sampled_logp(teachers[domain].model,ids)
            _, auxiliary = sampled_logp(teachers[1-domain].model,ids)
        reference = reference_logp(student,ids)
        _, current = sampled_logp(student.model,ids)
        advantage, _ = road_credit(current,routed,auxiliary,reference)
        target_loss = actor_loss(current,old,advantage,mask,sequence_mean=True)
        target_grads = torch.autograd.grad(target_loss,params)
        # Recompute graph on the SAME trajectory; no auxiliary-domain rollout.
        _, current = sampled_logp(student.model,ids)
        plain_advantage = (auxiliary-current.detach()).clamp(-10,10)
        auxiliary_loss = actor_loss(current,old,plain_advantage,mask,sequence_mean=True)
        auxiliary_grads = torch.autograd.grad(auxiliary_loss,params)
        corrected = []
        for target, peer in zip(target_grads,auxiliary_grads):
            conflict = float((target*peer).sum()) < 0
            revised, alpha = preventive_projection(target,peer,retention=retention)
            conflicts += int(conflict)
            projected_count += int(alpha>0)
            corrected.append(revised)
        domain_gradients.append(corrected)
        losses.append(float(target_loss.detach()))
        tokens += int(mask.sum())
    optimizer.zero_grad(set_to_none=True)
    for index,p in enumerate(params):
        p.grad = torch.stack([gradient[index] for gradient in domain_gradients]).mean(0)
    gradient = float(torch.nn.utils.clip_grad_norm_(params,1.))
    optimizer.step()
    return {"loss":sum(losses)/len(losses), "gradient_l2":gradient,
            "conflicting_tensors":conflicts,"projected_tensors":projected_count,
            "target_domains":len(domain_rows),"response_tokens":tokens}


def sft_trajectory(student, question, teacher_text, optimizer, max_tokens):
    prefix = _prompt(student.tokenizer,question,student.device)
    suffix = student.tokenizer(teacher_text,return_tensors="pt",add_special_tokens=False).input_ids.to(student.device)
    suffix = suffix[:,:max_tokens]
    if not suffix.numel():
        return None
    ids = torch.cat((prefix,suffix),-1)
    logits = _logits(student.model,ids)[:,prefix.shape[-1]-1:]
    loss = torch.nn.functional.cross_entropy(logits.flatten(0,1),suffix.flatten())
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    gradient = float(torch.nn.utils.clip_grad_norm_([p for p in student.model.parameters() if p.requires_grad],1.))
    optimizer.step()
    return {"loss":float(loss.detach()),"gradient_l2":gradient,"response_tokens":suffix.numel()}


def judge_boundary(analyzer, question, reference, student_text, expert_text, max_tokens):
    """Reference-aware external analyzer; no reference is sent to either solver."""
    prompt = ("You are an external training-data quality judge, not a solver. Return only a JSON object "
        "with numeric fields student_score, expert_score, quality, context_score, completeness in [0,1], "
        "and boolean clear, answerable, recommended. Score correctness and reasoning reliability; "
        "quality measures training suitability.\n"+json.dumps({"question":question,"reference":reference,
        "student_response":student_text,"expert_response":expert_text},ensure_ascii=False))
    ids,length = sample_path(analyzer,prompt,max_tokens,greedy=True)
    raw = decoded_response(analyzer,ids,length)
    matches = re.findall(r"\{[^{}]+\}",raw)
    if not matches:
        return None
    try:
        record = json.loads(matches[-1])
        numbers = {name:float(record[name]) for name in
                   ("student_score","expert_score","quality","context_score","completeness")}
        if any(not 0 <= value <= 1 for value in numbers.values()):
            return None
        flags = {name:record[name] for name in ("clear","answerable","recommended")}
        if any(type(value) is not bool for value in flags.values()):
            return None
        return BoundaryAssessment(question=question,**numbers,**flags)
    except (ValueError,TypeError,KeyError):
        return None


def boundary_train(student, teacher, expert, analyzer, train, optimizer, *, max_tokens,
                   priming_examples, rounds, pool_examples, acquisition, replay_quota,
                   teacher_rollouts, analyzer_tokens):
    history = []
    for row in train[:priming_examples]:
        ids,length = sample_path(teacher,row["question"],max_tokens)
        text = decoded_response(teacher,ids,length)
        # Judge-free priming keeps nonempty teacher behavior, even if incorrect.
        update = sft_trajectory(student,row["question"],text,optimizer,max_tokens)
        if update:
            history.append({"stage":"priming",**update})
    previous = set()
    pool = train[priming_examples:priming_examples+pool_examples]
    if not pool:
        raise ValueError("BoundaryEvo requires a candidate pool disjoint from priming")
    for round_index in range(rounds):
        assessments, parse_failures = [], 0
        for row in pool:
            ids,length = sample_path(student,row["question"],max_tokens)
            student_text = decoded_response(student,ids,length)
            ids,length = sample_path(expert,row["question"],max_tokens)
            expert_text = decoded_response(expert,ids,length)
            assessment = judge_boundary(analyzer,row["question"],row["answer"],student_text,
                                        expert_text,analyzer_tokens)
            if assessment is None:
                parse_failures += 1
            else:
                assessments.append(assessment)
        selected = boundary_selection(assessments,previous,budget=acquisition,replay_quota=replay_quota)
        rows = {row["question"]:row for row in pool}
        verified, updates = 0, []
        for item in selected:
            row = rows[item.question]
            # Fresh teacher rollouts after QA selection, not cached expert answers.
            responses = []
            for _ in range(teacher_rollouts):
                ids,length = sample_path(teacher,row["question"],max_tokens)
                responses.append(decoded_response(teacher,ids,length))
            successes = [text for text in responses if verified_reward(text,row["answer"])]
            if successes:
                update = sft_trajectory(student,row["question"],successes[0],optimizer,max_tokens)
                if update:
                    verified += 1
                    updates.append(update)
        previous = {item.question for item in selected}
        event = {"stage":"evolution","round":round_index,"candidate_count":len(pool),
            "analyzer_parse_failures":parse_failures,"accepted_candidates":sum(a.accepted() for a in assessments),
            "selected_questions":len(selected),"verified_teacher_trajectories":verified,
            "optimizer_steps":len(updates),"selected_question_sha256":[hashlib.sha256(a.question.encode()).hexdigest() for a in selected],
            "assessments":[{k:v for k,v in asdict(a).items() if k!="question"} for a in assessments],
            "response_tokens":sum(u["response_tokens"] for u in updates)}
        history.append(event)
        print(json.dumps(event),flush=True)
    return history


def run_checkpoint(*, objective, student_path, student_id, student_revision, teacher_path,
    teacher_id, teacher_revision, train_path, validation_path, dataset_revision, split_manifest,
    output, auxiliary_path=None, auxiliary_id=None, auxiliary_revision=None,
    expert_path=None, expert_id=None, expert_revision=None, analyzer_path=None,
    analyzer_id=None, analyzer_revision=None, seed=42, steps=2, max_tokens=64, group=2,
    validation_examples=4, learning_rate=1e-5, device="cuda", forks=3, continuations=2,
    pbr_weight=1., min_fork_gap=1, credit_size=6, kl_weight=.01, retention=.6,
    priming_examples=2, rounds=2, pool_examples=4, acquisition=2, replay_quota=1,
    teacher_rollouts=2, analyzer_tokens=256):
    if objective not in OBJECTIVES or min(steps,max_tokens,group,validation_examples) < 1:
        raise ValueError("invalid objective or runtime budget")
    if objective=="boundary-evo" and (min(priming_examples,pool_examples,acquisition)<1 or rounds<2 or teacher_rollouts<2):
        raise ValueError("priming, acquisition and at least two fresh teacher rollouts required")
    if not re.fullmatch(r"[0-9a-fA-F]{40}",dataset_revision):
        raise ValueError("immutable public dataset commit required")
    split = validate_holdout(split_manifest,train_path,validation_path,dataset_revision=dataset_revision)
    if not split["verified"]:
        raise ValueError("verified public training-only holdout manifest is required")
    train,valid = load_public_rows(train_path),load_public_rows(validation_path)
    torch.manual_seed(seed)
    student = load_role(student_path,student_id,student_revision,device)
    teacher = load_role(teacher_path,teacher_id,teacher_revision,device)
    same_tokenizer = student.tokenizer.get_vocab()==teacher.tokenizer.get_vocab()
    if objective in {"branch-opd","road-mopd"} and not same_tokenizer:
        raise ValueError("BranchOPD/Road require identical token identities")
    if objective=="cast" and same_tokenizer:
        raise ValueError("CAST runtime validates the actual cross-tokenizer path; choose heterogeneous tokenizers")
    install_lora(student.model)
    params = [p for p in student.model.parameters() if p.requires_grad]
    before = [p.detach().clone() for p in params]
    optimizer = torch.optim.AdamW(params,lr=learning_rate,weight_decay=0)
    identities = {"student":student.identity,"teacher":teacher.identity}
    if objective=="road-mopd":
        auxiliary = load_role(auxiliary_path,auxiliary_id,auxiliary_revision,device)
        if (auxiliary.identity["id"],auxiliary.identity["revision"]) == (teacher.identity["id"],teacher.identity["revision"]):
            raise ValueError("Road requires distinct frozen teachers, not renamed copies")
        if auxiliary.tokenizer.get_vocab()!=student.tokenizer.get_vocab():
            raise ValueError("auxiliary teacher token identities must match student")
        domains = sorted({row.get("domain","") for row in train})
        if len(domains)!=2 or "" in domains:
            raise ValueError("Road requires exactly two explicitly labeled domains")
        domain_data = [[row for row in train if row["domain"]==domain] for domain in domains]
        identities["auxiliary"] = auxiliary.identity
    history = []
    if objective=="boundary-evo":
        expert = load_role(expert_path,expert_id,expert_revision,device)
        analyzer = load_role(analyzer_path,analyzer_id,analyzer_revision,device)
        identities.update(expert=expert.identity,analyzer=analyzer.identity)
        history = boundary_train(student,teacher,expert,analyzer,train,optimizer,max_tokens=max_tokens,
            priming_examples=priming_examples,rounds=rounds,pool_examples=pool_examples,acquisition=acquisition,
            replay_quota=replay_quota,teacher_rollouts=teacher_rollouts,analyzer_tokens=analyzer_tokens)
    else:
        for step in range(steps):
            question = train[step%len(train)]["question"]
            if objective=="branch-opd":
                item = branch_step(student,teacher,question,optimizer,max_tokens=max_tokens,forks=forks,
                    continuations=continuations,pbr_weight=pbr_weight,min_fork_gap=min_fork_gap)
            elif objective=="cast":
                item = cast_step(student,teacher,question,optimizer,max_tokens=max_tokens,group=group,
                                 credit_size=credit_size,kl_weight=kl_weight)
            else:
                item = road_step(student,[teacher,auxiliary],[rows[step%len(rows)] for rows in domain_data],
                                 optimizer,max_tokens=max_tokens,retention=retention)
            item["step"] = step
            history.append(item)
            print(json.dumps(item),flush=True)
    correct = 0
    for row in valid[:validation_examples]:
        ids,length = sample_path(student,row["question"],max_tokens,greedy=True)
        correct += verified_reward(decoded_response(student,ids,length),row["answer"])
    n = min(validation_examples,len(valid))
    delta = sum(float((p.detach()-old).square().sum()) for p,old in zip(params,before))**.5
    activity = {}
    if objective=="branch-opd":
        activity = {"sampled_branches":sum(item["branches"] for item in history),
                    "pbr_constraints":sum(item["pbr_constraints"] for item in history)}
    elif objective=="cast":
        activity = {"aligned_tokens":sum(item["aligned_tokens"] for item in history),
                    "unaligned_tokens":sum(item["unaligned_tokens"] for item in history)}
    elif objective=="road-mopd":
        activity = {"projected_tensors":sum(item["projected_tensors"] for item in history),
                    "conflicting_tensors":sum(item["conflicting_tensors"] for item in history)}
    else:
        evolution = [item for item in history if item["stage"]=="evolution"]
        activity = {"priming_optimizer_steps":sum(item["stage"]=="priming" for item in history),
            "evolution_optimizer_steps":sum(item["optimizer_steps"] for item in evolution),
            "boundary_rounds_with_updates":sum(item["optimizer_steps"]>0 for item in evolution),
            "analyzer_parse_failures":sum(item["analyzer_parse_failures"] for item in evolution)}
    result = {"schema_version":1,"adapter_key":objective,"seed":seed,"diagnostic_only":True,
        "evaluation_tier":"l1_mechanism","claim_scope":"bounded real checkpoint runtime validation; no benchmark gain claim",
        "models":identities,"dataset":{"id":split["source_id"],"revision":dataset_revision,
        "train_sha256":hashlib.sha256(Path(train_path).read_bytes()).hexdigest(),
        "validation_sha256":hashlib.sha256(Path(validation_path).read_bytes()).hexdigest()},
        "budget":{"steps":steps,"max_tokens":max_tokens,"group":group,"forks":forks,
        "continuations":continuations,"priming_examples":priming_examples,"rounds":rounds,
        "pool_examples":pool_examples,"acquisition":acquisition,"teacher_rollouts":teacher_rollouts},
        "metrics":{"adapter_parameter_delta_l2":delta,"validation_examples":n,
                   "validation_exact_match":correct/n,**activity},"history":history,"split_provenance":split,
        "test_read":False,"validation_used_for_selection":False,"gold_in_rollout":False}
    output = Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n")
    return result


def run_adapter(key, dataset_dir, seed):
    """Packaged adapter entry; require explicit real-checkpoint configuration."""
    dataset_dir = Path(dataset_dir)
    path = dataset_dir/f"oct12-{key}.json"
    if not path.is_file():
        raise ValueError(f"real checkpoint configuration required: {path}; see scripts/run_oct12_post_training.py --help")
    config = json.loads(path.read_text())
    if config.get("objective",key)!=key or any("test" in name for name in config):
        raise ValueError("adapter objective mismatch or forbidden test input")
    for name in ("student_path","teacher_path","auxiliary_path","expert_path","analyzer_path",
                 "train_path","validation_path","split_manifest","output"):
        if config.get(name):
            value = Path(config[name])
            config[name] = value if value.is_absolute() else dataset_dir/value
    config.update(objective=key,seed=seed)
    result = run_checkpoint(**config)
    # The generic artifact writer then enriches this with its result schema v2.
    result.pop("schema_version",None)
    return result


def render(result):
    metrics = result["metrics"]
    return (f"# {result['adapter_key']} 实际 checkpoint 诊断\n\n"
        "短预算、单 seed 结果不支持稳定提升；论文原始指标不与此结果比较。\n\n"
        f"LoRA 参数变化 L2：{metrics['adapter_parameter_delta_l2']:.6g}；"
        f"validation exact match：{metrics['validation_exact_match']:.4f} "
        f"（{metrics['validation_examples']} 题）。\n\n"
        "公开 train-only holdout 哈希已校验，test 未读取，gold 不进入 solver rollout。\n")
