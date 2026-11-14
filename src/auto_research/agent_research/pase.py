"""PASE patch transaction and validation acceptance; no program execution or LLM."""
import ast
from dataclasses import dataclass, replace
from hashlib import sha256
import math

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class ProgramSkill:
    identity: str
    description: str
    program: str

    def __post_init__(self):
        if not all(isinstance(x, str) and x for x in (self.identity, self.description, self.program)):
            raise ValueError("identified textual skill and linked program required")
        if len(self.program) > 100_000:
            raise ValueError("program exceeds this reference component's size bound")
        ast.parse(self.program)  # Syntax validation is not safety or task correctness.

    @property
    def program_digest(self):
        return sha256(self.program.encode()).hexdigest()


@dataclass(frozen=True)
class ProgramPatch:
    skill_id: str
    expected_program_digest: str
    replacement_program: str
    replacement_description: str | None = None


@dataclass(frozen=True)
class PatchDecision:
    accepted: bool
    skill: ProgramSkill
    previous_digest: str
    proposed_digest: str


def apply_validated_patch(skill: ProgramSkill, patch: ProgramPatch, *, baseline_score: float,
                          candidate_score: float, split: str):
    """Apply equations 8-9 using externally measured validation scores.

    Does not execute candidate code, synthesize a patch, or impersonate an actor.
    A syntactically valid patch remains untrusted until external sandbox evaluation.
    """
    if split != "validation":
        raise ValueError("selection must use held-out validation, never test scores")
    if any(type(x) not in {int, float} or not math.isfinite(x)
           for x in (baseline_score, candidate_score)):
        raise ValueError("finite externally measured validation scores required")
    if patch.skill_id != skill.identity or patch.expected_program_digest != skill.program_digest:
        raise ValueError("patch target/preimage mismatch; stale updates are not applicable")
    candidate = replace(skill, program=patch.replacement_program,
                        description=(skill.description if patch.replacement_description is None
                                     else patch.replacement_description))
    accepted = candidate_score > baseline_score
    return PatchDecision(accepted, candidate if accepted else skill,
                         skill.program_digest, candidate.program_digest)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("PASE patch transactions are CPU-only")
    source = ProgramSkill("month", "Read the month mapping.", "def month(x):\n    return x[0]\n")
    patch = ProgramPatch("month", source.program_digest, "def month(x):\n    return x[1]\n")
    better = apply_validated_patch(source, patch, baseline_score=.5, candidate_score=.75, split="validation")
    tied = apply_validated_patch(source, patch, baseline_score=.5, candidate_score=.5, split="validation")
    worse = apply_validated_patch(source, patch, baseline_score=.5, candidate_score=.25, split="validation")
    test_rejected = False
    try:
        apply_validated_patch(source, patch, baseline_score=.5, candidate_score=1., split="test")
    except ValueError:
        test_rejected = True
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"accepted_patch_count": int(better.accepted), "rollback_count": 2},
            "checks": {"strict_validation_improvement": better.accepted,
                       "tie_and_decline_rollback": tied.skill is source and worse.skill is source,
                       "source_immutable": source.program_digest == patch.expected_program_digest,
                       "skill_program_pair_preserved": better.skill.identity == source.identity,
                       "test_not_used_for_selection": test_rejected}}
