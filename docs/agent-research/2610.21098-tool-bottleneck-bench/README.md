# ToolBottleneckBench：受控压力与固定预算下的公共工具评测接口

> 本地为 `evaluation_protocol_interface`：有限任务编译器、真实状态沙箱、九义务 exact grader，以及一组官方历史行的 CPU 复算。`adapter: null`、`diagnostic_only: true`、`promotion_eligible: false`、`evolve_integrated: false`；没有评测新的 Agent。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets](https://arxiv.org/abs/2610.21098) |
| 公司/机构 | 一作 Zichuan Xu：University of Osaka；合作者 Initial S、Nagoya University |
| 首次公开日期 | 2026-10-15，arXiv v1 01:59:58 UTC（北京时间 09:59:58） |
| 原文开源代码 | [已发布官方仓库](https://github.com/zichuanxu/tool-bottleneck-bench/tree/6f7fe7157c702c5c10937080f15bb3d48ce73d69)，MIT；未执行上游脚本 |
| 本地 Adapter | 无（`adapter: null`）；本地 key：`tool-bottleneck-bench` |
| 本地复现代码 | `src/auto_research/agent_research/tool_bottleneck_bench.py`；`scripts/run_tool_bottleneck_bench.py` |

## 原始论文总结

### 背景与主要改动

工具 Agent 的失败不只取决于模型：工具目录、可见菜单、工作流和返回记录编码会与 token/call/turn 上限交互。论文固定请求、事实和决策，分别操纵注册目录 R、可见菜单 V、认证工作流 W、返回状态 D。原协议有 36 个 family、12 个企业意图；routed menu 使用真值辅助缩窄，不能视为无需 oracle 的能力方案。

```mermaid
flowchart LR
    A[固定任务语义] --> B[R V W D 单因素变体]
    B --> C[固定 harness 预算]
    C --> D[真实工具执行和状态轨迹]
    D --> E[九义务 exact grader]
    E --> F[首个未满足义务与终止原因]
```

<!-- paper-figure:start -->
### 原论文关键图

[![原文 Figure 1：四种压力、固定预算与九义务评测](assets/paper-figure-01.png)](https://arxiv.org/html/2610.21098v1#S1.F1)

> Figure 1，官方仓库发布的原文 overview。图片来自[原论文](https://arxiv.org/html/2610.21098v1)，版权归原作者所有；仓库图文件固定至上表 revision。
<!-- paper-figure:end -->

### 核心公式

验证成功为 $Y=A\land S\land P\land Q\land E\land X\land G\land B\land C$，依次检查工具可用、选择、依赖有效程序、JSON 答案、精确引用、精确允许状态变化、无未请求变化、预算和 completion 完整性。失败标签为首个未满足义务，**不等于因果归因**。终止原因另按 completion cap、token/call budget、turn limit、不可行早停、错误结论、其他合同违反排序。

目录压力使用 ITT：$Y_R=A\cdot S$。工具未检索到、缺失响应或基础设施失败不能被删出计划分母。主论文容量对比按 family 聚类，Discovery 按 18 个 required-tool cluster 聚类；本地只复算后一类单配置记录。

### 论文离线与线上效果

原文 21 个模型/harness 配置、26,576 条 scored conditions。routed/fixed menu 从 8→128 时 VTS 分别下降 12.3/17.5 个百分点；截断重的六配置将 cap 提高 16 倍后，菜单惩罚从 -43.7 收窄至 -2.7 个百分点。91.5% exact-graded 失败终止于 harness limit。以上是论文整体结果，不是本地运行；未报告生产线上 A/B。

## 本地复现

### 数据协议与来源

仅使用固定 revision `6f7fe7157c702c5c10937080f15bb3d48ce73d69` 的一组 Gemini 3.6 Flash Discovery frozen plan 和对应官方 scored rows。小文件原样保存在 [frozen plan](validation/upstream/gemini-36-flash-primary-discovery.json) 与 [scored rows](validation/upstream/gemini-36-flash-primary-discovery.jsonl)；MIT 许可见 [LICENSE](validation/upstream/LICENSE)。

| 官方路径 | SHA256 |
| --- | --- |
| `results/prospective-plans/core-main/gemini-36-flash-primary-discovery.json` | `486ae15a5591645df4c6fffa9d47733f5225f45a1e19a197ce381a5b18074ac7` |
| `results/prospective-execution/core/gemini-36-flash-primary-discovery.jsonl` | `b5a57e002faed5f309d622cf82e5d32430599bce9c3e625776505b96c13eb6b0` |

导入时验证 condition 内容 hash、plan hash、每条件唯一性，以及 official `success` 与 A×S/status 的一致性。计划全部 216 条是分母；未知条件、重复条件或 hash 不匹配直接拒绝。缺行计失败，若整个 case 都缺失导致 required-tool cluster 无法确定，则保留 ITT 点估计而不编造聚类区间。

```bash
PYTHONPATH=src python scripts/run_tool_bottleneck_bench.py \
  --plan docs/agent-research/2610.21098-tool-bottleneck-bench/validation/upstream/gemini-36-flash-primary-discovery.json \
  --rows docs/agent-research/2610.21098-tool-bottleneck-bench/validation/upstream/gemini-36-flash-primary-discovery.jsonl \
  --resamples 10000 --seed 42 --output runs/tool-bottleneck-bench/official-discovery-cpu.json
```

### CPU 复算结果

| 子集 | 成功/计划 | ITT success | 95% required-tool cluster bootstrap |
| --- | ---: | ---: | --- |
| 全部六个目录/检索器单元 | 163/216 | 75.46% | 不将异质单元混成一个区间 |
| R=2048，flat | 7/36 | 19.44% | 5.56%–38.89% |
| R=2048，hierarchical | 28/36 | 77.78% | 58.33%–94.44% |

53 条 `capability_unavailable` 全保留，缺行 0。每单元 18 个 required-tool clusters、10,000 次重采样、统计种子 42。完整固定指标和真实执行命令见 [CPU 复算产物](metrics/official-discovery-cpu.json)。这是上游历史输出的重算，不是重新调用 Gemini，也不验证新模型能力；统计 seed 不是训练 seed。

### 代码映射、验证与边界

`compile_task` 独立实现 **仅 escalation_assessment 子集**，不是官方 36-family compiler：2/4/6 次读、可分支依赖、opaque IDs、R/V 等级和四种可逆编码。该子集只读，九义务中的 X/G 检查禁止任何状态变化；未实现论文有请求的可逆写操作。`Sandbox` 在实际 JSON 状态上执行 search/get 和空返回邻路工具，不执行任意 shell/网络。`grade_episode` 独立重放轨迹、核对 hash 链、允许任意合法分支顺序、逐项判定引用/答案/预算/completion。公开视图不包含 facts、decision、records 或隐藏程序。

单测中的无模型 public-handoff controller 只是 sandbox/合同诊断，不是论文 Agent。测试覆盖依赖逆序、伪造轨迹、未见引用、状态篡改、缺工具、completion 截断、预算失败、失踪/重复历史行和 lossless 编码。没有全量 retriever、所有企业意图、26,576 条原实验或 API 模型调用；没有 executable evolve operator。

成本决策：原实验公开估价约 USD 768.38，21 个托管配置及多组 repairs/cap sweeps 超出本轮零 API、零训练预算；**成本过高，不复现（审查 DONE）**，`full_experiment_status: not_reproduced_high_cost`。已完成的是有限公共接口和选定历史数据复算，不是原论文完整复现。
