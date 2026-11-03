"""Step 1. Deduplicate records and compute every number in the PRISMA 2020 flow diagram.

Inputs : data/raw/openalex_records.csv, data/raw/scopus_records.csv, data/raw/citation_search_seeds.csv,
         data/decisions/openalex_title_abstract_screening.csv, data/decisions/scopus_title_abstract_screening.csv,
         data/decisions/fulltext_eligibility.csv, data/extraction/extraction_quality.csv
Outputs: outputs/prisma_counts.json, outputs/screening_log.csv, outputs/search_log.csv

Deduplication
- OpenAlex: normalised title; first occurrence kept.
- Scopus: DOI (or normalised title when there is no DOI) within Scopus, then DOI or normalised title against OpenAlex.
  Records flagged DUP in the Scopus screening file are duplicates found by hand (same paper, different DOI).
"""
from collections import Counter

from common import (CODES, DATA, OUT, QA_THRESHOLD, SEARCH_DATE, load_studies, norm_title,
                    read_csv, write_csv, write_json)


def main():
    oa = read_csv(DATA / "raw" / "openalex_records.csv")
    sc = read_csv(DATA / "raw" / "scopus_records.csv")
    ta_oa = {r["openalex_id"]: r["decision"] for r in read_csv(DATA / "decisions" / "openalex_title_abstract_screening.csv")}
    ta_sc = {r["eid"]: r for r in read_csv(DATA / "decisions" / "scopus_title_abstract_screening.csv")}
    ft_rows = read_csv(DATA / "decisions" / "fulltext_eligibility.csv")
    ft = {(r["source"], r["record_id"]): r["decision"] for r in ft_rows}
    seeds = read_csv(DATA / "raw" / "citation_search_seeds.csv")
    studies = load_studies()

    log = []
    # --- OpenAlex
    seen = {}
    for r in oa:
        k = norm_title(r["title"])
        dup_of = seen.get(k, "")
        seen.setdefault(k, r["openalex_id"])
        d_ta = "" if dup_of else ta_oa[r["openalex_id"]]
        d_ft = ft.get(("openalex", r["openalex_id"]), "") if d_ta in ("I", "M") else ""
        log.append(dict(source="OpenAlex", record_id=r["openalex_id"], doi=r["doi"], year=r["year"], title=r["title"],
                        duplicate_of=dup_of, title_abstract=d_ta, full_text=d_ft,
                        reason=CODES.get(d_ft or d_ta, "duplicate" if dup_of else "")))
    oa_doi = {r["doi"].lower(): r["openalex_id"] for r in oa if r["doi"]}
    oa_title = {norm_title(r["title"]): r["openalex_id"] for r in oa}
    # --- Scopus
    seen_sc, dup_counts = {}, Counter()
    for r in sc:
        doi = r["doi"].lower().strip()
        key = doi or norm_title(r["title"])
        if key in seen_sc:
            dup_of, kind = seen_sc[key], "within Scopus"
        elif (doi and doi in oa_doi) or norm_title(r["title"]) in oa_title:
            dup_of, kind = oa_doi.get(doi) or oa_title.get(norm_title(r["title"])), "in OpenAlex"
        else:
            dup_of, kind = "", ""
        seen_sc.setdefault(key, r["eid"])
        d_ta = ""
        if not dup_of:
            dec = ta_sc[r["eid"]]
            if dec["decision"] == "DUP":
                dup_of, kind = dec["note"].replace("duplicate of ", "").split(" ")[0], "found by hand"
            else:
                d_ta = dec["decision"]
        if dup_of:
            dup_counts[kind] += 1
        d_ft = ft.get(("scopus", r["eid"]), "") if d_ta in ("I", "M") else ""
        log.append(dict(source="Scopus", record_id=r["eid"], doi=r["doi"], year=r["year"], title=r["title"],
                        duplicate_of=dup_of, title_abstract=d_ta, full_text=d_ft,
                        reason=CODES.get(d_ft or d_ta, f"duplicate ({kind})" if dup_of else "")))

    screened = [x for x in log if not x["duplicate_of"]]
    sought = [x for x in screened if x["title_abstract"] in ("I", "M")]
    missing = [x["record_id"] for x in sought if not x["full_text"]]
    assert not missing, f"full-text decision missing for {missing}"

    ta_count = Counter(x["title_abstract"] for x in screened)
    ft_count = Counter(x["full_text"] for x in sought)
    cs = {k[1]: v for k, v in ft.items() if k[0] == "citation_search"}
    cs_count = Counter(cs.values())
    sb_identified = sum(int(s["records_identified"]) for s in seeds)
    included = [s for s in studies if s["qa_total"] >= QA_THRESHOLD]
    assert ft_count["INC"] + cs_count["INC"] == len(studies), "eligible studies and extraction sheet do not match"

    prisma = dict(
        db_identified=len(log), openalex_identified=len(oa), scopus_identified=len(sc),
        duplicates=len(log) - len(screened), duplicates_detail=dict(openalex_internal=sum(1 for x in log if x["source"] == "OpenAlex" and x["duplicate_of"]),
                                                                     **{f"scopus_{k.replace(' ', '_')}": v for k, v in dup_counts.items()}),
        screened=len(screened), screened_openalex=sum(x["source"] == "OpenAlex" for x in screened),
        screened_scopus=sum(x["source"] == "Scopus" for x in screened),
        excluded_ta=sum(v for k, v in ta_count.items() if k.startswith("EC")),
        ta_breakdown=dict(sorted(ta_count.items())),
        sought=len(sought), not_retrieved=ft_count["NR"], assessed=len(sought) - ft_count["NR"],
        excluded_full={k: v for k, v in sorted(ft_count.items()) if k.startswith("EC")},
        eligible_db=ft_count["INC"],
        eligible_by_source=dict(Counter(x["source"] for x in sought if x["full_text"] == "INC")),
        sb_identified=sb_identified, sb_excluded_title=sb_identified - len(cs), sb_sought=len(cs),
        sb_not_retrieved=cs_count["NR"], sb_assessed=len(cs) - cs_count["NR"],
        sb_excluded={k: v for k, v in sorted(cs_count.items()) if k.startswith("EC")}, sb_eligible=cs_count["INC"],
        eligible_total=len(studies), below_qa=len(studies) - len(included), included=len(included),
        qa_mean=round(sum(s["qa_total"] for s in included) / len(included), 2),
        qa_min=min(s["qa_total"] for s in included), qa_max=max(s["qa_total"] for s in included),
    )
    write_json(OUT / "prisma_counts.json", prisma)
    write_csv(OUT / "screening_log.csv", log)
    search_log = [dict(date=SEARCH_DATE, source="OpenAlex (title and abstract)", query_or_seed="data/search/openalex_oql.txt",
                       filters="2021-2026; article or conference paper", results=len(oa)),
                  dict(date=SEARCH_DATE, source="Scopus (TITLE-ABS-KEY)", query_or_seed="data/search/scopus_blocks.txt (#1 AND #2 AND #3)",
                       filters="2021-2026; article or conference paper; English", results=len(sc))]
    search_log += [dict(date=s["date"], source=f"OpenAlex citation search ({s['direction']})", query_or_seed=s["seed_openalex_id"],
                        filters=s["filter"], results=s["records_identified"]) for s in seeds]
    write_csv(OUT / "search_log.csv", search_log)

    print("PRISMA 2020 counts")
    for k, v in prisma.items():
        print(f"  {k:20s} {v}")
    return prisma


if __name__ == "__main__":
    main()
