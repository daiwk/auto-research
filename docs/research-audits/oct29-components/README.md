# 10月29日：新公告、Google/Meta来源与学习资料

本轮固定交付 **8个低成本L1组件、1篇高成本资料**，另更新已有EmbeddingGemma2正式论文与Meta RPL官方代码。不是9个刚刚首发的新模型，也不是完整论文能力复现。

## 范围与成本终态

| 条目 | 来源类型 | 本地交付 | 完整实验 |
| --- | --- | --- | --- |
| [Google Sleep](../../foundation-models/2606.03979-sleep-lti/README.md) · P0 | 10/27官网介绍触发历史补漏，arXiv v1在6月；论文还声明2025年更早版本 | CPU：LTI token编辑/外部语义混合奖励 | 高成本，不复现，审查DONE |
| [DeepMind HOPE](../../foundation-models/2607.21366-hope-hilbert/README.md) · P0 | 10/27官方源码发布触发7月论文补漏；不是Sleep的同名Hope架构 | CPU：Hilbert/ReLU核、剪枝率、BN均值补偿与单步恢复 | 高成本，不复现，审查DONE |
| [ResCom](../../foundation-models/2610.35955-rescom/README.md) | 近期公告，v1提交10/25，早于上次capture | CUDA：中心化流式矩、ridge白化/SVD和截距 | 高成本，不复现，审查DONE |
| [Select-TTT](../../foundation-models/2610.36794-select-ttt/README.md) | 10/27 v1 | CUDA：query-CE选块、clip后不重归一的写入倍率与真实fast-weight更新 | 高成本，不复现，审查DONE |
| [GUI-JEPA](../../foundation-models/2610.36877-gui-jepa/README.md) | 10/27 v1 | CUDA：真实三层候选条件predictor、结构head与listwise loss | 高成本，不复现，审查DONE |
| [KL-MOPD](../../recommendation-components/2610.36973-kl-mopd/README.md) | 10/27 v1；正文5天真实A/B通过工业门槛 | CUDA：一次初始校准、固定位置权重、student-to-teacher KL | 高成本，不复现，审查DONE |
| [DiscernMem](../../agent-research/2610.36652-discernmem/README.md) | 10/27 v1 | CPU：配对重放测量、双参照修复门槛、版本证据重置 | 高成本，不复现，审查DONE |
| [RuHarness](../../agent-research/2610.36826-ruharness/README.md) | 10/27 v1 | CPU：六格联合后验、保守准则frontier及validation准入 | 高成本，不复现，审查DONE |
| [PailitaoMMSearch2.0](../../recommendation-components/2610.36958-pailitao-mmsearch2/README.md) | 10/27 v1；正文14天A/B及全流量部署证据 | 资料收录，无占位模型/算子/指标 | 高成本，不复现，审查DONE |

固定9篇中，6篇arXiv首发晚于上次capture；ResCom是更早提交的近期公告，另2篇为历史官方来源触发。另有Guided-RLVR在审查记录中明确高成本不复现，保留公式歧义，不虚构可用控制器。

## 实际执行与边界

冻结提交 `4fd3d0c5845f7f88b9a68333c33c9035f47b3983`，12个源码/合同文件由可携带Git对象证明绑定。CPU执行8组件×3seed，约3.30秒；真实 **NVIDIA A100-SXM4-80GB** 执行4 CUDA组件×3seed，约1.52秒，均不含网络/启动开销。无checkpoint、公开能力数据集、LLM/API调用或完整训练。

每个seed必须通过固定59项CPU机制检查；CUDA子集31项。结果为数值公式、梯度、状态或统计合同，不是GUI成功率、遗忘率、ImageNet准确率、推荐收入提升或统一Evolve证据。

- [固定执行规格](execution-spec.json)、[CPU原始结果](raw-cpu.json)、[CUDA原始结果](raw-cuda.json)
- [冻结源码证明](frozen-sources.json)、[逐篇范围与成本](task-scope.json)
- 4个独立GPU回执：[ResCom](../../gpu-validations/rescom-a100-20261029.json)、[Select-TTT](../../gpu-validations/select-ttt-a100-20261029.json)、[GUI-JEPA](../../gpu-validations/gui-jepa-a100-20261029.json)、[KL-MOPD](../../gpu-validations/kl-mopd-a100-20261029.json)

启动时曾有一次命令参数提交号与真实证明不符，运行器在导入torch/执行组件前拒绝；修正为实际冻结提交后重跑，不产生伪造GPU产物。交叉审查还修复KL极大有限差距归一化溢出、RuHarness非原生bool序列化、ResCom非对称矩输入及HOPE极端均值消减；没有放宽检查或替换核心机制。

## 来源覆盖，不混淆首发/版本/源码

[来源覆盖](source-coverage.json)保留8个最新公告与8个recent页面回执。实际最新公告仍为**10月28日**，并非抓取当天29日；recent补取27日与重叠列表。分类条目包含交叉收录和旧文替换，不能当作新论文数量；未宣称全部召回身份逐篇读完全文。

[Google/Meta/DeepMind当前目录快照](official-source-inventory.json)44/44页成功：Google435、Meta144、DeepMind266个URL。Google历史基线由旧快照及后续差集重建，发现7个未见URL、2个旧URL当前消失，净增5不是5篇新论文。仅摘要分流、日期未确认、原环境不可用的条目单列，不标为完成全文审查。Meta分页是有界6页，不承诺机构或全网穷尽。

新增官方源码线索中，Meta sixthview benchmark尚无核实论文身份，仅保留发布记录；Genie4/Gemini4 Carbon公告未确认规范论文/公开可复现模型，不编造论文。已有[RPL](../../agent-research/2610.24854-rpl/README.md)只补官方仓库和许可；[EmbeddingGemma2](../../multimodal-models/embeddinggemma2/README.md)只补同模型正式技术论文与原图，不重复建key、不改旧GPU结果。

全局审查水位仍为**2026-10-15**。本批限定交付完成，不等于10/16–29所有来源、所有论文全文审查闭环；高成本已作终态决策，不进入自动重试或实现队列。

## 学习资料

新增9篇各4层问答（基础、机制、对比、实现），并给旧EmbeddingGemma2/RPL各补1个问题；合计**38个逐篇新问题**。同步9个专题精读的机制对照、取舍、跨论文自测和来源指纹；自动生成最近新增、主题入口及全部问答。不把教学数值示例当作论文实测。

[学习入口](../../learning/index.md) · [最近新增](../../learning/recent.md) · [专题精读](../../learning/deep-dives/index.md)

## 交付检查

- 本地完整测试首轮6267项通过、2项跳过；3项元数据衔接失败已修复：高成本资料的终态字段/理由，以及RPL官方代码公开后的旧断言。相关69项回归全部通过，并增加共同篡改scope/账本理由仍不能伪造验收的负控；未降低算法或证据检查。
- `compileall`、Ruff、最小wheel安装、文档严格构建、目录/学习资料生成、论文覆盖审计、GPU证据与平台合同通过；1001个指标文件无需迁移。原始执行与冻结源码未被文档修正重写。
- PR中的完整CI结果以实际检查状态为准；本地分层验收不冒称云端CI已完成。
