"""Real frozen reasoner/encoder, trained MLP heads, equal-generation controls."""
from __future__ import annotations

import hashlib
import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.oct13_common import (CostLedger, ExecutionFailure, causal_response_features,
    load_policy, load_split, result_payload, sample_prefix)
from auto_research.reproductions.progressive_contraction.algorithm import paragraph_prefixes
from .algorithm import (CorrectnessGate, INSTRUCTION, PositionHead, boxed_token_position, calibrated_gate,
                        position_loss, remaining_response_budget)


def _digest(module):
    return hashlib.sha256(b"".join(p.detach().float().cpu().numpy().tobytes() for p in module.parameters())).hexdigest()


def intervention_prefix_tokens(reasoner,messages,retained_tokens):
    """Append actual chat-role suffix tokens to the ORIGINAL retained tokens.

    Re-encoding prompt+generated text can merge tokens at their boundary. The
    original prefix is therefore never decoded/re-encoded for model input.
    Only new turn delimiters/instruction are tokenized from the real template.
    """
    tokenizer=reasoner.tokenizer
    if not getattr(tokenizer,"chat_template",None):
        raise ExecutionFailure("UPTURN requires an explicit chat turn template")
    retained=tokenizer.decode(retained_tokens,skip_special_tokens=False)
    closing="</think>" if retained.count("<think>")>retained.count("</think>") else ""
    original_text=tokenizer.apply_chat_template(list(messages),tokenize=False,add_generation_prompt=True)
    suffix_messages=tuple(messages)+({"role":"assistant","content":closing},
                                     {"role":"user","content":INSTRUCTION})
    closed_text=tokenizer.apply_chat_template(list(suffix_messages),tokenize=False,add_generation_prompt=True)
    if not closed_text.startswith(original_text):
        raise ExecutionFailure("chat template changed the original open-assistant prefix; no approximate cut used")
    suffix=tokenizer(closed_text[len(original_text):],add_special_tokens=False).input_ids
    return tuple(retained_tokens)+tuple(suffix)


def run(config, *, seed=42):
    train, validation, split = load_split(config)
    ledger = CostLedger()
    encoder = load_policy(config, seed=seed)
    reasoner = load_policy(config, role="teacher", seed=seed)
    if encoder.vocabulary_sha256 != reasoner.vocabulary_sha256:
        raise ValueError("encoder must consume the exact generated tokens, not re-tokenized text")
    hidden = encoder.model.config.hidden_size
    position = PositionHead(hidden).to(encoder.device)
    gate = CorrectnessGate(hidden).to(encoder.device)
    pos_before, gate_before = _digest(position), _digest(gate)
    pos_optimizer = torch.optim.AdamW(position.parameters(), lr=1e-3, weight_decay=0)
    gate_optimizer = torch.optim.AdamW(gate.parameters(), lr=1e-3, weight_decay=0)
    max_tokens, group = int(config.get("max_tokens",512)), int(config.get("group",4))
    cuts_per_group, suffixes = int(config.get("cuts",4)), int(config.get("suffixes",2))
    if min(group, cuts_per_group-1, suffixes) < 1 or len(train) < 2:
        raise ValueError("positive rollout budget, >=2 cuts and separate gate train/calibration prompts required")
    delimiter = reasoner.tokenizer("\n\n", add_special_tokens=False).input_ids
    def encode(messages,tokens):
        prompt=reasoner.prompt_ids(messages)
        ledger.encoder_calls+=1
        ledger.encoded_input_tokens+=prompt.shape[1]+len(tokens)
        return causal_response_features(encoder,messages,tokens,prompt_token_ids=prompt)
    gate_train, gate_calibration, failed = [], [], []
    for row_index,row in enumerate(train):
        messages = problem_messages("Write reasoning paragraphs separated by blank lines.\n"+row["question"])
        responses = ledger.sample(reasoner, messages, role="frozen_reasoner_training", samples=group,max_tokens=max_tokens)
        for response in responses:
            features = encode(messages,response.tokens)
            correctness = 0. if response.truncated else verified_reward(response.text,row["answer"])
            box = boxed_token_position(response.tokens, encoder.tokenizer)
            if box is not None:
                destination = gate_calibration if row_index >= max(1,len(train)*3//4) else gate_train
                destination.append((features[box],correctness))
            cuts = paragraph_prefixes(response.tokens, delimiter, limit=int(config.get("max_cuts",16)))
            cuts = [cut for cut in cuts if cut < max_tokens]
            if not correctness and len(cuts)>=2:
                failed.append((row,messages,response,features,cuts))
    if not gate_train or not gate_calibration or not failed:
        raise ExecutionFailure("insufficient real boxed gate data or failed rollouts with >=2 paragraph cuts",
            {"gate_training_cases":len(gate_train),"gate_calibration_cases":len(gate_calibration),
             "eligible_failed_rollouts":len(failed),"cost":ledger.to_dict()})
    gate_features = torch.stack([x[0] for x in gate_train])
    gate_labels = torch.tensor([x[1] for x in gate_train],device=encoder.device)
    gate_history = []
    for epoch in range(int(config.get("gate_epochs",20))):
        gate_optimizer.zero_grad(set_to_none=True)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(gate(gate_features),gate_labels)
        loss.backward()
        gate_optimizer.step()
        gate_history.append(float(loss.detach()))
    cal_features = torch.stack([x[0] for x in gate_calibration])
    cal_labels = torch.tensor([x[1] for x in gate_calibration],device=encoder.device)
    with torch.no_grad():
        cal_logits = gate(cal_features)
        temperatures = (.5,1.,1.38,2.)
        scores = [float(torch.nn.functional.binary_cross_entropy_with_logits(cal_logits/t,cal_labels)) for t in temperatures]
        temperature = temperatures[min(range(len(scores)),key=lambda i:scores[i])]
    training = []
    for step in range(int(config.get("steps",2))):
        row,messages,response,features,cuts = failed[step%len(failed)]
        candidate_features = features[torch.tensor([cut-1 for cut in cuts],device=encoder.device)]
        with torch.no_grad():
            old_logits = position(candidate_features)
            selected = torch.multinomial(old_logits.softmax(-1),min(cuts_per_group,len(cuts)),replacement=False).tolist()
            old = old_logits.log_softmax(-1)[selected].detach()
        rewards = []
        for index in selected:
            cut = cuts[index]
            prefix=intervention_prefix_tokens(reasoner,messages,response.tokens[:cut])
            revised = sample_prefix(reasoner,messages,prefix,ledger,role="position_rescue_training",
                                    samples=suffixes,max_tokens=remaining_response_budget(max_tokens,cut))
            rewards.append(sum(0. if r.truncated else verified_reward(r.text,row["answer"]) for r in revised)/suffixes)
        pos_optimizer.zero_grad(set_to_none=True)
        loss,audit = position_loss(position(candidate_features),selected,old,rewards)
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(position.parameters(),1.,error_if_nonfinite=True)
        if float(norm)>0:
            pos_optimizer.step()
        training.append({"step":step+1,"cuts": [cuts[i] for i in selected],"loss":float(loss.detach()),
                         "gradient_l2_norm":float(norm),"optimizer_update_executed":float(norm)>0,**audit})
    evaluation_group = int(config.get("evaluation_group",2))
    def assess():
        base_rows,method_rows,budgets = [],[],[]
        devices = [torch.cuda.current_device()] if str(encoder.device).startswith("cuda") else []
        with torch.random.fork_rng(devices=devices):
            torch.manual_seed(seed+10000)
            for row in validation:
                messages = problem_messages("Write reasoning paragraphs separated by blank lines.\n"+row["question"])
                originals = ledger.sample(reasoner,messages,role="evaluation_originals",samples=evaluation_group,max_tokens=max_tokens)
                extras = ledger.sample(reasoner,messages,role="matched_base_extra",samples=evaluation_group,max_tokens=max_tokens)
                revised_pool, corrections, regeneration_tokens = [],0,0
                for original in originals:
                    features = encode(messages,original.tokens)
                    box = boxed_token_position(original.tokens,encoder.tokenizer)
                    score = (float(calibrated_gate(gate(features[box]),temperature=temperature)) if box is not None else 0.)
                    cuts = [c for c in paragraph_prefixes(original.tokens,delimiter,limit=16) if c<max_tokens]
                    if score>=.4 or not cuts:
                        revised_pool.append(original)
                        continue
                    with torch.no_grad():
                        logits = position(features[torch.tensor([c-1 for c in cuts],device=encoder.device)])
                        cut = cuts[int(torch.multinomial(logits.softmax(-1),1))]
                    prefix=intervention_prefix_tokens(reasoner,messages,original.tokens[:cut])
                    revised = sample_prefix(reasoner,messages,prefix,ledger,role="evaluation_correction",
                        samples=1,max_tokens=remaining_response_budget(max_tokens,cut))[0]
                    revised_pool.append(revised)
                    corrections += 1
                    regeneration_tokens += len(revised.tokens)
                base_reward = [0. if r.truncated else verified_reward(r.text,row["answer"]) for r in originals+extras]
                method_reward = [0. if r.truncated else verified_reward(r.text,row["answer"]) for r in revised_pool]
                base_rows.append((sum(base_reward)/len(base_reward),float(any(base_reward))))
                method_rows.append((sum(method_reward)/len(method_reward),float(any(method_reward))))
                budgets.append({"method_generations":evaluation_group+corrections,"base_generations":2*evaluation_group,
                    "method_generated_tokens":sum(len(r.tokens) for r in originals)+regeneration_tokens,
                    "base_generated_tokens":sum(len(r.tokens) for r in originals+extras),
                    "maximum_response_token_allowance":2*evaluation_group*max_tokens})
        def metric(rows):
            return {"avg_accuracy":sum(r[0] for r in rows)/len(rows),"pass_rate":sum(r[1] for r in rows)/len(rows),"examples":len(rows)}
        return metric(base_rows),metric(method_rows),budgets
    baseline,after,budgets = assess()
    return result_payload("upturn",config,seed,split,reasoner,ledger,baseline,after,training,
        parameters_changed=pos_before!=_digest(position) and gate_before!=_digest(gate),
        encoder=encoder.provenance,encoder_frozen=all(not p.requires_grad for p in encoder.model.parameters()),
        reasoner_frozen=all(not p.requires_grad for p in reasoner.model.parameters()),
        gate={"training_bce":gate_history,"training_cases":len(gate_train),"calibration_cases":len(gate_calibration),
              "calibration_temperature":temperature,"training_classes":sorted(set(gate_labels.tolist())),
              "threshold":.4,"calibration_split":"disjoint final quarter of train prompts; not validation"},
        position_informative_groups=sum(a["nonzero_rescue_advantage"] for a in training),
        execution_status="passed" if any(a["nonzero_rescue_advantage"] for a in training) else "failed-no-rescue-signal",
        generation_budget_controls=budgets,
        limitations=["Qwen2.5 frozen 0.5B encoder/7B reasoner and tiny GSM8K replace original Qwen3 and DAPO.",
                     "Only learned gate controls inference; correctness labels are never visible to gate/cut policy.",
                     "Zero rescue advantages and one-class gate labels remain visible and are not capability evidence.",
                     "Matched maximum generations and token allowance do not imply equal actual runtime."])
