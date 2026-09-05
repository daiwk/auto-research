from pathlib import Path
import numpy as np
from ..industrial_2026 import base_scores,evaluate,load_industrial_data,summary_result,tune_blend
from .model import CoralLoop


def reproduce_coral(dataset_dir:Path,seed:int=42):
    data=load_industrial_data(dataset_dir); rng=np.random.default_rng(seed); sources=4
    loop=CoralLoop(sources,float(sources)); trace=[]
    conversion=np.array([.52,.41,.30,.19])+rng.normal(0,.005,sources); cost=np.array([1.1,.9,.8,.7])
    for cycle in range(5):
        config,effect=loop.step(conversion+cycle*np.array([.002,-.001,.003,0]),cost)
        trace.append({"cycle":cycle+1,"configuration":config.tolist(),"effect":effect,"budget":float(config.sum())})
    signal=np.zeros(data.item_count)
    for source,weight in enumerate(loop.config): signal[data.domains%sources==source]=weight
    method=lambda history: base_scores(data,history)+.15*signal+.1*data.transition[history[-1]]
    baseline_fn=lambda history:base_scores(data,history); alpha,blended,_=tune_blend(data,baseline_fn,method)
    return summary_result(key="coral",paper={"arxiv_id":"2609.02730","title":"CORAL: An LLM-Native Harness for Production Recommender Systems","url":"https://arxiv.org/abs/2609.02730","organization":"Meta AI"},data=data,baseline_name="fixed equal retrieval allocation",method_name=f"five-cycle CORAL allocation (blend={alpha:.1f})",baseline=evaluate(data,baseline_fn),proposed=evaluate(data,blended),stages={"cycles":len(trace),"memory_horizon":3,"all_budget_feasible":all(x["budget"]<=sources+1e-7 for x in trace),"trace":trace},paper_results={"watch_time_percent":.15,"sessions_percent":.16,"new_low_signal_sessions_percent":.23,"second_round_savings_increase_percent":44.0},scope="公开 MovieLens 上运行固定控制流、三周期记忆、约束投影和结果反馈；不接入 Meta 私有遥测、LLM 或线上实验系统。")


from ..industrial_2026 import render_standard as render
