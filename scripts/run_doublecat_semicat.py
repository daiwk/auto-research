"""Train true bidirectional diffusion LMs on isolated public WikiText bytes."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import torch

from auto_research.foundation_models.doublecat_semicat import DiffusionLM, corrupt, denoising_loss, sample
from auto_research.foundation_models.oct13_runtime import check_dataset_identity

WIKITEXT_ID = "Salesforce/wikitext"
WIKITEXT_REVISION = "b08601e04326c79dfdd32d625aee71d232d685c3"


class ForwardAudit:
    """Count actual model calls, including detached SC and evaluation calls."""

    def __init__(self, model):
        self.phase = "training"
        self.counts = {phase: {"total": 0, "with_grad": 0, "no_grad": 0}
                       for phase in ("training", "validation", "test", "sampling")}
        self.handle = model.register_forward_pre_hook(self.record)

    def record(self, _model, _inputs):
        count = self.counts[self.phase]
        count["total"] += 1
        count["with_grad" if torch.is_grad_enabled() else "no_grad"] += 1


def read_blocks(path: Path, length: int, limit: int, device: str) -> torch.Tensor:
    data = path.read_bytes()
    count = min(len(data) // length, limit)
    if count < 2:
        raise ValueError("at least two independent raw-byte text blocks required")
    return torch.tensor(list(data[:count * length]), device=device).reshape(count, length)


@torch.no_grad()
def evaluate(model, tokens, method: str, seed: int) -> float:
    model.eval()
    generator = torch.Generator(device=tokens.device).manual_seed(seed)
    times = torch.full((len(tokens),), .5, device=tokens.device)
    corruption = corrupt(tokens, 256, times, method=method, generator=generator)
    return float(denoising_loss(model, tokens, corruption, use_self_condition=model.self_conditioning,
                                l2_weighting=False, reduction="per_unrevealed_token"))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--dataset-id", required=True)
    p.add_argument("--dataset-revision", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", default="cuda")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=40)
    p.add_argument("--sequence-length", type=int, default=32)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--width", type=int, default=64)
    p.add_argument("--layers", type=int, default=2)
    p.add_argument("--nfe", type=int, default=32)
    p.add_argument("--self-conditioning", action=argparse.BooleanOptionalAction, default=False,
                   help="opt-in standard Eq. 2.5/Table 8 ablation; not DoubleCat's free two-level mechanism")
    p.add_argument("--self-conditioning-probability", type=float, default=.5,
                   help="local Bernoulli p_sc for the optional ablation; the paper does not fix its value")
    args = p.parse_args()
    if min(args.steps, args.batch_size, args.nfe) < 1:
        p.error("positive train and sampling budgets required")
    if not 0 <= args.self_conditioning_probability <= 1:
        p.error("self-conditioning probability must be in [0,1]")
    if args.dataset_id != WIKITEXT_ID or args.dataset_revision != WIKITEXT_REVISION:
        p.error("this public protocol requires the fixed Salesforce/wikitext revision")
    dataset_manifest = check_dataset_identity(args.data, args.dataset_id, args.dataset_revision,
                                             ("train.txt", "validation.txt", "test.txt"))
    if dataset_manifest.get("configuration") != "wikitext-2-raw-v1":
        p.error("this small protocol requires the verified wikitext-2-raw-v1 mirror")
    train = read_blocks(args.data / "train.txt", args.sequence_length, 64, args.device)
    validation = read_blocks(args.data / "validation.txt", args.sequence_length, 8, args.device)
    results, models, audits = {}, {}, {}
    for method in ("onehot", "doublecat", "semicat"):
        torch.manual_seed(args.seed)
        model = DiffusionLM(width=args.width, layers=args.layers, length=args.sequence_length,
                            self_conditioning=args.self_conditioning).to(args.device)
        audit = ForwardAudit(model)
        parameters = list(model.parameters())
        before = torch.cat([p.detach().flatten() for p in parameters]).clone()
        optimizer = torch.optim.AdamW(parameters, lr=1e-3)
        generator = torch.Generator(device=args.device).manual_seed(args.seed)
        history, selected, best, sc_steps = [], None, float("inf"), 0
        for step in range(args.steps):
            model.train()
            audit.phase = "training"
            indices = torch.randint(len(train), (args.batch_size,), device=args.device, generator=generator)
            tokens = train[indices]
            time = torch.rand((len(tokens),), device=args.device, generator=generator) * .998 + .001
            corruption = corrupt(tokens, 256, time, method=method, generator=generator)
            optimizer.zero_grad()
            use_sc = args.self_conditioning and bool(torch.rand((), device=args.device, generator=generator)
                                                     < args.self_conditioning_probability)
            sc_steps += int(use_sc)
            loss = denoising_loss(model, tokens, corruption, use_self_condition=use_sc)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(parameters, 1.)
            optimizer.step()
            history.append(float(loss.detach()))
            if step == args.steps - 1 or (step + 1) % 10 == 0:
                audit.phase = "validation"
                score = evaluate(model, validation, method, args.seed + 10000)
                if score < best:
                    best, selected = score, copy.deepcopy(model.state_dict())
        model.load_state_dict(selected)
        results[method] = {"validation_denoising_ce_t05": best,
                           "training_loss_history": history,
                           "standard_self_conditioning_steps": sc_steps,
                           "parameter_delta_l2": float((torch.cat([p.detach().flatten() for p in parameters]) - before).norm())}
        models[method] = model
        audits[method] = audit
    # All architecture/training/checkpoint selection has completed before test
    # bytes are tokenized/evaluated. The earlier manifest hash check is only an
    # integrity operation. Neither test/reference text enters sampling.
    test = read_blocks(args.data / "test.txt", args.sequence_length, 8, args.device)
    for method, model in models.items():
        audit = audits[method]
        audit.phase = "test"
        results[method]["test_denoising_ce_t05"] = evaluate(model, test, method, args.seed + 20000)
        audit.phase = "sampling"
        sampled, diagnostic = sample(model, 4, args.sequence_length, method=method, steps=args.nfe,
                                     generator=torch.Generator(device=args.device).manual_seed(args.seed + 30000))
        histogram = torch.bincount(sampled.flatten(), minlength=256).float()
        distribution = histogram / histogram.sum()
        entropy = float(-(distribution * distribution.clamp_min(1e-12).log()).sum())
        results[method].update(sampling=diagnostic, sampled_byte_entropy=entropy,
                               generated_hex=[bytes(row).hex() for row in sampled.cpu().tolist()],
                               actual_denoiser_forward_calls=audit.counts)
        expected_training = args.steps + results[method]["standard_self_conditioning_steps"]
        if audit.counts["training"]["total"] != expected_training or audit.counts["sampling"]["total"] != args.nfe:
            raise RuntimeError("actual model calls must match the declared training/SC/NFE budget")
        audit.handle.remove()
    report = {"paper": "2610.13834", "seed": args.seed, "diagnostic_only": True,
              "promotion_eligible": False, "fidelity": "core_mechanism", "evaluation_tier": "l1_mechanism",
              "dataset": {"id": args.dataset_id, "revision": args.dataset_revision,
                          "split_hashes": {name: dataset_manifest["files"][f"{name}.txt"]
                                           for name in ("train", "validation", "test")},
                          "configuration": dataset_manifest["configuration"],
                          "all_input_hashes_verified": True},
              "checkpoint": {"id": "random-initialized bidirectional DiT denoiser",
                             "revision": "doublecat-semicat-byte-dit-v2-no-extra-forward-core", "seed": args.seed},
              "steps": args.steps, "sequence_length": args.sequence_length, "width": args.width,
              "layers": args.layers, "self_conditioning": args.self_conditioning,
              "standard_self_conditioning_probability": args.self_conditioning_probability if args.self_conditioning else 0.,
              "self_conditioning_protocol": "optional standard Eq. 2.5 ablation" if args.self_conditioning else "off; two-level interpolant only",
              "training_objective": {"loss": "unrevealed position sum, batch mean",
                                     "l2_weighting": "Appendix E.1: divide CE by sg(sqrt(||pi-X1||_2 + 1e-2))"},
              "reported_ce": "unweighted mean over unrevealed tokens at t=0.5",
              "gamma": "linear t", "kappa": "sqrt(t)", "simplex_prior": "Dirichlet(1)",
              "results": results, "test_isolated_from_selection": True,
              "limitations": ["small random-initialized byte-vocabulary diffusion LM",
                               "WikiText-2, not TinyGSM/OpenWebText paper benchmark",
                               "denoising CE is not exact likelihood or GPT-2 generative perplexity",
                               "no downstream reasoning accuracy, scaling or stable uplift claim"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
