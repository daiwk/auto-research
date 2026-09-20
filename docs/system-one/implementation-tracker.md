# Jev 社区实现全量快照

本页整理 [Jev Reproductions Tracker](https://huggingface.co/spaces/multimodalart/jev-reproductions-tracker) 在 **2026-09-19** 的公开条目，便于查重和后续选型。该 tracker 为社区维护，与 TypeSafe 无隶属关系；条目名称中的 Jev、RLCD 或 System One 不代表项目获得了官方权重、数据或训练算法。

## 快照统计

| 类别 | 数量 | 含义 |
|---|---:|---|
| 直接 logits / 并行约束解码 | 17 | 使用现有模型和推理技巧，通常没有训练新模型 |
| 扩散语言模型路线 | 4 | 基于 DiffusionGemma 等非自回归模型探索一步决策 |
| 训练模型 / 决策头 | 16 | 提供或声称训练 checkpoint、head、LoRA 或 fine-tune；其中 1 项尚未发布 |
| 先验工作 | 2 | 更早的动态分类、抽取或专用判别模型 |
| 评测、行为研究与索引 | 9 | benchmark、黑盒研究、解释材料和 awesome list |
| **合计** | **48** | 只有通过本仓库执行门槛后才算已集成 |

## 直接 logits 与并行约束解码（17） {#decode-routes}

| 项目 | 主要形态 | 备注 |
|---|---|---|
| [Qwen-2.5-1B-RLCD](https://huggingface.co/harshatheg/Qwen-2.5-1B-RLCD) | Qwen checkpoint + [parallel constrained decoding demo](https://huggingface.co/spaces/drinkmoonshine/parallel-constrained-decoding) | 需区分 checkpoint 声称与可复核训练证据 |
| [openjev-sglang](https://github.com/ekzhang/openjev-sglang) | SGLang 并行约束解码 | GPU serving 工程路线 |
| [SemIf](https://github.com/TheoLeeCJ/SemIf) | 直接 option logits | 原 OpenJev；canonical repo 已更名 |
| [PocketJev](https://github.com/NullPo-jp/PocketJev) | 轻量本地封装 | 偏接口/推理实现 |
| [jevmlx](https://github.com/bnsd55/jevmlx) | MLX 本地推理 | Apple Silicon 路线 |
| [jev-on-a-laptop](https://github.com/rorshopping/jev-on-a-laptop) | 笔记本本地运行 | 工程 demo |
| [jevfire](https://github.com/kikoncuo/jevfire) | Jev 风格推理封装 | 需独立审核评测边界 |
| [LFM2.5-RLCD 350M](https://huggingface.co/notnotsamuel/LFM2.5-350M-RLCD) / [2.6B](https://huggingface.co/monotykamary/LFM2.5-2.6B-RLCD) | LFM checkpoint | 需确认训练资产和 typed contract |
| [parallelConstraintDecoding](https://github.com/stephanj/parallelConstraintDecoding) | 并行约束解码 | 通用推理技术 |
| [system-one](https://github.com/snellingio/system-one) | typed decision wrapper | 社区接口实现 |
| [open-jev](https://github.com/daseinlabs/open-jev) | logits / wrapper | 社区独立实现 |
| [openvons](https://github.com/genai-craft/openvons) | open System One interface | 社区独立实现 |
| [openjev](https://github.com/zhihz/openjev) | Jev 风格推理 | 社区独立实现 |
| [system-one](https://github.com/sgoedecke/system-one) | 最小 System One demo | 工程/教学基线 |
| [Reflex](https://github.com/kshetrajna12/reflex) | typed decision API | 候选互操作基线 |
| [LitJev](https://github.com/zhengxuyu/litjev) | 轻量 Jev 风格实现 | 适合烟测，不代表能力上限 |
| [snapjudge](https://github.com/Micha0827/snapjudge) | 一步判别/接口封装 | 适合接口比较 |

## 训练模型与决策头（16） {#trained-routes}

| 项目 | 公开资产 / 方法 | 状态判断 |
|---|---|---|
| [Bespoke Nimble](https://github.com/bespokelabsai/nimble) / [9B checkpoint](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B) | Qwen3.5-9B LoRA、数据和训练配方；flat schema enum/boolean logits | **P0 候选**；作者不保证校准 |
| [jevlike](https://github.com/vinnylarouge/jevlike) | option attention、候选概率 | 训练式社区实现 |
| [openjev](https://huggingface.co/AlexWortega/openjev) / [source](https://github.com/mikesmullin/openjev) | 公开模型与源码 | 待审核训练/评测协议 |
| [decider-2b](https://github.com/Mapika/decider) / [checkpoint](https://huggingface.co/Mapika/decider-2b) | 决策模型，另有视觉版本 | 待审核 typed primitives |
| [jeff](https://github.com/logan-markewich/jeff) | GLiFormer/GLiNER 路线 | 相邻 schema-head 基线 |
| [Verdict](https://github.com/Heman10x-NGU/Verdict-open-jev) / [rlcd-modernbert-151m](https://huggingface.co/heman10x/rlcd-modernbert-151m) | ModernBERT 决策模型 | 待审核 RLCD 声称与数据 |
| [open-jev](https://huggingface.co/spaces/pngwn/open-jev) / [scorer](https://huggingface.co/pngwn/system-one-qwen3.5-4b-scorer-v2b) | Qwen3.5 scorer | 待审核 checkpoint revision 和协议 |
| [jevbetter](https://github.com/olanotolu/jevbetter) | 训练式社区实现 | 待复核公开资产 |
| [system-one-open](https://github.com/mithalouni/system-one-open) | 开放 System One 模型 | 待复核训练证据 |
| [qwen-rlcd](https://github.com/shamazharikh/qwen-rlcd) | Qwen 决策微调 | 待复核 RLCD 定义与数据 |
| [system-one-gemma](https://github.com/akash-kamat/system-one-gemma) | Gemma 决策微调 | 待复核训练与校准 |
| [Laya](https://github.com/NandhaKishorM/laya) / [checkpoint](https://huggingface.co/convaiinnovations/laya) | typed decision、温度校准、demo/notebook | **P0 候选**；领域依赖且高候选受限 |
| [System One Mini](https://huggingface.co/DavidHatley/system-one-mini) | 小型公开 checkpoint | 待审核数据和评测 |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) / [checkpoint](https://huggingface.co/C-Tianyu/NanoJev) | Qwen3-0.6B + decision heads；Choice/Boolean/Score | **P0 候选**；公开训练与服务路径 |
| [mini-jev](https://github.com/r-ms/mini-jev) | 小型训练式复现 | 待审核训练资产 |
| Archer Hume open-weight Jev-like model | 仅有预告/说明 | **尚未发布**；不得计为可运行实现 |

## 扩散语言模型路线（4） {#diffusion-routes}

| 项目 | 主要形态 | 边界 |
|---|---|---|
| [vLLM DiffusionGemma PR #57250](https://github.com/vllm-project/vllm/pull/57250) | DiffusionGemma serving 支持 | 基础设施，不是 Jev checkpoint |
| [razorback16/openjev](https://github.com/razorback16/openjev) | DiffusionGemma-as-Jev | 独立行为复现 |
| [JoshuaSP/open-jev](https://github.com/JoshuaSP/open-jev) | 扩散模型决策路线 | 独立行为复现 |
| [LocalJev](https://github.com/githubnext/localjev) | GitHub Next 本地实验 | 需单独验证校准与吞吐 |

## 先验工作（2） {#prior-work}

| 项目 | 与 System One 的关系 | 边界 |
|---|---|---|
| [GLiNER 2.5 models](https://huggingface.co/collections/fastino/gliner25-models) | 动态实体/schema 表示与判别 | 先验方法，不是 Jev 复现 |
| [DeepMost sales conversion model](https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning) | 专用概率决策模型 | 领域判别器；需按原论文任务理解 |

## 评测、行为研究与索引（9） {#evaluation-resources}

| 项目 | 类型 | 用途 |
|---|---|---|
| Archer Hume Jev architecture speculation | 解释文章 | 只作社区猜测，不作官方架构证据 |
| [jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration) | OOD / calibration | **P1 评测候选** |
| Matija Sosic Jev explainer | 视频解释 | 背景材料 |
| [typesafe-ai-benchmark](https://github.com/iammrduncan/typesafe-ai-benchmark) | API benchmark | **P1 在线黑盒协议候选** |
| [awesome-jev](https://github.com/AnotiaWang/awesome-jev) / [awesome-jev](https://github.com/hellogumbo/awesome-jev) | 索引 | 查重与发现，不是实现 |
| [jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks) | benchmark | **P1 公共评测候选** |
| hhkkmon community thread | 讨论 | 非技术证据 |
| mygtmhire long-form warning | 评论文章 | 风险提示，非实现 |
| [jev-behavior-study](https://github.com/RINNECODER/jev-behavior-study) | 黑盒行为研究 | **P1 协议证据候选** |

## 维护规则

- 新项目先进入本页并标注路线，再决定是否进入[选型与集成路线图](implementations.md)。
- 项目名称包含 Jev/RLCD 不足以证明复现质量；必须检查权重、数据、loss、评测切分和许可证。
- README 自报数字只作为候选线索；本仓库看板仅展示本地实际执行且通过数据隔离契约的结果。
- tracker 删除或更名的项目保留快照日期，避免链接变化被误判为本仓库已验证。
