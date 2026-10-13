"""Actual policy-driven search, context-isolated recall and LoRA GRPO updates."""
from __future__ import annotations

from pathlib import Path
import torch

from auto_research.oct12_public_sources import read_jsonl_mirror
from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.oct13_common import (CostLedger,ExecutionFailure,load_policy,load_split,
    policy_gradient_step,result_payload)
from .algorithm import (LexicalRetriever,internal_messages,normalize,parse_step,source_observation,source_reward)

SYSTEM=("Answer the question using actual INTERNAL and EXTERNAL information. "
        "Output <think>reasoning</think> then exactly one <search>atomic query</search> to fetch sources, "
        "or <information_source>internal/external</information_source><answer>concise answer</answer>. "
        "Never generate <information> yourself. A search receives both sources as an observation.")


def run(config,*,seed=42):
    train,validation,split=load_split(config)
    directory=Path(config["corpus_path"])
    documents,corpus=read_jsonl_mirror(directory,"documents.jsonl",config["corpus_id"],config["corpus_revision"],"train")
    retriever=LexicalRetriever(documents)
    policy,ledger=load_policy(config,seed=seed),CostLedger()
    reference=load_policy(config,seed=seed)
    max_tokens=int(config.get("max_tokens",256))
    max_turns=int(config.get("max_turns",3))
    group=int(config.get("group",4))
    variant=config.get("variant","source-consistent")
    if variant not in {"source-consistent","without-source-reward"} or min(max_turns,group-1)<1:
        raise ValueError("invalid source-aware workflow budget/ablation")
    def correct(answer,reference_answer):
        if config.get("verifier","numeric")=="numeric":
            return verified_reward(answer,reference_answer)
        return float(normalize(answer)==normalize(reference_answer))
    def episode(question):
        messages=({"role":"system","content":SYSTEM},{"role":"user","content":question})
        records,streams,searches=[],{"internal":"","external":""},0
        valid=True
        final={"kind":"invalid"}
        for turn in range(max_turns):
            response=ledger.sample(policy,messages,role="policy_trajectory",max_tokens=max_tokens)[0]
            records.append((messages,response))
            action=parse_step(response.text)
            if response.truncated or "<information>" in response.text:
                valid=False
            if action["kind"]=="answer":
                final=action
                break
            if action["kind"]!="search":
                valid=False
                break
            query=action["query"]
            # Uses same current policy parameters, but only isolated query context.
            recall=ledger.sample(policy,internal_messages(query),role="isolated_internal_recall",max_tokens=max_tokens)[0]
            retrieved=retriever.retrieve(query,top_k=3)
            internal=recall.text
            external="\n".join(d["text"] for d in retrieved)
            streams["internal"]+="\n"+internal
            streams["external"]+="\n"+external
            searches+=1
            messages=messages+({"role":"assistant","content":response.text},
                               {"role":"user","content":source_observation(internal,external)})
        return records,final,streams,valid,searches
    def assess():
        outputs=[]
        devices=[torch.cuda.current_device()] if str(policy.device).startswith("cuda") else []
        with torch.random.fork_rng(devices=devices):
            torch.manual_seed(seed+10000)
            for row in validation:
                records,final,streams,valid,searches=episode(row["question"])
                reward=correct(final.get("answer",""),row["answer"]) if final["kind"]=="answer" else 0.
                _,components=source_reward(final,streams,answer_correct=reward,format_valid=valid)
                outputs.append({"correct":reward,**components,"searches":searches})
        return {"accuracy":sum(o["correct"] for o in outputs)/len(outputs),
                "source_consistency":sum(o["source_match"] for o in outputs)/len(outputs),
                "format_compliance":sum(o["format"] for o in outputs)/len(outputs),
                "mean_searches":sum(o["searches"] for o in outputs)/len(outputs),"examples":len(outputs)}
    baseline=assess()
    policy.prepare_lora(learning_rate=float(config.get("learning_rate",1e-5)))
    before=policy.trainable_digest()
    training=[]
    for step in range(int(config.get("steps",2))):
        row=train[step%len(train)]
        trajectories,rewards,components=[],[],[]
        for _ in range(group):
            records,final,streams,valid,searches=episode(row["question"])
            answer_correct=correct(final.get("answer",""),row["answer"]) if final["kind"]=="answer" else 0.
            reward,parts=source_reward(final,streams,answer_correct=answer_correct,format_valid=valid,
                                      source_coefficient=.1 if variant=="source-consistent" else 0.)
            trajectories.append(records)
            rewards.append(reward)
            components.append({**parts,"searches":searches})
        # Same trajectory advantage for actual policy outputs only. Tool/recall
        # observation tokens never receive policy loss or labels.
        flat,repeated,old=[],[],[]
        with torch.no_grad():
            for records,reward in zip(trajectories,rewards):
                for messages,response in records:
                    flat.append((messages,response))
                    repeated.append(reward)
                    old.append(ledger.score(policy,messages,response.tokens,role="behavior").detach())
        # Compute the group statistics on TRAJECTORIES, not flattened turns.
        advantages=torch.tensor(rewards,device=policy.device)
        advantages=(advantages-advantages.mean())/(advantages.std(unbiased=False)+1e-6)
        turn_advantages=[float(a) for records,a in zip(trajectories,advantages) for _ in records]
        trajectory_token_counts=[sum(len(response.tokens) for _,response in records)
                                 for records in trajectories for _ in records]
        # Passing standardized trajectory advantages as rewards preserves their
        # signs but centering flattened unequal turns would change the target.
        # Use direct token surrogate below instead of a turn-weighted proxy.
        if not bool(advantages.abs().sum()):
            training.append({"step":step+1,"optimizer_update_executed":False,"zero_advantage_group":True,
                             "components":components})
            continue
        from auto_research.post_training.oct13_common import optimizer_step
        policy.model.train()
        losses=[]
        for index,(messages,response) in enumerate(flat):
            current=ledger.score(policy,messages,response.tokens,role="student_rl")
            ratio=(current-old[index]).exp()
            a=turn_advantages[index]
            with torch.no_grad():
                ref=ledger.score(reference,messages,response.tokens,role="reference")
            difference=ref-current
            token_loss=-torch.minimum(ratio*a,ratio.clamp(.8,1.2)*a)
            token_loss+=float(config.get("kl_beta",.001))*(difference.exp()-difference-1)
            loss=token_loss.sum()/trajectory_token_counts[index]
            losses.append(loss)
        audit=optimizer_step(policy,losses,denominator=group)
        training.append({"step":step+1,**audit,"components":components,"trajectory_rewards":rewards,
                         "trajectory_advantages":advantages.tolist(),"zero_advantage_group":False})
    changed=before!=policy.trainable_digest()
    if not changed:
        raise ExecutionFailure("all real source-aware trajectory groups had zero advantage; no update fabricated",
                               {"training":training,"cost":ledger.to_dict(),"corpus_revision":corpus["revision"]})
    return result_payload("soar",config,seed,split,policy,ledger,baseline,assess(),training,
        parameters_changed=changed,variant=variant,
        corpus={"public_id":corpus["public_id"],"revision":corpus["revision"],"file_sha256":corpus["files"]},
        limitations=["Lexical retrieval over a small hash-verified public source corpus replaces E5 + 2018 Wikipedia infrastructure.",
                     "Policy searches, internal recall, source declaration and GRPO updates are real; no gold-generated source text.",
                     "EM source matching is a bounded operationalization; published v1 does not specify its normalization code.",
                     "Tiny checkpoint/holdout diagnostics do not reproduce the seven QA benchmarks or external judge fabrication rate."])
