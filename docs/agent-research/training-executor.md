# 可训练 Agent policy 与真实 executor

本页对应 `AG-001` 和 `AG-002`，把过去的确定性机制模拟推进到两个可执行层级。

## Agent Lightning → checkpoint policy

`agent-policy-train` 把 rollout 拆成 prompt、失败 patch、成功 patch 三类 span；失败 transition
得到负 credit，成功 transition 得到正 credit，再以 pairwise causal-LM loss 更新固定 revision
的 SmolLM2 policy。更新前后都让模型在两个 patch 之间打分，并将选中的 patch 写入临时仓库，
真实执行 `python -m unittest -q`。

```bash
auto-research agent-policy-train \
  --model-id HuggingFaceTB/SmolLM2-135M-Instruct \
  --steps 6 --episodes 6 --learning-rate 1e-5 \
  --device cuda --output-dir runs/agent-lightning-policy
```

这验证的是 Agent Lightning 的“执行 trace 与训练解耦、transition credit 回传到可训练
policy”链路。micro fixture 不是官方 SWE-bench，不能外推为真实软件工程泛化能力。

A30 三步真实反传中产生 6 个 credit update；loss 为 `0.5013 / 0.4724 / 0.6142`。
训练前后 joint success 都是 `1.0`，说明桥接链路可执行，但饱和的三题 micro-suite 没有
能力提升。稳定摘要见 [`../experiments/roadmap-4-7.json`](../experiments/roadmap-4-7.json)。

## 同预算 executor 矩阵

`agent-matrix` 对所有方法复用完全相同的仓库、issue、测试和最多每 episode 四次 subprocess
预算，统一记录成功率、真实命令数、文件编辑数、复用率和成本：

```bash
auto-research agent-matrix \
  --methods direct,critic,agent-lightning,swe-agent,openhands \
  --episodes 12 --seeds 42,43,44
```

矩阵不会把不同 foundation model 或外部 API 费用混在一起；当前策略均不调用外部 LLM，
因此比较的是 controller/executor 机制。以后接真实 checkpoint 时，必须在整张矩阵固定同一
模型 revision、上下文长度、生成 token 和工具调用上限。

当前 12 episodes × 3 seeds 的结果中，direct joint success 为 `0.0`；CRITIC、
Agent Lightning、SWE-agent 与 OpenHands 均为 `1.0`。它们的平均成本分别为
`4.0 / 3.625 / 2.5 / 2.5`，Agent Lightning 的跨题复用率为 `0.75`。这些结果用于暴露
controller 成本和复用差异，不用于宣称大型代码 benchmark 排名。
