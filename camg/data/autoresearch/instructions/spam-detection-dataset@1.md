# OpenMLE-fast task

Task ID: `spam-detection-dataset@1`

Native metric: `SpamDetectionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2368 bytes)
- `data/sample_submission.csv` (37818 bytes); columns: ["id", "is_spam"]
- `data/test.csv` (131460 bytes); columns: ["id", "num_links", "num_words", "has_offer", "sender_score", "all_caps"]
- `data/train.csv` (558048 bytes); columns: ["id", "num_links", "num_words", "has_offer", "sender_score", "all_caps", "is_spam"]

## Public description

Title: Spam Probability Estimation (PR-AUC)

Problem statement
You are given a tabular dataset of emails with engineered features. Your task is to build a model that estimates, for each email, the probability that it is spam. Submissions are ranked by how well the predicted probabilities rank true spam messages ahead of legitimate mail.

Files provided after running prepare.py
- train.csv: Training data with all feature columns plus the target column is_spam and an id column.
- test.csv: Test data with the same feature columns and id, but without the target.
- sample_submission.csv: A sample submission file with columns id and is_spam, where is_spam contains example probability scores.

Data description
Each row corresponds to one email. Columns in train.csv and test.csv:
- id: Unique integer identifier for the email.
- num_links (int): Number of hyperlinks detected in the email body.
- num_words (int): Total tokenized word count of the email.
- has_offer (0/1): Whether an “offer”-like keyword was detected.
- sender_score (float in [0, 1]): Reputation score of the sender (higher is better).
- all_caps (0/1): Whether the subject/body is mostly uppercase.
- is_spam (0/1): Target label indicating whether the email is spam. Present only in train.csv.

Evaluation
- Metric: Average Precision (AP), i.e., area under the Precision–Recall curve for the positive class (spam = 1).
- Submission format: A CSV with two columns: id and is_spam, where is_spam is your predicted probability that the email is spam (values in [0, 1]). All ids from test.csv must be present exactly once with no extras.
- Handling of values: Predictions are treated as continuous scores. The evaluator validates the submission format and computes AP in a numerically stable way.

Recommended modeling considerations
- Class imbalance: The positive rate is around 9%, so consider class weighting, appropriate regularization, and calibration.
- Features: Standardize numeric features (num_links, num_words, sender_score). Keep has_offer and all_caps as binary indicators.
- Reproducibility: Fix random seeds in your pipeline for consistent results.

Data split
- A single stratified split is used to create train.csv and test.csv from the full dataset.

Final data files
- train.csv, test.csv, sample_submission.csv

Good luck building a well-calibrated, high-AP spam detector!
