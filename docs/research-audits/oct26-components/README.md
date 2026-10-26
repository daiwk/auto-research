# 2026-10-26：新公告与 Google 优先来源补漏

本批交付 **8 个低成本 L1 组件、8 篇仅资料收录**。8 个组件均以同一冻结版本在 CPU 和真实 **NVIDIA A100** 上执行42/43/44三个种子；完整大模型、私有日志、API 或多卡实验统一标为**成本过高，不复现（审查 DONE）**，不自动重试。

## 这次哪些是真正新增

八类 arXiv 官方页面均实际更新为 **10月26日公告**。页面共1180个分类条目，去重为835个论文身份；包含446个 new、289个 cross-list、445个 replacement 分类条目。相对上次快照增加802个身份、832个版本字符串——**这些不是新论文数量，更不是已全文审完835篇**。跨类、旧论文改版和周末提交不能相加成“今天发表了1180篇”。

本批选中的新公告论文，其 v1 大多在10月22--23日提交；它们进入新公告，但都早于上次10月25日抓取的结束时间，因此“选中条目中、上次抓取之后首次公开”的数量为0。两种口径分别保留，不把公告日期改成首次提交日期。

优先机构本次目录实际取回 Google29/29页、Meta6/6页、DeepMind9/9页。Google430条相对最后成功快照428条多两个 URL，分别是 **2025年的 Watch and Learn** 和 **2026年4月的 PaperOrchestra**，本次按历史目录补漏收录；Meta144条、DeepMind265条在此有限目录对比中没有新增URL，不等于机构或全网没有新论文。DetectorScope则是近期官方源码触发的补漏；仓库创建时间与历史提交时间分开记录。

精确计数、分类 ID、抓取时间与哈希见[来源覆盖](source-coverage.json)；每项交付状态及原始日期见[固定范围](task-scope.json)。这是限定交付闭环，不是整段日期或全网的全文穷尽声明，**全局审查水位仍为2026-10-15**。

## 已实现的低成本组件

| 优先级 | 论文 / 机构 | 本地实际覆盖 | 主要边界 |
| --- | --- | --- | --- |
| P0 | [DetectorScope，Google DeepMind合作](../../foundation-models/2610.30006-detector-scope/README.md) | SAE特征max-pool、描述验证mask、训练集RMS、proximal稀疏head及精确logit归因 | 不训练SAE/LLM，不生成描述，不报告文本检测能力 |
| P0 | [OPST，Google](../../post-training/2610.32770-opst/README.md) | 外部验证观测门、逐response等权归约、EMA | 原PDF散度权重有歧义；canonical JSD未实现，不静默改公式 |
| P1 | [HGE，美团](../../recommendation-components/2610.32420-hge/README.md) | HSAE、PLL和有符号残差/逐样本门控融合 | 不含DIN/DCN、完整Dice塔或712M私有日志训练；线上+1.42%为作者结果 |
| P1 | [Frontier-OPD，清华](../../agent-research/2610.32802-frontier-opd/README.md) | 有符号分歧、轨迹平衡节点排名、实测同长桥窗口接纳 | 环境、teacher、真实replay与蒸馏训练均为外部，接纳不等于任务成功 |
| P1 | [MART-GRPO，香港大学](../../post-training/2610.32431-mart-grpo/README.md) | 外部事件边界、失败前缀mask、原分母clipped PG | 不训练事件VLM或VLA，不宣称理想martingale无偏性成立 |
| P1 | [DT-JEPA，东南大学](../../foundation-models/2610.32657-dt-jepa/README.md) | 高斯未来目标、重参数、AdaLN、BC、双critic多步目标 | 模块由调用方给出，不替代真实DT、D4RL或环境 |
| P1 | [EditJev，北京大学](../../foundation-models/2610.32635-editjev/README.md) | 离线偏好loss、非padding hidden head、质量/速度路由 | 不生成图片，不读取测试质量，不加载Qwen或候选编辑器 |
| P1 | [UniAction，Stanford](../../multimodal-models/2610.32977-uniaction/README.md) | 共享语义码本、原生位置回调、基数校准joint attention | 不造替代RoPE，不运行视频世界模型，不宣称自定义kernel加速 |

定义性数值门槛与负对照在[执行规格](execution-spec.json)。[CPU原始结果](raw-cpu.json)、[A100原始结果](raw-cuda.json)和[可移植Git证明](frozen-sources.json)绑定同一科学快照 `fae525e8939a003d97452bef78b283389c718376`。每篇独立 metrics 与 GPU receipt 从上述论文页可见，不合并成一个虚假的通用准确率。

## 高成本资料：已审查，不复现

| 优先级 | 论文 | 不启动完整实验的依据 |
| --- | --- | --- |
| P0 | [FlexGlue，Google合作](../../multimodal-models/2610.32976-flexglue/README.md) | DINOv3与9层匹配器，作者多H200/多天配置；不把softmax替身当entmax/Fenchel--Young方法 |
| P0 | [Watch and Learn，Google合作](../../agent-research/2510.04673-watch-and-learn/README.md) | 8×A100训练IDM、53K视频轨迹、7B计算机Agent与真实桌面环境 |
| P0 | [PaperOrchestra，Google](../../agent-research/2604.05018-paperorchestra/README.md) | 多Agent写作、联网检索、图示与大量API/人工评测；社区skill不是作者开源实现 |
| P1 | [LazyFlash](../../foundation-models/2610.31911-lazyflash/README.md) | 8×H200、65K上下文、2500steps和自定义反向kernel；不拿普通mask宣称加速 |
| P1 | [PathJev](../../foundation-models/2610.32478-pathjev/README.md) | 病理数据、专门模型与多种子长时训练/生成式对照 |
| P1 | [ImageRSI](../../agent-research/2610.32120-image-rsi/README.md) | 真实图像生成、外部多维judge/修复和judge训练的完整闭环 |
| P1 | [RSI-Opt](../../agent-research/2610.32026-rsi-opt/README.md) | API代码Agent反复修改优化器并真实训练，多任务/多种子搜索；保留held-out lineage污染疑点 |
| P1 | [HarnessMM](../../agent-research/2610.32813-harnessmm/README.md) | 原生harness、真实callback证书与调用计费、多基准API矩阵；不伪造执行receipt |

这8项没有可执行operator、实验metrics或GPU通过声明。高成本审查完成不等于实验已实现，也不留下反复扫描时自动重试的隐藏队列。

## 验证与来源说明

```bash
PYTHONPATH=src python scripts/curate_oct26_components.py --check
python -m pytest tests/test_oct26_component_evidence.py \
  tests/test_oct26_foundation_components.py tests/test_detector_scope.py \
  tests/post_training/test_oct26_post_agent_components.py tests/reproductions/test_hge.py
```

GPU包仅同步本轮公开源码和冻结证明，无模型、数据、密钥或整个工作区。首次隔离导出发现既有JEV父包会急切导入未打包的benchmark依赖，执行失败且没有生成通过凭证；之后仅修正验证器为冻结文件加载，并与常规包导入单测分开核验。最终CPU/A100结果来自同一修正后的快照，不用第一次失败的部分运行充作结果。

本地临时站点、源码传输包和本轮远端临时目录在验收后清理；源代码、原始结果、失败说明与脱敏凭证保留。
