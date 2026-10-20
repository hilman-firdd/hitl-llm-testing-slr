# Replication package: Human-in-the-Loop Software Testing with Large Language Models (SLR)

This repository contains the data and Python scripts behind the article
**"A Systematic Literature Review of Human-in-the-Loop Software Testing with Large Language Models"**
(H. Firdaus, W. Sarasjati, D. Marutho, A. Ilham; Universitas Muhammadiyah Semarang).

With one command you can recompute every number in the PRISMA 2020 flow diagram, the tables of included
studies, roles, and evaluation levels, the quality-threshold sensitivity check, and the supplementary workbook.

| What | Value |
|---|---|
| Search date | 20 October 2026 |
| Sources | OpenAlex (title and abstract) plus backward and forward citation searching; Scopus pending |
| Records identified | 192 (database) + 110 (citation searching) |
| Studies eligible / included | 22 / 20 (quality threshold 3.0 of 6) |
| Reporting guideline | PRISMA 2020 |

---

## 1. Quick start (about 5 minutes)

You need **Python 3.10 or newer** (check with `python --version`).

```bash
# 1. Get the code
git clone https://github.com/<username>/hitl-llm-testing-slr.git
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
  db_identified      192
  ...
  included           20
  qa_mean            4.42
=== 02_synthesis.py ===
Included studies: 20 (mean QA 4.42)
  roles: {'Reviewer': 11, 'Specifier': 6, 'Explorer': 5, 'Oracle': 5, 'Teacher': 4, 'Editor': 3}
...
Done. Results are in outputs/.
```

Steps 5 and 6 print "skipped" until their input files exist (see sections 5 and 6).

---

## 2. Repository structure

```
hitl-llm-testing-slr/
├── README.md                     this tutorial
├── run_all.py                    runs steps 01 to 06
├── requirements.txt              openpyxl, matplotlib
├── protocol/protocol.md          review protocol (RQs, PICOC, criteria, QA items, search log)
├── data/
│   ├── search/
│   │   ├── openalex_oql.txt      exact OpenAlex query (OQL)
│   │   └── scopus_blocks.txt     Scopus block queries (#1 LLM, #2 testing, #3 human)
│   ├── raw/
│   │   ├── openalex_records.csv          192 records returned by the search (metadata only)
│   │   └── citation_search_seeds.csv     5 seeds used for citation searching
│   ├── decisions/
│   │   ├── title_abstract_screening.csv  one decision per record (I, M, EC1-EC4)
│   │   └── fulltext_eligibility.csv      full-text decisions (INC, NR, EC3-EC6) for both sources
│   ├── extraction/
│   │   └── extraction_quality.csv        22 eligible studies: coding + QA1-QA6 scores
│   └── scopus/                           put the Scopus CSV export here (step 6)
├── agreement/                            put the second-reviewer workbook here (step 5)
├── scripts/
│   ├── common.py                 paths, loaders, code labels
│   ├── 01_prisma_counts.py
│   ├── 02_synthesis.py
│   ├── 03_prisma_figure.py
│   ├── 04_supplementary_xlsx.py
│   ├── 05_kappa.py
│   └── 06_merge_scopus.py
└── outputs/                              everything below is generated
    ├── prisma_counts.json
    ├── screening_log.csv
    ├── search_log.csv
    ├── descriptives.json
    ├── Supplementary_HITL_SLR.xlsx
    ├── figures/prisma_flow.png
    └── tables/ included_studies.csv, roles_by_activity.csv, evaluation_levels.csv,
                intervention_points.csv, sensitivity_qa.csv
```

---

## 3. What each script does

| Step | Script | Reads | Writes | Used in the article |
|---|---|---|---|---|
| 1 | `01_prisma_counts.py` | raw records, decisions, extraction | `prisma_counts.json`, `screening_log.csv`, `search_log.csv` | Figure 1, Section 3.1 |
| 2 | `02_synthesis.py` | extraction | `descriptives.json`, `tables/*.csv` | Tables 5, 6, 7; Sections 3.2-3.4; sensitivity check |
| 3 | `03_prisma_figure.py` | `prisma_counts.json` | `figures/prisma_flow.png` | Figure 1 |
| 4 | `04_supplementary_xlsx.py` | all of the above | `Supplementary_HITL_SLR.xlsx` | Supplementary material |
| 5 | `05_kappa.py` | `agreement/Interrater_Agreement_HITL_SLR.xlsx` | `kappa.json` | Sections 2.5 and 2.7 |
| 6 | `06_merge_scopus.py` | `data/scopus/*.csv` | `scopus_check.json`, `scopus_new_records.csv` | Search update |

Each script can also be run on its own, for example `python scripts/02_synthesis.py`.

How the main numbers are derived:

- **Duplicates**: titles are lower-cased and stripped of everything except letters and digits; the first occurrence is kept.
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

## 5. Inter-rater agreement (Cohen's kappa)

A second author screened a 20% stratified random sample (38 of 188 records, seed 20261020) and independently
coded the 20 included studies in an Excel workbook. The workbook computes kappa with formulas.
To check it with Python:

1. Save the returned workbook as `agreement/Interrater_Agreement_HITL_SLR.xlsx`.
2. Run `python scripts/05_kappa.py`.
3. Compare `outputs/kappa.json` with the `Kappa` sheet; the values must be identical.

Interpretation follows Landis and Koch (1977): 0.61-0.80 substantial, above 0.80 almost perfect.

---

## 6. Adding the Scopus search

1. Open Scopus > **Advanced document search**.
2. Run each block in `data/search/scopus_blocks.txt` separately (#1, #2, #3).
3. In **Search history**, combine them: `#1 AND #2 AND #3 AND PUBYEAR > 2020 AND PUBYEAR < 2027`.
4. Limit to *Article* and *Conference paper*, language *English*.
5. Export **only the combined set**: Export > CSV > select all information.
6. Save the CSV in `data/scopus/` and run `python scripts/06_merge_scopus.py`.

The script checks that the export really is the combined set. At least 80% of records must contain a term from
all three blocks. It then removes records already found in OpenAlex (by DOI or normalised title) and writes the
rest to `outputs/scopus_new_records.csv` with an empty `decision` column for screening.

---

## 7. Reproducing the database search

The OpenAlex query in `data/search/openalex_oql.txt` was run on 20 October 2026 through the OpenAlex query
language (title and abstract fields; 2021-2026; journal articles and conference papers). OpenAlex grows daily, so a
rerun today will return more records. `data/raw/openalex_records.csv` is the exact snapshot used in the review.

---

## 8. Notes and limitations

- Abstracts are not redistributed; each record can be opened through its DOI or OpenAlex ID.
- For citation searching, the 101 records excluded by title (or already identified) are reported as counts per
  seed. The 9 reports sought in full are listed individually in `fulltext_eligibility.csv`.
- Screening and extraction were done by the first author. Agreement with a second author is reported through step 5.

---

## 9. License and citation

- Code: MIT. Data and outputs: CC BY 4.0 (see `LICENSE`). OpenAlex metadata is CC0.
- Please cite the article and this repository (see `CITATION.cff`). To get a permanent DOI, connect the
  repository to Zenodo and create a GitHub release.

Corresponding author: Hilman Firdaus, Magister Programme of Informatics, Universitas Muhammadiyah Semarang,
19182630014@student.unimus.ac.id
