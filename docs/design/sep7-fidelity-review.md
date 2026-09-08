# 2026-09-08：9 月 7 日批次保真度更正

本次修复撤销不成立的旧证据，不把核心算子测试升级为完整论文复现结论。

| 范围 | 已修正实现 | 验证 | 仍不包含 |
| --- | --- | --- | --- |
| BeaconKV / KVMEM | query normalization、模型实际 RoPE、逐 query head 的 GQA；移除虚构存储层计数 | A100、固定 Qwen3 revision、96 head-layer，完整 attention 输出最大误差 0；3 个 CPU 回归 | 32K/百万 token、真实服务吞吐、CPU/NVMe 分层调度 |
| AlleCompanion | 共享双塔、类别条件适配器、混合负样本与类别重建损失；实际 optimizer 更新 | CPU MovieLens 三 seed，同预算无适配器对照；各子模块梯度测试 | ComCat 多源映射、商品互补性数据集及线上 GMV |
| AutoLR | 独立候选评审输入、真实训练回调、validation 决策、独立保护指标、持久化恢复、固定参考、人工发布边界 | 三 seed 离线控制；门槛拒绝、恢复、不越权测试 | LLM 自主调研/代码生成、生产多专家辩论、线上试验权限 |
| AtomRec | 原子节点、链接、修订与多跳路径、容量淘汰 | 图路径、修订和悬空边回归；公开观察解析诊断 | LLM 语义编辑器和推荐任务效果 |
| CoSkill | 私有技能编辑、子树检索、执行验证后晋级、谱系；GiGPO 分组核心及共享参数联合损失 | 拒绝无效晋级、角色梯度、状态分组测试 | 完整 VERL / ALFWorld / WebShop LLM 训练 |
| SiLR | simulator 深拷贝、逐分支严重度准入、拒绝不修改实时状态 | scalar trap 反例、SAFE_PROGRESS / PASS 测试 | Gym-ANM / CityLearn 大规模恢复率、LLM GRPO 训练 |
| Multi-Harness RL | 同批 rollout 的 within/cross 相对信用、可微 clipped objective | 分组反例与实际参数更新测试 | SWE-bench 真实多 harness 训练与未见 harness 迁移率 |

## 证据规则

- 四个 Agent 的 legacy 策略只收到公开 `task_id / intent / context`。测试将 gold answer、gold plan、隐藏 required tools 设为抛异常属性。
- legacy mini-suite 是公开文本格式解析任务；满分不能说明工具能力。没有 simulator/rollout 时，不再伪造准入计数、held-out 次数或策略更新。
- 算子使用明确的 simulator、执行验证、rollout 回报输入；接入真实环境仍需单独验证，不通过注册名称推断已接入。
- GPU 修正证据保留原路径以避免断链，内容明确更正日期与旧结果作废原因。
- 重新生成器：`PYTHONPATH=src python scripts/regenerate_sep7_fidelity.py`。产物记录代码 commit 和数据指纹；用户自己的 `rl_papers_summary.md` 未修改。

## 本地验证命令

```bash
python -m pytest tests/test_sep7_fidelity.py tests/reproductions/test_sep_7_2026_batch.py tests/reproductions/test_kv_attention_fidelity.py -q
python scripts/validate_gpu_evidence.py
PYTHONPATH=src python scripts/manage_paper_specs.py check
PYTHONPATH=src python scripts/manage_paper_specs.py validate
python scripts/migrate_metric_schema_v2.py
python -m mkdocs build --strict
```
