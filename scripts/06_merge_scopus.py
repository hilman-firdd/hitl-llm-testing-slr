"""Step 6 (optional). Check a Scopus CSV export and merge it with the OpenAlex records.

Input : one or more CSV files in data/scopus/ (Scopus export, 'CSV' format, all fields)
Output: outputs/scopus_check.json      validation summary (block hits, duplicates)
        outputs/scopus_new_records.csv records not already in OpenAlex, ready for title/abstract screening
Why the check: an export of a single block (for example, the LLM block only) looks valid but is wrong.
Every record of a correct export contains at least one term from each of the three blocks.
"""
import csv
import glob
import re

from common import DATA, OUT, norm_title, read_csv, write_csv, write_json

BLOCKS = {
    "llm": [r"large language model", r"\bllms?\b", r"chatgpt", r"gpt-4", r"gpt-3\.5", r"generative ai", r"copilot"],
    "testing": [r"software testing", r"test cases?", r"test generation", r"unit test", r"test scripts?", r"test automation",
                r"test oracles?", r"gui testing", r"test suites?", r"acceptance test"],
    "human": [r"human-in-the-loop", r"human in the loop", r"human oversight", r"human-ai collaboration", r"human-ai interaction",
              r"human feedback", r"developer feedback", r"tester feedback", r"user study", r"manual review", r"human review",
              r"expert review", r"interactive test", r"human evaluation", r"human-cent(?:ered|ric)"],
}


def field(r, *names):
    for n in names:
        for k in r:
            if k.strip().lstrip("﻿").lower() == n.lower():
                return r[k] or ""
    return ""


def main():
    files = sorted(glob.glob(str(DATA / "scopus" / "*.csv")))
    if not files:
        print("No Scopus export in data/scopus/; skipped.")
        return
    rows = []
    for f in files:
        with open(f, newline="", encoding="utf-8-sig") as fh:
            rows += list(csv.DictReader(fh))
    oa = read_csv(DATA / "raw" / "openalex_records.csv")
    oa_doi = {r["doi"].lower() for r in oa if r["doi"]}
    oa_title = {norm_title(r["title"]) for r in oa}

    seen, new, hits = set(), [], {b: 0 for b in BLOCKS}
    all_three = dup_internal = dup_openalex = 0
    for r in rows:
        title, abstract = field(r, "Title"), field(r, "Abstract")
        kw = field(r, "Author Keywords") + " " + field(r, "Index Keywords")
        text = f"{title} {abstract} {kw}".lower()
        ok = {b: any(re.search(p, text) for p in pats) for b, pats in BLOCKS.items()}
        for b in ok:
            hits[b] += ok[b]
        all_three += all(ok.values())
        doi = field(r, "DOI").lower().strip()
        key = doi or norm_title(title)
        if key in seen:
            dup_internal += 1
            continue
        seen.add(key)
        if (doi and doi in oa_doi) or norm_title(title) in oa_title:
            dup_openalex += 1
            continue
        new.append(dict(title=title, year=field(r, "Year"), source=field(r, "Source title"), doc_type=field(r, "Document Type"),
                        doi=doi, eid=field(r, "EID"), hits_all_blocks=all(ok.values()), abstract=abstract, decision=""))

    report = dict(files=[f.split("/")[-1] for f in files], records=len(rows), block_hits=hits, records_matching_all_blocks=all_three,
                  duplicates_within_scopus=dup_internal, already_in_openalex=dup_openalex, new_records=len(new))
    report["looks_valid"] = all_three >= 0.8 * len(rows)
    write_json(OUT / "scopus_check.json", report)
    write_csv(OUT / "scopus_new_records.csv", new,
              ["title", "year", "source", "doc_type", "doi", "eid", "hits_all_blocks", "abstract", "decision"])
    for k, v in report.items():
        print(f"  {k}: {v}")
    if not report["looks_valid"]:
        print("WARNING: fewer than 80% of records contain all three blocks. "
              "Export the combined set (#1 AND #2 AND #3), not a single block.")


if __name__ == "__main__":
    main()
