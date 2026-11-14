"""Build individually checked title/abstract scope exclusions for the early pending block."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from route_nov09_title_abstract import load_observations

# Withdrawn after identifying a defining, independently inspectable method.
# Domain words or negative evaluation results must not regenerate a scope terminal.
PRIMARY_REVIEW_ONLY = frozenset({"2610.34459", "2610.24910", "2610.26433"})

DECISIONS = (
    ("2610.24153", "volumetric label maps", "医学体积分割掩膜生成，控制量是器官、肿瘤和人口统计；不是通用多模态基础模型。"),
    ("2610.26261", "RNA backbone", "为 RNA 构象集合设计的几何随机桥，终点是分子结构覆盖与恢复；不是语言/视觉基础模型。"),
    ("2610.28943", "protein optimization", "蛋白质序列多目标优化的领域采样方法；不属于本库通用后训练或 Agent 交互。"),
    ("2610.28985", "patient body models", "从不完整全身扫描补齐患者体表模型的临床几何估计。"),
    ("2610.29111", "molecular magnetism", "分子磁学的等变量子自旋代理；研究对象是物理可观测量而非本库模型。"),
    ("2610.29267", "radar heart-sound", "接触式/非接触式心脏生理信号与超声表型配对数据资源。"),
    ("2610.29322", "neonatal HIE", "新生儿缺氧缺血病灶在 ADC 图像中的专用定位，不是通用扩散预训练。"),
    ("2610.29589", "BRICS decomposition", "分子属性预测使用化学片段图的输入表示与归因，不是通用图语言模型。"),
    ("2610.29665", "cervical cytology", "宫颈细胞病理分类及置信度转诊的专用临床视觉模型。"),
    ("2610.29738", "thyroid ultrasound", "甲状腺超声结节分类的放射组学瓶颈，目标为可解释临床测量。"),
    ("2610.29815", "hearing assistive devices", "以 EEG 注意力辅助目标说话人提取的听力设备信号处理。"),
    ("2610.30104", "Cell Painting assay", "Cell Painting 显微图像批效应的专用生物影像排行榜，不是本库通用模型评测。"),
    ("2610.30207", "M/EEG", "线性高斯脑磁/脑电逆问题的测量约束与后验谱分解。"),
    ("2610.32493", "Ki67 cell typing", "针对乳腺病理 Ki67 的细胞分割聚类与染色类型量化。"),
    ("2610.33307", "RNA sequencing", "RNA 测序基因面板的 Boruta/随机森林参数实证，不是基础模型训练。"),
    ("2610.35163", "decision trees", "临床表格合成的树条件分布与变量顺序比较，非基础模型或后训练。"),
    ("2610.35204", "all-atom molecular dynamics", "48 个 RNA 系统的全原子动力学仿真资料，不是语言/视觉研究数据。"),
    ("2610.35378", "heartbeat representation", "心律失常分类专用 ECG 心搏自监督迁移学习。"),
    ("2610.35984", "plant disease", "橄榄树病害分类的图像增强与样本均衡策略，未提出本库通用模型。"),
    ("2610.28701", "ground plane normal", "球形移动测绘中用 RANSAC 估计地平面法线与里程计。"),
    ("2610.28712", "teleoperation", "人形遥操作的视觉—上肢角度映射与操作者体验实验。"),
    ("2610.28761", "human-robot interaction", "物理人机引导/跟随模式识别及自适应控制，非语言 Agent 或 VLA。"),
    ("2610.29356", "feedforward control", "刚性/弹性机械臂负载变化下的前馈控制跟踪。"),
    ("2610.29438", "multi-IMU", "腿式机器人多 IMU 传感器时空标定，研究目标为硬件外参精度。"),
    ("2610.29461", "snake robots", "可扭蛇形机器人的侧绕步态运动学与移动速度。"),
    ("2610.29474", "upper-limb prosthetic", "为上肢假肢的抓握部件定位扩展多物体视觉分割。"),
    ("2610.29478", "snake robots", "低净空蛇形机器人滚动步态与平面转向设计。"),
    ("2610.29565", "differential wrists", "耦合传动机械臂的饱和约束映射与遥操作手感连续性。"),
    ("2610.29570", "Jacobian", "串联机械臂 Jacobian 性能指标的关节角不变性和工作空间计算。"),
    ("2610.29839", "spline-based", "机器人运动基元的时空样条参数化与病人搬运动作同步。"),
    ("2610.29964", "Mobile manipulators", "半静态环境中移动机械臂的几何主动感知与避碰规划。"),
    ("2610.30102", "commercial", "商业微分段工具在多机器人 IoT 网络上的实验部署报告，非 Agent 算法。"),
    ("2610.32259", "GNSS", "GNSS/IMU 紧耦合定位的完整性保护级别与城市峡谷故障检测。"),
    ("2610.28327", "weather prediction", "气象站稀疏观测同化和天气场降尺度，目标为温度/降水分析。"),
    ("2610.28973", "Enhanced Rock Weathering", "以冻结天气表征辅助岩石风化碳移除采样的环境监测应用。"),
    ("2610.30007", "woodland class", "遥感土地覆盖分割边界的细胞自动机修正；不是通用视觉模型。"),
    ("2610.33482", "climate", "气候再分析场的公里级降尺度算子，面向温度与降水。"),
    ("2610.35956", "CSI", "无线通信上下行信道状态预测与频谱效率，不是信息检索。"),
    ("2610.35972", "water distribution", "供水管网多处漏点定位的图神经网络应用。"),
    ("2610.29630", "ionospheric", "以雷达和空间天气参数预报电离层不规则体分布。"),
    ("2610.29594", "Visible Light", "可见光通信室内定位的跨区域迁移和能耗优化。"),
    ("2610.29638", "Visible Light Communication", "工业可见光定位跨场地迁移和参考点成本评价。"),
    ("2610.29643", "channel coding", "面向图像传输的联合信道编码和调制，核心是通信物理层。"),
    ("2610.26967", "weakly submodular", "弱次模最大化在拟阵约束下的贪心近似理论。"),
    ("2610.27317", "partial differential equations", "为流体和等离子体识别控制方程的稀疏谱 PDE 求解。"),
    ("2610.27888", "partial differential equations", "非结构网格 PDE 上约束自动微分与正反物理问题求解。"),
    ("2610.28141", "PPAD", "多面体博弈相关均衡与不动集合的计算复杂性证明。"),
    ("2610.28800", "Gaussian measure", "高斯测度下浅深神经网络逼近复杂性的形式理论，没有训练算子。"),
    ("2610.28978", "exposition", "多视图公共信息与经典相关分析的自包含综述性论述。"),
    ("2610.29007", "Wasserstein gradient flow", "能量核最大均值差异的测度梯度流、收敛和粒子理论。"),
    ("2610.29227", "measure-valued data", "测度值数据的随机最优传输重心模型，非通用语言/视觉模型。"),
    ("2610.29425", "generalization", "随机学习算法的向量相关泛化界和统计理论。"),
    ("2610.29510", "Stein", "非归一化统计模型估计的评分规则与渐近效率理论。"),
    ("2610.29575", "online prediction from experts", "差分隐私专家在线预测的 regret 上下界理论。"),
    ("2610.29673", "multi-armed bandit", "共享回报多玩家 bandit 的稳定性及收敛证书理论。"),
    ("2610.29679", "distribution-valued data", "分布值数据的 Wasserstein PCA 统计降维，不是基础模型。"),
    ("2610.29798", "hypothesis testing", "未知分布采样下的非对称假设检验样本复杂度。"),
    ("2610.29949", "Mumford-Shah", "Gaussian Mumford–Shah 图像分段能量的极小解存在性证明。"),
    ("2610.29982", "current treatment effects", "非平稳 bandit 上即时处理效应的统计推断与 regret 权衡。"),
    ("2610.30122", "fixed point", "无扩张映射近似不动点的准多项式复杂度与随机博弈理论。"),
    ("2610.35958", "point-process filters", "高斯点过程滤波在长静默后的显式更新超调理论。"),
    ("2610.25565", "bone scaffolds", "可打印骨支架的多尺度拓扑优化与力学可制造性，不是通用生成模型。"),
    ("2610.28703", "topology optimization", "材料结构应力约束下的大规模拓扑优化，不是神经架构搜索。"),
    ("2610.28949", "wafer defect", "半导体晶圆缺陷签名的超维计算专用分类。"),
    ("2610.28974", "material CT", "材料 CT 的确定性多阶段伪标注与微结构量化。"),
    ("2610.29047", "fish", "水产鱼体测量的弱监督分割和轨迹提示，非通用多模态方法。"),
    ("2610.29091", "blood pressure", "PPG 血压跟踪中采集上下文与会话校准的临床信号比较。"),
    ("2610.29101", "Sperm whales", "鲸类声码结构的节奏/声谱双通道表征，不是通用音频语言模型。"),
    ("2610.29120", "tourism", "城市旅游路线规划中的 Z-Number 不确定性建模，不是 Agent 工具学习。"),
    ("2610.29158", "optical flow", "事件相机 SNN 光流估计的专用时变瓶颈。"),
    ("2610.29205", "connectomes", "果蝇脑连接组重建差异与神经生物回路模型的稳健性研究。"),
    ("2610.29212", "industrial inspection", "工业巡检视频实例分割的部署优化，不是搜广推或通用基础模型。"),
    ("2610.29493", "crystal-exchange", "特定 11×11 棋盘谜题的最短解及计算机辅助证明。"),
    ("2610.29841", "metalens", "中波红外金属透镜的光学设计与成像，不是 AI 模型。"),
    ("2610.30086", "crystalline materials", "在 Wyckoff 轨道上生成晶体候选并筛查物理材料性质。"),
    ("2610.30713", "Industrial Internet of Things", "工业 IoT 流量的梯度提升/LightGBM 威胁检测应用。"),
    ("2610.31850", "Urban region", "城市移动/兴趣点/土地使用的区域向量应用，不是工业推荐模型。"),
    ("2610.32299", "aerodynamic", "非结构网格空气动力场预测的算子替代，目标为 RANS 仿真。"),
    ("2610.35963", "aerodynamic design", "商用飞机气动构型生成优化与几何约束，不是通用视觉/语言架构。"),
    ("2610.28710", "chapter", "翻译学的数据伦理章节，讨论版权、所有权、偏见与责任，不是算法。"),
    ("2610.29140", "Engineering graduates", "印度工程教育和招聘筛选中的 AI 使用质性研究。"),
    ("2610.33605", "book", "生成式/Agent AI 数据治理的法律和制度专著，不是论文复现对象。"),
    ("2610.29864", "two-layer linear network", "比例高维极限下两层线性网络梯度流的谱分布和对齐时标理论，没有可接入本库的训练算子或能力基准。"),
    ("2610.33522", "physical devices", "利用电子/光学器件变量与物理变换实现的物理神经网络路由，依赖设备模型而非本库通用基础模型或后训练。"),
    ("2610.35554", "IMU embedded in the Insta360", "消费级全景相机嵌入式 IMU 的结构恢复尺度标定与传感器计量，非 AI 算法或 Agent 论文复现。"),
    ("2610.24334", "fixed hierarchical tree", "固定树上下文无关文法上温度重标定与互信息幂律的物理统计类比，未引入模型训练算法。"),
)

NOT_SELECTED = (
    ("2610.26941", "systematic overview", "工业 Agent 的系统性概览、能力分类、概念架构与应用综述，贡献为设计参考而非已验证的新算法或公开能力基准；本轮不选。"),
    ("2610.27051", "This review presents", "天体物理与宇宙学图神经网络的原理、应用和最佳实践综述，非原创模型算法或新的公开基准；本轮不选。"),
    ("2610.29187", "this tutorial paper reviews", "学习控制十年进展的入门教程，随文示例用于教学而非宣称新算法或新公开能力基准；本轮不选。"),
    ("2610.30221", "It reports no empirical results", "AAM/5C 为概念专著和待验证的规范性参考模型，摘要明确没有实证结果，非已交付的新算法或公共能力基准；本轮不选。"),
    ("2610.35089", "This survey organizes the literature", "围绕记忆生命周期、载体和系统角色组织既有 LLM 记忆文献，贡献为综述路线图，非原创算法或新公开基准；本轮不选。"),
    ("2610.22650", "mismatch between AdamW and Muon", "在既有 AdamW/Muon 间切换进行预训练、续训和 SFT 对照，贡献为优化器匹配成本的经验复查，非新优化算法或公开基准；本轮不选。"),
    ("2610.24692", "Using CARE-Bench", "在既有 CARE-Bench/HealthBench 上比较 JEV 的临床分诊准确率、校准和澄清需求，贡献为领域应用评估而非新算法或公开基准；本轮不选。"),
    ("2610.29654", "seeing measurements from the Maunakea summit", "比较既有 GP、FloTS、RNN、LSTM 对天文台大气视宁度的概率预报，贡献为单一环境应用对照，非新通用算法或公开能力基准；本轮不选。"),
    ("2610.31467", "menstrual health monitoring", "将既有 RAG 与提示约束用于月经健康记录摘要，比较临床一致性和可读性，贡献为医疗叙事应用实证，非新通用算法或公开基准；本轮不选。"),
    ("2610.32060", "corpus-grounded taxonomy of communication failures", "整理既有多 Agent 失败轨迹形成交流故障分类，贡献为现象分类和设计建议，非新交流算法或已定义的可执行公开基准；本轮不选。"),
    ("2610.32726", "Iterated Prisoner's Dilemma", "在既有重复囚徒困境中对照模型群组、语言提示与合作传播，贡献为集体行为实证，非新多 Agent 算法或公开基准；本轮不选。"),
    ("2610.34163", "train a Soft Actor-Critic (SAC) agent", "用现有 SAC 与人群模拟学习动态隔栏配置，贡献为特定人流控制基础设施应用，非新 RL 算法或公开能力基准；本轮不选。"),
    ("2610.22745", "We compare it with LDA, MiniLM and FinBERT", "以历史截止预训练编码器和既有主题/预测模型进行股票收益回测，贡献是单一金融应用的前视偏差与选模观察，并非新的通用算法或公开能力基准；本轮不选。"),
    ("2610.22882", "five production models", "用既有集体风险博弈比较五个模型的合作行为与伙伴响应，贡献是机器行为实证而非新 Agent 算法或新公开基准；本轮不选。"),
    ("2610.22961", "using fMRI data collected during dialogue", "以对话 fMRI 研究 LLM 表征与人脑语言产生/理解的关联，贡献为认知神经实证，不是新基础模型算法或公开能力基准；本轮不选。"),
    ("2610.24045", "We audit released code", "复核既有图异常检测器的测试标签泄漏与结构敏感性，贡献为专科图检测评测审计，而非本库新模型算法或公开基准；本轮不选。"),
    ("2610.24086", "we compare pretrained (Base)", "对七条已发布模型谱系在既有社会困境中做 Base/SFT/Aligned 对照，结论为记忆与合作的行为观察，不是新后训练算法或公开基准；本轮不选。"),
    ("2610.24260", "classify survey text data into 16 classes", "对问卷文本的 16 类分类应用比较 RoBERTa、GPT-3.5 与集成的成本和准确率，非新训练算法或公开能力基准；本轮不选。"),
    ("2610.24671", "compares six state-of-the-art explicit memory systems", "在现有 LongMemEval-S/BEAM-100K 上对照六个显式记忆系统与原始历史 RAG，贡献是控制变量下的重复评估，不是新算法或新公开基准；本轮不选。"),
    ("2610.25158", "using the 2022 EU Loneliness Survey", "检验 LLM 调查模拟是否重现既有欧洲孤独调查的年龄差，属于社会调查模拟的单一应用实证，不是新算法或公开能力基准；本轮不选。"),
    ("2610.25440", "35 pages of transcribed data", "将现有小型 VLM 微调用于拉科塔语档案 OCR，研究少量页面、分割和扫描质量的实际约束；贡献是领域案例而非新通用算法或公开基准，本轮不选。"),
    ("2610.25788", "This single-study audit", "针对已发表 Rel-A.I. 的人类依赖率表做模拟用户复查，作者明确限于单一研究审计；没有交付新的算法或公开能力基准，本轮不选。"),
    ("2610.25816", "We evaluate seven LMs", "在四个既有语言数据集上比较模型的情态词语义消歧和语料频率效应，贡献是语言学行为实证，不是新算法或公开基准；本轮不选。"),
    ("2610.25826", "We evaluate six recent FL methods", "在 SWE-bench Verified 与 Defects4J 上统一比较六个既有故障定位方法的修复收益，贡献为方法效用复查而非新定位/修复算法或公开基准；本轮不选。"),
    ("2610.26008", "interrupted time-series regression", "以中断时间序列观察 ChatGPT 发布前后科学摘要文风的变化，贡献是写作社会语言学实证，不是训练算法或能力基准；本轮不选。"),
    ("2610.26416", "compare SPARK-style rollout recycling", "把既有 SPARK 式轨迹回收迁移到代码并与 GRPO 对照，报告单适配器漂移和未泛化结果；本轮不将该重复/迁移实证列作新算法或公开基准复现。"),
    ("2610.26461", "We present a controlled study", "在 SQuAD 2.0/RepLiQA 的既有 logistic readout 上控制负例与校准条件，贡献为实验因素分析而非新读出算法或公开基准；本轮不选。"),
    ("2610.26595", "examine eight attacks against three open-weight language models", "在既有八类越狱和三模型上比较 ASR 判定与采样预算，提出报告建议而非新攻击/防御算法或公开基准；本轮不选。"),
    ("2610.26651", "using the ESM-2 family of protein language models", "对蛋白质模型既有过滤和微调措施进行有效性/持续性复查，贡献为特定生物模型防护实证，非新通用算法或公开基准；本轮不选。"),
    ("2610.27002", "evaluate five ASR architectures on Lhasa Tibetan", "用字符、音节、分词误差比较既有藏语识别架构和适配配置，贡献为低资源语音评测实证，非新算法或公开能力基准；本轮不选。"),
    ("2610.27027", "evaluate four systems", "比较单模型和三种既有多 Agent 拓扑在临床任务中的幻觉，贡献是协作是否可靠的重复对照，非新算法或公开基准；本轮不选。"),
    ("2610.27360", "evaluate 19 models", "在八个既有多模态基准上逐题比较同族模型尺寸的反向缩放，贡献是经验规律而非新架构或公开基准；本轮不选。"),
    ("2610.27381", "in the AIDev dataset", "对既有 AIDev 的 AI PR 做文档共变与后续修复的观察性分析，非新的 Agent 算法或公开能力基准；本轮不选。"),
    ("2610.27610", "full-text coding of 114 eligible studies", "对 114 篇 RSI 研究的评价设计做人类编码和证据综述，提出报告规范，不是新自改进算法或可执行能力基准；本轮不选。"),
    ("2610.27790", "circuit discovery methods from the mechanistic interpretability field", "使用既有电路发现方法比较五个 LLM 的语言/算术电路，贡献为机制观察而非新的模型算法或公开评测基准；本轮不选。"),
    ("2610.27889", "compare optimized harnesses with their pre-optimization counterparts", "以既有 pass@k 分析区分 harness 优化的覆盖扩展与成功率诱发，贡献是优化收益的控制实证，而非新算法或公开基准；本轮不选。"),
    ("2610.28772", "integrated application of large language models", "把现有 LLM 与任务分解用于心理治疗忠实度和督导反馈，临床验证对象为应用流程，非新通用算法或公开能力基准；本轮不选。"),
    ("2610.28799", "all 26 CATO factors", "在既有法律 CATO 因子上用线性探针和稀疏自编码器比较三个模型，贡献为法律概念表征定位实证，非新算法或公开基准；本轮不选。"),
    ("2610.28843", "isolate field-label effects", "控制视觉问答字段标签、提示顺序与辅助线索来观察模型判断变化，贡献为提示因素实证，不是新视觉模型算法或公开基准；本轮不选。"),
    ("2610.28904", "Using tropical cyclones in GraphCast as a test case", "将既有稀疏自编码器用于气象 GraphCast 的台风属性探查，贡献为专科气象表征观察，非新基础模型算法或公开基准；本轮不选。"),
    ("2610.28947", "We compare the two at equal bits", "在现有内核、GPU 和模型上比较 2:4 稀疏与量化的精度/吞吐，贡献是硬件适用条件实证，而非新压缩算法或公开能力基准；本轮不选。"),
    ("2610.28957", "compare 11 retrieval configurations", "固定证据分段和答案生成器比较既有检索与 JEV/Decisions/Clef 全文扫描，贡献为质量成本对照，非新检索算法或公开基准；本轮不选。"),
    ("2610.29152", "existing Cheff-identified or SynthCheX candidates", "以现成胸片生成候选、质量判断与来源分类器审计医疗数据准入，贡献为应用性证据链分析，不是新通用算法或公开能力基准；本轮不选。"),
    ("2610.29189", "This study reviews frameworks", "推理—搜索增强系统的操作分类、基准难度分析和既有消融证据综述，非原创算法或新公开基准；本轮不选。"),
    ("2610.29507", "two benchmark families used in the transfer analysis", "在既有时间推理基准间做微调迁移与认知需求分析，贡献为基准解释的实证复核，不是新模型算法或公开基准；本轮不选。"),
    ("2610.29533", "under matched tokenisation, context length, model capacity", "将既有块扩散与自回归配方用于 MIMIC-IV 并比较临床表征和推理效率，贡献为领域应用对照，非新通用算法或公开基准；本轮不选。"),
    ("2610.29602", "under an identical retrieval-based few-shot protocol", "在 ToTTo 上统一比较既有扩散/自回归模型与 QLoRA 的相似度和忠实性，贡献是诊断实证，不是新算法或公开基准；本轮不选。"),
    ("2610.29657", "using the BBQ benchmark", "在既有 BBQ 上比较尺寸、量化、提示与弃答的偏见混淆，贡献为公平评测的因素分析，非新训练算法或公开基准；本轮不选。"),
    ("2610.30413", "approximately 824K tweets", "以现有语言分析工具研究 Twitter 收购前后的心理健康自我披露，贡献为社交媒体行为观察，不是模型或 Agent 算法；本轮不选。"),
    ("2610.30564", "historical tests over 2023-2025", "对金融新闻信号的时效处理在既有 RL/LLM 投资组合中做历史回测，贡献为单应用配置对照，非新通用算法或公开能力基准；本轮不选。"),
    ("2610.30755", "a naive RAG baseline", "把既有 dense retrieval 和 reranking 作为原始历史基线，与现有记忆系统在四个公开基准上复查，未提出新的记忆算法或新基准；本轮不选。"),
    ("2610.30763", "in the public PRISM dataset", "对已公开 PRISM 中自陈偏好和人类评分作相关及预测分析，贡献为人类反馈行为观察，非新偏好优化算法或公开基准；本轮不选。"),
    ("2610.31135", "These exploratory results", "通过移动既有问答证据比较 Transformer、SSM、混合模型的位置偏差，作者定位为探索性机制实证，不是新序列混合器或公开基准；本轮不选。"),
    ("2610.31193", "museum collection", "在博物馆藏品描述应用中控制元数据字段和图像，分析生成内容的依据，非新通用模型算法或公开能力基准；本轮不选。"),
    ("2610.31199", "World Values Survey", "比较国家人格和语言线索对既有价值调查及开放生成的影响，贡献为文化偏见实证，不是新对齐算法或公开基准；本轮不选。"),
    ("2610.31202", "Using the entire MER60 dataset strictly as a held-out test set", "以现有上下文学习修正音乐情感基模型预测，贡献为特定音乐情感应用的文本/音频示例配置对照，非新通用算法或公开基准；本轮不选。"),
    ("2610.31586", "Spanish MIR residency examination", "在既有西班牙住院医考试上比较四模型的准确率、信心和图像依赖，贡献为临床考试实证，不是新算法或公开能力基准；本轮不选。"),
    ("2610.31624", "Using InstrumentalEval", "对 OLMo-3 既有 SFT/DPO/RLVR 检查点在同一风险基准上的非单调行为做复查，贡献为安全轨迹实证，非新后训练算法或公开基准；本轮不选。"),
    ("2610.32578", "six-week case study of my personal system", "作者个人仓库六周规则、失败与文档审计的探索性案例，未形成新的通用算法或公开能力基准；本轮不选。"),
    ("2610.33243", "proof of concept work", "使用既有 U-Net/ResNet34 在 541 张图像上做象牙识别概念验证，贡献为野生动物执法应用案例，非新通用算法或公开能力基准；本轮不选。"),
    ("2610.33475", "systematic review", "按 PRISMA 汇总云端 LLM 硬件虚拟化、编排和推理文献，贡献为跨层分类与路线图，非原创算法或公开基准；本轮不选。"),
    ("2610.33488", "retrospective comparison", "以课程聊天特征和既有六种估计器预测学生成绩，作者明确未建立学习效果，贡献为教育应用的回顾比较；本轮不选算法复现。"),
    ("2610.33813", "compare both regimes on prompt-safety classification", "控制 LoRA/全量微调的格式、学习率与种子，检验既有适配方法在提示安全分类中的差异，贡献为配置因素实证，非新算法或公开基准；本轮不选。"),
    ("2610.33969", "drawn from prior work", "比较既有数据质量指标对固定微调预算效用的预测，贡献为指标实证而非新数据选择算法或公开基准；本轮不选。"),
    ("2610.34487", "two of them, Proptest-AI and Agentic-PBT", "将既有 PBT 生成器迁移到十个软件目标并复核分支覆盖和漏洞报告，贡献为工具泛化实证，不是新生成算法或新公开基准；本轮不选。"),
    ("2610.34591", "one object and one wearer", "单件项链与单个佩戴者的视觉估价场景实验，虽发布数据代码，但作者明确需多对象与人类基准复查，非新算法或成熟公共能力基准；本轮不选。"),
    ("2610.34613", "study 349,156 IaC pull requests", "分析既有 GitHub IaC PR 的作者类型、合入率和可持续性问题，贡献为软件工程观察性研究，非 Agent 算法或新公开基准；本轮不选。"),
    ("2610.35297", "We analyze 114,134 pull requests", "比较现有 Java 仓库中 Agent 支持与人类 PR 的测试结构和覆盖，贡献为观察性软件工程研究，不是新 Agent 算法或公开能力基准；本轮不选。"),
    ("2610.35411", "Using an extraction pipeline established", "用已有情感向量提取管线复查 Gemma 2 六个模型单元的尺度/深度/微调差异，贡献为重复机制研究，不是新算法或公开基准；本轮不选。"),
    ("2610.35496", "empirical study of 42 trajectory-reduction configurations", "比较既有轨迹删除配置在 SWE-bench Verified 的成功率、缓存和成本，贡献为成本核算与配置实证，不是新记忆算法或新公开基准；本轮不选。"),
    ("2610.35560", "MACE models trained on ANI-1x", "对原子势 MACE 的既有多保真训练方案做不确定性分解复查，贡献为材料模型应用实证，非新通用算法或公开基准；本轮不选。"),
    ("2610.35671", "independent safety evaluation", "在既有及内部安全套件上报告 DeepSeek 更新版风险的独立系统评估，贡献为模型安全报告，非新训练算法或新公开能力基准；本轮不选。"),
    ("2610.35857", "study 46 vision encoders", "在现有视觉编码器上比较概念方向的局部/全局线性，贡献为表征机制实证，不是新视觉算法或公开能力基准；本轮不选。"),
    ("2610.35961", "controlled study of offline response-based knowledge distillation", "用既有离线响应蒸馏比较视网膜病分级教师、温度和权重，贡献为临床轻量化应用对照，非新蒸馏算法或公开能力基准；本轮不选。"),
    ("2610.35971", "two public corpora", "在现有软件 Agent 轨迹语料上比较早停预测器、重启和继续运行，贡献为已有策略效用与成本的实证审计，不是新算法或新公开基准；本轮不选。"),
    ("2610.25296", "In this Perspective", "世界模型可解释性的观点文章：提出 Ground/Structure/Verify/Act 研究议程，而非已验证的新算法或公开评测基准；本轮不选作复现。"),
    ("2610.25996", "principles for integrating", "以神经符号视角讨论 Agent 程序记忆与显式目标图的构建原则和挑战，贡献为概念框架而非已评估的独立算法或公开基准；本轮不选。"),
    ("2610.29674", "design perspective", "围绕接受、回避和情感黏性的社交 Agent 设计观点及进行中的设计案例，不是新的可独立复现算法或公开能力基准；本轮不选。"),
    ("2610.29741", "36 semi-structured interviews", "依据 36 次访谈形成 BARD 四阶段需求工程过程理论，研究贡献为工作过程解释而非 Agent 算法或公开基准；本轮不选。"),
    ("2610.29925", "We recommend three critical paths", "关于通用 LLM 情境隐私的立场与三条治理建议，未将建议定义为新的独立算法或公开基准；本轮不选。"),
    ("2610.30307", "extrapolation", "软件买建边界与 AI 编程经济性的市场观察和趋势外推，摘要明确区分外推与预测；不是新的模型算法或公开评测基准，本轮不选。"),
    ("2610.31306", "report no measured effect", "超智能软件工程治理的观点与启发式设计；作者明确未报告 OSTEON 的实测效果，机制论断属于观点，不作为本轮算法复现。"),
    ("2610.31862", "tutorial style", "以教程形式串联 SFT、RLHF、DPO、逆强化学习与离散选择的数学基础，不是原创算法或新的公开评测基准；本轮不选。"),
    ("2610.32313", "qualitative analysis of illustrative PRs", "描述既有 GitHub Copilot 会话与 PR 的干预、迭代分布及案例，贡献是经验观察而非新算法或新公开基准；本轮不选。"),
    ("2610.32464", "perspective paper", "将 Agent 记忆管理视作信息检索前沿的观点论文，提出分类与未来研究议程，非已交付的算法或公开能力基准；本轮不选。"),
    ("2610.32636", "report a case study", "两次工业机器人 focus day 的案例报告，研究工程师使用 Agent 的体验、学习曲线和生产率，非新的通用算法或公开基准；本轮不选。"),
    ("2610.33301", "psychological closeness", "通过个性化反事实叙事研究人类政策风险感知与心理距离的行为实验，Agent 为实验材料生成工具，而非新的模型算法或公开评测基准；本轮不选。"),
    ("2610.34241", "experience report", "基于作者个人编程会话的回顾性系统经验报告，异质任务与量化模型队列不构成统一基准或新算法；本轮不选。"),
    ("2610.34847", "remains untested", "编码 Agent 指令中的伦理条款静态内容研究，摘要明确 Agent 是否遵循指令仍未测试；非行为算法或公开能力基准，本轮不选。"),
    ("2610.35179", "empirical failure-mode analysis", "在既有模型与文本分析数据上比较稳定性、域外泛化和优化影响的失败模式实证，非新训练算法或新公开基准；本轮不选。"),
    ("2610.35451", "qualitative analysis", "汇总 OpenClaw 社区帖文和 GitHub 问题中的安全关切、CWE 类别与缓解建议，贡献为质性社区研究，不是新攻击防御算法或公开能力基准；本轮不选。"),
)


def build(source_dir: Path, inventory_bytes: bytes) -> dict:
    inventory = json.loads(inventory_bytes)
    queue = {r[0]: r for rows in inventory["pending_identities_by_local_first_publication"].values() for r in rows}
    observations, receipts = load_observations(source_dir)
    records, missing = [], []
    decisions = [(identity, witness, reason, "out_of_scope") for identity, witness, reason in DECISIONS]
    decisions += [(identity, witness, reason, "not_selected_this_window") for identity, witness, reason in NOT_SELECTED]
    if PRIMARY_REVIEW_ONLY.intersection(identity for identity, *_ in decisions):
        raise ValueError("withdrawn method candidates require original review, not a regenerated scope terminal")
    for identity, witness, reason, decision in decisions:
        row = observations[identity, queue[identity][1]]
        if witness.casefold() not in row["abstract"].casefold():
            missing.append((identity, witness, row["abstract"]))
            continue
        if any(row.get(key) for key in ("priority_review_required", "priority_query_matches", "priority_source_matches")):
            raise ValueError(f"{identity}: institutional priority must receive original-source review")
        records.append({
            "id": identity, "revision": row["revision"], "title": row["title"], "published": row["published"],
            "source_url": f"https://arxiv.org/abs/{identity}v{row['revision']}",
            "metadata_sha256": row["metadata_sha256"], "capture": row["captures"][0],
            "rule": "individually_reviewed_specialist_or_nonalgorithm_scope" if decision == "out_of_scope" else "individually_reviewed_report_or_perspective_not_selected",
            "title_witness": " ".join(row["title"].split()[:7]), "abstract_witness": witness,
            "reason": reason, "decision": decision, "review_done": True, "fulltext_review_completed": False,
            "automatic_retry": False, "automatic_implementation_queue": False,
        })
    if missing:
        raise ValueError("Missing exact abstract witnesses: " + json.dumps(missing, ensure_ascii=False))
    return {
        "schema_version": 1, "review_scope": "individual_specialist_title_and_abstract_scope_only",
        "terminal_window_scope_only": True, "fulltext_or_cost_inferred": False,
        "input_inventory_sha256": sha256(inventory_bytes).hexdigest(),
        "reviewed_scope_candidates": len(records),
        "owned_block": "pending in-window identity < 2610.36000",
        "source_receipts": receipts,
        "counts": dict(Counter(r["rule"] for r in records)), "records": records,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source_dir", type=Path)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = build(args.source_dir, args.inventory.read_bytes())
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"]))


if __name__ == "__main__":
    main()
