# 开源实现对照

| 实现 | 类型 | 特点 | 集成方式 |
|---|---|---|---|
| [TypeSafe Jev](https://docs.typesafe.ai/introduction) | 官方托管模型 | Choice / Score / Noul；完整概率与 confidence | 可选 HTTPS provider；不缓存密钥或响应内容 |
| [GLiClass](https://github.com/Knowledgator/GLiClass) | 论文官方代码 | 动态 label、uni/bi encoder、多种 scorer | 作为结构来源；本仓库提供轻量独立 scorer |
| [NanoJev](https://github.com/TianyuCodings/NanoJev) | 社区独立复现 | Qwen3-backed、动态候选、公开模型与数据 | 登记为外部对照，不冒充官方 Jev |
| [jevlike](https://github.com/vinnylarouge/jevlike) | 社区独立复现 | option attention、每候选概率 | 登记为外部对照，不复制其代码 |

社区项目均明确基于公开行为自行设计。由于 Jev 的真实架构未公开，本仓库不使用“官方复现”“等价实现”等表述。
