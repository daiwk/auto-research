# Boundary-aware Curriculum RL（CoBA-RL）

> 定位当前能力边界，对边界附近样本提供教师引导，再用 RL 固化新增推理模式。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Curriculum Reinforcement Learning Can Incentivize Reasoning Capacity in LLMs Beyond the Base Model](https://arxiv.org/abs/2606.22317) |
| 公司 / 机构 | Zhejiang University / National University of Singapore |
| 首次公开日期 | 2026-06-21 |
| 原作者代码 | 未发布 / 未发现独立官方仓库 |
| 本地 adapter / CLI key | `coba-rl` |
| 本地复现代码 | `src/auto_research/post_training/` |

## 原始论文总结

### 背景与主要改动

普通 RLVR 可能只重新分配 base model 已有轨迹的概率，提升 pass@1 却不扩展高采样
pass@k 所反映的能力边界。该方法先用多次采样估计边界，在边界附近/之外注入教师
推理，再用 RL 巩固。

```mermaid
flowchart LR
    D["按难度组织问题"] --> K["pass@k 探测能力边界"]
    K --> S["选择边界附近样本"]
    S --> T["失败时教师引导"]
    T --> R["verifier reward + RL 固化"]
    R --> K
```

<!-- paper-figure:start -->
### 原论文关键图

[![Boundary-aware Curriculum RL（CoBA-RL） 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2606.22317v1/x1.png)

> **原论文 Figure 2（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2606.22317)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

$$
b_{t+1}=\operatorname{clip}\!\left(
\alpha b_t+(1-\alpha)(d(x)+\Delta(\widehat{\mathrm{pass}})),0,1
\right),
$$

本地以 $b_t$ 选择难度最接近的样本，并对自由生成序列执行 clipped policy update。

### 论文离线与线上效果

论文在 Qwen、Llama、DeepSeek base models 上同时提升 pass@1 与 pass@256；平均
pass@256 相对 base model 提升 9.8 个百分点、相对 Vanilla RLVR 提升 10.3 个百分点。
没有生产线上 A/B 实验。

## 本地复现

本地算术 suite 带可复现难度；训练器维护动态 curriculum boundary、采样边界样本，
无正确 rollout 时记录 teacher-guidance 事件，并以 numeric verifier 进行 sequence RL。

```bash
auto-research post-train --algorithm coba-rl --dataset arithmetic-generate \
  --maximum-examples 48 --steps 6 --seeds 42,43,44 --offline
```

稳定指标：
[`free-generation-post-training-seeds42-44.json`](../../experiments/free-generation-post-training-seeds42-44.json)。

## 复现边界

实现了边界状态、难度课程、教师触发和自由生成 RL 闭环；本地未计算论文规模的
pass@256，也未蒸馏外部大教师，因此不能宣称复现论文中的能力边界增量。
