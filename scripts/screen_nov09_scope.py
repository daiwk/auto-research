"""Resolve explicit cross-domain collisions without guessing review or cost."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re

from build_nov09_review_inventory import MODES, RUNS, TRACKS, read


@dataclass(frozen=True)
class Rule:
    key: str
    title: str
    corroboration: str
    reason: str


# Signals are restricted to the *subject* of a study, not a missing A/B or
# amount of retrieval overlap. Vetoes intentionally favor false negatives.
RULES = (
    Rule("wireless_physical_layer",
         r"\b(?:NOMA|OFDMA|ISAC|beamforming|MIMO|beam steering|reconfigurable intelligent surfaces?|"
         r"radio resource|mmwave|cell.free networks?|channel estimation|spectrum sensing|waveform design)\b",
         r"\b(?:channel|spectral efficiency|signal.to.noise|base station|wireless|antennas?|uplink|downlink)\b",
         "无线通信物理层、资源配置或信号估计，不是本库研究的模型或服务。"),
    Rule("physical_science_measurement",
         r"\b(?:inertial odometry|synthetic aperture radar|seismic inversion|seismic imaging|"
         r"fluid dynamics|astrophysical|gravitational waves?|radio interferometry|magnetohydrodynamic|"
         r"finite element|molecular dynamics|quantum monte carlo|lattice boltzmann)\b",
         r"\b(?:estimat\w*|simulat\w*|solv\w*|reconstruct\w*|measure\w*|predict\w*)\b",
         "主任务是物理测量、反演、数值求解或专用模拟。"),
    Rule("power_and_process_control",
         r"\b(?:power grid|distribution grids?|microgrids?|power systems?|power dispatch|economic dispatch|"
         r"wind turbines?|electric vehicle charging|water distribution networks?|voltage regulation|battery management)\b",
         r"\b(?:power|energy|flow|control|scheduling|simulation|forecasting|optimization)\b",
         "工程对象是能源或流体设施的控制、调度、预测或优化。"),
    Rule("unimodal_biomedical_imaging",
         r"\b(?:fundus|retinal|histopathology|mammography|magnetic resonance imaging|cardiac magnetic resonance|"
         r"computed tomography|X.ray|ultrasound|endoscopic)\b",
         r"\b(?:segment\w*|classif\w*|detect\w*|reconstruct\w*|lesions?|volumes?|tissues?)\b",
         "医学图像的专用检测、分类、分割或重建；没有通用模型机制证据。"),
    Rule("crop_and_ecology",
         r"\b(?:crop yield|fertili[sz]er|fruit disease|plant disease|crop health|agricultural irrigation|"
         r"forest biomass|forest inventory|ecological species|species distribution)\b",
         r"\b(?:crop|agricultur\w*|soil|harvest|forest|species|vegetation|farm\w*)\b",
         "主贡献是农业或生态专用预测和管理，不是工业搜广推或通用 AI 方法。"),
    Rule("classical_statistics",
         r"\b(?:gaussian processes|finite.sample bounds|nonconvex optimization|"
         r"randomized block coordinate descent|survey sampling|missing not at random|"
         r"survival analysis|instrumental variable|causal forests?)\b",
         r"\b(?:asymptotic|convergence|covariance|estimator|bounds?|identifiability|hypothesis test|theorem)\b",
         "主贡献是经典统计估计或数学优化分析，未指向本库的研究对象。"),
    Rule("clinical_or_social_observation",
         r"\b(?:retrospective cohort|ecological study|case.control study|randomized clinical trial|"
         r"clinical outcomes|clinical epidemiology|population prevalence)\b",
         r"\b(?:patients?|incidence|hospital|participant|hazard ratio|cohort|prevalence)\b",
         "临床或人群观察、试验或统计分析，而非本库的模型方法或标准评测。"),
    Rule("engineering_vision_specialist",
         r"\b(?:vessel classifiers?|stereo matching|human mesh recovery|optic flow estimation|"
         r"road surface distress|skin lesion segmentation|industrial defect detection|"
         r"SLAM|laser scanning|LiDAR.inertial|terrain models?|as.built BIM)\b",
         r"\b(?:camera|stereo|mapping|recognition|reconstruction|segmentation|"
         r"detection|positioning|classification|sensing|classifier)\b",
         "专用视觉识别、定位或重建任务，摘要未给出通用模型或本库研究方向。"),
    Rule("formal_math_or_statistics",
         r"\b(?:Bernstein inequalities|oracle complexity|graphical separation criteria|Haussler lemma|"
         r"conditional independence test|regenerative processes|confidence bands for distribution functions|"
         r"stationary distribution estimation|von mises|finite.sample confidence|"
         r"correlation analysis|risk conversion|minimax adaptation|convex cones)\b",
         r"\b(?:theorem|theoretical|inequalit\w*|estimat\w*|bound\w*|statistic\w*|convergence|proof)\b",
         "主贡献为数学或统计理论，不属于通用模型、后训练、Agent 或工业搜广推。"),
    Rule("specialized_hardware_and_signals",
         r"\b(?:SRAM|brain.computer inference|transmission electron microscopy|"
         r"bandit channel selection|Doppler|ray.tracing based automotive|"
         r"acoustic signature optimisation|wave spectra|antenna arrays?)\b",
         r"\b(?:hardware|signal|radar|wireless|physical|acoustic|energy|predict\w*|estimat\w*)\b",
         "硬件、电磁、声学或专用信号研究，不把泛优化或推理命中当成核心主题。"),
    Rule("specialist_control_or_simulation",
         r"\b(?:inverse design|biomimetic robots?|insect flight|hydraulic control|"
         r"hybrid rigid.continuum space manipulator|wind farm|"
         r"tropical cyclone attributes|aerodynamic configuration)\b",
         r"\b(?:engineering|robotics?|manipulat\w*|flight|simulation|control|weather|dynamics)\b",
         "具体物理对象的仿真、设计或控制研究，没有通用模型机制证据。"),
    Rule("biology_and_clinical_specialist",
         r"\b(?:DNA methylation|RNA ensemble|ACL risk|anterior cruciate ligament|"
         r"prostate surgical phantoms?|renal tumor classification|"
         r"medical image registration|ADNI|cell painting|exchange.correlation functionals?)\b",
         r"\b(?:clinical|patients?|biomedical|molecular|biomarker|MRI|"
         r"simulation|diagnos\w*|classif\w*|segment\w*|spectral)\b",
         "专用生物或临床任务，没有独立的本库模型方法或评测依据。"),
)

VETO = re.compile(
    r"\b(?:LLMs?|VLMs?|MLLMs?|LVLMs?|VLA|GPT\w*|Claude|Gemini|Llama\w*|Qwen\w*|Mistral|"
    r"language models?|foundation models?|vision.language|multimodal|world models?|JEPA|JEV|"
    r"generative models?|pre.train\w*|fine.tun\w*|attention|transformers?|sparse autoencoders?|"
    r"agents?|agentic|in.context|autoregressive|tool.use|harness|"
    r"large language|language flows?|tokeniz\w*|speculative decoding|mixture.of.experts|MoE|"
    r"world.action|latent world|self.supervised|benchmarking AI|autonomous|model.hardware co.design|"
    r"recommenders?|recommendation systems?|retrieval|ranking|advertis\w*|e.commerce|"
    r"production|live traffic|A/B|full.traffic|"
    r"post.training|distillation|RLHF|GRPO|DPO|reward models?|reinforcement learning)\b", re.I,
)


def scope_decision(candidate: dict) -> dict | None:
    """Return only high-precision exclusions with a named primary metadata witness."""
    if (candidate.get("priority_review_required") or candidate.get("priority_query_matches")
            or candidate.get("priority_source_matches") or candidate.get("institutional_source")):
        return None
    title, abstract = candidate["title"], candidate["abstract"]
    if not title or not abstract or VETO.search(f"{title} {abstract}"):
        return None
    for rule in RULES:
        primary = re.search(rule.title, title, re.I)
        secondary = re.search(rule.corroboration, abstract, re.I)
        if primary and secondary:
            return {
                "rule": rule.key, "title_witness": primary[0], "abstract_witness": secondary[0],
                "reason": rule.reason,
            }
    return None


def evidence(source_dir: Path, queue: dict[str, list]) -> tuple[dict, dict]:
    candidates: dict[str, dict] = {}
    receipts: dict[str, str] = {}
    for run in RUNS:
        for track in TRACKS:
            for prefix in MODES.values():
                source = source_dir / run / f"{track}-paper-candidates" / f"paper-{prefix}-{track}.json"
                key = source.relative_to(source_dir).as_posix()
                receipts[key] = sha256(source.read_bytes()).hexdigest()
                for row in read(source)["candidates"]:
                    identity = row["arxiv_id"]
                    if identity not in queue or row["revision"] != queue[identity][1]:
                        continue
                    official = any(
                        "google" in str(ref.get("source_url", "")).lower()
                        or "meta" in str(ref.get("organization", "")).lower()
                        for ref in row.get("source_provenance", [])
                    )
                    previous = candidates.get(identity, {})
                    source_refs = list(previous.get("receipts", [])) + [key]
                    candidates[identity] = row | {
                        "priority_review_required": previous.get("priority_review_required")
                        or row.get("priority_review_required"),
                        "priority_query_matches": sorted(set(previous.get("priority_query_matches", []))
                                                         | set(row.get("priority_query_matches", []))),
                        "priority_source_matches": sorted(set(previous.get("priority_source_matches", []))
                                                          | set(row.get("priority_source_matches", []))),
                        "institutional_source": official or previous.get("institutional_source", False),
                        "receipts": source_refs,
                    }
    return candidates, receipts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--inventory", type=Path, required=True,
                        help="original, unreconciled pending inventory")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    prior_bytes = args.inventory.read_bytes()
    prior = json.loads(prior_bytes)
    queue = {r[0]: r for rows in prior["pending_identities_by_local_first_publication"].values() for r in rows}
    candidates, receipts = evidence(args.source_dir, queue)
    rows = []
    for identity, row in sorted(candidates.items()):
        match = scope_decision(row)
        if match:
            rows.append({
                "id": identity, "revision": row["revision"], "title": row["title"], "published": row["published"],
                "source_url": f"https://arxiv.org/abs/{identity}v{row['revision']}",
                "metadata_sha256": row["metadata_sha256"], "capture": row["receipts"][0],
                **match, "decision": "out_of_scope", "review_done": True, "fulltext_review_completed": False,
                "automatic_retry": False, "automatic_implementation_queue": False,
            })
    counts = dict(sorted(Counter(row["rule"] for row in rows).items()))
    value = {
        "schema_version": 1, "review_scope": "explicit_cross_domain_primary_metadata_only",
        "fulltext_or_cost_inferred": False, "terminal_window_scope_only": True,
        "input_inventory_sha256": sha256(prior_bytes).hexdigest(),
        "examined_candidates": len(candidates), "counts": counts, "source_receipts": receipts, "records": rows,
    }
    args.output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"examined": len(candidates), "closed": len(rows), "counts": counts}))


if __name__ == "__main__":
    main()
