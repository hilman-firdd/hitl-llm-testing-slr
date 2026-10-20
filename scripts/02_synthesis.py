"""Step 2. Descriptive synthesis of the included studies (Tables 5 to 7 and the sensitivity check).

Input  : data/extraction/extraction_quality.csv
Outputs: outputs/descriptives.json
         outputs/tables/included_studies.csv      (Table 5)
         outputs/tables/roles_by_activity.csv     (Table 6)
         outputs/tables/evaluation_levels.csv     (Table 7)
         outputs/tables/intervention_points.csv
         outputs/tables/sensitivity_qa.csv        (thresholds 2.5 to 4.0)
"""
from collections import Counter

from common import (EVAL_LEVELS, OUT, POINTS, QA_THRESHOLD, ROLES, TABLES, load_studies,
                    split_codes, write_csv, write_json)


def counts(studies):
    return dict(
        n=len(studies),
        year=dict(sorted(Counter(s["year"] for s in studies).items())),
        activity=dict(Counter(s["activity"] for s in studies).most_common()),
        roles=dict(Counter(r for s in studies for r in split_codes(s["roles"])).most_common()),
        point=dict(Counter(p for s in studies for p in split_codes(s["point"])).most_common()),
        evaluation=dict(sorted(Counter(s["evaluation"] for s in studies).items())),
        evidence=dict(Counter(s["evidence"] for s in studies).most_common()),
        country=dict(Counter(s["country"] for s in studies).most_common()),
        roles_per_study=dict(sorted(Counter(len(split_codes(s["roles"])) for s in studies).items())),
    )


def main():
    studies = load_studies()
    inc = [s for s in studies if s["qa_total"] >= QA_THRESHOLD]
    D = counts(inc)
    D["qa_mean"] = round(sum(s["qa_total"] for s in inc) / len(inc), 2)
    write_json(OUT / "descriptives.json", D)

    # Table 5
    write_csv(TABLES / "included_studies.csv", [
        dict(study=s["key"], year=s["year"], activity=s["activity"], roles=s["roles"], point=s["point"],
             evaluation=s["evaluation"], qa_total=s["qa_total"], evidence=s["evidence"], doi=s["doi"])
        for s in sorted(inc, key=lambda s: (-s["qa_total"], s["key"]))])

    # Table 6: roles x activity
    acts = list(D["activity"].keys())
    rows = []
    for a in acts:
        sub = [s for s in inc if s["activity"] == a]
        row = {"activity": f"{a} ({len(sub)})"}
        row.update({r: sum(r in split_codes(s["roles"]) for s in sub) for r in ROLES})
        rows.append(row)
    total = {"activity": "Total"}
    total.update({r: sum(row[r] for row in rows) for r in ROLES})
    write_csv(TABLES / "roles_by_activity.csv", rows + [total])

    # Table 7: evaluation levels
    labels = {"E1": "Controlled study with participants under two or more conditions",
              "E2": "Field or log data on human decisions",
              "E3": "Human step present but not measured",
              "E4": "Qualitative study of practice and perception"}
    write_csv(TABLES / "evaluation_levels.csv", [
        dict(level=e, description=labels[e], n=sum(s["evaluation"] == e for s in inc),
             studies="; ".join(s["key"] for s in inc if s["evaluation"] == e)) for e in EVAL_LEVELS])

    write_csv(TABLES / "intervention_points.csv", [
        dict(point=p, n=sum(p in split_codes(s["point"]) for s in inc)) for p in POINTS])

    # Sensitivity of the main patterns to the QA threshold
    sens = []
    for th in (2.5, 3.0, 3.5, 4.0):
        sub = [s for s in studies if s["qa_total"] >= th]
        c = counts(sub)
        sens.append(dict(threshold=th, studies=len(sub), top_role=next(iter(c["roles"]), ""),
                         reviewer=c["roles"].get("Reviewer", 0),
                         **{e: c["evaluation"].get(e, 0) for e in EVAL_LEVELS}))
    write_csv(TABLES / "sensitivity_qa.csv", sens)

    print(f"Included studies: {len(inc)} (mean QA {D['qa_mean']})")
    for k in ("roles", "point", "evaluation", "activity"):
        print(f"  {k}: {D[k]}")
    print("  sensitivity:", [(r['threshold'], r['studies'], r['top_role']) for r in sens])


if __name__ == "__main__":
    main()
