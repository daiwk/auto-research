# 历史审查与当前实现状态

本页由当前 manifest 与冻结审查登记自动对账。审查决定不随实现变化；
目录登记、可执行注册、GPU 运行验证与能力比较是不同事实。

| 已接受候选的当前状态 | 数量 |
| --- | ---: |
| 已出现在目录 | 0 |
| 尚未出现在目录 | 14 |

目录存在不等于论文完整实现，也不代表能力提升。GPU 回执只核验运行，
不能替代公平 baseline、隔离 split、足够预算和结果审查。

逐篇字段见 [机器可读对账](implementation-status.json)。
当前审查水位以 [统一状态](../../paper-discovery-watermark.json) 为准；
本页不复活已退休的全来源穷尽水位。

重新生成：`python scripts/reconcile_discovery_implementation.py`。
