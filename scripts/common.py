"""Shared paths, loaders and code labels for the replication scripts."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
TABLES = OUT / "tables"
FIGURES = OUT / "figures"
for p in (OUT, TABLES, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

QA_THRESHOLD = 3.0
SEARCH_DATE = "2026-10-20"

CODES = {
    "I": "Include to full text",
    "M": "Unclear, check full text",
    "EC1": "Not about testing a software artefact",
    "EC2": "No LLM or generative model",
    "EC3": "Human only as research evaluator",
    "EC4": "Secondary, conceptual, short paper, thesis or preprint",
    "EC5": "Duplicate or earlier version of an included study",
    "EC6": "Human role not described",
    "NR": "Report not retrieved",
    "INC": "Eligible",
}
ROLES = ["Specifier", "Explorer", "Reviewer", "Editor", "Oracle", "Teacher"]
POINTS = ["Before", "Loop", "After"]
EVAL_LEVELS = ["E1", "E2", "E3", "E4"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    rows = list(rows)
    fields = fields or (list(rows[0].keys()) if rows else [])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


def norm_title(t):
    """Normalised title used for duplicate detection."""
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def split_codes(x):
    return [t.strip() for t in (x or "").split(";") if t.strip()]


def load_studies():
    """22 eligible studies with QA scores as floats and a qa_total field."""
    studies = read_csv(DATA / "extraction" / "extraction_quality.csv")
    for s in studies:
        s["year"] = int(s["year"])
        s["qa"] = [float(s[f"QA{i}"]) for i in range(1, 7)]
        s["qa_total"] = sum(s["qa"])
    return studies
