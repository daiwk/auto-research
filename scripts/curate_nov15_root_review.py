"""Record individually inspected original-source decisions, never implementations."""
from __future__ import annotations

import json
from hashlib import sha256

from prepare_nov15_review_closure import AUDIT, CACHE, WINDOW, write

# Each explanation refers to the fixed manuscript sections read for this window.
# 'Fulltext' below means those necessary original sections, not a claim of reading
# every word, validating a theorem, training a model or reproducing a result.
SCOPE = {
    "2604.01171": "Open-Industry 的20类工业点云与正常/已知/未知缺陷实验；production指采集产线，不是本库搜广推线上或通用基础模型。",
    "2609.35075": "ReCo在Plegma上回放传感器套件重定位，部署是NILM仪表采集计划，不是LLM Agent或推荐生产实验。",
    "2611.13203": "贡献是流体控制的模型式RL与审计梯度；对象为物理流场，而非语言后训练、通用VLA或搜广推。",
    "2611.13972": "旅游多模态推荐的数据质量问题讨论与领域数据描述，没有通过工业生产线上门槛的算法对照。",
    "2611.14100": "SHROOM-Visions共享任务的字符级幻觉跨度检测系统；deployed仅推理配置，未作为本窗口重点通用方法收录。",
    "2611.15162": "智能电网GAN攻击在冻结的离线72小时块上评测；不是线上A/B，也非本库LLM/Agent后训练。",
    "2611.17463": "电弧炉温度及12种成分的历史反馈回归，production为炼钢时间记录，非本库广告/审核/推荐决策。",
    "2611.18189": "句子级手语模板检索与姿态生成，production指手语产出；本轮不选择这一专用姿态生成方向。",
    "2611.18253": "单服装准静态神经形变及局部梯度直方图损失，production指动画资产生产，不是通用基础模型。",
    "2611.19061": "LLM用于AI基础设施的分类综述和异质结果综合，不是新可独立复现算法或统一公开基准；本窗口不收录。",
    "2611.19525": "将临床投诉拆成可判定判断并审计1446份医疗笔记，属于专用临床评测；production notes不是搜广推流量A/B。",
}
NO_PRODUCTION = {
    "2604.14586": "CPGRec+的PER/PRG模块在Steam I/II离线比较准确性与多样性；实验和附录未建立真实生产随机A/B。",
    "2604.14833": "SF-UBM使用三个跨域公开数据对、软prompt与事实/反事实蒸馏；正文实验为离线HR/Valid Ratio，不是隐私生产A/B。",
    "2610.40658": "CEU用因果解释在输出分数层做遗忘；三个公开数据集的离线遗忘/推荐效用不能替代真实线上实验。",
    "2611.13914": "将反事实推荐编辑转成LLM解释的人类叙述研究；用户解释评估不是生产推荐效果A/B。",
    "2611.14004": "LUMIR对异构模态做解耦表示并在下一POI任务离线评估；未报告真实产品流量随机实验。",
    "2611.15160": "在TN/QB/EB-NeRD上审计13类推荐模型的有害内容传播；离线交互和安全指标不等于生产A/B。",
    "2611.16139": "短信风控有真实私有日志及已部署DistilBERT，但8749条留出集与2万条平衡生产评估并不同切分；新TemporalBertSpam的公平对照尚列未来工作，无生产对照A/B。",
    "2611.16159": "TraGR并行SID、概率反馈和轨迹关系学习在四个公开数据集验证，没有正文生产流量实验。",
    "2611.17921": "RecMem在MerRec上比较16记忆槽与HSTU历史，明确说明系统结果不是端到端生产服务，故不能因推荐/效率题目进入工业P0。",
    "2611.18027": "电商缓存危害排序在1270万请求实迹做因果归属和回放；是回顾性干预设计，不是真实生产随机分流A/B。",
    "2611.18244": "RACE为不确定性感知容量定制的序列推荐，正文公共数据离线精度/资源评估，没有真实用户生产对照。",
}
HIGH = {
    "2610.24122": ("HAVANA双系统未来隐计划/局部反应路径及三种机器人迁移与真实机器人验证。", "未来视觉监督世界模型、多embodiment导航与真机；完整链路超出一次单卡廉价诊断", "§3方法、§4.1设置与§4.4真实导航"),
    "2610.29922": ("四个8B/12B骨干的48个价值适配器及跨价值行为审计。", "原文8H100；训练120 GPU小时、评估400 GPU小时", "Appendix B训练及末尾资源披露"),
    "2610.15020": ("PATTERN记忆泄漏与未见图模式的修订结果，不把官方高分当泛化。", "原文GRASS/PPGT为200 epochs、3 seeds、每seed约20小时T4，另多模型对照", "实验与复现说明、训练配置"),
    "2611.07854": ("Drex四种typed decision模型、选项置换稳定性与RLAF。", "8B/9B/35B/27B四模型、1150460决策训练记录、多套公开/私有决策评测与B200/B300服务", "§3—6模型/数据、§9及附录推理优化"),
    "2611.08577": ("MR0三阶段VLA及Rollback/CFG-DAgger，保留真机与仿真证据区别。", "147M图文样本、15060小时机器人轨迹、12 embodiments与真实硬件", "§2数据、训练阶段及真实机器人结果"),
    "2611.09949": ("区分视频计数的表征/读出失败、oracle符号与实际检测头。", "7B—30B多骨干、多干预训练、人工盲审视频与跨种子对照；完整campaign预计小时级", "§4—6结果、REALCOUNT与训练控制"),
    "2611.09964": ("六个VLA在四个LIBERO套件上比较示范数/训练步数，不将零样本优劣等同适配效率。", "6骨干×4套件×多示范预算与训练检查点、闭环评估", "实验设置与Appendix C各预算结果"),
    "2611.13378": ("Looped CED以递归深度和末轮KV控制内存，保留训练与服务压测区别。", "29.6B-token训练；552B DeepSeek骨干在4GB200/8H200节点压测", "§5.5、§6与Appendix I"),
    "2611.13393": ("Plumbline用生命周期检查和诊断规则追根，Amazon真实使用不是搜广推随机A/B。", "13框架—模型组合、3框架5模型Day-0及分布式生产训练故障复核", "系统设计、生产使用案例与实验配置"),
    "2611.14834": ("冻结VLA上学习低时延动作验证，不能把真机器人评估用mock替代。", "H100 80GB策略服务、40-epoch验证器、多任务闭环及真实机器人", "实验设置、Appendices B—D"),
    "2611.15250": ("QNN多头替换Qwen3层，原文纠缠/冻结控制还限制其特异优势结论。", "Qwen3-30B-A3B、精确量子态训练及156-qubit IBM Heron硬件", "模型手术、消融及硬件实验"),
    "2611.17560": ("可解释物理生成设计，完整空气动力学及燃烧室campaign不复现。", "原文空气动力代理A100 80GB训练190小时，燃烧室另74分钟及实测数据", "训练超参表与生成设计实验"),
    "2611.18908": ("MemeEconomy在模拟经济压力下审计BDI与有害内容选择，不是真实金融/用户生产A/B。", "10个模型、四个frontier家族、多轮市场及32B/27B等评估；完整API/推理campaign高成本", "方法、单/多Agent实验与模型表"),
    "2611.19858": ("BTG领域术语挖掘、过滤与SFT/RL，线上人工译文打分不等于生产流量A/B。", "5M样本、30K例10指标、Qwen3-8B SFT/RL及多frontier对照", "数据构造、训练范式与实验表"),
}
PRIVATE = {
    "2611.12727": ("Airbnb OptiCover通过生产门槛：表4明确访客级随机分配，以当前房东封面为对照；首页CTR+1.5%，搜索bookers+0.35%，后者95%CI[0.01%,0.69%]；另一CTR增益不显著，不能混报。", "数亿私有图片、5周探索训练与2—6周百万/千万访客三项独立两臂A/B实验", "§4.3/4.7训练、§4.8及Table4线上对照"),
    "2611.14938": ("好奇心推荐在§7与附录D给出真实在线对照及生产近似计算；不是仅把问卷次序随机当A/B。完整私有平台实验不复现。", "私有生产用户/物品向量、消费状态与在线流量，另含人类问卷及线下对照", "§7在线控制实验、Appendix D"),
}
AFFORDABLE = {
    "2611.01514": "HVMap跨嵌入空间模糊对比映射与公开异构向量库协议可作为后续低成本组件候选；2.5M样本及1TB内存全评测不在本轮运行，QPS基准不是线上A/B。",
    "2611.12737": "Runway的SLA声明、不可变结果缓存和可追溯决策协议可独立实现；本文是引擎/实例压测与治理经验，不能转成线上收益。",
    "2611.13441": "tokenization premium/sovereignty cost是可复用测量定义；实际语言样本与模型对照未在本轮重跑，不从部署动机推导生产证据。",
    "2611.13758": "EEG/ECG weight-space programming比较LLM直接写权重与同架构梯度训练；可审查小网络接口，不能把API写权重当作反向传播训练复现。",
    "2611.14953": "RSLiveBench-UAV的时间窗、实体关联和确定性计分可作协议候选；production为数据答案生产，真实无人机采集与人工标注不在本轮实施。",
    "2611.15911": "路由成本阈值、校准与级联盈亏条件可做算术接口；§5/5.2的GSM8K分析与价格假设不是实际生产收益保证。",
    "2611.17726": "多模态数字图书馆嵌入与向量库扩展评测可作协议候选；十亿页规模为外推讨论，现有查询测试不证明生产随机A/B。",
    "2611.19840": "双judge/顺序交换/已知答案catch trials的协议与0.6B偏好训练是可审查候选；A/B swap为盲评顺序控制，不是生产A/B，负结果必须保留。",
}


def main() -> None:
    sources = {r["id"]: r for r in json.loads((CACHE / "root-fetch-receipts.json").read_bytes())["records"]}
    assigned = json.loads((CACHE / "assigned-root.json").read_bytes())["records"]
    result = []
    for record in assigned:
        identity, raw = record["id"], record["metadata"]
        source = sources[identity]
        if sha256((CACHE / source["path"]).read_bytes()).hexdigest() != source["source_sha256"]:
            raise ValueError(f"Source bytes changed: {identity}")
        base = {"id": identity, "revision": record["revision"], "title": raw["title"], "published": raw["published"],
                "metadata_sha256": raw.get("metadata_sha256"), "source_url": source["source_url"], "source_sha256": source["source_sha256"],
                "track": "foundation-model", "priority": "P1", "review_done": True, "fulltext_review_completed": True,
                "review_scope": "bounded-original-method-experiment-sections", "automatic_retry": False,
                "automatic_implementation_queue": False, "implementation_status": "not_implemented_by_review"}
        if identity in SCOPE or identity in NO_PRODUCTION:
            base.update(decision="out_of_scope" if identity in SCOPE else "rejected", priority="P2",
                        resolution="outside_current_topic_scope" if identity in SCOPE else "industrial_online_gate_not_met",
                        reason=(SCOPE | NO_PRODUCTION)[identity], locations=["原文方法", "实验设置/结果及限制"])
            if identity in NO_PRODUCTION:
                base["track"] = "recommendation"
        elif identity in HIGH or identity in PRIVATE:
            reason, scale, location = (HIGH | PRIVATE)[identity]
            resolution = "not_reproduced_private_data" if identity in PRIVATE else "not_reproduced_high_cost"
            base.update(decision="reviewed_deferred", resolution=resolution,
                        reason=reason + (" 私有数据/真实生产资源不可得，完整实验不复现（审查DONE）。" if identity in PRIVATE else " 成本过高，完整实验不复现（审查DONE）。"),
                        locations=[location], cost_assessment={"source_url": source["source_url"], "basis": location, "scale": scale,
                        "available_resource": "one A100 or A30, or local Mac", "cost_type": "published_configuration_and_resource_based_estimate_not_local_measurement"})
            if identity in PRIVATE:
                base.update(track="recommendation", priority="P0", production_gate_passed=True)
        elif identity in AFFORDABLE:
            base.update(decision="accepted", resolution="affordable_core_review_candidate", reason=AFFORDABLE[identity],
                        locations=["原文方法/协议", "实验与局限"], full_campaign_executed=False)
        else:
            raise ValueError(f"No individually authored decision: {identity}")
        result.append(base)
    write(AUDIT / "root-primary-reviews.json", {"schema_version": 1, "window": WINDOW, "reviewed_on": "2026-11-18",
          "scope": "Necessary original source sections, not whole-article verification; no implementation/training", "reviews": result})
    print(len(result))


if __name__ == "__main__":
    main()
