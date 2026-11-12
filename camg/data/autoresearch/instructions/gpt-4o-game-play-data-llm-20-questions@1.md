# OpenMLE-fast task

Task ID: `gpt-4o-game-play-data-llm-20-questions@1`

Native metric: `TwentyQuestionsAnsweringMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3021 bytes)
- `data/sample_submission.csv` (746345 bytes); columns: ["row_id", "p_yes"]
- `data/test.csv` (16908730 bytes); columns: ["row_id", "keyword", "alts", "question", "context"]
- `data/train.csv` (68387357 bytes); columns: ["row_id", "keyword", "alts", "question", "context", "answer"]

## Public description

Competition: LLM 20 Questions – Answerer Imitation

Problem statement
You are given transcripts from “20 Questions” games played between a Guesser and an Answerer. The hidden keyword is known to the Answerer. Your task is to predict whether the Answerer replies “yes” or “no” to each natural-language question, conditioned on the keyword and optionally the dialogue history.

Why this is challenging
- Free-form questions require world knowledge and subtle reasoning.
- Semantics depend on the hidden keyword and the evolving dialogue context.
- Class imbalance exists between “yes” and “no” answers, so calibrated probabilities matter.

Files
- train.csv: Labeled examples for model development.
- test.csv: Unlabeled examples for final prediction.
- sample_submission.csv: Example submission file with the required format.

Columns
Each row corresponds to one turn (a question asked to the Answerer).
- row_id: Unique identifier for the row. Use this to align predictions.
- keyword: The hidden object the Answerer knows (e.g., “electric toothbrush”).
- alts: Optional alternate forms/plurals of the keyword (may be empty).
- question: The current question at this turn.
- context: Concatenated history of earlier turns in the same game in the format: "Q: <q1> A: <a1> | Q: <q2> A: <a2> | ...". It may be empty for the first turn. Only present for train/test to help modeling; it is not a target.
- answer (train.csv only): The Answerer’s binary response, one of {yes, no}.

Target
- Predict the probability that the Answerer replies “yes” for every row in test.csv.

Submission format
Submit a CSV with exactly these columns:
- row_id: Must match those in test.csv, order arbitrary.
- p_yes: A real number in [0,1] representing P(answer = "yes").

Evaluation
- Metric: Binary Log Loss on p_yes.
  - For each row with ground-truth y ∈ {0,1} (1 for “yes”), and submitted probability p = p_yes, the per-row loss is: -[y * log(p) + (1 - y) * log(1 - p)].
  - The leaderboard score is the mean of the per-row losses over all test rows.
  - Submissions are validated for correct format (row coverage, uniqueness, numeric bounds) and probabilities are safely clipped to avoid numerical issues.

Data preparation notes (applied for you in train/test)
- All available game transcripts are combined.
- Basic cleaning: whitespace stripped; answers lowercased; any non-binary-labeled rows removed.
- Group-aware split: entire games (same underlying game across a file) are kept together in either train or test to prevent leakage from shared history.
- Guesser guesses and round numbers are not included for modeling because they are not necessary to predict the Answerer’s current yes/no.

Modeling tips
- Strong baselines include text encoders (e.g., transformer-based) over keyword + question (+ context). Classical NLP approaches can also perform competitively.
- Handle class imbalance via calibrated probability modeling and appropriate loss (e.g., log loss).

Good luck and have fun!
