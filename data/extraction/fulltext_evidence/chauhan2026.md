# chauhan2026 — LLM-dsWF (JESTR 19(2), 2026)
Source read: publisher PDF uploaded by first author, 8 pp., full paper; read 26 Oct 2026.
HUMAN ACTIONS: "the test engineer to pose queries regarding the test reasoning or ... alter [...]" (3, Human Feedback Loop); algorithm step "If human review enabled: a. Collect expert corrections b. Update prompt constraints".
TIMING: loop (feedback updates prompts), after (validation).
EVALUATION: Defects4J, three runs, vs AutoTest and EvoSuite+ML; ablation including "(i) eliminating human-in-the-loop feedback" (Table 2); user study with 12 participants (7 industry, 5 academic), each assessed 30 test cases.
OUTCOMES: Full vs without human feedback: coverage 88.2 vs 81.3, defect localization 86.9 vs 80.1, human agreement rate 0.84 vs 0.71 (Table 2); "34% reduction in the average verification time" attributed to structured reasoning traces.
LLM: not named ("model M"). THREATS: no dedicated section; qualitative disagreement analysis only.
CAUTION: internal inconsistencies (says no gradient training, then gives gradient-based correction equation 10); user-study design described briefly.
PROPOSED CODING: Teacher + Reviewer; Loop + After; E1 unchanged. IMPORTANT: the ablation removes human feedback, so this is a second study that estimates the effect of human feedback (claim "only TiCoder isolated" must change, with a quality caveat).
