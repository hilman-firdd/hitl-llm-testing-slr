"""Step 1. Deduplicate records and compute every number in the PRISMA 2020 flow diagram.

Inputs : data/raw/openalex_records.csv, data/raw/citation_search_seeds.csv,
         data/decisions/title_abstract_screening.csv, data/decisions/fulltext_eligibility.csv,
         data/extraction/extraction_quality.csv
Outputs: outputs/prisma_counts.json, outputs/screening_log.csv, outputs/search_log.csv
"""
from collections import Counter

from common import (CODES, DATA, OUT, QA_THRESHOLD, SEARCH_DATE, load_studies, norm_title,
                    read_csv, write_csv, write_json)


def main():
    records = read_csv(DATA / "raw" / "openalex_records.csv")
    ta = {r["openalex_id"]: r["decision"] for r in read_csv(DATA / "decisions" / "title_abstract_screening.csv")}
    ft_rows = read_csv(DATA / "decisions" / "fulltext_eligibility.csv")
    ft_db = {r["openalex_id"]: r["decision"] for r in ft_rows if r["source"] == "database"}
    ft_cs = {r["openalex_id"]: r["decision"] for r in ft_rows if r["source"] == "citation_search"}
    seeds = read_csv(DATA / "raw" / "citation_search_seeds.csv")
    studies = load_studies()

    # 1. duplicates (normalised title, first occurrence kept)
    seen, log = {}, []
    for r in records:
        k = norm_title(r["title"])
        dup_of = seen.get(k, "")
        seen.setdefault(k, r["openalex_id"])
        d_ta = "" if dup_of else ta[r["openalex_id"]]
        d_ft = ft_db.get(r["openalex_id"], "") if d_ta in ("I", "M") else ""
        log.append(dict(openalex_id=r["openalex_id"], doi=r["doi"], year=r["year"], title=r["title"],
                        duplicate_of=dup_of, title_abstract=d_ta, full_text=d_ft,
                        reason=CODES.get(d_ft or d_ta, "duplicate" if dup_of else "")))
    screened = [x for x in log if not x["duplicate_of"]]
    sought = [x for x in screened if x["title_abstract"] in ("I", "M")]
    missing = [x["openalex_id"] for x in sought if not x["full_text"]]
    assert not missing, f"full-text decision missing for {missing}"

    ta_count = Counter(x["title_abstract"] for x in screened)
    ft_count = Counter(x["full_text"] for x in sought)
    cs_count = Counter(ft_cs.values())
    sb_identified = sum(int(s["records_identified"]) for s in seeds)
    sb_sought = len(ft_cs)

    included = [s for s in studies if s["qa_total"] >= QA_THRESHOLD]
    assert ft_count["INC"] + cs_count["INC"] == len(studies), "eligible studies and extraction sheet do not match"

    prisma = dict(
        db_identified=len(records), duplicates=len(records) - len(screened), screened=len(screened),
        excluded_ta=sum(v for k, v in ta_count.items() if k.startswith("EC")),
        ta_breakdown=dict(sorted(ta_count.items())),
        sought=len(sought), not_retrieved=ft_count["NR"], assessed=len(sought) - ft_count["NR"],
        excluded_full={k: v for k, v in sorted(ft_count.items()) if k.startswith("EC")},
        eligible_db=ft_count["INC"],
        sb_identified=sb_identified, sb_excluded_title=sb_identified - sb_sought, sb_sought=sb_sought,
        sb_not_retrieved=cs_count["NR"], sb_assessed=sb_sought - cs_count["NR"],
        sb_excluded={k: v for k, v in sorted(cs_count.items()) if k.startswith("EC")}, sb_eligible=cs_count["INC"],
        eligible_total=len(studies), below_qa=len(studies) - len(included), included=len(included),
        qa_mean=round(sum(s["qa_total"] for s in included) / len(included), 2),
        qa_min=min(s["qa_total"] for s in included), qa_max=max(s["qa_total"] for s in included),
    )
    write_json(OUT / "prisma_counts.json", prisma)
    write_csv(OUT / "screening_log.csv", log)
    search_log = [dict(date=SEARCH_DATE, source="OpenAlex (title and abstract)", query_or_seed="data/search/openalex_oql.txt",
                       filters="2021-2026; article or conference paper", results=len(records))]
    search_log += [dict(date=s["date"], source=f"OpenAlex citation search ({s['direction']})", query_or_seed=s["seed_openalex_id"],
                        filters=s["filter"], results=s["records_identified"]) for s in seeds]
    write_csv(OUT / "search_log.csv", search_log)

    print("PRISMA 2020 counts")
    for k, v in prisma.items():
        print(f"  {k:18s} {v}")
    return prisma


if __name__ == "__main__":
    main()
