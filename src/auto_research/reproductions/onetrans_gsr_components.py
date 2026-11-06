"""OneTrans-GSR CPU decoding/reward references; not the learned slate policy."""
from dataclasses import dataclass
import math
import random

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Candidate:
    key: str
    tags: frozenset[str]
    embedding: tuple[float,...] = ()


@dataclass(frozen=True)
class TagRule:
    tag: str
    window: int
    minimum: int
    maximum: int
    mandatory: bool = False
    penalty: float = .1

    def __post_init__(self):
        if (not self.tag or any(type(v) is not int for v in (self.window,self.minimum,self.maximum))
                or self.window < 1 or not 0 <= self.minimum <= self.maximum <= self.window
                or type(self.mandatory) is not bool or not math.isfinite(self.penalty) or self.penalty < 0):
            raise ValueError('valid tag/window/quota/penalty required')


def business_logits(candidates, base_logits, prefix, rules, remaining_tag_counts, *,
                    similarity_weight=0., advertising_boost=0.):
    """Eq. 9/10 local checks; no claim that interacting quotas stay feasible.

    remaining_tag_counts bounds tagged availability before appending a candidate;
    an independent check is not a global constraint solver. Deduplication is hard,
    quota controls are finite unless explicitly declared mandatory.
    """
    candidates, base_logits, prefix, rules = tuple(candidates), tuple(base_logits), tuple(prefix), tuple(rules)
    lookup = {c.key:c for c in candidates}
    if (len(lookup)!=len(candidates) or len(candidates)!=len(base_logits) or not candidates
            or len(set(prefix))!=len(prefix) or any(key not in lookup for key in prefix)
            or any(math.isnan(v) or v==math.inf for v in base_logits)
            or not math.isfinite(similarity_weight) or similarity_weight<0
            or not math.isfinite(advertising_boost)
            or any(type(v) is not int or v<0 for v in remaining_tag_counts.values())):
        raise ValueError('aligned unique candidates, valid prefix and finite adjustments required')
    result = []
    for candidate, base in zip(candidates,base_logits):
        score = float(base)
        if candidate.key in prefix:
            result.append(-math.inf)
            continue
        for rule in rules:
            previous = prefix[-(rule.window-1):] if rule.window>1 else ()
            count = sum(rule.tag in lookup[key].tags for key in previous)
            tagged = rule.tag in candidate.tags
            count += tagged
            slots = max(0,rule.window-len(previous)-1)
            future = min(slots,max(0,remaining_tag_counts.get(rule.tag,0)-int(tagged)))
            violation = (tagged and count>rule.maximum) or (not tagged and count+future<rule.minimum)
            if violation:
                score += -math.inf if rule.mandatory else -rule.penalty
        if similarity_weight and prefix:
            vectors = [candidate.embedding,*(lookup[key].embedding for key in prefix)]
            if (not vectors[0] or any(len(v)!=len(vectors[0]) or any(not math.isfinite(x) for x in v)
                                      or math.fsum(x*x for x in v)<=0 for v in vectors)):
                raise ValueError('aligned finite nonzero embeddings required for similarity')
            def cosine(a,b):
                return math.fsum(x*y for x,y in zip(a,b))/math.sqrt(math.fsum(x*x for x in a)*math.fsum(y*y for y in b))
            score -= similarity_weight*math.fsum(cosine(candidate.embedding,lookup[key].embedding) for key in prefix)/len(prefix)
        if 'ad' in candidate.tags:
            score += advertising_boost
        if math.isnan(score) or score == math.inf:
            raise ValueError('nonfinite logit arithmetic; do not mask numerical overflow')
        result.append(score)
    if not any(math.isfinite(score) for score in result):
        raise ValueError('at least one unmasked candidate required; do not silently relax rules')
    return tuple(result)


def geometric_reward(objective_scores, weights, *, epsilon=1e-8, floor=1e-4):
    """Eq. 13/14 float64 reference: per-request ranges, floor then geometric mean.

    Callers supply RM ensemble/LTV scores. This is not learned reward-model
    calibration, and geometric aggregation guarantees neither Pareto gains nor
    improvement in measured online business objectives.
    """
    rows, weights = tuple(map(tuple,objective_scores)), tuple(weights)
    if (not rows or not weights or any(len(row)!=len(weights) for row in rows)
            or any(not math.isfinite(v) for row in rows for v in row)
            or any(not math.isfinite(w) or w<=0 for w in weights)
            or not math.isclose(math.fsum(weights),1.,rel_tol=0,abs_tol=1e-12)
            or not math.isfinite(epsilon) or epsilon<=0 or not math.isfinite(floor) or not 0<floor<=1):
        raise ValueError('finite aligned scores, positive unit-sum weights and numerical guards required')
    minimum = [min(row[j] for row in rows) for j in range(len(weights))]
    maximum = [max(row[j] for row in rows) for j in range(len(weights))]
    if any(not math.isfinite(hi-lo+epsilon) for lo,hi in zip(minimum,maximum)):
        raise ValueError('objective range overflows finite arithmetic')
    return tuple(math.exp(math.fsum(w*math.log(max(floor,(row[j]-minimum[j])/(maximum[j]-minimum[j]+epsilon)))
                                    for j,w in enumerate(weights))) for row in rows)


def separate_advantages(model_reward, rule_reward, *, rule_weight=.1, epsilon=1e-8):
    model_reward, rule_reward = tuple(model_reward), tuple(rule_reward)
    if (not model_reward or len(model_reward)!=len(rule_reward)
            or any(not math.isfinite(x) for x in (*model_reward,*rule_reward))
            or not math.isfinite(rule_weight) or rule_weight<0 or not math.isfinite(epsilon) or epsilon<=0):
        raise ValueError('finite aligned per-request rewards required')
    def normalize(values):
        mean = math.fsum(values)/len(values)
        scale = math.sqrt(math.fsum((v-mean)**2 for v in values)/len(values)+epsilon)
        return tuple((v-mean)/scale for v in values)
    return tuple(a+rule_weight*b for a,b in zip(normalize(model_reward),normalize(rule_reward)))


def diagnostic(seed=42, device='cpu'):
    if device != 'cpu':
        raise ValueError('CPU arithmetic/decoding contracts only')
    rng = random.Random(seed)
    candidates = [Candidate('ad',frozenset({'ad'})),Candidate('organic',frozenset()),Candidate('other',frozenset())]
    logits = business_logits(candidates,[0.,0.,0.],['organic'],[TagRule('ad',2,1,1)],{'ad':1})
    rewards = geometric_reward([[1.,3.],[2.,3.],[3.,3.]],[.5,.5])
    advantages = separate_advantages([rng.random() for _ in range(3)],[0.,1.,2.])
    return {'seed':seed,'diagnostic_only':True,'evaluation_tier':'l1_mechanism',
            'metrics':{'finite_quota_penalty':logits[2],'constant_objective_floor_reward':rewards[0],
                       'advantage_mean':math.fsum(advantages)/3},
            'checks':{'dedup_hard_mask':logits[1]==-math.inf,'quota_not_hard_by_default':math.isfinite(logits[2]),
                      'constant_objective_keeps_positive_floor':math.isclose(rewards[0],1e-4,abs_tol=1e-15),
                      'separate_group_centering':abs(math.fsum(advantages))<1e-12}}
