from __future__ import annotations

import json


def render_report(result: dict) -> str:
    baseline = result["results"]["item_transformer"]
    method = result["results"]["sessionrec_transformer"]
    gain = 100 * (method["ndcg_at_20"] - baseline["ndcg_at_20"]) / max(baseline["ndcg_at_20"], 1e-12)
    return f"""# SessionRec 本地复现结果\n\n- 数据：{result['dataset']}\n- Item Transformer NDCG@20：{baseline['ndcg_at_20']:.6f}\n- SessionRec NDCG@20：{method['ndcg_at_20']:.6f}\n- 相对变化：{gain:+.2f}%\n\n```json\n{json.dumps(result, ensure_ascii=False, indent=2)}\n```\n"""
