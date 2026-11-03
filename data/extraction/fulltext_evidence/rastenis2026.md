# rastenis2026 — AutoCover at Uber (ICSE-SEIP 2026)
Source read: author copy, https://homes.cs.washington.edu/~rjust/publ/auto_cover_icse_2026.pdf; full paper through Conclusions; read 26 Oct 2026 via WebFetch.
HUMAN ACTIONS: "IDE for human-in-the-loop generation that captures intent and provides rapid test repair" (Abstract); "generating merge requests with new tests and routing them to owning teams for review" (1); IDE actions emitted to AutoCover, users "have the ability to cancel and insert test case" (6.4); "explicitly accepted by users" (4.3.2).
TIMING: before (IDE intent capture), after (merge-request review, IDE acceptance); mid-generation interjection only a requested feature (4.4.2).
EVALUATION: deployment to all Uber engineers (Sep 2024-Sep 2025); expert review by two PhD experts vs Cursor-0.46.8 on nine subjects (4.2.1); survey of 29 users (23 active, 6 inactive) (4.4.1).
OUTCOMES: "about 11% of all new tests that are reviewed and added to Uber's codebase"; IDE tests "explicitly accepted by users at a rate of about 44%" (4.3.2); survey 83% vs 40% agree productivity improves.
LLM: GPT 5 Thinking, GPT 4.1, Claude 4 Sonnet (Table 2); prompts not reported in full.
THREATS: "4.5 Threats to Validity".
CODING IMPLICATION: Specifier + Reviewer (currently Reviewer only?); Before + After; E2.
