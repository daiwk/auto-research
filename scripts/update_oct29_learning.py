"""Apply this batch's authored topic comparisons, not generic fallback Q&A.

Each prose update is tied to explicit paper identities and current source
fingerprints. A subsequent source edit requires a new authored update.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-29"
# theme/topic, new memberships, existing source updates, authored analysis,
# cross-paper self-test, and paper-specific comparison rows.
UPDATES = [
    ("foundation-models", "compression-and-cache", ["rescom", "hope-hilbert"], [],
     "ResCom与HOPE压缩的对象不同：前者在固定量化宿主外增加读取activation rounding residual的低秩校正，校准统计与截距需对应同一宿主；后者用Gaussian-ReLU/Hilbert代理评价神经元结构删除，并补偿下游均值。它们不是一个在任意模型上保证等价的剪枝量化组合；本地都只实现精确小组件，未跑LLM或ImageNet能力矩阵。",
     "为什么ResCom的校正rank预算不能直接当作HOPE的可删神经元数？",
     "ResCom预算控制的是输出误差补偿分支的低秩容量，HOPE的候选成本还依赖神经元Hilbert容量与初始参数footprint。它们的参数位置、状态和校准假设不同，不能互换预算单位。",
     "教学例：保留一层的全部量化输出并加rank2校正，与删掉两个神经元再补下游均值，不是同一前向网络。",
     {"rescom": ("以中心化残差/输出误差统计白化，再做截断SVD和截距恢复。", "校准只适用于固定宿主，未实现量化器或原生低比特内核。"),
      "hope-hilbert": ("以biased Gaussian-ReLU核和Hilbert代理计算剪枝率，支持小Dense层均值补偿与单步恢复。", "假设激活的Gaussian代理，不实现MERGE/EVICT/完整HOPE或DEFT；与Sleep的Hope架构不是同一方法。")}),
    ("foundation-models", "context-and-state", ["select-ttt", "sleep-lti"], [],
     "Select-TTT根据当前query的token概率质量调整上下文chunk写入fast weight的力度，apply-before-write保留时序；clip后总写入预算可能低于chunk数，不能再归一化伪装守恒。Sleep则把活跃与离线巩固分阶段，本地仅其LTI奖励。与冻结参数的状态更新相比，后者完整方法要训练扩展参数，不能把一个奖励核当成记忆已写入模型。",
     "query条件写入系数变化，与Sleep奖励变化，分别能证明哪一步真的执行了？",
     "Select-TTT本地参考实际更新小fast-weight矩阵，可检查写入前输出和最终状态；Sleep本地只返回奖励，没有优化器或参数扩展。两者均不证明长上下文能力，更不能把奖励值直接解释为长期记忆保持率。",
     "教学例：一份记忆表的数值真的改变，和给一段续写打0.9分，是不同的执行证据。",
     {"select-ttt": ("对query token的低CE位置top-k聚合，T×softmax分配并clip写入倍率。", "必须传入真实冻结head/RMSNorm与NTP对齐特征；不含LLM或分布式内核。"),
      "sleep-lti": ("把外部语义二元奖励与阈值化token编辑相似度混合。", "只做LTI奖励，不实现CMS、梦境、知识播种或LoRA，完整Sleep高成本不复现。")}),
    ("multimodal-models", "world-state-actions", ["foundation-models:gui-jepa"], [],
     "GUI-JEPA在当前屏幕latent上预测候选动作导致的残差后继，并结合动作ROI/global区域和结构余弦评分。它与像素视频生成的监督/输出不同，也不等于真实GUI执行器；当前组件接外部冻结latent和文本匹配分数，保留真实三层predictor与训练头，但不使用训练正样本标签替forward选动作。",
     "GUI-JEPA预测latent后继，为什么不能直接当作已在手机上验证动作成功？",
     "后继是学到的表示预测，模型可能漏掉状态约束；执行成功需真实环境反馈。小latent前向、候选排列等变和梯度检查只验证模块合同，不能替代动作到环境的闭环。",
     "教学例：模型预测点击后的页面向量接近目标，不等于已经检测到真实设备按钮可点击或请求成功。",
     {"foundation-models:gui-jepa": ("候选动作条件残差predictor及ROI/global结构评分，listwise正例损失。", "真实屏幕编码、候选生成与环境外置；没有GUI benchmark能力结果。")}),
    ("agent-research", "memory-and-skills", ["discernmem"], [],
     "DiscernMem把失败先分为记忆使用范围不对和内容缺陷：对同任务、seed、配置做单记忆/无记忆配对重放，再检查修复是否同时守住父记忆与无记忆基线。它补充了简单追加反思的风险控制：团队结果差不能直接归罪某条记忆；新版本也不能继承旧版本已测效果。本地只做这些测量和版本合同，没有LLM修复或重放。",
     "为何修复后比父记忆好，还可能不能接收？",
     "父记忆本来就可能有害；候选还必须不弱于无记忆基线，守住历史任务并不增加完全失败数。单一正增益不能替代双参照非退化检查。",
     "教学例：父记忆得0.2，候选0.4，无记忆0.8；候选比父版好，但仍不能据此称记忆有价值。",
     {"discernmem": ("配对效果、范围优先归因、双参照修复门槛及版本证据清空。", "scope/defect/replay分数外部提供，不用规则冒充LLM诊断与修复。")}),
    ("agent-research", "harness-and-self-improvement", ["ruharness"], [],
     "RuHarness的criterion frontier不是按一次正确率排序：2×3行为/结果联合表用Jeffreys-Dirichlet后验估计保守utility分位，集合新颖性和冗余仍固定来自已测轨迹。它把有限样本不确定性和候选准入分开，只有active准则能进入frontier，最终harness修改还要独立validation严格增益。本地没有LLM评审或harness生成。",
     "RuHarness为什么不把新颖性和冗余也随每个Dirichlet样本重抽？",
     "这两项来自固定轨迹集合的重叠关系，不是六格结果概率。把它们一同随机化会改变原文不确定性模型；后验保守分位也不等于已证明真实Agent更强。",
     "教学例：两条准则标记了完全相同的失败轨迹，抽一次成功/失败概率不应让这两集合忽然不再相同。",
     {"ruharness": ("六格联合后验、2000次抽样0.2分位、active frontier与validation准入。", "行为标签、执行结果和验证分数外置；统计排序不是完整自进化运行。")}),
    ("recommendation", "feedback-multitask-causality", ["kl-mopd"], [],
     "KL-MOPD把点击/价值的竞争定位到SID位置，而非只合并整物品分数：初始学生到两教师的KL差距校准一次并冻结，当前学生在自己前缀上计算加权反向KL。这与动态追逐当前KL或算术平均教师概率不同；线上收入+1.63%属于完整系统，本地只验损失与梯度，不推出业务因果效果。",
     "两位教师的权重为何不能每一步按当前学生差距重新计算？",
     "原方法的alpha来自固定初始策略，构成训练期间固定目标的一部分；动态计算会改变目标和梯度语义。即使某动态方案也有效，仍需作为不同方法单独验证。",
     "教学例：初始差距1比3给出1/4与3/4，后续差距变了仍保持原权重。",
     {"kl-mopd": ("一次校准位置级教师差距，以固定alpha最小化两项student||teacher KL。", "没有初始/当前学生采样器、推荐骨干或语义ID评测，不继承线上收益。")}),
    ("recommendation", "generative-retrieval-reasoning", ["pailitao-mmsearch2"], [],
     "PailitaoMMSearch2.0将多意图图文请求直接解码为商品SID候选集合，以数据工具、CPT、混合预算SFT和意图均衡RL扩展服务。Sample–Beam使推理采样与候选束生成分别对应训练/展示需要；大模型或更长思考不保证所有意图更好。与其他生成式召回对比时应固定候选集合、预算和生产混排口径，而不是只比模型名字。完整方案本地不复现。",
     "为何不能把Pailitao的完整线上增益当作Sample–Beam一个模块的因果收益？",
     "线上测的是完整部署配置，含训练数据、模型和最终呈现/混排。模块作用由匹配控制的离线消融提供不同证据，二者不可直接等同；本地仅资料收录，也没有可执行接口。",
     "教学例：换了训练数据、模型和候选混排后交易增加，不能仅因同时用了新beam配方就把全部提升归给beam。",
     {"pailitao-mmsearch2": ("统一图文到SID集合，多意图/预算训练与Sample–Beam服务对齐。", "完整多模型多阶段和私有生产实验高成本不复现；无本地占位模型。")}),
    ("multimodal-models", "alignment-interfaces", [], ["embedding-gemma2"],
     "EmbeddingGemma 2新正式论文对应已有10月6日模型，不再增加重复身份。论文明确512维骨干均值后投影到768；固定官方实现已把线性投影放在last_hidden_state返回前，同权mask均值与投影可交换。本地旧16图GPU结果保持原等级，不能因论文发布升级为音频/视频或七套benchmark验收。",
     "正式论文顺序与官方代码顺序不同，何时可以沿用既有结果？",
     "先核实际算子。这里同一个无偏置线性投影与同权mask均值可交换，且运行源码和checkpoint未变；若是非线性、不同权重或重新训练，则不能据此自动等价。当前只更新文献来源。",
     "教学例：mean(W h1,W h2)=W mean(h1,h2)；mean(GELU(h1),GELU(h2))通常不是GELU(mean(h1,h2))。", {}),
    ("agent-research", "tools-and-collaboration", [], ["rpl"],
     "Meta官方retrieval-programs现已可核验，更新RPL旧条目的开源状态；主体CC-BY-NC4，vendored检索/训练组件保留各自许可。代码公开不等于本地typed grammar突然覆盖任意Python、跨轮状态、神经检索或RL；本轮未复制源码或改变原L1证据。", 
     "官方仓库补上后，为何仍需保留RPL本地组件边界？",
     "来源完整性与执行保真度是两条轴。拿到完整训练代码并未使已有受限SDK执行完整策略、神经检索或蒸馏；若以后接入，需要另定成本、真实运行与许可边界。",
     "教学例：原来能检查检索程序语法，现在知道官方训练入口，也不能把语法测试改叫多跳QA评测。", {}),
]


def main():
    records = {}
    for path in (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json"):
        row = json.loads(path.read_text())
        records[f'{row["domain"]}:{row["key"]}'] = row
    for theme, topic, additions, changed, body, question, answer, example, comparisons in UPDATES:
        identity = lambda key: key if ":" in key else f"{theme}:{key}"
        additions, changed = list(map(identity, additions)), list(map(identity, changed))
        affected = additions + changed
        topic_path = ROOT / f"docs/learning/topics/{theme}.json"
        topics = json.loads(topic_path.read_text())
        target = next(t for t in topics["topics"] if t["id"] == topic)
        deep_path = ROOT / f"docs/learning/deep-dives/{theme}.json"
        deep = json.loads(deep_path.read_text())
        record = deep["topics"][topic]
        if any(u["date"] == DATE and set(u["papers"]) == set(affected) for u in record["updates"]):
            raise ValueError("authored update already applied; do not silently re-approve edited sources")
        for item in additions:
            if item in target["papers"]:
                raise ValueError("new membership already exists")
            target["papers"].append(item)
            record["reviewed_papers"].append(item)
        representative = record["comparisons"][0]["paper"]
        linked = list(dict.fromkeys([representative, *affected]))
        record["analysis"].append({"title": "10月29日：新方法与来源变化", "body": body, "papers": linked})
        record["questions"].append({"id": "oct29-method-boundary", "question": question,
            "answer": answer, "example": example, "papers": linked})
        for key, (position, tradeoff) in comparisons.items():
            record["comparisons"].append({"paper": identity(key), "position": position, "tradeoff": tradeoff,
                                          "sections": ["背景与主要改动", "核心公式"]})
        record["updated"] = DATE
        record["updates"].append({"date": DATE, "summary": body, "papers": affected,
            "source_revisions": {key: hashlib.sha256((ROOT / "docs" / records[key]["detail_path"]).read_bytes()).hexdigest()
                                 for key in affected}})
        for path, value in ((topic_path, topics), (deep_path, deep)):
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
