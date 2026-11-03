"""Proposed coding changes after full-text reading (26 Oct 2026). AI-assisted extraction: every row must be
verified by the first author before it replaces library.STUDIES. Evidence is in fulltext/<key>.md."""
P = {  # key: (roles, point, evaluation, qa tuple, status, note)
 "wu2026":       ("Specifier; Reviewer; Editor", "Before; Loop; After", "E1", (1, 1, 0.5, 1, 0.5, 1), "INC", "user supplies program and loop bound, edits prompt, inspects and updates tests"),
 "kitsios2025":  ("Reviewer", "After", "E2", (1, 1, 1, 1, 0.5, 1), "INC", "maintainers judge proposed tests on PRs; 6/11 valid"),
 "ardic2026":    ("Specifier; Explorer; Reviewer; Editor", "Before; Loop; After", "E2", (1, 1, 1, 1, 0.5, 1), "INC", "students prompt, take test ideas, critique and modify outputs"),
 "rastenis2026": ("Specifier; Reviewer; Editor", "Before; After", "E2", (1, 1, 0.5, 1, 0.5, 1), "INC", "IDE intent capture and repair; MR review; mid-generation input only requested"),
 "santana2025":  ("Specifier; Reviewer", "Before; Loop; After", "E4", (1, 1, 0.5, 1, 0.5, 1), "INC", "15 interviews; prompt, refine, evaluate before integrating"),
 "haldar2025":   ("Specifier; Reviewer", "Before; Loop; After", "E1", (1, 1, 1, 1, 0.5, 1), "INC", "E1 questionable: sequential manual-then-AI on same students"),
 "paduraru2025": ("Specifier; Reviewer; Editor", "Before; Loop; After", "E2", (1, 1, 1, 0.5, 1, 0.5), "INC", "users confirm/edit each step; iterations per step measured (4.7 vs 2.3)"),
 "aranda2025":   ("", "", "", (1, 0.5, 1, 1, 0, 1), "EC3", "researchers set objectives and accepted all outputs; humans only research raters"),
 "ehab2026":     ("Specifier; Reviewer; Editor", "Before; Loop; After", "E2", (1, 1, 0.5, 1, 0.5, 1), "INC", "engineers give spec, confirm at gates, validate and correct; 40% effort, 70% accepted"),
 "alrabie2025":  ("Specifier; Explorer; Reviewer", "Before; After", "E4", (1, 1, 0, 1, 0, 0.5), "INC", "15 testers survey + 4 interviews; verify outputs; rating feedback designed"),
 "chauhan2026":  ("Reviewer; Teacher", "Loop; After", "E1", (1, 1, 0, 1, 1, 0.5), "INC", "ablation without human feedback: coverage 88.2 vs 81.3; internal inconsistencies"),
 "su2024":       ("Explorer; Oracle", "After", "E1", (1, 1, 0, 1, 1, 1), "INC", "unchanged coding; 16 participants, control group"),
 "minani2026":   ("Specifier; Reviewer; Editor; Oracle", "Before; Loop; After", "E2", (1, 1, 1, 1, 0.5, 1), "INC", "HITL builds ground truth, refines prompt, maps to executable tests; 5 manual testers baseline"),
 "hariharan2026":("Oracle; Teacher", "Loop; After", "E3", (1, 1, 0, 0.5, 0, 0.5), "INC", "QEs judge defects; feedback becomes RL reward; human decisions not measured"),
}
