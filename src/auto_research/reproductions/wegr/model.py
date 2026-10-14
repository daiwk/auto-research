"""WeGR equations 1--14, with small trainable networks instead of fixtures."""
from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


def horizon(step: int, stage_steps: int, levels: int) -> int:
    if step < 0 or stage_steps < 1 or levels < 1:
        raise ValueError("positive stage budget/levels and nonnegative step required")
    return min(1 + step // stage_steps, levels)


def prefix_rewards(samples, positives, values, *, horizon_length):
    """Maximum logged reward among matching positive prefixes (Eq. 10)."""
    if not 1 <= horizon_length <= samples.shape[-1]:
        raise ValueError("invalid reward horizon")
    matches = (samples[:, :, None, :horizon_length]
               == positives[:, None, :, :horizon_length]).all(-1)
    return (matches * values[:, None, :]).amax(-1)


def dhpo_loss(logp, old_logp, rewards, *, horizon_length, clip=0.2):
    if logp.shape != old_logp.shape or logp.shape[:2] != rewards.shape:
        raise ValueError("rollout log probabilities/rewards must align")
    if not 1 <= horizon_length <= logp.shape[-1] or not 0 < clip < 1:
        raise ValueError("invalid optimizer horizon or clip")
    advantage = (rewards - rewards.mean(-1, keepdim=True)) / (
        rewards.std(-1, keepdim=True, unbiased=False) + 1e-6)
    ratio = (logp[..., :horizon_length] - old_logp[..., :horizon_length].detach()).exp()
    advantage = advantage.detach()[..., None]
    return -torch.minimum(ratio * advantage,
                          ratio.clamp(1 - clip, 1 + clip) * advantage).mean()


def multi_positive_loss(logp, valid):
    """Each session contributes its mean positive-SID NLL (Eq. 13)."""
    if logp.ndim != 3 or valid.shape != logp.shape[:2] or not valid.any(-1).all():
        raise ValueError("every session must contain an observed positive")
    return (-(logp.mean(-1) * valid).sum(-1) / valid.sum(-1)).mean()


class CoCoVAE(nn.Module):
    def __init__(self, features: int, dimension=24, codebook_sizes=(8, 8, 8)):
        super().__init__()
        if min(features, dimension, *codebook_sizes) < 2:
            raise ValueError("invalid tokenizer dimensions")
        self.encoder = nn.Sequential(nn.Linear(features, dimension), nn.Tanh(),
                                     nn.Linear(dimension, dimension))
        self.decoder = nn.Linear(dimension, features)
        self.books = nn.ParameterList([nn.Parameter(torch.randn(k, dimension) * .1)
                                       for k in codebook_sizes])
        self.projection = nn.Linear(dimension, dimension, bias=False)
        self.register_buffer("usage", torch.zeros(codebook_sizes[0]))

    def forward(self, x, *, far=True):
        z = self.encoder(x)
        residual, quantized, codes, fidelities, collisions = z, torch.zeros_like(z), [], [], []
        for book in self.books:
            distance = torch.cdist(residual, book).square()
            index = distance.argmin(-1)
            selected = book[index]
            codes.append(index)
            similarity = F.normalize(residual, dim=-1) @ F.normalize(book, dim=-1).T
            top_values, top_indices = similarity.topk(min(3, len(book)), dim=-1)
            soft = (book[top_indices] * top_values.softmax(-1)[..., None]).sum(1)
            fidelities.append((1 - F.cosine_similarity(residual, soft)).mean())
            probability = (similarity / .1).softmax(-1)
            overlap = probability @ probability.T
            n = len(x)
            collisions.append((overlap.sum() - overlap.diagonal().sum()) / (n * (n - 1))
                              if n > 1 else overlap.sum() * 0)
            quantized = quantized + selected
            residual = residual - selected
        straight = z + (quantized - z).detach()
        reconstruction = F.mse_loss(self.decoder(straight), x)
        commitment = F.mse_loss(z, quantized.detach()) + F.mse_loss(z.detach(), quantized)
        fidelity, collision = torch.stack(fidelities).mean(), torch.stack(collisions).mean()
        # A detached projection head lets collaboration gradients reach the
        # continuous encoder, never through discrete code assignment.
        loss = reconstruction + .25 * commitment
        if far:
            loss = loss + .4 * (.9 * fidelity + collision)
        return z, torch.stack(codes, -1), loss, {
            "reconstruction": reconstruction, "fidelity": fidelity, "collision": collision}

    def collaborative_loss(self, query_features, item_features, neighbor_features):
        def project(features):
            return F.normalize(F.linear(self.encoder(features), self.projection.weight.detach()), dim=-1)
        q, item, neighbor = map(project, (query_features, item_features, neighbor_features))
        labels = torch.arange(len(item), device=item.device)
        q2i = F.cross_entropy(q @ item.T / .1, labels)
        i2i = F.cross_entropy(neighbor @ item.T / .1, labels)
        return .2 * q2i + .05 * i2i

    @torch.no_grad()
    def refresh(self, codes, *, decay=.9, threshold=.1):
        self.usage.mul_(decay).add_(torch.bincount(codes[:, 0], minlength=len(self.usage)),
                                  alpha=1 - decay)
        active = (self.usage >= threshold).nonzero().flatten()
        dead = (self.usage < threshold).nonzero().flatten()
        if not len(active) or not len(dead):
            return 0
        parents = active[torch.randint(len(active), (len(dead),), device=active.device)]
        self.books[0][dead] = self.books[0][parents] + .01 * torch.randn_like(self.books[0][dead])
        return len(dead)


class SIDPolicy(nn.Module):
    def __init__(self, context_dimension, *, dimension=24, levels=3, vocabulary=8):
        super().__init__()
        self.levels, self.vocabulary = levels, vocabulary
        self.context = nn.Linear(context_dimension, dimension)
        self.tokens = nn.Embedding(vocabulary + 1, dimension)
        self.position = nn.Embedding(levels + 2, dimension)
        layer = nn.TransformerEncoderLayer(dimension, 2, dimension * 2,
                                           dropout=0., batch_first=True, norm_first=True)
        self.network = nn.TransformerEncoder(layer, 2, enable_nested_tensor=False)
        self.head = nn.Linear(dimension, vocabulary)

    def logits(self, context, prefix):
        bos = torch.full((len(prefix), 1), self.vocabulary, dtype=torch.long, device=prefix.device)
        sequence = torch.cat((bos, prefix), -1)
        x = torch.cat((self.context(context)[:, None, :], self.tokens(sequence)), 1)
        x = x + self.position(torch.arange(x.shape[1], device=x.device))[None]
        mask = torch.ones(x.shape[1], x.shape[1], dtype=torch.bool, device=x.device).triu(1)
        return self.head(self.network(x, mask=mask)[:, 1:])

    def log_prob(self, context, sid):
        return self.logits(context, sid[:, :-1]).log_softmax(-1).gather(-1, sid[..., None])[..., 0]

    @torch.no_grad()
    def sample(self, context, group):
        expanded = context.repeat_interleave(group, 0)
        prefix = torch.empty((len(expanded), 0), dtype=torch.long, device=context.device)
        for _ in range(self.levels):
            probabilities = self.logits(expanded, prefix)[:, -1].softmax(-1)
            token = torch.multinomial(probabilities, 1)
            prefix = torch.cat((prefix, token), -1)
        logp = self.log_prob(expanded, prefix)
        return prefix.reshape(len(context), group, self.levels), logp.reshape(len(context), group, self.levels)
