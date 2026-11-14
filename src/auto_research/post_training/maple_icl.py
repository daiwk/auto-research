"""MAPLE donated-example initialization selection, not AIM/PE or a DP release."""
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


def _scalar(value):
    return isinstance(value, (str, int, float)) and not isinstance(value, bool) and (
        not isinstance(value, float) or math.isfinite(value))


def _row(schema, values):
    if not isinstance(values, Mapping) or set(values) != set(schema):
        raise ValueError("metadata must contain exactly the public schema fields")
    if any(not _scalar(v) or v not in schema[k] for k, v in values.items()):
        raise ValueError("metadata value outside its categorical domain")
    return tuple(values[k] for k in schema)


@dataclass(frozen=True)
class Donation:
    identity: str
    metadata: Mapping
    text: str
    consent_ref: str

    def __post_init__(self):
        if any(not isinstance(x, str) or not x.strip() for x in (self.identity, self.text, self.consent_ref)):
            raise ValueError("donation identity, text and external consent provenance required")
        if not isinstance(self.metadata, Mapping):
            raise ValueError("categorical metadata mapping required")


def select_examples(synthetic_metadata, donations: Sequence[Donation], schema: Mapping, *, k=10):
    """Select lowest unweighted categorical Hamming counts, stable input ties.

    The caller must supply genuinely DP-generated synthetic metadata and genuinely
    donated/public examples. This function cannot establish either claim. Raw
    private corpus, AIM training and generation are deliberately not inputs.
    Dividing counts by the common field count does not change the ranking.
    """
    if not isinstance(schema, Mapping) or not schema or any(
        not isinstance(key, str) or not key or isinstance(domain, (str, bytes))
        or not isinstance(domain, Sequence) or not domain or not all(_scalar(x) for x in domain)
        or len(set(domain)) != len(domain) for key, domain in schema.items()
    ):
        raise ValueError("public nonempty categorical schema required")
    if type(k) is not int or k < 1:
        raise ValueError("positive integer example count required")
    if isinstance(donations, (str, bytes)) or not isinstance(donations, Sequence) or not donations:
        raise ValueError("explicit donated-example sequence required")
    if any(not isinstance(row, Donation) for row in donations) or len({d.identity for d in donations}) != len(donations):
        raise ValueError("typed uniquely identified donations required")
    target = _row(schema, synthetic_metadata)
    distances = [(sum(x != y for x, y in zip(target, _row(schema, d.metadata))), index, d)
                 for index, d in enumerate(donations)]
    return tuple((d, distance) for distance, _, d in sorted(distances, key=lambda row: (row[0], row[1]))[:k])


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only donated-example selection required")
    schema = {"area":("a", "b"), "length":(100., 200.)}
    donations = [Donation("x", {"area":"a", "length":100.}, "public example x", "fixture:consent-x"),
                 Donation("y", {"area":"b", "length":100.}, "public example y", "fixture:consent-y"),
                 Donation("z", {"area":"a", "length":200.}, "public example z", "fixture:consent-z")]
    result = select_examples({"area":"a", "length":200.}, donations, schema, k=2)
    checks = {"exact_categorical_match_first":result[0][0].identity == "z" and result[0][1] == 0,
              "not_numeric_euclidean":result[1][0].identity == "x" and result[1][1] == 1,
              "donated_text_not_regenerated":result[0][0] is donations[2],
              "no_dp_claim_or_private_training":REQUIRES_GPU_VALIDATION is False}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","checks":checks,
            "metrics":{"selected_examples":len(result),"best_hamming_count":result[0][1],"schema_fields":len(schema)}}
