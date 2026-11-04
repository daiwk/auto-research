"""ReuseGR Eq. 5/6/10 CPU reference contracts; no planner or learned BudgetCut."""
from dataclasses import dataclass
from collections import Counter
import math
import random

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class ClickRow:
    row_id: str
    sid: tuple[int, ...]
    clicks: int


@dataclass(frozen=True)
class DepthLabel:
    depth: int
    known: bool
    coverages: tuple[float, ...]
    lower_bounds: tuple[float, ...]


def wilson_lower(successes: int, total: int, z: float = 1.96) -> float:
    if (type(successes) is not int or type(total) is not int
            or total < 1 or not 0 <= successes <= total or not math.isfinite(z) or z <= 0):
        raise ValueError('finite Wilson parameters and valid integer counts required')
    if successes == 0:
        return 0.
    p = successes / total
    z2 = z*z
    return (p + z2/(2*total) - z*math.sqrt(p*(1-p)/total + z2/(4*total*total))) / (1+z2/total)


def label_reuse_depth(rows, *, max_depth=3, top_n=32, threshold=.4, min_rows=5):
    """Fit-only whole-row LOO targets; row-macro coverage, click-mass ranking.

    This does not fit the query-text classifier or measure model-frontier reachability.
    The Wilson endpoint is the paper's finite-support criterion, not an IID guarantee
    for dependent leave-one-out estimates.
    """
    rows = tuple(rows)
    if (any(type(v) is not int or v < 1 for v in (max_depth, top_n, min_rows))
            or not math.isfinite(threshold) or not 0 <= threshold <= 1):
        raise ValueError('invalid label configuration')
    if len({row.row_id for row in rows}) != len(rows):
        raise ValueError('aggregated row identities must be unique')
    if any(not row.row_id or len(row.sid) <= max_depth
           or type(row.clicks) is not int or row.clicks <= 0 for row in rows):
        raise ValueError('nonempty complete SIDs and positive aggregated clicks required')
    if len(rows) < min_rows:
        return DepthLabel(0, False, (), ())
    coverages, bounds = [], []
    for depth in range(1, max_depth+1):
        mass = Counter()
        for row in rows:
            mass[row.sid[:depth]] += row.clicks
        hits = 0
        for row in rows:
            held_out = mass.copy()
            held_out[row.sid[:depth]] -= row.clicks
            frontier = sorted((p for p in held_out if held_out[p] > 0),
                              key=lambda p: (-held_out[p], p))[:top_n]
            hits += row.sid[:depth] in frontier
        coverages.append(hits/len(rows))
        bounds.append(wilson_lower(hits, len(rows)))
    depth = 0
    for level, lower in enumerate(bounds, 1):
        if lower < threshold:
            break
        depth = level
    return DepthLabel(depth, True, tuple(coverages), tuple(bounds))


def cache_route(prepared: bool, depth: int) -> str:
    if type(prepared) is not bool or type(depth) is not int or not 0 <= depth <= 3:
        raise ValueError('explicit cache availability and depth 0..3 required')
    return 'cold_e2e' if not prepared else ('prepared_root' if depth == 0 else 'prepared_prefix')


def composite_score(prefix_log_score, suffix_log_scores, *, beta=1.):
    suffix_log_scores = tuple(suffix_log_scores)
    if (not math.isfinite(beta) or beta < 0
            or any(not math.isfinite(v) or v > 0 for v in (prefix_log_score, *suffix_log_scores))):
        raise ValueError('finite nonpositive model log probabilities and nonnegative beta required')
    return beta*prefix_log_score + math.fsum(suffix_log_scores)


def diagnostic(seed=42, device='cpu'):
    if device != 'cpu':
        raise ValueError('CPU protocol component only')
    rng = random.Random(seed)
    rows = [ClickRow(str(i), (1, 1, i, rng.randrange(32)), rng.randrange(1, 5)) for i in range(8)]
    label = label_reuse_depth(rows, top_n=2)
    heldout = label_reuse_depth([ClickRow('a',(1,1,1,1),100), ClickRow('b',(2,2,2,2),1)],
                               top_n=1, min_rows=2)
    return {'seed':seed,'diagnostic_only':True,'evaluation_tier':'l1_mechanism',
            'metrics':{'selected_depth':label.depth,'first_depth_coverage':label.coverages[0],
                       'first_depth_wilson_lower':label.lower_bounds[0]},
            'checks':{'whole_row_not_single_click':heldout.coverages==(0.,0.,0.),
                      'ancestors_required':label.depth==2,
                      'depth_zero_not_miss':cache_route(True,0)!=cache_route(False,0),
                      'suffix_score_exact':composite_score(-2.,[-.5,-.25])==-2.75}}
