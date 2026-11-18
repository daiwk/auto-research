"""Check the bounded CPU reference, not ANNS throughput or recall."""

from dataclasses import replace
import math

import pytest

from auto_research.foundation_models import ginger


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_positive_conditional_centroids_and_distortion(bits):
    book = ginger.build_codebook(bits)
    cuts = (0.0, *book.coarse_thresholds, math.inf)
    for u, row in enumerate(book.fine):
        assert len(row) == 2**bits
        assert cuts[u] < row[0] < row[-1] < cuts[u + 1]
        assert all(a < b for a, b in zip(row, row[1:]))
        # Independent normal-CDF moments for each midpoint-delimited cell.
        edges = (cuts[u], *[(a + b) / 2 for a, b in zip(row, row[1:])], cuts[u + 1])
        for c, a, b in zip(row, edges[:-1], edges[1:], strict=True):
            mass = (math.erf(b / math.sqrt(2)) - math.erf(a / math.sqrt(2))) / 2
            first = (math.exp(-a * a / 2) - math.exp(-b * b / 2)) / math.sqrt(2 * math.pi)
            assert c == pytest.approx(first / mass, abs=3e-10)
    assert book.coarse_distortion == pytest.approx(0.009501008, rel=1e-7)
    assert 0 < book.fine_distortion < book.coarse_distortion


def test_nearest_centroids_manual_decoding_and_signed_query():
    book = ginger.build_codebook()
    x = (1.5, 0.0, -0.125, -3.5, 10.0, -9.0, 8.0)
    norm = math.sqrt(sum(value * value for value in x))
    coarse_centers, fine_centers = [], []
    for value in x:
        y = abs(value) * math.sqrt(len(x)) / norm
        u = min(range(8), key=lambda i: abs(y - book.coarse[i]))
        nearest_fine = min(book.fine[u], key=lambda c: abs(y - c))
        sign = -1 if value < 0 else 1
        coarse_centers.append(sign * book.coarse[u])
        fine_centers.append(sign * nearest_fine)
    code = ginger.encode(x, book)
    for centers, distortion, decoded in (
        (coarse_centers, book.coarse_distortion, ginger.decode_navigation(code.navigation, book)),
        (fine_centers, book.fine_distortion, ginger.decode_refined(code, book)),
    ):
        factor = norm / math.sqrt((1 - distortion) * sum(c**2 for c in centers))
        assert decoded == pytest.approx([c * factor for c in centers])
        query = (0.5, 1, 2, 0, -1, -2, 3)
        assert ginger.inner_product(query, decoded) == pytest.approx(
            factor * sum(q * c for q, c in zip(query, centers, strict=True))
        )
    # The navigation bytes, metadata, and decoder do not need a fine stream.
    other = ginger.build_codebook(3)
    assert ginger.encode(x, other).navigation == code.navigation
    assert ginger.decode_navigation(code.navigation, other) == ginger.decode_navigation(
        code.navigation, book,
    )


def test_refinement_bits_span_bytes_and_padding_is_canonical():
    book = ginger.build_codebook(3)
    vector = (1.0, -3.0, 2.0, 9.0, -4.0)
    code = ginger.encode(vector, book)
    assert len(code.navigation.packed) == 3
    assert len(code.refinement) == 2
    assert code.navigation.packed[-1] < 16
    assert code.refinement[-1] < 128
    with pytest.raises(ValueError, match="padding"):
        ginger.decode_refined(replace(code, refinement=code.refinement[:-1] + b"\xff"), book)
    with pytest.raises(ValueError, match="stream length"):
        ginger.decode_refined(replace(code, refinement=b""), book)
    with pytest.raises(ValueError, match="bit width"):
        ginger.decode_refined(code, ginger.build_codebook(2))


@pytest.mark.parametrize("vector", [(), (0.0, 0.0), (math.nan,), (math.inf,)])
def test_reject_unrepresentable_input(vector):
    with pytest.raises(ValueError, match="nonzero norm"):
        ginger.encode(vector, ginger.build_codebook())


def test_cuda_is_not_silently_relabelled_cpu():
    with pytest.raises(ValueError, match="CPU-only"):
        ginger.diagnostic(42, device="cuda")
    with pytest.raises(ValueError, match="dimension"):
        ginger.inner_product((1.0,), (2.0, 3.0))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_l1_mechanism_receipt(seed):
    row = ginger.diagnostic(seed)
    assert row["seed"] == seed
    assert row["diagnostic_only"]
    assert row["evaluation_tier"] == "l1_mechanism"
    assert row["checks"] and all(value is True for value in row["checks"].values())
