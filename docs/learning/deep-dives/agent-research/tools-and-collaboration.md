---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 从会调用到能交付：工具接口、可靠性与协作合同

[Agent](../index.md) · 更新 2026-11-27 · 55 篇主题资料 / 12 篇重点对照

Toolformer 学何时调用，SWE-agent 设计动作接口，RATED 处理相关工具的运行可靠性；AutoGen 定义消息程序，MetaGPT 约束角色交付物，World of SWEcraft 再用隐藏下游检验群体产出。每层都可能失败，调用格式正确不是端到端完成的替身。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/tools-and-collaboration.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：改进对象是调用策略、交互接口、工具选择还是团队协议 · 反馈来自语言loss、实际执行、结构交付物还是隐藏下游 · 协作状态是一段对话、显式中间物还是跨会话仓库资产 · 失败和资源如何进入最终交付口径

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [原始来源](https://arxiv.org/abs/2302.04761)<br>章节：背景与主要改动、核心公式、复现边界 | 采样API候选，通过真实返回对后续token loss的帮助筛选，再继续语言模型训练。 | 训练效用不等于所有部署工具可靠；本地确定性utility替代GPT-J loss，未执行完整continued training。 |
| [SWE-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [原始来源](https://arxiv.org/abs/2405.15793)<br>章节：背景与主要改动、核心公式、复现边界 | 以专门ACI控制搜索、查看、精确编辑与测试，把软件任务变成可反复执行的动作循环。 | 接口降低操作负担，不替代理解和验证；本地真实临时仓库属于micro benchmark，不是官方SWE-bench resolved rate。 |
| [AutoGen](../../../agent-research/2308.08155-autogen/README.md) · [原始来源](https://arxiv.org/abs/2308.08155)<br>章节：背景与主要改动、核心公式、复现边界 | 以ConversableAgent、回复策略和停止条件编程消息交互，支持群聊与嵌套会话。 | 抽象灵活但协议仍需设计，角色数量不等于协作质量；本地只执行消息与交接协议，未接完整运行时。 |
| [MetaGPT](../../../agent-research/2308.00352-metagpt/README.md) · [原始来源](https://arxiv.org/abs/2308.00352)<br>章节：背景与主要改动、核心公式、复现边界 | 把软件SOP写入角色流程，每步生产结构化中间物供下游消费和验证。 | 结构化交付限制自由聊天，但上游错误仍可能被后续继承；本地有真实编辑测试，仍不代表完整LLM团队。 |
| [RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics](../../../reproductions/2610.13889-rated/README.md) · [原始来源](https://arxiv.org/abs/2610.13889)<br>章节：背景与主要改动、核心公式、结果、验证与边界 | 冻结语义双encoder取Top-K，再由metadata与逐工具discounted LinUCB利用真实执行反馈重排。 | 只知道选中工具的反馈，不能给未调用项虚构回报；本地encoder短训实际执行，但授权binding失败，未证明原生态能力。 |
| [World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds](../../../agent-research/2610.24061-world-of-swecraft/README.md) · [原始来源](https://arxiv.org/abs/2610.24061v1)<br>章节：背景与主要改动、核心公式、本地复现与成本判断 | 持久会话、issue/PR和包依赖组成软件世界，隐藏下游安装冻结版本检验集体产物。 | 本地微基准通过不足以证明下游收益，指令计数也不是墙钟；完整55K会话环境高成本，本地未运行。 |
| [RuntimeTickets: Source-Grounded Security Obligations for Agent Skills](../../../agent-research/2611.03772-runtime-tickets/README.md) · [原始来源](https://arxiv.org/abs/2611.03772)<br>章节：核心公式、数据协议与实现边界、高成本完整实验 | 从宿主授权收紧得到有源冻结ticket，在发送前核对接收者、对象和累计额度，先判Deny，再判Defer，最后才Allow。 | 依赖可信宿主validator和真实副作用边界；本地仅原子CPU gate与记录链，不实现完整代理、观测账户或安全能力。 |
| [ReTrace: Distilling Tool-Using Agents into Planner-Free Workflows](../../../agent-research/2611.14492-retrace/README.md) · [原始来源](https://arxiv.org/abs/2611.14492)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 从SOP和推理/工具轨迹恢复前置条件、参数来源与证据引用，编译为代码选择下一步的decision-list工作流。 | Planner-free不排除工具内部模型；本地限定typed guard子集，无LLM抽取/聚合/合成或生产工具执行，未见分支保留unwitnessed标记。 |
| [CapLite: Prompt-Injection Defense for Small Language Model Agents without Model-Written Security Artifacts](../../../agent-research/2611.17115-caplite/README.md) · [原始来源](https://arxiv.org/abs/2611.17115v1)<br>章节：背景与主要改动、核心公式 | 可信schema推导authority，请求精确grounding限制值，读取前提交的写序列限制动作，首次失败停止剩余副作用。 | RuntimeTickets依赖有源obligation、host grant收紧和累计预算；CapLite的信任根是schema及请求。两者都要求所有真实副作用经过可信host，局部callback不是网络隔离保证。 |
| [fork() for Agents: Agent Kernel for Non-blocking LLM Orchestration](../../../agent-research/2611.31727-agent-kernel/README.md) · [原始来源](https://arxiv.org/abs/2611.31727v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、同主题比较与边界、完整实验与成本决定 | Agent-Kernel将依赖图恢复放到内容编排层：异常使后代不可达，SGR只重试失败子图，保存已完成兄弟，并让子节点继承真实父文本；选择性恢复本身继承分布式系统已有思想，不是新的planner或failure detector。 | RuntimeTickets在外部副作用前冻结并检查权限/obligation，对callback异常不自动重发；Agent-Kernel维护SAB内部依赖/状态，重试可以再次执行有副作用的节点。两层可组合但不互相替代。恢复完成不等于授权合法，更不意味着网络exactly-once。 |
| [CAPE: Coordinating Calibration and Search for Tool-Use Policies](../../../agent-research/2611.31938-cape/README.md) · [原始来源](https://arxiv.org/abs/2611.31938v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、同主题比较与边界、完整实验与成本决定 | CAPE离线校准可复制parser配置族，持续存可执行策略并按响应scope做local closure；unknown效果的乐观松弛只指引获取和上界，不能作为部署答案。目标先最大化逐配置完成，再最小化调用总量，并保留初始R0。 | CapLite从可信请求/schema冻结authority grounding与写序列；CAPE在已选操作固定后解决其表示在隐藏parser下怎样执行。reference相等的commit不证明用户授权；CAPE的最优证书也不保证CapLite的write-prefix合同。 |
| [LLM Agent Authorization Across Context Compaction](../../../agent-research/2611.32194-compaction-authorization/README.md) · [原始来源](https://arxiv.org/abs/2611.32194v1)<br>章节：背景与主要改动、核心公式、论文离线与线上效果、数据协议与代码映射、结果、负控与边界、同主题比较与边界、完整实验与成本决定 | 在策略生成前，以入口见证、完整有序列表commit和当前计数绑定用户原始授权文本；agent的摘要工作上下文不参与授权归因。 | RuntimeTickets在副作用前核收件者、对象和预算合同，HMAC审计链不自证前缀完整；本文当前计数拒绝取消省略，却不提供对象validator或安全策略语义。 |

</div>

## 取舍分析 {#analysis}

### 会选工具，还不等于工具能用

Toolformer 的调用样本依据后续预测是否受益筛选，它主要提供策略训练信号；SWE-agent 把可执行接口及返回形态整理给模型；RATED 再将语义相关与近期可靠性拆开。于是“模型愿意调用”“调用格式合法”“接口实际成功”和“答案完成任务”应是分开的记录。相关但失效的工具不能靠更高语义分弥补，接口成功也不能给未调用候选制造反事实奖励。

对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [swe-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [rated](../../../reproductions/2610.13889-rated/README.md)

### 消息协议、中间物与生态后果

AutoGen 让谁回复、何时继续和停止成为可编程协议；MetaGPT 进一步把角色输入输出收束成SOP交付物。World of SWEcraft 将观察范围扩到跨仓库长期维护：一个包自己的测试可能通过，下游却被破坏。它们分别约束沟通控制、信息交接与最终外部影响，不能仅用消息数、角色数或产物数量替代后者。长期协作还需要持久资产与会话预算，而非无限加长单条群聊。

对照来源：[autogen](../../../agent-research/2308.08155-autogen/README.md) · [metagpt](../../../agent-research/2308.00352-metagpt/README.md) · [world-of-swecraft](../../../agent-research/2610.24061-world-of-swecraft/README.md)

### 10月29日：新方法与来源变化

Meta官方retrieval-programs现已可核验，更新RPL旧条目的开源状态；主体CC-BY-NC4，vendored检索/训练组件保留各自许可。代码公开不等于本地typed grammar突然覆盖任意Python、跨轮状态、神经检索或RL；本轮未复制源码或改变原L1证据。

对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [rpl](../../../agent-research/2610.24854-rpl/README.md)

### 被允许的工具也必须受交付对象和额度约束

只按工具名或接收端授权会遗漏复用合法端点的数据外泄。RuntimeTickets让宿主冻结来源可追溯的recipient/object/amount约束，再由模型无关gate逐副作用检查。它仍依赖完整可信网络边界和观察覆盖；本地HMAC前缀可校验但不能证明完整账户已sealed/closed，也不能因为callback至多一次而宣称网络exactly-once。

对照来源：[runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md) · [toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [swe-agent](../../../agent-research/2405.15793-swe-agent/README.md)

### 模型学会何时调用，与代码决定下一步不是同一交付物

Toolformer按真实返回对后续token loss的帮助筛选调用，再继续训练模型；ReTrace则从SOP/推理恢复条件并把运行时选择编译到代码。前者保留模型生成控制，后者仍允许固定工具内部调用模型。它们不能只按工具调用数量排名：本地Toolformer使用确定性utility而非GPT-J loss，本地ReTrace也仅typed IR，均没有完整原模型/生产结果。

对照来源：[retrace](../../../agent-research/2611.14492-retrace/README.md) · [toolformer](../../../agent-research/2302.04761-toolformer/README.md)

### 在副作用前检查，还要说明检查依据从哪里来

CapLite不让小模型写安全策略，而从可信schema和请求绑定authority，附加写序列承诺。RuntimeTickets保留模型提出obligation的路径，但通过原文依据和host批准冻结权限，再检查对象与预算。它们均不能让不可信观察自封授权，也不证明绕过mediator的工具被保护；安全边界不是简单的allow布尔值。

对照来源：[caplite](../../../agent-research/2611.17115-caplite/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

### 恢复子图与保护副作用：状态不丢，不等于效果不重

SGR的保证域是C = V ∖ ({f} ∪ Desc(f))的state与outputs不变。异常检测与retry budget在外部，DSP先级联unreachable再由caller决定是否retry；子节点必须等所有父节点complete，真实输出按声明序继承。prompt-mutation是附录初步探针，不是已交付主循环。本地SQLite事务claim和generation/owner负控拒绝重开前晚到结果，显式单scheduler交接不是分布式租约证明；字符上限准入不冒充模型token预算。副作用后异常负控实际执行两次mutation，保留无exactly-once保证。三seed4节点/5调用只验证重试范围、兄弟保留与文本依赖，不验证Agent能力、语义纠错或论文延迟提升。

对照来源：[agent-kernel](../../../agent-research/2611.31727-agent-kernel/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

### 局部闭合的编译证书，不是部署时偷看配置

CAPE的校准阶段知道候选h，可在隔离测试环境取得f(a,h)=(o,g)；返回policy仅有action和响应分支，部署只读工具观测。closed动作以G∪children组合成功集，以|V|+ΣMchild计算调用mass。未知program乐观立即成功，未知probe乐观每配置独立响应，selected T2只收紧当前动作的两调用续段。witness覆盖R0并在一致新效果后仍可执行，root有效lower=upper才证最优。本地1–8配置/1–4calls、query-count而非wall-clock预算；4配置诊断取得全20格，没有校准节省。独立oracle留在评估侧；随机有限表、中断R0、上下界和V外未知效果负控不等于真实CSV/JSON或LLM胜率。

对照来源：[cape](../../../agent-research/2611.31938-cape/README.md) · [caplite](../../../agent-research/2611.17115-caplite/README.md)

### 认证来源不替代语义授权，副作用合同不替代请求完整性

两条输入必须分开：摘要服务Agent任务，认证原文服务授权器。occurrence MAC、顺序commit、current count/fresh boundary缺一会留echo/replay/omission缝隙。持久counter测试只在keys/state/issuer可信的前提内成立，SQLite不是Agent隔离。RuntimeTickets则冻结host收紧合同并在effect前审计，callback不确定不重发；它本地的审计链不证明被截短前缀完整。两层可组合但没有本地LLM攻击成功率；完整多模型/live矩阵高成本不复现。

对照来源：[compaction-authorization](../../../agent-research/2611.32194-compaction-authorization/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### Toolformer 筛出一个有用API调用后，RATED 为什么仍可能在部署时降低这个工具的优先级？ {#cross-usefulness-versus-reliability}

??? note "展开答案与例子"

    **答案：** 训练筛选说明返回值曾帮助后续预测，不能保证服务一直可用或参数行为不漂移。RATED 先限定语义相关候选，再从实际选中工具的成功、错误和超时更新可靠性统计，用折扣适应变化。训练有用与当前可执行是两个条件，也不能因本次失败给所有未尝试工具打负分。

    **教学例子：** 教学例：汇率API在训练样本很有用，部署后连续超时；语义依旧匹配，但实际可靠性证据应影响下一次选择。

    对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [rated](../../../reproductions/2610.13889-rated/README.md)

### AutoGen 里已有程序员和测试员，为什么 MetaGPT 还强调结构化交付物，SWE-agent 又强调ACI？ {#cross-message-protocol-versus-artifact}

??? note "展开答案与例子"

    **答案：** 角色名只说明职责，AutoGen 的回复与终止协议组织交互；MetaGPT 规定需求、设计、实现等角色具体交付什么，减少信息在自由聊天中漂移；SWE-agent 则约束单次查看、编辑和测试怎样落地。三者分别处理控制、信息合同和动作接口，可组合但不能互相冒充。

    **教学例子：** 教学例：测试员知道何时回复，不代表拿到了明确接口规格；即便规格完整，编辑命令若不能精确定位，代码仍会改错。

    对照来源：[autogen](../../../agent-research/2308.08155-autogen/README.md) · [metagpt](../../../agent-research/2308.00352-metagpt/README.md) · [swe-agent](../../../agent-research/2405.15793-swe-agent/README.md)

### MetaGPT/SWE-agent 的仓库测试通过后，World of SWEcraft 为什么还用隐藏下游包检查？ {#cross-local-tests-versus-downstream}

??? note "展开答案与例子"

    **答案：** 本仓库测试只能覆盖维护者可见合同，跨包接口变化可能破坏真实依赖者，也可能只优化自己可见的微基准。隐藏下游在冻结发布版本上安装并检查，评价不同层面的集体交付。失败包不能从速度平均里静默移除，strict/carry也需明确；这仍不是用一个本地micro通过推导生态能力。

    **教学例子：** 教学例：库作者把函数参数改名并更新自身测试，下游仍按旧参数调用而崩溃；只有依赖者检查能暴露这种回归。

    对照来源：[metagpt](../../../agent-research/2308.00352-metagpt/README.md) · [swe-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [world-of-swecraft](../../../agent-research/2610.24061-world-of-swecraft/README.md)

### 官方仓库补上后，为何仍需保留RPL本地组件边界？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** 来源完整性与执行保真度是两条轴。拿到完整训练代码并未使已有受限SDK执行完整策略、神经检索或蒸馏；若以后接入，需要另定成本、真实运行与许可边界。

    **教学例子：** 教学例：原来能检查检索程序语法，现在知道官方训练入口，也不能把语法测试改叫多跳QA评测。

    对照来源：[toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [rpl](../../../agent-research/2610.24854-rpl/README.md)

### 两个系统都能输出同一个查询工具调用，怎样区分Toolformer训练和ReTrace工作流分派？ {#cross-compiled-rule-versus-learned-call}

??? note "展开答案与例子"

    **答案：** 要看调用如何产生及由什么证据保证。Toolformer通过训练改变模型生成调用的概率；ReTrace运行时检查已可得的guard并选第一个匹配规则，参数有来源。相同单次输出不证明训练链或编译链已经实现，也不能让缺失观察被工具未来返回补齐。

    **教学例子：** 教学例：同为查询订单，一个来自模型预测，另一个来自“尚未查订单”的代码条件；两者都输出查询并不说明后续异常分支等价。

    对照来源：[retrace](../../../agent-research/2611.14492-retrace/README.md) · [toolformer](../../../agent-research/2302.04761-toolformer/README.md)

### 只要CapLite参数都能ground到请求，就能替代RuntimeTickets的总量限制吗？ {#cross-cross-nov15-caplite}

??? note "展开答案与例子"

    **答案：** 不能。grounding限定值是否被请求提及，未限制合法动作累计多少次／多少bytes。后者必须由独立grant和预算合同实现，且要防重放。

    **教学例子：** 教学例：向用户指定邮箱发送一次合法，不表示可重复发送一千次。

    对照来源：[caplite](../../../agent-research/2611.17115-caplite/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

### SGR的状态保持能替代RuntimeTickets的副作用合同吗？ {#cross-cross-nov25-agent-kernel}

??? note "展开答案与例子"

    **答案：** 不能。SGR保护SAB里的兄弟状态并允许重执行；RuntimeTickets在副作用前核权限与obligation，callback不确定时不自动重发。编排恢复与授权/副作用边界是不同层。

    **教学例子：** 教学例：付款已成功后节点抛错，SGR可再次执行；需要下层事务/幂等合同，不能拿兄弟节点没变证明不会重复付款。

    对照来源：[agent-kernel](../../../agent-research/2611.31727-agent-kernel/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

### CAPE保留初始覆盖是否等于CapLite的安全保证？ {#cross-cross-nov25-cape}

??? note "展开答案与例子"

    **答案：** 不等于。CAPE在parser候选族上最大化完成数并再省调用；CapLite冻结可信写序列及authority grounding。结果符合reference不能证明写入被用户授权，覆盖最优也不保证顺序权限。

    **教学例子：** 教学例：一个上传策略能在四种日期parser都commit，仍可能把正确数据发给未经授权的接收者。

    对照来源：[cape](../../../agent-research/2611.31938-cape/README.md) · [caplite](../../../agent-research/2611.17115-caplite/README.md)

### 该门与RuntimeTickets保护的是同一边界吗？ {#cross-cross-nov27-compaction-authorization}

??? note "展开答案与例子"

    **答案：** 不是。本文保护策略生成前的原始授权输入；RuntimeTickets在真实副作用前核冻结recipient/object/budget合同。原文完整不证明策略语义正确，合法发送也不证明摘要来源真实。

    **教学例子：** 教学例：认证用户原句后生成器仍可能错误放宽recipient，需要下层ticket核具体交付，而不是把MAC当语义理解。

    对照来源：[compaction-authorization](../../../agent-research/2611.32194-compaction-authorization/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-27** · 真实HMAC-SHA256 occurrence/sequence分域、精确UTF-8与长度前缀framing、完整有序计数、fresh session/boundary及SQLite持久消费。只释放认证原文，不执行LLM授权语义或真实Agent攻击；可信入口/key/counter隔离是外部前提。1MiB/有符号计数为本地准入，不承诺可用性或生产安全。 成本过高，不复现（审查 DONE）；仅承接小型CPU认证协议。

涉及：[compaction-authorization](../../../agent-research/2611.32194-compaction-authorization/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

**2026-11-25** · 1–8配置、1–4调用的标准库有限编译器保留local closure、持久witness、Eq1–7乐观program/probe松弛、双frontier、三级query获取与selected两调用收紧；完全取得效果时有限递推精确。query-count上限替代wall-clock预算。校准可查询候选h；部署Policy只保存action/响应分支，execute不接活跃h、完整表或gold；独立full-information oracle仅评估侧。教学4配置全20格校准、无校准节省；非DuckDB/pandas真实数据、非LLM工具胜率、非完整性能复现。 完整高成本campaign终态不复现，审查DONE。

涉及：[cape](../../../agent-research/2611.31938-cape/README.md) · [caplite](../../../agent-research/2611.17115-caplite/README.md)

**2026-11-25** · 标准库SQLite/WAL、7态SAB、五动词、事务claim、失败/取消级联、SGR和声明序实际父文本继承。fork不等待执行，run为有界线程池driver；executor仅收task/context、不读gold。显式单owner重开撤销running旧claim，generation/owner拒绝陈旧完成；不是分布式租约证明。字符上限是本地准入而非模型token预算；没有LLM、prompt-mutation、语义恢复或真实tool服务；外部副作用不保证exactly-once。 完整高成本campaign终态不复现，审查DONE。

涉及：[agent-kernel](../../../agent-research/2611.31727-agent-kernel/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

**2026-11-15** · 可信schema推导authority，请求精确grounding限制值，读取前提交的写序列限制动作，首次失败停止剩余副作用。 RuntimeTickets依赖有源obligation、host grant收紧和累计预算；CapLite的信任根是schema及请求。两者都要求所有真实副作用经过可信host，局部callback不是网络隔离保证。

涉及：[caplite](../../../agent-research/2611.17115-caplite/README.md) · [runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

**2026-11-11** · 加入ReTrace，区分模型内工具学习与代码外工作流控制，明确pre-action信息、typed参数来源、unwitnessed分支和工具内部模型边界。只验证CPU IR，不声称私有生产SOP或公开benchmark完整接入。

涉及：[retrace](../../../agent-research/2611.14492-retrace/README.md) · [toolformer](../../../agent-research/2302.04761-toolformer/README.md)

**2026-11-05** · 补入RuntimeTickets，将工具权限与具体交付合同分开：相同合法接收端仍可能承载非法对象或超额发送。逐副作用前的失败、未知、允许分支，先留记录再执行，以及不确定回调后的不重发，是与工具是否可调用不同的运行时合同；CPU负控不等于真实网络安全验收。完整实验高成本不复现，审查DONE。

涉及：[runtime-tickets](../../../agent-research/2611.03772-runtime-tickets/README.md)

**2026-10-29** · Meta官方retrieval-programs现已可核验，更新RPL旧条目的开源状态；主体CC-BY-NC4，vendored检索/训练组件保留各自许可。代码公开不等于本地typed grammar突然覆盖任意Python、跨轮状态、神经检索或RL；本轮未复制源码或改变原L1证据。

涉及：[rpl](../../../agent-research/2610.24854-rpl/README.md)

**2026-10-27** · 首版：比较调用学习、ACI、消息编排、SOP交付、可靠性重排与隐藏下游协作评价。

覆盖 49 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 55 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [RuntimeTickets: Source-Grounded Security Obligations for Agent Skills](../../../agent-research/2611.03772-runtime-tickets/README.md)
- [Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning](../../../agent-research/2610.24854-rpl/README.md)
- [World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds](../../../agent-research/2610.24061-world-of-swecraft/README.md)
- [TRACER: Trajectory-Aware Tool Retrieval for LLM Agents](../../../agent-research/2610.21267-tracer/README.md)
- [SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems](../../../agent-research/2610.21113-structural-signal-retriever/README.md)
- [LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents](../../../agent-research/2610.22280-leash/README.md)
- [JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs](../../../agent-research/2610.21412-jev-agent-harness/README.md)
- [A team of Gemini 4 Argon agents beats Minecraft](../../../agent-research/2610.22319-gemini-minecraft/README.md)
- [Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure](../../../agent-research/2610.21281-diviner/README.md)
- [ARIA: Runtime Inspection and Amendment for Multi-Agent Systems](../../../agent-research/2610.20780-aria/README.md)
- [RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics](../../../reproductions/2610.13889-rated/README.md)
- [When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows](../../../reproductions/2610.13092-jev-workflow/README.md)
- [Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks](../../../agent-research/2610.02001-mingbird/README.md)
- [CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents](../../../agent-research/2609.18779-cera-moa/README.md)
- [RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views](../../../agent-research/2609.16936-repoatlas/README.md)
- [Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration](../../../agent-research/2609.12464-hcrg/README.md)
- [Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks](../../../agent-research/2609.08404-feedback-scaffold/README.md)
- [SWE-Prime: Fewer Trajectories, Better Performance](../../../agent-research/2608.27449-swe-prime/README.md)
- [TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development](../../../agent-research/2608.26086-traceml/README.md)
- [TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving](../../../agent-research/2608.25523-topas/README.md)
- [ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs](../../../agent-research/2608.25992-progrouter/README.md)
- [AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research](../../../agent-research/2608.25559-adavdr/README.md)
- [SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification](../../../agent-research/2608.24571-smith/README.md)
- [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](../../../agent-research/2608.06811-pmcoder/README.md)
- [CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents](../../../agent-research/2608.05886-codegrep/README.md)
- [MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems](../../../agent-research/2607.28527-manta/README.md)
- [CAM-DF](../../../agent-research/2607.27083-cam-df/README.md)
- [Formalizing Mathematics at Scale](../../../agent-research/2605.29955-autoformbot/README.md)
- [PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving](../../../agent-research/mlsys2026-prompts/README.md)
- [PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing](../../../agent-research/2604.05018-paperorchestra/README.md)
- [AIRA2: Overcoming Bottlenecks in AI Research Agents](../../../agent-research/2603.26499-aira2/README.md)
- [Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair](../../../agent-research/2601.19066-dynamic-brt/README.md)
- [Watch and Learn: Learning to Use Computers from Online Videos](../../../agent-research/2510.04673-watch-and-learn/README.md)
- [ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients](../../../agent-research/2508.04086-toolgrad/README.md)
- [ToolRL](../../../agent-research/2504.13958-toolrl/README.md)
- [ReTool](../../../agent-research/2504.11536-retool/README.md)
- [OpenHands](../../../agent-research/2407.16741-openhands/README.md)
- [SWE-agent](../../../agent-research/2405.15793-swe-agent/README.md)
- [AutoGen](../../../agent-research/2308.08155-autogen/README.md)
- [MetaGPT](../../../agent-research/2308.00352-metagpt/README.md)
- [ToolBench](../../../agent-research/2305.16504-toolbench/README.md)
- [CRITIC](../../../agent-research/2305.11738-critic/README.md)
- [CAMEL](../../../agent-research/2303.17760-camel/README.md)
- [HuggingGPT](../../../agent-research/2303.17580-hugginggpt/README.md)
- [ART](../../../agent-research/2303.09014-art/README.md)
- [Toolformer](../../../agent-research/2302.04761-toolformer/README.md)
- [PAL](../../../agent-research/2211.10435-pal/README.md)
- [MRKL](../../../agent-research/2205.00445-mrkl/README.md)
- [SayCan](../../../agent-research/2204.01691-saycan/README.md)
- [WebGPT](../../../agent-research/2112.09332-webgpt/README.md)
- [ReTrace: Distilling Tool-Using Agents into Planner-Free Workflows](../../../agent-research/2611.14492-retrace/README.md)
- [CapLite: Prompt-Injection Defense for Small Language Model Agents without Model-Written Security Artifacts](../../../agent-research/2611.17115-caplite/README.md)
- [fork() for Agents: Agent Kernel for Non-blocking LLM Orchestration](../../../agent-research/2611.31727-agent-kernel/README.md)
- [CAPE: Coordinating Calibration and Search for Tool-Use Policies](../../../agent-research/2611.31938-cape/README.md)
- [LLM Agent Authorization Across Context Compaction](../../../agent-research/2611.32194-compaction-authorization/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/tools-and-collaboration.md) · [返回全部精读卡片](../index.md)
