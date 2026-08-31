from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import tarfile
import urllib.request
import zipfile
from pathlib import Path

SHAKESPEARE_URL = (
    "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
)
# GroupLens' TLS certificate expired in August 2026 and broke clean CI runners.
# This immutable GitHub mirror is byte-identical to the official archive; the
# SHA-256 gate below prevents the mirror from silently changing the benchmark.
MOVIELENS_URL = (
    "https://raw.githubusercontent.com/rudrasingh21/Data-ML-100k-/"
    "f74a79d7debb00d39a8b757876b6b2038d52825c/ml-100k.zip"
)
MOVIELENS_SHA256 = "50d2a982c66986937beb9ffb3aa76efe955bf3d5c6b761f4e3a7cd717c6a3229"
MOVIELENS_1M_BASE_URL = (
    "https://raw.githubusercontent.com/vandit15/Movielens-Data/"
    "19e4c9d1423bf3f2ccc1a3093823c362c49950b9/ml-1m"
)
MOVIELENS_1M_FILES = {
    "ratings.dat": "506d64ca44484487c11dc2d9a28de5c54948213e6b96285e298afe28d6ea4e0f",
    "movies.dat": "0140fc2356357c1a851d0f52e893a1e4d3696df632c4141cea8d5bc3d621f0b9",
}
AMAZON_BEAUTY_5CORE_URL = (
    "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Beauty_5.json.gz"
)
MDCNS_BEAUTY_BASE_URL = (
    "https://raw.githubusercontent.com/Lyz103/SIGIR26-MDCNS/main/MDCNS_Code/data"
)
KUAIRAND_PURE_URL = "https://zenodo.org/records/10439422/files/KuaiRand-Pure.tar.gz"
WIKITEXT_2_BASE_URL = (
    "https://raw.githubusercontent.com/pytorch/examples/main/word_language_model/data/wikitext-2"
)
ALPACA_URL = "https://raw.githubusercontent.com/tatsu-lab/stanford_alpaca/main/alpaca_data.json"
GSM8K_REVISION = "3101c7d5072418e28b9008a6636bde82a006892c"
GSM8K_BASE_URL = (
    "https://raw.githubusercontent.com/openai/grade-school-math/"
    f"{GSM8K_REVISION}/grade_school_math/data"
)
GSM8K_FILES = {
    "train.jsonl": "17f347dc51477c50d4efb83959dbb7c56297aba886e5544ee2aaed3024813465",
    "test.jsonl": "3730d312f6e3440559ace48831e51066acaca737f6eabec99bccb9e4b3c39d14",
}
DELICIOUS_2K_BASE_URL = (
    "https://raw.githubusercontent.com/qcymkxyc/RecSys/"
    "cb313bf92f80d3cd7c7bde39b12ab4319ccf61a8/data/delicious-2k"
)
DELICIOUS_2K_FILES = {
    "user_taggedbookmarks-timestamps.dat": (
        "df88bb692dc67dbdb844221f967dc8d1a89fb068c6d2f3bb8f602b952dd9cca2"
    ),
    "user_contacts-timestamps.dat": (
        "67bb2d462bd794a331f501d7d480fc02eef196548f51a5a23a28e2e50736968c"
    ),
    "bookmark_tags.dat": "a178dfa1169729c0fe592449342856e2e855dbaf280a5016faff75d2f65464b4",
}


def tiny_shakespeare(root: Path, allow_network: bool = True) -> str:
    target = root / "tiny_shakespeare.txt"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        _download(SHAKESPEARE_URL, target)
    return target.read_text(encoding="utf-8")


def wikitext_2(root: Path, allow_network: bool = True) -> dict[str, str]:
    """Load the standard WikiText-2 train/validation/test files."""
    directory = root / "wikitext-2"
    result = {}
    for split, filename in (
        ("train", "train.txt"),
        ("validation", "valid.txt"),
        ("test", "test.txt"),
    ):
        target = directory / filename
        if not target.exists():
            if not allow_network:
                raise FileNotFoundError(f"dataset missing and network disabled: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            _download(f"{WIKITEXT_2_BASE_URL}/{filename}", target)
        result[split] = target.read_text(encoding="utf-8")
    return result


def alpaca_instructions(root: Path, allow_network: bool = True) -> list[dict[str, str]]:
    """Load Stanford Alpaca's public instruction-following examples."""
    target = root / "alpaca" / "alpaca_data.json"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        _download(ALPACA_URL, target)
    rows = json.loads(target.read_text(encoding="utf-8"))
    return [
        {
            "instruction": str(row["instruction"]),
            "input": str(row.get("input", "")),
            "output": str(row["output"]),
        }
        for row in rows
    ]


def gsm8k(root: Path, allow_network: bool = True) -> dict[str, list[dict[str, str]]]:
    """Load OpenAI's official GSM8K train/test JSONL files."""
    directory = root / "gsm8k"
    result = {}
    for split in ("train", "test"):
        target = directory / f"{split}.jsonl"
        if not target.exists():
            if not allow_network:
                raise FileNotFoundError(f"dataset missing and network disabled: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            _download(
                f"{GSM8K_BASE_URL}/{split}.jsonl",
                target,
                expected_sha256=GSM8K_FILES[f"{split}.jsonl"],
            )
        result[split] = [
            {
                "question": str(row["question"]),
                "answer": str(row["answer"]),
            }
            for row in (
                json.loads(line)
                for line in target.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        ]
    return result


def movielens_100k(root: Path, allow_network: bool = True) -> list[tuple[int, int, float, int]]:
    target = root / "ml-100k" / "u.data"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {target}")
        archive = root / "ml-100k.zip"
        archive.parent.mkdir(parents=True, exist_ok=True)
        _download(MOVIELENS_URL, archive, expected_sha256=MOVIELENS_SHA256)
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(root)
    rows: list[tuple[int, int, float, int]] = []
    with target.open(encoding="utf-8") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            rows.append((int(row[0]), int(row[1]), float(row[2]), int(row[3])))
    return rows


def movielens_1m(root: Path, allow_network: bool = True) -> list[tuple[int, int, float, int]]:
    directory = root / "ml-1m"
    required = tuple(directory / filename for filename in MOVIELENS_1M_FILES)
    missing = tuple(path for path in required if not path.exists())
    if missing:
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {missing[0]}")
        directory.mkdir(parents=True, exist_ok=True)
        for path in missing:
            _download(
                f"{MOVIELENS_1M_BASE_URL}/{path.name}",
                path,
                expected_sha256=MOVIELENS_1M_FILES[path.name],
            )
    target = directory / "ratings.dat"
    rows: list[tuple[int, int, float, int]] = []
    with target.open(encoding="utf-8") as stream:
        for line in stream:
            user, item, rating, timestamp = line.rstrip().split("::")
            rows.append((int(user), int(item), float(rating), int(timestamp)))
    return rows


def delicious_2k_files(root: Path, allow_network: bool = True) -> Path:
    """Return the official HetRec 2011 Delicious-2K directory.

    ConnectionMind evaluates on Delicious and Foursquare.  Delicious-2K is the
    smaller fully public graph and contains the three relations needed by the
    local reproduction: user-bookmark-tag events, bookmark-tag edges and social
    contacts.  Only those relations are downloaded; each file is pinned to an
    immutable mirror commit and checksum-verified.
    """
    directory = root / "hetrec2011-delicious-2k"
    target = directory / "user_taggedbookmarks-timestamps.dat"
    required = tuple(directory / filename for filename in DELICIOUS_2K_FILES)
    if all(path.exists() for path in required):
        return directory
    if not allow_network:
        raise FileNotFoundError(f"dataset missing and network disabled: {target}")
    directory.mkdir(parents=True, exist_ok=True)
    for filename, sha256 in DELICIOUS_2K_FILES.items():
        _download(
            f"{DELICIOUS_2K_BASE_URL}/{filename}",
            directory / filename,
            expected_sha256=sha256,
        )
    return directory


def amazon_beauty_5core(
    root: Path, allow_network: bool = True
) -> list[tuple[str, str, float, int]]:
    target = root / "amazon-beauty-5core" / "reviews_Beauty_5.json.gz"
    if not target.exists():
        if not allow_network:
            raise FileNotFoundError(f"dataset missing and network disabled: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        _download(AMAZON_BEAUTY_5CORE_URL, target)
    rows: list[tuple[str, str, float, int]] = []
    with gzip.open(target, "rt", encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            rows.append(
                (
                    record["reviewerID"],
                    record["asin"],
                    float(record.get("overall", 1.0)),
                    int(record["unixReviewTime"]),
                )
            )
    return rows


def mdcns_beauty_sequences(
    root: Path, allow_network: bool = True
) -> dict[str, list[tuple[int, ...]]]:
    directory = root / "mdcns-beauty"
    result: dict[str, list[tuple[int, ...]]] = {}
    for split in ("train", "val", "test"):
        target = directory / f"Beauty_{split}.txt"
        if not target.exists():
            if not allow_network:
                raise FileNotFoundError(f"dataset missing and network disabled: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            _download(f"{MDCNS_BEAUTY_BASE_URL}/Beauty_{split}.txt", target)
        with target.open(encoding="utf-8") as stream:
            result[split] = [tuple(map(int, line.split())) for line in stream if line.strip()]
    return result


def kuairand_pure_files(root: Path, allow_network: bool = True) -> Path:
    """Return the official KuaiRand-Pure data directory, downloading it if needed."""
    directory = root / "kuairand-pure" / "data"
    target = directory / "log_standard_4_22_to_5_08_pure.csv"
    if target.exists():
        return directory
    if not allow_network:
        raise FileNotFoundError(f"dataset missing and network disabled: {target}")
    archive = root / "KuaiRand-Pure.tar.gz"
    archive.parent.mkdir(parents=True, exist_ok=True)
    _download(KUAIRAND_PURE_URL, archive)
    extraction = root / "kuairand-pure"
    extraction.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        prefix = members[0].name.split("/", 1)[0] + "/"
        for member in members:
            member.name = member.name.removeprefix(prefix)
            if member.name:
                if member.issym() or member.islnk():
                    raise ValueError(f"archive links are not allowed: {member.name}")
                destination = (extraction / member.name).resolve()
                if extraction.resolve() not in destination.parents:
                    raise ValueError(f"unsafe archive member: {member.name}")
                bundle.extract(member, extraction)
    return directory


def _download_and_extract(
    root: Path, archive_name: str, url: str, target: Path, allow_network: bool
) -> None:
    if not allow_network:
        raise FileNotFoundError(f"dataset missing and network disabled: {target}")
    archive = root / archive_name
    archive.parent.mkdir(parents=True, exist_ok=True)
    _download(url, archive)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(root)


def _download(url: str, target: Path, *, expected_sha256: str | None = None) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "auto-research/0.1"})
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
    if expected_sha256:
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected_sha256:
            raise ValueError(
                f"dataset checksum mismatch for {url}: expected {expected_sha256}, got {actual}"
            )
    target.write_bytes(payload)
