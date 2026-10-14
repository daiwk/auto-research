# 10 月 14 日标签与执行边界检查

本轮对 AST inventory 新出现的字段访问与计数器逐项检查；inventory 仍是审查工具，不是能力证明。

| 源码 | 新访问/计数 | 允许作用域与行为证据 |
| --- | --- | --- |
| `agent_research/memcon.py` | policy update / episode counter | 只在实际 memory backend 操作和 terminal feedback 后更新；计数不代表 Agent 能力。60 episodes 的可观测 record 检索诊断与维护/反馈持久化测试单独验证，未读旧 Task 的 answer/plan。 |
| `system_one/regional_transfer.py` | prediction gold / fallback gold | 只用于文件输入一致性检查、公开预测评分，以及 **validation** 温度/路由选择；test gold 不参与选择。变更 test label 不改变温度、阈值或 validation 路由的回归测试通过。 |
| `system_one/request_audit.py` | scorer 专属 `positive_labels` | 请求编译器仅取显示证据与当前问题；独立请求 bytes 不因其他问题、路由标签或评分标签变化。指标计算才接触标注，不把它交给模型。 |
| WeGR | 训练期 SID / logged reward | tokenizer 只对 train items/sessions 拟合，validation 选 arm，test 只报告；评分与查询日志均为 MovieLens 公开替代，不暗称生产标签。 |
| EmbeddingGemma 2 | caption-image 配对 ID | 编码只看真实图像/文本；配对 ID 在编码后进入多正例 scorer。四个 MRL 维度预先固定并全报告，无留出集择优。 |

本轮不存在新 Agent gold-answer 直返路径。MemCon 是记忆控制算子，JEV request audit 是协议；它们均未自动获得 evolve 晋级资格。五篇延期论文没有可执行 adapter 或指标产物。
