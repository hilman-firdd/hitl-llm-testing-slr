# Replication package: Human-in-the-Loop Software Testing with Large Language Models (SLR)

This repository contains the data and Python scripts behind the article
**"A Systematic Literature Review of Human-in-the-Loop Software Testing with Large Language Models"**
(H. Firdaus, W. Sarasjati, D. Marutho, A. Ilham; Universitas Muhammadiyah Semarang).

With one command you can recompute every number in the PRISMA 2020 flow diagram, the tables of included
studies, roles, and evaluation levels, the quality-threshold sensitivity check, and the supplementary workbook.

| What | Value |
|---|---|
| Search date | 20 October 2026 |
| Sources | OpenAlex (title and abstract), Scopus (TITLE-ABS-KEY), citation searching, a targeted search for practitioner studies, and a completeness search of SBC OpenLib (via OpenAlex, DOI prefix 10.5753) |
| Records identified | 389 from databases (OpenAlex 192, Scopus 197; 88 duplicates) + 192 from citation searching, the practitioner search, and the SBC OpenLib search |
| Studies eligible / included | 42 / 35 (quality threshold 3.0 of 6); 25 read in full text, 10 from abstracts |
| Reporting guideline | SEGRESS (PRISMA 2020 adapted to software engineering); checklist in `protocol/SEGRESS_checklist.md` |

---

## 1. Quick start (about 5 minutes)

You need **Python 3.10 or newer** (check with `python --version`).

```bash
# 1. Get the code
git clone https://github.com/hilman-firdd/hitl-llm-testing-slr.git
cd hitl-llm-testing-slr
#    (or click "Code > Download ZIP" on GitHub and unzip it)

# 2. Create a virtual environment (recommended)
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

# 3. Install the two dependencies
pip install -r requirements.txt

# 4. Run the whole pipeline
python run_all.py
```

Expected end of the output:

```
=== 01_prisma_counts.py ===
  db_identified        389
  ...
  included             35
  qa_mean              4.47
=== 02_synthesis.py ===
Included studies: 35 (mean QA 4.47)
  roles: {'Reviewer': 24, 'Specifier': 18, 'Editor': 9, 'Oracle': 8, 'Explorer': 6, 'Teacher': 5}
...
Done. Results are in outputs/.
```

Step 5 (`06_merge_scopus.py`) needs the raw Scopus export, which is not redistributed (section 6) and is skipped when the file is
absent. The metadata needed for steps 1-4 is already in `data/raw/scopus_records.csv`.

---

## 2. Repository structure

```
hitl-llm-testing-slr/
├── README.md                     this tutorial
├── run_all.py                    runs the pipeline (steps 01 to 04, then 06 and 07)
├── requirements.txt              openpyxl, matplotlib
├── protocol/protocol.md          review protocol (RQs, PICOC, criteria, QA items, search log)
├── data/
│   ├── search/
│   │   ├── openalex_oql.txt      exact OpenAlex query (OQL)
│   │   ├── scopus_blocks.txt     Scopus block queries (#1 LLM, #2 testing, #3 human)
│   │   └── supplementary_oql.txt practitioner search and backward search (21 Oct 2026)
│   ├── raw/
│   │   ├── openalex_records.csv          192 OpenAlex records (metadata only)
│   │   ├── scopus_records.csv            197 Scopus records (metadata only, no abstracts)
│   │   └── citation_search_seeds.csv     citation-search seeds and the supplementary search
│   ├── decisions/
│   │   ├── openalex_title_abstract_screening.csv  one decision per OpenAlex record (I, M, EC1-EC4)
│   │   ├── scopus_title_abstract_screening.csv    one decision per new Scopus record (I, M, EC1-EC4, DUP)
│   │   └── fulltext_eligibility.csv      full-text decisions (INC, NR, EC3-EC6) for all sources
│   ├── extraction/
│   │   ├── extraction_quality.csv        42 eligible studies: coding + QA1-QA6 scores + isolated flag
│   │   ├── fulltext_recoding_log.csv     14 studies re-coded from full text (old vs new, verified)
│   │   └── fulltext_evidence/            short verbatim excerpts per re-coded study (see its README)
│   └── scopus/                           put the raw Scopus CSV export here (step 6; not distributed)
├── scripts/
│   ├── common.py                 paths, loaders, code labels
│   ├── 01_prisma_counts.py
│   ├── 02_synthesis.py
│   ├── 03_prisma_figure.py
│   ├── 04_supplementary_xlsx.py
│   ├── 06_merge_scopus.py
│   └── 07_robustness.py          checklist coverage, venue coverage, CIs, full-text-only counts
└── outputs/                              everything below is generated
    ├── prisma_counts.json
    ├── screening_log.csv
    ├── search_log.csv
    ├── descriptives.json
    ├── fulltext_primary.json
    ├── Supplementary_HITL_SLR.xlsx
    ├── figures/prisma_flow.png
    └── tables/ included_studies.csv, roles_by_activity.csv, evaluation_levels.csv,
                intervention_points.csv, sensitivity_qa.csv,
                checklist_coverage.csv, venue_coverage.csv, proportion_cis.csv, fulltext_primary.csv
```

---

## 3. What each script does

| Step | Script | Reads | Writes | Used in the article |
|---|---|---|---|---|
| 1 | `01_prisma_counts.py` | raw records, decisions, extraction | `prisma_counts.json`, `screening_log.csv`, `search_log.csv` | Figure 1, Section 5.1 |
| 2 | `02_synthesis.py` | extraction | `descriptives.json`, `tables/*.csv` | Tables 6, 7, 8; Sections 5.2-5.4; sensitivity check |
| 3 | `03_prisma_figure.py` | `prisma_counts.json` | `figures/prisma_flow.png` | Figure 1 |
| 4 | `04_supplementary_xlsx.py` | all of the above | `Supplementary_HITL_SLR.xlsx` | Supplementary material |
| 5 | `06_merge_scopus.py` | `data/scopus/*.csv` (your own export) | `scopus_check.json`, `scopus_new_records.csv` | Search update (optional) |
| 6 | `07_robustness.py` | extraction | `tables/checklist_coverage.csv`, `tables/venue_coverage.csv`, `tables/proportion_cis.csv`, `tables/fulltext_primary.csv`, `fulltext_primary.json` | Table 12; Sections 5.2, 5.6, 6.1 (checklist coverage, venue coverage, Wilson CIs, full-text-only counts) |

Each script can also be run on its own, for example `python scripts/02_synthesis.py`.

How the main numbers are derived:

- **Duplicates**: OpenAlex records are compared by normalised title (lower-cased, letters and digits only). Scopus records are
  compared by DOI (or normalised title) within Scopus and then against OpenAlex; one republished paper was flagged by hand (`DUP`).
- **Sought for full text**: title/abstract decision `I` (include) or `M` (unclear).
- **Included**: eligible studies with a quality score of at least 3.0 out of 6 (six items scored 1, 0.5, or 0).
- **Sensitivity**: the role and evaluation counts are recomputed at thresholds 2.5, 3.0, 3.5, and 4.0.

---

## 4. Data dictionary

### Decision codes

| Code | Meaning |
|---|---|
| I | Include to full text |
| M | Unclear from title/abstract, checked in full text |
| EC1 | Not about testing a software artefact |
| EC2 | No LLM or generative model |
| EC3 | Humans only rate outputs for research; no role in the testing workflow |
| EC4 | Secondary study, position/vision paper, short paper, thesis, or preprint |
| EC5 | Duplicate or earlier version of an included study |
| EC6 | Human role not described well enough to code |
| NR | Report not retrieved |
| INC | Eligible |

### `data/extraction/extraction_quality.csv`

| Column | Content |
|---|---|
| key, openalex_id, authors, year, title, venue, vol, no, pages, doi | bibliographic data |
| country | country of the first author's affiliation |
| activity | testing activity (six groups) |
| llm | model(s) reported |
| roles | human roles: Specifier, Explorer, Reviewer, Editor, Oracle, Teacher (separated by `;`) |
| point | when the human steps in: Before, Loop, After |
| human | short description of the human action |
| evaluation | E1 controlled study, E2 field/log data, E3 present but not measured, E4 qualitative |
| eval_detail, finding | evaluation design and main result |
| evidence | F = full text read, A = abstract or publisher page only |
| QA1-QA6 | quality items (see `protocol/protocol.md`) |

---

## 5. Second reviewer

No independent second reviewer coded the studies, so no agreement statistic (Cohen's kappa) is reported. Screening, eligibility,
quality appraisal, and coding were done by the first author with AI assistance (Claude, Anthropic) and checked by the first author
against the sources. The article discusses this single-reviewer design as the main threat to validity.

---

## 6. Checking a Scopus export (optional)

1. Open Scopus > **Advanced document search**.
2. Run each block in `data/search/scopus_blocks.txt` separately (#1, #2, #3).
3. In **Search history**, combine them: `#1 AND #2 AND #3 AND PUBYEAR > 2020 AND PUBYEAR < 2027`.
4. Limit to *Article* and *Conference paper*, language *English*.
5. Export **only the combined set**: Export > CSV > select all information.
6. Save the CSV in `data/scopus/` and run `python scripts/06_merge_scopus.py`.

The Scopus export itself is licensed and is therefore **not included** in this repository; `data/raw/scopus_records.csv` holds only
the bibliographic metadata (EID, DOI, year, source, title, authors) of the 197 records used in the review.
The script checks that the export really is the combined set. At least 80% of records must contain a term from
all three blocks. It then removes records already found in OpenAlex (by DOI or normalised title) and writes the
rest to `outputs/scopus_new_records.csv` with an empty `decision` column for screening.

---

## 7. Reproducing the database search

The OpenAlex query in `data/search/openalex_oql.txt` was run on 20 October 2026 through the OpenAlex query
language (title and abstract fields; 2021-2026; journal articles and conference papers). The Scopus blocks in
`data/search/scopus_blocks.txt` were run the same day and combined as `#1 AND #2 AND #3`. Both indexes grow daily, so a
rerun today will return more records. `data/raw/` holds the exact snapshots used in the review.

---

## 8. Notes and limitations

- Scopus abstracts and the raw Scopus export are not redistributed (licensed); each record can be opened through its DOI, OpenAlex ID, or Scopus EID.
- Quotations from the studies in `data/extraction/fulltext_evidence/` are shortened to under 15 words; the full text is available through the DOI.
- Evidence for 10 of the 35 included studies comes from abstracts or publisher pages (column `evidence` = A). On 26 Oct 2026, 14 studies first coded
  from abstracts were read in full and re-coded; one was excluded (EC3). See `data/extraction/fulltext_recoding_log.csv`.
- The supplementary search (21 Oct 2026) was added after the main screening because the human block missed practice studies;
  its records are reported with citation searching as "other methods".
- The SBC OpenLib completeness search (26 Oct 2026; 41 records, 3 included) is in `data/search/sol_search.txt` and
  `data/decisions/sol_title_abstract_screening.csv`.
- For citation searching, the 101 records excluded by title (or already identified) are reported as counts per
  seed. The 9 reports sought in full are listed individually in `fulltext_eligibility.csv`.
- Screening and extraction were done by the first author with AI assistance (Claude) and checked by the first author. There was no
  independent second reviewer (section 5).

---

## 9. License and citation

- Code: MIT. Data and outputs: CC BY 4.0 (see `LICENSE`). OpenAlex metadata is CC0.
- Please cite the article and this repository (see `CITATION.cff`). The version used in the article is release **v1.0.2**,
  archived on Zenodo (DOI: [10.5281/zenodo.23917944](https://doi.org/10.5281/zenodo.23917944)).

Corresponding author: Hilman Firdaus, Magister Programme of Informatics, Universitas Muhammadiyah Semarang,
19182630014@student.unimus.ac.id
