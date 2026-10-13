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

LeWAM 已补齐 `0f5dca9f` A100 三 seed 原生联合训练→新候选三臂闭环，各 seed 有 4 次非零更新；三臂均为 16.67% ± 28.87%，未观测到规划优势，目标来自训练轨迹而非 holdout。SmolWAM 已补齐 `2b84c377` A100 三 seed 实际 teacher KD、两布局课程与新学生闭环，每 seed 8 次更新、38 次真实 policy queries，但学生与 no-op 均 0/2 成功；6 个原始文件、请求和新学生权重绑定独立核验通过。

SynthSelf、Progressive Contraction 的默认42/43/44完整核心链路已运行，并逐字段独立复算native与三种子回执。SynthSelf方法acquisition均值0.5、gold-SFT控制0.6667，retention两臂均0.3333；Contraction方法与full-SFT控制逐seed相同、均值0.5833。没有相对控制的稳定收益，曝光比只指SFT样本曝光，不是总计算节省。

UPTURN默认42/43/44也已实际执行：42/43有非零rescue信号，44救援奖励/优势全零，仅entropy项产生参数更新，仍是失败。完整execution cohort包含失败，不签三种子通过回执；旧有效seed42回执保留。三种子执行完成不等于三种子机制通过或能力提升。

SOAR `b9086275` A100默认42/43/44×两臂已完成，六份实际raw逐字段复算为独立三种子native与回执。方法12次、消融10次真实更新；消融43 validation准确率0及等值奖励跳过均保留。仅L1、每seed4条validation，不能升级为稳定能力提升或原benchmark比较。

修后难度课程A30 seed42五臂已完成并独立复算，实际更新19/4/7/10/10；unfiltered/static的13/4等值组全部正确跳过。staged准确率降为0、too-hard仍有非零更新均保留；这是阶段native，不是三种子回执。43/44十项同源同预算实际运行继续，全部15项核验后才签新的完整计划回执。

难度课程已补齐 `6aabe57a` A100 seed42 三臂的历史机制回执（实际更新 8/9/11）；独立重审这些已签组的奖励均有真实差异，未出现下述等值奖励伪更新。它不能替代数值修复后源码的新 GPU 核验。

A30 `51b4718a` unfiltered/static seed42 与 unfiltered/static/fixed seed43 已实际完成，但摘录核验发现 shared FP32 均值舍入残差被标准差归一化放大：unfiltered42 有 12/32 组、static42 有 3/8 组等值奖励误触发更新。这批控制结果不予验收；保留原始数值，不筛掉坏组后重新宣称通过。旧队列已定向停止，仅终止本轮记录的任务进程，保留中断，seed44 没有启动。修复后五臂三种子必须同一源码、同一设备、同预算重跑；A100 与 A30 的不同初始准确率也不能冒充严格配对对照。

## 剩余验证清单

全部使用固定公开 checkpoint/data revision，原始输出不可覆盖。默认 seed 为 42/43/44；
只能依据训练/validation 诊断调整训练预算，不以 test 挑方案。失败与零梯度必须保留。

| 优先序 | 论文 | 恢复后要执行的完整链路 |
| --- | --- | --- |
| 2 | SkillDreamer | 固定 checkpoint、公开 train-only GSM8K 子集；no-skills/direct/PSG+HSR+CSI 三臂实际工具执行，参考答案仅外部 scorer 可见 |
| 2 | MagicBeanStalk | 真实 teacher 分解、独立验证、effectivity、Goldilocks、非零优势 RLVR 与 seed-RLVR 对照；不合格合成不算完成 |
| 2 | GRPO 难度课程 | fixed-medium/staged/too-hard/unfiltered/static 独立同上限实验；记录校准和拒绝成本，零有效更新不推进 stage |

尚未完成的 CUDA adapter 保持 `requires_gpu_validation=True`，不伪造缺失 receipt。
10 月 14 日已补齐 OAL、NEAR、Beyond、CV-OPD、ReplaySSM、LeWAM、SmolWAM，以及SynthSelf、Progressive Contraction与SOAR完整三种子机制回执；UPTURN保留有效单seed回执和含失败的三seed执行记录。统一 GPU 门禁当前仅缺 MagicBeanStalk、SkillDreamer；另有难度课程修后五臂/三种子核验未完成，不能将门禁缺项数等同于全部剩余工作。
State-OPD 新三臂已完成并保存独立回执；旧快照仍保留，不替代或合并新实验。
因此 GPU evidence gate 在这份 TODO 关闭前不能被报告为通过，MR 也不能被标为全部完成。

## 资源与环境检查点

- 新增公开资源预算仍为不超过 20 GB；不传私有数据、密钥或整个工作区，不回传训练 checkpoint。
- 本机已核验 Qwen Base、SmolWAM、Wan VAE、LeWAM release/ToolHang、Cosmos teacher/单任务 demo 的固定版本与实际文件 SHA；同步断点不等于远端文件完整。
- 固定 LIBERO `8f1084e3132a39270c3a13ebe37270a43ece2a01` 的源 archive 已取得；恢复时为无 `.git` 镜像生成完整逐文件 SHA 清单，不伪造 Git HEAD。
- A100 两套 simulator overlay 先前 pip 因继承的非 UTF-8 metadata 失败。只在独立 overlay 使用精确小依赖的 `--target/--no-deps/--ignore-installed` 路径；不篡改共享 metadata、不重装共享 Torch。
- 10 月 14 日 A30 MiniLM、LongMem 原文及 raw-only provenance 全部逐字节核验通过；NEAR/Beyond 八项真实 GPU 结果及对应回执已保存，共享 Torch 未修改。详见[记忆检索恢复说明](oct13-memory-resume-notes.md)。
- SkillDreamer 旧 `6aabe57a` 的 seed 43 缺失模型输出字段，失败已保留；修复后 `0f5dca9f` 三 seed 已完成，但 CSI、真实技能加载和 SkillDreamer 工具动作均为 0，48/48 episode 未完成核心链路。不签通过回执，也不混入旧 seed42；下一步只使用独立 validation 格式诊断，不用 evaluation ID 挑方案。
- SmolWAM `2a061dd6` 的 adapter 输入错误已保留；修复只提取原生 latent adapter，不改变教师结构。`2b84c377` 三 seed 已完成并核验；24 次实际更新与新候选控制只证明缩放链路执行，不能把全零成功率包装成能力改善。
- MBS 首轮没有正常终止的 verified-hard 根题；SynthSelf 原口径未通过 Eq.6，且 gold/rewrite EOS 口径需统一；UPTURN 段落 token 检测漏切与无有效救援信号均须分开处理。三者真实失败、成本和源码哈希见[独立审计](oct14-post-failure-review.md)，不能仅凭参数变化签通过回执。
- SkillDreamer 每个 seed 必须实际发生 CSI 能力评估、真实 gallery 技能加载和工具执行才能签完成回执；全失败记录仍保留，但三 seed 本身不代表定义链路已执行。
- SkillDreamer 的独立 7B、8 题 validation 探针真实执行了 7 次 PSG/HSR、2 次 CSI/技能加载，但工具动作仍为 0。原提示未完整说明解析器要求的标签格式与四种决策枚举；只修提示说明、不放宽解析器，修复后必须新冻结源码再测。旧失败不被新结果覆写。
- MBS `0f5dca9f` 限定重跑已找到 3 个正常终止的 hard 根题，但没有合格后代、没有 RL 更新。SOAR `57b2314d` 7B train-only 格式探针 8 次均首轮无效、未发生检索或训练。旧探针未保存原响应正文，不能凭响应哈希猜测格式失败原因；下一步先补可审计的响应/拒绝阶段记录，不放宽论文核心门槛。
- 数值修复保留原 GRPO 优势公式和 `std + 1e-6`：CPU FP64 先平移奖励再中心化，等值组精确为零，最后转换成策略精度；SOAR 的逐轨迹标准化复用该计算。没有用容差强制抹掉真实奖励差异，没有改变 gate、奖励或训练预算；新源码仍须真实 GPU 重测后验收。
- `b9086275`新MBS限定run实际343.08秒，仍没有合格后代；实际响应显示第二子题丢失必要题设、独立验证拒绝，另外两根题的teacher算错，不能放宽验证器签通过。新SOAR同源train-only探针实际35.97秒，3条有效轨迹、2条source-match且真实发生检索；它没有训练或评估，只解除原格式阻碍，不算整方法通过。

每次恢复先核验源代码 SHA 和资源实际字节；确认后再运行。每篇结束取回 JSON/日志，
验证非零有效更新或明确的负对照边界，再生成 sanitized receipt，最后跑统一门禁。
本机大资源是待恢复用途，暂不删；每轮完成清理可重建的中转副本、站点/打包/页渲染，保留结果和失败证据。
