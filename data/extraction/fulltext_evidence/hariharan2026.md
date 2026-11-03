# hariharan2026 — RL-integrated agentic RAG for test case authoring (ICAIC 2026)
Source read: arXiv 2512.06060 (PDF), full paper through Conclusion; read 26 Oct 2026 via WebFetch.
HUMAN ACTIONS: "Quality Engineers retain full operational control" (III.B); "During and after execution, QEs perform defect identification, severity assessment, and tagging." (III.B.a); "QEs maintain complete control over test execution, using the AI-generated test cases as [...]" (IV.C); "Test cases that lead QE teams to discover high-priority or critical defects receive [...]" (IV.D.a); reward R_QE_effectiveness "derived from QE-reported defect detection success and quality ratings" (III.D.1).
TIMING: after execution; feedback enters the learning loop each test cycle.
EVALUATION: three enterprise Apple projects (15,000, 22,000, 18,000 test cases); baselines: earlier agentic RAG, static agentic RAG, "Traditional ML Testing"; participant numbers not reported; durations conflict (12 weeks vs 3 months).
OUTCOMES: accuracy 94.8% -> 97.2%; defect detection 78.3% -> 89.1% (Table I); QE execution time vs manual baseline announced but not reported.
LLM: not named; prompts not reported. THREATS: "B. Challenges and Limitations" only.
PROPOSED CODING: Teacher + Oracle (QEs judge defects and severity); Loop + After; E3 (human decisions feed rewards but are not themselves measured) — check against current E2.
