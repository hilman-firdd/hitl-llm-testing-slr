# aranda2025 — Image2Test (SAST 2025)
Source read: publisher PDF, https://sol.sbc.org.br/index.php/sast/article/download/36887/36673; full paper through Concluding Remarks; read 26 Oct 2026 via WebFetch.
HUMAN ACTIONS: "The researcher's role is limited to capturing and defining the test objectives." (3.2); "three different researchers elected objectives for each test" (3.2); "all tests were inspected by the authors to ensure they were executable" (3.2); "we accepted all ChatGPT outputs without filtering or regenerating low-quality responses" (3.2); 18 professionals and students rated blinded human vs ChatGPT tests (3.3).
TIMING: researchers before generation (objectives); evaluators after (research survey).
EVALUATION: blinded side-by-side survey, 18 raters (50% industry), completeness and clarity; similarity metrics.
LLM: GPT-4o via API, default settings; full prompt in Listing 2.
THREATS: "5 Threats to Validity".
CODING IMPLICATION: humans act only as researchers and research raters, no tester in the workflow -> candidate for EC3 (exclusion). Currently included (QA 3.0, E3). Flag for decision.
