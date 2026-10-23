"""ASTEROID Algorithm 1 on the paper's one-step three-door BAMDP.

This is a learned, causal history policy, not a hand-coded posterior sampler.
The three-door setting is an L1 mechanism diagnostic; it does not reproduce
the paper's gridworld, simulator, or physical-robot capability experiments.
Implementation is independent from the author's source (no license found).
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


@dataclass(frozen=True)
class PublicEpisode:
    """The entire public trajectory of a one-step episode; no latent goal."""

    action: int
    reward: int
    observation: int = 0
    terminal: bool = True

    def __post_init__(self) -> None:
        if self.action not in (0, 1, 2) or self.reward not in (0, 1):
            raise ValueError("three-door action/reward outside its public space")
        if self.observation != 0 or self.terminal is not True:
            raise ValueError("this bounded BAMDP has constant observation and one-step episodes")


@dataclass(frozen=True)
class ExpertExample:
    """Student context plus the complete successful one-step expert episode."""

    history: tuple[PublicEpisode, ...]
    expert_episode: PublicEpisode

    def __post_init__(self) -> None:
        if self.expert_episode.reward != 1:
            raise ValueError("ASTEROID retains successful expert trajectories only")


class ThreeDoorTask:
    """Latent is owned by the environment and exposed only to the teacher."""

    def __init__(self, goal: int) -> None:
        if goal not in (0, 1, 2):
            raise ValueError("goal must be one of the three doors")
        self.__goal = goal

    @property
    def observation(self) -> int:
        return 0

    def episode(self, action: int) -> PublicEpisode:
        return PublicEpisode(action=action, reward=int(action == self.__goal))

    def expert_episode(self) -> PublicEpisode:
        # Privileged state is used for this target, never for student inputs.
        return self.episode(self.__goal)


def public_tokens(
    histories: list[tuple[PublicEpisode, ...]], max_context: int, device: torch.device
) -> tuple[Tensor, Tensor, Tensor, Tensor]:
    """Encode only public history and the constant expert query observation.

    Every context episode contributes its action/reward/terminal tuple. The
    last valid token is the query (observation=0, no query action or reward).
    Its teacher action exists only in the separate loss target.
    """
    if not histories or max_context < 0:
        raise ValueError("nonempty histories and nonnegative context bound required")
    length = max_context + 1
    actions = torch.full((len(histories), length), 4, dtype=torch.long, device=device)
    rewards = torch.full_like(actions, 2)
    padding = torch.ones_like(actions, dtype=torch.bool)
    queries = torch.empty(len(histories), dtype=torch.long, device=device)
    for row, history in enumerate(histories):
        if len(history) > max_context:
            raise ValueError("context exceeds the configured episode budget")
        for col, episode in enumerate(history):
            if not isinstance(episode, PublicEpisode):
                raise TypeError("student histories must contain only public episodes")
            actions[row, col] = episode.action
            rewards[row, col] = episode.reward
        query = len(history)
        actions[row, query] = 3
        padding[row, : query + 1] = False
        queries[row] = query
    return actions, rewards, padding, queries


class CausalHistoryStudent(nn.Module):
    """Small causal transformer with categorical action likelihood, no oracle."""

    def __init__(self, max_context: int = 2, width: int = 24) -> None:
        super().__init__()
        if max_context < 0 or width < 4 or width % 4:
            raise ValueError("context must be nonnegative and width divisible by four")
        self.max_context = max_context
        self.action_embedding = nn.Embedding(5, width)
        self.reward_embedding = nn.Embedding(3, width)
        self.position_embedding = nn.Embedding(max_context + 1, width)
        layer = nn.TransformerEncoderLayer(
            width, 4, dim_feedforward=width * 2, dropout=0.0, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(layer, 1, enable_nested_tensor=False)
        self.head = nn.Linear(width, 3)

    def token_logits(self, actions: Tensor, rewards: Tensor, padding: Tensor) -> Tensor:
        if actions.ndim != 2 or rewards.shape != actions.shape or padding.shape != actions.shape:
            raise ValueError("token tensors must have identical batch/sequence shapes")
        if actions.shape[1] > self.max_context + 1:
            raise ValueError("token sequence exceeds context budget")
        positions = torch.arange(actions.shape[1], device=actions.device)
        embeddings = (
            self.action_embedding(actions)
            + self.reward_embedding(rewards)
            + self.position_embedding(positions)[None]
        )
        causal = torch.ones(
            actions.shape[1], actions.shape[1], device=actions.device, dtype=torch.bool
        ).triu(1)
        hidden = self.transformer(embeddings, mask=causal, src_key_padding_mask=padding)
        return self.head(hidden)

    def forward(self, histories: list[tuple[PublicEpisode, ...]]) -> Tensor:
        tokens = public_tokens(histories, self.max_context, self.head.weight.device)
        logits = self.token_logits(*tokens[:3])
        return logits[torch.arange(len(histories), device=logits.device), tokens[3]]


def imitation_loss(student: CausalHistoryStudent, examples: list[ExpertExample]) -> Tensor:
    """Equation 1: only expert query actions are supervised, not context actions."""
    if not examples:
        raise ValueError("expert examples required")
    histories = [example.history for example in examples]
    labels = torch.tensor(
        [example.expert_episode.action for example in examples],
        device=student.head.weight.device,
    )
    return F.cross_entropy(student(histories), labels)


@torch.no_grad()
def deploy(
    student: CausalHistoryStudent,
    task: ThreeDoorTask,
    episodes: int,
    generator: torch.Generator,
) -> tuple[PublicEpisode, ...]:
    """Alg2: start empty, sample actions from public online feedback only."""
    if episodes < 1:
        raise ValueError("positive deployment episode budget required")
    history: tuple[PublicEpisode, ...] = ()
    for _ in range(episodes):
        context = history[-student.max_context :] if student.max_context else ()
        probabilities = student([context]).softmax(-1)
        action = int(torch.multinomial(probabilities, 1, generator=generator).item())
        history += (task.episode(action),)
    return history


@torch.no_grad()
def collect_iteration(
    student: CausalHistoryStudent,
    goals: list[int],
    context_episodes: int,
    generator: torch.Generator,
) -> list[ExpertExample]:
    """Alg1: student k episodes then successful teacher episode at the SAME z.

    The discrete task's full episode has horizon one. The teacher never
    executes any of the student's context actions or determines their samples.
    All goals are training-task latents; there is no held-out gold input.
    """
    if not 0 <= context_episodes <= student.max_context or not goals:
        raise ValueError("invalid curriculum episode count or empty task list")
    tasks = [ThreeDoorTask(goal) for goal in goals]
    histories: list[tuple[PublicEpisode, ...]] = [() for _ in tasks]
    for _ in range(context_episodes):
        # Student sees histories only. Labels are queried AFTER all rollouts.
        probabilities = student(histories).softmax(-1)
        sampled = torch.multinomial(probabilities, 1, generator=generator).flatten().tolist()
        histories = [
            history + (task.episode(action),)
            for history, task, action in zip(histories, tasks, sampled, strict=True)
        ]
    return [
        ExpertExample(history, task.expert_episode())
        for history, task in zip(histories, tasks, strict=True)
    ]


def train_bounded(
    seed: int,
    device: str = "cpu",
    *,
    tasks_per_goal: int = 8,
    steps_per_round: int = 18,
) -> tuple[CausalHistoryStudent, list[ExpertExample], dict[str, float]]:
    """Two curriculum iterations, accumulated data, actual optimizer updates.

    This deliberately tiny budget is fixed a priori, never validation/test
    selected. Outputs are mechanism statistics, not benchmark capability.
    """
    if tasks_per_goal < 1 or steps_per_round < 1:
        raise ValueError("positive task and optimizer-step budgets required")
    target_device = torch.device(device)
    if target_device.type not in ("cpu", "cuda"):
        raise ValueError("only CPU and CUDA diagnostics are supported")
    cuda_devices = [target_device.index or 0] if target_device.type == "cuda" else []
    with torch.random.fork_rng(devices=cuda_devices):
        # Parameter initialization runs on CPU before transfer. Do not change
        # generators on unrelated CUDA devices when invoked as a CPU check.
        torch.random.default_generator.manual_seed(seed)
        student = CausalHistoryStudent().to(target_device)
        generator = torch.Generator(device=target_device).manual_seed(seed + 1009)
        optimizer = torch.optim.Adam(student.parameters(), lr=0.006)
        goals = [goal for goal in range(3) for _ in range(tasks_per_goal)]
        examples: list[ExpertExample] = []
        initial_parameters = torch.cat([p.detach().flatten() for p in student.parameters()])
        first_loss = 0.0
        last_loss = 0.0
        gradient_l2 = 0.0
        # k=0 is the context-free expert-trajectory initialization D0.
        for k in range(3):
            examples.extend(collect_iteration(student, goals, k, generator))
            for step in range(steps_per_round):
                optimizer.zero_grad(set_to_none=True)
                loss = imitation_loss(student, examples)
                if k == 0 and step == 0:
                    first_loss = float(loss.detach())
                loss.backward()
                gradient_l2 = float(
                    torch.stack([p.grad.detach().square().sum() for p in student.parameters()]).sum().sqrt()
                )
                optimizer.step()
                last_loss = float(loss.detach())
        with torch.no_grad():
            final_parameters = torch.cat([p.detach().flatten() for p in student.parameters()])
            parameter_delta = float((final_parameters - initial_parameters).norm())
            final_loss = float(imitation_loss(student, examples))
        return student, examples, {
            "initial_context_free_nll": first_loss,
            "last_training_nll": last_loss,
            "accumulated_expert_nll": final_loss,
            "parameter_update_l2": parameter_delta,
            "last_gradient_l2": gradient_l2,
            "optimizer_steps": float(3 * steps_per_round),
            "expert_query_count": float(len(examples)),
            "student_context_episodes": float(3 * len(goals)),
        }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Bounded L1 training/formula/isolation checks; no success-rate claim."""
    student, examples, metrics = train_bounded(seed, device)
    student.eval()
    with torch.no_grad():
        histories = [example.history for example in examples]
        logits = student(histories)
        labels = torch.tensor(
            [example.expert_episode.action for example in examples], device=logits.device
        )
        reference = -logits.log_softmax(-1)[torch.arange(len(labels), device=logits.device), labels].mean()
        nll = imitation_loss(student, examples)
        difference = float((nll - reference).abs())
        # Equal public histories must produce identical logits regardless of z.
        public_history = (PublicEpisode(0, 0),)
        alternate_labels = [
            ExpertExample(public_history, ThreeDoorTask(goal).expert_episode()) for goal in (1, 2)
        ]
        isolated_logits = student([example.history for example in alternate_labels])
        isolation_error = float((isolated_logits[0] - isolated_logits[1]).abs().max())
        altered = student([(PublicEpisode(0, 0),), (PublicEpisode(0, 1),)])
        history_effect = float((altered[0] - altered[1]).abs().max())
        tokens = public_tokens([()], student.max_context, logits.device)
        before = student.token_logits(*tokens[:3])[:, 0]
        changed_actions = tokens[0].clone()
        changed_rewards = tokens[1].clone()
        changed_actions[:, 1:] = 2
        changed_rewards[:, 1:] = 1
        after = student.token_logits(changed_actions, changed_rewards, tokens[2])[:, 0]
        future_error = float((before - after).abs().max())
    metrics.update({
        "nll_reference_abs_error": difference,
        "same_public_history_logit_abs_error": isolation_error,
        "history_reward_logit_effect": history_effect,
        "masked_future_logit_abs_error": future_error,
    })
    return {
        "seed": seed,
        "metrics": metrics,
        "checks": {
            "finite_metrics": all(math.isfinite(value) for value in metrics.values()),
            "real_parameter_update": metrics["parameter_update_l2"] > 0,
            "real_finite_gradient": math.isfinite(metrics["last_gradient_l2"]) and metrics["last_gradient_l2"] > 0,
            "expert_only_nll_matches_reference": difference < 1e-6,
            "student_never_receives_latent_or_label": isolation_error < 1e-6,
            "history_changes_learned_policy": history_effect > 1e-6,
            "causal_padding_isolation": future_error < 1e-6,
            "curriculum_zero_one_two_episodes": {len(x.history) for x in examples} == {0, 1, 2},
            "successful_teacher_episodes_only": all(x.expert_episode.reward == 1 for x in examples),
        },
    }
