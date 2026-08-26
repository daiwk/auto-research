# 声明式论文实现规范

每个已注册 adapter 旁都有一个 `paper.yaml`。它使用 JSON-compatible YAML，既可以被 YAML 工具读取，也能只依赖 Python 标准库完成确定性校验。当前全部 adapter 已迁移，不存在“只有新论文有 spec、旧论文仍靠人工同步”的双重口径。

## 单一声明包含什么

`paper.yaml` 明确记录论文链接、机构、精确 arXiv v1 日期、原作者代码状态、track/topics、本地代码与文档、复现 fidelity、评测层级、公开数据集、基线、指标、实际实现机制和可选 Evolve 算子。它与 registry 和文档共同接受 CI 对照，避免公司、日期、路径或指标在各目录漂移。

```json
{
  "schema_version": 1,
  "key": "rankmixer",
  "arxiv_id": "2507.15551",
  "paper_url": "https://arxiv.org/abs/2507.15551",
  "organization": "ByteDance",
  "published": "2025-07-21",
  "upstream_code": "not released / not found",
  "datasets": ["movielens-100k"],
  "baseline": "DIN",
  "metrics": ["ndcg_at_10"]
}
```

## 生成、校验与脚手架

```bash
# 从当前 registry/README 同步全部声明
PYTHONPATH=src python scripts/manage_paper_specs.py generate

# CI 使用：字节级检查声明是否过期，再做语义校验
PYTHONPATH=src python scripts/manage_paper_specs.py check
PYTHONPATH=src python scripts/manage_paper_specs.py validate

# 从审核后的声明建立新 adapter 骨架；拒绝覆盖已有目录
PYTHONPATH=src python scripts/manage_paper_specs.py scaffold \
  --spec paper.yaml \
  --destination src/auto_research/reproductions/new_paper
```

脚手架只建立 `adapter.py`、`experiment.py` 和声明文件，不会生成虚假的训练结果；开发者仍须实现论文机制、补公开数据实验和文档测试后才能注册。
