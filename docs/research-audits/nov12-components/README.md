# 2026-11-12：同公告补漏、Google 历史补漏与八项机制核

[English](../../en/research-audits/nov12-components/README.md)

本轮交付 **8 个低成本 L1 组件**：6 篇来自仍为 **11 月 11 日**的同一公告，2 篇是 Google 官网触发的历史补漏，**不是 8 篇今天新首发**。CPU 完成 8 组件×3 seed，真实单卡 A100 完成 3 组件×3 seed。7 篇完整系统/实验明确**成本过高，不复现（审查 DONE）**；APMD 是理论论文，大型实证不适用，不虚构高成本配置。

审查水位保持 **2026-11-09**。这次有界交付不等于 11 月 10–12 日全窗口闭环，也不把来源列表中的 956 个身份变成新论文数或实现队列。

## 固定交付与精确保真范围

| 论文 / 来源 | 本地实际实现 | 没有实现的完整链路 |
| --- | --- | --- |
| [Agent Gym](../../agent-research/2608.15591-agent-gym/README.md)，Google，2026-08-16 首发 | CPU：八种确定性条件、scope/priority 互斥、合并 continuation/patch 后按 3→2→1 改真实 JSON；target/collateral 与显式 SME 批准合同 | 真实 acting agent、LLM 规则发现/调查、语义纠错、自动规则晋升；批准参数不认证真人身份 |
| [BATS](../../agent-research/2511.17006-bats/README.md)，Google 合作，2025-11-21 首发 | CPU：逐工具预算、统一 token/tool 费用、外部 SUCCESS/CONTINUE/PIVOT 状态转移；换路不重置用量、任一工具耗尽即停 | 语义规划/验证/摘要、网页工具和答案 judge；外部 SUCCESS 不是 gold 正确率 |
| [BOPD](../../post-training/2611.13680-bopd/README.md)，同公告补漏 | CPU + A100：同前缀 full-vocabulary FKL、逐轨迹等权；冻结中间教师、从初始参数/buffer 精确重置新学生及新 optimizer | Stage I/II LLM rollout、reference prompt、原文 clipping、完整 OPD trainer；作者链接为空仓库，不写成训练源码已发布 |
| [APMD / reference reset](../../post-training/2611.14467-apmd-reference-reset/README.md)，同公告补漏 | CPU：有限分布的精确 mirror step、逐轮 reference reset、Kimi/Rebel 平方损失恒等式 | LLM/PPO 采样内循环、全部定理证明、任意 Transformer 收敛保证；大型实证状态为 `not_applicable_theory_only` |
| [LCS reference OPD](../../post-training/2611.13135-lcs-reference-opd/README.md)，同公告补漏 | CPU：精确 LCS 动态规划、两种明确归一化、同任务成功轨迹整序列去重与独立 argmax、失败样本归约 | 真实教师 reference 收集、学生交互轨迹、OPD loss/trainer/环境；reference 只给训练教师，不给学生 |
| [REAL Loss](../../foundation-models/2611.14399-real-loss/README.md)，同公告补漏 | CPU + A100：target 采样轨迹上的 q/p 截断路径权重、最后一步边缘化、固定 gamma 归一与 CE 混合；真实梯度和反例检查 | 大 target、drafter 完整训练、轨迹采样来源认证、投机解码 serving/吞吐评测 |
| [C²-Routing](../../multimodal-models/2611.14469-c2-routing/README.md)，同公告补漏 | CPU：四状态联合正确性风险 H−B、validation dataset-macro 成本比、不可变策略的接受/原图回退 | 图文特征、裁剪定位、训练后的选择/风险头、真实 VQA；推理不读取答案或在 test 拟合阈值 |
| [OnlyAct](../../multimodal-models/2611.14420-onlyact/README.md)，同公告补漏 | CPU + A100：外部两帧联合 token 的池化/冻结投影、完整 3N 候选双向 InfoNCE 与同视频非重叠 hard-negative 合同 | V-JEPA 2、LoRA、场景交换/RAFT、视频世界模型或真实动作解耦能力 |

每篇独立页均保存首发与审查版本、原始署名、上游代码状态、公式、原图、负控、中文/校对英文和四层学习问答。方法比较与专题精读也按真实机制更新。日期以原始 v1 为准：Google 官网旧称 CATS 的条目对应 BATS 的 2025 年首发；Agent Gym 当前审查 v3 不会把八月首发改成十一月新文。

逐项定义与成本依据见[固定范围](task-scope.json)、[逐篇原始来源回执](primary-source-receipts.json)，以及 [Agent](agent-review.json)、[后训练](post-training-review.json)、[基础/多模态](foundation-review.json)审查。原文核对范围明确到作者栏、定义机制与配置段落，不声称每篇所有文字都已核验。

## 真实执行证据：只验收 L1，不提升为模型能力

- [预检](preflight.json)：seed 42/43/44，每次最多 180 秒；无模型/评测数据下载、API 调用或预训练模型调用。
- [冻结源码与证明](frozen-sources.json)、[CPU 原始执行](raw-cpu.json)、[CUDA 原始执行](raw-cuda.json)绑定同一实际源码。CPU 8×3；A100 3×3。
- A100 回执：[BOPD](../../gpu-validations/bopd-a100-20261112.json)、[REAL Loss](../../gpu-validations/real-loss-a100-20261112.json)、[OnlyAct](../../gpu-validations/onlyact-a100-20261112.json)。

本轮 CUDA 组件核执行合计约 **1.37 秒**；这是小张量/机制 runner 的计时，不含调研、传输、环境启动，也不是原论文训练耗时。输入是显式小型张量、有限策略与合同夹具，无真实 checkpoint。测试会拒绝改设备、丢 seed、换源码或把诊断晋级为正式对照。

全部保留 `diagnostic_only=true`、`evaluation_tier=l1_mechanism`、`formal_comparison=false`。合成合同的多 seed 不等于独立模型能力样本，注册 local operator 不代表统一 Evolve 可执行集成；本轮 `promotion_eligible=false`、`evolve_integrated=false`。

## 完整系统的成本与理论状态

7 篇完整系统/实验均按公开配置或未解的实质成本不确定性标注不复现，不下载大资源、不做成本探针、不自动重试。例子包括 BOPD 的多 GPU 两阶段长 rollout、LCS 原文约 4500 A100 GPU-hours、REAL 的 140K steps 多损失/serving 矩阵、OnlyAct 的视频预处理和多个世界模型实验；不能用本地毫秒级梯度核代替这些链路。

**APMD 单独处理**：它是理论工作，有限策略数值核已实现，但没有原文大型实证矩阵可照跑，故 `full_experiment_status=not_applicable_theory_only`，不是高成本延期，也不是本地证明了全部定理。

## 工业来源异常：不确认，不臆改，也不指控

[SAM-D2Q 的固定原文记录](industrial-source-exception.json)保留所报 AliExpress Search 的量化 A/B 与对照说明，但同时发现：训练信号来自 **2025 年 8–11 月**，所报 A/B 在 **2025 年 6 月 8–28 日**，正文未解释这两个时期对应的模型版本。

这属于**无法确认的版本/时间对应**，不是对实验造假的指控。不能擅自改年份或假定线上版本就是后期训练系统。本轮作为非阻塞协议异常归档：不 catalog、不实现、不计入 8 篇，不提升为已确认符合门槛的线上证据；作者说明或原文修订可重开。

## 来源覆盖与仍未闭环的范围

[公告索引](announcement-index.json)保存八个 arXiv 分类 `new` 页面，当前仍为 11 月 11 日公告；含跨分类、替换稿的去重来源身份共 **956**。其中 `new` 标签表示相对仓库记录未匹配，**不表示 903 篇合格新文、未完成交付或自动任务**。未选身份没有据此完成方法审查。

[来源差集](source-coverage.json)只比较 Google 首/末页、Meta curated home 与 DeepMind landing 等有界页面；可见链接无新增不等于机构全站无新论文。Meta 主目录返回 unavailable；替代 results 页经网页渲染可读，但直接保存超时、历史年份混排，不宣称按日期穷尽。GSLM2 已知收录，不重复计新模型。审查水位、覆盖限制和实现证据彼此独立，水位仍为 11 月 9 日。

## 普通 clone 与维护者来源重查

安装仓库依赖后，普通 fresh clone 可只核验**已提交**的 scope/coverage/hash 链、冻结源码、实际运行和 GPU 回执，不需要联网或本地原文缓存：

```bash
PYTHONPATH=src python scripts/record_nov12_components.py --check
PYTHONPATH=src python -m pytest -q tests/test_nov12_evidence.py
```

这不声称重新读取了网页/PDF 的原始字节。若维护者保留本轮 `.cache/nov12-components/` 原始捕获，可额外执行：

```bash
PYTHONPATH=src python scripts/record_nov12_components.py --check --recheck-source-captures
```

首次追加账本必须核对原始捕获，后续默认检查保持可移植；显式来源重查缺文件或 hash 不符会失败，不静默转为“已重查”。两种检查都不会推进水位，也不会重跑完整论文实验。
