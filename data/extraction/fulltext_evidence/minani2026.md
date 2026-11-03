# minani2026 — TGenAI for IoT E2E tests (Internet of Things 39, 2026)
Source read: publisher PDF uploaded by first author, 27 pp., full paper; read 26 Oct 2026.
HUMAN ACTIONS: "the HITL first manually constructs a ground-truth (GT) test set" used "as the reference for evaluating the completeness and correctness" (4.1); HITL checks node, interaction, action coverage; "If the generated tests do not meet the required coverage, the prompt is [...]" (4.1); "the HITL uses a manually defined mapping table to translate abstract actions and [...]" (4.1).
TIMING: before (initial prompt, GT), loop (prompt refinement, up to three iterations), after (mapping, adjustments).
EVALUATION: two deployed IoT systems, seven LLMs; RQ4 compares with five human testers who created tests manually (time, missed/extra tests).
OUTCOMES: manual testers 131 and 141 minutes vs TGenAI 57.1 and 57.4 minutes (6.4.4); completeness/correctness 13% to 100% across LLMs.
LLM: GPT-3.5 Turbo, GPT-4 Turbo, GPT-4o, GPT-4o-mini, GPT-5 Nano, Llama 3-70B, Mixtral-8x7B; prompt shown (Fig. 5). THREATS: "7.3. Threats to validity".
PROPOSED CODING: Specifier + Reviewer + Editor + Oracle (now Reviewer, Editor); Before + Loop + After (now After); E1 or E2 (manual-tester baseline vs HITL workflow) -> flag; QA3 -> 1, QA6 -> 1.
