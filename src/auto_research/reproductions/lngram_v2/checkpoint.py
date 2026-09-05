"""Run Lngram v2 on real hidden states from a public VLM checkpoint."""

from __future__ import annotations
import argparse,json,time
from datetime import datetime,timezone
from pathlib import Path

from .model import LngramV2


def run(output:Path,model_id:str,revision:str,seed:int):
    import torch
    from huggingface_hub import model_info
    from PIL import Image, ImageDraw
    from transformers import AutoModelForImageTextToText,AutoProcessor
    torch.manual_seed(seed); resolved=model_info(model_id,revision=revision).sha
    processor=AutoProcessor.from_pretrained(model_id,revision=resolved)
    model=AutoModelForImageTextToText.from_pretrained(model_id,revision=resolved,torch_dtype=torch.bfloat16).cuda().eval()
    image=Image.new("RGB",(224,224),"white"); draw=ImageDraw.Draw(image); draw.rectangle((20,60,90,130),fill="red"); draw.ellipse((130,60,205,135),fill="blue")
    messages=[{"role":"user","content":[{"type":"image","image":image},{"type":"text","text":"Describe the relationship between the red square and blue circle."}]}]
    prompt=processor.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    inputs=processor(text=[prompt],images=[image],return_tensors="pt").to("cuda")
    torch.cuda.reset_peak_memory_stats(); start=time.perf_counter()
    with torch.inference_mode(): base=model(**inputs,output_hidden_states=True)
    torch.cuda.synchronize(); backbone_seconds=time.perf_counter()-start
    hidden=base.hidden_states[len(base.hidden_states)//2].float()
    module=LngramV2(width=hidden.shape[-1],routes=8,bits=3,memory_dim=32,orders=(1,2),heads=4).cuda()
    start=time.perf_counter(); augmented,diag=module(hidden,return_diagnostics=True); loss=(augmented-hidden).square().mean(); loss.backward(); torch.cuda.synchronize(); module_seconds=time.perf_counter()-start
    payload={"schema_version":3,"method":"lngram-v2-real-checkpoint","dataset":{"name":"deterministic RGB geometry multimodal probe","revision":"v1","examples":1,"tokens":int(hidden.shape[1])},"checkpoint":{"model_id":model_id,"revision":resolved},"setup":{"seed":seed,"routes":8,"bits":3,"orders":[1,2],"memory_dim":32},"metrics":{"finite_output":float(torch.isfinite(augmented).all()),"unique_route_ids":int(torch.unique(diag["route_ids"]).numel()),"sink_weight":float(diag["sink_weight"].detach()),"route_gradient_norm":float(module.route_projection.weight.grad.norm()),"backbone_seconds":backbone_seconds,"module_seconds":module_seconds,"peak_gpu_memory_mb":torch.cuda.max_memory_allocated()/1024**2},"created_at":datetime.now(timezone.utc).isoformat(),"scope":"Real public VLM checkpoint cross-modal hidden states with exact Lngram-v2 mechanism; not Keye-30B training or a paper-result claim."}
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(payload,indent=2)+"\n"); return payload


def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",type=Path,required=True); p.add_argument("--model-id",default="Qwen/Qwen2.5-VL-3B-Instruct"); p.add_argument("--revision",default="main"); p.add_argument("--seed",type=int,default=42); a=p.parse_args(); print(json.dumps(run(a.output,a.model_id,a.revision,a.seed)["metrics"],indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
