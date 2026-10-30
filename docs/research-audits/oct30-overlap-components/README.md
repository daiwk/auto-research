# 10月30日重叠补漏：来源增量为零，新增10个低成本组件

这不是一天内新首发10篇论文。实际可见 arXiv 最新公告仍为 **2026-10-28**，八类 new 列表与上次身份集合相同，共享 recent 日期也没有新增身份。Google / Meta / DeepMind 的有界官方目录亦无差集；本轮是对已有近期公告和 Google 历史线索的补审/补实现，不宣称全窗口全文审完。

## 固定范围

| 优先级 | 论文 | 本地低成本交付 | 未执行的完整实验 |
| --- | --- | --- | --- |
| P0 · Google合作 | [CONCUR](../../post-training/2610.36437-concur/README.md) | CPU：奖励 gate、保序/ceiling投影、累计earned-trust与整batch白化 | 32GPU/run、多模型多任务RL，成本过高，不复现（审查 DONE） |
| P0 · DeepMind合作 | [MERLIN](../../foundation-models/2610.37645-merlin/README.md) | CUDA：原始段矩、query方向均值/方差、双softmax门混合与因果可见段 | 大规模预训/中训与长上下文矩阵，不复现（审查 DONE） |
| P0 · Google历史补漏 | [CROP](../../agent-research/2604.14214-crop/README.md) | CPU：外部文本梯度回调与成本正则prompt选择，隔离validation | Gemini/7B多轮优化和评估API矩阵，不复现（审查 DONE） |
| P0 · 工业A/B | [PinGER](../../recommendation-components/2610.33435-pinger/README.md) | CUDA：非对称mask、单层前缀惩罚、所有前缀DPO加NTP锚 | 私有tokenizer/推荐器、十亿商品库和服务/A/B，不复现（审查 DONE） |
| P0 · 工业A/B | [Pinterest RLBP](../../recommendation-components/2610.33248-pinterest-rlbp/README.md) | CUDA：9动作、双头TD、奖励/融合/top-K与IPS | 私有campaign模型、拍卖/PID部署和付费流量，不复现（审查 DONE） |
| P1 | [FoldBias](../../foundation-models/2610.36520-fold-bias/README.md) | CUDA：约束ridge方向、实际BF16舍入后value重拟合 | 大模型KV/长上下文/serving对照，不复现（审查 DONE） |
| P1 | [SWIM](../../foundation-models/2610.36662-swim/README.md) | CUDA：真实门控逆动力学、cyclic对比损失、冻结sqrt(g)几何 | 完整JEPA视觉world model与CEM规划，不复现（审查 DONE） |
| P1 | [MPOPD](../../post-training/2610.36477-mpopd/README.md) | CUDA：几何proposal目标、滞后一token的单步权重与两次反向KL | 真实LM rollout/参数重置/长链蒸馏，不复现（审查 DONE） |
| P1 | [EMMA](../../agent-research/2610.35966-emma/README.md) | CPU：记忆ownership、单编辑/继承/容量守卫与overflow拼接 | 语义安全服务、LLM反思与AppWorld等任务，不复现（审查 DONE） |
| P1 | [EvalAlloc](../../agent-research/2610.37276-evalalloc/README.md) | CPU：Beta获取、固定外部响应模型MAP、配对轮校正和缓存预算 | MIRT warmup/两折refit与完整LLM搜索控制器，不复现（审查 DONE） |

CROP 首发于4月，是历史补漏；其余9篇是10/23–27首发的近期重叠补漏。MPOPD 阅读固定v2，v1首次日期另存，不重复计为两篇。Google合作不改写一作机构：CONCUR一作保留CMU，MERLIN一作保留Princeton。

## 实际执行与证据

科学执行冻结提交为 `af9b9245aa85b4cbeb3da27ca701cc01cb94da86`。15个执行源码/规格/成本范围文件由可携带 Git 对象证明绑定；只同步约88KB公开源码归档，没有传整个工作区、数据、密钥或checkpoint。

- CPU执行10组件×3seed，实测约 **3.43秒**。
- 真实 **NVIDIA A100-SXM4-80GB** 执行6 CUDA组件×3seed，实测约 **1.69秒**。
- 上述仅为运行器内部组件时间，不包括启动、传输、研究与测试。没有模型下载、LLM/API调用或完整训练。
- [固定执行规格](execution-spec.json) · [CPU原始结果](raw-cpu.json) · [CUDA原始结果](raw-cuda.json) · [冻结源码证明](frozen-sources.json) · [逐篇范围](task-scope.json)
- 每篇有自己的 `metrics/component-{cpu,cuda}-seeds42-44.json`；六份独立GPU回执（[MERLIN](../../gpu-validations/merlin-a100-20261030.json)、[FoldBias](../../gpu-validations/fold-bias-a100-20261030.json)、[SWIM](../../gpu-validations/swim-a100-20261030.json)、[MPOPD](../../gpu-validations/mpopd-a100-20261030.json)、[PinGER](../../gpu-validations/pinger-a100-20261030.json)、[RLBP](../../gpu-validations/pinterest-rlbp-a100-20261030.json)）由校验器绑定，不把一张批量总表冒称逐篇能力指标。

这些是公式、梯度、数值和状态合同：不是推荐业务收益、Agent成功率、LLM推理准确率或Evolve改善证据。完整高成本实验为终态审查DONE，不进自动重试或实现队列；低成本组件验收与完整复现状态分别记账。

## 来源差集与边界

[来源覆盖](source-coverage.json)保存16个完整列表抓取/解析回执、分类身份、共享recent日期差集。分类交叉收录与replacement不能当作新论文数量。未读的宽召回身份不冒称已逐篇全文审过。

[官方目录复核](official-directory-check.json)对照已提交的Oct29完整记录基线，44/44页成功，Google435、Meta144、DeepMind266个URL的解析记录相同；只保存本轮回执与已提交基线引用，不再次复制整套相同记录。[优先机构复核](priority-review.json)另记官网、博客、公开新建仓库与有界repo活动；push时间不是源码首发证据，Meta六页也不是机构穷尽保证。

本次没有声称发现10/29或10/30公告，没有把源码活动或旧文补漏包装成新首发。**全局审查水位仍为2026-10-15**；这10项限定交付不等于10/16–30所有来源全部闭环。

## 学习资料与质量检查

新增10篇各4层中文问答，共 **40个逐篇问题**；基础/机制/对比/实现均有具体教学示例，并引用真实章节。同步9个既有专题的机制对照、分析和跨论文自测，保留旧ID与更新历史，绑定实际阅读的README指纹。

[最近学习卡片](../../learning/recent.md) · [全部问答](../../learning/all.md) · [专题精读](../../learning/deep-dives/index.md)

交叉审查修正了极大有限输入的派生NaN/Inf、CONCUR可变历史、MERLIN逐组梯度、SWIM固定动作chunk的文档公式，以及RLBP未知数值预处理的外置接口。新增122项独立机制测试及40项来源/证据合同测试通过。全库回归发现的CROP原图版权说明缺项已补齐，受影响文档、学习卡片和来源合同已复验，严格文档构建与基础wheel安装检查通过；不把透明边界或测试通过提升为完整论文能力。
