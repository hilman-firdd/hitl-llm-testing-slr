"""Robustness and reporting analyses added in v1.0.2.

Produces four reproducible outputs, all from data/extraction/extraction_quality.csv:
  1. checklist_coverage.csv  - retrospective application of the six-item reporting
                               checklist to the included corpus (how often each item
                               is currently met). This is corpus-based validation, NOT
                               practitioner (face) validation, which remains future work.
  2. venue_coverage.csv      - publisher/venue distribution of the included studies,
                               i.e. how much IEEE/ACM-venue work the OpenAlex+Scopus
                               search actually captured.
  3. proportion_cis.csv      - Wilson 95% confidence intervals for the headline
                               proportions, so small-cell estimates carry uncertainty.
  4. fulltext_primary.csv    - the headline role/point/evaluation counts restricted to
                               the 25 full-text studies (the primary, more reliable set),
                               with the 10 abstract-only studies reported separately.
"""
import math
from common import load_studies, write_csv, write_json, split_codes, ROLES, POINTS, EVAL_LEVELS, QA_THRESHOLD, TABLES, OUT


def included():
    return [s for s in load_studies() if s["qa_total"] >= QA_THRESHOLD]


def wilson(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (round(p * 100, 1), round(max(0.0, centre - half) * 100, 1), round(min(1.0, centre + half) * 100, 1))


# ---------------------------------------------------------------- checklist
def checklist_coverage(studies):
    """Map each checklist item to the quality-appraisal signal that records it and
    count how many studies fully (score 1), partly (0.5), or do not (0) report it.
    Item 6 (effect isolated) is a yes/no coded item."""
    ft = [s for s in studies if s["evidence"] == "F"]

    def qa_breakdown(group, idx):
        full = sum(1 for s in group if s["qa"][idx] == 1)
        part = sum(1 for s in group if s["qa"][idx] == 0.5)
        none = sum(1 for s in group if s["qa"][idx] == 0)
        return full, part, none

    # (checklist item text, evidence signal, qa index or None for the isolated flag)
    items = [
        ("1-3 Person described (who, when, which action)", "QA2", 1),
        ("4 LLM and version reported", "QA3", 2),
        ("(support) Evaluation data and metrics defined", "QA4", 3),
        ("5 Human step measured", "QA5", 4),
        ("6 Effect of the human step isolated", "isolated flag", None),
    ]
    rows = []
    for label, signal, idx in items:
        if idx is None:
            fa = sum(1 for s in studies if s["isolated"] == "yes")
            fa_ft = sum(1 for s in ft if s["isolated"] == "yes")
            rows.append({"checklist_item": label, "evidence": signal,
                         "all35_fully": fa, "all35_partly": 0, "all35_not": len(studies) - fa,
                         "all35_pct_fully": round(fa / len(studies) * 100, 1),
                         "fulltext25_fully": fa_ft,
                         "fulltext25_pct_fully": round(fa_ft / len(ft) * 100, 1)})
        else:
            f, p, n = qa_breakdown(studies, idx)
            fft, _, _ = qa_breakdown(ft, idx)
            rows.append({"checklist_item": label, "evidence": signal,
                         "all35_fully": f, "all35_partly": p, "all35_not": n,
                         "all35_pct_fully": round(f / len(studies) * 100, 1),
                         "fulltext25_fully": fft,
                         "fulltext25_pct_fully": round(fft / len(ft) * 100, 1)})
    write_csv(TABLES / "checklist_coverage.csv", rows,
              ["checklist_item", "evidence", "all35_fully", "all35_partly", "all35_not",
               "all35_pct_fully", "fulltext25_fully", "fulltext25_pct_fully"])
    return rows


# ---------------------------------------------------------------- venue
def publisher_of(venue):
    v = (venue or "").lower()
    if "ieee" in v and "acm" in v:
        return "IEEE/ACM (joint, e.g. ICSE)"
    if "ieee" in v or "softcom" in v:
        return "IEEE"
    if "acm" in v or "chi conf" in v or "chitaly" in v or "sigchi" in v or "uist" in v:
        return "ACM"
    if any(k in v for k in ("acl", "emnlp", "naacl", "comput. linguist")):
        return "ACL Anthology"
    if any(k in v for k in ("internet of things", "information and software", "journal of systems",
                            "science of computer", "sciencedirect", "elsevier")):
        return "Elsevier"
    if any(k in v for k in ("springer", "lecture notes", "lncs", "empir", "software qual")):
        return "Springer"
    if any(k in v for k in ("sbc", "brazilian", "brasileiro", "sbes", "cbsoft", "sbqs", "anais", "simposio", "simpósio")):
        return "SBC (Brazilian CS)"
    if "arxiv" in v:
        return "arXiv"
    return "Other (regional/specialist venues)"


def venue_coverage(studies):
    from collections import Counter
    c = Counter(publisher_of(s["venue"]) for s in studies)
    rows = [{"publisher_or_source": k, "n_studies": v,
             "pct": round(v / len(studies) * 100, 1)}
            for k, v in sorted(c.items(), key=lambda x: -x[1])]
    ieee_acm = sum(v for k, v in c.items() if k.startswith(("IEEE", "ACM")))
    rows.append({"publisher_or_source": "-- IEEE or ACM venues (subtotal) --",
                 "n_studies": ieee_acm, "pct": round(ieee_acm / len(studies) * 100, 1)})
    write_csv(TABLES / "venue_coverage.csv", rows, ["publisher_or_source", "n_studies", "pct"])
    return rows


# ---------------------------------------------------------------- CIs
def proportion_cis(studies):
    ft = [s for s in studies if s["evidence"] == "F"]
    ab = [s for s in studies if s["evidence"] == "A"]

    def has_role(s, r): return r.lower() in [x.lower() for x in split_codes(s["roles"])]
    def after_only(s): return [p.lower() for p in split_codes(s["point"])] == ["after"]
    def before_or_loop(s):
        pts = [p.lower() for p in split_codes(s["point"])]
        return ("before" in pts) or ("loop" in pts)
    def one_role(s): return len(split_codes(s["roles"])) == 1

    defs = [
        ("Reviewer is coded (all 35)", sum(has_role(s, "Reviewer") for s in studies), len(studies)),
        ("Person acts before or during generation (all 35)", sum(before_or_loop(s) for s in studies), len(studies)),
        ("Person only after generation (all 35)", sum(after_only(s) for s in studies), len(studies)),
        ("After-only, full text", sum(after_only(s) for s in ft), len(ft)),
        ("After-only, abstract", sum(after_only(s) for s in ab), len(ab)),
        ("One role only, full text", sum(one_role(s) for s in ft), len(ft)),
        ("One role only, abstract", sum(one_role(s) for s in ab), len(ab)),
        ("Human step unmeasured (E3), full text", sum(s["evaluation"] == "E3" for s in ft), len(ft)),
        ("Human step unmeasured (E3), abstract", sum(s["evaluation"] == "E3" for s in ab), len(ab)),
    ]
    rows = []
    for label, k, n in defs:
        p, lo, hi = wilson(k, n)
        rows.append({"indicator": label, "k": k, "n": n, "pct": p,
                     "ci95_low": lo, "ci95_high": hi})
    write_csv(TABLES / "proportion_cis.csv", rows, ["indicator", "k", "n", "pct", "ci95_low", "ci95_high"])
    return rows


# ---------------------------------------------------------------- full-text primary
def fulltext_primary(studies):
    ft = [s for s in studies if s["evidence"] == "F"]

    def count_roles(group):
        return {r: sum(1 for s in group if r.lower() in [x.lower() for x in split_codes(s["roles"])]) for r in ROLES}
    def count_points(group):
        return {p: sum(1 for s in group if p.lower() in [x.lower() for x in split_codes(s["point"])]) for p in POINTS}
    def count_eval(group):
        return {e: sum(1 for s in group if s["evaluation"] == e) for e in EVAL_LEVELS}

    obj = {
        "n_fulltext": len(ft),
        "roles_fulltext": count_roles(ft),
        "points_fulltext": count_points(ft),
        "evaluation_fulltext": count_eval(ft),
    }
    write_json(OUT / "fulltext_primary.json", obj)
    rows = [{"dimension": "role", "label": r, "n_fulltext": obj["roles_fulltext"][r]} for r in ROLES]
    rows += [{"dimension": "point", "label": p, "n_fulltext": obj["points_fulltext"][p]} for p in POINTS]
    rows += [{"dimension": "evaluation", "label": e, "n_fulltext": obj["evaluation_fulltext"][e]} for e in EVAL_LEVELS]
    write_csv(TABLES / "fulltext_primary.csv", rows, ["dimension", "label", "n_fulltext"])
    return obj


if __name__ == "__main__":
    st = included()
    cl = checklist_coverage(st)
    vc = venue_coverage(st)
    ci = proportion_cis(st)
    fp = fulltext_primary(st)
    print("checklist_coverage rows:", len(cl))
    print("venue_coverage rows:", len(vc))
    print("proportion_cis rows:", len(ci))
    print("fulltext primary roles:", fp["roles_fulltext"])
