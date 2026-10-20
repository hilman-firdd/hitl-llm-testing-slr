# SLR Protocol: Human-in-the-Loop LLM-Based Software Testing

Version 1, 20 Oct 2026. Target: JUTIF (Sinta 2), English. Designed to Q2-Q3 standard.

## Title
A Systematic Literature Review of Human-in-the-Loop Software Testing with Large Language Models (12 words; JUTIF asks for no subtitle)

## Working definition
Human-in-the-loop (HITL) LLM-based testing: an LLM produces or transforms a testing artefact (test case, scenario, script, assertion/oracle, test report), and a human performs at least one action inside that workflow that shapes or gates the artefact. Actions: (a) supplies or refines the input (requirement, intention, prompt), (b) reviews, accepts or rejects output, (c) edits or repairs output, (d) gives feedback the system uses in a loop, (e) makes the final verdict (e.g., oracle or bug decision). Humans who only rate outputs afterwards for research measurement are NOT in the loop.

## Research questions
- RQ1 (where and who): In which testing activities are humans involved in LLM-based testing, and which roles do they take?
- RQ2 (how): How is the human-LLM interaction designed: when does the human step in, in what form, and how much control does the human keep?
- RQ3 (evidence): How do studies evaluate the human contribution, and what do they report about its effect on test quality and effort?
- RQ4 (gaps): Which challenges and open problems do the studies report?

## PICOC
- Population: software testing activities and the people who perform them (testers, QA engineers, developers).
- Intervention: LLM-based testing approaches in which a human takes part in the workflow.
- Comparison: fully automated LLM pipelines or manual testing, when reported (not required).
- Outcome: human roles, interaction designs, evaluation designs, reported effects, challenges.
- Context: academic and industrial studies, 2021-2026.

## Inclusion criteria
- IC1 Primary study that proposes or evaluates an LLM-based approach for a software testing activity.
- IC2 A human takes at least one in-the-loop action (definition above), or the study empirically investigates people using LLM-based testing support.
- IC3 Peer-reviewed journal article or conference paper, English, published 2021-2026.

## Exclusion criteria
- EC1 Not about testing a software artefact (e.g., code generation only, LLM benchmark evaluation, non-software domains).
- EC2 No LLM or generative model in the approach.
- EC3 Humans appear only as research evaluators or annotators, with no role in the testing workflow.
- EC4 Secondary study, position or vision paper without design or evaluation, editorial, extended abstract (2 pages or less), thesis, preprint.
- EC5 Duplicate or earlier version of an included study (most complete version kept).
- EC6 Full text and abstract give too little detail to identify the human role.

## Quality assessment (1 / 0.5 / 0; pass threshold >= 3 of 6)
- QA1 Aim and testing activity clearly stated.
- QA2 Human role described well enough to replicate (who, when, which action).
- QA3 LLM setup reported (model and version, prompting).
- QA4 Evaluation with defined data and metrics.
- QA5 Human contribution isolated (with vs without human, or human decisions/effort measured).
- QA6 Threats to validity or limitations discussed.

## Data extraction
id, authors, year, title, venue, doi, country (first author's affiliation country), testing activity, LLM(s), human role(s), interaction point (before / during loop / after), control level, evaluation design, human contribution measured (Y/N), key finding, challenges, source of evidence (full text / abstract), QA scores.

## Synthesis
Thematic synthesis (Thomas & Harden 2008). Descriptive codes for role, activity, interaction point and evaluation design; counts per code; cross-tabulation role x activity.

## Sources and search strings
1. OpenAlex (title and abstract), run 20 Oct 2026 via OpenAlex MCP.
2. Scopus (TITLE-ABS-KEY), export by author.
3. Backward/forward snowballing of included studies (Wohlin 2014), recorded as "other methods".

### OpenAlex OQL
works where title-abstract has (("large language model*" or LLM or LLMs or ChatGPT or "GPT-4" or "GPT-3.5" or "generative AI" or Copilot) and ("software testing" or "test case*" or "test generation" or "unit test*" or "test script*" or "test automation" or "test oracle*" or "GUI testing" or "test suite*" or "acceptance test*") and ("human-in-the-loop" or "human in the loop" or "human oversight" or "human-AI collaboration" or "human-AI interaction" or "human feedback" or "developer feedback" or "tester feedback" or "user study" or "manual review" or "human review" or "expert review" or "interactive test*" or "human evaluation" or "human-centered" or "human-centric")) and published since 2021 and type is (article or conference-paper)

### Scopus
See data/search/scopus_blocks.txt (three block queries combined in Scopus search history).

## String tuning log
- Adding "human-AI" (bare) raised results to 448 with mostly off-topic records (keyword matching). Rejected.
- Adding practitioner*, interactive, conversational, collaborative raised results to 521-685, mostly LLM chat pipelines without humans or medical papers. Rejected.
- Keyword-tag matching (title-abstract-keywords) gave 263; text-only matching (title-abstract) gave 192 with better precision. Text-only adopted.

## Scopus query, revised 20 Oct 2026
The full query was truncated at 500 characters in the user's Scopus interface. It was split into two queries (A: 448 chars, B: 436 chars) with identical LLM and testing blocks; the human block is divided between them, so A OR B equals the full query. Wildcards make the Scopus version slightly broader than the OpenAlex string (llm*, gpt*, "software test*", "test generat*", "test automat*", "GUI test*", "human-AI", "human-cent*"). Filters set in the Scopus interface: document type Article and Conference paper, language English. Superseded by the block approach in data/search/scopus_blocks.txt.

## Scopus export check, 20 Oct 2026 (attempt with split queries A/B)
Two CSVs received (80 and 86 records; 112 unique). Validation against the three blocks: 112 contain an LLM term, 24 a testing term, 11 a human term, only 1 all three; none of the 20 eligible studies appear (e.g., Fakhoury et al. 2024 TSE, which matches query B). Conclusion: the executed query was not the intended one (likely truncated or mangled). Exports kept in scopus_raw/ but NOT used. Next attempt: three block queries combined in Scopus search history (#1 AND #2 AND #3), exporting only the combined set.

## Scopus, third attempt plan (20 Oct 2026)
Three block queries (#1 LLM, #2 testing, #3 human; each under 400 characters) are run separately in Scopus Advanced search, then combined in Search history as `#1 AND #2 AND #3 AND PUBYEAR > 2020 AND PUBYEAR < 2027`, limited to Article and Conference paper, English. Only the combined set is exported. See data/search/scopus_blocks.txt in the replication package; scripts/06_merge_scopus.py validates the export (every record must hit all three blocks) before merging.
