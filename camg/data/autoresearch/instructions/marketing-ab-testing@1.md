# OpenMLE-fast task

Task ID: `marketing-ab-testing@1`

Native metric: `MarketingConversionLogLossMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2965 bytes)
- `data/sample_submission.csv` (3203220 bytes); columns: ["id", "converted"]
- `data/test.csv` (2892348 bytes); columns: ["id", "test_group", "total_ads", "most_ads_day", "most_ads_hour"]
- `data/train.csv` (12510289 bytes); columns: ["id", "test_group", "total_ads", "most_ads_day", "most_ads_hour", "converted"]

## Public description

Competition: Treatment-aware Conversion Probability Prediction

Problem statement
You are given anonymized user-level data from a large-scale randomized marketing experiment. Each user was assigned to either see ads (treatment) or public service announcements (control). For every user we provide the assignment, their total number of ad exposures, the day of week and the hour of day when their exposures peaked. Your task is to predict the probability that each user converts.

Make your predictions for the held-out test set as calibrated probabilities for the target converted. Lower log loss is better.

Files
- train.csv: Training set with all features and the target.
- test.csv: Test set with the same features as train.csv except the target.
- sample_submission.csv: Example submission file with the correct format and random but valid probabilities.

Columns
All CSVs are comma-separated and UTF-8 encoded.
- id: Row identifier (unique per user). Used to join predictions to users. Do not try to learn from it.
- test_group: Categorical, either ad or psa (treatment assignment).
- total_ads: Integer, total number of ad exposures for the user.
- most_ads_day: Categorical, day of the week when the user saw the most ads.
- most_ads_hour: Integer in [0, 23], hour of day when the user saw the most ads.
- converted: Target column present only in train.csv, boolean-like (1 for converted, 0 for not converted). Submissions must provide a probability for converted.

Task
- Train a model that outputs well-calibrated probabilities P(converted=1 | features) for each row in test.csv.
- This is a binary classification problem with notable class imbalance. Thoughtful preprocessing, feature engineering (e.g., categorical encodings, cyclic time features), and calibration can help.

Submission format
- File must be named however you like but must contain exactly two columns with headers: id, converted
- id must match the ids in test.csv exactly and appear in the same order or at least be a one-to-one match.
- converted must be a floating-point probability in [0, 1].

Evaluation
Primary metric: Log Loss (binary cross-entropy) on converted.
For N rows with ground truth yi ∈ {0, 1} and predicted probabilities pi ∈ (0, 1), log loss is:
LogLoss = - (1/N) * Σ [ yi * log(pi) + (1 - yi) * log(1 - pi) ]
We will clip pi to [1e-15, 1 - 1e-15] for numerical stability before computing the metric. Lower is better.

Rules and notes
- Use any features provided in train.csv and test.csv. The id column is for joining only and should not be used as a predictive signal.
- No additional external data is required. Standard ML techniques (e.g., logistic regression, gradient-boosted trees, calibrated ensembles) are appropriate.
- You may engineer features, but your submission must follow the specified format.

Deliverables to participants
- train.csv
- test.csv
- sample_submission.csv

Good luck, and aim for calibrated probabilities that minimize log loss!
