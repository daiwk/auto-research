# 2026-10-13 GPU 验证 TODO（网络恢复后继续）

2026-10-13 用户要求网络不稳定时先停止 A100/A30 的连接、传输和新实验，保留为 TODO。
2026-10-14 用户已明确恢复使用；两类 NVIDIA GPU 的 SSH 只读检查均成功，已有实验目录仍在。
当前按固定源码/资源 SHA 核验后续跑，下面未完成项仍不因连接恢复自动验收。
本轮不因这项暂停删除失败结果、降低 GPU 门禁或宣称 19 篇全部验收完成。
源码检查点：`ccad3e679787f6f5383b8bd3dd1c7b58e7c8c5d0`；之后的文档/工具收口以分支最新提交为准。
本地已完成的核验、已修复失败点及最终检查边界见[本地收口检查点](oct13-local-closeout.md)。
续办源码包按实验绑定 `4496283a`、`34148c2e`、`6aabe57a`；当前技能/机器人/MBS 修复快照为 `0f5dca9f7f0319c6e3bb57aa578cfe26499a6e7e`。仅含公开源码与执行脚本，
不包含工作区缓存、私有数据或密钥。不覆写旧运行目录，源码修复必须先提交新快照后再运行。

## 已有真实结果

| 论文 | 已核验结果 | 不覆盖的内容 |
| --- | --- | --- |
| UxSID | A100，42/43/44，943 用户、四结构实际训练、缓存一致性 | 原工业线上收益、完整 XLong/KuaiRec；本次无稳定提升 |
| State-OPD | A100 `6aabe57a`，state/full-history-opd/state-no-expansion 各 42/43/44；九次均有两次实际更新，52 个源码文件与原始结果 SHA 独立核验 | 三臂 8 题 accuracy 前后均为 0；实际响应池/token 成本不同，非正式能力提升或原环境比较 |
| GPPO / TAPO | A100 原快照各三 seed，独立 GRPO-control 三 seed；3 rollout groups × 2 inner updates = 6 次实际 optimizer 更新 | 大规模长轨迹能力结果；8 题仅为机制诊断 |
| DoubleCat / SemiCat | A30 新核心，42/43/44，真实 40 步与 32 NFE | 原 TinyGSM/OWT 规模；onehot/DoubleCat 坍缩负结果保留 |
| OAL | A100，42/43/44，实际分组/校准及 OAL/softmax 匹配 LoRA 更新；原始结果和源码哈希核验通过 | 仅一个中间层、3 步、32-token 块；seed 44 不优于基线，非原论文全规模或效率结果 |
| NEAR / Beyond | A30，共享 bank 100 queries 各三 seed，另各一项严格 bank-disjoint 30-query 诊断；八份原始结果和源码哈希核验通过 | 官方 evaluation 实例再切分的非官方诊断；相同数据的三 seed 非独立重复；严格协议仅 2 test queries，不能合并统计 |
| CV-OPD | A100，CDL / without-CDL 各 42/43/44，六臂均有真实非零更新；24 份输出/日志/状态及固定源码归档核验通过 | 测试均值主方法 4.17%、对照 12.5%，配对 −8.33pp；采样上限相同但实际 token 成本不同，非正式能力比较 |
| ReplaySSM | A100，48 步 × 42/43/44；作者四精度内核及独立 CUDA GDN/Mamba 回放、拒绝与刷新通过 | 保留旧编译失败；透明 JIT 括号兼容层，非 native serving；随机输入没有语言模型质量或 HBM 收益结论 |

对应指标与脱敏回执均在各篇详情页。旧标准 SC GPU 结果不能替代 DoubleCat 新核心的回执。

## 剩余验证清单

全部使用固定公开 checkpoint/data revision，原始输出不可覆盖。默认 seed 为 42/43/44；
只能依据训练/validation 诊断调整训练预算，不以 test 挑方案。失败与零梯度必须保留。

| 优先序 | 论文 | 恢复后要执行的完整链路 |
| --- | --- | --- |
| 2 | SkillDreamer | 固定 checkpoint、公开 train-only GSM8K 子集；no-skills/direct/PSG+HSR+CSI 三臂实际工具执行，参考答案仅外部 scorer 可见 |
| 2 | MagicBeanStalk | 真实 teacher 分解、独立验证、effectivity、Goldilocks、非零优势 RLVR 与 seed-RLVR 对照；不合格合成不算完成 |
| 2 | SynthSelf | 实际改写、拒绝采样、Eq.6 aligner 约束、SFT 与 gold-SFT 对照；acquisition/retention 分开，不通过约束不签通过回执 |
| 2 | UPTURN | 实际失败轨迹/切点、frozen encoder、gate/position head 更新、新 user-turn 救援与匹配预算；无 rescue 信号保留失败 |
| 2 | SOAR | 先准备独立公开知识库（不是题目答案库），再跑 source-consistent / without-source-reward 两臂实际 RL |
| 2 | GRPO 难度课程 | fixed-medium/staged/too-hard/unfiltered/static 独立同上限实验；记录校准和拒绝成本，零有效更新不推进 stage |
| 2 | Progressive Contraction | 真实教师 backbone、MC 前缀续写、teacher pool 收缩、student NLL 路由、full-SFT 对照与教师成本 |
| 3 | LeWAM | 独立 simulator overlay；固定 ToolHang 数据与发布 checkpoint；真实联合训练后以新 checkpoint 跑 reactive/best-of-k/gradient 三控制臂 |
| 3 | SmolWAM | 独立 LIBERO overlay；固定 Cosmos teacher、一个真实 demo；28→12 block KD、1764→1008 布局课程及新 student/发布模型的同初始状态闭环 |

尚未完成的 CUDA adapter 保持 `requires_gpu_validation=True`，不伪造缺失 receipt。
10 月 14 日已补齐 OAL、NEAR、Beyond、CV-OPD、ReplaySSM 五项真实回执；剩余九项按下表继续验收。
State-OPD 新三臂已完成并保存独立回执；旧快照仍保留，不替代或合并新实验。
因此 GPU evidence gate 在这份 TODO 关闭前不能被报告为通过，MR 也不能被标为全部完成。

## 资源与环境检查点

- 新增公开资源预算仍为不超过 20 GB；不传私有数据、密钥或整个工作区，不回传训练 checkpoint。
- 本机已核验 Qwen Base、SmolWAM、Wan VAE、LeWAM release/ToolHang、Cosmos teacher/单任务 demo 的固定版本与实际文件 SHA；同步断点不等于远端文件完整。
- 固定 LIBERO `8f1084e3132a39270c3a13ebe37270a43ece2a01` 的源 archive 已取得；恢复时为无 `.git` 镜像生成完整逐文件 SHA 清单，不伪造 Git HEAD。
- A100 两套 simulator overlay 先前 pip 因继承的非 UTF-8 metadata 失败。只在独立 overlay 使用精确小依赖的 `--target/--no-deps/--ignore-installed` 路径；不篡改共享 metadata、不重装共享 Torch。
- 10 月 14 日 A30 MiniLM、LongMem 原文及 raw-only provenance 全部逐字节核验通过；NEAR/Beyond 八项真实 GPU 结果及对应回执已保存，共享 Torch 未修改。详见[记忆检索恢复说明](oct13-memory-resume-notes.md)。
- SkillDreamer 旧 `6aabe57a` 的 seed 43 缺失模型输出字段，失败已保留；修复 schema 失败处理后必须在 `0f5dca9f` 上重跑完整三 seed，不混入旧 seed 42。
- MBS 首轮没有正常终止的 verified-hard 根题；SynthSelf 原口径未通过 Eq.6，且 gold/rewrite EOS 口径需统一；UPTURN 段落 token 检测漏切与无有效救援信号均须分开处理。三者真实失败、成本和源码哈希见[独立审计](oct14-post-failure-review.md)，不能仅凭参数变化签通过回执。
- SkillDreamer 每个 seed 必须实际发生 CSI 能力评估、真实 gallery 技能加载和工具执行才能签完成回执；全失败记录仍保留，但三 seed 本身不代表定义链路已执行。

每次恢复先核验源代码 SHA 和资源实际字节；确认后再运行。每篇结束取回 JSON/日志，
验证非零有效更新或明确的负对照边界，再生成 sanitized receipt，最后跑统一门禁。
本机大资源是待恢复用途，暂不删；每轮完成清理可重建的中转副本、站点/打包/页渲染，保留结果和失败证据。
