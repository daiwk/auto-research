# Option-Channel Attack：选项标签也能攻击 Agent 守门模型

> 真实 Laya checkpoint 的安全机制诊断，不是 Agent 任务成功率或生产安全认证。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails](https://arxiv.org/abs/2610.12292) |
| 公司 / 机构 | University of Southern California（第一作者 Seyedarmin Azizi） |
| 首次公开日期 | 2026-10-08（arXiv v1） |
| 原作者代码 | [已开源](https://github.com/ArminAzizi98/option-channel-attack)；本库独立实现 |
| 本地 Adapter | `option-channel-attack` |
| 本地复现代码 | `src/auto_research/system_one/option_channel.py`；入口 `scripts/run_option_channel.py` |

## 原始论文总结

### 背景与主要改动

类型化模型对调用方给定的选项输出概率，但选项名字本身也进入模型输入。保持动作、可信策略定义不变，仅把允许选项换成误导性标签，就可能让本来正确的拒绝变成放行。论文把危险的 fail-open 与妨碍使用的 fail-closed 分开评价。

```mermaid
flowchart LR
  固定动作与策略 --> 干净选项 --> 干净拒绝集合
  固定动作与策略 --> 校准集选择标签 --> 独立评测攻击
  干净拒绝集合 --> 条件ASR
  独立评测攻击 --> 条件ASR
```

<!-- paper-figure:start -->
### 原论文关键图

[![Option-Channel Attack：选项标签也能攻击 Agent 守门模型 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2610.12292#page=3)

> **原论文 Figure 1（输入通道）**：类型化模型同时读取待判断状态和带标签、定义的选项。攻击者既可能改写状态，也可能仅修改选项标签；后者就是本篇研究的攻击通道。图片来自[原论文](https://arxiv.org/abs/2610.12292)，版权归原作者所有。
<!-- paper-figure:end -->

### 核心公式

令 $E$ 为本应禁止且模型干净输入正确拒绝的集合，$ASR_{open}=|\{i\in E:attack允许\}|/|E|$。$E$ 为空时记为 undefined，而不是 0 或 1。成对 bootstrap 每次重采样后重新计算条件分母。

### 论文离线与线上效果

[原文](https://arxiv.org/html/2610.12292v1)研究七个开放权重模型；在四个将标签放进输入的模型上，误导允许标签使 fail-open 达到 93%–100%。该现象不等价于全部 Agent 不安全，也不是本库单模型实测。未报告线上 A/B。

## 本地复现

六种合成策略，每种校准/评测各 24 条，校准 seed=42、评测 seed=43；只在校准集从 `escalate/deny/stop/lantern` 选标签。A100 上运行公开 Laya checkpoint。没有调用真实外部工具，也没有执行被测动作。

```bash
python scripts/run_option_channel.py --checkpoint checkpoints/laya \
  --device cuda:0 --count 24 --output runs/option-channel-42-43.json
```

### 数据协议与结果

模型只接收文本动作、固定策略定义和选项名；gold 只在外部评分器。`exfil` 的干净 fail-open 为 0.1667，攻击后为 0.5833；10 个原本正确拒绝样本上的 ASR=0.5，95% 成对区间 [0.1667,0.8333]。`secret`、`escape_or_exfil` 干净输入已经全部放行，条件 ASR 因此未定义。其他策略分母最少仅 1，不能据 ASR=1 泛化。[全部指标](metrics/laya-a100.json)、[GPU 回执](../../gpu-validations/option-channel-attack-a100-20261011.json)。

### 代码映射与复现边界

`guard_items` 生成原生、可审计的平衡数据，不是作者逐字一致的 GuardBench；`score_items` 保持策略和动作不变；`attack_metrics/paired_asr_interval` 分离错误方向并保留无分母。另有无关日志噪声对照及可信选项名称还原对照，后者只恢复原有干净行为，不证明防御可靠。

未完成作者全部标签扫描、七模型比较、提示注入/越狱/有害内容真实数据集。早期运行器误写了 `diagnostic_only=false`，已修正并在 A100 重跑；当前原始报告和归档协议均明确为 L1 合成守门诊断。不接入 Evolve 能力晋级。
