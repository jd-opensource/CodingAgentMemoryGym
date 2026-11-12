# OpenMLE-fast task

Task ID: `spam-detection-dataset@2`

Native metric: `SpamDetectionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2512 bytes)
- `data/sample_submission.csv` (37775 bytes); columns: ["id", "is_spam"]
- `data/test.csv` (131460 bytes); columns: ["id", "num_links", "num_words", "has_offer", "sender_score", "all_caps"]
- `data/train.csv` (558048 bytes); columns: ["id", "num_links", "num_words", "has_offer", "sender_score", "all_caps", "is_spam"]

## Public description

Well-Calibrated Spam Probability Forecasting (LogLoss)

Problem statement
You are given tabular features extracted from emails. Your task is to build a model that predicts, for each message, the probability that it is spam. Submissions must provide a probability for every test email. The leaderboard is ranked by binary cross-entropy (log loss), which rewards accurate and well-calibrated probabilities.

Files
- train.csv: Training set with features, an id column, and the binary target is_spam.
- test.csv: Test set with the same features and an id column, but without is_spam.
- sample_submission.csv: Example submission file with id and a probability column named is_spam.

Data schema
- id: Unique integer identifier for each email.
- Features (per row):
  - num_links: Number of hyperlinks in the email (integer >= 0).
  - num_words: Total word count of the email (integer >= 0).
  - has_offer: Indicator whether typical promotional words appear (0/1).
  - sender_score: Sender reputation score in [0, 1].
  - all_caps: Indicator whether the subject/body is largely uppercase (0/1).
- Target (train.csv only):
  - is_spam: 1 if the email is spam, 0 otherwise.

Task
- Train any model(s) you like using train.csv.
- For each id in test.csv, output a single probability in [0, 1] under the column name is_spam.
- Save your predictions in a CSV with exactly two columns: id, is_spam. The order of rows does not matter, but ids must be unique and match test.csv exactly.

Evaluation metric
- Primary metric: Binary cross-entropy (log loss) on the test set.
- Definition: For N test rows with true labels y_i ∈ {0,1} and submitted probabilities p_i ∈ [0,1],
  LogLoss = - (1/N) * Σ [ y_i * log(p_i) + (1 - y_i) * log(1 - p_i) ]
- Numerical stability: p_i values are clipped to [1e-15, 1 - 1e-15] during evaluation to avoid infinities.
- Lower is better.

Split & reproducibility
- A single stratified split is used to create train/test, preserving the class distribution. The split is deterministic.
- Participants are free to use any internal validation or cross-validation within the training set for modeling and calibration.

Notes and tips
- The dataset is moderately imbalanced; probabilistic calibration (e.g., Platt scaling, isotonic regression) can improve log loss.
- Standardizing numeric features and keeping binary indicators as-is is a reasonable baseline.
- Reasonable starter models include regularized logistic regression, tree ensembles, and gradient boosting; consider class weighting.
