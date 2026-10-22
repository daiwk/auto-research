"""DeepSEA fixed-release external-prediction scorer and public-input projection.

Answer extraction/scoring semantics are ported from Google DeepSEA evaluate.py
at 7c3abc06824c8cb634930ab6049176da30cfa0e7 (Copyright 2026 Google LLC,
Apache-2.0: https://www.apache.org/licenses/LICENSE-2.0). Character corpus chrF2
follows SacreBLEU 2.5.1's default CHRF(word_order=0) mathematical statistics.
No upstream script is executed, no model/API is invoked, and no training or
hyperparameter search consumes these held-out benchmark records. MetricX-24 is
NOT implemented and is never substituted with the release scorer's chrF.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Callable
import zipfile


UPSTREAM_REVISION = "7c3abc06824c8cb634930ab6049176da30cfa0e7"
MGSM_ARCHIVE_SHA256 = "d662677629e5105e60f3f360761500ca97e284163a9b8b726c054c43475e8a22"
MGSM_JSON_SHA256 = "9527f9693fbc2ba4e5b6ec4546f947888093c693f9231641016d6b8a52cdfb7d"
HIGH_RESOURCE_LANGS = ("th", "id", "vi", "fil")
LOW_RESOURCE_LANGS = ("ceb", "ilo", "jv", "km", "lo", "ms", "su", "my")
ALL_LANGS = ("en",) + HIGH_RESOURCE_LANGS + LOW_RESOURCE_LANGS
TASK_METRICS = {"mgsm": "numeric_exact_match", "indommlu": "subject_macro_accuracy",
                "xquad": "first_reference_token_f1", "crosssum": "corpus_chrf2",
                "wmt24": "corpus_chrf2_not_metricx24"}


def extract_number(output: str | None) -> str:
    if output is None:
        return ""
    tagged = re.findall(r"<answer>(.*?)</answer>", output, re.DOTALL)
    if tagged:
        output = tagged[-1]
    output = output.replace(",", "").strip()
    match = re.search(r"(-?\d+[\d\.]*)", output)
    if match:
        value = match.group(0)
        try:
            number = float(value)
            return str(int(number)) if number.is_integer() else str(number)
        except ValueError:
            return value
    return output


def extract_option(output: str | None) -> str:
    if output is None:
        return ""
    tagged = re.findall(r"<answer>(.*?)</answer>", output, re.DOTALL)
    if tagged:
        output = tagged[-1]
    match = re.search(r"\b([A-D])\b", output)
    if match:
        return match.group(1)
    match = re.search(r"\b([a-d])\b", output)
    return match.group(1).upper() if match else output.strip()


def extract_qa_answer(output: str) -> str:
    if not output:
        return ""
    tagged = re.findall(r"<answer>(.*?)</answer>", output, re.DOTALL)
    if tagged:
        answer = tagged[-1].strip()
    else:
        match = re.search(r"answer is\s+(.*)", output, re.IGNORECASE)
        answer = match.group(1).strip() if match else ""
    if answer:
        if answer.upper().endswith("ANSWER"):
            answer = answer[:-len("ANSWER")].strip()
        if answer.upper().startswith("ANSWER"):
            answer = answer[len("ANSWER"):].strip()
        if answer.endswith("</answer>"):
            answer = answer[:-len("</answer>")].strip()
        match = re.search(r"<([^<>]+)", answer)
        if match:
            answer = match.group(1)
        if answer.endswith("."):
            answer = answer[:-1].strip()
    return answer


def extract_summary(output: str) -> str:
    if not output:
        return ""
    if "<Target_Summary>" in output:
        closed = re.search(r"<Target_Summary>(.*?)</Target_Summary>", output, re.DOTALL)
        if closed:
            return closed.group(1)
        opened = re.search(r"<Target_Summary>(.*?)", output)
        if opened:
            return opened.group(1)
    if "Summary:" in output:
        return output.split("Summary:")[1].strip()
    if "\n\n**" in output:
        return output.split("\n\n**")[0].strip()
    return output


def token_f1(gold: str, prediction: str) -> float:
    """Fixed upstream whitespace/Unicode-word tokenization, not Thai segmentation."""
    reference = re.sub(r"[^\w\s]", "", gold.lower()).split()
    candidate = re.sub(r"[^\w\s]", "", prediction.lower()).split()
    if not reference:
        return 1.0 if not candidate else 0.0
    if not candidate:
        return 0.0
    shared = sum((Counter(reference) & Counter(candidate)).values())
    if not shared:
        return 0.0
    precision, recall = shared/len(candidate), shared/len(reference)
    return 2*precision*recall/(precision+recall)


def corpus_chrf2(predictions: list[str], references: list[str]) -> float:
    """SacreBLEU 2.5.1 CHRF defaults: nc=6,nw=0,beta=2,space=no,eff=yes.

    Corpus sufficient statistics are summed BEFORE precision/recall averaging.
    A candidate's n-grams are not counted where that segment's reference has no
    n-grams at that order, matching SacreBLEU's _get_match_statistics exactly.
    Empty input is rejected as by the upstream CHRF corpus entry point.
    """
    if not predictions or len(predictions) != len(references):
        raise ValueError("chrF requires nonempty aligned candidate/reference corpora")
    if not all(isinstance(x, str) for x in predictions+references):
        raise ValueError("chrF corpora must contain strings")
    statistics = [[0, 0, 0] for _ in range(6)]
    for hypothesis, reference in zip(predictions, references):
        hypothesis, reference = "".join(hypothesis.split()), "".join(reference.split())
        for n in range(1, 7):
            h = Counter(hypothesis[i:i+n] for i in range(len(hypothesis)-n+1))
            r = Counter(reference[i:i+n] for i in range(len(reference)-n+1))
            statistics[n-1][0] += sum(h.values()) if r else 0
            statistics[n-1][1] += sum(r.values())
            statistics[n-1][2] += sum((h & r).values())
    effective = [(h, r, m) for h, r, m in statistics if h > 0 and r > 0]
    if not effective:
        return 0.0
    precision = sum(m/h for h, r, m in effective)/len(effective)
    recall = sum(m/r for h, r, m in effective)/len(effective)
    return 500*precision*recall/(4*precision+recall) if precision+recall else 0.0


def _test(items):
    return items["test"] if isinstance(items, dict) and "test" in items else items


def _predictions(root, language: str, count: int, task: str) -> list[str]:
    if not isinstance(root, dict) or language not in root:
        raise ValueError(f"missing language predictions for {task}/{language}")
    rows = root[language]
    if not isinstance(rows, list) or not all(isinstance(x, str) for x in rows):
        raise ValueError(f"predictions for {task}/{language} must be a list of strings")
    if len(rows) != count:
        raise ValueError(f"prediction count mismatch for {task}/{language}: {len(rows)} != {count}")
    return rows


def score_predictions(task: str, gold_data: dict, predictions: dict) -> dict:
    """Evaluator-only function; predictions are frozen external outputs, not gold.

    Rates use 0..100, matching the official scorer, and reference selection,
    extraction quirks and IndoMMLU's subject macro-average are preserved.
    """
    if task not in TASK_METRICS:
        if task.lower().replace("-", "").startswith("metricx"):
            raise NotImplementedError("MetricX-24 is not implemented; chrF is not a substitute")
        raise ValueError("unsupported DeepSEA task")
    if not isinstance(gold_data, dict) or not gold_data:
        raise ValueError("gold_data must be a nonempty language mapping")
    scores = {}
    for language, source in gold_data.items():
        rows = _test(source)
        if task == "indommlu":
            if not isinstance(predictions, dict) or not isinstance(predictions.get(language), dict):
                raise ValueError("IndoMMLU requires a subject prediction mapping per language")
            subject_scores = []
            for subject, items in rows.items():
                answers = [str(item["answer"]).strip().upper() for item in items]
                pred = _predictions(predictions[language], subject, len(answers), f"indommlu/{language}")
                correct = sum(g == extract_option(p) and g != "" for g, p in zip(answers, pred))
                subject_scores.append(100*correct/len(answers) if answers else 0.0)
            scores[language] = sum(subject_scores)/len(subject_scores) if subject_scores else 0.0
            continue
        pred = _predictions(predictions, language, len(rows), task)
        if task == "mgsm":
            answers = [extract_number(str(item.get("answer", ""))) for item in rows]
            correct = sum(g == extract_number(p) and g != "" for g, p in zip(answers, pred))
            scores[language] = 100*correct/len(answers) if answers else 0.0
        elif task == "xquad":
            values = [token_f1(item["answers"][0]["text"], extract_qa_answer(p))
                      for item, p in zip(rows, pred)]
            scores[language] = 100*sum(values)/len(values) if values else 0.0
        elif task == "crosssum":
            scores[language] = corpus_chrf2([extract_summary(p) for p in pred],
                                            [item["summary"] for item in rows])
        else:
            scores[language] = corpus_chrf2([p.strip() for p in pred],
                                            [item["target"] for item in rows])
    averages = {}
    for name, languages in (("high_sea", HIGH_RESOURCE_LANGS), ("low_sea", LOW_RESOURCE_LANGS),
                             ("all_sea", HIGH_RESOURCE_LANGS+LOW_RESOURCE_LANGS)):
        if all(language in scores for language in languages):
            averages[name] = sum(scores[language] for language in languages)/len(languages)
    return {"task": task, "metric": TASK_METRICS[task], "scale": "0..100",
            "per_language": scores, "tier_macro_averages": averages,
            "metricx_implemented": False, "upstream_revision": UPSTREAM_REVISION}


@dataclass(frozen=True)
class PublicExample:
    """Only fields the evaluated predictor may receive; values are immutable."""
    example_id: str
    task: str
    language: str
    fields: tuple[tuple[str, str | tuple[str, ...]], ...]

    def model_input(self) -> dict:
        return {name: list(value) if isinstance(value, tuple) else value for name, value in self.fields}


class DeepSEATask:
    """Evaluator-owned gold and separately constructed predictor-visible inputs.

    The predictor receives PublicExample only, never this object or _gold.
    This separation is an API data-flow contract, not an OS security sandbox.
    """
    def __init__(self, task: str, gold_data: dict):
        if task not in TASK_METRICS or not isinstance(gold_data, dict) or not gold_data:
            raise ValueError("known task and nonempty official language mapping required")
        self.task = task
        self._gold = deepcopy(gold_data)
        self._public: tuple[PublicExample, ...] = self._project()

    def _project(self) -> tuple[PublicExample, ...]:
        result = []
        fields = {"mgsm": ("question",), "xquad": ("context", "question"),
                  "crosssum": ("text",), "wmt24": ("source",),
                  "indommlu": ("question", "options")}[self.task]
        for language, source in self._gold.items():
            if language not in ALL_LANGS:
                raise ValueError("language outside fixed DeepSEA release")
            data = _test(source)
            branches = data.items() if self.task == "indommlu" else (("", data),)
            for subject, rows in branches:
                if not isinstance(rows, list):
                    raise ValueError("each task/subject split must be a list")
                for index, row in enumerate(rows):
                    projected = []
                    for name in fields:
                        value = row[name]
                        if name == "options":
                            if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
                                raise ValueError("options must be a list of strings")
                            value = tuple(value)
                        elif not isinstance(value, str):
                            raise ValueError("public source fields must be strings")
                        projected.append((name, value))
                    if subject:
                        projected.append(("subject", str(subject)))
                    identity = f"{self.task}/{language}/{subject}/{index}"
                    result.append(PublicExample(identity, self.task, language, tuple(projected)))
        return tuple(result)

    def public_examples(self) -> tuple[PublicExample, ...]:
        return self._public

    def score(self, predictions: dict) -> dict:
        return score_predictions(self.task, self._gold, predictions)

    def evaluate_predictor(self, predictor: Callable[[PublicExample], str]) -> dict:
        predictions: dict = {}
        for row in self._public:
            value = predictor(row)
            if not isinstance(value, str):
                raise ValueError("predictor must return a string")
            if self.task == "indommlu":
                subject = dict(row.fields)["subject"]
                predictions.setdefault(row.language, {}).setdefault(subject, []).append(value)
            else:
                predictions.setdefault(row.language, []).append(value)
        return self.score(predictions)


def load_official_json(path: Path, task: str, *, expected_sha256: str) -> DeepSEATask:
    """Read an explicitly supplied fixed public JSON; never execute an upstream file."""
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("a fixed source SHA-256 is mandatory")
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("official data SHA-256 mismatch")
    return DeepSEATask(task, json.loads(raw))


def inspect_fixed_mgsm_archive(path: Path) -> dict:
    """Hash/schema validation only: do not return benchmark text or any answer.

    The official archive password is a public anti-crawler notice, not a secret.
    Read one named member in memory; never extract paths or execute setup code.
    No predictions or model scores are generated from official test records.
    """
    archive = Path(path).read_bytes()
    if hashlib.sha256(archive).hexdigest() != MGSM_ARCHIVE_SHA256:
        raise ValueError("MGSM archive does not match the fixed official release")
    with zipfile.ZipFile(path) as source:
        info = source.getinfo("mgsm.json")
        if info.file_size != 1_954_503:
            raise ValueError("unexpected official MGSM member size")
        raw = source.read("mgsm.json", pwd=b"DeepSEA_Bench_2026")
    if hashlib.sha256(raw).hexdigest() != MGSM_JSON_SHA256:
        raise ValueError("MGSM JSON does not match the fixed official release")
    data = json.loads(raw)
    task = DeepSEATask("mgsm", data)
    examples = task.public_examples()
    counts = Counter(example.language for example in examples)
    if set(counts) != set(ALL_LANGS) or set(counts.values()) != {250}:
        raise ValueError("official release must have 13 languages and 250 test rows each")
    prefix = [example for language in ALL_LANGS for example in examples
              if example.language == language and example.example_id.endswith(("/0", "/1"))]
    serial = [{"id": e.example_id, "language": e.language, "public_input": e.model_input()} for e in prefix]
    encoded = json.dumps(serial, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return {"upstream_revision": UPSTREAM_REVISION, "archive_sha256": MGSM_ARCHIVE_SHA256,
            "json_sha256": MGSM_JSON_SHA256, "json_bytes": len(raw),
            "test_rows": len(examples), "language_test_counts": dict(counts),
            "projected_prefix_rows": len(prefix), "projected_prefix_sha256": hashlib.sha256(encoded).hexdigest(),
            "public_field_names": ["question"], "gold_fields_excluded": ["answer", "answer_with_cot"],
            "split": "test", "model_calls": 0, "used_for_training_or_selection": False,
            "benchmark_text_exported": False, "diagnostic_only": True}


def diagnostic(seed: int = 42) -> dict:
    """Synthetic scorer contracts only; no supplied-correct output called model accuracy."""
    gold = {"en": {"test": [{"question": "synthetic-q", "answer": "12", "answer_with_cot": "private-gold"},
                              {"question": "synthetic-r", "answer": "7"}]}}
    task = DeepSEATask("mgsm", gold)
    math_score = task.score({"en": ["<answer>12.0</answer>", "<answer>8</answer>"]})["per_language"]["en"]
    science = {"en": {"test": {"one": [{"question": "x", "options": ["one", "two"], "answer": "A"}],
                                 "many": [{"question": "y", "options": ["one", "two"], "answer": "B"}]*3}}}
    macro = score_predictions("indommlu", science, {"en": {"one": ["A"], "many": ["A"]*3}})["per_language"]["en"]
    qa = score_predictions("xquad", {"en": [{"context": "x", "question": "q", "answers": [{"text": "red blue"}, {"text": "green"}]}]},
                           {"en": ["<answer>green</answer>"]})["per_language"]["en"]
    summary = score_predictions("crosssum", {"en": [{"text": "source", "summary": "a"}]},
                                {"en": ["<Target_Summary>a</Target_Summary>"]})["per_language"]["en"]
    translation = score_predictions("wmt24", {"th": [{"source": "input", "target": "ภาษาไทย"}]},
                                    {"th": ["ภาษาไทย"]})["per_language"]["th"]
    rejected = 0
    for bad in ({}, {"en": ["one"]}, {"en": ["one", 12]}):
        try:
            task.score(bad)
        except ValueError:
            rejected += 1
    metricx_rejected = False
    try:
        score_predictions("metricx24", gold, {})
    except NotImplementedError:
        metricx_rejected = True
    private = any("answer" in key or "gold" in key for example in task.public_examples()
                  for key in example.model_input())
    error = max(abs(a-b) for a, b in zip((math_score, macro, qa, summary, translation),
                                        (50.0, 50.0, 0.0, 100.0, 100.0)))
    checks = {"five_task_reference_scores": error < 1e-12, "subject_macro_not_micro": macro == 50,
              "first_qa_reference_not_oracle": qa == 0, "prediction_coverage_rejected": rejected == 3,
              "public_input_excludes_gold": not private, "metricx_not_substituted": metricx_rejected,
              "unicode_chrf_and_whitespace": corpus_chrf2(["ภาษา ไทย"], ["ภาษาไทย"]) == 100}
    return {"seed": seed, "checks": checks,
            "metrics": {"scorer_contract_cases": 7.0, "reference_score_error": float(error),
                        "coverage_rejection_count": float(rejected), "model_calls": 0.0},
            "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost",
            "upstream_revision": UPSTREAM_REVISION}
