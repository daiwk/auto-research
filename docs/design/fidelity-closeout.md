# 新论文增量前的统一收尾

范围：用户要求一次完成四项，统一 MR；不能把单元测试、固定候选或注册名称算作真实能力。

## 验收清单

- [x] 全库保真度审计：按源文件/方法列出 gold label 访问和仅计数器路径；诊断实现不能支撑能力声明。
- [x] CI 防回归：新增泄漏/未执行算子必须失败；历史诊断明确隔离，不能被 evolve 晋级。
- [x] CoSkill 真实闭环：checkpoint 生成动作、环境实际执行、私有技能编辑、重置后验证、角色隔离信用、共享参数训练；独立 validation/test、多 seed、A100 运行证据；接入 evolve 并验证运行恢复。
- [x] 商品数据验证：AlleCompanion 完成公开数据三种子对照；AtomRec 完成修正版 checkpoint 原子记忆、多阶段生成、无标签候选排序和严格失败路径的 A100 复跑。
- [x] AutoLR 实验闭环：真实 checkpoint 动态提案、双 reviewer、反向传播验证、validation 选优、账本恢复和最终一次 test 均完成 A100 端到端运行。
- [x] KV 任务级验证：多文本、长上下文任务正确率、延迟和峰值显存，统一预算；A100 实跑。
- [x] 结果、文档与看板已同步；完整测试、生成契约和 PR CI 均通过，统一收录于 PR #152。

## 实施约束

- 不删除负结果，不因模型失败而换成标准答案或预定义正确动作。
- 原始数据、checkpoint 和远端日志不提交；只提交脱敏可复核证据。
- 论文完整规模不作为门槛，但定义方法的生成、训练、推理路径不能替换为代理。
- GPU 实验使用用户指定 A100/A30；上传遵循用户授权和平台审批。
- 已合并 #151 是本轮基础，不重复计算为本轮的新完成项。

## 2026-09-10 收尾记录

- 已隔离 legacy Agent evolve：mini-suite 和固定补丁环境不能晋级；ToolRoute 的通用路由算子与论文实现名称分离，未知论文算子直接失败。
- `scripts/audit_fidelity_boundaries.py` 生成全 `src` 的属性、字面量下标和 `get/getattr` 标签访问及状态更新清单，CI 检查漂移。当前 50 个文件共 1,292 条审阅点；按下述角色完成分类，但动态键和跨函数数据流仍由行为测试兜底。
- CoSkill 已在 A100 执行真实 Qwen3-4B checkpoint。最初两个训练任务的优势/梯度全零，保留为失败的训练覆盖诊断；扩到 12 个训练任务后，三个 seed 均发生参数变化且两个角色有非零梯度，但验证没有稳定提升。统一控制器另以一轮真实 CLI smoke 验证候选执行、负结果选优、最终 test、报告和 checkpoint 恢复。
- Amazon Beauty 原始商品元数据和交互数据已执行 1,000 用户、2,000 商品上限、三种子双塔对照。当前类别适配器在 next-product 任务上弱于双塔；不能冒充语义互补性评测，也不能因为负结果删除记录。AtomRec 另在严格 pre-target 重建和无 gold fallback 下完成小样本公开商品记忆实验，test 结果为负。
- AutoLR 已增加动态提案、独立 reviewer 回调、执行验证和恢复接口；公开 Amazon Beauty 上的三个真实提案均未胜过基线，负结果和最终 test 已保留。
- KV 已从固定 revision 的公共镜像在 A100 直接下载并校验 WikiText-2 test，完成 6 段非重叠文本评测。KVMem 质量接近 full 但 Python 实现慢 56 倍；参考后端保留完整 backing cache，峰值显存未下降，不宣称加速或节省。
- 本轮实现、公开结果、A100 脱敏证据、本地生成契约与 PR CI 已全部核验；后续回到近期论文增量扫描。

## 审阅分类

| 路径族 | 标签读取的允许位置 | 能力声明边界 |
|---|---|---|
| `datasets.py`、`*data.py` | 数据解析/切分阶段 | 不进入 policy observation；由隔离测试保证 |
| `*benchmark.py`、`*evaluation.py`、`generation.py` 的 verifier | 环境与评测器 | 只在动作/文本生成完成后评分 |
| `agent_research/method_families`、`latest_*`、`p0/p1_*` | legacy fixture 方法曾读取标签 | 全部属于 L1 机制诊断，不能进入 evolve 晋级 |
| `post_training` 候选策略 | 候选集由 gold 构造 | 明确 `diagnostic_only`；只有自由生成路径可晋级 |
| `multimodal`、foundation checkpoint 评测 | 评测器读公开 benchmark 标签 | checkpoint/prompt 不接收标签 |
| `evolution/composable.py` | legacy 环境及评测聚合 | mini-suite 禁止晋级；真实 ToolRoute 只暴露公开观察 |

状态更新清单只说明“代码确实改变了某个计数器/缓存”，不能证明模型、工具、优化器或论文算法执行。能力证据必须同时有行为测试、真实执行轨迹及独立 split；公开看板以显式 `diagnostic_only` 为最高优先级，不允许旧的 `formal_comparison` 标签覆盖它。
