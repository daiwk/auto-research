"""Reproduce the manually checked specialist/survey scope decisions."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from screen_nov09_scope import evidence


# Each decision was checked against the pinned title and its source abstract.
# The short witnesses let the reconciliation validate that the evidence still
# belongs to the same revision. No wildcard rule can generate a new exclusion.
DECISIONS = (
    ("2610.23834", "quantum circuits", "radar-like tasks", "任务对齐的量子电路频谱归纳偏置，以小规模频谱和雷达分类验证；不是本库模型架构。"),
    ("2610.24858", "MRI Super-Resolution", "brain-parcellation agreement", "专用各向异性 MRI 超分重建；以病灶敏感度和脑区分割保真度为终点。"),
    ("2610.26239", "Job-Shop Scheduling", "public FJSP benchmarks", "柔性作业车间排程的神经组合求解器；求解可行性及速度质量与工业搜广推无关。"),
    ("2610.27264", "Theorem prover Arend", "formalizations in constructive algebra", "已有 Arend 形式证明语言及 IDE 的说明文章，无学习式证明 Agent。"),
    ("2610.28747", "Reverse-Gold Theorem", "substitutable context-free languages", "正样本形式语言可识别性的理论结果，验证对象是形式语言类而非大模型训练。"),
    ("2610.28791", "LiDAR-Camera Calibration", "the rigid discrepancy", "利用目标物估计和检验传感器刚体外参；不是通用模型或机器人策略。"),
    ("2610.28968", "Quantum Machine Learning", "quantum computer", "可穿戴健康数据的差分隐私量子分类及量子机小试；无本库模型方法。"),
    ("2610.29141", "MRI Synthesis", "3T-to-7T MRI datasets", "三特斯拉到七特斯拉 MRI 专用图像合成与结构保真；非通用生成模型预训练。"),
    ("2610.29220", "Multistage Manufacturing", "LiquidSugar dataset", "多阶段制造的延迟对齐和成品质量预测；不涉及广告、检索或推荐。"),
    ("2610.29311", "Mixed-Integer Linear Programming", "SCIP's default cut selection", "遗传编程给整数规划求解器选择割平面；以 SCIP 求解时长为指标。"),
    ("2610.29586", "Quadrupedal Jumping in Lunar Gravity", "lunar-gravity offloading", "控制四足在低重力下起跳；以卸载重力装置、功率和硬件极限验证，不是语言后训练。"),
    ("2610.29617", "Endoscopic Segmentation", "compact low-bit hardware", "针对内镜分割的特制小网络及 45 nm 算术阵列，不是通用模型的量化方法。"),
    ("2610.30080", "Controllers Walk on the Moon", "lunar regolith", "人形行走控制在月面重力与土壤接触仿真中的迁移；不是可通用 VLA 策略。"),
    ("2610.30109", "Gaussian Mixtures", "local Hellinger bracketing entropy", "高斯混合非参数最大似然的 Hellinger 风险与证明。"),
    ("2610.36097", "Online Linear Optimisation", "coefficient of the expected regret", "在线线性优化的 regret 上界及正则化系数理论，不是在线推荐实验。"),
    ("2610.36428", "Multiple Sclerosis Lesions", "lesion forecasting", "多发性硬化患者 MRI 病灶未来位置预测的临床专题研究。"),
    ("2610.36440", "thermodynamics of liquid mixtures", "multi-phase equilibria", "拟合混合物活度系数并预测相平衡；针对化工热力学。"),
    ("2610.36984", "Quantum Evolution Kernel", "Pasqal's Pulser library", "中性原子量子图核的专用模拟，示例是数字识别。"),
    ("2610.37021", "Crop Classification", "17 crop classes", "将地面照片监督蒸馏到卫星作物分类，终点是地区/时间迁移；非大模型后训练。"),
    ("2610.37045", "CNOT Decompositions", "quantum circuit compilation", "贡献是约束拓扑上的量子电路分解与等式，不是可复用的研究 Agent 或其评测。"),
    ("2610.37134", "MRI-to-CT Translation", "preoperative planning", "专用脊椎医学模态转换，用于术前影像，不是通用图文或扩散预训练。"),
    ("2610.37199", "Lunar Monoped", "2D jump", "月面单腿机器人的形态/轨迹协同优化与着陆控制。"),
    ("2610.37213", "clinical MRI", "MPF mapping", "用 MRI 成像物理估计髓鞘相关 MPF 成像量；目标不是通用视觉表征。"),
    ("2610.37310", "Periodic Orbits Stabilization", "orbital stabilization", "周期轨道稳定性的控制器设计，在 butterfly robot 轨迹上验证。"),
    ("2610.37965", "Medical Image Registration", "Jacobian determinant", "医用可变形配准初始化的迭代预算比较，以形变与配准误差评价。"),
    ("2611.02091", "Financial Forecasting", "probabilistic forecasts", "市场状态下的量子混合时间序列预测，不是商业搜索或推荐排序。"),
    ("2611.08544", "Strain Maps", "cardiac function assessment", "从心脏 MRI 生成运动和应变图；临床影像量测专题。"),
    ("2611.08771", "Brain MRI Synthesis", "multi-site generative models", "多中心脑 MRI 专用联邦合成的集中/联邦对照，不是通用基础模型。"),
    ("2611.08962", "medical image segmentation", "regional calibration", "医学像素级误差报警的区域校准，评价病灶分割覆盖而非 LLM 置信度。"),
    ("2611.09156", "Rainfall Detection", "neighboring links", "用卫星微波链路识别降雨，比较 RF/CNN 的气象检测。"),
    ("2611.09309", "Retinal Classification", "BRSET dataset", "眼底照片和患者风险因素的病种图分类；不是通用多模态基础模型。"),
    ("2611.09436", "Medical Image Segmentation", "Kvasir- SEG and ARCADE", "比较医疗分割的循环细化块与噪声稳健性，没有通用视觉模型对照。"),
    ("2611.09703", "Post-Quantum Cryptography", "SSH hosts on port 22", "实测 SSH 后量子密码采用率的统计，不是模型、Agent 或评测协议。"),
    ("2611.09707", "Cryptography Adoption", "baseline Cloudflare datasets", "统计 TLS 后量子密码支持情况，不是本库 AI 方法或证据。"),
    ("2610.24275", "bilingual naming performance", "Boston Naming Test", "用自组织映射模拟双语命名行为的认知模型，不是语言模型训练。"),
    ("2610.28133", "Wage Growth", "cross-occupational distribution of tasks", "职业任务结构与工资变化的实证经济学。"),
    ("2610.24492", "Backend-Frontend Converter", "C#/TypeScript boundary", "固定 .NET 组件迁移和等价性核对，不是智能体或模型迁移。"),
    ("2610.28912", "Simply Logical", "Prolog teaching materials", "Prolog 课本与教学工具演进，不是可执行的论文研究算法。"),
    ("2610.28878", "Privately Learnable", "standard definition of learnability", "差分隐私 PAC 可学习性的理论证明，没有语言模型或算法实训。"),
    ("2610.29030", "Printable Humanoid", "3D printer", "可打印灵巧手的结构、连杆和原型测试，不是世界模型或 VLA。"),
    ("2610.28687", "Surface Technosignatures", "Mars Reconnaissance Orbiter", "行星表面潜在人工结构的观测研究，摘要中模型仅为后续方案。"),
    ("2610.28699", "A survey", "RL-driven hardware systems", "综述专用硬件上的强化学习与芯片实现，不是本文原创后训练算法。"),
    ("2611.02049", "A Survey", "physics-based rewards", "高能物理应用强化学习的综述，研究总结而非新后训练方法。"),
    ("2611.09075", "Practitioners Survey", "reviews the latest techniques", "端侧 LLM 部署技术的二手综述，没有新推理算子或新标准评测。"),
    ("2611.00171", "A Survey", "survey over 100 papers", "已有 Text-to-SQL 模型、范式和资料的综述，未给出原创实现对象。"),
    ("2610.31304", "A Survey", "specialized RS sub-fields", "遥感视觉语言资料综述与未来路线，未交付新通用模型、数据或训练方法。"),
)


def build(source_dir: Path, raw_inventory: bytes) -> dict:
    inventory = json.loads(raw_inventory)
    queue = {
        row[0]: row for rows in inventory["pending_identities_by_local_first_publication"].values()
        for row in rows
    }
    candidates, receipts = evidence(source_dir, queue)
    records = []
    for identity, title_witness, abstract_witness, reason in DECISIONS:
        row = candidates[identity]
        if (title_witness.casefold() not in row["title"].casefold()
                or abstract_witness.casefold() not in row["abstract"].casefold()
                or any(row.get(k) for k in ("priority_review_required", "priority_source_matches",
                                            "priority_query_matches", "institutional_source"))):
            raise ValueError(f"{identity}: scope exclusion lost its witness or requires priority review")
        records.append({
            "id": identity, "revision": row["revision"], "title": row["title"], "published": row["published"],
            "source_url": f"https://arxiv.org/abs/{identity}v{row['revision']}",
            "metadata_sha256": row["metadata_sha256"], "capture": row["receipts"][0],
            "rule": "reviewed_specialist_scope", "title_witness": title_witness, "abstract_witness": abstract_witness,
            "reason": reason, "decision": "out_of_scope", "review_done": True, "fulltext_review_completed": False,
            "automatic_retry": False, "automatic_implementation_queue": False,
        })
    return {
        "schema_version": 1, "review_scope": "individual_specialist_title_and_abstract_scope_only",
        "fulltext_or_cost_inferred": False, "terminal_window_scope_only": True,
        "input_inventory_sha256": sha256(raw_inventory).hexdigest(),
        "counts": dict(Counter(row["rule"] for row in records)), "source_receipts": receipts, "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.source_dir, args.inventory.read_bytes())
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
