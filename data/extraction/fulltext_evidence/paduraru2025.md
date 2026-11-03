# paduraru2025 — Agentic AI for BDD testing (ICAART 2025)
Source read: publisher PDF, https://scitepress.org/Papers/2025/133744/133744.pdf; full paper through Conclusion; read 26 Oct 2026 via WebFetch.
HUMAN ACTIONS: "with the human giving instructions in natural language" (Intro); "the user can edit the generated response if the LLM suggestions are incorrect" (Intro); "with the user in full control: rewinding, editing steps" (4.1); "the error is reported to the user and they are asked for help [...]" (4.2); "The user can confirm, edit or add missing parameters" (Fig. 3); "until the user's final approval" (5.3).
TIMING: before (instructions/user story), loop (iterations per step), after (final approval).
EVALUATION: user study with 7 non-technical designers/artists and 4 software engineers, each wrote 10 tests, no control condition (5.3); synthetic evaluation with GPT-4 variations (5.2).
OUTCOMES: average 4.7 iterations per step (non-technical) vs 2.3 (technical) (5.3); 1484 of 1983 synthetic tests matched (Table 2).
LLM: fine-tuned Llama 3.1 8B; GPT-4 for synthetic data; prompt templates in Listings 3-5.
THREATS: "5.4 Limitations and Technical Challenges" (no dedicated threats section).
CODING IMPLICATION: Specifier + Reviewer + Editor (currently Reviewer only?); Before + Loop + After (currently After only); E2 (human iterations measured) instead of E3.
