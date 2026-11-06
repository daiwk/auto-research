"""SPADE OA-BPE and SDBS CPU operators, not STAR/MARS-DPO or a query model."""
from collections import defaultdict
from dataclasses import dataclass
import math
import random

REQUIRES_GPU_VALIDATION = False


def oa_pair_scores(corpus, weights):
    corpus, weights = tuple(map(tuple, corpus)), tuple(weights)
    if len(corpus) != len(weights) or not corpus:
        raise ValueError('one weight per nonempty corpus required')
    if any(not math.isfinite(w) or w < 0 for w in weights):
        raise ValueError('finite nonnegative business weights required')
    scores = defaultdict(list)
    for tokens, weight in zip(corpus, weights):
        if any(not isinstance(t, str) or not t for t in tokens):
            raise ValueError('tokens must be nonempty strings')
        for pair in zip(tokens, tokens[1:]):
            scores[pair].append(weight)
    return {pair: math.fsum(values) for pair, values in sorted(scores.items())}


def merge_pair(tokens, pair):
    if len(pair) != 2 or any(not isinstance(t, str) or not t for t in pair):
        raise ValueError('two nonempty token strings required')
    tokens, result, index = tuple(tokens), [], 0
    while index < len(tokens):
        if tokens[index:index+2] == tuple(pair):
            result.append(''.join(pair))
            index += 2
        else:
            result.append(tokens[index])
            index += 1
    return tuple(result)


def sigmoid_bonus(rank, *, alpha=1., beta=.4, gamma=1.):
    if (type(rank) is not int or rank < 0 or not all(math.isfinite(v) for v in (alpha,beta,gamma))
            or alpha <= 0 or beta < 0 or not 0 < gamma <= 1):
        raise ValueError('rank>=0, alpha>0, beta>=0, 0<gamma<=1 required')
    return beta*(1/(1+gamma*math.exp(-alpha*rank))-1/(1+gamma))


@dataclass(frozen=True)
class Beam:
    tokens: tuple[str, ...]
    score: float


def sdbs_step(beams, next_tokens, *, beam_size, alpha=1., beta=.4, gamma=1.):
    """Algorithm 1's single expansion/prune step on external model logp.

    Parent rank (not token rank or pairwise overlap) determines the bonus.
    Scores include all earlier bonuses. Zero top-parent bonus does not guarantee
    that its continuation remains top after rivals receive their bonuses.
    """
    beams, next_tokens = tuple(beams), tuple(next_tokens)
    if type(beam_size) is not int or beam_size < 1 or len(beams) != len(next_tokens) or not beams:
        raise ValueError('positive beam size and aligned external readouts required')
    if any(not math.isfinite(b.score) for b in beams) or any(a.score < b.score for a,b in zip(beams,beams[1:])):
        raise ValueError('parents must be sorted by finite accumulated score')
    expanded = []
    for rank,(beam,readout) in enumerate(zip(beams,next_tokens)):
        choices = tuple(readout)
        if len({token for token,_ in choices}) != len(choices):
            raise ValueError('next-token identities must be unique per parent')
        if any(not isinstance(token,str) or not token or not math.isfinite(logp) or logp > 0 for token,logp in choices):
            raise ValueError('finite nonpositive log probabilities required')
        for token,logp in sorted(choices,key=lambda row:(-row[1],row[0]))[:2*beam_size]:
            expanded.append(Beam(beam.tokens+(token,),beam.score+logp+sigmoid_bonus(rank,alpha=alpha,beta=beta,gamma=gamma)))
    return sorted(expanded,key=lambda beam:(-beam.score,beam.tokens))[:beam_size]


def diagnostic(seed=42, device='cpu'):
    if device != 'cpu':
        raise ValueError('CPU tokenizer/decoding operators only')
    rng = random.Random(seed)
    weight = rng.uniform(2.5,4.)
    scores = oa_pair_scores([('a','a','a'),('b','c')],[1.,weight])
    beams = [Beam(('A',),0.),Beam(('B',),-.01)]
    choices = [[('x',-.1),('y',-.2)]]*2
    result = sdbs_step(beams,choices,beam_size=2)
    bonus = [sigmoid_bonus(i) for i in range(5)]
    return {'seed':seed,'diagnostic_only':True,'evaluation_tier':'l1_mechanism',
            'metrics':{'rare_pair_weighted_count':scores[('b','c')],
                       'rank_one_bonus':bonus[1],'accumulated_best_score':result[0].score},
            'checks':{'weighted_count_changes_merge_order':scores[('b','c')]>scores[('a','a')],
                      'top_parent_unperturbed':bonus[0]==0.,
                      'rank_not_semantic_distance':result[0].tokens==('B','x'),
                      'ordinary_beam_limit':sdbs_step(beams,choices,beam_size=2,beta=0)[0].tokens==('A','x'),
                      'nonoverlap_merge':merge_pair(('a','a','a'),('a','a'))==('aa','a')}}
