# Jev 开放实现：选型与集成路线图

本页不是“谁最像官方 Jev”的排行榜，而是帮助用户判断不同开源项目究竟解决了什么问题。社区项目复现的是 **System One 的接口形态或决策行为**；TypeSafe 尚未公开 Jev 的权重、训练数据、RLCD 算法或内部网络，因此没有任何项目应被写成官方等价复现。

完整的 48 项社区资料见[社区实现全量快照](implementation-tracker.md)。本页只保留值得实际选型和后续接入统一评测的主干。

## 官方边界 {#official-jev}

| 实现 | 可验证内容 | 未公开内容 | 本仓库状态 |
|---|---|---|---|
| [TypeSafe Jev](https://docs.typesafe.ai/introduction) | Choice、Score、Noul 协议；概率与 confidence；托管 API | 权重、训练集、模型结构、RLCD loss 与训练配方 | typed contract 与可选 HTTPS provider 已接入；不把本地基线称为 Jev 复现 |

## 五条技术路线

| 路线 | 核心做法 | 适合验证什么 | 不应误解为 |
|---|---|---|---|
| 直接 logits / 并行约束解码 | 复用现有语言模型，一次 prefill 后直接读取候选 token 或约束分支的 logits | 延迟、接口、候选规模和 serving 工程 | 训练出了新的 Jev 类模型 |
| 训练决策头或微调模型 | 在公开基座上训练 Choice、Score、Noul 或类型化 schema head | 校准、泛化、训练目标和 checkpoint 对照 | 复现了未公开的 RLCD |
| 扩散语言模型 | 利用 DiffusionGemma 等并行生成/判别特性构造一步决策 | 并行推理与非自回归决策 | 已具备 Jev 的校准能力 |
| 先验分类/抽取模型 | 动态标签分类、schema extraction 或专用判别器 | 方法谱系与强非生成式基线 | Jev 社区复现 |
| 评测与行为研究 | 比较准确率、Brier、ECE、延迟、OOD 与接口行为 | 统一验证和识别伪复现 | 可直接部署的模型 |

## P0：优先接入统一评测的公开 checkpoint

| 项目 | 公开资产 | 定义性机制 | 主要限制 | 建议 |
|---|---|---|---|---|
| [Bespoke Nimble](https://github.com/bespokelabsai/nimble) | 9B checkpoint、训练数据与配方；支持 MLX/CUDA | 对 flat typed schema 直接读取 enum/boolean logits，不生成 JSON | 作者明确不保证概率已校准；Score/嵌套 schema 不完整 | **P0 checkpoint 对照**：最适合先验证真实模型、延迟和 Choice/Noul |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | Qwen3-0.6B 权重、数据、训练与服务代码 | set attention 决策头；Choice、Boolean、Score；proper loss | 小模型与社区数据，不能代表官方产品质量 | **P0 多原语对照**：最适合扩展当前 Choice-only 公共协议 |
| [Laya](https://github.com/NandhaKishorM/laya) | checkpoint、demo 与微调 notebook | 类型化决策和温度校准 | 零样本接近随机；微调模型有领域依赖；高候选数受 token budget 限制 | **P0 校准对照**：验证 ECE/Brier 与 validation-only 温度拟合 |

只有把公开 revision 固定、接入相同数据切分、实际执行并产出指标，才算“已接入”。当前三项均为**已收录、待接入**，不能在看板上作为本仓库实验结果展示。

## P1：工程与服务基线

| 项目 | 路线 | 可复用点 | 定位 |
|---|---|---|---|
| [SemIf](https://github.com/TheoLeeCJ/SemIf)（原 OpenJev） | 直接 option logits | shared-state prefill、固定 revision/fixture、延迟对照 | 首选并行约束解码基线 |
| [Reflex](https://github.com/kshetrajna12/reflex) | logits / typed decision | Jev 风格接口和本地执行 | API/contract 互操作对照 |
| [openjev-sglang](https://github.com/ekzhang/openjev-sglang) | SGLang serving | 高吞吐并行约束解码 | GPU serving 工程基线 |
| [LitJev](https://github.com/zhengxuyu/litjev) / [snapjudge](https://github.com/Micha0827/snapjudge) | 轻量解码封装 | 最小可运行实现与接口比较 | 教学/烟测，不作为能力上限 |
| [jeff](https://github.com/logan-markewich/jeff) | 训练式 schema head | 基于 GLiFormer/GLiNER 的结构化抽取路线 | 与动态候选 scorer 的相邻基线 |

这些项目适合验证实现复杂度、吞吐和契约兼容性。若路径依赖 CUDA，必须按仓库 GPU gate 在真实 A100/A30 上执行并提交去机器化 receipt，才能声明集成完成。

## P1：评测资产

| 项目 | 作用 | 本仓库计划 |
|---|---|---|
| [jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks) | 汇总 Jev 风格任务与实现比较 | 审核数据许可和 gold 隔离后映射到统一协议 |
| [jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration) | OOD 与概率校准 | 扩展 coverage-risk、ECE/Brier 和分布外候选 |
| [jev-behavior-study](https://github.com/RINNECODER/jev-behavior-study) | 托管 API 行为研究 | 仅作为黑盒协议证据；不反推官方网络 |
| [typesafe-ai-benchmark](https://github.com/iammrduncan/typesafe-ai-benchmark) | TypeSafe API 对照 | 用户显式提供 API key 时运行固定公开样本 |

## 按目标选实现

| 目标 | 首选 | 次选 | 原因 |
|---|---|---|---|
| 公开 checkpoint 能力对照 | Bespoke Nimble | NanoJev、Laya | 有权重、数据或训练配方，可实际复验 |
| Choice / Score / Noul 全协议 | NanoJev | Laya | 覆盖多种决策原语和训练目标 |
| 低延迟工程验证 | SemIf | openjev-sglang | 不依赖自回归 JSON，可测 prefill/候选扩展成本 |
| 校准与 OOD | Laya + jev-ood-calibration | NanoJev | 可以验证温度校准、proper metrics 与 coverage-risk |
| Apple Silicon 本地试用 | Bespoke Nimble MLX | PocketJev、jevmlx | 前者有训练资产，后两者更偏运行时封装 |
| 扩散路线研究 | DiffusionGemma / vLLM 路线 | LocalJev、open-jev | 应单列实验，不与训练式 head 混排行 |

## 接入门槛

一个外部项目进入本仓库统一看板前必须同时满足：

1. 固定公开模型、数据和代码 revision，并记录许可证；
2. 明确属于训练模型、推理解码还是概念诊断，不能用同一标签混淆；
3. 适配 `Choice`、`Score` 或 `Noul` 中至少一种 typed contract；
4. validation 选择参数，test 只做最终报告，并输出 accuracy、NLL、Brier、ECE 和成本/延迟；
5. 不允许模型读取 gold answer/plan；只验证接口的 fixture 必须标成 diagnostic；
6. CUDA 路径在真实 A100/A30 上通过，并提交净化后的 GPU evidence。

因此，tracker 中出现不等于本仓库已经实现；“已收录”“适配中”“已执行评测”将在后续看板中保持不同状态。
