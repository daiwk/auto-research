# 2026-10-14 post-training 旧失败独立审计

## 结论与范围

本审计记录已真实执行、但**未通过 GPU 验证门禁**的四个 seed 42 诊断。它不是 GPU passed receipt，不修改旧失败，不因参数变化、gate 拟合或单元测试通过而宣称论文方法已验证有效。

四次执行均绑定源码 commit `6aabe57a97ec3a586aac7aeea66128750f9441da`。本次只读取旧运行的结果、失败、启动和退出记录，以及相关实现和已缓存的原文；没有运行 GPU、重新生成响应、下载资源或读取 train/validation/test 数据行。旧结果中已有的验证集汇总和成本仅作为历史执行事实引用；没有用其选择后续方案，官方 test 未打开。

| 旧运行 | 实际判定 | 独立审计结论 |
| --- | --- | --- |
| MBS `magicbeanstalk-s42` | 无合格 verified-hard 根题，exit 1 | 当前四题及终止预算未形成可进入递归构建的根题；不是 effectivity 或 Goldilocks 成功 |
| SynthSelf `synthself-gold-control-s42` | Eq.6 不满足，exit 1 | 严格 sequence-NLL 判定失败正确；另有 gold/rewrite EOS 口径不对称，需要独立核验，不能认定只是模型不适配 |
| UPTURN `upturn-7b-reasoner-s42` | eligible failed rollouts 为 0，exit 1 | 确认段落边界检测有 tokenizer 漏切；缺少逐响应审计，不能解释为“7B 太强、全部答对” |
| UPTURN `upturn-small-reasoner-s42` | position informative groups 为 0，exit 1 | gate 实际训练、head 参数实际变化，但 position 梯度只有熵项，未验证 rescue-learning |

## 固定论文与公开资源身份

论文机构取自本地规格；算法核对使用既有固定 v1 原文，不新增论文扫描。

| 方法 | 原始论文 | 公司/机构 |
| --- | --- | --- |
| MagicBeanStalk | [arXiv 2610.12659v1](https://arxiv.org/abs/2610.12659v1) | NVIDIA / University of Washington / Carnegie Mellon University / Stanford University |
| SynthSelf | [arXiv 2610.13113v1](https://arxiv.org/abs/2610.13113v1) | LG AI Research / KAIST AI |
| UPTURN | [arXiv 2610.13672v1](https://arxiv.org/abs/2610.13672v1) | KAIST |

| 资源 | 固定 revision / SHA256 | 用途 |
| --- | --- | --- |
| `Qwen/Qwen2.5-0.5B-Instruct` | `7ae557604adf67be50417f59c2c2f167def9a775` | MBS/SynthSelf 学生、UPTURN encoder；small 诊断也用作 reasoner |
| `Qwen/Qwen2.5-7B-Instruct` | `bb46c15ee4bb56c5b63245ef50fd7637234d6f75` | MBS/SynthSelf teacher/aligner、UPTURN 7B reasoner |
| `openai/grade-school-math` | `3101c7d5072418e28b9008a6636bde82a006892c` | 仅官方 train 派生的既有 train/validation holdout |
| 原始公开 train 内容 SHA256 | `17f347dc51477c50d4efb83959dbb7c56297aba886e5544ee2aaed3024813465` | 旧结果保存的数据身份 |
| train 分区 SHA256 | `6b8672439c8cf6f6b6e65bf5f0e515fbf4c497c9066eefb62a6a6a61ced158e3` | normalized-question SHA256 的固定分区 |
| validation 分区 SHA256 | `2cf1119ad7b2e31e825274487ef32c073e03a8ed44f08ecd3e0366c1f40ebdb7` | 仅引用旧元数据；本审计未读取其内容 |

旧运行 context 上限为 4096；MBS 用 4 train 题，其他三项用 8 train 题，旧运行均配置 4 validation 题。这些是既有配置，不代表正式能力比较。完整公开 checkpoint 文件 hash 保留在旧结果及资源审计中；本文件不复制权重、响应、题目或答案。

## MBS：没有 verified-hard，不等于递归构建成功

`6aabe57a` 的根题入口要求全部实际目标学生 rollout 失败，且全部未截断：`not any(rewards) and not any(truncated)`。旧 raw 的四组结果为：

| 根题序号 | 四条实际奖励 | 截断标记 | accepted |
| --- | --- | --- | --- |
| 1 | `[1,1,1,1]` | `[false,false,false,false]` | false |
| 2 | `[0,1,0,1]` | `[false,false,false,false]` | false |
| 3 | `[0,0,0,0]` | `[true,false,true,false]` | false |
| 4 | `[1,1,0,0]` | `[false,false,false,false]` | false |

第三组不能把预算耗尽的失败伪装为已验证困难。四题都没有通过根题 gate，raw 只记录 `seed-hardness-calibration`；因此未证明实际分解、effectivity、合成、novelty、目标 Goldilocks 或 RLVR 更新发生。错误消息“无合格 descendant”是终止结果，不能推断已经执行下游全部阶段。

该次属于固定小样本/预算下的构建失败；不得放宽 hard/termination gate、伪造答案或将混合成功率题改名为 hard 来签 passed。后续不同源码或 train-only 根题池实验须另开不可变运行，不能改写这次失败。

## SynthSelf：Eq.6 原值与 EOS 风险

从已缓存固定原文核对，Eq.4/5 对整个响应的 token log-probability **求和**再按样本平均，不是 token 均值。Eq.6 同时要求 `L(aligner) < L(gold)` 和 `R(aligner) > R(self)`。

旧 seed 42 的原值：

| 指标 | 实测值 |
| --- | ---: |
| gold sequence NLL | 69.12544560432434 |
| rewrite sequence NLL | 76.84697580337524 |
| rewrite − gold sequence NLL | 7.721530199050903 |
| aligner quality | 1.0（8/8 verified、均未截断） |
| self quality | 0.75 |
| empirical constraints satisfied | false |

质量条件成立，NLL 条件不成立。旧脚本虽随后真实执行方法和 gold-SFT 各两次更新，仍保存 `failed-aligner-constraints` 并返回 1，判定正确。方法每次监督 659 token，对照每次 762 token；相同 epoch 不等于等实际监督 token。不得用已有权重变化绕过 Eq.6，也不能改用 token 均值或截短 rewrite 求通过。

另有必须说明的协议风险：`synthself/checkpoint.py` 将 gold 用 `add_special_tokens=False` 编码，而 `ResponsePolicy.generate` 保留生成的 EOS。固定 Qwen tokenizer 的 EOS 是 ID `151645`、`<|im_end|>`；因此当前 gold 与 rewrite 的结束 token 口径不一致。对比的 NLL 可能受到影响，但已存 aggregate 没有逐响应 token/NLL 分解，本审计无法量化 EOS 对 7.72153 差值的贡献，不能声称修正后一定通过。

后续须在看新结果前预声明一致的完整响应终止约定，保留 sequence 求和与严格不等式；不能从“带 EOS / 不带 EOS”两种结果中择优晋级。旧 raw 仍按原口径保留为失败。

## UPTURN 7B：真实段落边界漏检与归因限制

旧 failure 记录 gate training cases 24、calibration cases 8、eligible failed rollouts 0；在训练 head 前终止。它没有保存逐响应 correctness、truncation、真实字符段落数和检测 cuts 数，因此无法区分“全部正确”“失败但缺少可切段落”“tokenizer 漏切”等原因。

已确认共享 `progressive_contraction.algorithm.paragraph_prefixes` 的实现只搜索孤立 `tokenizer("\n\n")` 的 token 子串；UPTURN construction/evaluation 调用该函数。原文定义是实际双换行段落边界，不保证其 tokenizer 编码在不同上下文中恒定。

本次仅加载既有固定 tokenizer、未加载模型的 CPU 反例：

```text
text = "First step.\n\nSecond step.\n\nFinal \\boxed{2}"
token IDs = [5338,3019,382,15666,3019,382,19357,1124,79075,90,17,92]
isolated "\n\n" token IDs = [271]
token ID 382 decodes to ".\n\n"
真实双换行边界数 = 2
旧 paragraph_prefixes 返回 = []
按原 token 截止位置应为 cuts = [3,6]
```

CPU 核验使用既有 `.cache/oct14-skill-public-transfer` tokenizer。其 `tokenizer.json` SHA256 为 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`，`tokenizer_config.json` SHA256 为 `5b5d4f65d0acd3b2d56a35b56d374a36cbc1c8fa5cf3b3febbbfabf22f359583`，与该固定 Qwen tokenizer 身份相符。

修复契约应扫描真实 decoded 双换行边界并映射回**原生成 token**截止索引，保留原 `tokens[:cut]`，不重编码 prompt/prefix；cut 排序、去重、按上限截取，拒绝响应末端和 `cut >= Lmax`。共享 helper 同时影响 Progressive Contraction，需两调用路径的回归。源码修正、测试和冻结后才能另开 GPU run；这不是更改论文段落定义。

该 bug 可影响 eligible 数，不能由 CPU 反例断言它解释了旧 7B 全部失败。旧结果必须保留，不能直接改名为“7B 太强”。

## UPTURN small：熵项更新不等于救援学习

旧 small reasoner/encoder 均为固定 0.5B。gate 实际运行 20 次 BCE 更新，训练/校准样本为 5/1，训练标签含 0/1，BCE 从 `0.650352418422699` 降至 `0.0020837492775171995`；单个校准样本不支撑稳定 gate 性能。

| Position step | 采样 cut | rescue rewards / advantages | 梯度 L2 | loss |
| --- | --- | --- | ---: | ---: |
| 1 | `[197,172,442,137]` | 四项均 0 / 四项均 0 | 0.000027731650334317237 | -0.0013861844781786203 |
| 2 | `[280,537]` | 两项均 0 / 两项均 0 | 0.0001910477294586599 | -0.0006919213919900358 |

`position_loss` 使用组内中心化奖励，两个 group 的 surrogate 均为零；loss 数值来自 `-0.001 × entropy`。虽然 optimizer 实际执行、参数 digest 改变，`position_informative_groups=0`，不是非零 rescue 优势训练。旧 `failed-no-rescue-signal` / exit 1 判定正确。

这是真实已采样切点上的负结果，不证明全部段落切点、不同预算或不同 reasoner 永远不能救援；段落漏检也限制了原候选集合。不能拿熵项参数更新或 gate 拟合来签 rescue-learning passed。

## 已核对的实际成本

下表取自旧 raw `cost` / `exit.json`；generation calls 是生成 API 调用数，**不是生成响应数**。预算上限、模型加载、未执行阶段与实测成本分开，不用 launch 的理论上界冒充实测。

| 旧运行 | 实际 generated tokens | scored response tokens | frozen encoder forward / input tokens | 墙钟秒 | exit |
| --- | ---: | ---: | --- | ---: | ---: |
| MBS | 6,282 | 0 | 0 / 0 | 85.59944366663694 | 1 |
| SynthSelf + gold control | 6,076 | 4,263 | 0 / 0 | 164.40409300103784 | 1 |
| UPTURN 7B | 7,556 | 0 | 32 / 11,220 | 79.60914537124336 | 1 |
| UPTURN small | 25,532 | 0 | 40 / 21,793 | 250.56925148144364 | 1 |

实际成本逐角色拆分：

- MBS：evaluation 4 calls / 1,541 token；target calibration 4 calls / 4,741 token。无 construction/rescue/训练角色记录。
- SynthSelf：evaluation 12 calls / 4,560 token；aligner 8 calls / 659 token；self rewrite 8 calls / 857 token。初始 NLL scoring 1,421 token；方法与 gold-SFT 合计 2,842 token。既有验证调用已计费，本审计未重跑。
- UPTURN 7B：training rollout 8 calls / 7,556 token；没有 rescue、gate 或 position 更新发生。
- UPTURN small：training rollout 8 calls / 13,843 token；rescue training 6 calls / 2,241 token；evaluation originals 4 calls / 3,310 token；base extra 4 calls / 5,246 token；evaluation correction 6 calls / 892 token。只有最大允许生成预算匹配，不代表实际 token/墙钟相等。

## 一次最小有界后续建议（未执行）

这是 training-only 协议核验建议，不是恢复授权、passed 声明或新实验结果。必须先修正协议、通过 CPU 合同、由主冻结源码和授予 GPU 槽位，再创建新的不可变 attempt；旧失败 source 绑定不变。

固定原 8 条 train、seed 42、公开模型 revision，不读 validation/test，不扩样本、不换模型、不重试：

1. SynthSelf：8 条 aligner 与 8 条 self greedy rewrite，`max_tokens=512`。预声明两侧完整响应 EOS 恰好一次，重算 Eq.4–6；仅构建/NLL 核验，不做 LoRA/SFT 或评测。此阶段本身不能代替通过约束后的真实 SFT 验收。
2. UPTURN：修正段落映射后，用同 8 train、7B reasoner、0.5B encoder，`group=4/max_tokens=768/max_cuts=16/cuts=4/suffixes=2`，gate 20 epochs、position 最多 2 steps，仅训练不 assessment。eligible 仍为 0 或 rescue 优势仍全为 0 即保留失败并停止。

严格总上限：64 个生成输出、45,040 generated token（SynthSelf ≤8,192；UPTURN ≤24,576 原 rollout +12,272 suffix）、32 次 frozen encoder forward（每次完整输入 ≤4,096 token）、16 条 sequence-NLL scoring（响应总 token ≤4,866：固定原 gold 762 加 8 个 EOS，再加 rewrite ≤4,096）、零 LoRA 更新、20 次 gate 更新、position ≤2 次，整体墙钟 ≤1,200 秒。原 gold 的 762 token 来自旧对照汇总，不重新读取或挑选数据行；若固定样本身份/长度不一致，应失败而非扩大预算。未使用预算不转移到额外样本或新配置。任何参数/数据/源码变更都需新 run，不根据失败或 test 结果追加尝试。

## 旧 raw 索引与 SHA256

这些原始运行文件是本地忽略缓存，不提交题目、答案、checkpoint 或日志。下表路径相对仓库根；完整路径为公共前缀 `.cache/oct14-post-training/post-raw-attempt01/` 加“运行目录/文件”。hash 对应本次读取的旧原始字节，可用于核对保留的失败。`launch.json` / `runtime.log` 本身不复制到本文；这里只保存其 SHA256。

| 运行目录/文件 | SHA256 |
| --- | --- |
| `magicbeanstalk-s42/launch.json` | `fc1675dc64ca98b49f5086fd8191fa9f8b07417f6df184a372787f8375e8b484` |
| `magicbeanstalk-s42/exit.json` | `a18d57f66dba8964ccc8219e56ee099bffdf24f8ce60fe78266365ce0cb69c33` |
| `magicbeanstalk-s42/runtime.log` | `f32d9cf8aff30e551a39f29c53f2b75cf21097db0c3536c0a38f406abfaa472e` |
| `magicbeanstalk-s42/evidence/failure.json` | `5fd3a7305d462e1caf2dd0c24b3898b2fb9d5c167f1bff999200f5e312099bca` |
| `synthself-gold-control-s42/launch.json` | `d1cc894c71d3c127a34a1cb8fa55b944c0085b328a98b626a51a37953502063f` |
| `synthself-gold-control-s42/exit.json` | `3bd063b3009b81675ece2d9a0ed0e10ffb6fb90e96b2a4b3877bf234f23157aa` |
| `synthself-gold-control-s42/runtime.log` | `880e4af216d08cefe784985889df3597f18d2266a1a7b25903b99a42507626c9` |
| `synthself-gold-control-s42/evidence/result.json` | `33280c1a0cc3357e15fd9d9d7e9059baa8422aef1e32608d741c94bae3d3f21f` |
| `upturn-7b-reasoner-s42/launch.json` | `267075019fae72a16e7fd3fb2c121675ee6dd22712f8f6081d0895ac6fb8ae8a` |
| `upturn-7b-reasoner-s42/exit.json` | `ed44bbcb038ac5569fa450793ec3b7f6ea862ef49096a47b422c0e0a883bf2cb` |
| `upturn-7b-reasoner-s42/runtime.log` | `7ecf87b51732d48ba4683b467cfb41e22dcbc5ae3ac4d9d308a77b9fc335cbf6` |
| `upturn-7b-reasoner-s42/evidence/failure.json` | `95fea3546302fb434623c8ca84ee9993b707a8c7d1ac124b32176c068752cb8b` |
| `upturn-small-reasoner-s42/launch.json` | `2c83fd1062bea40676741ee28e53e1d703e9718a1a11cb79536132cfd6772860` |
| `upturn-small-reasoner-s42/exit.json` | `668197efb374eecadc9571e5478b58fa2321509b1ca351212580788ca94e152a` |
| `upturn-small-reasoner-s42/runtime.log` | `6460c7e06ec1bc4c381794fa60f006b5f91a71fe551d111f6d822043fe64b857` |
| `upturn-small-reasoner-s42/evidence/result.json` | `779c3d7675edca755d5d246530f136d47440b2231544dcb3d0567275950cca87` |

关键执行源码 SHA256 从各 `launch.json` 的固定 source6a 映射引用，而非按后续工作树重新绑定：

| source6a 文件 | SHA256 |
| --- | --- |
| `scripts/run_oct13_post_training.py` | `f482471e2c33189bcfed7c02fce0e79fb58ba9606a3a354c12ee2a63bfca8f6b` |
| `src/auto_research/post_training/oct13_common.py` | `739f276633d74a85ba790e4d6df25504bce89950c40867ed57302cde03f1ada9` |
| `src/auto_research/post_training/response_policy.py` | `e380a5b4d1d53974b973b72b7d9ad6328129dc8c9bae4d233f6c1cbdf8508bf7` |
| `src/auto_research/reproductions/magicbeanstalk/checkpoint.py` | `f509334fea6b6db2e68668bb7957e8f6e29c522e63012be440779b9346d1c9e0` |
| `src/auto_research/reproductions/synthself/checkpoint.py` | `9835b086272d9262f057a0fc0975d19ff3b84d5e1766cc234ca1e11985164891` |
| `src/auto_research/reproductions/upturn/checkpoint.py` | `83ac66cead272cb391fe27c56f838df5414712283db42f2b8088d3509de311f3` |
| `src/auto_research/reproductions/progressive_contraction/algorithm.py` | `176743356415111e3e19a26427cf59391b4b84b56697adf8d3fe3038ad0de3c1` |

原文核对使用既有 `.cache/oct13-scan/fulltext/2610.13113v1.html.html`（SHA256 `c9efb4a2c920629101e847e312be5fcc08a6adf85d47017deecae300750ef803`）和 `2610.13672v1.html.html`（SHA256 `56ae1afa9358c70e86988f45a097d95e1453b8489fb11edc7c1b8b032f33d0a4`）。算法、旧测量、CPU 反例与未执行建议分开记录；后续修复或新跑结果不得覆盖本文的 source6a 失败事实。
