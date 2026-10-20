# 39 项 Google / DeepMind 线索：有界主源审查收口

本轮仅覆盖冻结清单中的 **39 个唯一 arXiv ID**：16 项接受为可负担核心/评测候选（全部未实现），14 项完整复现实验以高成本或私有资源终态关闭，9 项 scope 终态。**不新增实现、不训练、不下载模型、不进入自动实施/重试队列、不接入 Evolve。** SpecGuard 与 Video Encoder Selection 由父批次另行验收，不属于这 39 项的新实现。

审查 DONE 指列明的方法、实验、资源和公开代码关键段已审查，不表示逐段通读、最新修订已覆盖或论文实验复现。所有条目 `full_article_read=false`。没有本轮完全不可读的论文原文；终端 arXiv DNS 失败已原样保留，浏览工具官方 HTML 路径成功，因此不构造来源例外。没有刷新整体研究水位，也没有扩大为全部 497 项已审查。

## 证据与时间边界

- [机器可读审查表](google39-reviews.json) 包含每项的状态、方法、实验、成本、实际章节和证据哈希；[代码主源回执](evidence/google39-code-primary-receipts.json) 仅证明链接仓库可读，未执行其代码。
- arXiv 主源关键段抓取窗口：2026-10-20 18:48:00–18:56:04 UTC；代码仓库复核窗口：18:56:34–18:57:03 UTC。只记录会话有界窗口，不伪造逐请求精确时间。
- 冻结 ID 顺序的 SHA-256（每行一个 ID，含最后换行）：`8623baeb7c2e1132ce70ede629aef201b24ab6cbdfa5038e9848acb7beae6f3b`。
- `source_sha256` 哈希的是公开的 URL/实际定位/UTC/中文转述摘要回执；每份回执另以 `original_capture_sha256` 绑定原始浏览捕获。**原始长捕获仅存本轮私有临时目录，不提交；两者都不是完整原始 HTTP 响应或论文文件哈希。** 公开回执不保留内部浏览引用或整段逐字原文。未使用 DeepXiv、Superpowers 或二手摘要代替原文。
- 论文统一按 v1 关键段审查；其中已见到的新版本（如 Cogeneration、ME-POIs v3）没有假装复核。最新修订差异不属于本有界收口声明。

## 关键判断

- AI-Propeller §5.4 明确报告 Search 相对生产 Ext-TSP 提升 0.23%；已保留生产证据，不因摘要缺少 A/B 拒绝。但正文未披露流量分组/规模或明确全流量，不能标严格 A/B/全流量门槛通过。
- GroundSet 为 8×A100×72h；PointDiT-B 仅论文训练阶段折算 352 H100 GPUh；Live-kBench 单 patch 至少 30 分钟。高成本依据是原文配置，不是本轮本地测量。
- VIPE 一个实验生成 18,160 条视频；按论文当时 $3.20/条约 $58,112，未查当前价格，也未进行付费调用。
- AMS 原文 10–40 秒扫描不含模型取得/加载；它属于可负担核心候选，不把整个 14 配置权重矩阵当作已复现。
- TFRBench 的 gold 反馈用于 trace/benchmark 构建；不得将读取未来真值优化的循环宣传为无泄露预测 Agent。mild 的 synthetic expert 与真实 routing 也分开标记。
- 2606.00369 的历史审计日期 2026-07-10 被本轮 arXiv v1 页头纠正为 **2026-05-29**。

## 逐项结论

### 2601.00372 · LLM-Powered Analysis of IoT User Reviews: Tracking and Ranking Security and Privacy Concerns

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2601.00372v1)；v1 日期 2026-01-01；作者/机构角色：North Carolina State University。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：GPT-3.5-Turbo两阶段SFT：CRC分类/解释/低层分类，TM主题映射，动态few-shot；属于IoT评论安全隐私主题实证，不提出通用推荐/Agent/基础模型机制。
- 实验/资源：91,149条无标注Amazon评论；2,454条人工转换标签；SFT 3 epochs，Linux16GB RAM与RTX3070M用于BERT embedding；正文结果是离线分类/主题统计。
- 公开代码：正文给出匿名IoT-Products-SecurityAndPrivacy仓库，明确产品信息/数据；未核实算法训练代码已发布。 [主源链接](https://anonymous.4open.science/r/IoT-Products-SecurityAndPrivacy-5F5D/README.md)；状态 `project_or_data_link_only_no_algorithm_code_confirmed`。
- 成本决定：不启动91K评论批量API与SFT；本项scope终态，不以成本代替方法审查。
- 生产证据：未报告真实生产A/B或全流量；离线Amazon评论不是线上实验。
- 实际读取：§3 Methodology；§4 Results导航/摘要指标；正文作者/日期；浏览源行定位 L119-L145。[公开摘要回执](evidence/google39/2601.00372.json)，SHA-256 `144665c0eee9b8eca2f7554bc52ef4d8a4de6c1a76d08feabc8e7549a8ce0f3e`。

### 2601.19066 · Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2601.19066v1)；v1 日期 2026-01-27；作者/机构角色：Google。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：Passerine中TDD/TLD/Freeform联合生成fix+BRT；BRT在原bug失败、修后通过验证；test-aware patch selection结合reviewer过滤、归一化分组及多数选择。
- 实验/资源：120个Google私有bug、六语言、5配置，每bug20条trajectory、每条25步，Gemini2.5 Pro；内部部署与人工代码审查被描述，但对照是离线重放，不是量化生产A/B。
- 公开代码：未在已读正文找到作者公开Passerine/私有bug代码。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：完整5×120×20=12,000轨迹、最多300,000 agent步及私有monorepo测试，明确超出单卡/Mac短验预算；估算基于步数上界，不是实测。小规模真实patch/BRT选择核心可负担，未获本轮实施授权。
- 生产证据：正文明确Passerine内部部署；未找到本方法的量化真实生产A/B或明确全流量采纳。
- 实际读取：§2.1 Our Agentic APR System；§3 Dynamic Cogeneration；§4.2配置；§5结果摘要；浏览源行定位 L88-L139;L256;L329。[公开摘要回执](evidence/google39/2601.19066.json)，SHA-256 `a3556e9374f3ded4cf6da3efccb95d34c58491866202094acc694d6d4df316d5`。

### 2601.21149 · Mobility-Embedded POIs: Learning What a Place Is and How It’s Used from Human Movement

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_private_data`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2601.21149v1)；v1 日期 2026-01-29；作者/机构角色：University of Southern California。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：visit Transformer与POI原型对比学习；多尺度Gaussian anchor分布迁移＋KL，anchor直接监督与text cosine alignment；冻结表示后轻量头。
- 实验/资源：Veraset LA一年/Houston20天私有移动数据；53.7M参数、4层8头d512；20 epoch预训练、100 epoch微调早停，V100 16GB；5项地图属性probe。
- 公开代码：已读正文/附录未找到作者训练实现仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：模型单卡可放下；原数据为付费/私有移动轨迹与Safegraph，原尺度训练与多个embedding API成本未量化，不能承诺完整复现。可负担有界机制候选，未实施；不把V100使用本身视为高成本证明。
- 生产证据：5个离线地图任务，不是线上A/B；未找到明确生产全流量。
- 实际读取：§3.3-3.6；§4.1；Appendix A.1.4-A.3；浏览源行定位 L125-L177;L406-L418。[公开摘要回执](evidence/google39/2601.21149.json)，SHA-256 `bf0a285cb148b3b6ea24f6da6d5d7f25e595293085374a35faad4c1dea9ee2a4`。

### 2602.02164 · Co-RedTeam: Orchestrated Security Discovery and Exploitation with LLM Agents

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.02164v1)；v1 日期 2026-02-02；作者/机构角色：Michigan State University / Google collaboration。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：多Agent漏洞发现与隔离Docker执行：Planner/Validation/Execution/Evaluation循环，三层pattern/strategy/technical memory；代码上下文与真实执行反馈。
- 实验/资源：CyBench/BountyBench/CyberGym多模型、多对照及迭代消融；Gemini系列与GPT5-mini/o4-mini/Claude4.5/open20B/32B；正文报告安全benchmark而非线上用户A/B。
- 公开代码：已读正文未找到作者Co-RedTeam实现仓库；OpenHands链接是baseline。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：三benchmark×多backbone×多baseline长执行轨迹＋独立Docker目标环境，需付费API/20B-32B模型与多轮发现/利用；完整多臂成本明显超出短单卡预算，按配置推断未实测。
- 生产证据：仅隔离安全评测，无生产A/B或全流量证据。
- 实际读取：§3.2-3.4；§4 Experiments；Appendix A.5/C；浏览源行定位 L104-L131;L329-L370。[公开摘要回执](evidence/google39/2602.02164.json)，SHA-256 `1fd8770e975ee9a8bcbdfacb2bae88cbd49113399f32f27ec29f091749ef735e`。

### 2602.02690 · Outrunning LLM Cutoffs: A Live Kernel Crash Resolution Benchmark for All,

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.02690v1)；v1 日期 2026-02-02；作者/机构角色：Columbia University。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：Live-kBench按时间持续采集内核bug；kEnv解耦agent与编译/执行环境，Crash Resolution Feedback与patch-equivalence judge。
- 实验/资源：534 Linux bugs；3 scaffolds、Gemini3Pro/Flash与ClaudeOpus4.5；judge每patch9票；单内核补丁编译测试至少30分钟。
- 公开代码：正文未找到本框架的具名作者仓库；公开dashboard/benchmark声明不等于源码已验证。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：仅534 bug一次30分钟即≥267串行小时，尚未含多agent/模型/重复验证；这是正文单例下界外推而非测量。内核VM与云执行也非Mac/单A100替代可忠实覆盖。
- 生产证据：公开离线benchmark，不是生产A/B。
- 实际读取：§3 kEnv导航；§4 Live-kBench；§5.1；引言成本；浏览源行定位 L45-L59;L140-L190。[公开摘要回执](evidence/google39/2602.02690.json)，SHA-256 `4e68b191ee36a17f566160667907aa2a2afc368109dd61a83100d4823440b1b5`。

### 2602.06276 · Statistical Learning from Attribution Sets

Google 官方列表短名为 “Learning from Attribution Sets”；主标题以原文为准。

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.06276v1)；v1 日期 2026-02-06；作者/机构角色：Google Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：由匿名attribution sets和先验构造无偏population-loss estimator，再ERM；与随机分配/最大先验伪标签baseline比较。
- 实验/资源：MNIST、CIFAR10、Higgs；MLP/CNN；k=2^0…2^8；10学习率×10重复，MNIST200epoch、其余100epoch。正文是初步离线模拟归因集合实验。
- 公开代码：已读正文未发现作者实现仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：完整网格约(9+9+8)×3×10×10=7,800次训练，100–200epoch，远超单卡短运行；核心loss小数据CPU机制可负担，未授权本轮实现。
- 生产证据：无真实广告生产A/B或全流量；不能把行业启发式baseline当线上对照。
- 实际读取：§3-4章节导航；§5 Experiments；浏览源行定位 L235-L253。[公开摘要回执](evidence/google39/2602.06276.json)，SHA-256 `dde635f3f538fead75f4540ef5ac3c6605c8ce64640f5bfeb333609bec728354`。

### 2602.07266 · ADCanvas: Accessible and Conversational Audio Description Authoring for Blind and Low Vision Creators

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.07266v1)；v1 日期 2026-02-06；作者/机构角色：Carnegie Mellon University / Google Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：ADCanvas屏幕阅读器/键盘WebVTT编辑器，视频问答与音频描述脚本协作界面；贡献是无障碍交互设计与用户研究，不是独立可比较的Agent算法。
- 实验/资源：12名盲人/低视力创作者的形成性authoring study；三个视频任务，质性观察与可用性反馈。
- 公开代码：已读方法/用户研究未核到作者公开系统代码。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：scope终态；API原型可编写不等于本论文用户研究能在单卡自动复现；不安排受试者招募。
- 生产证据：小样本用户研究不是生产A/B或全流量。
- 实际读取：§3.2 Design Rationale；§3.3技术实现定位；§4用户研究任务/流程；浏览源行定位 L227-L247;L273;L316-L328。[公开摘要回执](evidence/google39/2602.07266.json)，SHA-256 `48461145d250e77c956113131a1275558986abd7a9585b4d06ca2b053fd7f108`。

### 2602.07918 · Causal Armor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.07918v1)；v1 日期 2026-02-08；作者/机构角色：Seoul National University / Google collaboration。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：privileged action处LOO因果消融，比较用户与不可信段落影响，触发选择性sanitization；清除注入后assistant CoT并重新生成action。
- 实验/资源：AgentDojo1.2.2四环境/三攻击template与DoomArena TauBench115场景×5seed；VertexAI多backbone/sanitizer，原环境8×A100。
- 公开代码：已读正文未核到作者CausalArmor仓库；AgentDojo链接为benchmark而非作者实现。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：原文8×A100与多模型/攻击/seed完整矩阵成本过高；不尝试下载或启动。LOO/masking有界组件可单卡/CPU模型接入，未在本轮批准实施。
- 生产证据：隔离Agent安全评测，未报告生产A/B或全流量。
- 实际读取：§3-4机制导航；Algorithm 1；Appendix C/D.1；浏览源行定位 L545-L608;L632-L634。[公开摘要回执](evidence/google39/2602.07918.json)，SHA-256 `5eca3db81e91f363b5eb4da5a10247f56796693890f579788561287c00bb17f6`。

### 2602.12481 · Online Advertising with Spatial Interactions

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.12481v1)；v1 日期 2026-02-12；作者/机构角色：Google Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：广告slot建模为metric points；nearest-neighbor外部性转grouped pseudo-disk、LP rounding得到18近似并论证truthful；另有简单log近似与2D PTAS。
- 实验/资源：理论算法与证明；正文目录至hardness/附录，无实验章，全文检索experiment无结果；不是生产广告实验。
- 公开代码：已读原文未发现作者代码链接。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：小规模LP/几何实例CPU可负担；无必须大模型/数据；未在本轮批准实现，不用缺A/B否认理论算法。
- 生产证据：未报告生产A/B或全流量；理论广告机制不满足工业上线证据门槛。
- 实际读取：§2.1-2.3；Algorithm简单slot选择；全文章节/experiment检索；浏览源行定位 L178-L246;L308-L354。[公开摘要回执](evidence/google39/2602.12481.json)，SHA-256 `205f87ef58138591d91b3919a3d20e4d9c6d8478ae81ff64fa24efd18b51315c`。

### 2602.16938 · ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.16938v1)；v1 日期 2026-02-18；作者/机构角色：Google。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：ConvApparel好/坏recommender采集数据，PLSA行为统计、训练discriminator的HLS与跨策略counterfactual validation；Prompt/ICL(k3)/SFT模拟器。
- 实验/资源：4,146真人对话＋3,549模拟对话训练Gemini2.5FlashLite discriminator；各simulator生成300好＋300坏对话；90年代Turing类比不是生产证据；KS/MWU检验及HLS显示realism gap。
- 公开代码：已读正文未找到作者公开代码仓库；数据发布声明不自动等于代码。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：有界统计/validation框架可负担；完整真人数据采集、多个GeminiSFT与数千多轮rollout不在单卡短预算，原完整实验不复现。
- 生产证据：受试者交互采集好/坏系统并非生产真实流量A/B或明确全流量。
- 实际读取：§4-6；§6.1 discriminator配置；§6.2结果；浏览源行定位 L120-L153;L169-L202。[公开摘要回执](evidence/google39/2602.16938.json)，SHA-256 `9c5a79260f66684ce72cb66467b78de5b39b3b1416de333862dbc41d3853b9c7`。

### 2602.17554 · A Theoretical Framework for Modular Learning of Robust Generative Models

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_implemented`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2602.17554v1)；v1 日期 2026-02-19；作者/机构角色：Google Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：normalized robust gate最小化最坏mixture KL；stochastic primal-dual训练，SIR/rejection sampling与cached-logit结构蒸馏causal router；不是普通expert均值。
- 实验/资源：synthetic vocab100/seq10、1层2头ff32、embedding6/8/16/20；expert/baseline/gate800步，5重复；结构蒸馏5K序列。已读部分可明确CPU小机制可行。
- 公开代码：已读正文未发现作者代码仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：正文小型Transformer实验可在Mac/单卡负担；不因为标题涉及LLM而判高成本；本轮未批准实施。真实数据§8.4-8.5尚未逐段审读，不据此声称完整实验复现可负担。
- 生产证据：已读为synthetic/离线建模，无生产A/B或全流量证据。
- 实际读取：§7.3 Algorithm5；§8.1-8.3；浏览源行定位 L827-L915。[公开摘要回执](evidence/google39/2602.17554.json)，SHA-256 `eef22aa59cc164eccd4f7baf425753daa5c87bafa48c74103d4a94d33b269d03`。

### 2603.01293 · Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.01293v1)；v1 日期 2026-03-01；作者/机构角色：USC / Google Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：线性回归in-context weight预测理论：pretrain covariance与SFT/OS数据分配；OS是outcome-supervised regression，明确不是完整policy-gradient RL。
- 实验/资源：LSA d100/130epochs；GPT2架构9.5M、12层8头d256、batch64，SFT100步/OS12K步，10重复；synthetic covariance shift。
- 公开代码：已读正文未发现作者代码。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：LSA核心CPU可负担；完整GPT2×多B/n/k×10run×12K OS步预计长训练，按网格规模推断超短预算，不启动；未在本轮批准LSA组件。
- 生产证据：synthetic理论验证，无生产A/B或全流量。
- 实际读取：§1任务/OS边界；§8 Experiments；浏览源行定位 L59-L61;L275-L317。[公开摘要回执](evidence/google39/2603.01293.json)，SHA-256 `b8065a6fd16e805d23e3de4352dc184ad3b6ba1b031fc892f4494946a33bc89c`。

### 2603.06981 · Diffusion Controller: Framework, Algorithms and Parameterization

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.06981v1)；v1 日期 2026-03-07；作者/机构角色：CMU / Google Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：DiffCon将reverse diffusion看作LS-MDP控制：f-divergence regularized PG/PPO与reward-weighted regression；冻结backbone+暴露中间输出的轻量side control score修正。
- 实验/资源：SD1.4，5种参数化×SFT/RWL/PPO；side12M，LoRA17M；SFT1000/RWL2000/PPO2400步；HPS/CLIP/PickScore及人工评测。
- 公开代码：已读正文未核到作者代码仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：完整15训练臂、SD1.4与多个reward模型/图像生成评测及数千步PPO，按配置预计多小时以上，不在单A100/A30短预算；非本地测量。
- 生产证据：离线图像偏好比较，不是生产A/B。
- 实际读取：§1模型定义；§5.1-5.2配置及Table1；浏览源行定位 L77-L81;L319-L354。[公开摘要回执](evidence/google39/2603.06981.json)，SHA-256 `225d3c64ba529e58ca3ebbd26192ef238252266dcfd8ad17198f92ceb70268e9`。

### 2603.10465 · MoXaRt: Audio-Visual Object-Guided Sound Interaction for XR

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.10465v1)；v1 日期 2026-03-11；作者/机构角色：Google。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：MoXaRt XR音频：AudioScopeV2粗分离、视觉人脸/乐器anchors、分支refinement与teacher-student distillation；贡献偏XR声学交互系统。
- 实验/资源：30条一分钟混音录制与22人user study；视觉3.2M/33M、粗音6M、speech9M/music7M，约2秒交互时延。
- 公开代码：已读正文未核到作者完整系统/蒸馏代码。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：scope终态，不启动YFCC100M预训练、多专模teacher distillation或受试者研究。
- 生产证据：技术评测/受试者study，不是生产A/B。
- 实际读取：§3.2.1-3.2.4；§5/6技术与用户研究摘要；浏览源行定位 L187-L228;L93-L95。[公开摘要回执](evidence/google39/2603.10465.json)，SHA-256 `8101409b163ea7e86c321094f2ab2d0606f66f42ebfb15ba6652bed06f1b8772`。

### 2603.14609 · GroundSet: A Cadastral-Grounded Dataset for Spatial Understanding with Vector Data

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.14609v1)；v1 日期 2026-03-15；作者/机构角色：官方Google来源，原文作者机构需以源页面为准。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：GroundSet将地籍vector对象与航空影像对齐，自动生成spatial理解任务；vanilla VLM LoRA作为数据贡献baseline，无额外空间网络。
- 实验/资源：85,864km²/20行政区、20cm影像；多VLM在caption/VQA/classification/detection/REC/segmentation上比较；1 epoch LoRA用8×A100约72h。
- 公开代码：已读原文未找到作者实现仓库链接。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：论文已测8×A100×72h=576 GPUh，仅主训练就远超1×A100/A30预算；不下载遥感语料或模型。
- 生产证据：离线遥感benchmark，无生产A/B。
- 实际读取：§3数据构建；§4.2-4.3；浏览源行定位 L93;L221-L238。[公开摘要回执](evidence/google39/2603.14609.json)，SHA-256 `0028b9f91234a8ecab28b888a0e14cd2afcd0793e3d6b2057f168a6e182022b7`。

### 2603.14769 · POLCA: Stochastic Generative Optimization with LLM

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.14769v1)；v1 日期 2026-03-16；作者/机构角色：University of Wisconsin-Madison。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：POLCA优先队列追踪候选评价历史、epsilon-Net embedding保持多样性、LLM Summarizer聚合局部历史；按噪声分配探索/利用，非简单evolution标签。
- 实验/资源：tau-bench/HotpotQA/VeriBench/KernelBench；Veri41题每题最多50 compiler calls×3run×多baseline；Kernel16题、Claude3.7与Gemini embedding。
- 公开代码：作者论文明确开源，已核论文链接到rlx-lab/POLCA；仓库运行要求尚未下载/执行。 [主源链接](https://github.com/rlx-lab/POLCA)；状态 `released_primary_repository_reachable`。
- 成本决定：完整多benchmark多baseline×3/6seed、每题50迭代与付费LLM/API的搜索矩阵成本过高；epsilon-Net/队列有界core可负担，未批准本轮实现。
- 生产证据：离线优化任务，无生产A/B或全流量。
- 实际读取：§1机制；Appendix D VeriBench/KernelBench配置与预算；浏览源行定位 L99-L106;L725-L745;L769-L775。[公开摘要回执](evidence/google39/2603.14769.json)，SHA-256 `936c7c6cc3242b8bf6b04e8aaf2402390e960601bed9d535049e424f3017e4d9`。

### 2603.24591 · Vibe Coding XR: Accelerating AI + XR Prototyping with XR Blocks and Gemini

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.24591v1)；v1 日期 2026-03-25；作者/机构角色：Google XR Labs。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：XR Blocks将WebXR perception/interaction封装semantic primitives，Gemini系统prompt＋templates生成可运行XR脚本；重点是XR开发框架/交互工作流。
- 实验/资源：VCXR60 pilot技术评测，桌面模拟和Android XR headset场景；非通用agent学习/优化算法的受控能力比较。
- 公开代码：作者官方google/xrblocks链接明确公开。 [主源链接](https://github.com/google/xrblocks)；状态 `released_primary_repository_reachable`。
- 成本决定：scope终态；不因API演示可用就另开XR实现，也不需大模型/训练来关闭审查。
- 生产证据：pilot技术评测不是生产A/B或全流量。
- 实际读取：§1/§3框架与workflow；§4 Preliminary Technical Evaluation定位；浏览源行定位 L55-L85。[公开摘要回执](evidence/google39/2603.24591.json)，SHA-256 `b8e9b1c9aea42b8ee8efd861663ba85b2e1c96caa851943087fbc31d4f73fc40`。

### 2603.28896 · Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.28896v1)；v1 日期 2026-03-30；作者/机构角色：Yale University / Google XR。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：冻结VGGT/pi3/MapAnything，用calibration tokens适配fisheye；camera-type linear classifier控制attention mask保持perspective兼容，支持SL/SSL。
- 实验/资源：ScanNet++/ADT/KITTI360多几何任务；每层K8 tokens、前12层除外；40K步AdamW，gradient checkpointing；4×RTX A6000 48GiB。
- 公开代码：已读正文未找到作者Fisheye3R代码仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：三个大3Dbackbone×多适配配置×40K步、原文4×48GiB GPU与多数据集图像，完整实验成本过高；不以1分钟CPU相机分类器冒充整个适配算法。
- 生产证据：离线3D评测，无生产A/B。
- 实际读取：§3 masked calibration；训练/评估/硬件配置；浏览源行定位 L142-L149;L332-L347。[公开摘要回执](evidence/google39/2603.28896.json)，SHA-256 `c8ba18b1d695e0193276c207d941d884308b370b35bd65f2cae18d53038daabe`。

### 2603.29470 · AI-Simulated Expert Panels for Socio-Technical Scenarios and Decision Guidance

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.29470v1)；v1 日期 2026-03-31；作者/机构角色：HTML作者机构不可见，未独立确认。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：单Gemini模拟能源专家，CIB cross-impact stochastic pathways＋MCDA stakeholder选择＋情景量化；德国能源转型proof-of-concept，不是agent能力benchmark。
- 实验/资源：5模拟专家、15×3 descriptor states；方法承认CIB一致性不能保证叙事合理；保留超过250K词讨论但缺真实专家对照能力实验。
- 公开代码：已读正文仅accompanying resources/transcripts声明，未核到作者算法代码；Google机构身份在HTML未显示，保留原官方源归属，不声称第一作者Google。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：scope终态；无需把250K词模拟panel重复为能力复现；不以高成本掩盖来源身份未确认。
- 生产证据：政策scenario模拟，非生产A/B。
- 实际读取：§2 Methods；§3.1-3.3 Results；浏览源行定位 L69-L77;L138-L170。[公开摘要回执](evidence/google39/2603.29470.json)，SHA-256 `a0791bb14f867ae57b07c93c835bf67dd3cc3720924dd8c9f9dbbad749fc9e4f`。

### 2603.29791 · Reasoning-Driven Synthetic Data Generation and Evaluation

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2603.29791v1)；v1 日期 2026-03-31；作者/机构角色：EPFL / Google internship。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：Simula seedless taxonomy构造、局部meta-prompt/complexification、全局层次节点采样、double critic rejection与calibrated complexity/Elo；需真实M3生成/批判。
- 实验/资源：Gemini2.5Flash；CTI/法律/GSM8K/GlobalMMLU多语言，每数据集512K唯一点、5系统版本；13gram/Jaccard decontamination；BS=N5评分。
- 公开代码：已读正文未发现作者实现仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：每任务512K样本×多版本＋多次critic/复杂度与下游训练，付费多模态API数百万调用量级风险；完整实验成本过高。小有界taxonomy/critic核心可负担，未在本轮批准实现。
- 生产证据：离线合成数据/下游评测，未报告生产A/B。
- 实际读取：§3 Experimental Setup；§3.2数据规模；Appendix E成本示例；浏览源行定位 L133-L160;L674-L685。[公开摘要回执](evidence/google39/2603.29791.json)，SHA-256 `31797910eae4658e36df7db22237fecb2dc4b8ee39d5f0bb22fb719906ef0f8c`。

### 2604.05364 · TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2604.05364v1)；v1 日期 2026-04-07；作者/机构角色：University of Kentucky / Google collaboration。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：TFRBench reason/search/forecast/verify/summary多agent生成grounded traces，最多K3循环，按MASE与一致性选trace；这是有标签benchmark构建，不可把gold反馈循环当无泄露预测Agent。
- 实验/资源：10数据集/5领域，多Gemini/Claude预测和LLMjudge对比；候选生成验证访问未来ground truth，forecast本身不读；领域外部事件检索包含未来horizon。
- 公开代码：作者benchmark主页明确给出；未在已读正文核到独立算法源码发布。 [主源链接](https://tfrbench.github.io/)；状态 `project_or_data_link_only_no_algorithm_code_confirmed`。
- 成本决定：完整10数据集×多backbone×多候选/3loop＋检索/judge的API矩阵昂贵；小规模benchmark协议与评分接口可负担，未实施。标签隔离必须明确。
- 生产证据：离线forecasting benchmark，无生产A/B。
- 实际读取：§3 Algorithm1/6steps；§4结果表片段；浏览源行定位 L165-L224;L616-L672。[公开摘要回执](evidence/google39/2604.05364.json)，SHA-256 `573ddf1fa3c2c4aa17ea4776f708c999a3ac96578e5c952f4b709caa48db9e57`。

### 2604.09803 · MAGE: Modality-Agnostic Music Generation and Editing

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2604.09803v1)；v1 日期 2026-04-10；作者/机构角色：Google (internship)。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：MAGE Controlled Multimodal FluxFormer latent flow matching、audio-visual nexus时序对齐、乘性cross-gated modulation与dynamic modality masking；统一生成/mixture编辑。
- 实验/资源：MUSIC benchmark；AdamW1e-4，1K epochs且每epoch数据重复5次；70%mixture、20%zero-mixture、10%CFG fallback；Euler2eval与MixWavCodec。
- 公开代码：已读正文未发现作者实现仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：1000epoch×5数据重复的音视频flow训练及多评测臂预计多小时/天，原模型/codec多资源，完整实验成本过高；未测量、不下载。
- 生产证据：离线音乐评测，无生产A/B。
- 实际读取：Appendix A模型/训练/推理；评测段定位；浏览源行定位 L315-L343。[公开摘要回执](evidence/google39/2604.09803.json)，SHA-256 `dbf1e594ba8530befc001b170937bb1667df54a0c1e1ddda516dfbcaeccebfd7`。

### 2604.20329 · Image Generators are Generalist Vision Learners

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2604.20329v1)；v1 日期 2026-04-22；作者/机构角色：Google / Google DeepMind。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：Vision Banana对NanoBananaPro instruction-tuning，将segmentation/depth/normals编码为可逆/可解析RGB图像输出；保留原generation数据混合。
- 实验/资源：多2D/3D公开benchmark与生成editing benchmark；depth仅synthetic训练；基础NanoBananaPro原训练数据/可训练checkpoint非公开。
- 公开代码：项目主页公开；未在已读正文核到作者可训练代码、NBP权重或原始training mix。 [主源链接](https://vision-banana.github.io/)；状态 `project_or_data_link_only_no_algorithm_code_confirmed`。
- 成本决定：核心要求闭源NBP训练接口与原始generation corpus，单卡无法取得相同训练链路；成本/资源不可获得，不用RGB编码小函数冒充generalist训练。
- 生产证据：离线zero-shot视觉/生成评测，无生产A/B。
- 实际读取：§2 Method；Table1；§3.2 metric depth编码/训练协议；浏览源行定位 L61-L85;L219-L244。[公开摘要回执](evidence/google39/2604.20329.json)，SHA-256 `832a2b2e678fbed6c8a46ed3980d80d94c0d1976f3b8ffb46f152b84c7f0084d`。

### 2604.23099 · ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2604.23099v1)；v1 日期 2026-04-25；作者/机构角色：Google DeepMind。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：ProEval预训练GP surrogate，Bayesian quadrature估计总体性能与superlevel set failure采样；TPF/RPF/SF迁移；topic UCB1＋LLM failure pattern转置。
- 实验/资源：16LLM/VLM×reasoning/knowledge/safety/text/image多benchmark；failure discovery100迭代；GP使用历史外部模型score，目标test gold不能给evaluated agent。
- 公开代码：作者明确开源google-deepmind/proeval。 [主源链接](https://github.com/google-deepmind/proeval)；状态 `released_primary_repository_reachable`。
- 成本决定：现有历史score上的GP/BQ有界core可CPU负担；完整16模型多benchmark与LLM query synthesis昂贵，不本轮重跑；未批准实现。
- 生产证据：离线评价方法，无生产A/B或全流量。
- 实际读取：§2 Algorithm2；§3.1数据/模型/feature；Table5；浏览源行定位 L274-L336;L452-L462。[公开摘要回执](evidence/google39/2604.23099.json)，SHA-256 `5704d72b8d22dedb0b0411bc1ed476c103825a93ca54939f2ccec8e8e3907611`。

### 2604.27723 · Optimized Deferral for Imbalanced Settings

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_implemented`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2604.27723v1)；v1 日期 2026-04-30；作者/机构角色：Google Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：mild把imbalanced expert deferral转为input-expert cost-sensitive分类，margin surrogate与一致性界；利用真实expert输出训练router，不能让inference读取标签。
- 实验/资源：CIFAR人为synthetic expert覆盖比例7/2/1等；真实LLM routing有Qwen2.5 0.5B/1.5B等；实验区别synthetic oracle专家与真实模型。
- 公开代码：已读原文未发现作者代码仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：loss/router有界CPU机制可负担；不必下载多个LLM就可审查，但不得把synthetic gold expert诊断当真实routing能力；本轮未批准实施。
- 生产证据：离线classification/routing，无生产A/B或全流量。
- 实际读取：§5.3 Deferral loss；Appendix C.1/C.2；浏览源行定位 L306-L326;L536-L572。[公开摘要回执](evidence/google39/2604.27723.json)，SHA-256 `69f6576ef83d97e8e782bee058a70029f9baa72f9c93b9d18da64a7b1f8c7a0c`。

### 2605.26340 · Scientist-One: Verifiable Autonomous Research via Chain-of-Evidence

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2605.26340v1)；v1 日期 2026-05-25；作者/机构角色：Google Cloud AI Research。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：ScientistOne CoE将claim连接code/evaluator/bibliography，I1 score复算、I2 spec违规、I3引文查询、I4 method-code alignment与CPR；全自动research pipeline维护provenance。
- 实验/资源：ADRS五系统研究任务×五research系统×3run，Gemini3.1Pro，最多20 solver迭代与2小时code窗口；evaluator5次复算、judges多数投票。
- 公开代码：已读正文未核到ScientistOne作者独立发布仓库；baseline开源不等于其开源。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：5×5×3=75完整research runs，单run上限2小时且可能重试3次；多轮500篇pool/100notes的外部研究；完整实验明显高成本。有界provenance/审计接口可负担但本轮未授权实现。
- 生产证据：离线ADRS，不是生产A/B。
- 实际读取：§5 Integrity Audit；§6 Experiments；Appendix paper investigation；浏览源行定位 L200-L246;L463-L471。[公开摘要回执](evidence/google39/2605.26340.json)，SHA-256 `5d965c86619f27647d82ee82b0170bb417e9b1443a13fe40eba517987abb9415`。

### 2605.29729 · Realistic honeypot evaluations for scheming propensity

- 处置：deferred：完整实验不复现；`not_reproduced_resource_unavailable`。完整实验另轴：`not_reproduced_private_environment`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2605.29729v1)；v1 日期 2026-05-28；作者/机构角色：Google DeepMind。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：真实内部alignment代码honeypots，code review与agentic coding分别设sabotage机会，agency/hidden goal提示调节，检测思考/行为trigger；是评价框架非训练改进。
- 实验/资源：code review12honeypot+1baseline/10commit chain；coding11honeypot+2baseline、Antigravity Google code副本；多Gemini模型与提示变体。
- 公开代码：Google内部alignment研究代码不公开；已读正文未找到对应可运行公开环境/实现。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：原内部代码环境不可获得，26场景×多model/prompt长coding轨迹与人工/CoT审查成本不明且显著；按成本gate不尝试外部昂贵近似，保留资源不可用原因。
- 生产证据：作者明确deployment-like，不是in-deployment生产A/B；未触发也不构成安全证明。
- 实际读取：§3 Methods；§3.1 Model prompting；引言部署边界；浏览源行定位 L99-L140;L48-L58。[公开摘要回执](evidence/google39/2605.29729.json)，SHA-256 `845d4f3e64430e54cbfda1c8adde5b03e2a179a013af3497530fcba52aad7505`。

### 2605.30174 · LiveSVG: Zero-Shot SVG Animation via Video Generation

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2605.30174v1)；v1 日期 2026-05-28；作者/机构角色：Google / Hebrew University。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：LiveSVG先视频生成，再用differentiable rasterizer拟合原SVG：group homography＋Bezier offsets，sphere-packing recoloring消歧；无骨骼先验。
- 实验/资源：AniClipart/ChallengeSVG，Veo3.1/Wan/LTX三video variants；每SVG10–20候选视频，Gemini3.1Pro两阶段rerank；GPU优化每成功样本5.2分钟，含AMT偏好study。
- 公开代码：项目主页公开；已读正文未核到作者公开实现仓库。 [主源链接](https://levymsn.github.io/LiveSVG)；状态 `project_or_data_link_only_no_algorithm_code_confirmed`。
- 成本决定：原完整benchmark×10–20生成视频/每样本＋Gemini rerank＋多baseline拟合/人工study高成本；5.2分钟仅拟合成功样本不含视频生成，不能据此声称完整路径便宜。
- 生产证据：AMT pairwise A/B是离线人工偏好，非真实生产流量A/B。
- 实际读取：§3机制；Appendix F implementation；运行效率与human study；浏览源行定位 L87-L92;L404;L440-L475。[公开摘要回执](evidence/google39/2605.30174.json)，SHA-256 `f819c31e580dbb974239bb2e82076d89ba07c4829462226656c91b573821c351`。

### 2605.30322 · Gram: Assessing sabotage propensities via automated alignment auditing

- 处置：deferred：完整实验不复现；`not_reproduced_resource_unavailable`。完整实验另轴：`not_reproduced_private_evaluation`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2605.30322v1)；v1 日期 2026-05-28；作者/机构角色：Google DeepMind。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：Gram对Petri auditor约束减少leading，17 sabotage seed scenarios；investigator将动态trajectory转静态环境、做causal interventions，区分overeagerness/roleplay。
- 实验/资源：Gemini2.5Pro/3.0Pro/3.1Pro；17scenarios仅4公开、13private heldout；LLMjudge与人工复核，原始2–3%sabotage不能泛化真实部署率。
- 公开代码：已读正文未找到Gram完整公开实现；13/17 seed明确私有，不应补造。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：完整动态auditor×target多模型/多提示/多trajectory＋人工审查，13私有场景不可获得；成本与资源不确定，按gate不启动昂贵probe。
- 生产证据：模拟部署前审计，不是生产真实流量A/B。
- 实际读取：§2.1-2.2；§1 evaluation边界；浏览源行定位 L74-L139。[公开摘要回执](evidence/google39/2605.30322.json)，SHA-256 `c3cd1ca60b5cd69dd32699f0e65337bc17df1b3c8a37d6c558e57914378156f0`。

### 2606.00131 · AI-PROPELLER: Warehouse-Scale Inter-Procedural Code Layout Optimization with AlphaEvolve

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2606.00131v1)；v1 日期 2026-05-28；作者/机构角色：Google。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：AI-Propeller Magellan让AlphaEvolve修改Propeller interprocedural code-layout heuristic，再Vizier调compiler flags；每candidate实际编译/执行硬件counter而非静态代理。
- 实验/资源：Clang100 modules训练12AlphaEvolve迭代/1200Vizier trials/2.7天，每binary10次；48cores96GB受控Xeon；Clang/LevelDB/Redis/Search；Search单独重训。
- 公开代码：已读正文未核到AI-Propeller/Magellan完整公开代码；Propeller/LLVM具名上游不等于作者新policy全套已发布。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：原训练2.7天，1200trials×每binary10次、重编译Clang及私有Search大二进制；单A100/A30不替代所需受控CPU与内部workload，完整实验高成本。
- 生产证据：§5.4明确相对deployed Ext-TSP生产Search提升0.23%；但未披露流量分组/规模或明确全流量，不标严格A/B/全流量已满足。
- 实际读取：§4方法；§5训练/评测；§5.4 Warehouse Scale；浏览源行定位 L88-L115;L124-L156。[公开摘要回执](evidence/google39/2606.00131.json)，SHA-256 `08a3e83c916e8107808c35f0df816ffa145cf299a7b50003e30c40a6529499f6`。

### 2606.00369 · Quantifying the Salience of Geo-Cultural Values for Pluralistic Safety Alignment

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2606.00369v1)；v1 日期 2026-05-29；作者/机构角色：Columbia University / Google DeepMind internship。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：对安全标注数据做meta-analysis，IW文化zone与demographics的multilevel logistic/linear mixed models；评价LLM rater surrogate/triage，非新的alignment训练或agent算法。
- 实验/资源：8安全数据集概览/6数据集显著性；item/rater随机效应与文化/人口固定效应；发现LLM不能可靠代替文化多样标注。
- 公开代码：已读原文方法与结果未核到作者公开代码仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：scope终态；统计分析本身可负担，不用高成本拒绝；不另开受试者/标注收集。
- 生产证据：标注/安全评价meta-analysis，无生产A/B。
- 实际读取：§4.1文化操作化；§4.2 mixed models；摘要实证范围；浏览源行定位 L156-L181;L73-L88。[公开摘要回执](evidence/google39/2606.00369.json)，SHA-256 `e4c94a79c808f4f0d536874bb36eac7ce830ebe9ba5d68508b1625a89ff4010d`。

### 2607.02515 · PointDiT: Pixel-Space Diffusion for Monocular Geometry Estimation

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2607.02515v1)；v1 日期 2026-07-02；作者/机构角色：ETH Zurich / Google。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：PointDiT从raw3D pointmap patch预测clean point map，frozenDINOv3四层features拼接条件；plainViT、velocity loss、sky球映射与rectified t0 sampling。
- 实验/资源：B223M/L771M/H1.807B；pretrain30epochs，16/16/64H100×12/21/22h；finetune64/64/128H100×2.5/7/5.5h。
- 公开代码：已读正文未核到作者公开代码仓库；不据baseline链接断言开源。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：最小B主训练192H100h＋finetune160H100h=352H100h；L784/H2112H100h；均远超单A100/A30预算，数字按论文GPUs×walltime相乘，非本地测量。
- 生产证据：离线几何评测，无生产A/B。
- 实际读取：§3.2-3.3；Appendix训练成本Table6；浏览源行定位 L137-L163;L455-L460。[公开摘要回执](evidence/google39/2607.02515.json)，SHA-256 `c9fd2f768b7e39d7ddef8e1bf57016975cb23e06b042a3c7ca28baa9922efe0f`。

### 2607.13614 · VIP-MINGLE: A Corpus for Videoconference and In-Person Multimodal Interaction in Group Language Engagement

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2607.13614v1)；v1 日期 2026-07-15；作者/机构角色：New York University / Google collaboration。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：VIP-MINGLE是跨inperson/video conference受试者配对多模态语料，speech timing/language complexity/facial features统计与interaction annotation；非新的通用模型或Agent算法。
- 实验/资源：59h/32groups/105participants；7077个10秒片段、192annotators；mixed-effects/Wilcoxon比较环境domain shift。
- 公开代码：已读原文未核到作者完整处理pipeline公开代码。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：scope终态；不重采集59h人类交互，也不以数据分析可CPU运行冒充原语料复现。
- 生产证据：受试者配对研究，非生产A/B。
- 实际读取：§2数据设计摘要；§3.1-3.3；§4 annotations；浏览源行定位 L44-L62;L94-L113。[公开摘要回执](evidence/google39/2607.13614.json)，SHA-256 `37be407ed96b5b57907daf687209446b46da9094132ece85df830a4f3b285206`。

### 2607.25537 · Visual prompt engineering for video models

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2607.25537v1)；v1 日期 2026-07-28；作者/机构角色：Google DeepMind。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：VIPE ideator生成视觉改写idea，image editor修改任务图，可选filter保持语义；freeform open-loop或ACE edits，与video test-time scaling比较。
- 实验/资源：6视觉任务；20variants、每edit best5；单实验18,160个720p/8s视频，Veo3.1；论文API成本$3.20/video与约$0.40/VIPE。
- 公开代码：项目主页公开；已读原文未核到作者执行代码。 [主源链接](https://visual-prompt-engineering.github.io/)；状态 `project_or_data_link_only_no_algorithm_code_confirmed`。
- 成本决定：仅18,160×$3.20=$58,112视频API费（按论文当时价格估算），尚未含编辑、filter、其他实验；明确高成本，未验证当前价格也未调用付费生成。
- 生产证据：离线video reasoning benchmark，非生产A/B。
- 实际读取：§4 automated VIPE配置；Appendix B预算；§5 test-time scaling；浏览源行定位 L151-L162;L177-L180;L335-L337。[公开摘要回执](evidence/google39/2607.25537.json)，SHA-256 `22c92799af3dea509393aec62c87ab209b72c7513a039cef8a115f52aff8d6e0`。

### 2608.05578 · Detecting Safety Training Modification in Language Models via Activation Analysis

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2608.05578v1)；v1 日期 2026-08-06；作者/机构角色：Google Cloud。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：AMS三个安全概念各16 contrastive pairs，扫40–80%深度activation取最大separation层，direction/sigma；Tier1阈值与Tier2 baseline cos/drift验证。
- 实验/资源：14model configs/4families；LOO threshold71%(10/14)、20JailbreakBench prompts/model；A10040GB扫描10–40秒但不含模型加载；bootstrap区间宽且部分跨PASS阈值。
- 公开代码：作者正式公开Apache2 GoogleCloudPlatform/activation-model-scanner和Zenodo归档。 [主源链接](https://github.com/GoogleCloudPlatform/activation-model-scanner)；状态 `released_primary_repository_reachable`。
- 成本决定：单已缓存3B/7B模型扫描本身低成本，无需训练；14config权重总下载较大，完整矩阵不本轮下载。可负担core候选not_implemented；不能据71%判生产安全扫描已validated。
- 生产证据：离线模型tamper检测，无生产A/B。
- 实际读取：§IV-F algorithm；Resource requirements；Data availability/摘要统计；浏览源行定位 L242-L277;L583-L602;L631-L646。[公开摘要回执](evidence/google39/2608.05578.json)，SHA-256 `724cd5f758a0b87229282126e12cddcc3f3e0116203ff551a5fbf874bf06fd53`。

### 2608.11367 · Gaze Target Estimation Anywhere with Concepts

- 处置：deferred：完整实验不复现；`not_reproduced_high_cost`。完整实验另轴：`not_reproduced_high_cost`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2608.11367v1)；v1 日期 2026-08-11；作者/机构角色：University of Illinois Urbana-Champaign / Google。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：PGE promptable subject识别与gaze统一；frozen图文encoders＋detector transformer同时localization/inframe/heatmap；120K Gaze-Co由MLLM概念生成与human verification。
- 实验/资源：119,525train samples/3公开test及私有临床OOD；25+5epochs、batch128、4×H100；L40S推理与DigiLens ARGO smartglass。
- 公开代码：作者明确公开IrohXu/GazeAnywhere。 [主源链接](https://github.com/IrohXu/GazeAnywhere)；状态 `released_primary_repository_reachable`。
- 成本决定：4H100×30epoch、多backbone/baseline与120K multimodal数据/MLLM构建，完整实验明显超单A100/A30短预算；私有临床数据不可替代作论文级结论。
- 生产证据：AR实地demo和临床OOD评价非生产A/B/全流量。
- 实际读取：§5.1 implementation；Appendix数据与model细节；浏览源行定位 L242-L246;L427-L473。[公开摘要回执](evidence/google39/2608.11367.json)，SHA-256 `4ca88f4973bfbd30b7b993cc917566f0a0e815d2f4bce90e53e0fffa25b32375`。

### 2609.01588 · Designing Proactive Thought Partners for Writing

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2609.01588v1)；v1 日期 2026-09-01；作者/机构角色：Google DeepMind collaboration。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：可配置role/timing的proactive writing thought partners，NextJS/BlockNote＋Gemini decision engine；核心贡献为technology probe交互design space。
- 实验/资源：16人一周diary/interview；FlashLite选择partner<1s，Flash suggestion约8s；作者明确此study不是产品efficacy评测。
- 公开代码：已读正文未发现作者完整probe实现仓库，附录仅prompts。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：scope终态；不重复受试者研究，不把廉价API原型冒充能力算法。
- 生产证据：探索性一周部署study非生产A/B/全流量。
- 实际读取：§3设计目标；§4.5 implementation；§5 user study；浏览源行定位 L114-L119;L189-L207。[公开摘要回执](evidence/google39/2609.01588.json)，SHA-256 `e3aa3647a99f4bc82cf95f45f189343c5fa662729ff994dc09c61ee67f770757`。

### 2609.01834 · Architecting Conversational Data Systems for Stateless LLM APIs

- 处置：scope：不纳入算法复现；`out_of_scope`。完整实验另轴：`not_applicable_scope`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2609.01834v1)；v1 日期 2026-09-01；作者/机构角色：Google官方收录；本文作者机构未另核。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：Hydration Proxy三层架构pattern：UI/secure gateway/relational ledger＋object storage；按stable prefix/full-history hydration设计context治理。
- 实验/资源：原文153行，§2架构、§3cache strategy/§4benefits后结论/参考；Evaluation检索无匹配。没有受控量化实验或具体待复现算法。
- 公开代码：已读正文未发现作者公开实现仓库。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：概念架构而非可验收论文算法；scope终态，不用成本理由。
- 生产证据：production-grade是需求措辞，无真实生产A/B/全流量量化证据。
- 实际读取：§2架构；§3 cache-aware context；结论及全文章节/Evaluation检索；浏览源行定位 L53-L124;L127-L138。[公开摘要回执](evidence/google39/2609.01834.json)，SHA-256 `2e0a42d1801fd8d1e21c610ca4cdfc8c6e8383cf90d5b1d85d5ae085a4d9de2a`。

### 2609.12464 · Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration

- 处置：accepted：候选核心未实现；`accepted_core_not_implemented_this_run`。完整实验另轴：`not_implemented`；本轮实现状态：`not_implemented`。
- 主源：[arXiv v1](https://arxiv.org/html/2609.12464v1)；v1 日期 2026-09-11；作者/机构角色：Google官方收录；本文作者机构未另核。Google共同作者可优先，不要求第一作者Google；仅官方元数据归属的条目明确保留未核作者机构边界。
- 方法：HCRG tree-sitter AST入graph、architecture skeleton缓存、拓扑顺序迁移，3hop检索；对照800char/150overlap/top5向量RAG；AST+pyflakes七结构指标。
- 实验/资源：spring-petclinic Java→Python单repo；Gemini2.5Pro T0、Spanner/Vertex1h context cache；DRQ34.8→65.9%、PCC26.7→45.5%，但cyclomatic一致性下降。无多seed/多repo泛化证据。
- 公开代码：原文链接输入benchmark repo而非作者pipeline代码；未核到HCRG实现公开。；状态 `not_found_in_reviewed_primary_sources`。
- 成本决定：小public repo的AST/拓扑检索与静态指标core可负担，付费云服务可替为同语义本地graph但须实际LLM迁移；未获本轮实施授权，未测总代价。
- 生产证据：离线代码迁移，非企业生产A/B或全流量。
- 实际读取：§4.2实验参数；§5.2指标；§6结果；浏览源行定位 L128-L175;L212-L225。[公开摘要回执](evidence/google39/2609.12464.json)，SHA-256 `1aaf750fa1321128cc804923bf9021b1da88aa8789c97f97c365279ec1151ed6`。

## 集成边界

父批次可把 39 行转换为新的 ledger 批次，但须原样保留 `accepted/not_implemented/automatic_implementation_queue=false` 与完整实验终态分轴。`accepted` 只认可具体核心候选机会，不是本轮实施授权、不自动满足工业 A/B 门槛，也不是已实现或 GPU 验证完成。

任何未发现作者代码的记录都仅表示“本轮已读主源未找到”，不能转写为作者确认未发布。源文件、失败检索、成本估算和不利结果边界均保留。
