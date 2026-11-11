# 2026-11-11：优先机构、低成本组件与双语学习资料

[English](../../en/research-audits/nov11-components/README.md)

本轮固定交付 **17 篇：16 个低成本 L1 组件、1 篇仅成本与机制审查的资料**。16 个组件均有 CPU 三 seed 诊断，其中 4 个 CUDA 路径另在真实单卡 A100 完成三 seed 验证。全部完整论文规模实验均明确**成本过高，不复现（审查 DONE）**，不把机制测试改称模型能力或 Evolve 效果。

**审查水位仍为 2026-11-09**。这是一次有界选题与交付，不是 11 月 10–11 日全窗口审查闭环。原始四轨两通道捕获有一条触顶查询，Meta 论文目录也有真实访问限制；详见[来源范围](source-coverage.json)。

## 本次固定清单

下表日期取原始 v1 的 UTC 时间；AlphaProof Code 只有官方发布日精度。相对上海时区 11 月 9 日水位，13 篇为后续首发、4 篇为历史或重叠补漏。发现日、公告日和 arXiv 编号月份不替代首发日期。

| 论文 / 资料 | 原始发布日期（UTC） | 本地交付 | 完整实验 |
| --- | --- | --- | --- |
| [ReproBridge](../../agent-research/2611.08452-reprobridge/README.md)（Google 合作） | 2026-11-05 18:45:36；补漏 | CPU：私有参考隔离、Student-t 预测区间、四件套与审计证据合同 | 不复现 |
| [LiSA](../../agent-research/2605.14454-lisa/README.md)（Google 合作） | 2026-05-14 06:47:35；补漏 | CPU：Beta 下界、平均链接聚类、局部冲突与记忆复用 | 不复现 |
| [MaxIM](../../post-training/2611.12825-maxim/README.md)（Google Research） | 2026-11-09 18:25:42 | CPU：归一化 PMI / 增量摘要奖励核 | 不复现 |
| [Excursion TD](../../post-training/2611.13275-excursion-td/README.md)（Google DeepMind 合作） | 2026-11-09 21:41:23 | CPU：有限 MDP 精确算子、excursion 权重与给定轨迹 target | 不复现 |
| [DRD-MOPD](../../post-training/2611.13249-drd-mopd/README.md) | 2026-11-09 21:21:41 | CPU + A100：全参数增量的梯度路由、逐分量独立 AdamW；无教师蒸馏 loss | 不复现 |
| [MCPO](../../post-training/2611.14015-mcpo/README.md) | 2026-11-10 12:51:43 | CPU：margin 不确定度、优势符号加权与逐响应归一 | 不复现 |
| [Stochastic Rounding](../../foundation-models/2611.13545-stochastic-rounding/README.md) | 2026-11-10 04:07:19 | CPU + A100：真实随机舍入数值与设备路径 | 不复现 |
| [WikiTrace](../../agent-research/2611.14320-wikitrace/README.md) | 2026-11-10 16:46:59 | CPU：来源链接记忆、显式下钻与只读证据 | 不复现 |
| [FGSE](../../agent-research/2611.14326-fgse/README.md) | 2026-11-10 16:52:25 | CPU：迁移增益、证伪风险、旧任务损伤的三重准入门控 | 不复现 |
| [PASE](../../agent-research/2611.14019-pase/README.md) | 2026-11-10 12:53:12 | CPU：skill-program 对与程序补丁事务，held-out validation 接受或回滚 | 不复现 |
| [RETRACE](../../agent-research/2611.14492-retrace/README.md) | 2026-11-10 18:49:47 | CPU：guard、typed 依赖 IR、参数来源与有序规则分派；无 planner | 不复现 |
| [ARE-Bench](../../agent-research/2611.14364-are-bench/README.md) | 2026-11-10 17:21:31 | CPU：任务上下文隔离、严格 checklist conjunction 与逐任务 macro 计分接口 | 不复现 |
| [RS-JEPA](../../multimodal-models/2611.14496-rs-jepa/README.md) | 2026-11-10 18:51:05 | CPU + A100：scanpath、GRL、四路邻域 KL；无完整 predictor | 不复现 |
| [ADIndex](../../foundation-models/2611.12956-adindex/README.md) | 2026-11-07 06:35:09；补漏 | CPU + A100：分组索引蒸馏、冻结骨干与因果稀疏选择 | 不复现 |
| [B3](../../foundation-models/2611.14387-b3/README.md) | 2026-11-10 17:40:24 | CPU：一拍滞后自校准 spawn gate 与 block-causal mask | 不复现 |
| [StepRefine](../../multimodal-models/2611.12901-steprefine/README.md) | 2026-10-14 07:52:29；补漏 | CPU：熵突增、软 embedding、KL 停止与预算记账 | 不复现 |
| [AlphaProof Code](../../agent-research/alphaproof-code/README.md)（Google DeepMind / Google） | 2026-11-10，日精度 | 仅官方报告、证明仓库与成本审查；无本地验证器、Adapter 或指标 | 不复现 |

逐项方法、原文核对位置、署名、上游代码状态、可执行代码范围与成本依据保留在独立论文页、[固定范围](task-scope.json)及三份审查记录：[优先机构](priority-review.json)、[后训练](post-training-review.json)、[Agent / JEPA](agent-review.json)。不宣称读完每篇全部正文；核对范围明确到方法、评测配置与成本相关段落。

## Google / Meta 与工业证据门槛

Google 优先交付 ReproBridge、LiSA、MaxIM、Excursion TD，以及仅资料收录的 AlphaProof Code。实际机构按原始署名核对；B3 一作为 Technion / Amazon Web Services，不能因模型、作者印象或标题猜为 Google。

Meta / NUS 的 [2611.13539：Exploiting Feature-invariant Scaling Laws for Efficient A/B Experimentation in Recommendation Systems](https://arxiv.org/html/2611.13539v1)已核正文 §5、§8–10，但**本轮拒绝收录/实现**。文中的 A/B 指候选架构/特征等离线对照，Criteo 4.2B 训练与末日 validation、MovieLens20M 及 LLM 微调未建立随机生产流量与量化线上收益。标题出现 A/B、摘要未写或背景提 online data 都不能替代正文生产证据门槛。本轮不把它换到基础模型/评测接口绕过标准，不新增经典例外。

该拒绝独立进入账本，不计入 17 篇交付。原配置成本仅作事实说明，不被包装成“接受后因高成本延期”。e-means、GSLM2 为已知收录，不重复计新论文；官方目录新增的遥感应用与 OSS / 治理研究另按实际核对范围分流。

## 验证证据与边界

- [预检](preflight.json)：固定 16 组件、seed 42/43/44，单次最多 180 秒；无 API、预训练模型调用、模型/数据下载或完整实验。
- [冻结源码](frozen-sources.json)：保存实际执行 commit 与源码 SHA-256；不是用提交后的名字倒填运行证据。
- [CPU 原始结果](raw-cpu.json)：16 组件 × 3 seed。[CUDA 原始结果](raw-cuda.json)：4 组件 × 3 seed。
- 真实 A100 回执：[DRD-MOPD](../../gpu-validations/drd-mopd-a100-20261111.json)、[Stochastic Rounding](../../gpu-validations/stochastic-rounding-a100-20261111.json)、[RS-JEPA](../../gpu-validations/rs-jepa-a100-20261111.json)、[ADIndex](../../gpu-validations/adindex-a100-20261111.json)。公共输入均为源码定义的固定小型张量/有限 MDP/合同夹具，无真实 checkpoint。

所有结果均为 `diagnostic_only: true` / `evaluation_tier: l1_mechanism`，不提供原论文准确率、吞吐或线上 uplift 的复现声明。相同确定性合同的三 seed 不等于三份独立能力样本；测试参考、成功阈值和答案不暴露给 actor。注册 local operator 不代表已接入统一 Evolve；本轮 `promotion_eligible` 与 `evolve_integrated` 均为 false。

每篇补充四层学习问答与校对英文版，并更新对应专题精读；它们解释论文与本地边界，不升级证据等级。论文原图、来源与截取方式保留在论文页及图清单中。

## 来源范围与后续线索

本轮复用 11 月 11 日实际四轨两通道 CI 捕获：请求窗口 10 月 28 日至 11 月 11 日，实际含 10 月 27 日重叠。**有文件不等于全部候选都已方法审查**。Foundation late-index 的 `LLM` 查询在 2,000 条触顶，另外七路捕获取尽其已配置查询；补充后训练 Atom 只返回关键词查询 111 条中的前 100 条。

官方来源只核有限页面：Google 首/末页及相关详情、DeepMind publication landing / AlphaProof 项目与公告；Meta 主论文目录返回 unavailable 内容，主页不变不能推出全站零新增。Google 462 与此前 450 的目录计数差不是 12 篇新论文。真实 URL、内容 hash、实际来源失败与局限见 [source-coverage.json](source-coverage.json)。

仍只作为有限、未完成方法审查的线索：Bootstrapped OPD（2611.13680）、Coverage Collapse / Reference Resets（2611.14467）、Action-Sequence Alignment OPD（2611.13135）。不自动进入实现队列，不把未读方法写成高成本 DONE。补齐触顶查询及窗口级逐项审查是未来推进水位的独立工作；本轮不顺带承诺完成。

## 可复核入口

```bash
PYTHONPATH=src python scripts/record_nov11_components.py --check
PYTHONPATH=src python scripts/audit_paper_coverage.py --strict
```

记录脚本在验证原始运行、冻结源码、叶子指标和 A100 回执一致后才追加账本；重复执行默认拒绝覆盖，`--check` 只读核验。完整实验不重试、不进入自动训练/实现/Evolve 队列；仅用户看过成本后明确重开。
