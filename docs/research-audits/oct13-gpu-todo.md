# 2026-10-13 GPU 验证 TODO（网络恢复后继续）

2026-10-13 用户要求网络不稳定时先停止 A100/A30 的连接、传输和新实验，保留为 TODO。
2026-10-14 用户已明确恢复使用；两类 NVIDIA GPU 的 SSH 只读检查均成功，已有实验目录仍在。
当前按固定源码/资源 SHA 核验后续跑，下面未完成项仍不因连接恢复自动验收。
本轮不因这项暂停删除失败结果、降低 GPU 门禁或宣称 19 篇全部验收完成。
源码检查点：`ccad3e679787f6f5383b8bd3dd1c7b58e7c8c5d0`；之后的文档/工具收口以分支最新提交为准。
本地已完成的核验、已修复失败点及最终检查边界见[本地收口检查点](oct13-local-closeout.md)。
续办源码包绑定提交 `4496283ac8e37c070b8f71b20af6138526cbba15`；仅含公开源码与本轮执行脚本，
不包含工作区缓存、私有数据或密钥。不覆写旧运行目录，源码修复必须先提交新快照后再运行。

## 已有真实结果

| 论文 | 已核验结果 | 不覆盖的内容 |
| --- | --- | --- |
| UxSID | A100，42/43/44，943 用户、四结构实际训练、缓存一致性 | 原工业线上收益、完整 XLong/KuaiRec；本次无稳定提升 |
| State-OPD | A100 原快照，42/43/44，实际更新；8 题 accuracy 前后均为 0 | 新源码默认路径、完整历史 OPD / 无扩采控制 |
| GPPO / TAPO | A100 原快照各三 seed，独立 GRPO-control 三 seed；3 rollout groups × 2 inner updates = 6 次实际 optimizer 更新 | 大规模长轨迹能力结果；8 题仅为机制诊断 |
| DoubleCat / SemiCat | A30 新核心，42/43/44，真实 40 步与 32 NFE | 原 TinyGSM/OWT 规模；onehot/DoubleCat 坍缩负结果保留 |
| OAL | A100，42/43/44，实际分组/校准及 OAL/softmax 匹配 LoRA 更新；原始结果和源码哈希核验通过 | 仅一个中间层、3 步、32-token 块；seed 44 不优于基线，非原论文全规模或效率结果 |
| NEAR / Beyond | A30，共享 bank 100 queries 各三 seed，另各一项严格 bank-disjoint 30-query 诊断；八份原始结果和源码哈希核验通过 | 官方 evaluation 实例再切分的非官方诊断；相同数据的三 seed 非独立重复；严格协议仅 2 test queries，不能合并统计 |

对应指标与脱敏回执均在各篇详情页。旧标准 SC GPU 结果不能替代 DoubleCat 新核心的回执。

## 剩余验证清单

全部使用固定公开 checkpoint/data revision，原始输出不可覆盖。默认 seed 为 42/43/44；
只能依据训练/validation 诊断调整训练预算，不以 test 挑方案。失败与零梯度必须保留。

| 优先序 | 论文 | 恢复后要执行的完整链路 |
| --- | --- | --- |
| 1 | State-OPD | 最新源码 default/state、full-history-opd、state-no-expansion 三种路径；同预算，实际 token/动作成本单独报告；重绑定 source receipt |
| 1 | ReplaySSM | 固定作者 Triton 源码；Mamba2/GDN、四精度、独立读写 rounding、回放/rollback；不宣称 FP32 仿真具有低位 HBM 收益 |
| 1 | CV-OPD | 已准备的 COCO train2017 16/8/8 分区；八真实类别、正负裁剪与 gate、实际 VLM 更新；全拒绝如实失败 |
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
10 月 14 日 OAL、NEAR、Beyond 三项已补齐真实回执；当前 GPU evidence gate 仍报告 **11 项缺失**。
CV-OPD 六臂实际进程已结束，但整理核验和回执尚未完成，暂不移出缺失清单。
因此 GPU evidence gate 在这份 TODO 关闭前不能被报告为通过，MR 也不能被标为全部完成。

## 资源与环境检查点

- 新增公开资源预算仍为不超过 20 GB；不传私有数据、密钥或整个工作区，不回传训练 checkpoint。
- 本机已核验 Qwen Base、SmolWAM、Wan VAE、LeWAM release/ToolHang、Cosmos teacher/单任务 demo 的固定版本与实际文件 SHA；同步断点不等于远端文件完整。
- 固定 LIBERO `8f1084e3132a39270c3a13ebe37270a43ece2a01` 的源 archive 已取得；恢复时为无 `.git` 镜像生成完整逐文件 SHA 清单，不伪造 Git HEAD。
- A100 两套 simulator overlay 先前 pip 因继承的非 UTF-8 metadata 失败。只在独立 overlay 使用精确小依赖的 `--target/--no-deps/--ignore-installed` 路径；不篡改共享 metadata、不重装共享 Torch。
- 10 月 14 日 A30 MiniLM 全部资源逐字节核验通过；LongMem 原文及 raw-only provenance 已补齐并核验。新独立 overlay 安装/metadata 审计与 CPU 前向已通过，共享 Torch 未修改。NEAR/Beyond 待显式诊断标记修复冻结后启动 CUDA，不能把这些准备工作当作 GPU 结果。详见[记忆检索恢复说明](oct13-memory-resume-notes.md)。

每次恢复先核验源代码 SHA 和资源实际字节；确认后再运行。每篇结束取回 JSON/日志，
验证非零有效更新或明确的负对照边界，再生成 sanitized receipt，最后跑统一门禁。
本机大资源是待恢复用途，暂不删；每轮完成清理可重建的中转副本、站点/打包/页渲染，保留结果和失败证据。
