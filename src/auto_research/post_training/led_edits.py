"""LED v1 fixed-block LCS supervision and simultaneous edit application.

No diffusion checkpoint, multi-stage trainer or capability benchmark is implied.
"""

import math

MASK, INSERT, DELETE = "[Mask]", "[Ins]", "[Del]"
REQUIRES_GPU_VALIDATION = False


def _tokens(values, *, clean=False):
    if (not isinstance(values, (list, tuple)) or not 1 <= len(values) <= 4096
            or any(not isinstance(x, str) or not x for x in values)
            or any(x in {INSERT, DELETE} for x in values)
            or (clean and MASK in values)):
        raise ValueError("nonempty bounded token sequence; output actions are not input tokens")
    return list(values)


def edit_targets(source, target):
    s, y = _tokens(source), _tokens(target, clean=True)
    if len(s) != len(y):
        raise ValueError("source and target must share fixed block length")
    b = len(s)
    dp = [[0]*(b+1) for _ in range(b+1)]
    for i in range(b-1, -1, -1):
        for j in range(b-1, -1, -1):
            dp[i][j] = 1+dp[i+1][j+1] if s[i] == y[j] else max(dp[i+1][j], dp[i][j+1])
    anchors, i, j = [], 0, 0
    while i < b and j < b:
        if s[i] == y[j]:
            anchors.append((i, j))
            i, j = i+1, j+1
        elif dp[i+1][j] > dp[i][j+1]:
            i += 1
        else:
            j += 1
    labels = [None]*b
    for i, j in anchors:
        labels[i] = y[j]
    bounds = [(-1, -1), *anchors, (b, b)]
    for left, right in zip(bounds[:-1], bounds[1:], strict=True):
        src = list(range(left[0]+1, right[0]))
        dst = list(range(left[1]+1, right[1]))
        length = min(len(src), len(dst))
        for pos, idx in zip(src[:length], dst[:length], strict=True):
            labels[pos] = y[idx]
        for pos in src[length:]:
            labels[pos] = DELETE
        if len(dst) > length and right[0] < b:
            labels[right[0]] = INSERT
    return labels, tuple(anchors)


def selected_positions(source, predictions, confidence, *, mask_threshold=0.5, edit_threshold=0.):
    s = _tokens(source)
    if (not isinstance(predictions, (list, tuple)) or len(predictions) != len(s)
            or any(not isinstance(x, str) or not x or x == MASK for x in predictions)
            or len(confidence) != len(s)):
        raise ValueError("one valid output and confidence per block position required")
    if any(type(x) not in {float, int} or not math.isfinite(x) or not 0 <= x <= 1
           for x in [*confidence, mask_threshold, edit_threshold]):
        raise ValueError("finite thresholds and confidence in [0,1] required")
    masked = [i for i, t in enumerate(s) if t == MASK]
    chosen = [i for i in masked if confidence[i] >= mask_threshold]
    if masked and not chosen:
        chosen = [max(masked, key=lambda i: confidence[i])]
    chosen += [i for i, t in enumerate(s) if t != MASK and predictions[i] != t
               and confidence[i] >= edit_threshold]
    return tuple(sorted(chosen))


def apply_edits(source, predictions, selected):
    s = _tokens(source)
    if (not isinstance(predictions, (list, tuple)) or len(predictions) != len(s)
            or any(not isinstance(x, str) or not x or x == MASK for x in predictions)
            or not isinstance(selected, (list, tuple))
            or len(set(selected)) != len(selected)
            or any(type(i) is not int or not 0 <= i < len(s) for i in selected)):
        raise ValueError("valid position-aligned outputs and distinct selected indices required")
    chosen, out = set(selected), []
    for i, token in enumerate(s):
        prediction = predictions[i] if i in chosen else token
        if prediction == INSERT:
            out.extend([MASK, token])
        elif prediction != DELETE:
            out.append(prediction)
    return (out+[MASK]*len(s))[:len(s)]


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required for fixed-block edit bookkeeping")
    s, y = ["a", "c", "d", "extra"], ["a", "b", "c", "d"]
    labels, anchors = edit_targets(s, y)
    first = apply_edits(s, labels, list(range(4)))
    second_labels, _ = edit_targets(first, y)
    second = apply_edits(first, second_labels, list(range(4)))
    fallback = selected_positions([MASK, "a"], ["b", "a"], [0.1, 0.9])
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {
                "lcs_retains_shifted_anchors": anchors == ((0, 0), (1, 2), (2, 3)),
                "insert_targets_right_anchor_and_delete_surplus": labels == ["a", INSERT, "d", DELETE],
                "insert_preserves_anchor_and_makes_mask": first == ["a", MASK, "c", "d"],
                "second_round_recovers_target": second == y,
                "masked_fallback_makes_progress": fallback == (0,),
                "trailing_target_gap_has_no_fictitious_anchor": edit_targets(["a", "x"], ["a", "b"])[0] == ["a", "b"],
            }, "metrics": {"block_length": 4, "lcs_anchors": len(anchors),
                           "insert_targets": labels.count(INSERT), "delete_targets": labels.count(DELETE)}}
