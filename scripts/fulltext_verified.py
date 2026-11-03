"""Full-text recoding accepted by the first author (verification workbook returned 26 Oct 2026, 21:22 WIB,
plus answers on the three partial agreements). Source proposals: fulltext_proposals.P; evidence: fulltext/<key>.md.
Rows not listed here keep their abstract-based coding."""
from fulltext_proposals import P

def _p(key, **over):
    r, p, e, qa, st, _ = P[key]
    d = dict(roles=r, point=p, evaluation=e, qa=qa, status=st)
    d.update(over)
    return d

FINAL = {
    "wu2026": _p("wu2026", qa=(1, 0.5, 0.5, 1, 0.5, 0)),          # roles and points accepted; QA kept (threats section not read)
    "kitsios2025": _p("kitsios2025"),
    "ardic2026": _p("ardic2026"),
    "rastenis2026": _p("rastenis2026"),
    "santana2025": _p("santana2025"),
    "haldar2025": _p("haldar2025"),
    "paduraru2025": _p("paduraru2025"),
    "aranda2025": _p("aranda2025"),                                 # excluded, EC3
    "ehab2026": _p("ehab2026"),
    "alrabie2025": _p("alrabie2025", roles="Specifier; Reviewer"), # Explorer not accepted
    "chauhan2026": _p("chauhan2026"),
    "su2024": _p("su2024"),
    "minani2026": _p("minani2026"),
    "hariharan2026": _p("hariharan2026", evaluation="E2", qa=(1, 1, 0.5, 0.5, 0.5, 0)),  # roles/points accepted; E2 kept; QA unchanged
}

# Evaluation details and findings re-extracted from the full texts (same sources as fulltext/<key>.md).
DETAIL = {
 "wu2026": ("Within-subject user study (N=12: 6 PhD, 5 MSc, 1 BSc) comparing PALM with a plain LLM chat box on two programs in varied order.",
            "Accuracy on path-comprehension questions was 0.92-1.0 with PALM; completion time was similar (5.43 vs 5.17 min); confidence was higher (4.92 vs 3.00)."),
 "kitsios2025": ("Three-month in-vivo deployment of a bot on three Mozilla repositories (32 pull requests); maintainers judged each proposed test.",
            "Maintainers judged 6 of 11 proposed tests to be valid issue-reproducing tests, and 2 were added to the test suites."),
 "ardic2026": ("Observational study of bachelor students on two testing tasks (Dec 2023-May 2024); screen recordings, think-aloud protocols, and interviews; four interaction strategies compared descriptively.",
            "Strategies yielded similar test quality (mean mutation score 88.96%, no significant differences); students who relied on one-shot generation had to correct outputs and reported lower trust and ownership."),
 "rastenis2026": ("Deployment to all engineers at Uber (Sep 2024-Sep 2025), expert review of nine benchmark subjects against Cursor, and a survey of 29 users.",
            "About 11% of all new tests reviewed and added to Uber's codebase are generated; users explicitly accepted about 44% of IDE-generated tests."),
 "santana2025": ("Semi-structured interviews with 15 testing professionals (4 junior, 5 mid-level, 6 senior); grounded-theory-informed thematic analysis.",
            "Testers define the objective, iteratively refine prompts, and evaluate outputs before integrating them, relying on human oversight because of hallucinations."),
 "haldar2025": ("Two postgraduate capstone cohorts (47 students analysed) who first produced artefacts manually and then with ChatGPT-3.5 or Copilot; analytical questions, sentiment and thematic analysis.",
            "Students found the tools fast and helpful, but manual validation was needed to correct inaccuracies; the tools did not replace manual testing."),
 "paduraru2025": ("Synthetic evaluation with GPT-4-generated variations and a user study with 7 non-technical and 4 technical users who each wrote 10 tests; no control condition.",
            "Users needed on average 4.7 (non-technical) and 2.3 (technical) iterations per step; 1,484 of 1,983 synthetic tests were matched."),
 "ehab2026": ("Industrial deployment across six EDA verification domains (18 specifications, about 95-150 tests), compared with the established manual process; aggregated estimates.",
            "End-to-end QA effort fell by about 40% and about 70% of generated tests were accepted by the responsible QA engineer."),
 "alrabie2025": ("Case study in an Italian public administration: questionnaire with 15 system testers and follow-up interviews with 4; thematic analysis.",
            "Testers valued speed and knowledge support but had to verify answers because of hallucinations, generic responses, and unclear sources."),
 "chauhan2026": ("Defects4J with three runs against AutoTest and EvoSuite+ML; ablation that removes human-in-the-loop feedback; user study with 12 participants assessing 30 test cases each.",
            "Removing human feedback lowered coverage (88.2% to 81.3%), defect localisation (86.9% to 80.1%), and human agreement (0.84 to 0.71); verification time fell by 34% with reasoning traces."),
 "su2024": ("User study with 16 participants (8 per group, paired by experience) doing two-hour exploratory testing of Firefox with the approach or the SoapOperaTG baseline.",
            "The experimental group found 36 new bugs (19 confirmed) against 21 in the control group (Welch's t-test, p = 0.010)."),
 "minani2026": ("Two deployed IoT systems, seven LLMs, and a comparison with five testers who wrote the same tests manually.",
            "Manual test design took 131 and 141 minutes against about 57 minutes with the HITL workflow; completeness and correctness ranged from 13% to 100% across LLMs."),
 "hariharan2026": ("Three enterprise projects (15,000-22,000 test cases each) over about three months, compared with earlier agentic RAG versions; number of quality engineers not reported.",
            "Defect detection rose from 78.3% to 89.1% and generation accuracy from 94.8% to 97.2%; quality engineers' feedback served as the reinforcement-learning reward."),
}
