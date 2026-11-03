# kitsios2025 — BLAST issue-reproducing tests (ASE 2025)
Source read: arXiv 2509.01616v1 (HTML), https://arxiv.org/html/2509.01616v1; full paper through Conclusion; read 26 Oct 2026 via WebFetch (AI-assisted extraction).
HUMAN ACTIONS: "we ask the maintainer(s) of the repos to provide feedback on the test [...]" (VII-A); tests proposed as PR comments, "we proposed only a single test per PR" (VII-A); developer suggestions led researchers to change bot triggering (VII-B) [researcher action, not system learning].
TIMING: after generation (maintainer feedback on proposed tests).
EVALUATION: in-vivo GitHub bot, 3 months, 3 Mozilla repositories (bugbug, bugbot, libmozdata), 32 PRs analysed; no human comparator.
OUTCOMES: "The developer considered 6/11 (55%) tests as valid issue-reproducing tests", "two of which were successfully included in the projects' test suite" (VII-B).
LLM: gpt-4o (2024-08-06), llama-3.3-70b-versatile, deepseek-r1-distill-llama-70b (VI-D); prompt outline in Fig. 4, full prompt in replication package.
THREATS: "Threats to Validity" in VIII Discussion.
CODING IMPLICATION: Reviewer; After; E2 (unchanged). QA3 and QA6 = 1.
