import pytest

torch = pytest.importorskip("torch")

from auto_research.multimodal import rs_jepa  # noqa: E402


def test_scan_paths_are_papers_mirrors_not_reverse_or_snake():
    assert rs_jepa.scan_path(2, 3, "row") == (0, 1, 2, 3, 4, 5)
    assert rs_jepa.scan_path(2, 3, "column") == (0, 3, 1, 4, 2, 5)
    assert rs_jepa.scan_path(2, 3, "row_mirror") == (2, 1, 0, 5, 4, 3)
    assert rs_jepa.scan_path(2, 3, "column_mirror") == (3, 0, 4, 1, 5, 2)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_rs_jepa_cpu_tensor_reference_controls(seed):
    result = rs_jepa.diagnostic(seed, "cpu")
    assert result["device"] == "cpu"
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(result["checks"].values())
    assert result["metrics"]["relational_loss"] > 0
    assert rs_jepa.REQUIRES_GPU_VALIDATION is True


def test_partition_is_disjoint_identity_and_reverses_gradient_exactly():
    z = torch.tensor([[[1., 0.], [2., 1.], [-1., 3.], [0., -2.]]], requires_grad=True)
    w = torch.tensor([.2, .3], requires_grad=True)
    a, b, ia, ib = rs_jepa.adversarial_partition(z, w)
    assert ia.shape == ib.shape == (1, 2)
    assert torch.equal(a, z.gather(1, ia[..., None].expand(-1, -1, 2)))
    assert torch.equal(b, z.gather(1, ib[..., None].expand(-1, -1, 2)))
    normal = torch.tensor([1., -2.], requires_grad=True)
    (rs_jepa.reverse_gradient(normal).square().sum()).backward()
    assert torch.equal(normal.grad, -2 * normal.detach())


def _reference_kl(embeddings, temperature):
    normalized = [torch.nn.functional.normalize(row, dim=-1) for row in embeddings]
    count = len(normalized[0])
    distributions = []
    for query, gallery in ((0, 0), (1, 1), (2, 3), (3, 2)):
        rows = []
        for i in range(count):
            logits = torch.stack([(normalized[query][i] * normalized[gallery][j]).sum() / temperature
                                  for j in range(count) if i != j])
            rows.append(torch.softmax(logits, 0))
        distributions.append(torch.stack(rows))
    target = ((distributions[0] + distributions[1]) / 2).detach()
    return sum((target * (target.log() - row.log())).sum() for row in distributions) / (4 * count)


def test_consensus_matches_independent_loop_value_and_detached_target_gradient():
    generator = torch.Generator().manual_seed(6)
    values = [torch.randn(4, 3, generator=generator, dtype=torch.float64, requires_grad=True) for _ in range(4)]
    copied = [row.detach().clone().requires_grad_() for row in values]
    actual = rs_jepa.neighbourhood_consensus(*values, temperature=.7)
    expected = _reference_kl(copied, .7)
    assert torch.allclose(actual, expected, atol=1e-12)
    actual.backward(); expected.backward()
    assert all(torch.allclose(a.grad, b.grad, atol=1e-12) for a, b in zip(values, copied, strict=True))


def test_twin_exclusion_two_samples_has_one_neighbor_and_zero_kl():
    matrices = [torch.randn(2, 3) for _ in range(4)]
    assert rs_jepa.neighbourhood_consensus(*matrices).item() == 0.
    with pytest.raises(ValueError):
        rs_jepa.neighbourhood_consensus(*(row[:1] for row in matrices))
    with pytest.raises(ValueError):
        rs_jepa.adversarial_partition(torch.randn(1, 3, 2), torch.randn(2))


@pytest.mark.skipif(not torch.cuda.is_available(), reason="real CUDA validation is run separately on A100/A30")
def test_explicit_cuda_diagnostic_executes_on_cuda():
    result = rs_jepa.diagnostic(42, "cuda")
    assert result["device"].startswith("cuda:")
    assert all(result["checks"].values())
