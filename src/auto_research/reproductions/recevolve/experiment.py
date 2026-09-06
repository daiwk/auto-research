from pathlib import Path
import numpy as np
from ..industrial_2026 import base_scores,evaluate,load_industrial_data,summary_result
from .model import Candidate,ResearchLoop


def reproduce_recevolve(dataset_dir:Path,seed:int=42):
    del seed
    data=load_industrial_data(dataset_dir)
    def scorer(candidate,history):
        base=base_scores(data,history)
        watch=np.power(np.maximum(data.popularity,1e-5),candidate.watch_power)
        cross=data.cosine[list(history[-8:])].mean(0)*data.transition[history[-1]]
        return base/max(candidate.temperature,.05)+.12*watch+candidate.cross_strength*cross
    def validation(candidate):
        metrics=evaluate(data,lambda h:scorer(candidate,h),target_split="validation")
        return metrics["ndcg_at_10"]+.25*metrics["hit_at_10"]
    candidates=[Candidate(),Candidate(.8),Candidate(.8,.5),Candidate(.8,.5,.5),Candidate(.8,.5,.5,True),Candidate(.01,1,1)]
    loop=ResearchLoop(candidates[0])
    for candidate in candidates: loop.evaluate(candidate,validation)
    baseline=evaluate(data,lambda h:scorer(candidates[0],h)); method=evaluate(data,lambda h:scorer(loop.champion,h))
    return summary_result(key="recevolve",paper={"arxiv_id":"2609.01622","title":"RecEvolve: A Knowledge-Driven Autonomous Agent System for Recommender Systems","url":"https://arxiv.org/abs/2609.01622","organization":"Google"},data=data,baseline_name="fixed Two-Tower-style similarity",method_name="validation-selected RecEvolve champion",baseline=baseline,proposed=method,stages={"experiments":len(candidates),"isolated_trials":len(loop.knowledge),"rollbacks":loop.rollbacks,"reward_hacks_blocked":loop.reward_hacks,"champion":loop.champion.__dict__},paper_results={"offline_ndcg50_gain_percent":19.9,"online_user_satisfaction_percent":3.77,"online_unique_content_percent":7.44,"autonomous_runs":41},scope="公开 MovieLens 上执行提案、critic gate、隔离评价、冠军继承、回滚和 reward-hack 拒绝；不复刻 Google 私有 Two-Tower、TPU 集群和线上流量。")


from ..industrial_2026 import render_standard as render
